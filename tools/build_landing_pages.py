#!/usr/bin/env python3
"""Generate static, service-matched landing pages and Google Ads asset suggestions.

Source of truth:
  tools/services.json
  tools/landing_template.html

Run: python3 tools/build_landing_pages.py
The generated HTML is committed, so Vercel does not need a build step.
"""
from __future__ import annotations

import html
import json
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
BASE_URL = "https://adslanding-law.vercel.app"
CONFIG = json.loads((TOOLS / "services.json").read_text(encoding="utf-8"))
TEMPLATE = (TOOLS / "landing_template.html").read_text(encoding="utf-8")
BRAND = CONFIG["brand"]
SERVICES = CONFIG["services"]
ORDER = CONFIG["service_order"]


def e(value: object) -> str:
    return html.escape(str(value), quote=True)


def wa(message: str) -> str:
    return "https://wa.me/" + BRAND["whatsapp_number"] + "?text=" + quote(message, safe="")


def canonical(key: str, page: dict) -> str:
    return BASE_URL + ("/" if key == "general" else "/" + page["file"])


def render_topic_cards(key: str, page: dict) -> str:
    cards = []
    for i, item in enumerate(page.get("topic_cards", []), 1):
        msg_url = e(wa(item["message"]))
        details = ""
        if item.get("href"):
            details = '<a class="topic-details" href="' + e(item["href"]) + '">تفاصيل الخدمة</a>'
        cards.append(
            '<article class="topic-card"><div class="topic-card-top">'
            '<span class="topic-index">' + f"{i:02d}" + '</span><span class="topic-mark" aria-hidden="true"></span></div>'
            '<h3>' + e(item["title"]) + '</h3><p>' + e(item["description"]) + '</p>'
            '<div class="topic-actions"><a class="topic-wa" href="' + msg_url + '" target="_blank" '
            'rel="noopener noreferrer" data-contact="whatsapp" data-service="' + e(key)
            + '" data-position="topic_card">اسأل عبر واتساب</a>' + details + '</div></article>'
        )
    return "".join(cards)


def render_prep(page: dict) -> str:
    prep = page.get("prep")
    if not prep:
        return ""
    items = "".join("<li>" + e(item) + "</li>" for item in prep.get("items", []))
    return (
        '<section class="prep-section" aria-labelledby="prep-title"><div class="prep-inner">'
        '<div class="prep-intro"><p class="kicker">قبل التواصل</p><h2 id="prep-title">' + e(prep["title"]) + '</h2>'
        '<p>' + e(prep.get("intro", "")) + '</p></div><ol class="prep-list">' + items + '</ol>'
        '</div></section>'
    )


def render_steps(page: dict) -> str:
    steps = []
    for i, item in enumerate(page.get("steps", []), 1):
        steps.append(
            '<article class="step-card"><span class="step-number">' + f"{i:02d}" + '</span>'
            '<h3>' + e(item["title"]) + '</h3><p>' + e(item["text"]) + '</p></article>'
        )
    return "".join(steps)


