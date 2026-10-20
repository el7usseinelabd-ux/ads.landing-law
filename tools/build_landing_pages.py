#!/usr/bin/env python3
"""Build four lightweight, static Arabic landing pages for Vercel and GitHub Pages.

Requirements: Pillow, fonttools, brotli. Run from any directory with Python 3.
The generated HTML is checked into the repository; Vercel serves it without a build step.
"""
from __future__ import annotations

import hashlib
import html
import json
from pathlib import Path
from urllib.parse import quote

from PIL import Image, ImageOps
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
VERCEL_URL = "https://adslanding-law.vercel.app"
PHONE = "966556799995"
PHONE_DISPLAY = "055 679 9995"
MAP_URL = "https://maps.app.goo.gl/rDctwALN59WZ3zFf6"
GTM_ID = "GTM-KKHH6SBP"

PAGES = {
    "general": {
        "file": "index.html",
        "canonical": f"{VERCEL_URL}/",
        "title": "محامي في جدة | استشارات قانونية سريعة للأفراد والشركات",
        "description": "استشارة قانونية فورية في جدة، تمثيل احترافي للأفراد والشركات، ومتابعة دقيقة في القضايا المدنية والجنائية والعقود. احجز استشارة الآن.",
        "eyebrow": "استشارات قانونية في جدة",
        "h1": "محامٍ في جدة يضع لك الحل الصحيح",
        "subtitle": "استشارة سريعة، سرية تامة، وخبرة عملية في القضايا المدنية والجنائية والعقود.",
        "intro": "نساعد الأفراد والشركات على اتخاذ القرار الصحيح في الوقت المناسب: قضايا تجارية، نزاعات، عقود، توثيق، ومشكلات قانونية تحتاج إلى توجيه مهني وفعلي.",
        "call_text": "احجز استشارة الآن",
        "popup_call_text": "اتصل بالمكتب الآن",
        "whatsapp_text": "تواصل عبر واتساب",
        "main_message": "السلام عليكم، أرغب في استشارة قانونية. نوع المسألة: ...",
        "popup_title": "تحتاج إلى محامٍ في جدة؟",
        "popup_description": "تحدث مع مكتبنا الآن لتحديد الخدمة المناسبة لك.",
        "popup_whatsapp": "السلام عليكم، أرغب في استشارة قانونية. نوع المسألة: ...",
        "chips": [
            ("قضايا جزائية", "السلام عليكم، أرغب في استشارة بخصوص: قضايا جزائية."),
            ("أحوال شخصية", "السلام عليكم، أرغب في استشارة بخصوص: أحوال شخصية."),
            ("عقود وتجارية", "السلام عليكم، أرغب في استشارة بخصوص: عقود وتجارية."),
            ("عقاري وعمالي", "السلام عليكم، أرغب في استشارة بخصوص: عقاري وعمالي."),
        ],
        "perks": [
            ("استشارة عاجلة", "رد سريع وتقييم أولي في دقائق"),
            ("سرية تامة", "حماية خصوصية العميل في كل خطوة"),
            ("تمثيل احترافي", "مرافعة ومتابعة قانونية دقيقة"),
            ("حل عملي", "توصية واضحة قبل اتخاذ القرار"),
        ],
        "faqs": [
            ("كيف أطلب استشارة قانونية؟", "يمكنك التواصل مباشرة عبر الهاتف أو واتساب، مع ذكر نوع المسألة، وسنحدد لك الخدمة المناسبة في أقرب وقت."),
            ("هل توجد استشارة عاجلة؟", "نعم، نحرص على الاستجابة السريعة، خاصة في القضايا التي تتطلب متابعة فورية أو قرارات سريعة."),
            ("كيف تُحدد الأتعاب؟", "تحدد الرسوم حسب نوع الخدمة، مدى تعقيد القضية، وطبيعة العمل المطلوب من المكتب."),
            ("هل يتم التعامل بسرية؟", "نعم، خصوصية العميل وسريته تضمنها إجراءات المكتب في جميع مراحل الاستشارة والمتابعة."),
        ],
    },
    "criminal": {
        "file": "criminal.html",
        "canonical": f"{VERCEL_URL}/?service=criminal",
        "title": "محامي جنائي في جدة | دفاع سريع وسري",
        "description": "محامي جنائي في جدة، تمثيل في القضايا الجزائية، مخدرات، تزوير، تشهير، جرائم إلكترونية، واستشارات عاجلة مع سرية تامة.",
        "eyebrow": "القضايا الجنائية · جدة",
        "h1": "محامي جنائي في جدة",
        "subtitle": "دفاع سريع، سرية تامة، ومتابعة دقيقة في القضايا العاجلة.",
        "intro": "إذا كنت تواجه استدعاء، تحقيقاً أو اتهاماً، لا تتردد في التواصل. نراجع الأوراق، نحدد المسار القانوني الأنسب، ونسعى إلى أفضل نتيجة مع الالتزام بسرية العميل.",
        "call_text": "استشارة جنائية عاجلة",
        "whatsapp_text": "ارسل تفاصيل القضية",
        "main_message": "السلام عليكم، أحتاج استشارة جنائية. نوع القضية: ... وهل توجد جلسة أو استدعاء للتحقيق؟",
        "popup_title": "قضية جنائية؟",
        "popup_description": "تحدث مع محامٍ جنائي الآن بسرية تامة.",
        "popup_whatsapp": "السلام عليكم، أحتاج استشارة جنائية. نوع القضية: ... وهل توجد جلسة أو استدعاء للتحقيق؟",
        "chips": [
            ("مخدرات", "السلام عليكم، أرغب في استشارة بخصوص: مخدرات."),
            ("ابتزاز وتشهير", "السلام عليكم، أرغب في استشارة بخصوص: ابتزاز وتشهير."),
            ("تزوير ونصب", "السلام عليكم، أرغب في استشارة بخصوص: تزوير ونصب."),
            ("جرائم إلكترونية", "السلام عليكم، أرغب في استشارة بخصوص: جرائم إلكترونية."),
            ("نقض واعتراض", "السلام عليكم، أحتاج استشارة بشأن نقض أو اعتراض في قضية جنائية."),
        ],
        "perks": [
            ("استجابة فورية", "تقييم أولي سريع للأوضاع والقضايا"),
            ("سرية كاملة", "نحافظ على خصوصية كل محادثة"),
            ("دفاع متقن", "مراجعة الأوراق وبلورة الخطط المناسبة"),
            ("توقيت صحيح", "قدرة على اتخاذ القرار قبل التأخر"),
        ],
        "faqs": [
            ("ماذا أفعل إذا استُدعيت للتحقيق؟", "تواصل مع المكتب قبل الحضور إن أمكن، وأرسل ملخصاً بالواقعة ليتم تقييم الموقف بشكل صحيح قبل اتخاذ أي خطوة."),
            ("هل يمكن بدء الاستشارة عن بُعد؟", "نعم، يمكن الاستشارة عبر الهاتف أو واتساب، ثم متابعة القضية بحسب الحاجة."),
            ("هل يوجد سريّة في التعامل؟", "نعم، جميع الاستشارات والمراسلات تُدار بسرية تامة بما يحفظ خصوصية العميل."),
            ("كم يستغرق تقييم القضية؟", "يتم تقييم الموقف أولياً في وقت قصير، ثم يتم تحديد الخطوات المناسبة بحسب طبيعة القضية."),
        ],
    },
    "family": {
        "file": "family.html",
        "canonical": f"{VERCEL_URL}/?service=family",
        "title": "محامي أحوال شخصية في جدة | حل سريع وشرعي",
        "description": "استشارات وتمثيل في قضايا الأحوال الشخصية بجدة: طلاق، خلع، نفقة، حضانة، ميراث، وحقوق الأسرة. تواصل الآن.",
        "eyebrow": "الأحوال الشخصية والميراث · جدة",
        "h1": "محامي أحوال شخصية في جدة",
        "subtitle": "مساعدة عملية في الطلاق، النفقة، الحضانة، والميراث مع متابعة دقيقة وقرارات مدروسة.",
        "intro": "نساعدك على فهم حقوقك وتحديد أولى الخطوات بشكل صحيح لتقليل التوتر والوقت، سواء كان الأمر يتعلق بطلاق، نفقة، حضانة، أو ميراث وتركات.",
        "call_text": "احجز استشارة أسرية الآن",
        "whatsapp_text": "استشارة أسرية عبر واتساب",
        "main_message": "السلام عليكم، أحتاج استشارة في قضية أسرية. نوعها: (طلاق / خلع / نفقة / حضانة / ميراث / إثبات النسب).",
        "popup_title": "قضية أسرية؟",
        "popup_description": "تحدث مع محامي الأحوال الشخصية الآن لتحديد الخطوة الصحيحة.",
        "popup_whatsapp": "السلام عليكم، أحتاج استشارة في قضية أسرية. نوعها: (طلاق / خلع / نفقة / حضانة / ميراث / إثبات النسب).",
        "chips": [
            ("طلاق وخلع", "السلام عليكم، أحتاج استشارة في جدة بخصوص الطلاق أو الخلع."),
            ("نفقة وحضانة", "السلام عليكم، أحتاج استشارة في جدة بخصوص النفقة أو الحضانة."),
            ("ميراث وتركات", "السلام عليكم، أحتاج استشارة في جدة بخصوص الميراث أو التركة."),
            ("إثبات النسب", "السلام عليكم، أحتاج استشارة في جدة بخصوص إثبات النسب."),
        ],
        "perks": [
            ("استشارة حساسة", "معالجة دقيقة وخصوصية كاملة"),
            ("خطوات واضحة", "نشرح لك الحقوق والبدائل العملية"),
            ("تخطيط قانوني", "تصعيد مناسب في الوقت المناسب"),
            ("دعم مستمر", "مرافقة حتى اتخاذ القرار"),
        ],
        "faqs": [
            ("كيف أبدأ دعوى الطلاق أو الخلع؟", "يمكنك التواصل معنا أولاً لتحديد الحالة، ثم نوضح لك المستندات اللازمة والخطوات التي يجب اتباعها."),
            ("هل يمكن الاستشارة عن بُعد؟", "نعم، الاستشارة ممكنة عبر الهاتف أو واتساب، مع متابعة مناسبة وفقاً لحالة العميل."),
            ("هل يهم التوقيت في قضايا الأسرة؟", "نعم، التوقيت مهم في بعض القضايا، لذلك ننصح بالاستشارة مبكراً لتحديد الخيار الأنسب."),
            ("هل يتم التعامل مع الحالات الحساسة بسرية؟", "نعم، نعامل جميع القضايا الأسرية بخصوصية كاملة واحترام كامل للبيانات الشخصية."),
        ],
    },
    "documentation": {
        "file": "documentation.html",
        "canonical": f"{VERCEL_URL}/?service=documentation",
        "title": "موثق معتمد في جدة | وكالات وإفراغ عقاري",
        "description": "توثيق الوكالات، الإفراغ العقاري، الإقرارات المالية، وعقود الشركات في جدة. استشارة سريعة ومتابعة دقيقة من مكتب معتمد.",
        "eyebrow": "خدمات التوثيق العدلي · جدة",
        "h1": "موثق معتمد في جدة",
        "subtitle": "توثيق الوكالات والإفراغ العقاري والإقرارات وعقود الشركات بطريقة دقيقة وفعالة.",
        "intro": "نوثّق الوكالات، الإفراغ، والوثائق العقارية والمالية في جدة، مع متابعة دقيقة للتأكد من صحة المستندات وسلاسة الإجراءات.",
        "call_text": "اتصل بالموثق الآن",
        "whatsapp_text": "اسأل عن توثيق وكالة",
        "main_message": "السلام عليكم، أرغب في توثيق: (وكالة / إفراغ عقاري / إقرار / عقد شركة). ما المستندات المطلوبة؟",
        "popup_title": "تريد توثيق وكالة أو إفراغ؟",
        "popup_description": "تواصل مع المكتب الآن لمعرفة المستندات المطلوبة والخطوة التالية.",
        "popup_whatsapp": "السلام عليكم، أرغب في توثيق: (وكالة / إفراغ عقاري / إقرار / عقد شركة). ما المستندات المطلوبة؟",
        "chips": [
            ("توثيق وكالات", "السلام عليكم، أرغب في استشارة بخصوص: توثيق وكالات."),
            ("إفراغ عقاري", "السلام عليكم، أرغب في استشارة بخصوص: إفراغ عقاري."),
            ("إقرارات مالية", "السلام عليكم، أرغب في استشارة بخصوص: إقرارات مالية."),
            ("عقود شركات", "السلام عليكم، أرغب في استشارة بخصوص: عقود شركات."),
        ],
        "perks": [
            ("دقة في التوثيق", "فحص كامل للمستندات قبل التنفيذ"),
            ("تسهيل الإجراءات", "إرشاد واضح قبل الحضور أو التوقيع"),
            ("إشراف متفقد", "مراجعة كاملة للمعاملة"),
            ("خدمة احترافية", "استفسار سريع وتوجيه مناسب"),
        ],
        "faqs": [
            ("ما المستندات المطلوبة لتوثيق وكالة؟", "تختلف حسب نوع الوكالة، ويمكن للحالة أن تستوجب مستندات إضافية بحسب طبيعة المعاملة."),
            ("هل التوثيق متاح للشركات؟", "نعم، الخدمة متاحة للأفراد والشركات والمنشآت، مع متابعة عبر الخطوات المناسبة لكل حالة."),
            ("هل يمكن الاستفسار قبل الحضور؟", "نعم، يمكن الاستفسار أولاً عبر الهاتف أو واتساب لتحقيق أفضل توجيه قبل الحضور."),
            ("هل يتم تجهيز المعاملة في الوقت المناسب؟", "نعم، نسعى إلى سرعة الإنجاز دون إهمال دقة المستندات أو شروط التوثيق."),
        ],
    },
}

