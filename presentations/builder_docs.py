import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, hex_color):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def add_callout(doc, text, title="MUHIM ESLATMA:", hex_bg="F5F8FC", border_color="155EEF"):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    cell = tbl.cell(0, 0)
    cell.width = Inches(6.5)
    set_cell_background(cell, hex_bg)
    set_cell_margins(cell, top=140, bottom=140, left=200, right=200)

    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    r_t = p.add_run(f"{title}\n")
    r_t.bold = True
    r_t.font.name = "Calibri"
    r_t.font.size = Pt(10.5)
    r_t.font.color.rgb = RGBColor(21, 94, 239)

    r_c = p.add_run(text)
    r_c.font.name = "Calibri"
    r_c.font.size = Pt(10)
    r_c.font.color.rgb = RGBColor(23, 43, 77)

    # Empty spacer paragraph after table
    sp = doc.add_paragraph()
    sp.paragraph_format.space_before = Pt(2)
    sp.paragraph_format.space_after = Pt(4)

# =============================================================================
# BUILD SPEAKER NOTES (.DOCX)
# =============================================================================
def build_speaker_notes_docx(output_path):
    doc = docx.Document()
    
    # Page setup (Letter / A4 with 1-inch margins)
    for section in doc.sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.8)
        section.right_margin = Inches(0.8)

    # Document Header / Title
    p_meta = doc.add_paragraph()
    p_meta.paragraph_format.space_after = Pt(2)
    r_meta = p_meta.add_run("MILLIY STARTAP TADBIRI — TOSHKENT 2026  |  NUTQ SSENARIYSI")
    r_meta.bold = True
    r_meta.font.name = "Calibri"
    r_meta.font.size = Pt(9.5)
    r_meta.font.color.rgb = RGBColor(21, 94, 239)

    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_after = Pt(4)
    r_title = p_title.add_run("NEXTGEN AI — Spiker Nutqi va Sahnadagi Harakatlar Qo'llanmasi")
    r_title.bold = True
    r_title.font.name = "Calibri"
    r_title.font.size = Pt(22)
    r_title.font.color.rgb = RGBColor(18, 59, 114)

    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_after = Pt(12)
    r_sub = p_sub.add_run("180 kishilik zal (Vazirliklar, investorlar, sanoat rahbarlari, hakamlar) oldida 8–10 daqiqalik professional pitch nutqi.\nMuallif va ma'ruzachi: Shohjahon Abdullayev")
    r_sub.font.name = "Calibri"
    r_sub.font.size = Pt(11)
    r_sub.font.color.rgb = RGBColor(100, 116, 139)

    add_callout(doc, 
        "Taqdimot davomiyligi: Qat'iy 8–10 daqiqa. Sahnada dadil turing, ovoz tembrini xotirjam va ishonchli ushlang. "
        "Har bir slaydga 30–60 soniya vaqt ajrating. 'Biz o'ylayapmiz' yoki 'ehtimol' degan noaniq so'zlarni ishlatmang. "
        "Faqat faktlar, raqamlar va aniq texnik arxitekturaga tayaning.",
        title="SPIKER UCHUN STRATEGIK TAVSIYA:")

    slides_notes = [
        ("Slayd 01: Muqova / Titul", "00:00 – 00:45",
         "Kirish va auditoriya diqqatini jalb qilish",
         "Assalomu alaykum, hurmatli forum ishtirokchilari, muhtaram hakamlar hay'ati va investorlar! "
         "Mening ismim Shohjahon Abdullayev. Bugun men sizlarga O'zbekiston sanoati uchun eng og'riqli muammolardan birini "
         "hal etishga qaratilgan milliy texnologik yechimimiz — NEXTGEN AI platformasini taqdim etaman. "
         "Bizning shiorimiz: 'Har bir kilovatt — aqlli qaror, samarali kelajak'. "
         "NEXTGEN AI — bu korxona rahbarlari va bosh energetiklariga elektr energiyasi sarfini shaffof, "
         "tushunarli va tejamkor boshqarish imkonini beruvchi korporativ intellektual platformadir.",
         "Sahnaga chiqqanda zalga to'g'ri qarang, ekranga qaramasdan auditoriya bilan ko'z aloqasini o'rnating. Shiorni alohida pauza bilan ayting."),

        ("Slayd 02: Ijroiya xulosasi (Executive Summary)", "00:45 – 01:30",
         "Loyiha mohiyatini 30 soniyada ifodalash",
         "Keling, loyiha mohiyatini 30 soniyada tushuntirib beraman. Bugun O'zbekistondagi har qanday zavod yoki fabrika "
         "har oyda o'nlab, ba'zan yuzlab million so'm elektr energiyasiga to'laydi. Ammo rahbar bu summaning qanchasi samarasiz "
         "yo'qotilganini bilmaydi. NEXTGEN AI 4 ta ustun ustiga qurilgan: birinchidan — hisoblagichlar kesimida to'liq soatlik shaffoflik; "
         "ikkinchidan — kechki va dam olish kunlaridagi anomaliyalarni bir zumda aniqlash; uchinchidan — sun'iy intellekt orqali o'zbek tilida "
         "aniq biznes tavsiyalari; to'rtinchidan — ishlab chiqarish quvvatini pasaytirmagan holda oylik xarajatlarni 8–15% ga qisqartirish.",
         "Qo'l harakati bilan ekrandagi 4 ta kartani ko'rsating. 8-15% raqamini aniq va jarangdor talaffuz qiling."),

        ("Slayd 03: Asosiy muammo (The Problem)", "01:30 – 02:30",
         "Bozordagi real og'riq va xarajatlarning 'qora quti'si",
         "Nima uchun bu tizim aynan bugun kerak? Amaliyotda sanoat korxonalari 3 ta jiddiy qiyinchilikka duch kelmoqda. "
         "Birinchisi — ko'r-ko'rona iste'mol. Oylik hisob-faktura oy tugagandan so'ng keladi. Raqam 20% ga oshib ketgan, lekin qaysi sex "
         "yoki qaysi liniya ko'p sarflagani noma'lum. Ikkinchisi — kechki isrofgarchilik. Smena tugagan, ammo kompressorlar, sovutgichlar "
         "va transformatorlar bekorga ishlab turadi. Uchinchisi — mavjud ASKUE tizimlari faqat quruq raqamlarni yig'adi, bosh energetikda "
         "esa millionlab qatorlarni tahlil qilib xulosa chiqarishga vaqt va analitik vosita yo'q.",
         "Zaldagi biznes egalari va ishlab chiqaruvchilarga qaratib gapiring. 'Oy oxiridagi kutilmagan faktura' iborasiga urg'u bering."),

        ("Slayd 04: O'zbekiston uchun strategik ahamiyati", "02:30 – 03:30",
         "Davlat siyosati, PF-57 va tarif islohotlari",
         "Ushbu muammo davlat miqyosida nima uchun birinchi o'ringa chiqdi? O'zbekiston Respublikasi Prezidentining PF-57 farmoni "
         "va hukumat qarorlari bilan energetika bozorida tub islohotlar amalga oshirildi. Yuridik shaxslar uchun tariflar erkinlashtirildi "
         "va 1 kilovatt narxi 900–1000 so'mga ko'tarildi. Ilgari elektr arzon paytda bunga e'tibor bermagan rahbarlar, endi energiya xarajatlari "
         "mahsulot tannarxining 20–25 foizini tashkil etayotganini ko'rmoqda. Bundan tashqari, O'zbekiston-2030 strategiyasida sanoatda energiya "
         "sig'imini 30 foizga kamaytirish davlat darajasidagi qat'iy maqsad qilib belgilangan. NEXTGEN AI mana shu davlat siyosatiga to'liq xizmat qiladi.",
         "Huquqiy asoslarni (PF-57, O'zbekiston-2030) tilga olganda rasmiy, vazmin va professional ohangda gapiring."),

        ("Slayd 05: Bizning yechim (Our Solution)", "03:30 – 04:30",
         "Ma'lumotdan biznes intellektiga 5 bosqichli zanjir",
         "Biz bu muammoni qanday hal etamiz? NEXTGEN AI 5 bosqichli intellektual zanjir asosida ishlaydi. "
         "1-bosqich: Korxona o'z hisoblagich ma'lumotlarini kiritadi (Excel yoki ASKUE protokoli orqali). "
         "2-bosqich: Dastur ma'lumotlarni avtomatik tozalaydi va o'lchov birliklarini tekshiradi. "
         "3-bosqich: Energiya analitikasi faol quvvat (kW), sarf (kWh) va pik soatlar bo'yicha hisob-kitoblarni amalga oshiradi. "
         "4-bosqich: Sun'iy intellekt va statistik Z-Score modeli orqali me'yordan oshgan anomaliyalar va shubhali yuklamalar ajratib olinadi. "
         "5-bosqich: Rahbariyat va bosh muhandisga o'zbek tilida tayyor biznes harakati va tejamkorlik choralari taqdim etiladi.",
         "Diagrammani ketma-ketlikda tushuntiring. 'Quruq raqamdan tayyor biznes harakatiga' formulasi asosiy kalit so'zdir."),

        ("Slayd 06: Foydalanuvchi yo'li (User Journey)", "04:30 – 05:15",
         "Korxonani ulashdan natijaga qadar 9 qadam",
         "Korxona tizimdan qanday foydalanadi? Hech qanday murakkab serverlar yoki oylik o'rnatishlar shart emas. "
         "Barcha jarayon 9 ta oson qadamdan iborat: tashkilot profilini ochish, hisoblagichni kiritish, oylik yoki kunlik jurnalni yuklash. "
         "Qolgan barcha bosqichlar — validatsiya, sarf tahlili, anomaliya filtrlari, keyingi oy xarajatlari bashorati va AI tahlilnomasi "
         "avtomatik tarzda shakllanadi va Telegram orqali yuboriladi.",
         "Jarayonning qanchalik oson va tezkorligini his qildiring."),

        ("Slayd 07: Mahsulot platformasi (The Product)", "05:15 – 06:00",
         "Haqiqiy ishlayotgan veb ekotizim (nextgen-ai-87ff.vercel.app)",
         "Ekranda ko'rib turganingiz — bu loyihaning kelajakdagi orzusi emas. Bu hozirgi daqiqada nextgen-ai-87ff.vercel.app manzilida "
         "faol ishlab turgan NEXTGEN veb platformasining haqiqiy boshqaruv panelidir. "
         "Bu yerda rahbar umumiy sarfni, maksimal quvvatni, hisoblangan to'lovni va aniqlangan anomaliyalarni interaktiv ko'radi. "
         "Excel yuklash bo'limi, dinamik grafiklar va AI maslahatchi xonasi to'liq ishchi holatda.",
         "Ekranga ishora qilib, 'Bu real ishlab turgan tizim' degan gapni qat'iy ta'kidlang."),

        ("Slayd 08: Telegram ekotizimi (@nextgenuzz_bot)", "06:00 – 06:45",
         "O'zbekiston biznesi uchun mobil boshqaruv va push-ogohlantirish",
         "Nima uchun Telegram ekotizimini yaratdik? Chunki O'zbekiston biznesida Telegram — birlamchi operatsion aloqa vositasidir. "
         "Rahbar har kuni kompyuterda o'tirmasligi mumkin, lekin Telegramni doim tekshiradi. Bizning @nextgenuzz_bot orqali "
         "har qanday anomal sarf yuz berganda xabar 2 soniyada muhandis va rahbarning cho'ntagiga boradi. "
         "Shuningdek, /apk komandasi orqali korxona xodimlari bevosita Android mobil ilovamizni yuklab olishlari mumkin.",
         "Cho'ntagingizdagi telefonni ko'rsatib, 'energetika dispecheri endi cho'ntagingizda' deb ta'rif bering."),

        ("Slayd 09: Sun'iy intellekt va arxitektura", "06:45 – 07:30",
         "Gallyutsinatsiyasiz deterministik va generativ gibrid tizim",
         "Ko'pchilik texnik mutaxassislar haqli savol berishadi: 'Sun'iy intellekt sanoatda xato qilsa-chi? Gallyutsinatsiya bo'lsa nima bo'ladi?' "
         "Biz bu masalani fundamental hal qildik. NEXTGEN AI sof generativ model emas, bu ikki qatlamli gibrid tizimdir. "
         "Birinchi qatlamda barcha raqamlar, kilovattlar, tariflar va Z-score anomaliyalari qat'iy deterministik SQL va Python algoritmlari bilan hisoblanadi. "
         "Sun'iy intellekt esa faqatgina tayyor matematik faktlarni o'zbek tilida tushunarli sharhlab berish uchun xizmat qiladi. "
         "Texnologik stekimiz: Next.js 14, FastAPI, PostgreSQL/SQLite va Aiogram 3.",
         "Texnik hakamlarga qarab, arxitekturaning matematik ishonchliligiga alohida urg'u bering."),

        ("Slayd 10: Korporativ xavfsizlik (Enterprise Security)", "07:30 – 08:00",
         "Multi-tenant izolyatsiya va On-Premise imkoniyati",
         "Sanoatda korxona elektr sarfi — bu tijorat siridir. Biz ma'lumotlar xavfsizligini 4 ta darajada ta'minlaymiz: "
         "har bir korxona ma'lumotlari to'liq alohida konteynerda saqlanadi (Multi-tenancy), rollarga bo'lingan kirish tizimi (RBAC), "
         "har bir amalning audit jurnali yuritiladi va eng muhimi — yirik strategik korxonalar uchun tizimni to'g'ridan-to'g'ri "
         "korxonaning o'z ichki serverlariga (On-Premise) o'rnatish imkoniyati mavjud.",
         "Xavfsizlik va ma'lumotlar maxfiyligi qat'iy kafolatlanganini bildiring."),

        ("Slayd 11: Bozor hajmi va mijozlar", "08:00 – 08:30",
         "TAM/SAM/SOM va maqsadli sanoat segmentlari",
         "Bizning bozorimiz: O'zbekistonda 50,000 dan ortiq sanoat korxonasi faoliyat yuritadi (TAM: $60M+). "
         "Bizning birinchi navbatdagi maqsadimiz (SAM) — oylik elektr to'lovi 20 million so'mdan yuqori bo'lgan 8,000 ta korxona: "
         "to'qimachilik fabrikalari, oziq-ovqat ishlab chiqaruvchilar, qurilish materiallari va yirik omborxonalar. "
         "Dastlabki 2 yillik maqsadimiz (SOM) — 250 ta korxonani platformaga ulashdir.",
         "Segmentlar aniq va erishsa bo'ladigan ekanligini ifodalang."),

        ("Slayd 12: Raqobat ustunliklari", "08:30 – 09:00",
         "Mavjud ASKUE va xorijiy tizimlardan ustun tomonlarimiz",
         "Bozordagi raqobatchilar bilan taqqoslasak: an'anaviy ASKUE faqat hisob-kitob uchun xizmat qiladi, unda tejamkorlik aqli yo'q. "
         "Siemens yoki Schneider kabi xorijiy tizimlar o'n minglab dollar turadi, o'zbek tilida yo'q va mahalliy tariflarni tushunmaydi. "
         "Qo'lda Excel yuritish esa xatolar va kechikishlarga to'la. "
         "NEXTGEN AI — mahalliy tariflarni tushunadigan, o'zbek tilidagi AI maslahatchiga ega, Telegramga ulangan va 1 kunda ishga tushadigan qulay milliy yechimdir.",
         "Taqqoslash jadvaliga ishora qiling, raqobatchilarni kamsitmasdan xolis ustunliklarni ayting."),

        ("Slayd 13: Biznes model va monetizatsiya", "09:00 – 09:30",
         "B2B SaaS obuna va yuqori ROI",
         "Biznes modelimiz — B2B SaaS. Kichik sexlar uchun Starter tarifi oyiga 500 ming so'm. "
         "O'rta korxonalar uchun Pro tarifi — 1.5 million so'm. Yirik zavodlar uchun esa Enterprise shartnomaviy tarifi. "
         "Eng muhim iqtisodiy mantiq: agar o'rtacha fabrika oyiga 50 million so'm elektr to'lasa va NEXTGEN yordamida atigi 5% (2.5 million so'm) tejasa ham, "
         "platforma o'z xarajatini birinchi oydayoq ortig'i bilan qoplaydi.",
         "Unit economics va mijoz uchun ROI o'zini qoplashini tushuntiring."),

        ("Slayd 14: Rivojlanish xaritasi (Roadmap)", "09:30 – 10:00",
         "Bugungi holat, 5 ta pilot va xalqaro kengayish",
         "Bizning yo'l xaritamiz: 1-bosqich yakunlandi — ishlayotgan MVP, veb platforma, backend, Telegram bot va APK tayyor. "
         "Hozir 2-bosqichdamiz — 5 ta sanoat korxonasida 30 kunlik bepul pilot dasturini amalga oshirmoqdamiz. "
         "3-bosqichda 50 ta to'lovchi korxonaga yetamiz, 2027-yilda esa Markaziy Osiyo (Qozog'iston, Qirg'iziston) bozoriga chiqamiz.",
         "Bosqichlar ketma-ketligini ravon tushuntiring."),

        ("Slayd 15: Kutilayotgan iqtisodiy va ekologik samara", "10:00 – 10:30",
         "Korxona va davlat miqyosidagi o'lchanadigan foyda",
         "Loyiha qanday samara beradi? Bitta korxona misolida: har oyda 8–15% tejamkorlik, bu yiliga 75–140 million so'm degani! "
         "Bundan tashqari, reaktiv jarimalar yo'qoladi, uskunalar xizmat muddati 20% ga uzayadi. "
         "Davlat miqyosida: tarmoqdagi pik zo'riqishlar kamayadi, avariyalar qisqaradi, har 1000 kWh tejalgan elektr 450–500 kg CO2 chiqindisini kamaytiradi. "
         "Bu yashil iqtisodiyotga qo'shiladigan real hissadir.",
         "Raqamlar jiddiyligini ko'rsating."),

        ("Slayd 16: Yakuniy chaqiriq (Call to Action)", "10:30 – 11:00",
         "5 ta bepul pilot taklifi va investorlar bilan muloqot",
         "Hurmatli do'stlar va korxona rahbarlari! Bugun biz zaldagi 5 ta sanoat korxonasiga 30 kunlik to'liq bepul pilot loyihasini taklif qilamiz. "
         "Biz sizning tizimingizni ulaymiz, isroflarni topamiz va birinchi oydayoq tejamkorlik rejasini beramiz. "
         "Shuningdek, biz ushbu milliy startapni kengaytirish uchun investorlar va soha mutaxassislari bilan hamkorlikka ochiqmiz. "
         "Platformani hoziroq sinab ko'ring: nextgen-ai-87ff.vercel.app yoki Telegramda @nextgenuzz_bot. "
         "E'tiboringiz uchun katta rahmat! Savollaringizga mamnuniyat bilan javob beraman.",
         "Zalga samimiy minnatdorchilik bildiring, qo'llaringizni ochib savollarga tayyor ekanligingizni ifodalang.")
    ]

    for title, timing, goal, speech, tips in slides_notes:
        h = doc.add_heading(level=2)
        r_h = h.add_run(f"{title}  ({timing})")
        r_h.font.name = "Calibri"
        r_h.font.size = Pt(13)
        r_h.font.color.rgb = RGBColor(18, 59, 114)

        p_g = doc.add_paragraph()
        p_g.paragraph_format.space_after = Pt(2)
        r_g_lbl = p_g.add_run("Slayd maqsadi: ")
        r_g_lbl.bold = True
        r_g_lbl.font.color.rgb = RGBColor(21, 94, 239)
        p_g.add_run(goal)

        p_sp = doc.add_paragraph()
        p_sp.paragraph_format.space_before = Pt(3)
        p_sp.paragraph_format.space_after = Pt(4)
        r_sp_lbl = p_sp.add_run("Nutq matni:\n")
        r_sp_lbl.bold = True
        r_sp_lbl.font.color.rgb = RGBColor(15, 23, 42)
        r_sp = p_sp.add_run(f"“{speech}”")
        r_sp.italic = True
        r_sp.font.size = Pt(10)

        p_tp = doc.add_paragraph()
        p_tp.paragraph_format.space_before = Pt(2)
        p_tp.paragraph_format.space_after = Pt(10)
        r_tp_lbl = p_tp.add_run("Sahna harakati va intonatsiya: ")
        r_tp_lbl.bold = True
        r_tp_lbl.font.color.rgb = RGBColor(18, 166, 106)
        r_tp = p_tp.add_run(tips)
        r_tp.font.size = Pt(9.5)

    doc.save(output_path)
    print(f"Speaker notes saved to {output_path}")