def render_page(key: str, page: dict) -> str:
    trust_items = "".join("<li>" + e(item) + "</li>" for item in page.get(
        "trust_items", ["مراعاة سرية المعلومات", "توضيح الخطوات والمستندات", "الأتعاب تُحدد قبل البدء"]
    ))
    faqs = []
    for question, answer in page["faqs"]:
        faqs.append('<details class="faq-item"><summary>' + e(question)
                    + '</summary><p>' + e(answer) + '</p></details>')
    replacements = {
        "@@TITLE@@": e(page["title"]),
        "@@DESCRIPTION@@": e(page["description"]),
        "@@CANONICAL@@": e(canonical(key, page)),
        "@@MAP_URL@@": e(BRAND["map_url"]),
        "@@GTM_ID@@": e(BRAND["gtm_id"]),
        "@@PHONE_DISPLAY@@": e(BRAND["phone_display"]),
        "@@SERVICE@@": e(key),
        "@@EYEBROW@@": e(page["eyebrow"]),
        "@@H1@@": e(page["h1"]),
        "@@SUBTITLE@@": e(page["subtitle"]),
        "@@INTRO@@": e(page["intro"]),
        "@@CALL_TEXT@@": e(page["call_text"]),
        "@@WHATSAPP_TEXT@@": e(page["whatsapp_text"]),
        "@@MAIN_WA_URL@@": e(wa(page["main_message"])),
        "@@VISUAL_TITLE@@": e(page["label"]),
        "@@VISUAL_COPY@@": e(page.get("visual_copy", "نوضح الخطوات والمستندات المطلوبة بحسب طبيعة طلبك.")),
        "@@TRUST_ITEMS@@": trust_items,
        "@@TOPICS_HEADING@@": e(page.get("topics_heading", "اختر موضوع استفسارك")),
        "@@TOPICS_INTRO@@": e(page.get("topics_intro", "اختر الموضوع الأقرب إلى طلبك لبدء رسالة واتساب مخصصة.")),
        "@@TOPIC_CARDS@@": render_topic_cards(key, page),
        "@@PREP_SECTION@@": render_prep(page),
        "@@STEPS@@": render_steps(page),
        "@@FAQS@@": "".join(faqs),
        "@@POPUP_TITLE@@": e(page.get("popup_title", "هل تحتاج إلى استشارة قانونية؟")),
        "@@POPUP_COPY@@": e(page.get("popup_copy", "تواصل مع المكتب واذكر نوع طلبك باختصار لبحث الخطوة التالية.")),
        "@@POPUP_CALL_TEXT@@": e(page.get("popup_call_text", page["call_text"])),
        "@@POPUP_WA_TEXT@@": e(page.get("popup_wa_text", page["whatsapp_text"])),
        "@@CONTACT_TITLE@@": e(page.get("contact_title", "تواصل مع المكتب")),
        "@@CONTACT_COPY@@": e(page.get("contact_copy", "ابدأ بملخص واضح للمسألة. تُحدد المستندات ونطاق العمل والأتعاب قبل البدء.")),
        "@@LOCATION_TEXT@@": e(page.get("location_text", "جدة · طريق صاري · حي الروضة")),
    }
    output = TEMPLATE
    for token, value in replacements.items():
        output = output.replace(token, value)
    if "@@" in output:
        raise ValueError(f"Unfilled template token in {key}")
    return output

def make_routes() -> dict:
    routes = []
    for key in ORDER:
        if key == "general":
            continue
        routes.append({
            "src": "^/$",
            "has": [{"type": "query", "key": "service", "value": key}],
            "dest": "/" + SERVICES[key]["file"],
        })
    routes.append({"src": "^/$", "dest": "/index.html"})
    asset_headers = []
    for asset in (
        "hero.bef4cef4bf71.webp",
        "logo.81477f2c0280.webp",
        "tajawal-400.d89ada41ad2e.woff2",
        "tajawal-700.4f1754100d5a.woff2",
    ):
        asset_headers.append({
            "source": "/assets/" + asset,
            "headers": [{"key": "Cache-Control", "value": "public, max-age=31536000, immutable"}],
        })
    return {"routes": routes, "headers": asset_headers}


def validate() -> None:
    for key in ORDER:
        p = SERVICES[key]
        for i, headline in enumerate(p["headlines"], 1):
            if len(list(headline)) > 30:
                raise ValueError(f"{key}: headline {i} exceeds 30 characters: {headline}")
        for i, description in enumerate(p["ad_descriptions"], 1):
            if len(list(description)) > 90:
                raise ValueError(f"{key}: description {i} exceeds 90 characters: {description}")
        if not p["keywords"] or not p["topic_cards"] or not p["faqs"] or not p["steps"]:
            raise ValueError(f"{key}: missing keywords, topic cards, steps, or FAQs")
        if p.get("headlines") and p.get("h1") and p["headlines"][0] not in p["h1"] and p["h1"] not in p["headlines"][0]:
            raise ValueError(f"{key}: first ad headline and H1 are not aligned")