CSS_TEMPLATE = r"""@font-face{font-family:Tajawal;src:url('./assets/@@FONT400@@') format('woff2');font-weight:400;font-display:swap}
@font-face{font-family:Tajawal;src:url('./assets/@@FONT700@@') format('woff2');font-weight:700;font-display:swap}
:root{color-scheme:light;--forest:#10271d;--forest-2:#17392a;--gold:#dfb66e;--ink:#18231d;--muted:#5d6b62;--paper:#f7f7f2;--line:#dce3dc;--white:#fff}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:var(--paper);color:var(--ink);font-family:Tajawal,Arial,sans-serif;font-size:17px;line-height:1.65}a{color:inherit}button,input,textarea,select{font:inherit}img{max-width:100%;display:block}strong,b{font-weight:700}.skip-link{position:absolute;left:-9999px;top:auto}.skip-link:focus{left:16px;top:16px;z-index:9999;background:#fff;padding:8px 12px;border-radius:8px}.site-header{position:sticky;top:0;z-index:20;background:rgba(16,39,29,.88);backdrop-filter:blur(10px);border-bottom:1px solid rgba(223,182,110,.22)}.header-inner{max-width:1120px;margin:0 auto;height:72px;padding:0 20px;display:flex;align-items:center;justify-content:space-between}.brand{display:flex;align-items:center;gap:12px;text-decoration:none}.brand img{width:52px;height:49px;border-radius:14px}.brand-text{display:flex;flex-direction:column;color:#fff;line-height:1.1}.brand-text strong{font-size:15px}.brand-text small{font-size:12px;color:rgba(255,255,255,.72)}.header-call{display:inline-flex;align-items:center;justify-content:center;padding:10px 14px;border-radius:999px;background:rgba(223,182,110,.12);border:1px solid rgba(223,182,110,.52);color:#fff;text-decoration:none;font-weight:700}.hero{position:relative;overflow:hidden;background:radial-gradient(ellipse at 80% 10%,rgba(45,83,61,.38),transparent 50%),var(--forest);color:#fff}.hero-inner{max-width:1120px;margin:0 auto;padding:36px 20px 24px;display:grid;grid-template-columns:minmax(0,1.3fr) minmax(320px,.7fr);gap:26px;align-items:center;min-height:470px}.eyebrow{margin:0 0 12px;color:#f3d69a;font-size:14px;letter-spacing:.02em;font-weight:700}.hero h1{margin:0;line-height:1.15;font-size:clamp(2.2rem,4vw,4rem);font-weight:800}.hero-subtitle{margin:18px 0 0;font-size:1.1rem;line-height:1.7;color:rgba(255,255,255,.88);max-width:38rem}.hero-actions{display:flex;flex-wrap:wrap;gap:12px;margin-top:22px}.btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;padding:14px 20px;border-radius:14px;text-decoration:none;font-weight:700;transition:transform .18s ease,box-shadow .18s ease}.btn:hover{transform:translateY(-1px)}.btn-call{background:var(--gold);color:#18231d;box-shadow:0 14px 30px rgba(223,182,110,.25)}.btn-wa{background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.18);color:#fff}.trustline{margin:18px 0 10px;font-size:14px;color:rgba(255,255,255,.8)}.service-chips{display:flex;flex-wrap:wrap;gap:10px;margin-top:6px}.service-chips a{display:inline-flex;align-items:center;padding:8px 12px;border-radius:999px;background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.14);text-decoration:none;color:#fff;font-size:13px}.intro{margin:26px 0 0;max-width:42rem;font-size:1rem;color:rgba(255,255,255,.82)}.hero-visual{position:relative;display:flex;align-items:center;justify-content:center;min-height:360px;border-radius:26px;border:1px solid rgba(223,182,110,.35);background:linear-gradient(134deg,rgba(255,255,255,.04),rgba(42,77,57,.18)),url('./assets/@@HERO@@') center/cover no-repeat;box-shadow:0 24px 70px rgba(0,0,0,.24)}.hero-visual::before{content:"";position:absolute;inset:24px;border-radius:20px;border:1px solid rgba(255,255,255,.14);background:linear-gradient(180deg,rgba(16,39,29,.1),rgba(16,39,29,.44))}.perks-section{max-width:1120px;margin:0 auto;padding:8px 20px 0}.perk-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px}.perk-card{background:var(--white);border:1px solid var(--line);border-radius:16px;padding:18px 16px;box-shadow:0 12px 30px rgba(16,39,29,.04)}.perk-card strong{display:block;color:var(--forest);font-size:16px;margin-bottom:6px}.perk-card span{display:block;color:var(--muted);font-size:14px;line-height:1.6}.faq-section,.contact-details{max-width:1120px;margin:0 auto;padding:30px 20px 20px}.faq-section h2{margin:0 0 14px;font-size:clamp(1.5rem,2vw,2rem);color:var(--forest);font-weight:800}.faq-list{display:grid;grid-template-columns:1fr 1fr;gap:12px}.faq-list details{border:1px solid var(--line);border-radius:14px;background:#fff;padding:14px 16px}.faq-list summary{cursor:pointer;font-weight:700;color:var(--forest);list-style:none}.faq-list summary::-webkit-details-marker{display:none}.faq-list p{margin:10px 0 0;color:var(--muted);font-size:15px}.contact-details{padding-top:10px;padding-bottom:34px}.details-inner{background:#fff;border:1px solid var(--line);border-radius:18px;padding:20px 22px;display:flex;flex-wrap:wrap;gap:10px 16px;align-items:center;justify-content:space-between;color:var(--ink)}.details-inner a{color:var(--forest);font-weight:700;text-decoration:none}.site-footer{background:#0f1f18;color:rgba(255,255,255,.82)}.footer-inner{max-width:1120px;margin:0 auto;padding:18px 20px 64px;display:flex;justify-content:space-between;gap:16px;align-items:center;flex-wrap:wrap}.footer-name{font-weight:700}.footer-links{display:flex;gap:16px;flex-wrap:wrap}.footer-links a{text-decoration:none;color:#fff}.mobile-bar{position:fixed;left:0;right:0;bottom:0;display:none;z-index:22;padding:10px 12px;background:rgba(9,18,15,.95);border-top:1px solid rgba(223,182,110,.2);backdrop-filter:blur(8px)}.mobile-bar a{flex:1 1 0;display:inline-flex;align-items:center;justify-content:center;padding:12px 10px;border-radius:12px;text-decoration:none;font-weight:700}.mobile-call{background:var(--gold);color:#18231d}.mobile-wa{background:#0e7a43;color:#fff}.info-dialog,.welcome-dialog{width:min(560px,calc(100% - 32px));max-height:min(78vh,680px);overflow:auto;border:0;border-radius:18px;padding:20px;background:#fff;color:var(--ink);box-shadow:0 20px 60px rgba(10,20,16,.2)}.info-dialog::backdrop,.welcome-dialog::backdrop{background:rgba(11,18,16,.52)}.dialog-head,.welcome-head{display:flex;align-items:flex-start;justify-content:space-between;gap:12px}.dialog-head h2,.welcome-head h2{margin:0;color:var(--forest)}.dialog-close,.welcome-close{margin:0;border:0;background:transparent;font-size:28px;color:var(--muted);cursor:pointer}.welcome-dialog{padding:22px 22px 18px}.welcome-kicker{display:inline-block;background:rgba(223,182,110,.12);color:var(--forest);padding:6px 10px;border-radius:999px;font-size:12px;font-weight:700}.welcome-body{padding-top:20px}.welcome-body h2{margin:0 0 10px;font-size:clamp(1.7rem,3vw,2.2rem);color:var(--forest)}.welcome-body p{margin:0 0 18px;color:var(--muted)}.welcome-actions{display:flex;flex-wrap:wrap;gap:10px}.welcome-actions a{display:inline-flex;align-items:center;justify-content:center;padding:12px 16px;border-radius:12px;text-decoration:none;font-weight:700}.welcome-actions .cta-phone{background:var(--gold);color:#18231d}.welcome-actions .cta-wa{background:#0e7a43;color:#fff}.site-header .brand-text small {color:rgba(255,255,255,.75)}
@media(min-width:861px){.hero-inner{grid-template-columns:minmax(0,1.2fr) minmax(300px,.8fr)}.hero-visual{display:block;min-height:350px;max-height:440px;border:1px solid rgba(223,182,110,.35);border-radius:26px}}@media(max-width:760px){body{font-size:16px}.site-header{height:64px}.header-inner{padding:0 15px;height:64px}.brand img{width:45px;height:43px}.brand-text{font-size:14px}.brand-text small{font-size:11px}.header-call{padding:9px 12px;font-size:13px}.hero-inner{grid-template-columns:1fr;padding:28px 15px 20px;min-height:auto}.hero h1{font-size:2.4rem}.hero-subtitle{font-size:1rem}.perk-grid{grid-template-columns:1fr 1fr}.faq-list{grid-template-columns:1fr}.details-inner{flex-direction:column;align-items:flex-start}.mobile-bar{display:flex}.site-footer{padding-bottom:74px}.footer-inner{padding-bottom:82px}}@media(max-width:500px){.perk-grid{grid-template-columns:1fr}.} @media(max-width:360px){.header-inner{padding:0 10px}.brand{gap:6px}.brand img{width:40px;height:38px}.brand-text{font-size:13px}.brand-text small{display:none}.header-call{font-size:12px;padding:8px 10px}.hero h1{font-size:2.1rem}.btn{width:100%}}@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}*,*::before,*::after{animation-duration:.01ms!important;animation-iteration-count:1!important;transition-duration:.01ms!important}}
"""

