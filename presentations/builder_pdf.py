import os
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.utils import simpleSplit

# 16:9 Landscape Dimensions
WIDTH = 13.333 * inch
HEIGHT = 7.5 * inch

# Colors
PRIMARY_BLUE = colors.HexColor("#155EEF")
DEEP_BLUE = colors.HexColor("#123B72")
DARK_NAVY = colors.HexColor("#0F172A")
DARK_TEXT = colors.HexColor("#172B4D")
SECONDARY_TEXT = colors.HexColor("#64748B")
LIGHT_BG = colors.HexColor("#F5F8FC")
CARD_BG = colors.HexColor("#FFFFFF")
BORDER_COLOR = colors.HexColor("#E4EAF2")
SUCCESS_GREEN = colors.HexColor("#12A66A")
WARNING_AMBER = colors.HexColor("#F59E0B")
WHITE = colors.HexColor("#FFFFFF")
LIGHT_BLUE_TEXT = colors.HexColor("#BAEDFD")
LIGHT_BLUE_SUB = colors.HexColor("#93C5FD")
CARD_DARK_BG = colors.HexColor("#18427D")
CARD_DARK_BORDER = colors.HexColor("#2D5FAA")

def pt_to_y(from_top):
    """Converts a top-down y coordinate (in inches) to ReportLab bottom-up y coordinate."""
    return HEIGHT - (from_top * inch)

def draw_header(c, category, title, subtitle=""):
    c.saveState()
    # Category tag
    c.setFont("Helvetica-Bold", 9.5)
    c.setFillColor(PRIMARY_BLUE)
    c.drawString(0.8 * inch, HEIGHT - 0.65 * inch, category.upper())

    # Title
    c.setFont("Helvetica-Bold", 20)
    c.setFillColor(DARK_NAVY)
    c.drawString(0.8 * inch, HEIGHT - 1.05 * inch, title)

    # Subtitle
    if subtitle:
        c.setFont("Helvetica", 11)
        c.setFillColor(SECONDARY_TEXT)
        c.drawString(0.8 * inch, HEIGHT - 1.35 * inch, subtitle)
    c.restoreState()

def draw_footer(c, current_slide, total_slides=20):
    c.saveState()
    # Divider line
    c.setStrokeColor(BORDER_COLOR)
    c.setLineWidth(1)
    c.line(0.8 * inch, 0.65 * inch, (13.333 - 0.8) * inch, 0.65 * inch)

    # Left text
    c.setFont("Helvetica", 8.5)
    c.setFillColor(SECONDARY_TEXT)
    c.drawString(0.8 * inch, 0.42 * inch, "NEXTGEN AI — O'zbekiston sanoati uchun energiya intellekti platformasi  |  Muallif: Shohjahon Abdullayev")

    # Right text
    c.setFont("Helvetica-Bold", 8.5)
    c.setFillColor(PRIMARY_BLUE)
    c.drawRightString((13.333 - 0.8) * inch, 0.42 * inch, f"{current_slide:02d} / {total_slides:02d}")
    c.restoreState()

def draw_card(c, x_in, y_top_in, w_in, h_in, bg_color=CARD_BG, border_color=BORDER_COLOR, radius=6):
    c.saveState()
    x = x_in * inch
    y = HEIGHT - (y_top_in + h_in) * inch
    w = w_in * inch
    h = h_in * inch

    c.setFillColor(bg_color)
    if border_color:
        c.setStrokeColor(border_color)
        c.setLineWidth(1)
        c.roundRect(x, y, w, h, radius, stroke=1, fill=1)
    else:
        c.roundRect(x, y, w, h, radius, stroke=0, fill=1)
    c.restoreState()

def draw_card_accent(c, x_in, y_top_in, w_in, accent_color, bar_h_in=0.08):
    c.saveState()
    x = x_in * inch
    y = HEIGHT - (y_top_in + bar_h_in) * inch
    w = w_in * inch
    h = bar_h_in * inch
    c.setFillColor(accent_color)
    c.rect(x, y, w, h, stroke=0, fill=1)
    c.restoreState()

def draw_text_lines(c, lines, x_in, y_start_top_in, font_name="Helvetica", font_size=10, color=DARK_TEXT, line_height_pt=14):
    c.saveState()
    c.setFont(font_name, font_size)
    c.setFillColor(color)
    x = x_in * inch
    y = HEIGHT - (y_start_top_in * inch)
    for line in lines:
        c.drawString(x, y, line)
        y -= (line_height_pt / 72.0) * inch
    c.restoreState()

