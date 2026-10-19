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
        "title": "مكتب محاماة في جدة | محامي للأفراد والشركات | العديني",
        "description": "مكتب محاماة في جدة. محامي للأفراد والشركات: استشارات وقضايا وعقود. اتصل أو راسلنا نحدد لك الخدمة المناسبة.",
        "eyebrow": "مكتب محاماة في جدة · للأفراد والشركات",
        "h1": "مكتب محاماة في جدة",
        "subtitle": "محامي في جدة للأفراد والشركات: استشارات وقضايا وعقود. اتصل أو راسلنا نحدد لك الخدمة المناسبة.",
        "intro": "مكتب محاماة في جدة يقدم استشارات وتمثيلاً قانونياً للأفراد والشركات، من القضايا الجزائية والأسرية إلى التجارية والعقارية وصياغة العقود.",
        "call_text": "استشارة قانونية الآن",
        "popup_call_text": "اتصل بالمكتب الآن",
        "whatsapp_text": "تواصل عبر واتساب",
        "main_message": "السلام عليكم، أرغب في استشارة قانونية. نوع المسألة: ...",
        "popup_title": "تحتاج إلى محامٍ في جدة؟",
        "popup_description": "اتصل بالمكتب الآن لتحديد الخدمة المناسبة.",
        "popup_whatsapp": "السلام عليكم، أرغب في استشارة قانونية. نوع المسألة: ...",
        "chips": [
            ("جزائي", "السلام عليكم، أرغب في استشارة بخصوص: جزائي."),
            ("أحوال شخصية", "السلام عليكم، أرغب في استشارة بخصوص: أحوال شخصية."),
            ("تجاري وعقود", "السلام عليكم، أرغب في استشارة بخصوص: تجاري وعقود."),
            ("عقاري وعمالي", "السلام عليكم، أرغب في استشارة بخصوص: عقاري وعمالي."),
        ],
        "faqs": [
            ("كيف أطلب استشارة قانونية؟", "يمكنك الاتصال بالمكتب على 0556799995 أو التواصل عبر واتساب، مع ذكر نوع المسألة وملخصها. يحدد المكتب معك آلية الاستشارة وموعدها والأتعاب بحسب نطاقها."),
            ("كيف تُحدد الأتعاب؟", "بحسب نوع الخدمة، وحجم المستندات، وطبيعة المسألة ونطاق العمل المطلوب. يتضح نطاق الخدمة والأتعاب بالاتفاق قبل البدء فيها."),
        ],
    },
    "criminal": {
        "file": "criminal.html",
        "canonical": f"{VERCEL_URL}/?service=criminal",
        "title": "محامي جنائي في جدة | مكتب عبدالعزيز العديني",
        "description": "دفاع وتمثيل في القضايا الجزائية بجدة: مخدرات، ابتزاز، تشهير، تزوير، جرائم إلكترونية، ونقض. اتصل بالمكتب أو راسلنا عبر واتساب.",
        "eyebrow": "القضايا الجنائية · جدة",
        "h1": "محامي جنائي في جدة",
        "subtitle": "دفاع وتمثيل أمام النيابة العامة والمحاكم الجزائية، بسرية تامة.",
        "intro": "نتولى قضايا المخدرات والابتزاز والتشهير والتزوير والنصب والاحتيال والجرائم الإلكترونية، وإعداد لوائح الاعتراض والنقض.",
        "call_text": "اتصل بمحامٍ جنائي الآن",
        "whatsapp_text": "استشارة جنائية عاجلة",
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
        "faqs": [
            ("ماذا أفعل إذا استُدعيت للتحقيق؟", "تواصل مع المكتب قبل الحضور إن أمكن، وأرسل ملخصاً بالواقعة ليوضح لك الخيارات."),
            ("هل يمكن بدء الاستشارة عن بُعد؟", "نعم، بالاتصال أو واتساب."),
        ],
    },
    "family": {
        "file": "family.html",
        "canonical": f"{VERCEL_URL}/?service=family",
        "title": "محامي أحوال شخصية في جدة | مكتب عبدالعزيز العديني",
        "description": "استشارات وتمثيل في قضايا الأحوال الشخصية بجدة: طلاق وخلع، نفقة وحضانة، ميراث وتركات. تواصل مع المكتب عبر الاتصال أو واتساب.",
        "eyebrow": "الأحوال الشخصية والميراث · جدة",
        "h1": "محامي أحوال شخصية في جدة",
        "subtitle": "طلاق وخلع، نفقة وحضانة، ميراث وتركات، بخصوصية وإجراءات واضحة.",
        "intro": "نتولى قضايا الطلاق والخلع والنفقة والحضانة والميراث وقسمة التركات وإثبات النسب.",
        "call_text": "اتصل بمحامي الأحوال الشخصية",
        "whatsapp_text": "استشارة أسرية عبر واتساب",
        "main_message": "السلام عليكم، أحتاج استشارة في قضية أسرية. نوعها: (طلاق / خلع / نفقة / حضانة / ميراث / إثبات النسب).",
        "popup_title": "قضية أسرية؟",
        "popup_description": "تحدث مع محامي الأحوال الشخصية الآن.",
        "popup_whatsapp": "السلام عليكم، أحتاج استشارة في قضية أسرية. نوعها: (طلاق / خلع / نفقة / حضانة / ميراث / إثبات النسب).",
        "chips": [
            ("طلاق وخلع", "السلام عليكم، أحتاج استشارة في جدة بخصوص الطلاق أو الخلع."),
            ("نفقة وحضانة", "السلام عليكم، أحتاج استشارة في جدة بخصوص النفقة أو الحضانة."),
            ("ميراث وتركات", "السلام عليكم، أحتاج استشارة في جدة بخصوص الميراث أو التركة."),
            ("إثبات النسب", "السلام عليكم، أحتاج استشارة في جدة بخصوص إثبات النسب."),
        ],
        "faqs": [
            ("كيف أبدأ دعوى الطلاق أو الخلع؟", "أرسل ملخصاً لموقفك ويوضح لك المكتب الخطوات والمستندات."),
            ("هل يمكن الاستشارة عن بُعد؟", "نعم، بالاتصال أو واتساب."),
        ],
    },
    "documentation": {
        "file": "documentation.html",
        "canonical": f"{VERCEL_URL}/?service=documentation",
        "title": "موثق معتمد في جدة: وكالات وإفراغ عقاري | مكتب العديني",
        "description": "توثيق الوكالات والإفراغ العقاري والإقرارات المالية وعقود الشركات في جدة. اتصل أو اسأل عن المستندات المطلوبة عبر واتساب.",
        "eyebrow": "خدمات التوثيق العدلي · جدة",
        "h1": "موثق معتمد في جدة",
        "subtitle": "توثيق الوكالات والإفراغ العقاري والإقرارات وعقود الشركات.",
        "intro": "نوثّق الوكالات والإفراغ والتوثيق العقاري والإقرارات المالية وعقود الشركات في جدة ومنطقة مكة المكرمة. الوكالة الإلكترونية تُصدر من المنصة الحكومية؛ تواصل معنا بشأن خدمات التوثيق التي يقدمها المكتب.",
        "call_text": "اتصل بالموثق الآن",
        "whatsapp_text": "اسأل عن توثيق وكالة",
        "main_message": "السلام عليكم، أرغب في توثيق: (وكالة / إفراغ عقاري / إقرار / عقد شركة). ما المستندات المطلوبة؟",
        "popup_title": "تريد توثيق وكالة أو إفراغ؟",
        "popup_description": "اتصل بالموثق الآن.",
        "popup_whatsapp": "السلام عليكم، أرغب في توثيق: (وكالة / إفراغ عقاري / إقرار / عقد شركة). ما المستندات المطلوبة؟",
        "chips": [
            ("توثيق وكالات", "السلام عليكم، أرغب في استشارة بخصوص: توثيق وكالات."),
            ("إفراغ عقاري", "السلام عليكم، أرغب في استشارة بخصوص: إفراغ عقاري."),
            ("إقرارات مالية", "السلام عليكم، أرغب في استشارة بخصوص: إقرارات مالية."),
            ("عقود شركات", "السلام عليكم، أرغب في استشارة بخصوص: عقود شركات."),
        ],
        "faqs": [
            ("ما المستندات المطلوبة لتوثيق وكالة؟", "تختلف حسب الوكالة، ويرسل لك المكتب القائمة بعد معرفة طلبك."),
            ("هل التوثيق متاح للشركات؟", "نعم، للأفراد والشركات والمنشآت."),
        ],
    },
}