HTML_TEMPLATE = r"""<!doctype html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>@@TITLE@@</title>
<meta name="description" content="@@DESCRIPTION@@">
<meta name="robots" content="noindex, nofollow">
<link rel="canonical" href="@@CANONICAL@@">
<link rel="icon" href="./assets/@@LOGO@@" type="image/webp">
<link rel="preload" href="./assets/@@FONT400@@" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="./assets/@@FONT700@@" as="font" type="font/woff2" crossorigin>
<meta property="og:site_name" content="مكتب عبدالعزيز العديني للمحاماة">
<meta property="og:type" content="website">
<meta property="og:url" content="@@CANONICAL@@">
<meta property="og:title" content="@@TITLE@@">
<meta property="og:description" content="@@DESCRIPTION@@">
<meta property="og:image" content="@@HERO_ABSOLUTE@@">
<meta property="og:image:width" content="@@HERO_WIDTH@@">
<meta property="og:image:height" content="@@HERO_HEIGHT@@">
<meta property="og:image:alt" content="مكتب عبدالعزيز العديني للمحاماة والاستشارات القانونية في جدة">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="@@TITLE@@">
<meta name="twitter:description" content="@@DESCRIPTION@@">
<meta name="twitter:image" content="@@HERO_ABSOLUTE@@">
<link rel="preconnect" href="https://www.googletagmanager.com" crossorigin>
<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);})(window,document,'script','dataLayer','@@GTM_ID@@');</script>
<style>@@CSS@@</style>
</head>
<body data-service="@@SERVICE@@">
<a class="skip-link" href="#main">انتقل إلى المحتوى</a>
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=@@GTM_ID@@" height="0" width="0" style="display:none;visibility:hidden" title="Google Tag Manager"></iframe></noscript>
<header class="site-header" id="top"><div class="header-inner">
<a class="brand" href="./" aria-label="مكتب عبدالعزيز العديني للمحاماة، بداية الصفحة"><img src="./assets/@@LOGO@@" width="52" height="49" alt="شعار مكتب العديني"><span class="brand-text"><strong>مكتب العديني</strong><small>للمحاماة والاستشارات</small></span></a>
<a class="header-call" href="tel:+966556799995" data-contact="phone" data-service="@@SERVICE@@" data-position="hero" aria-label="اتصل بمكتب العديني على 055 679 9995">اتصل: <span>055 679 9995</span></a>
</div></header>
<main id="main">
<section class="hero" aria-labelledby="hero-title"><div class="hero-inner"><div class="hero-copy">
<p class="eyebrow">@@EYEBROW@@</p>
<h1 id="hero-title">@@H1@@</h1>
<p class="hero-subtitle">@@SUBTITLE@@</p>
<div class="hero-actions"><a class="btn btn-call" href="tel:+966556799995" data-contact="phone" data-service="@@SERVICE@@" data-position="hero">@@CALL_TEXT@@</a><a class="btn btn-wa" href="@@MAIN_WHATSAPP_URL@@" target="_blank" rel="noopener noreferrer" data-contact="whatsapp" data-service="@@SERVICE@@" data-position="hero">@@WHATSAPP_TEXT@@</a></div>
<p class="trustline">سرية تامة في التعامل · استجابة سريعة · جدة، طريق صاري، حي الروضة</p>
<nav class="service-chips" aria-label="اختر موضوع الاستفسار">@@CHIPS@@</nav>
<p class="intro">@@INTRO@@</p>
</div><div class="hero-visual" aria-hidden="true"></div></div></section>
<section class="perks-section" aria-label="مزايا المكتب"><div class="perk-grid">@@PERKS@@</div></section>
<section class="faq-section" aria-labelledby="faq-title"><h2 id="faq-title">أسئلة شائعة</h2><div class="faq-list">@@FAQS@@</div></section>
<section class="contact-details" aria-label="عنوان المكتب"><div class="details-inner"><span><strong>مكتب العديني للمحاماة</strong> · جدة · طريق صاري · حي الروضة</span><a href="@@MAP_URL@@" target="_blank" rel="noopener noreferrer">موقع المكتب</a><a href="tel:+966556799995" data-contact="phone" data-service="@@SERVICE@@" data-position="footer">055 679 9995</a></div></section>
</main>
<footer class="site-footer"><div class="footer-inner"><div><div class="footer-name">مكتب عبدالعزيز العديني للمحاماة والاستشارات القانونية</div><div>مساعدة قانونية للأفراد والشركات في جدة</div></div><nav class="footer-links" aria-label="روابط الموقع"><a href="tel:+966556799995">اتصل</a><a href="@@MAIN_WHATSAPP_URL@@" target="_blank" rel="noopener noreferrer">واتساب</a><a href="@@MAP_URL@@" target="_blank" rel="noopener noreferrer">الخريطة</a></nav></div></footer>
<nav class="mobile-bar" aria-label="تواصل سريع"><a class="mobile-call" href="tel:+966556799995" data-contact="phone" data-service="@@SERVICE@@" data-position="sticky">اتصل الآن</a><a class="mobile-wa" href="@@MAIN_WHATSAPP_URL@@" target="_blank" rel="noopener noreferrer" data-contact="whatsapp" data-service="@@SERVICE@@" data-position="sticky">واتساب</a></nav>
<dialog id="privacy-dialog" class="info-dialog" aria-labelledby="privacy-title"><div class="dialog-head"><h2 id="privacy-title">سياسة الخصوصية</h2><button type="button" class="dialog-close" data-close-dialog aria-label="إغلاق">×</button></div><p>يُستخدم هذا الموقع لتقديم المعلومات العامة عن خدمات المكتب واستقبال طلبات التواصل. لا يتم تخزين بيانات حساسة إلا وفق ضوابط الاستخدام المعتمدة من المكتب.</p></dialog>
<dialog id="terms-dialog" class="info-dialog" aria-labelledby="terms-title"><div class="dialog-head"><h2 id="terms-title">شروط الاستخدام</h2><button type="button" class="dialog-close" data-close-dialog aria-label="إغلاق">×</button></div><p>يُعتبر الاتصال عبر الهاتف أو واتساب طلباً للاستشارة، وتخضع الخدمة لاحقاً لتقدير المكتب وتحديد نطاق العمل المطلوب.</p></dialog>
<dialog id="welcome-dialog" class="welcome-dialog" aria-labelledby="welcome-title" aria-describedby="welcome-description"><div class="welcome-head"><span class="welcome-kicker">مكتب العديني للمحاماة</span><button type="button" class="welcome-close" data-close-welcome aria-label="إغلاق">×</button></div><div class="welcome-body"><h2 id="welcome-title">استشارة قانونية فورية</h2><p id="welcome-description">لديك سؤال قانوني؟ تواصل الآن وسنساعدك في تحديد الخطوة المناسبة.</p><div class="welcome-actions"><a class="cta-phone" href="tel:+966556799995" data-contact="phone" data-service="@@SERVICE@@" data-position="popup">@@POPUP_CALL_TEXT@@</a><a class="cta-wa" href="@@POPUP_WHATSAPP_URL@@" target="_blank" rel="noopener noreferrer" data-contact="whatsapp" data-service="@@SERVICE@@" data-position="popup">@@POPUP_WHATSAPP_TEXT@@</a></div></div></dialog>
<script>
(() => {'use strict';
const service=document.body.dataset.service||'general';
const dataLayer=window.dataLayer=window.dataLayer||[];

document.addEventListener('click',event => {
  const link=event.target.closest('a[data-contact]');
  if(!link) return;
  const method=link.dataset.contact;
  const position=link.dataset.position||'hero';
  const serviceName=link.dataset.service||service;
  dataLayer.push({event:'contact_click',contact_method:method,contact_channel:method,position,service:serviceName,landing_service:serviceName,legal_service:serviceName});
});

document.querySelectorAll('[data-dialog]').forEach(button => button.addEventListener('click', () => document.getElementById(button.dataset.dialog).showModal()));
document.querySelectorAll('[data-close-dialog]').forEach(button => button.addEventListener('click', () => button.closest('dialog').close()));
const welcome=document.getElementById('welcome-dialog');
document.querySelector('[data-close-welcome]').addEventListener('click', () => welcome.close());
welcome.addEventListener('close', () => document.documentElement.classList.remove('popup-open'));
const preview=new URLSearchParams(location.search).get('popup')==='1';let seen=false;try{seen=!preview&&sessionStorage.getItem('aledini-contact-welcome')==='1';}catch{}
const reveal=()=>{if(seen||document.hidden||welcome.open||typeof welcome.showModal!=='function')return false;welcome.showModal();document.documentElement.classList.add('popup-open');seen=true;try{sessionStorage.setItem('aledini-contact-welcome','1');}catch{};dataLayer.push({event:'welcome_popup_view',service});return true;};
if(!seen){window.setTimeout(()=>{if(reveal())return;const retry=()=>{if(reveal())document.removeEventListener('visibilitychange',retry);};document.addEventListener('visibilitychange',retry);},180);}
document.querySelectorAll('dialog').forEach(dialog => dialog.addEventListener('click', event => {if(event.target===dialog){const box=dialog.getBoundingClientRect();if(event.clientX<box.left||event.clientX>box.right||event.clientY<box.top||event.clientY>box.bottom){dialog.close();}}}));
})();
</script>
</body>
</html>
"""