# =============================================================================
# BUILD Q&A (.DOCX)
# =============================================================================
def build_qa_docx(output_path):
    doc = docx.Document()
    
    for section in doc.sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.8)
        section.right_margin = Inches(0.8)

    p_meta = doc.add_paragraph()
    r_meta = p_meta.add_run("NEXTGEN AI  |  HAKAMLAR VA INVESTORLAR UCHUN SAVOL-JAVOBLAR KONSEPTI")
    r_meta.bold = True
    r_meta.font.name = "Calibri"
    r_meta.font.size = Pt(9.5)
    r_meta.font.color.rgb = RGBColor(21, 94, 239)

    p_title = doc.add_paragraph()
    r_title = p_title.add_run("Hakamlar, Investorlar va Energetiklar Uchun 16 ta Strategik Savol-Javob")
    r_title.bold = True
    r_title.font.name = "Calibri"
    r_title.font.size = Pt(20)
    r_title.font.color.rgb = RGBColor(18, 59, 114)

    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_after = Pt(12)
    p_sub.add_run("Ushbu hujjat taqdimotdan keyingi savol-javob sessiyasida hakamlar hay'ati, xususiy investorlar, davlat idoralari va bosh energetiklar tomonidan berilishi mumkin bo'lgan eng o'tkir savollarga dalillarga asoslangan javoblarni o'z ichiga oladi.")

    qa_items = [
        ("1. ASKUE (ASKUE/ASUE) tizimlaridan farqingiz nimada? Ularning o'zi yetarli emasmi?",
         "ASKUE apparat darajasidagi ma'lumot yig'ish tizimi bo'lib, uning asosiy mijozi — 'Hududiy elektr tarmoqlari' (HET) hisoblanadi. Uning vazifasi korxonaga sarflangan elektr uchun hisob-faktura chiqarishdir. "
         "U yerda zavod rahbariga energiya tejash yo'llari, anomaliyalar sababi yoki optimallashtirish tavsiyalari ko'rsatilmaydi. "
         "NEXTGEN AI esa korxonaning o'zi uchun ishlaydigan tahliliy aqldir. Biz ASKUE ma'lumotlarini qabul qilib, ularni rahbar tushunadigan moliyaviy va operatsion tavsiyalarga aylantiramiz."),

        ("2. Sun'iy intellekt hisob-kitoblarda adashib (gallyutsinatsiya qilib) korxonaga zarar keltirmaydimi?",
         "Mutlaqo yo'q. Bizning tizimimizda sun'iy intellekt hisob-kitoblarni bajarmaydi. Barcha raqamlar, kilovattlar, pul to'lovlari, o'rtacha ko'rsatkichlar va Z-score anomaliya chegaralari 100% deterministik SQL va Python algoritmlari yordamida qat'iy matematik hisoblanadi. "
         "LLM esa faqat hisoblangan tayyor natijalarni o'zbek tilida professional izohlab berish uchun qo'llaniladi. Agar bazada ma'lumot bo'lmasa, AI taxmin qilmaydi, balki to'g'ridan-to'g'ri 'Ma'lumot yetarli emas' deb javob beradi."),

        ("3. Agar korxonada zamonaviy elektron hisoblagich bo'lmasa, ma'lumotlarni qanday kiritadi?",
         "NEXTGEN AI o'ta moslashuvchan. Birinchi bosqichda korxona har kuni yoki oy yakunida energetik to'ldiradigan oddiy Excel/CSV jurnallarini tizimga yuklashi mumkin. Tizim avtomatik ravishda jadvalni tozalaydi va grafiklar chizadi. "
         "Ikkinchi bosqichda esa biz ASKUE modemlari yoki MQTT/Modbus protokollari orqali to'g'ridan-to'g'ri avtomatik uzatishni sozlab beramiz."),

        ("4. Korxonaning elektr iste'moli tijorat siri hisoblanadi. Ma'lumotlar xavfsizligini qanday kafolatleysiz?",
         "Biz xavfsizlikni 3 ta mustahkam mexanizm bilan ta'minlaymiz: birinchidan, har bir tashkilot ma'lumotlari multi-tenant arxitekturada qat'iy izolyatsiya qilingan; ikkinchidan, rolga asoslangan kirish (RBAC) va xatti-harakatlarning to'liq audit jurnali yuritiladi; "
         "uchinchidan, yirik davlat yoki xususiy strategik korxonalar uchun tizimni internetga bog'lamagan holda to'liq korxonaning o'z ichki serverlariga (On-Premise) o'rnatib bera olamiz."),

        ("5. O'zbekistondagi tabaqalashtirilgan yangi tariflar tizimda qanday hisobga olingan?",
         "Tizimimiz O'zbekiston Respublikasi Vazirlar Mahkamasi qarorlariga muvofiq differensial tariflar matrisasini to'liq qo'llab-quvvatlaydi. "
         "Sutka 3 qismga bo'linadi: tungi arzon soatlar (23:00–06:00, 0.5x koeffitsiyent), yarim pik soatlari (06:00–17:00 va 21:00–23:00, 1.0x asosiy) hamda eng qimmat pik soatlari (17:00–21:00, 1.5x oshirilgan koeffitsiyent). "
         "NEXTGEN nafaqat to'lovni hisoblaydi, balki yuklamani qimmat pik soatlardan arzon tungi soatlarga ko'chirish bo'yicha tayyor tavsiyalar beradi."),

        ("6. Korxona birinchi oydayoq qancha mablag' tejashi mumkin?",
         "Sanoat tajribasi shuni ko'rsatadiki, korxona jiddiy kapital sarflamasdan turib ham, birinchi oyda 8–15% elektr xarajatini tejashi mumkin. "
         "Bu asosan kechki paytda va dam olish kunlarida bekorga ishlab turgan uskunalar, sovutgich va kompressorlar o'chirilishi, shuningdek, pik soatlardagi yuklamani to'g'rilash hisobiga erishiladi. "
         "Oyiga 80 million so'm to'laydigan korxona uchun bu 6.5–12 million so'm tejash demakdir."),

        ("7. Nima uchun Telegram bot yaratildi? Veb platformaning o'zi yetarli emasmi?",
         "O'zbekistonda rahbarlar va muhandislar har kuni veb-saytga kirishga vaqt topolmasligi mumkin, biroq Telegram ularning qo'lidan tushmaydi. "
         "Favqulodda holat — masalan, tunda yuklama me'yordan oshishi yoki qisqa tutashuv xavfi yuzaga kelganda Telegram orqali 2 soniyada xabar beriladi. Bu falokatning oldini oladi."),

        ("8. Siemens, Schneider Electric kabi xalqaro gigantlar bilan qanday raqobatlasha olasiz?",
         "Xorijiy tizimlar juda kuchli, ammo ularning narxi O'zbekiston o'rta biznesi uchun qimmatlik qiladi (o'n minglab dollar). Bundan tashqari, ularning tili rus yoki ingliz tilida, mahalliy milliy tariflarimizga moslashtirilmagan va Telegram integratsiyasi mavjud emas. "
         "NEXTGEN AI esa mahalliy sharoitga 100% moslashgan, o'zbek tilida gapiradigan va 1 kunda o'rnatiladigan hamyonbop milliy yechimdir."),

        ("9. Sizning biznes modelingiz qanday va qancha daromad kutmoqdasiz?",
         "Biznes modelimiz B2B SaaS (oylik va yillik obuna). Kichik korxonalar uchun Starter — 500,000 so'm/oy, o'rta korxonalar uchun Pro — 1,500,000 so'm/oy, yirik xoldinglar uchun Enterprise kelishuv asosida. "
         "Dastlabki 2 yilda 250 ta korxonani ulash orqali yillik takroriy daromadimiz (ARR) 4.5 milliard so'mdan ($360,000) oshadi."),

        ("10. Korxonaga tizimni joriy etish (onboarding) qancha vaqt oladi?",
         "Excel/CSV orqali yuklash rejimida joriy etish atigi 1 kun — hatto 1 soat vaqt oladi. Hisoblagich ma'lumotlari fayli yuklanishi bilan tahlillar darhol ko'rinadi. "
         "To'g'ridan-to'g'ri apparat integratsiyasi va maxsus datchiklar o'rnatish esa korxona kattaligiga qarab 3 kundan 7 kungacha vaqt talab qiladi."),

        ("11. Hozirda tizimning qaysi qismlari tayyor va sinovdan o'tgan?",
         "Platformaning to'liq MVP bosqichi yakunlangan: Vercel'da ishlayotgan frontend (nextgen-ai-87ff.vercel.app), FastAPI REST backend, SQLite/PostgreSQL ma'lumotlar bazasi, @nextgenuzz_bot Telegram boti va rasmiy kompilyatsiya qilingan Android APK ilovasi tayyor holatda."),

        ("12. Pilot dasturiga qanday korxonalarni qabul qilasiz va uning shartlari qanday?",
         "Biz 5 ta ishlab chiqarish korxonasini (to'qimachilik, oziq-ovqat, metallurgiya yoki yirik omborlar) 30 kunlik bepul pilotga qabul qilamiz. "
         "Yagona shart — korxona o'zining so'nggi 3–6 oylik elektr jurnallarini taqdim etishi va muhandislari tizim bilan ishlashga tayyor bo'lishi kerak. Biz ularga tejamkorlik natijasini isbotlab beramiz."),

        ("13. 'Hududiy elektr tarmoqlari' (HET) yoki Energetika vazirligi bilan hamkorlik qilasizmi?",
         "Ha, bu bizning strategik maqsadlarimizdan biridir. Biz HET bilan raqobatchi emasmiz, aksincha, ularning yuklamalarini muvozanatlashga yordam beruvchi hamkormiz. "
         "Tizimimiz korxonalarga pik soatlarda yuklamani kamaytirishni tavsiya qilish orqali umumiy davlat energetika tizimining zo'riqishini yumshatadi."),

        ("14. Korxonada internet uzilib qolsa, tizim qanday ishlaydi?",
         "Lokal server (On-premise) o'rnatilgan korxonalarda tizim internetga umuman bog'liq emas. "
         "Bulutli versiyada esa qurilmalarimizda lokal xotira (bufer) mavjud: ma'lumotlar apparatda to'planib turadi va internet tiklangach avtomatik sinxronizatsiya qilinadi. Hech qanday ko'rsatkich yo'qolmaydi."),

        ("15. Reaktiv quvvat va kosines fi (cos φ) monitoringi tizimda bormi?",
         "Ha, korxonalar uchun eng katta jarimalardan biri bu past kosines fi (0.85 dan past) uchun qo'llaniladigan sanktsiyalardir. "
         "NEXTGEN faol va to'liq quvvat ko'rsatkichlarini taqqoslab, reaktiv quvvat darajasini nazorat qiladi va kondensator qurilmalarini o'rnatish yoki sozlash zarurligini oldindan ogohlantiradi."),

        ("16. Loyihaning muallifi va jamoasi kimlardan iborat?",
         "Loyiha asoschisi va bosh dasturchisi — Shohjahon Abdullayev. Men dasturiy arxitektura, sun'iy intellekt integratsiyasi va energetika analitikasini mustaqil loyihalashtirib, ishchi platformani yaratdim. "
         "Keyingi bosqichda jamoamizga energetika auditi bo'yicha mutaxassislar va korporativ sotuvlar bo'yicha menejerlarni jalb qilishni rejalashtirganmiz.")
    ]

    for q, a in qa_items:
        hq = doc.add_heading(level=3)
        rq = hq.add_run(q)
        rq.font.name = "Calibri"
        rq.font.size = Pt(11.5)
        rq.font.color.rgb = RGBColor(18, 59, 114)

        pa = doc.add_paragraph()
        pa.paragraph_format.space_before = Pt(2)
        pa.paragraph_format.space_after = Pt(8)
        ra_lbl = pa.add_run("Javob: ")
        ra_lbl.bold = True
        ra_lbl.font.color.rgb = RGBColor(21, 94, 239)
        ra = pa.add_run(a)
        ra.font.size = Pt(10)
        ra.font.color.rgb = RGBColor(23, 43, 77)

    doc.save(output_path)
    print(f"Q&A document saved to {output_path}")

if __name__ == "__main__":
    out_dir = os.path.dirname(os.path.abspath(__file__))
    build_speaker_notes_docx(os.path.join(out_dir, "NEXTGEN_AI_Speaker_Notes.docx"))
    build_qa_docx(os.path.join(out_dir, "NEXTGEN_AI_QA.docx"))