CSS_TEMPLATE = r"""@font-face{font-family:Tajawal;src:url('./assets/@@FONT400@@') format('woff2');font-weight:400;font-display:swap}
@font-face{font-family:Tajawal;src:url('./assets/@@FONT700@@') format('woff2');font-weight:700;font-display:swap}
:root{color-scheme:light;--forest:#10271d;--forest-2:#17392a;--gold:#dfb66e;--ink:#18231d;--muted:#5d6b62;--paper:#f7f7f2;--line:#dce3dc;--white:#fff}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:var(--paper);color:var(--ink);font-family:Tajawal,Arial,sans-serif;font-size:17px;line-height:1.65}a{color:inherit}button{font:inherit}.skip-link{position:absolute;top:-60px;right:12px;z-index:200;background:#fff;padding:8px 12px;border-radius:8px}.skip-link:focus{top:8px}.site-header{height:74px;background:var(--forest);color:#fff;border-bottom:1px solid rgba(255,255,255,.13)}.header-inner{max-width:1120px;height:100%;margin:auto;padding:0 22px;display:flex;align-items:center;justify-content:space-between;gap:16px}.brand{display:flex;align-items:center;gap:11px;text-decoration:none;font-weight:700;line-height:1.2}.brand img{width:52px;height:49px;object-fit:contain}.brand-text{display:grid;gap:3px}.brand-text small{font-size:12px;font-weight:400;color:#d5ddd7}.header-call{display:inline-flex;align-items:center;gap:8px;color:#fff;text-decoration:none;font-weight:700;border:1px solid rgba(223,182,110,.7);border-radius:12px;padding:9px 15px;white-space:nowrap}.header-call:hover{background:rgba(223,182,110,.12)}
.hero{position:relative;overflow:hidden;background:radial-gradient(ellipse at 80% 10%,rgba(45,83,61,.38),transparent 50%),var(--forest);color:#fff}.hero-inner{max-width:1120px;min-height:470px;margin:auto;padding:48px 22px 42px;display:grid;grid-template-columns:minmax(0,1.25fr) minmax(280px,.75fr);gap:38px;align-items:center}.hero-copy{position:relative;z-index:1}.eyebrow{margin:0 0 9px;color:var(--gold);font-size:15px;font-weight:700;letter-spacing:.01em}.hero h1{max-width:720px;margin:0 0 14px;font-size:clamp(34px,5.1vw,55px);line-height:1.2;letter-spacing:-.02em}.hero-subtitle{max-width:680px;margin:0 0 21px;color:#e5ebe6;font-size:clamp(17px,2vw,21px);line-height:1.65}.hero-actions{display:flex;align-items:center;gap:12px;max-width:650px}.btn{min-height:54px;display:inline-flex;align-items:center;justify-content:center;gap:9px;border-radius:12px;padding:12px 21px;text-decoration:none;font-weight:700;line-height:1.3;text-align:center;transition:transform .16s ease,background .16s ease}.btn:hover{transform:translateY(-1px)}.btn-call{background:var(--gold);color:#18251e;flex:1.25;box-shadow:0 5px 18px rgba(0,0,0,.16)}.btn-wa{border:1px solid rgba(255,255,255,.55);color:#fff;flex:1;background:rgba(255,255,255,.04)}.btn-wa:hover{background:rgba(255,255,255,.11)}.trustline{margin:14px 0 15px;color:#dce5df;font-size:15px}.service-chips{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 16px}.service-chips a{display:inline-flex;align-items:center;justify-content:center;min-height:38px;padding:6px 13px;border:1px solid rgba(223,182,110,.55);border-radius:999px;color:#f4e4c4;text-decoration:none;font-size:14px;line-height:1.3}.service-chips a:hover{background:rgba(223,182,110,.12);border-color:var(--gold)}.intro{max-width:650px;margin:0;color:#d9e2dc;font-size:16px}.hero-visual{display:none}.contact-details{background:var(--white);border-bottom:1px solid var(--line)}.details-inner{max-width:1120px;margin:auto;padding:17px 22px;display:flex;align-items:center;justify-content:space-between;gap:14px;color:var(--muted);font-size:15px}.details-inner strong{color:var(--ink)}.map-link{color:#275d43;font-weight:700;text-decoration-thickness:1px;text-underline-offset:3px;white-space:nowrap}
.faq-section{max-width:960px;margin:0 auto;padding:34px 22px 28px}.faq-section h2{margin:0 0 14px;font-size:23px;line-height:1.3}.faq-list{display:grid;grid-template-columns:1fr 1fr;gap:12px}.faq-list details{background:#fff;border:1px solid var(--line);border-radius:13px;padding:13px 16px}.faq-list summary{font-weight:700;cursor:pointer}.faq-list details p{margin:9px 0 0;color:var(--muted);font-size:15px}.site-footer{background:#10271d;color:#dce5df;padding:21px 22px calc(21px + env(safe-area-inset-bottom))}.footer-inner{max-width:1120px;margin:auto;display:flex;align-items:center;justify-content:space-between;gap:14px}.footer-name{font-weight:700}.footer-note{font-size:13px;color:#c0ccc3}.footer-links{display:flex;gap:15px;align-items:center}.footer-links button{background:none;border:0;padding:4px 0;color:#f1d7a8;text-decoration:underline;text-underline-offset:3px;cursor:pointer;font-size:14px}
.mobile-bar{display:none}.info-dialog{width:min(560px,calc(100% - 32px));max-height:min(78vh,680px);overflow:auto;border:0;border-radius:18px;padding:22px 23px;background:#fff;color:var(--ink);box-shadow:0 20px 70px rgba(0,0,0,.3)}.info-dialog::backdrop{background:rgba(7,20,13,.64)}.dialog-head{display:flex;align-items:center;justify-content:space-between;gap:10px}.dialog-head h2{margin:0;font-size:22px}.dialog-close{border:1px solid var(--line);background:#f5f7f4;border-radius:9px;padding:6px 12px;cursor:pointer}.info-dialog p{font-size:15px;color:#4d5b52}.info-dialog h3{font-size:17px;margin:18px 0 5px}.welcome-dialog{width:min(470px,calc(100% - 32px));max-height:min(82vh,620px);overflow:auto;border:0;border-radius:23px;padding:25px 25px 20px;background:#fff;color:var(--ink);box-shadow:0 24px 80px rgba(0,0,0,.35)}.welcome-dialog::backdrop{background:rgba(7,20,13,.68)}.welcome-kicker{display:block;margin-bottom:4px;color:#815d2c;font-size:14px;font-weight:700}.welcome-dialog h2{margin:0 0 6px;color:var(--forest);font-size:25px;line-height:1.3}.welcome-dialog p{margin:0 0 15px;color:#536158}.welcome-dialog .popup-call{width:100%;min-height:54px;background:var(--gold);color:#15231b;font-size:18px}.popup-wa{display:block;margin-top:11px;padding:9px 12px;text-align:center;border:1px solid #a9b7ad;border-radius:10px;color:#24573e;text-decoration:none;font-weight:700;font-size:15px}.popup-dismiss{display:block;margin:13px auto 0;border:0;background:none;color:#526259;text-decoration:underline;text-underline-offset:3px;cursor:pointer;font-size:14px}.welcome-dialog[open]{animation:dialog-in .18s ease-out}@keyframes dialog-in{from{opacity:0;transform:translateY(7px)}to{opacity:1;transform:translateY(0)}}
@media(min-width:861px){.hero-inner{grid-template-columns:minmax(0,1.2fr) minmax(300px,.8fr)}.hero-visual{display:block;min-height:350px;max-height:440px;border:1px solid rgba(223,182,110,.35);border-radius:25px;background:linear-gradient(180deg,rgba(16,39,29,.08),rgba(16,39,29,.4)),url('./assets/@@HERO@@') center 38%/cover no-repeat;box-shadow:0 18px 45px rgba(0,0,0,.2)}}
@media(max-width:760px){body{font-size:16px}.site-header{height:64px}.header-inner{padding:0 15px}.brand img{width:45px;height:43px}.brand{gap:8px}.brand-text{font-size:14px}.brand-text small{font-size:10px}.header-call{padding:8px 10px;font-size:14px}.hero-inner{display:block;min-height:0;padding:25px 18px 21px}.hero h1{font-size:clamp(31px,8.5vw,39px);line-height:1.23;margin-bottom:9px}.hero-subtitle{font-size:17px;line-height:1.5;margin-bottom:14px}.hero-actions{display:grid;grid-template-columns:1fr;gap:9px}.btn{min-height:50px;padding:11px 15px}.btn-call{font-size:18px}.btn-wa{min-height:43px;font-size:15px}.trustline{margin:11px 0;font-size:14px}.service-chips{gap:7px;margin-bottom:12px}.service-chips a{min-height:35px;padding:6px 11px;font-size:13px}.intro{font-size:15px;line-height:1.55}.details-inner{padding:14px 18px;display:block;font-size:14px}.map-link{display:inline-block;margin-top:5px}.faq-section{padding:24px 16px 27px}.faq-section h2{font-size:20px}.faq-list{grid-template-columns:1fr;gap:8px}.faq-list details{padding:11px 13px}.site-footer{padding:17px 16px calc(84px + env(safe-area-inset-bottom))}.footer-inner{align-items:flex-start;flex-direction:column;gap:8px}.footer-links{gap:15px}.mobile-bar{position:fixed;z-index:30;inset:auto 0 0;display:grid;grid-template-columns:1fr 1fr;gap:8px;padding:9px 12px calc(9px + env(safe-area-inset-bottom));background:rgba(16,39,29,.97);border-top:1px solid rgba(255,255,255,.16)}.mobile-bar a{min-height:45px;display:flex;align-items:center;justify-content:center;border-radius:10px;text-decoration:none;font-weight:700;font-size:15px}.mobile-call{background:var(--gold);color:#18251e}.mobile-wa{border:1px solid rgba(255,255,255,.58);color:#fff}.popup-open .mobile-bar{display:none}.welcome-dialog{position:fixed;inset:auto 0 0;margin:0;width:100%;max-width:none;max-height:min(320px,calc(100dvh - 215px));overflow:auto;border-radius:20px 20px 0 0;padding:18px 18px calc(14px + env(safe-area-inset-bottom));}.welcome-dialog::backdrop{background:rgba(7,20,13,.43)}.welcome-dialog h2{font-size:22px}.welcome-dialog p{font-size:15px;margin-bottom:11px}.welcome-dialog .popup-call{min-height:49px;font-size:17px}.popup-wa{margin-top:8px;padding:7px 10px}.popup-dismiss{position:sticky;bottom:0;margin-top:10px;padding:5px 8px;background:#fff}.info-dialog{max-height:calc(100dvh - 40px);padding:18px}.info-dialog p{font-size:14px}}
@media(max-height:600px) and (max-width:760px){.site-header{height:56px}.hero-inner{padding-top:14px;padding-bottom:14px}.hero h1{font-size:30px}.hero-subtitle{font-size:15px;margin-bottom:10px}.trustline{margin:8px 0}.service-chips{margin-bottom:8px}.welcome-dialog{max-height:calc(100dvh - 185px);padding-top:12px;padding-bottom:10px}.welcome-dialog p{margin-bottom:8px}.welcome-dialog .popup-call{min-height:44px}.popup-wa{margin-top:6px}.popup-dismiss{margin-top:5px}}
@media(max-width:360px){.header-inner{padding:0 10px}.brand{gap:6px}.brand img{width:40px;height:38px}.brand-text{font-size:13px}.brand-text small{display:none}.header-call{font-size:12px;padding:7px 8px;gap:5px}}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}*,*::before,*::after{animation-duration:.01ms!important;animation-iteration-count:1!important;transition-duration:.01ms!important}}
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
<a class="brand" href="./" aria-label="مكتب عبدالعزيز العديني للمحاماة، بداية الصفحة"><img src="./assets/@@LOGO@@" width="52" height="49" alt="شعار مكتب العديني" fetchpriority="high" decoding="async"><span class="brand-text">عبدالعزيز العديني<small>للمحاماة والاستشارات القانونية</small></span></a>
<a class="header-call" href="tel:+966556799995" data-contact="phone" data-service="@@SERVICE@@" data-position="hero" aria-label="اتصل بمكتب العديني على 055 679 9995">اتصل: <span dir="ltr">@@PHONE_DISPLAY@@</span></a>
</div></header>
<main id="main">
<section class="hero" aria-labelledby="hero-title"><div class="hero-inner"><div class="hero-copy">
<p class="eyebrow">@@EYEBROW@@</p>
<h1 id="hero-title">@@H1@@</h1>
<p class="hero-subtitle">@@SUBTITLE@@</p>
<div class="hero-actions"><a class="btn btn-call" href="tel:+966556799995" data-contact="phone" data-service="@@SERVICE@@" data-position="hero">@@CALL_TEXT@@</a><a class="btn btn-wa" href="@@MAIN_WHATSAPP_URL@@" target="_blank" rel="noopener noreferrer" data-contact="whatsapp" data-service="@@SERVICE@@" data-position="hero">@@WHATSAPP_TEXT@@</a></div>
<p class="trustline">سرية تامة في التعامل مع قضيتك · جدة، طريق صاري، حي الروضة</p>
<nav class="service-chips" aria-label="اختر موضوع الاستفسار">@@CHIPS@@</nav>
<p class="intro">@@INTRO@@</p>
</div><div class="hero-visual" aria-hidden="true"></div></div></section>
<section class="faq-section" aria-labelledby="faq-title"><h2 id="faq-title">أسئلة شائعة</h2><div class="faq-list">@@FAQS@@</div></section>
<section class="contact-details" aria-label="عنوان المكتب"><div class="details-inner"><span><strong>مكتب العديني للمحاماة</strong> · جدة · طريق صاري · حي الروضة · 23326</span><a class="map-link" href="@@MAP_URL@@" target="_blank" rel="noopener noreferrer">افتح موقع المكتب على خرائط Google</a></div></section>
</main>
<footer class="site-footer"><div class="footer-inner"><div><div class="footer-name">مكتب عبدالعزيز العديني للمحاماة والاستشارات القانونية</div><div class="footer-note">المحتوى للتعريف بالخدمة ولا يُعد رأيًا قانونيًا في واقعة بعينها.</div></div><div class="footer-links"><button type="button" data-dialog="privacy-dialog">سياسة الخصوصية</button><button type="button" data-dialog="terms-dialog">شروط الاستخدام</button></div></div></footer>
<nav class="mobile-bar" aria-label="تواصل سريع"><a class="mobile-call" href="tel:+966556799995" data-contact="phone" data-service="@@SERVICE@@" data-position="sticky">اتصل الآن</a><a class="mobile-wa" href="@@MAIN_WHATSAPP_URL@@" target="_blank" rel="noopener noreferrer" data-contact="whatsapp" data-service="@@SERVICE@@" data-position="sticky">واتساب</a></nav>
<dialog id="privacy-dialog" class="info-dialog" aria-labelledby="privacy-title"><div class="dialog-head"><h2 id="privacy-title">سياسة الخصوصية</h2><button type="button" class="dialog-close" data-close-dialog>إغلاق</button></div><p>هذه الصفحة للتعريف بخدمات مكتب عبدالعزيز العديني للمحاماة وتيسير التواصل معه. لا تحتوي على نموذج يجمع أسماء الزوار أو مستنداتهم.</p><h3>التواصل والمعلومات</h3><p>عند الاتصال أو استخدام واتساب، تقدم معلوماتك مباشرة عبر الوسيلة التي اخترتها. يرجى إرسال ملخص أولي فقط والتنسيق مع المكتب قبل إرسال مستندات أو معلومات حساسة.</p><h3>قياس أداء الإعلانات</h3><p>تستخدم الصفحة Google Tag Manager وGoogle Ads لقياس أداء الإعلانات والتفاعل مع أزرار الاتصال وواتساب. يسجل حدث النقر وسيلة التواصل ونوع الخدمة وموضع الزر، ولا يتضمن محتوى المكالمة أو رسالة واتساب. قد تعالج Google بيانات تقنية عن الزيارة وفق سياساتها وإعدادات الموافقة المعمول بها.</p><h3>تخزين الجلسة</h3><p>تحفظ الصفحة علامة مؤقتة في جلسة التصفح لمنع تكرار نافذة التواصل، دون حفظ بيانات شخصية أو استخدامها للتعرف عليك.</p><h3>للاستفسار</h3><p>تواصل مع المكتب على <a href="tel:+966556799995" dir="ltr">055 679 9995</a>.</p></dialog>
<dialog id="terms-dialog" class="info-dialog" aria-labelledby="terms-title"><div class="dialog-head"><h2 id="terms-title">شروط الاستخدام</h2><button type="button" class="dialog-close" data-close-dialog>إغلاق</button></div><p>يعرض الموقع معلومات تعريفية عن المكتب وخدماته، ولا يُعد محتواه العام رأيًا قانونيًا في واقعة بعينها.</p><h3>طلب الخدمة</h3><p>التواصل الأولي أو إرسال رسالة لا يعني قبول التكليف أو بدء التمثيل القانوني. يتحدد نطاق الخدمة والأتعاب والالتزامات وفق الاتفاق مع المكتب.</p><h3>النتائج والإجراءات</h3><p>تتوقف النتائج على الوقائع والمستندات والإجراءات وتقدير الجهات المختصة. لا يتضمن الموقع ضمانًا لنتيجة قضائية أو مدة محددة لإنجاز المعاملة.</p><h3>الروابط الخارجية</h3><p>تفتح أزرار الاتصال وواتساب والخرائط تطبيقات أو خدمات خارج الصفحة، وفق إعدادات جهازك وشروط مزوديها.</p></dialog>
<dialog id="welcome-dialog" class="welcome-dialog" aria-labelledby="welcome-title" aria-describedby="welcome-description"><span class="welcome-kicker">مكتب العديني للمحاماة · جدة</span><h2 id="welcome-title">@@POPUP_TITLE@@</h2><p id="welcome-description">@@POPUP_DESCRIPTION@@</p><a class="btn popup-call" href="tel:+966556799995" data-contact="phone" data-service="@@SERVICE@@" data-position="popup">@@POPUP_CALL_TEXT@@</a><a class="popup-wa" href="@@POPUP_WHATSAPP_URL@@" target="_blank" rel="noopener noreferrer" data-contact="whatsapp" data-service="@@SERVICE@@" data-position="popup">@@POPUP_WHATSAPP_TEXT@@</a><button class="popup-dismiss" type="button" data-close-welcome>متابعة تصفح الصفحة</button></dialog>
<script>
(()=>{'use strict';
const service=document.body.dataset.service||'general';
const dataLayer=window.dataLayer=window.dataLayer||[];
document.addEventListener('click',event=>{const link=event.target.closest('a[data-contact]');if(!link)return;const method=link.dataset.contact;const position=link.dataset.position||'hero';const selected=link.dataset.service||service;dataLayer.push({event:'contact_click',contact_channel:method,contact_placement:position,legal_service:selected,landing_service:service,contact_method:method,service:selected,position});});
document.querySelectorAll('[data-dialog]').forEach(button=>button.addEventListener('click',()=>document.getElementById(button.dataset.dialog).showModal()));
document.querySelectorAll('[data-close-dialog]').forEach(button=>button.addEventListener('click',()=>button.closest('dialog').close()));
const welcome=document.getElementById('welcome-dialog');document.querySelector('[data-close-welcome]').addEventListener('click',()=>welcome.close());
welcome.addEventListener('close',()=>{document.documentElement.classList.remove('popup-open');});
const preview=new URLSearchParams(location.search).get('popup')==='1';let seen=false;try{seen=!preview&&sessionStorage.getItem('aledini-contact-welcome')==='1';}catch{}
const reveal=()=>{if(seen||document.hidden||welcome.open||typeof welcome.showModal!=='function')return false;welcome.showModal();document.documentElement.classList.add('popup-open');seen=true;if(!preview){try{sessionStorage.setItem('aledini-contact-welcome','1');}catch{}}dataLayer.push({event:'welcome_popup_view',landing_service:service,service,position:'popup'});return true;};
if(!seen){window.setTimeout(()=>{if(reveal())return;const retry=()=>{if(reveal())document.removeEventListener('visibilitychange',retry);};document.addEventListener('visibilitychange',retry);},180);}
document.querySelectorAll('dialog').forEach(dialog=>dialog.addEventListener('click',event=>{if(event.target===dialog){const box=dialog.getBoundingClientRect();if(event.clientX<box.left||event.clientX>box.right||event.clientY<box.top||event.clientY>box.bottom)dialog.close();}}));
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