def hashed_asset(prefix: str, suffix: str, data: bytes) -> str:
    digest = hashlib.sha256(data).hexdigest()[:12]
    filename = f"{prefix}.{digest}{suffix}"
    (ASSETS / filename).write_bytes(data)
    return filename


def optimize_assets() -> dict[str, object]:
    ASSETS.mkdir(exist_ok=True)
    for prefix in ("hero.", "logo.", "tajawal-400.", "tajawal-700."):
        for old in ASSETS.glob(prefix + "*"):
            if old.is_file():
                old.unlink()

    hero_source = ROOT / "2025-12-13.jpg"
    logo_source = ROOT / "logo-main.png"
    with Image.open(hero_source) as source:
        hero = ImageOps.exif_transpose(source).convert("RGB")
        hero.thumbnail((1200, 1600), Image.Resampling.LANCZOS)
        hero_size = hero.size
        hero_path = ASSETS / ".hero.webp"
        hero.save(hero_path, format="WEBP", quality=80, method=6)
        hero_data = hero_path.read_bytes()
        hero_path.unlink()
    hero_name = hashed_asset("hero", ".webp", hero_data)

    with Image.open(logo_source) as source:
        logo = ImageOps.exif_transpose(source).convert("RGBA")
        logo.thumbnail((128, 128), Image.Resampling.LANCZOS)
        logo_path = ASSETS / ".logo.webp"
        logo.save(logo_path, format="WEBP", quality=90, method=6, alpha_quality=90)
        logo_data = logo_path.read_bytes()
        logo_size = logo.size
        logo_path.unlink()
    logo_name = hashed_asset("logo", ".webp", logo_data)

    fonts: dict[int, str] = {}
    for weight in (400, 700):
        source = ROOT / f"tajawal-{weight}.ttf"
        temp = ASSETS / f".tajawal-{weight}.woff2"
        font = TTFont(source)
        font.recalcTimestamp = False
        font.flavor = "woff2"
        font.save(temp)
        font.close()
        font_data = temp.read_bytes()
        temp.unlink()
        fonts[weight] = hashed_asset(f"tajawal-{weight}", ".woff2", font_data)

    return {
        "hero": hero_name,
        "hero_size": hero_size,
        "hero_bytes": len(hero_data),
        "logo": logo_name,
        "logo_size": logo_size,
        "logo_bytes": len(logo_data),
        "font400": fonts[400],
        "font700": fonts[700],
        "font_bytes": {weight: (ASSETS / name).stat().st_size for weight, name in fonts.items()},
    }