def build_pdf(output_path):
    c = canvas.Canvas(output_path, pagesize=(WIDTH, HEIGHT))

    # =========================================================================
    # SLIDE 01 — MUQOVA / TITLE SLIDE (Hero Dark Blue)
    # =========================================================================
    c.setFillColor(DEEP_BLUE)
    c.rect(0, 0, WIDTH, HEIGHT, stroke=0, fill=1)

    # Top accent strip
    c.setFillColor(PRIMARY_BLUE)
    c.rect(0, HEIGHT - 0.12 * inch, WIDTH, 0.12 * inch, stroke=0, fill=1)

    # Category Pill
    draw_card(c, 1.0, 1.1, 4.3, 0.42, bg_color=colors.HexColor("#1A4B8C"), border_color=PRIMARY_BLUE, radius=12)
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(LIGHT_BLUE_TEXT)
    c.drawString(1.2 * inch, HEIGHT - 1.37 * inch, "MILLIY STARTAP TADBIRI  |  TOSHKENT 2026")

    # Title
    c.setFont("Helvetica-Bold", 44)
    c.setFillColor(WHITE)
    c.drawString(1.0 * inch, HEIGHT - 2.4 * inch, "NEXTGEN AI")

    # Subtitle
    c.setFont("Helvetica-Bold", 20)
    c.setFillColor(LIGHT_BLUE_SUB)
    c.drawString(1.0 * inch, HEIGHT - 3.1 * inch, "Enterprise Energy Intelligence Platform")

    # Tagline
    c.setFont("Helvetica-Oblique", 15)
    c.setFillColor(colors.HexColor("#E0EEFF"))
    c.drawString(1.0 * inch, HEIGHT - 3.75 * inch, "“Har bir kilovatt — aqlli qaror, samarali kelajak.”")

    # Context Card (Lower left)
    draw_card(c, 1.0, 4.5, 7.2, 1.8, bg_color=CARD_DARK_BG, border_color=CARD_DARK_BORDER, radius=8)
    c.setFont("Helvetica-Bold", 11)
    c.setFillColor(LIGHT_BLUE_TEXT)
    c.drawString(1.25 * inch, HEIGHT - 4.9 * inch, "Loyiha missiyasi:")

    c.setFont("Helvetica", 11.5)
    c.setFillColor(WHITE)
    txt_m = "O'zbekiston sanoat va ishlab chiqarish korxonalarida elektr energiyasi sarfini sun'iy intellekt va aniq analitika orqali shaffof boshqarish, isrofgarchilikni yo'qotish va xarajatlarni 8–15% ga qisqartirish."
    m_lines = simpleSplit(txt_m, "Helvetica", 11.5, 6.7 * inch)
    draw_text_lines(c, m_lines, 1.25, 5.25, font_name="Helvetica", font_size=11.5, color=WHITE, line_height_pt=16)

    # Attribution Card (Lower right)
    draw_card(c, 8.5, 4.5, 3.8, 1.8, bg_color=CARD_DARK_BG, border_color=CARD_DARK_BORDER, radius=8)
    c.setFont("Helvetica", 10)
    c.setFillColor(LIGHT_BLUE_TEXT)
    c.drawString(8.75 * inch, HEIGHT - 4.85 * inch, "Loyiha muallifi va dasturchi:")
    c.setFont("Helvetica-Bold", 15)
    c.setFillColor(WHITE)
    c.drawString(8.75 * inch, HEIGHT - 5.25 * inch, "Shohjahon Abdullayev")
    c.setFont("Helvetica", 9.5)
    c.setFillColor(LIGHT_BLUE_SUB)
    c.drawString(8.75 * inch, HEIGHT - 5.65 * inch, "Platforma: nextgen-ai-87ff.vercel.app")
    c.drawString(8.75 * inch, HEIGHT - 5.95 * inch, "Telegram Bot: @nextgenuzz_bot")

    # Cover Footer
    c.setFont("Helvetica", 9)
    c.setFillColor(LIGHT_BLUE_SUB)
    c.drawString(1.0 * inch, 0.45 * inch, "O'zbekiston Respublikasi  •  Milliy texnologik startap taqdimoti  •  2026")
    c.showPage()

    # =========================================================================
    # SLIDE 02 — EXECUTIVE SUMMARY
    # =========================================================================
    c.setFillColor(LIGHT_BG)
    c.rect(0, 0, WIDTH, HEIGHT, stroke=0, fill=1)
    draw_header(c, "Loyiha pasporti", "Ijroiya xulosasi: 30 soniyada NEXTGEN AI mohiyati", "Korxona elektr sarfini nazoratsiz 'qora quti'dan o'lchanadigan iqtisodiy foydaga aylantirish")
    draw_footer(c, 2)

    pillars = [
        ("01. Shaffoflik", "To'liq ko'rinuvchanlik", "Hisoblagichlar va sexlar kesimida soatma-soat elektr sarfini vizuallashtirish. Oylik hisob-fakturani kutmasdan, real vaqtda sarf dinamikasini ko'rish.", PRIMARY_BLUE),
        ("02. Nazorat", "Anomaliyalarni aniqlash", "Kechki payt yoki dam olish kunlari uskunalar behuda ishlashi, qisqa tutashuvlar va yuklama me'yordan oshishini darhol aniqlash va xabar berish.", WARNING_AMBER),
        ("03. Intellekt", "Grounded AI Tahlilchi", "Sun'iy intellekt korxona sarf matrisasini tahlil qilib, rahbar va muhandisga o'zbek tilida aniq, faktlarga asoslangan optimallashtirish tavsiyalarini beradi.", PRIMARY_BLUE),
        ("04. Iqtisod", "8–15% Tejamkorlik", "Reaktiv quvvat jarimalari, samarasiz yuklama va tungi isroflarni bartaraf etish hisobiga oylik elektr xarajatlarini sezilarli darajada qisqartirish.", SUCCESS_GREEN)
    ]
    col_w = 2.78
    gap = 0.2
    for idx, (st, tp, dp, acc) in enumerate(pillars):
        x = 0.8 + idx * (col_w + gap)
        draw_card(c, x, 1.85, col_w, 3.2)
        draw_card_accent(c, x, 1.85, col_w, acc)

        c.setFont("Helvetica-Bold", 9.5)
        c.setFillColor(acc)
        c.drawString((x + 0.2) * inch, HEIGHT - 2.2 * inch, st.upper())

        c.setFont("Helvetica-Bold", 13)
        c.setFillColor(DARK_NAVY)
        c.drawString((x + 0.2) * inch, HEIGHT - 2.5 * inch, tp)

        lines = simpleSplit(dp, "Helvetica", 10, (col_w - 0.4) * inch)
        draw_text_lines(c, lines, x + 0.2, 2.85, font_name="Helvetica", font_size=10, color=DARK_TEXT, line_height_pt=14)

    # Bottom Metric Band
    draw_card(c, 0.8, 5.25, 11.733, 1.35, bg_color=CARD_BG, border_color=PRIMARY_BLUE)
    m_items = [
        ("8–15%", "O'rtacha xarajat qisqarishi", "Ishlab chiqarish quvvatini kamaytirmasdan"),
        ("100%", "Gallyutsinatsiyasiz hisob", "Faqat matematik formulalar asosida aniqlik"),
        ("< 2 daqiqa", "Ogohlantirish tezligi", "Anomal sarf yuzaga kelganda Telegram xabari"),
        ("O'zbek tilida", "Mahalliy tilda to'liq qo'llab-quvvatlash", "Web interfeys, hisobotlar va Telegram bot")
    ]
    sub_w = 11.733 / 4.0
    for idx, (val, lbl, note) in enumerate(m_items):
        mx = 0.8 + idx * sub_w
        c.setFont("Helvetica-Bold", 17)
        c.setFillColor(PRIMARY_BLUE)
        c.drawString((mx + 0.2) * inch, HEIGHT - 5.6 * inch, val)

        c.setFont("Helvetica-Bold", 10)
        c.setFillColor(DARK_NAVY)
        c.drawString((mx + 0.2) * inch, HEIGHT - 5.95 * inch, lbl)

        c.setFont("Helvetica", 8.5)
        c.setFillColor(SECONDARY_TEXT)
        c.drawString((mx + 0.2) * inch, HEIGHT - 6.25 * inch, note)
    c.showPage()

    # =========================================================================
    # SLIDE 03 — BOZORDAGI ASOSIY MUAMMO
    # =========================================================================
    c.setFillColor(LIGHT_BG)
    c.rect(0, 0, WIDTH, HEIGHT, stroke=0, fill=1)
    draw_header(c, "Bozor tahlili", "Asosiy muammo: Korxonalarda elektr energiyasi 'qora quti' bo'lib qolmoqda", "Bugungi kunda sanoat korxonalari elektr xarajatlarini boshqarishda 3 ta tizimli qiyinchilikka duch kelmoqda")
    draw_footer(c, 3)

    prob_blocks = [
        ("Muammo 1", "Ko'r-ko'rona iste'mol va kechikkan hisob",
         "Oylik hisob-faktura faqat oy tugagandan so'ng keladi. Rahbar nima sababdan elektr to'lovi 20% ga oshib ketganini o'sha paytda aniqlay olmaydi.",
         ["Ko'rsatkichlar faqat oy oxirida ko'riladi", "Kunlik va soatlik iste'mol dinamikasi yo'q", "Reaktiv yondashuv: pul to'lanadi, sabab noma'lum", "Sexlar o'rtasida sarf bo'yicha mas'uliyat yo'q"],
         colors.HexColor("#EF4444")),
        
        ("Muammo 2", "Kechki isrofgarchilik va yashirin anomaliyalar",
         "Ish vaqtidan tashqari ochiq qolgan sovutgichlar, kompressorlar, havoni shamollatish tizimlari va noto'g'ri sozlangan uskunalar hisobiga ulkan isrof yuz beradi.",
         ["Ish to'xtagan vaqtda ham bazaviy yuklama yuqori", "Uskunalarning amortizatsiyasi va qizib ketishi", "Tungi rejimda elektrning asossiz sarflanishi", "Muhandislar nosozlikni faqat uskuna buzilgach biladi"],
         WARNING_AMBER),

        ("Muammo 3", "Analitik qurol va kadrlar yetishmovchiligi",
         "Mavjud ASKUE/ASUE tizimlari faqat 'quruq' raqamlarni yig'adi. Bosh energetikda millionlab qator ma'lumotlarni tahlil qilib xulosa chiqarishga vaqt va dastur yo'q.",
         ["Ma'lumotlar bor, lekin tushunarli tahlil yo'q", "Kadrlar yetishmovchiligi va qo'lda Excel yuritish", "Reaktiv quvvat va pik soat jarimalarini oldindan bilmaslik", "Rahbariyat uchun qaror qabul qilish mexanizmi yo'qligi"],
         PRIMARY_BLUE)
    ]
    col3_w = 3.7
    gap3 = 0.3
    for idx, (tag_p, title_p, desc_p, bullets, accent) in enumerate(prob_blocks):
        x = 0.8 + idx * (col3_w + gap3)
        draw_card(c, x, 1.85, col3_w, 4.7)
        draw_card_accent(c, x, 1.85, col3_w, accent)

        c.setFont("Helvetica-Bold", 10)
        c.setFillColor(accent)
        c.drawString((x + 0.25) * inch, HEIGHT - 2.2 * inch, tag_p.upper())

        c.setFont("Helvetica-Bold", 13.5)
        c.setFillColor(DARK_NAVY)
        c.drawString((x + 0.25) * inch, HEIGHT - 2.5 * inch, title_p)

        lines = simpleSplit(desc_p, "Helvetica", 9.5, (col3_w - 0.5) * inch)
        draw_text_lines(c, lines, x + 0.25, 2.85, font_name="Helvetica", font_size=9.5, color=DARK_TEXT, line_height_pt=13)

        c.setFont("Helvetica-Bold", 10)
        c.setFillColor(DARK_NAVY)
        c.drawString((x + 0.25) * inch, HEIGHT - 3.8 * inch, "Amaliy oqibatlari:")

        y_b = 4.1
        for b in bullets:
            b_lines = simpleSplit(f"• {b}", "Helvetica", 9, (col3_w - 0.5) * inch)
            draw_text_lines(c, b_lines, x + 0.25, y_b, font_name="Helvetica", font_size=9, color=SECONDARY_TEXT, line_height_pt=12)
            y_b += len(b_lines) * 0.22 + 0.1
    c.showPage()

    # =========================================================================
    # SLIDE 04 — O'ZBEKISTON UCHUN DOLZARBLIGI
    # =========================================================================
    c.setFillColor(LIGHT_BG)
    c.rect(0, 0, WIDTH, HEIGHT, stroke=0, fill=1)
    draw_header(c, "Davlat siyosati va bozor", "O'zbekiston uchun strategik ahamiyati: Yangi energiya realligi", "Elektr tariflarining erkinlashishi va energiya samaradorligi bo'yicha milliy vazifalar")
    draw_footer(c, 4)

    # Left Column: Policy and Laws
    draw_card(c, 0.8, 1.85, 5.7, 4.7)
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(PRIMARY_BLUE)
    c.drawString(1.05 * inch, HEIGHT - 2.2 * inch, "DAVLAT DASTURLARI VA HUQUQIY POYDEVOR")

    c.setFont("Helvetica-Bold", 13)
    c.setFillColor(DARK_NAVY)
    c.drawString(1.05 * inch, HEIGHT - 2.55 * inch, "Prezident Farmoni (PF-57) va VM Qarorlari")

    items_law = [
        ("Tabaqalashtirilgan tariflar islohoti (2024–2026)", 
         "Yuridik shaxslar va sanoat korxonalari uchun elektr narxi erkinlashtirildi. 1 kWh narxi 900–1000 so'mga yetdi. Pik va tungi soatlarda differensial to'lovlar joriy etildi."),
        ("O'zbekiston – 2030 Milliy Strategiyasi", 
         "2030 yilgacha iqtisodiyot tarmoqlarida energiya sarfi sig'imini 30 foizga qisqartirish bo'yicha qat'iy davlat ko'rsatkichi belgilandi."),
        ("Majburiy energetik audit va hisobdorlik", 
         "Yirik sanoat va tijorat iste'molchilari uchun energiya samaradorligi me'yorlari va resurslarni oqilona sarflash nazorati kuchaytirilmoqda."),
        ("Eksport qiluvchi korxonalar uchun ESG talablari", 
         "Yevropa bozorlariga mahsulot yetkazib beruvchi to'qimachilik korxonalari uchun uglerod izini qisqartirish talab qilinmoqda.")
    ]
    y_law = 2.9
    for lh, ld in items_law:
        c.setFont("Helvetica-Bold", 9.5)
        c.setFillColor(DARK_NAVY)
        c.drawString(1.05 * inch, HEIGHT - y_law * inch, f"•  {lh}")
        y_law += 0.22
        lines = simpleSplit(ld, "Helvetica", 9, 5.2 * inch)
        draw_text_lines(c, lines, 1.2, y_law, font_name="Helvetica", font_size=9, color=SECONDARY_TEXT, line_height_pt=12)
        y_law += len(lines) * 0.2 + 0.15

    # Right Column: Stats
    stat_cards = [
        ("900 – 1000 so'm / kWh", "Sanoat uchun yangi tarif chegarasi", 
         "Elektr narxining 2 baravardan ortiq oshishi korxona xarajatlar strukturasida energiyaning ulushini 15–25% ga yetkazdi.", PRIMARY_BLUE),
        ("30% ga kamaytirish", "O'zbekiston-2030 davlat maqsadi", 
         "Prezident qarorlariga ko'ra sanoatda har bir birlik mahsulotga to'g'ri keluvchi energiya intensivligini keskin pasaytirish shart.", SUCCESS_GREEN),
        ("50,000+ korxona", "O'zbekistondagi faol sanoat korxonalari", 
         "Davlat statistika qo'mitasi ma'lumotlariga ko'ra mamlakatda minglab korxonalar har oyda energiya xarajatlarini optimallashtirishga muhtoj.", DEEP_BLUE)
    ]
    for idx, (num, st_t, st_d, clr) in enumerate(stat_cards):
        cy = 1.85 + idx * 1.6
        draw_card(c, 6.8, cy, 5.733, 1.45)
        draw_card_accent(c, 6.8, cy, 0.1, clr, bar_h_in=1.45)

        c.setFont("Helvetica-Bold", 16)
        c.setFillColor(clr)
        c.drawString(7.1 * inch, HEIGHT - (cy + 0.35) * inch, num)

        c.setFont("Helvetica-Bold", 10.5)
        c.setFillColor(DARK_NAVY)
        c.drawString(7.1 * inch, HEIGHT - (cy + 0.65) * inch, st_t)

        lines = simpleSplit(st_d, "Helvetica", 9, 5.2 * inch)
        draw_text_lines(c, lines, 7.1, cy + 0.85, font_name="Helvetica", font_size=9, color=SECONDARY_TEXT, line_height_pt=12)
    c.showPage()

    # =========================================================================
    # SLIDE 05 — BIZNING YECHIM (5-Stage Architecture)
    # =========================================================================
    c.setFillColor(LIGHT_BG)
    c.rect(0, 0, WIDTH, HEIGHT, stroke=0, fill=1)
    draw_header(c, "Texnologik konsepsiya", "Bizning yechim: Ma'lumotdan intellektga 5 bosqichli zanjir", "Xom hisoblagich raqamlarini korxona rahbari va muhandisi uchun tayyor biznes harakatiga aylantirish")
    draw_footer(c, 5)

    stages = [
        ("01", "KORXONA MA'LUMOTLARI", "Hisoblagichlar, Excel/CSV fayllar va ASKUE protokollari orqali sarf ko'rsatkichlari yig'iladi.", PRIMARY_BLUE, "Yagona raqamli markaz"),
        ("02", "MA'LUMOTLARNI TOZALASH", "Yetishmayotgan qatorlar to'ldiriladi, birliklar (kW vs kWh) tekshiriladi va validatsiya qilinadi.", DEEP_BLUE, "100% toza ma'lumot"),
        ("03", "ENERGIYA ANALITIKASI", "Pik soatlar, bazaviy yuklama, kunlik/oylik o'rtacha qiymatlar va dinamika hisoblanadi.", PRIMARY_BLUE, "Shaffof soatlik matrisa"),
        ("04", "AI & ANOMALIYA QATLAMI", "Z-score va statistik modellar orqali shubhali sakrashlar aniqlanadi, sarf bashorati tuziladi.", WARNING_AMBER, "Anomal isrofni tutish"),
        ("05", "AMALIY BIZNES QARORI", "O'zbek tilida tayyor tavsiyalar, Telegram tezkor ogohlantirishlari va PDF hisobotlar beriladi.", SUCCESS_GREEN, "8-15% xarajat qisqarishi")
    ]
    col5_w = 2.18
    gap5 = 0.2
    for idx, (num, st_t, st_d, clr, ben) in enumerate(stages):
        x = 0.8 + idx * (col5_w + gap5)
        draw_card(c, x, 2.0, col5_w, 4.5)
        draw_card_accent(c, x, 2.0, col5_w, clr, bar_h_in=0.6)

        c.setFont("Helvetica-Bold", 10.5)
        c.setFillColor(WHITE)
        c.drawString((x + 0.3) * inch, HEIGHT - 2.38 * inch, f"BOSQICH  {num}")

        c.setFont("Helvetica-Bold", 11)
        c.setFillColor(DARK_NAVY)
        t_lines = simpleSplit(st_t, "Helvetica-Bold", 11, (col5_w - 0.3) * inch)
        draw_text_lines(c, t_lines, x + 0.15, 2.9, font_name="Helvetica-Bold", font_size=11, color=DARK_NAVY, line_height_pt=14)

        lines = simpleSplit(st_d, "Helvetica", 9.5, (col5_w - 0.3) * inch)
        draw_text_lines(c, lines, x + 0.15, 3.6, font_name="Helvetica", font_size=9.5, color=DARK_TEXT, line_height_pt=13)

        c.setFont("Helvetica-Bold", 9.5)
        c.setFillColor(clr)
        c.drawString((x + 0.15) * inch, HEIGHT - 5.5 * inch, "Natija:")

        c.setFont("Helvetica-Bold", 9.5)
        c.setFillColor(DARK_NAVY)
        c.drawString((x + 0.15) * inch, HEIGHT - 5.8 * inch, ben)
    c.showPage()

    # =========================================================================
    # SLIDE 06 — FOYDALANUVCHI YO'LI / USER JOURNEY (9 Steps)
    # =========================================================================
    c.setFillColor(LIGHT_BG)
    c.rect(0, 0, WIDTH, HEIGHT, stroke=0, fill=1)
    draw_header(c, "Amaliyot jarayoni", "NEXTGEN qanday ishlaydi: Korxona uchun 9 qadamli oqim", "Tizimga ulanishdan tortib har oylik iqtisodiy samarani olishgacha bo'lgan to'liq yo'l")
    draw_footer(c, 6)

    steps = [
        ("1. Profil yaratish", "Korxona tizimda o'z tashkilot profilini ro'yxatdan o'tkazadi va xodimlarni qo'shadi."),
        ("2. Hisoblagichlarni kiritish", "Sexlar, uskunalar va transformator punktlari bo'yicha hisoblagichlar biriktiriladi."),
        ("3. Ma'lumotlarni yuklash", "Elektr sarfi ko'rsatkichlari CSV/Excel orqali yoki to'g'ridan-to'g'ri kiritiladi."),
        ("4. Avtomatik validatsiya", "Tizim ma'lumotlar butunligini, o'lchov birliklarini va xatoliklarni soniyada tekshiradi."),
        ("5. Sarf tahlili va metrikalar", "Kunduzgi, tungi va pik soatlar kesimida sarf, maksimal quvvat hisoblanadi."),
        ("6. Anomaliyalarni aniqlash", "Algoritm me'yordan ortiq sarflarni va kechki paytdagi yo'qotishlarni aniqlaydi."),
        ("7. Kelajak xarajatini bashorat", "Trendlar asosida keyingi oy uchun kutilayotgan elektr iste'moli hisoblab chiqiladi."),
        ("8. Grounded AI Tahlilnomasi", "Sun'iy intellekt korxona uchun energiya tejash bo'yicha faktik tavsiyalar beradi."),
        ("9. Telegram va PDF hisobotlar", "Boshqaruv xulosasi va ogohlantirishlar rahbarning Telegramiga yuboriladi.")
    ]
    grid_w = 3.7
    grid_h = 1.4
    gap_x = 0.3
    gap_y = 0.2
    for idx, (st_t, st_d) in enumerate(steps):
        row = idx // 3
        col = idx % 3
        x = 0.8 + col * (grid_w + gap_x)
        y = 1.85 + row * (grid_h + gap_y)

        draw_card(c, x, y, grid_w, grid_h)
        c.setFont("Helvetica-Bold", 10.5)
        c.setFillColor(PRIMARY_BLUE)
        c.drawString((x + 0.15) * inch, HEIGHT - (y + 0.3) * inch, st_t)

        lines = simpleSplit(st_d, "Helvetica", 9, (grid_w - 0.3) * inch)
        draw_text_lines(c, lines, x + 0.15, y + 0.55, font_name="Helvetica", font_size=9, color=DARK_TEXT, line_height_pt=12)
    c.showPage()

    # =========================================================================
    # SLIDE 07 — MAHSULOT PLATFORMASI / THE PRODUCT (Real Screenshot)
    # =========================================================================
    c.setFillColor(LIGHT_BG)
    c.rect(0, 0, WIDTH, HEIGHT, stroke=0, fill=1)
    draw_header(c, "Ishlab turgan tizim", "Mahsulot platformasi: Veb boshqaruv interfeysi", "nextgen-ai-87ff.vercel.app manzilida faol ishlab turgan zamonaviy korporativ panel")
    draw_footer(c, 7)

    # Screenshot on Left
    screenshot_path = "presentations/assets/dashboard_vercel.png"
    if os.path.exists(screenshot_path):
        c.drawImage(screenshot_path, 0.8 * inch, HEIGHT - 6.35 * inch, width=6.8 * inch, height=4.35 * inch)
        c.setFont("Helvetica", 8.5)
        c.setFillColor(SECONDARY_TEXT)
        c.drawString(0.8 * inch, HEIGHT - 6.55 * inch, "Haqiqiy ishchi interfeys (Next.js 14 + Recharts + Grounded AI) • nextgen-ai-87ff.vercel.app")
    else:
        draw_card(c, 0.8, 1.85, 6.8, 4.5)

    # Right: 4 Features
    r_x = 7.85
    r_w = 4.683
    feat_h = 1.05
    f_gap = 0.12
    features = [
        ("Interaktiv Boshqaruv Paneli (Dashboard)", "Umumiy energiya sarfi (kWh), eng yuqori yuklama (kW), hisoblangan xarajat va aktiv anomaliyalar soni real vaqtda ko'rsatiladi."),
        ("Ko'p O'lchovli Analitika va Grafiklar", "Kunlik, haftalik va oylik dinamika, soatlik iste'mol grafigi hamda pik vaqtlar taqsimoti interaktiv tarzda aks etadi."),
        ("Excel / CSV Import va Validatsiya", "Korxona o'z hisoblagich jurnallarini bir tugma bilan yuklaydi. Tizim xatoliklarni avtomatik tuzatadi va bazaga yozadi."),
        ("AI Maslahatchi va Grounded Tahlil", "Foydalanuvchi tizimga savol berishi mumkin: 'Nega o'tgan hafta sarf 15% oshdi?' AI faqat haqiqiy bazadagi raqamlarga asoslanib javob beradi.")
    ]
    for idx, (ft, fd) in enumerate(features):
        fy = 1.85 + idx * (feat_h + f_gap)
        draw_card(c, r_x, fy, r_w, feat_h)
        draw_card_accent(c, r_x, fy, 0.08, PRIMARY_BLUE, bar_h_in=feat_h)

        c.setFont("Helvetica-Bold", 10.5)
        c.setFillColor(DARK_NAVY)
        c.drawString((r_x + 0.2) * inch, HEIGHT - (fy + 0.3) * inch, ft)

        lines = simpleSplit(fd, "Helvetica", 8.5, (r_w - 0.35) * inch)
        draw_text_lines(c, lines, r_x + 0.2, fy + 0.5, font_name="Helvetica", font_size=8.5, color=DARK_TEXT, line_height_pt=11)
    c.showPage()

    # =========================================================================
    # SLIDE 08 — TELEGRAM EKOTIZIMI (@nextgenuzz_bot)
    # =========================================================================
    c.setFillColor(LIGHT_BG)
    c.rect(0, 0, WIDTH, HEIGHT, stroke=0, fill=1)
    draw_header(c, "Mobil qulaylik", "NEXTGEN Telegram ekotizimi: @nextgenuzz_bot", "O'zbekiston biznesi uchun qulay mobil boshqaruv va tezkor xabardorlik kanali")
    draw_footer(c, 8)

    # Left: Why Telegram
    draw_card(c, 0.8, 1.85, 5.6, 4.7)
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(PRIMARY_BLUE)
    c.drawString(1.05 * inch, HEIGHT - 2.2 * inch, "NEGA TELEGRAM INTEGRATSIYASI TANLANDI?")

    c.setFont("Helvetica-Bold", 13)
    c.setFillColor(DARK_NAVY)
    c.drawString(1.05 * inch, HEIGHT - 2.55 * inch, "O'zbekistonda biznes Telegram orqali yuritiladi")

    t_reasons = [
        ("Darhol yetib boruvchi Push-xabarlar", "Kritik anomaliya yuz berganda xabar 2 soniyada bosh muhandis va rahbarning cho'ntagiga boradi. Veb-saytga kirishni kutish shart emas."),
        ("O'rganish uchun nol vaqt talab etiladi", "Har bir korxona rahbari va xodimi Telegramdan foydalanishni biladi. Qo'shimcha qiyin dasturiy ta'lim shart emas."),
        ("Ovozli va matnli so'rovlar", "Rahbar oddiy audio xabar bilan: 'Bugun qancha sarfladik?' deb so'rashi va AI tahlildan tezkor ovozli/matnli javob olishi mumkin."),
        ("Mobil ilova (Android APK) tarqatish", "Bot orqali korxona xodimlari to'g'ridan-to'g'ri NEXTGEN Android ilovasini yuklab olishi mumkin (/apk komandasi).")
    ]
    y_tel = 2.9
    for rh, rd in t_reasons:
        c.setFont("Helvetica-Bold", 9.5)
        c.setFillColor(DARK_NAVY)
        c.drawString(1.05 * inch, HEIGHT - y_tel * inch, f"✔  {rh}")
        y_tel += 0.22
        lines = simpleSplit(rd, "Helvetica", 9, 5.1 * inch)
        draw_text_lines(c, lines, 1.25, y_tel, font_name="Helvetica", font_size=9, color=SECONDARY_TEXT, line_height_pt=12)
        y_tel += len(lines) * 0.2 + 0.15

    # Right: Bot Features & Implementation
    bot_cards = [
        ("@nextgenuzz_bot asosiy komandalari", [
            "/start — Xavfsiz avtorizatsiya va profilni bog'lash",
            "/stats — Bugungi va oylik elektr sarfi qisqacha hisoboti",
            "/anomalies — Oxirgi 24 soatdagi shubhali sarflar ro'yxati",
            "/forecast — Keyingi oy uchun hisoblangan elektr to'lovi",
            "/apk — Android mobil ilovani yuklab olish",
            "AI Maslahatchi — Istalgan savolga tezkor javob"
        ], PRIMARY_BLUE),
        ("Haqiqiy ishlab turgan texnologik holat", [
            "Aiogram 3.x zamonaviy asinxron freymvorkida yaratilgan",
            "Veb-platforma ma'lumotlar bazasi bilan to'liq sinxron",
            "Multi-tenant xavfsizlik: har bir xodim faqat o'z zavodini ko'radi",
            "O'zbek tilida to'liq interaktiv tugmalar (Inline keyboard)"
        ], SUCCESS_GREEN)
    ]
    for idx, (b_title, b_items, b_clr) in enumerate(bot_cards):
        by = 1.85 + idx * 2.4
        draw_card(c, 6.8, by, 5.733, 2.25)
        draw_card_accent(c, 6.8, by, 5.733, b_clr)

        c.setFont("Helvetica-Bold", 11.5)
        c.setFillColor(DARK_NAVY)
        c.drawString(7.05 * inch, HEIGHT - (by + 0.35) * inch, b_title)

        y_bi = by + 0.65
        for item in b_items:
            c.setFont("Helvetica", 9.5)
            c.setFillColor(DARK_TEXT)
            c.drawString(7.05 * inch, HEIGHT - y_bi * inch, f"•  {item}")
            y_bi += 0.24
    c.showPage()

    # =========================================================================
    # SLIDE 09 — SUN'IY INTELLEKT VA ARXITEKTURA
    # =========================================================================
    c.setFillColor(LIGHT_BG)
    c.rect(0, 0, WIDTH, HEIGHT, stroke=0, fill=1)
    draw_header(c, "Texnologik poydevor", "Sun'iy intellekt va arxitektura: Deterministik hisob + LLM", "Sun'iy intellekt gallyutsinatsiyasini nolga tushiruvchi ikki qatlamli gibrid arxitektura")
    draw_footer(c, 9)

    # Left: Hybrid Grounding
    draw_card(c, 0.8, 1.85, 5.7, 4.7)
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(PRIMARY_BLUE)
    c.drawString(1.05 * inch, HEIGHT - 2.2 * inch, "GALLYUTSINATSIYASIZ SUN'IY INTELLEKT")

    c.setFont("Helvetica-Bold", 13)
    c.setFillColor(DARK_NAVY)
    c.drawString(1.05 * inch, HEIGHT - 2.55 * inch, "Ikki Qatlamli Ishonchli Model (Two-Layer Grounding)")

    layers = [
        ("1-Qatlam: Deterministik Matematika (SQL & Python)", 
         "Barcha raqamlar, jami kWh sarfi, pik vaqtlar, tarif hisoblari va Z-score anomaliya chegaralari qat'iy matematik formulalar bilan hisoblanadi. LLM bu hisoblarga aralashmaydi."),
        ("2-Qatlam: Grounded Generativ AI (Interpretatsiya)", 
         "Hisoblangan qat'iy natijalar tizimli kontekst (prompt) sifatida LLMga beriladi. AI faqat ushbu raqamlarni o'zbek tilida sharhlaydi va biznes tavsiyalari beradi."),
        ("Qat'iy xavfsizlik cheklovi (Guardrail)", 
         "Agar ma'lumotlar yetarli bo'lmasa, AI taxmin qilmaydi, balki to'g'ridan-to'g'ri 'Ma'lumot yetarli emas' deb javob beradi. Bu korporativ xavfsizlikni ta'minlaydi.")
    ]
    y_lay = 2.9
    for lh, ld in layers:
        c.setFont("Helvetica-Bold", 9.5)
        c.setFillColor(DARK_NAVY)
        c.drawString(1.05 * inch, HEIGHT - y_lay * inch, f"✔  {lh}")
        y_lay += 0.22
        lines = simpleSplit(ld, "Helvetica", 9, 5.2 * inch)
        draw_text_lines(c, lines, 1.25, y_lay, font_name="Helvetica", font_size=9, color=SECONDARY_TEXT, line_height_pt=12)
        y_lay += len(lines) * 0.2 + 0.15

    # Right: Stack Cards
    tech_cards = [
        ("Frontend: Next.js 14 & Tailwind CSS", "Server-Side Rendering (SSR), tezkor yuklanish, zamonaviy Recharts grafik kutubxonasi, to'liq moslashuvchan dizayn.", PRIMARY_BLUE),
        ("Backend: FastAPI & Python 3.11+", "Yuqori tezlikdagi asinxron REST API, qat'iy ma'lumotlar sxemasi (Pydantic), avtomatik OpenAPI/Swagger hujjatlari.", DEEP_BLUE),
        ("Ma'lumotlar bazasi: PostgreSQL / SQLite", "ACID tranzaksiyalari, ko'p ijarachilik (Multi-tenancy), korxona ma'lumotlarini qat'iy ajratish va indeksatsiya.", SUCCESS_GREEN),
        ("Bot & Mobil: Aiogram 3 & Android Native", "Asinxron Telegram boti, Webhook arxitekturasi, APK paket orqali to'g'ridan-to'g'ri mobil boshqaruv.", WARNING_AMBER)
    ]
    for idx, (t_name, t_desc, t_clr) in enumerate(tech_cards):
        ty = 1.85 + idx * 1.15
        draw_card(c, 6.8, ty, 5.733, 1.05)
        draw_card_accent(c, 6.8, ty, 0.08, t_clr, bar_h_in=1.05)

        c.setFont("Helvetica-Bold", 10.5)
        c.setFillColor(DARK_NAVY)
        c.drawString(7.05 * inch, HEIGHT - (ty + 0.3) * inch, t_name)

        lines = simpleSplit(t_desc, "Helvetica", 8.5, 5.25 * inch)
        draw_text_lines(c, lines, 7.05, ty + 0.5, font_name="Helvetica", font_size=8.5, color=DARK_TEXT, line_height_pt=11)
    c.showPage()

    # =========================================================================
    # SLIDE 10 — XAVFSIZLIK VA KORPORATIV ISHONCHLILIK
    # =========================================================================
    c.setFillColor(LIGHT_BG)
    c.rect(0, 0, WIDTH, HEIGHT, stroke=0, fill=1)
    draw_header(c, "Kiberxavfsizlik", "Xavfsizlik va korporativ ishonchlilik", "Sanoat korxonalarining tijoriy sirlari va ma'lumotlarini kafolatli himoyalash")
    draw_footer(c, 10)

    sec_pillars = [
        ("Multi-Tenant Izolyatsiya", "Tashkilotlararo to'liq ajratish", 
         "Har bir korxona ma'lumotlari alohida virtual konteynerda saqlanadi. Hech bir mijoz boshqa korxonaning sarf ma'lumotlarini ko'ra olmaydi.",
         ["Tashkilot ID bo'yicha qat'iy filtr", "Bazada ma'lumotlar aralashmaydi", "To'liq konfidensiallik"],
         PRIMARY_BLUE),
        
        ("Rolga Asoslangan Ruxsat", "Vazifalar bo'yicha kirish huquqi",
         "Tizim foydalanuvchilari 3 toifaga bo'linadi: Administrator (to'liq nazorat), Bosh energetik (tahlil), Kuzatuvchi (faqat ko'rish).",
         ["Boshqaruv rollari matritsasi", "Parollarni argon2 bilan shifrlash", "Ruxsatsiz o'zgarishlar bloklanadi"],
         DEEP_BLUE),

        ("Audit Loglari va Nazorat", "Har bir harakat qayd etiladi",
         "Fayl qachon yuklandi, kim eksport qildi, qaysi ko'rsatkich o'zgardi — barcha amallar xronologik jurnalda saqlanadi va tahrirlanmaydi.",
         ["Vaqt belgisi bilan harakatlar jurnali", "Audit tekshiruvlariga tayyorlik", "Ichki xavfsizlik kafolati"],
         WARNING_AMBER),

        ("Lokal Server (On-Premise)", "Mustaqil ichki infratuzilma",
         "Strategik korxonalar uchun tizimni internetga ulamasdan, to'g'ridan-to'g'ri korxonaning o'z serverlariga (On-premise) o'rnatish imkoniyati mavjud.",
         ["Davlat korxonalari talablariga mos", "Tashqi tarmoqqa bog'liqlik yo'q", "O'zbekiston qonunlariga muvofiqlik"],
         SUCCESS_GREEN)
    ]
    col10_w = 2.78
    gap10 = 0.2
    for idx, (st, ssub, sdesc, spoints, sclr) in enumerate(sec_pillars):
        x = 0.8 + idx * (col10_w + gap10)
        draw_card(c, x, 1.85, col10_w, 4.7)
        draw_card_accent(c, x, 1.85, col10_w, sclr)

        c.setFont("Helvetica-Bold", 11.5)
        c.setFillColor(DARK_NAVY)
        c.drawString((x + 0.2) * inch, HEIGHT - 2.2 * inch, st)

        c.setFont("Helvetica-Bold", 9)
        c.setFillColor(sclr)
        c.drawString((x + 0.2) * inch, HEIGHT - 2.45 * inch, ssub)

        lines = simpleSplit(sdesc, "Helvetica", 9, (col10_w - 0.4) * inch)
        draw_text_lines(c, lines, x + 0.2, 2.75, font_name="Helvetica", font_size=9, color=DARK_TEXT, line_height_pt=12)

        c.setFont("Helvetica-Bold", 9)
        c.setFillColor(DARK_NAVY)
        c.drawString((x + 0.2) * inch, HEIGHT - 4.15 * inch, "Himoya mexanizmlari:")

        y_sp = 4.4
        for p in spoints:
            c.setFont("Helvetica", 8.5)
            c.setFillColor(SECONDARY_TEXT)
            c.drawString((x + 0.2) * inch, HEIGHT - y_sp * inch, f"✔ {p}")
            y_sp += 0.24
    c.showPage()

    # =========================================================================
    # SLIDE 11 — BOZOR HAJMI VA MAQSADLI MIJOZLAR
    # =========================================================================
    c.setFillColor(LIGHT_BG)
    c.rect(0, 0, WIDTH, HEIGHT, stroke=0, fill=1)
    draw_header(c, "Bozor tahlili", "Bozor hajmi va maqsadli mijozlar", "O'zbekistonda energiya boshqaruviga eng yuqori ehtiyoji bo'lgan sanoat segmentlari")
    draw_footer(c, 11)

    # Left: TAM SAM SOM
    draw_card(c, 0.8, 1.85, 5.7, 4.7)
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(PRIMARY_BLUE)
    c.drawString(1.05 * inch, HEIGHT - 2.2 * inch, "BOZOR HAJMI BAHOLANISHI (TAM / SAM / SOM)")

    c.setFont("Helvetica-Bold", 13)
    c.setFillColor(DARK_NAVY)
    c.drawString(1.05 * inch, HEIGHT - 2.55 * inch, "O'zbekiston sanoat va tijorat sektori")

    mkt_levels = [
        ("TAM (Umumiy bozor): 50,000+ korxona", 
         "O'zbekistondagi barcha ro'yxatdan o'tgan sanoat, qayta ishlash va ishlab chiqarish korxonalari. Yillik potentsial bozor: $60M+."),
        ("SAM (Erishish mumkin bo'lgan bozor): 8,000+ korxona", 
         "Oylik elektr energiyasi to'lovi 20 million so'mdan ortiq bo'lgan, raqamlashtirishga tayyor to'qimachilik, oziq-ovqat va metallurgiya korxonalari. Yillik hajm: ~$12M."),
        ("SOM (Dastlabki 2 yillik maqsad): 250 korxona", 
         "Toshkent, Farg'ona vodiysi va Samarqanddagi faol ishlab chiqarish korxonalari. Yillik rejalashtirilgan SaaS tushumi: $450,000+.")
    ]
    y_mkt = 2.9
    for mh, md in mkt_levels:
        c.setFont("Helvetica-Bold", 9.5)
        c.setFillColor(DARK_NAVY)
        c.drawString(1.05 * inch, HEIGHT - y_mkt * inch, f"★  {mh}")
        y_mkt += 0.22
        lines = simpleSplit(md, "Helvetica", 9, 5.2 * inch)
        draw_text_lines(c, lines, 1.25, y_mkt, font_name="Helvetica", font_size=9, color=SECONDARY_TEXT, line_height_pt=12)
        y_mkt += len(lines) * 0.2 + 0.18

    # Right: Verticals
    verticals = [
        ("To'qimachilik va tikuvchilik fabrikalari", "Uzluksiz 24/7 ish tartibi, yuzlab dastgohlar, kompressorlar. Elektr xarajatlari tannarxning 20% gacha qismini tashkil etadi.", PRIMARY_BLUE),
        ("Oziq-ovqat va qayta ishlash korxonalari", "Katta sovutish kameralari, qadoqlash liniyalari, pishirish sexlari. Tungi va kunduzgi rejimda sarf turlicha bo'ladi.", SUCCESS_GREEN),
        ("Qurilish materiallari va metallurgiya", "Kuchli elektr pechlari, prokat stanoklari, transformatorlar. Pik soatlarda jarimalarga tushish xavfi juda yuqori.", WARNING_AMBER),
        ("Yirik logistika va savdo majmualari", "Minglab kvadrat metrli sovutgichli omborlar, yoritish tizimlari va havoni shamollatish agregatlari.", DEEP_BLUE)
    ]
    for idx, (vt, vd, vclr) in enumerate(verticals):
        vy = 1.85 + idx * 1.15
        draw_card(c, 6.8, vy, 5.733, 1.05)
        draw_card_accent(c, 6.8, vy, 0.08, vclr, bar_h_in=1.05)

        c.setFont("Helvetica-Bold", 10.5)
        c.setFillColor(DARK_NAVY)
        c.drawString(7.05 * inch, HEIGHT - (vy + 0.3) * inch, vt)

        lines = simpleSplit(vd, "Helvetica", 8.5, 5.25 * inch)
        draw_text_lines(c, lines, 7.05, vy + 0.5, font_name="Helvetica", font_size=8.5, color=DARK_TEXT, line_height_pt=11)
    c.showPage()

    # =========================================================================
    # SLIDE 12 — RAQOBAT TAHLILI
    # =========================================================================
    c.setFillColor(LIGHT_BG)
    c.rect(0, 0, WIDTH, HEIGHT, stroke=0, fill=1)
    draw_header(c, "Raqobat tahlili", "Raqobat tahlili: NEXTGEN AI ustunliklari", "Mavjud yechimlar va xorijiy analoglar bilan xolis taqqoslash")
    draw_footer(c, 12)

    draw_card(c, 0.8, 1.85, 11.733, 4.7)
    c.setFont("Helvetica-Bold", 11)
    c.setFillColor(PRIMARY_BLUE)
    c.drawString(1.05 * inch, HEIGHT - 2.2 * inch, "BOZORDAGI YECHIMLAR TAQQOSLASH MATRITSASI")

    headers = ["Taqqoslash mezoni", "An'anaviy ASKUE", "Xorijiy dasturlar", "Qo'lda Excel", "NEXTGEN AI"]
    rows = [
        ("O'zbek tili va mahalliy tariflar", "❌  Yo'q (faqat rus/ingliz)", "❌  Yo'q (xorijiy standartlar)", "⚠️  Qisman formulalar", "✔  To'liq o'zbek tilida va mahalliy tariflar"),
        ("Sun'iy intellekt tavsiyalari", "❌  Yo'q (faqat raqam yig'adi)", "⚠️  Qisman ($$$ modul)", "❌  Yo'q", "✔  Grounded AI (faktik tavsiyalar)"),
        ("Anomaliyalarni erta aniqlash", "❌  Yo'q", "✔  Mavjud", "❌  Kech aniqlanadi", "✔  Statistik Z-Score va tezkor xabarlar"),
        ("Telegram orqali boshqaruv", "❌  Yo'q", "❌  Yo'q", "❌  Yo'q", "✔  @nextgenuzz_bot orqali 24/7 nazorat"),
        ("Joriy etish tezligi va narxi", "Oylar talab qiladi, qimmat", "$20,000+ va uzoq vaqt", "Arzon, ammo samarasiz", "1 kunda ishga tushadi, qulay SaaS"),
        ("Hisobotlarni avtomatlashtirish", "Faqat jadval ko'rinishida", "Murakkab korporativ shakl", "Qo'lda soatlab vaqt oladi", "1 tugma bilan PDF va Telegram hisobot")
    ]
    # Draw formatted table
    col_x = [1.05, 3.8, 5.8, 7.8, 9.8]
    # Header
    c.setFont("Helvetica-Bold", 9.5)
    c.setFillColor(DARK_NAVY)
    for i, h in enumerate(headers):
        c.drawString(col_x[i] * inch, HEIGHT - 2.55 * inch, h)

    c.setStrokeColor(BORDER_COLOR)
    c.setLineWidth(1)
    c.line(1.05 * inch, HEIGHT - 2.65 * inch, 12.3 * inch, HEIGHT - 2.65 * inch)

    y_row = 2.95
    for r in rows:
        c.setFont("Helvetica-Bold", 9)
        c.setFillColor(DARK_NAVY)
        c.drawString(col_x[0] * inch, HEIGHT - y_row * inch, r[0])

        c.setFont("Helvetica", 8.5)
        c.setFillColor(DARK_TEXT)
        for i in range(1, 5):
            if "✔" in r[i]:
                c.setFont("Helvetica-Bold", 8.5)
                c.setFillColor(SUCCESS_GREEN)
            else:
                c.setFont("Helvetica", 8.5)
                c.setFillColor(DARK_TEXT)
            c.drawString(col_x[i] * inch, HEIGHT - y_row * inch, r[i])
        y_row += 0.55
    c.showPage()

    # =========================================================================
    # SLIDE 13 — BIZNES MODEL VA MONETIZATSIYA
    # =========================================================================
    c.setFillColor(LIGHT_BG)
    c.rect(0, 0, WIDTH, HEIGHT, stroke=0, fill=1)
    draw_header(c, "Iqtisodiy model", "Biznes model va monetizatsiya", "B2B SaaS obuna va korxona hajmiga mos moslashuvchan tariflar")
    draw_footer(c, 13)

    plans = [
        ("Starter", "Kichik ishlab chiqarish", "500,000 so'm / oy", 
         "1–3 ta hisoblagichga ega kichik sexlar, novvoyxonalar va ustaxonalar uchun.",
         [
             "3 tagacha hisoblagich monitoringi",
             "Kunlik sarf va bazaviy grafiklar",
             "Excel / CSV yuklash imkoniyati",
             "Telegram bot haftalik xabarlari",
             "Standart texnik qo'llab-quvvatlash"
         ], PRIMARY_BLUE, False),
        
        ("Pro (Tavsiya etiladi)", "O'rta sanoat korxonalari", "1,500,000 so'm / oy", 
         "To'qimachilik, oziq-ovqat va yig'uv fabrikalari uchun to'liq tahliliy paket.",
         [
             "15 tagacha hisoblagich monitoringi",
             "To'liq Grounded AI tahlilchi",
             "Z-Score anomaliyalarni 24/7 aniqlash",
             "Real vaqtda Telegram ogohlantirishlari",
             "Kelgusi oy sarf va to'lov bashorati",
             "Avtomatik oylik PDF boshqaruv hisoboti"
         ], SUCCESS_GREEN, True),

        ("Enterprise", "Yirik zavodlar va xoldinglar", "Shartnoma asosida", 
         "Yirik sanoat korxonalari, metallurgiya va ko'p filialli ishlab chiqarish majmualari.",
         [
             "Cheksiz miqdordagi hisoblagichlar",
             "Lokal serverga (On-premise) o'rnatish",
             "ASKUE va ERP API integratsiyasi",
             "Shaxsiy AI modeli va hisobotlar",
             "Alohida muhandis va 24/7 SLA xizmati"
         ], DEEP_BLUE, False)
    ]
    col13_w = 3.7
    gap13 = 0.3
    for idx, (pname, ptarget, pprice, pdesc, pfeats, pclr, isrec) in enumerate(plans):
        x = 0.8 + idx * (col13_w + gap13)
        draw_card(c, x, 1.85, col13_w, 4.7, border_color=PRIMARY_BLUE if isrec else BORDER_COLOR)
        draw_card_accent(c, x, 1.85, col13_w, pclr)

        c.setFont("Helvetica-Bold", 12)
        c.setFillColor(pclr)
        c.drawString((x + 0.2) * inch, HEIGHT - 2.2 * inch, pname.upper())

        c.setFont("Helvetica-Bold", 16)
        c.setFillColor(DARK_NAVY)
        c.drawString((x + 0.2) * inch, HEIGHT - 2.55 * inch, pprice)

        c.setFont("Helvetica", 9)
        c.setFillColor(SECONDARY_TEXT)
        c.drawString((x + 0.2) * inch, HEIGHT - 2.8 * inch, ptarget)

        lines = simpleSplit(pdesc, "Helvetica", 9, (col13_w - 0.4) * inch)
        draw_text_lines(c, lines, x + 0.2, 3.0, font_name="Helvetica", font_size=9, color=DARK_TEXT, line_height_pt=12)

        c.setFont("Helvetica-Bold", 9.5)
        c.setFillColor(DARK_NAVY)
        c.drawString((x + 0.2) * inch, HEIGHT - 4.1 * inch, "Tarif imkoniyatlari:")

        y_pf = 4.35
        for feat in pfeats:
            c.setFont("Helvetica", 8.5)
            c.setFillColor(DARK_TEXT)
            c.drawString((x + 0.2) * inch, HEIGHT - y_pf * inch, f"✔  {feat}")
            y_pf += 0.24
    c.showPage()

    # =========================================================================
    # SLIDE 14 — RIVOJLANISH XARITASI (ROADMAP)
    # =========================================================================
    c.setFillColor(LIGHT_BG)
    c.rect(0, 0, WIDTH, HEIGHT, stroke=0, fill=1)
    draw_header(c, "Strategik reja", "Rivojlanish xaritasi: 2026–2027 yillar", "MVP bosqichidan milliy va xalqaro miqyosdagi yetakchi platformaga aylanish bosqichlari")
    draw_footer(c, 14)

    phases = [
        ("1-BOSQICH (Bajarildi)", "MVP va Demo Platforma", "2026-yil Q1", [
            "Vercel veb platformasi ishga tushirildi",
            "FastAPI backend va ma'lumotlar bazasi tayyor",
            "@nextgenuzz_bot Telegram boti ulandi",
            "Android APK mobil ilovasi tayyorlandi",
            "Deterministik AI tavsiyalar tekshirildi"
        ], SUCCESS_GREEN),
        
        ("2-BOSQICH (Joriy)", "5 ta Korxonada Pilot", "2026-yil Q2", [
            "To'qimachilik va oziq-ovqatda bepul pilot",
            "Real hisoblagich ma'lumotlari asosida test",
            "Tejamkorlik metrikalarini isbotlash",
            "Energetiklar fikrlari asosida takomillashtirish"
        ], PRIMARY_BLUE),

        ("3-BOSQICH (Tijoriy)", "O'zbekistonda Kengayish", "2026-yil Q3–Q4", [
            "50+ to'lovchi korxonani ulash",
            "ASKUE va HET tizimlari bilan API integratsiya",
            "Mobil ilovani Play Store'ga chiqarish",
            "Energiya auditi kompaniyalari bilan hamkorlik"
        ], DEEP_BLUE),

        ("4-BOSQICH (Xalqaro)", "Markaziy Osiyo Bozoriga Chiqish", "2027-yil", [
            "Qozog'iston va Qirg'izistonga kengayish",
            "Ko'p tilli qo'llab-quvvatlash (qozoq, qirg'iz, rus)",
            "Kompaniyalar uchun ESG uglerod izi sertifikati",
            "A seriya investitsiyalarini jalb qilish"
        ], WARNING_AMBER)
    ]
    col14_w = 2.78
    gap14 = 0.2
    for idx, (pnum, ptitle, ptime, ptasks, pclr) in enumerate(phases):
        x = 0.8 + idx * (col14_w + gap14)
        draw_card(c, x, 1.85, col14_w, 4.7)
        draw_card_accent(c, x, 1.85, col14_w, pclr)

        c.setFont("Helvetica-Bold", 9.5)
        c.setFillColor(pclr)
        c.drawString((x + 0.2) * inch, HEIGHT - 2.2 * inch, pnum)

        c.setFont("Helvetica-Bold", 12)
        c.setFillColor(DARK_NAVY)
        c.drawString((x + 0.2) * inch, HEIGHT - 2.5 * inch, ptitle)

        c.setFont("Helvetica", 9)
        c.setFillColor(SECONDARY_TEXT)
        c.drawString((x + 0.2) * inch, HEIGHT - 2.75 * inch, ptime)

        c.setFont("Helvetica-Bold", 9)
        c.setFillColor(DARK_NAVY)
        c.drawString((x + 0.2) * inch, HEIGHT - 3.1 * inch, "Asosiy vazifalar:")

        y_pt = 3.35
        for task in ptasks:
            lines = simpleSplit(f"• {task}", "Helvetica", 8.5, (col14_w - 0.4) * inch)
            draw_text_lines(c, lines, x + 0.2, y_pt, font_name="Helvetica", font_size=8.5, color=DARK_TEXT, line_height_pt=11.5)
            y_pt += len(lines) * 0.18 + 0.08
    c.showPage()

    # =========================================================================
    # SLIDE 15 — KUTILAYOTGAN IQTISODIY SAMARA
    # =========================================================================
    c.setFillColor(LIGHT_BG)
    c.rect(0, 0, WIDTH, HEIGHT, stroke=0, fill=1)
    draw_header(c, "Samaradorlik va ROI", "Kutilayotgan iqtisodiy va ekologik samara", "Korxona, energetika tizimi va davlat miqyosidagi o'lchanadigan natijalar")
    draw_footer(c, 15)

    # Left: Enterprise ROI
    draw_card(c, 0.8, 1.85, 5.7, 4.7)
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(PRIMARY_BLUE)
    c.drawString(1.05 * inch, HEIGHT - 2.2 * inch, "KORXONA DARAJASIDAGI FOYDA (ROI)")

    c.setFont("Helvetica-Bold", 13)
    c.setFillColor(DARK_NAVY)
    c.drawString(1.05 * inch, HEIGHT - 2.55 * inch, "O'rtacha ishlab chiqarish korxonasi misolida:")

    roi_items = [
        ("8 – 15% oylik tejamkorlik", "Oylik elektr to'lovi 80 mln so'm bo'lgan korxona har oyda 6.4 – 12 mln so'm tejaydi. Yillik iqtisod: 75 – 140 mln so'm."),
        ("Reaktiv quvvat jarimalarini bartaraf etish", "Kosines fi (cos φ) pasayib ketishi oqibatida qo'llaniladigan jarimalar va ortiqcha to'lovlar 0 ga tushiriladi."),
        ("Uskunalar resursini 15–20% ga uzaytirish", "Ortiqcha qizib ketish, quruq ishlash va ortiqcha zo'riqishlar oldi olinishi hisobiga ta'mirlash xarajatlari kamayadi."),
        ("Investitsiyaning oqlanishi (Payback period)", "NEXTGEN obuna narxi tejalgan mablag'ning atigi 10–15% qismini tashkil etadi. Tizim birinchi haftadayoq o'zini oqlaydi.")
    ]
    y_roi = 2.9
    for rh, rd in roi_items:
        c.setFont("Helvetica-Bold", 9.5)
        c.setFillColor(DARK_NAVY)
        c.drawString(1.05 * inch, HEIGHT - y_roi * inch, f"✔  {rh}")
        y_roi += 0.22
        lines = simpleSplit(rd, "Helvetica", 9, 5.2 * inch)
        draw_text_lines(c, lines, 1.25, y_roi, font_name="Helvetica", font_size=9, color=SECONDARY_TEXT, line_height_pt=12)
        y_roi += len(lines) * 0.2 + 0.15

    # Right: National / ESG
    draw_card(c, 6.8, 1.85, 5.733, 4.7)
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(SUCCESS_GREEN)
    c.drawString(7.05 * inch, HEIGHT - 2.2 * inch, "MILLIY VA EKOLOGIK TA'SIR (ESG)")

    c.setFont("Helvetica-Bold", 13)
    c.setFillColor(DARK_NAVY)
    c.drawString(7.05 * inch, HEIGHT - 2.55 * inch, "O'zbekiston energetika tizimiga qo'shiladigan hissa:")

    nat_items = [
        ("Tarmoqdagi pik yuklamalarni yumshatish", "Pik soatlarda (17:00–21:00) korxonalarning asossiz yuklamalarini kamaytirish orqali umumiy tarmoq avariyalarining oldi olinadi."),
        ("Uglerod izini (CO2) qisqartirish", "Har 1,000 kWh tejalgan elektr energiyasi atmosferaga chiqariladigan taxminan 450–500 kg CO2 chiqindisini kamaytiradi."),
        ("O'zbekiston – 2030 strategiyasini qo'llash", "Iqtisodiyotda energiya sig'imini 30% ga kamaytirish bo'yicha davlat dasturiga to'g'ridan-to'g'ri amaliy hissa qo'shadi."),
        ("Eksportbop korxonalar uchun sertifikatlar", "Yevropa bozoriga eksport qiluvchi korxonalar uglerod solig'i (CBAM) to'lashdan tejaladi.")
    ]
    y_nat = 2.9
    for nh, nd in nat_items:
        c.setFont("Helvetica-Bold", 9.5)
        c.setFillColor(DARK_NAVY)
        c.drawString(7.05 * inch, HEIGHT - y_nat * inch, f"★  {nh}")
        y_nat += 0.22
        lines = simpleSplit(nd, "Helvetica", 9, 5.2 * inch)
        draw_text_lines(c, lines, 7.25, y_nat, font_name="Helvetica", font_size=9, color=SECONDARY_TEXT, line_height_pt=12)
        y_nat += len(lines) * 0.2 + 0.15
    c.showPage()

    # =========================================================================
    # SLIDE 16 — YAKUNIY CHAQIRIQ / CALL TO ACTION (Hero Dark Blue)
    # =========================================================================
    c.setFillColor(DEEP_BLUE)
    c.rect(0, 0, WIDTH, HEIGHT, stroke=0, fill=1)
    c.setFillColor(PRIMARY_BLUE)
    c.rect(0, HEIGHT - 0.12 * inch, WIDTH, 0.12 * inch, stroke=0, fill=1)

    # Pill
    draw_card(c, 1.0, 0.9, 4.5, 0.42, bg_color=colors.HexColor("#1A4B8C"), border_color=PRIMARY_BLUE, radius=12)
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(LIGHT_BLUE_TEXT)
    c.drawString(1.2 * inch, HEIGHT - 1.17 * inch, "HAMKORLIK VA PILOT LOYIHA  |  2026")

    # Headline
    c.setFont("Helvetica-Bold", 34)
    c.setFillColor(WHITE)
    c.drawString(1.0 * inch, HEIGHT - 2.1 * inch, "NEXTGEN AI bilan energiyani aqlli boshqaring!")

    # Left: Pilot Program Invitation
    draw_card(c, 1.0, 2.7, 6.0, 3.8, bg_color=CARD_DARK_BG, border_color=CARD_DARK_BORDER, radius=8)
    c.setFont("Helvetica-Bold", 11)
    c.setFillColor(LIGHT_BLUE_TEXT)
    c.drawString(1.25 * inch, HEIGHT - 3.05 * inch, "BUGUNGI TAKLIFIMIZ:")

    c.setFont("Helvetica-Bold", 14.5)
    c.setFillColor(WHITE)
    c.drawString(1.25 * inch, HEIGHT - 3.4 * inch, "5 ta Sanoat Korxonasiga 30 Kunlik Bepul Pilot")

    inv_points = [
        "Hisoblagich ma'lumotlarini bepul audit qilish va tizimga ulash",
        "Kechki isroflar va anomaliyalarni aniqlash hisoboti",
        "O'zbek tilidagi AI maslahatchi va Telegram botga to'liq kirish",
        "Korxona rahbariyati uchun 8–15% tejamkorlik yo'l xaritasi",
        "Hech qanday dastlabki to'lov yoki majburiyat talab etilmaydi"
    ]
    y_inv = 3.75
    for pt in inv_points:
        c.setFont("Helvetica", 10)
        c.setFillColor(colors.HexColor("#E0EEFF"))
        c.drawString(1.25 * inch, HEIGHT - y_inv * inch, f"✔  {pt}")
        y_inv += 0.38

    # Right: Contact Card
    draw_card(c, 7.3, 2.7, 5.0, 3.8, bg_color=CARD_DARK_BG, border_color=PRIMARY_BLUE, radius=8)
    c.setFont("Helvetica-Bold", 11)
    c.setFillColor(LIGHT_BLUE_TEXT)
    c.drawString(7.55 * inch, HEIGHT - 3.05 * inch, "BOG'LANISH VA MUALLIF:")

    c.setFont("Helvetica-Bold", 16)
    c.setFillColor(WHITE)
    c.drawString(7.55 * inch, HEIGHT - 3.45 * inch, "Shohjahon Abdullayev")

    c.setFont("Helvetica", 10)
    c.setFillColor(LIGHT_BLUE_SUB)
    c.drawString(7.55 * inch, HEIGHT - 3.75 * inch, "NEXTGEN AI asoschisi va loyiha yetakchisi")

    c_details = [
        ("Veb platforma", "nextgen-ai-87ff.vercel.app"),
        ("Telegram Bot", "@nextgenuzz_bot"),
        ("Mobil ilova", "Telegram orqali /apk buyrug'i"),
        ("Hamkorlik", "Toshkent shahri, O'zbekiston")
    ]
    y_cd = 4.2
    for clbl, cval in c_details:
        c.setFont("Helvetica-Bold", 10)
        c.setFillColor(LIGHT_BLUE_TEXT)
        c.drawString(7.55 * inch, HEIGHT - y_cd * inch, f"•  {clbl}:")
        c.setFont("Helvetica", 10)
        c.setFillColor(WHITE)
        c.drawString(8.8 * inch, HEIGHT - y_cd * inch, cval)
        y_cd += 0.35

    # Footer
    c.setFont("Helvetica-Oblique", 10)
    c.setFillColor(LIGHT_BLUE_TEXT)
    c.drawString(1.0 * inch, 0.45 * inch, "E'tiboringiz uchun tashakkur! Savollaringizga mamnuniyat bilan javob beraman.")
    c.showPage()

    # =========================================================================
    # SLIDE 17 (APPENDIX A) — TIZIMNING TO'LIQ TEXNIK ARXITEKTURASI
    # =========================================================================
    c.setFillColor(LIGHT_BG)
    c.rect(0, 0, WIDTH, HEIGHT, stroke=0, fill=1)
    draw_header(c, "Texnik ilova (Appendix A)", "Tizimning to'liq arxitekturasi va komponentlar o'zaro aloqasi", "Frontend, API Gateway, Analitika Dvigateli, Xavfsizlik va Bot integratsiyasi")
    draw_footer(c, 17)

    app_cards = [
        ("1. Mijoz Qatlami (Client Layer)", [
            "Next.js 14 App Router, TypeScript, Tailwind CSS",
            "Recharts yordamida interaktiv SVG grafiklar",
            "PWA & Responsive veb dizayn barcha ekranlar uchun",
            "Telegram Bot (@nextgenuzz_bot) va Android APK ilovasi"
        ], PRIMARY_BLUE),

        ("2. API & Xavfsizlik Qatlami (Backend)", [
            "FastAPI yuqori unumdorlikdagi asinxron ASGI server",
            "JWT va Argon2 asosidagi ko'p bosqichli autentifikatsiya",
            "Multi-tenant ajratish (Har bir korxona uchun tenant_id)",
            "CORS, Rate Limiting va so'rovlar validatsiyasi"
        ], DEEP_BLUE),

        ("3. Hisoblash va Analitika Dvigateli", [
            "SQLAlchemy ORM + Pandas / NumPy statistik hisoblar",
            "Z-Score (keskin sakrash) va IQR (oraliq) anomaliya filtri",
            "Differensial tarif matrisasi: Tungi, Kunduzgi, Pik soatlar",
            "Eksponensial tekislash orqali keyingi oy sarf bashorati"
        ], WARNING_AMBER),

        ("4. Grounded AI & Tahlil Qatlami", [
            "Deterministik ma'lumotlar bilan chegaralangan promptlar",
            "Gallyutsinatsiyani cheklovchi xavfsizlik filtrlari",
            "O'zbek tili leksikasiga moslashtirilgan tahlilchi shablonlar",
            "Telegram va PDF hisobotlar generatori"
        ], SUCCESS_GREEN)
    ]
    for idx, (ac_t, ac_items, ac_clr) in enumerate(app_cards):
        row = idx // 2
        col = idx % 2
        x = 0.8 + col * 5.95
        y = 1.85 + row * 2.4

        draw_card(c, x, y, 5.75, 2.25)
        draw_card_accent(c, x, y, 5.75, ac_clr)

        c.setFont("Helvetica-Bold", 11.5)
        c.setFillColor(DARK_NAVY)
        c.drawString((x + 0.2) * inch, HEIGHT - (y + 0.35) * inch, ac_t)

        y_it = y + 0.65
        for item in ac_items:
            c.setFont("Helvetica", 9)
            c.setFillColor(DARK_TEXT)
            c.drawString((x + 0.2) * inch, HEIGHT - y_it * inch, f"•  {item}")
            y_it += 0.24
    c.showPage()

    # =========================================================================
    # SLIDE 18 (APPENDIX B) — HISOBLASH METODOLOGIYASI
    # =========================================================================
    c.setFillColor(LIGHT_BG)
    c.rect(0, 0, WIDTH, HEIGHT, stroke=0, fill=1)
    draw_header(c, "Texnik ilova (Appendix B)", "Hisoblash metodologiyasi va matematik modellar", "Quvvat (kW), sarf (kWh), Z-Score anomaliya va differensial tarif formulalari")
    draw_footer(c, 18)

    math_blocks = [
        ("1. Faol Quvvat (kW) va Sarf (kWh) Aloqasi", 
         "E(kWh) = P(kW) × t(soat)",
         "Iste'mol qilingan energiya (kWh) uskunaning joriy faol quvvati (kW) va ishlash vaqti ko'paytmasiga teng. NEXTGEN ikkala ko'rsatkichni ham alohida kuzatadi: kW — tarmoq zo'riqishini, kWh — pul xarajatini belgilaydi."),
        
        ("2. Z-Score Anomaliya Aniqlash Modeli", 
         "Z = (X - μ) / σ  (Chegara: |Z| > 2.5 yoki 3.0)",
         "X — joriy soatlik sarf, μ — o'rtacha iste'mol, σ — standart og'ish. Agar Z-score 2.5 dan oshsa, bu me'yordan tashqari kritik anomaliya hisoblanadi va ogohlantirish yuboriladi."),

        ("3. Differensial Tariflash Formulasi", 
         "Jami To'lov = Σ (E_tungi × T_tungi) + Σ (E_yarim_pik × T_yarim) + Σ (E_pik × T_pik)",
         "O'zbekiston sanoat tariflariga muvofiq: Tungi soatlar (23:00–06:00, 0.5x arzon koeffitsiyent), Yarim pik (06:00–17:00, 21:00–23:00, 1.0x asosiy), Pik soatlar (17:00–21:00, 1.5x oshirilgan koeffitsiyent)."),

        ("4. Reaktiv Quvvat va Kosines Fi (cos φ)", 
         "cos φ = P / S  (P — faol quvvat kW, S — to'liq quvvat kVA)",
         "Agar korxonada reaktiv quvvat kompensatsiyasi yaxshi bo'lmasa va cos φ 0.85 dan pastga tushsa, elektr tarmoqlari korxonasiga jarima to'lanadi. NEXTGEN buni oldindan ogohlantiradi.")
    ]
    for idx, (m_title, m_formula, m_exp) in enumerate(math_blocks):
        row = idx // 2
        col = idx % 2
        x = 0.8 + col * 5.95
        y = 1.85 + row * 2.4

        draw_card(c, x, y, 5.75, 2.25)

        c.setFont("Helvetica-Bold", 11)
        c.setFillColor(DARK_NAVY)
        c.drawString((x + 0.2) * inch, HEIGHT - (y + 0.3) * inch, m_title)

        c.setFont("Courier-Bold", 10)
        c.setFillColor(PRIMARY_BLUE)
        c.drawString((x + 0.2) * inch, HEIGHT - (y + 0.6) * inch, m_formula)

        lines = simpleSplit(m_exp, "Helvetica", 8.5, 5.35 * inch)
        draw_text_lines(c, lines, x + 0.2, y + 0.85, font_name="Helvetica", font_size=8.5, color=DARK_TEXT, line_height_pt=11.5)
    c.showPage()

    # =========================================================================
    # SLIDE 19 (APPENDIX C) — XATARLAR TAHLILI VA ULARNI YUMSHATISH
    # =========================================================================
    c.setFillColor(LIGHT_BG)
    c.rect(0, 0, WIDTH, HEIGHT, stroke=0, fill=1)
    draw_header(c, "Texnik ilova (Appendix C)", "Xatarlar tahlili va ularni yumshatish choralari", "Texnik, operatsion, qonunchilik va xavfsizlik risklarini professional boshqarish")
    draw_footer(c, 19)

    risks = [
        ("1. Ma'lumotlar sifati pastligi (GIGO)", 
         "Xatar: Korxona hisoblagichlarida uzilishlar bo'lishi yoki Excel faylda noto'g'ri raqamlar kiritilishi.",
         "Yumshatish: Tizim ichiga avtomatlashtirilgan validatsiya, anomaliya filtrlari va yetishmayotgan qatorlarni statistik to'ldirish algoritmlari kiritilgan.",
         WARNING_AMBER),

        ("2. Korxonada Internet uzilishi", 
         "Xatar: Sanoat zonalarida internet vaqti-vaqti bilan uzilib qolishi mumkin.",
         "Yumshatish: Lokal kesh va oflayn rejim. Internet tiklanganda to'plangan ma'lumotlar avtomatik sinxronizatsiya qilinadi.",
         PRIMARY_BLUE),

        ("3. Xodimlarning o'rganishni istamasligi", 
         "Xatar: Bosh muhandis yoki energetiklar murakkab dasturlarni o'rganishni istamasligi.",
         "Yumshatish: O'ta sodda veb-panel va har kimga tanish bo'lgan Telegram boti. Barcha hisobotlar tushunarli o'zbek tilida beriladi.",
         SUCCESS_GREEN),

        ("4. Kiberxavfsizlik va ma'lumotlar sizishi", 
         "Xatar: Korxonaning elektr iste'moli ma'lumotlarining tashqariga chiqishi.",
         "Yumshatish: Multi-tenant arxitektura, shifrlangan ma'lumotlar bazasi va strategik zavodlar uchun to'liq lokal On-Premise o'rnatish imkoniyati.",
         DEEP_BLUE)
    ]
    for idx, (rt, rdesc, rmit, rclr) in enumerate(risks):
        row = idx // 2
        col = idx % 2
        x = 0.8 + col * 5.95
        y = 1.85 + row * 2.4

        draw_card(c, x, y, 5.75, 2.25)
        draw_card_accent(c, x, y, 5.75, rclr)

        c.setFont("Helvetica-Bold", 11)
        c.setFillColor(DARK_NAVY)
        c.drawString((x + 0.2) * inch, HEIGHT - (y + 0.35) * inch, rt)

        lines1 = simpleSplit(rdesc, "Helvetica", 8.5, 5.35 * inch)
        draw_text_lines(c, lines1, x + 0.2, y + 0.6, font_name="Helvetica", font_size=8.5, color=DARK_TEXT, line_height_pt=11.5)

        lines2 = simpleSplit(f"✔  Yechim: {rmit}", "Helvetica-Bold", 8.5, 5.35 * inch)
        draw_text_lines(c, lines2, x + 0.2, y + 1.25, font_name="Helvetica-Bold", font_size=8.5, color=rclr, line_height_pt=11.5)
    c.showPage()

    # =========================================================================
    # SLIDE 20 (APPENDIX D) — HAKAMLAR VA INVESTORLAR UCHUN ASOSIY Q&A
    # =========================================================================
    c.setFillColor(LIGHT_BG)
    c.rect(0, 0, WIDTH, HEIGHT, stroke=0, fill=1)
    draw_header(c, "Texnik ilova (Appendix D)", "Hakamlar va investorlar uchun asosiy savol-javoblar", "Eng ko'p beriladigan 5 ta strategik savolga qisqa va qat'iy javoblar")
    draw_footer(c, 20)

    qa_list = [
        ("1. ASKUE tizimidan farqingiz nima?", 
         "ASKUE — elektr tarmog'i (HET) uchun hisob-faktura chiqaruvchi apparat tizim. NEXTGEN AI esa korxona direktoriga pulni tejash yo'llarini ko'rsatuvchi tahliliy aql va dasturiy ta'minotdir."),
        ("2. Sun'iy intellekt xato hisoblab qo'ymaydimi?", 
         "Yo'q. Barcha kilovattlar, xarajatlar va anomaliyalar qat'iy matematik formulalar (SQL/Python) bilan hisoblanadi. LLM faqat olingan natijani tushunarli o'zbek tilida bayon qiladi."),
        ("3. Qanday korxonalarga birinchi navbatda kirasiz?", 
         "Oylik elektr sarfi 20 million so'mdan ortiq bo'lgan to'qimachilik, oziq-ovqat va metallurgiya korxonalari. Ular uchun har 10% tejamkorlik yillik yuz millionlab so'm foydadir."),
        ("4. Hozirda tizimning qaysi qismlari tayyor?", 
         "Veb boshqaruv paneli (Vercel), FastAPI backend, @nextgenuzz_bot Telegram boti va Android APK to'liq ishlab turibdi. 5 ta korxonada pilot loyiha boshlanmoqda."),
        ("5. Birinchi oydayoq qancha mablag' tejaladi?", 
         "Amaliyotda kechki rejimdagi asossiz yuklamalar va noto'g'ri sozlangan uskunalarni to'g'rilash hisobiga korxonalar birinchi oydayoq 8–15% tejamkorlikka erishadi.")
    ]
    card20_h = 0.9
    gap20 = 0.08
    for idx, (q, a) in enumerate(qa_list):
        y = 1.85 + idx * (card20_h + gap20)
        draw_card(c, 0.8, y, 11.733, card20_h)
        draw_card_accent(c, 0.8, y, 0.08, PRIMARY_BLUE, bar_h_in=card20_h)

        c.setFont("Helvetica-Bold", 10)
        c.setFillColor(DARK_NAVY)
        c.drawString(1.05 * inch, HEIGHT - (y + 0.28) * inch, q)

        lines = simpleSplit(f"Javob: {a}", "Helvetica", 9, 11.2 * inch)
        draw_text_lines(c, lines, 1.05, y + 0.5, font_name="Helvetica", font_size=9, color=DARK_TEXT, line_height_pt=12)
    c.showPage()

    # Save PDF
    c.save()
    print(f"PDF successfully saved to {output_path}")

if __name__ == "__main__":
    out_dir = os.path.dirname(os.path.abspath(__file__))
    out_pdf = os.path.join(out_dir, "NEXTGEN_AI_Presentation_UZ.pdf")
    build_pdf(out_pdf)
