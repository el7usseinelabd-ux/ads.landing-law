# صفحات هبوط مكتب المحامي عبدالعزيز عبدالله العديني للمحاماة والاستشارات القانونية

موقع صفحات HTML ثابتة بالعربية، بتصميم موحّد ومحتوى خاص بكل خدمة.

## مصدر المحتوى والبناء
- `tools/services.json`: نصوص الصفحات والكلمات المفتاحية والعناوين والأوصاف لكل خدمة.
- `tools/landing_template.html`: قالب التصميم المتجاوب.
- `tools/build_landing_pages.py`: مولّد الصفحات وملف توجيه Vercel ولوحة أصول الإعلانات.
- `google-ads-assets.html`: روابط Final URL وكلمات مفتاحية وعناوين وأوصاف مقترحة لكل مجموعة.

## التصميم والمراجعة
- تصميم موحّد جديد يعتمد على واجهة متجاوبة وبطاقات خدمات برسائل واتساب مخصصة.
- نافذة التواصل تظهر مرة واحدة في الجلسة، مع الاتصال أولًا ثم واتساب.
- أحداث التفاعل: `click_call` و`click_whatsapp` وتتضمن `service` و`position`.
- رابط الخريطة المعتمد في الإعدادات: https://share.google/wMPubnTMSV2CPrDpF
- التذييل يتضمن سياسة الخصوصية وشروط الاستخدام والتنبيه القانوني التعريفي.

## صفحات السياسات
- [سياسة الخصوصية](https://adslanding-law.vercel.app/privacy.html)
- [شروط الاستخدام](https://adslanding-law.vercel.app/terms.html)

## روابط صفحات الهبوط
| الخدمة | Final URL |
|---|---|
| عامة | https://adslanding-law.vercel.app/ |
| تجارية | https://adslanding-law.vercel.app/commercial.html |
| الشركات والحوكمة | https://adslanding-law.vercel.app/companies.html |
| منازعات الشركاء | https://adslanding-law.vercel.app/partnership.html |
| القضايا العمالية | https://adslanding-law.vercel.app/labor.html |
| القضايا العقارية | https://adslanding-law.vercel.app/realestate.html |
| الأحوال الشخصية والميراث | https://adslanding-law.vercel.app/family.html |
| صياغة ومراجعة العقود | https://adslanding-law.vercel.app/contracts.html |
| القضايا الجنائية | https://adslanding-law.vercel.app/criminal.html |
| التنفيذ وتحصيل الحقوق | https://adslanding-law.vercel.app/execution.html |
| الاستشارات القانونية | https://adslanding-law.vercel.app/consultation.html |
| التوثيق العدلي | https://adslanding-law.vercel.app/documentation.html |

تبقى روابط الاستعلام القديمة مثل `/?service=criminal` و`/?service=family` مدعومة عبر `vercel.json`. الرابط العام `/` لم يتغير.

## البناء محليًا
يتطلب Python 3:
```bash
python3 tools/build_landing_pages.py
```
يفحص المولّد حد 30 حرفًا للعناوين و90 حرفًا للأوصاف، ثم ينشئ الصفحات الثابتة و`vercel.json` و`google-ads-assets.html`. ملفات HTML جاهزة للنشر على Vercel دون خطوة بناء في الاستضافة.

## القياس
تستخدم الصفحات حاوية GTM الحالية `GTM-KKHH6SBP`، وتسجل `contact_click` مع الخدمة وطريقة التواصل ومكان الزر ومعلمات UTM وgclid. النقر لا يثبت إجراء مكالمة أو إرسال رسالة. يجب اختبار الوسوم والتحويلات عبر GTM/Tag Assistant قبل الاعتماد على بيانات الأداء.

## أمور تتطلب تأكيدًا قبل إطلاق الحملات
- القضايا العمالية كانت موثقة كخدمة متوقفة؛ الصفحة جاهزة تقنيًا لكنها موسومة بانتظار التأكيد ولا تُفعّل حملتها قبل تأكيد توفر الخدمة.
- التوثيق العدلي يحتاج تأكيد الصفة المهنية الدقيقة ونطاق الخدمات قبل نشر الإعلان.
- الكلمات والعناوين والأوصاف اقتراحات أولية، وتحتاج مراجعة مع تقرير مصطلحات البحث والكلمات السلبية والميزانية والاستهداف الجغرافي.
- تأكد من رقم الهاتف والعنوان والمسمى المهني، وراجع سياسة الخصوصية والموافقة على القياس في GTM.
- صفحات الحملات تستخدم `noindex, nofollow` عن قصد؛ لا يوجد sitemap في هذه النسخة.

## نطاق التغيير
لم تُنشأ أو تُعدّل حملات Google Ads أو إعدادات GTM أو إعدادات Vercel. سيجري النشر تلقائيًا إذا كان Vercel مرتبطًا بفرع `main`.