def e(value: str) -> str:
    return html.escape(str(value), quote=True)


def whatsapp_url(message: str) -> str:
    return f"https://wa.me/{PHONE}?text={quote(message, safe='')}"


def render_page(page: dict[str, object], service: str, assets: dict[str, object]) -> str:
    chips = []
    for label, message in page["chips"]:  # type: ignore[index]
        chips.append(
            '<a href="' + e(whatsapp_url(message)) + '" target="_blank" rel="noopener noreferrer" '
            'data-contact="whatsapp" data-service="' + e(service) + '" data-position="chip">'
            + e(label) + '</a>'
        )
    perks = []
    for title, caption in page["perks"]:  # type: ignore[index]
        perks.append(
            '<article class="perk-card"><strong>' + e(title) + '</strong><span>' + e(caption) + '</span></article>'
        )
    faqs = []
    for question, answer in page["faqs"]:  # type: ignore[index]
        faqs.append('<details><summary>' + e(question) + '</summary><p>' + e(answer) + '</p></details>')

    replacements = {
        "@@TITLE@@": e(page["title"]),
        "@@DESCRIPTION@@": e(page["description"]),
        "@@CANONICAL@@": e(page["canonical"]),
        "@@EYEBROW@@": e(page["eyebrow"]),
        "@@H1@@": e(page["h1"]),
        "@@SUBTITLE@@": e(page["subtitle"]),
        "@@INTRO@@": e(page["intro"]),
        "@@CALL_TEXT@@": e(page["call_text"]),
        "@@POPUP_CALL_TEXT@@": e(page.get("popup_call_text", page["call_text"])),
        "@@WHATSAPP_TEXT@@": e(page["whatsapp_text"]),
        "@@POPUP_WHATSAPP_TEXT@@": e(page.get("popup_whatsapp_text", "أو راسلنا عبر واتساب")),
        "@@MAIN_WHATSAPP_URL@@": e(whatsapp_url(page["main_message"])),
        "@@POPUP_WHATSAPP_URL@@": e(whatsapp_url(page["popup_whatsapp"])),
        "@@POPUP_TITLE@@": e(page["popup_title"]),
        "@@POPUP_DESCRIPTION@@": e(page["popup_description"]),
        "@@CHIPS@@": "".join(chips),
        "@@PERKS@@": "".join(perks),
        "@@FAQS@@": "".join(faqs),
        "@@MAP_URL@@": e(MAP_URL),
        "@@SERVICE@@": e(service),
        "@@PHONE_DISPLAY@@": e(PHONE_DISPLAY),
        "@@LOGO@@": str(assets["logo"]),
        "@@HERO@@": str(assets["hero"]),
        "@@HERO_ABSOLUTE@@": e(f"{VERCEL_URL}/assets/{assets['hero']}"),
        "@@HERO_WIDTH@@": str(assets["hero_size"][0]),  # type: ignore[index]
        "@@HERO_HEIGHT@@": str(assets["hero_size"][1]),  # type: ignore[index]
        "@@FONT400@@": str(assets["font400"]),
        "@@FONT700@@": str(assets["font700"]),
        "@@GTM_ID@@": GTM_ID,
        "@@CSS@@": CSS_TEMPLATE.replace("@@FONT400@@", str(assets["font400"]))
        .replace("@@FONT700@@", str(assets["font700"]))
        .replace("@@HERO@@", str(assets["hero"])),
    }
    output = HTML_TEMPLATE
    for key, value in replacements.items():
        output = output.replace(key, value)
    if "@@" in output:
        raise ValueError(f"Unfilled template token for service {service}")
    return output