def render_ad_assets() -> str:
    cards = []
    for key in ORDER:
        p = SERVICES[key]
        paused = p.get("status") in ("paused", "confirm")
        status_label = ("موقوفة حتى التأكيد" if p.get("status") == "paused"
                        else "تحتاج تأكيدًا" if p.get("status") == "confirm" else "جاهزة للمراجعة")
        kws = "".join('<span class="keyword">' + e(x) + '</span>' for x in p["keywords"])
        headlines = "".join('<li><span class="asset-text">' + e(x) + '</span><span class="count"></span></li>' for x in p["headlines"])
        descriptions = "".join('<li><span class="asset-text">' + e(x) + '</span><span class="count"></span></li>' for x in p["ad_descriptions"])
        url = BASE_URL + ("/" if key == "general" else "/" + p["file"])
        buttons = ('<button class="btn btn-copy" type="button" disabled title="' + e(p.get("status_note", "أكد توفر الخدمة قبل النشر.")) + '">بانتظار التأكيد</button>'
                   if paused else '<button class="btn btn-copy" type="button" data-copy="' + e(key) + '">نسخ المجموعة</button>')
        status_cls = "hold" if paused else "ready"
        note = '<p class="status-note">' + e(p.get("status_note", "")) + '</p>' if p.get("status_note") else ""
        cards.append(
            '<article class="ad-card" data-service="' + e(key) + '" data-search="' + e(" ".join([p["label"]] + p["keywords"])) + '">'
            '<div class="card-top"><div><h3>' + e(p["label"]) + '</h3><code>' + e(key) + '</code></div>'
            '<span class="status ' + status_cls + '">' + status_label + '</span></div>'
            '<div class="final-url"><span>Final URL</span><a href="' + e(url) + '" target="_blank" rel="noopener noreferrer">' + e(url) + '</a></div>'
            + note
            + '<span class="label">الكلمات المفتاحية المقترحة</span><div class="keywords">' + kws + '</div>'
            + '<span class="label">العناوين <small>(30 حرفًا كحد أقصى)</small></span><ul class="assets headlines">' + headlines + '</ul>'
            + '<span class="label">الأوصاف <small>(90 حرفًا كحد أقصى)</small></span><ul class="assets descriptions">' + descriptions + '</ul>'
            + '<div class="card-actions"><a class="btn btn-open" href="' + e(url) + '" target="_blank" rel="noopener noreferrer">فتح صفحة الهبوط</a>' + buttons + '</div></article>'
        )
    tracking = "utm_source=google&utm_medium=cpc&utm_campaign={campaignid}&utm_content={adgroupid}&utm_term={keyword}"
    return """<!doctype html>
<html lang="ar" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>أصول Google Ads | مكتب المحامي عبدالعزيز عبدالله العديني للمحاماة والاستشارات القانونية</title>
<meta name="robots" content="noindex,nofollow">
<style>
*{box-sizing:border-box}body{margin:0;background:#f5f6f2;color:#19261f;font-family:Tahoma,Arial,sans-serif;line-height:1.7}
header{background:#10271d;color:#fff;padding:30px 20px 25px;border-bottom:3px solid #dfb66e}
.wrap{max-width:1200px;margin:auto;padding:0 18px}header h1{margin:0;font-size:clamp(24px,4vw,34px)}header p{margin:8px 0 0;color:#d9e4dc}
.setup{margin:20px auto;padding:18px 20px;background:#fff;border:1px solid #dfe5de;border-radius:14px}.setup code{display:block;direction:ltr;text-align:left;overflow-wrap:anywhere;background:#f5f6f2;padding:10px;border-radius:8px;margin-top:8px}
.toolbar{display:flex;gap:12px;align-items:center;justify-content:space-between;flex-wrap:wrap;margin:24px auto 14px}.toolbar input{min-width:240px;flex:1;padding:12px 14px;border:1px solid #cad4cb;border-radius:10px;font:inherit;background:#fff}.toolbar .summary{font-size:14px;color:#59695e}
.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px;padding-bottom:36px}.ad-card{background:#fff;border:1px solid #dce4dd;border-radius:16px;padding:20px;min-width:0;box-shadow:0 8px 22px #10271d0a}.card-top{display:flex;align-items:flex-start;justify-content:space-between;gap:12px}.card-top h3{margin:0;color:#10271d;font-size:20px}.card-top code{font-size:12px;color:#69786d;direction:ltr;display:inline-block}
.status{white-space:nowrap;border-radius:999px;padding:4px 9px;font-size:12px;font-weight:bold}.status.ready{background:#e7f3e9;color:#245c32}.status.hold{background:#fff2d6;color:#805613}
.final-url{display:grid;gap:3px;margin:14px 0;direction:ltr;text-align:left}.final-url span{font-size:11px;color:#69786d}.final-url a{font-size:13px;overflow-wrap:anywhere;color:#305b45}
.status-note{margin:10px 0;padding:9px 11px;border-radius:8px;background:#fff4df;color:#76500f;font-size:13px}
.label{display:block;margin:15px 0 7px;font-weight:bold;font-size:14px;color:#4c5e51}.label small{font-size:11px;color:#79877d;font-weight:normal}
.keywords{display:flex;gap:6px;flex-wrap:wrap}.keyword{padding:4px 8px;background:#f0f3ee;border:1px solid #e4e9e2;border-radius:6px;font-size:12px}
.assets{list-style:none;margin:0;padding:0;display:grid;gap:6px}.assets li{display:flex;align-items:flex-start;justify-content:space-between;gap:10px;padding:8px 10px;border:1px solid #e7ebe6;border-radius:8px;font-size:14px}.count{white-space:nowrap;color:#748275;font-size:11px;direction:ltr}
.card-actions{display:flex;gap:9px;flex-wrap:wrap;margin-top:18px}.btn{display:inline-flex;align-items:center;justify-content:center;padding:10px 13px;border-radius:9px;text-decoration:none;border:1px solid #c4d0c5;font:inherit;font-size:13px;font-weight:bold;cursor:pointer}.btn-open{background:#10271d;color:#fff;border-color:#10271d}.btn-copy{background:#fffaf0;color:#604810;border-color:#d4b66b}.btn:disabled{opacity:.55;cursor:not-allowed}
footer{background:#10271d;color:#d8e2d9;padding:22px 18px;font-size:13px}
@media(max-width:800px){.grid{grid-template-columns:1fr}.card-top h3{font-size:18px}}
</style></head><body>
<header><div class="wrap"><h1>أصول الحملات الإعلانية — مكتب المحامي عبدالعزيز عبدالله العديني للمحاماة والاستشارات القانونية</h1><p>اقتراحات كلمات مفتاحية وعناوين وأوصاف، مع رابط مستقل لكل صفحة هبوط. راجعها قبل إضافتها إلى Google Ads.</p></div></header>
<section class="setup wrap"><strong>لاحقة تتبّع مقترحة</strong><p>أضفها في إعدادات تتبع Google Ads مرة واحدة فقط، بعد مراجعة إعدادات الحساب الحالية:</p><code>""" + tracking + """</code></section>
<div class="toolbar wrap"><input id="search" type="search" placeholder="ابحث باسم الخدمة أو كلمة مفتاحية..." aria-label="البحث في المجموعات"><span class="summary" id="summary">""" + str(len(ORDER)) + """ مجموعة مقترحة</span></div>
<main class="grid wrap">""" + "".join(cards) + """</main>
<footer><div class="wrap">هذه اقتراحات نصية وليست حملات منشأة داخل حساب Google Ads. تحقق من توفر كل خدمة وصحة بيانات المكتب، واختبر روابط الاتصال والوسوم قبل النشر.</div></footer>
<script>
(function(){
var search=document.getElementById('search'),cards=[].slice.call(document.querySelectorAll('.ad-card')),summary=document.getElementById('summary');
function filter(){var q=search.value.trim().toLocaleLowerCase();var n=0;cards.forEach(function(card){var show=card.dataset.search.toLocaleLowerCase().indexOf(q)!==-1;card.hidden=!show;if(show)n++;});summary.textContent=n+' من '+cards.length+' مجموعة';}
search.addEventListener('input',filter);
cards.forEach(function(card){card.querySelectorAll('.headlines .asset-text,.descriptions .asset-text').forEach(function(el){var count=el.parentElement.querySelector('.count');var max=el.closest('.headlines')?'30':'90';var len=Array.from(el.textContent.trim()).length;count.textContent=len+'/'+max;if(len>Number(max))count.style.color='#b3261e';});
var btn=card.querySelector('[data-copy]');if(!btn)return;btn.addEventListener('click',async function(){var text=function(selector){return Array.from(card.querySelectorAll(selector+' .asset-text')).map(function(el,i){return (i+1)+'. '+el.textContent.trim();}).join('\n');};
var kws=Array.from(card.querySelectorAll('.keyword')).map(function(el){return '• '+el.textContent.trim();}).join('\n');
var url=card.querySelector('.final-url a').href;
var payload=card.querySelector('h3').textContent+'\nFinal URL: '+url+'\n\nالكلمات المفتاحية المقترحة:\n'+kws+'\n\nالعناوين:\n'+text('.headlines')+'\n\nالأوصاف:\n'+text('.descriptions');
try{await navigator.clipboard.writeText(payload);var old=btn.textContent;btn.textContent='تم النسخ';setTimeout(function(){btn.textContent=old;},1600);}catch(e){window.prompt('انسخ النص التالي:',payload);}
});});
})();
</script></body></html>"""


def main() -> None:
    validate()
    for key in ORDER:
        page = SERVICES[key]
        out = ROOT / page["file"]
        out.write_text(render_page(key, page), encoding="utf-8")
        print(f"generated {page['file']}")
    (ROOT / "vercel.json").write_text(json.dumps(make_routes(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (ROOT / "google-ads-assets.html").write_text(render_ad_assets(), encoding="utf-8")
    (ROOT / "robots.txt").write_text("User-agent: *\nAllow: /\n", encoding="utf-8")
    print(f"Generated {len(ORDER)} landing pages, Vercel routes, ad assets, and robots.txt.")


if __name__ == "__main__":
    main()