def main() -> None:
    assets = optimize_assets()
    for service, page in PAGES.items():
        rendered = render_page(page, service, assets)
        target = ROOT / str(page["file"])
        target.write_text(rendered, encoding="utf-8")
        print(f"generated {target.name}: {len(rendered.encode('utf-8')):,} bytes")

    routes = []
    for service in ("criminal", "family", "documentation"):
        routes.append({
            "src": "^/$",
            "has": [{"type": "query", "key": "service", "value": service}],
            "dest": "/" + str(PAGES[service]["file"]),
        })
    routes.append({"src": "^/$", "dest": "/index.html"})
    headers = []
    for name in (assets["hero"], assets["logo"], assets["font400"], assets["font700"]):
        headers.append({
            "source": "/assets/" + str(name),
            "headers": [{"key": "Cache-Control", "value": "public, max-age=31536000, immutable"}],
        })
    (ROOT / "vercel.json").write_text(
        json.dumps({"routes": routes, "headers": headers}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (ROOT / "robots.txt").write_text("User-agent: *\nAllow: /\n", encoding="utf-8")

    print(f"hero: {assets['hero_size']} {assets['hero_bytes']:,} bytes")
    print(f"logo: {assets['logo_size']} {assets['logo_bytes']:,} bytes")
    print("font bytes:", json.dumps(assets["font_bytes"], ensure_ascii=False))
    print("wrote vercel.json and robots.txt")


if __name__ == "__main__":
    main()
