import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

# --- COLOR SYSTEM ---
PRIMARY_BLUE = RGBColor(21, 94, 239)       # #155EEF
DEEP_BLUE = RGBColor(18, 59, 114)          # #123B72
DARK_NAVY = RGBColor(15, 23, 42)           # #0F172A
DARK_TEXT = RGBColor(23, 43, 77)           # #172B4D
SECONDARY_TEXT = RGBColor(100, 116, 139)   # #64748B
LIGHT_BG = RGBColor(245, 248, 252)         # #F5F8FC
CARD_BG = RGBColor(255, 255, 255)          # #FFFFFF
BORDER_COLOR = RGBColor(228, 234, 242)     # #E4EAF2
SUCCESS_GREEN = RGBColor(18, 166, 106)     # #12A66A
WARNING_AMBER = RGBColor(245, 158, 11)     # #F59E0B
ACCENT_LIGHT = RGBColor(238, 244, 255)     # #EEF4FF
WHITE = RGBColor(255, 255, 255)

FONT_HEADING = "Calibri"
FONT_BODY = "Calibri"

def apply_background(slide, color):
    bg_shape = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5)
    )
    bg_shape.fill.solid()
    bg_shape.fill.fore_color.rgb = color
    bg_shape.line.fill.background()
    return bg_shape

def add_header(slide, category, title, subtitle):
    # Category Tag / Breadcrumb
    tag_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.42), Inches(11.5), Inches(0.3))
    tf_tag = tag_box.text_frame
    tf_tag.word_wrap = True
    tf_tag.margin_left = tf_tag.margin_top = tf_tag.margin_right = tf_tag.margin_bottom = 0
    p_tag = tf_tag.paragraphs[0]
    p_tag.text = category.upper()
    p_tag.font.name = FONT_HEADING
    p_tag.font.size = Pt(9.5)
    p_tag.font.bold = True
    p_tag.font.color.rgb = PRIMARY_BLUE

    # Title
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.72), Inches(11.5), Inches(0.55))
    tf_title = title_box.text_frame
    tf_title.word_wrap = True
    tf_title.margin_left = tf_title.margin_top = tf_title.margin_right = tf_title.margin_bottom = 0
    p_title = tf_title.paragraphs[0]
    p_title.text = title
    p_title.font.name = FONT_HEADING
    p_title.font.size = Pt(21)
    p_title.font.bold = True
    p_title.font.color.rgb = DARK_NAVY

    # Subtitle
    if subtitle:
        sub_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.30), Inches(11.5), Inches(0.35))
        tf_sub = sub_box.text_frame
        tf_sub.word_wrap = True
        tf_sub.margin_left = tf_sub.margin_top = tf_sub.margin_right = tf_sub.margin_bottom = 0
        p_sub = tf_sub.paragraphs[0]
        p_sub.text = subtitle
        p_sub.font.name = FONT_BODY
        p_sub.font.size = Pt(11.5)
        p_sub.font.color.rgb = SECONDARY_TEXT

def add_footer(slide, current_slide, total_slides=20):
    # Divider line
    line = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(6.85), Inches(11.733), Inches(0.015)
    )
    line.fill.solid()
    line.fill.fore_color.rgb = BORDER_COLOR
    line.line.fill.background()

    # Left text
    box_left = slide.shapes.add_textbox(Inches(0.8), Inches(6.92), Inches(9.5), Inches(0.3))
    tf_left = box_left.text_frame
    tf_left.word_wrap = True
    tf_left.margin_left = tf_left.margin_top = tf_left.margin_right = tf_left.margin_bottom = 0
    p_l = tf_left.paragraphs[0]
    p_l.text = "NEXTGEN AI — O'zbekiston sanoati uchun energiya intellekti platformasi  |  Muallif: Shohjahon Abdullayev"
    p_l.font.name = FONT_BODY
    p_l.font.size = Pt(8.5)
    p_l.font.color.rgb = SECONDARY_TEXT

    # Right text (Slide number)
    box_right = slide.shapes.add_textbox(Inches(10.5), Inches(6.92), Inches(2.0), Inches(0.3))
    tf_right = box_right.text_frame
    tf_right.word_wrap = True
    tf_right.margin_left = tf_right.margin_top = tf_right.margin_right = tf_right.margin_bottom = 0
    p_r = tf_right.paragraphs[0]
    p_r.alignment = PP_ALIGN.RIGHT
    p_r.text = f"{current_slide:02d} / {total_slides:02d}"
    p_r.font.name = FONT_HEADING
    p_r.font.size = Pt(8.5)
    p_r.font.bold = True
    p_r.font.color.rgb = PRIMARY_BLUE

def add_card(slide, left, top, width, height, bg_color=CARD_BG, border_color=BORDER_COLOR):
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    if border_color:
        card.line.color.rgb = border_color
        card.line.width = Pt(1)
    else:
        card.line.fill.background()
    return card

def set_speaker_notes(slide, notes_text):
    notes_slide = slide.notes_slide
    tf = notes_slide.notes_text_frame
    tf.text = notes_text

def build_presentation(output_path):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # =========================================================================
    # SLIDE 01 — MUQOVA / TITLE SLIDE (Hero Dark Blue)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    apply_background(s1, DEEP_BLUE)

    # Accent decorative top strip
    top_strip = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.12))
    top_strip.fill.solid()
    top_strip.fill.fore_color.rgb = PRIMARY_BLUE
    top_strip.line.fill.background()

    # Category Pill
    pill = add_card(s1, Inches(1.0), Inches(1.1), Inches(4.3), Inches(0.42), bg_color=RGBColor(26, 75, 140), border_color=PRIMARY_BLUE)
    tb_pill = s1.shapes.add_textbox(Inches(1.1), Inches(1.16), Inches(4.1), Inches(0.3))
    tf_p = tb_pill.text_frame
    p_pill = tf_p.paragraphs[0]
    p_pill.text = "MILLIY STARTAP TADBIRI  |  TOSHKENT 2026"
    p_pill.font.name = FONT_HEADING
    p_pill.font.size = Pt(10)
    p_pill.font.bold = True
    p_pill.font.color.rgb = RGBColor(186, 215, 255)

    # Main Brand Title
    tb_brand = s1.shapes.add_textbox(Inches(0.95), Inches(1.75), Inches(11.0), Inches(1.1))
    tf_b = tb_brand.text_frame
    p_b = tf_b.paragraphs[0]
    p_b.text = "NEXTGEN AI"
    p_b.font.name = FONT_HEADING
    p_b.font.size = Pt(46)
    p_b.font.bold = True
    p_b.font.color.rgb = WHITE

    # Subtitle
    tb_sub = s1.shapes.add_textbox(Inches(1.0), Inches(2.95), Inches(11.0), Inches(0.6))
    tf_s = tb_sub.text_frame
    p_s = tf_s.paragraphs[0]
    p_s.text = "Enterprise Energy Intelligence Platform"
    p_s.font.name = FONT_HEADING
    p_s.font.size = Pt(22)
    p_s.font.color.rgb = RGBColor(147, 197, 253)

    # Tagline in Uzbek
    tb_tag = s1.shapes.add_textbox(Inches(1.0), Inches(3.65), Inches(11.0), Inches(0.6))
    tf_t = tb_tag.text_frame
    p_t = tf_t.paragraphs[0]
    p_t.text = "“Har bir kilovatt — aqlli qaror, samarali kelajak.”"
    p_t.font.name = FONT_BODY
    p_t.font.size = Pt(16)
    p_t.font.italic = True
    p_t.font.color.rgb = RGBColor(224, 238, 255)

    # Context Card (Lower left)
    card_info = add_card(s1, Inches(1.0), Inches(4.5), Inches(7.2), Inches(1.8), bg_color=RGBColor(24, 66, 125), border_color=RGBColor(45, 95, 170))
    tb_ci = s1.shapes.add_textbox(Inches(1.2), Inches(4.65), Inches(6.8), Inches(1.5))
    tf_ci = tb_ci.text_frame
    tf_ci.word_wrap = True
    p1 = tf_ci.paragraphs[0]
    p1.text = "Loyiha missiyasi:"
    p1.font.bold = True
    p1.font.size = Pt(11)
    p1.font.color.rgb = RGBColor(186, 215, 255)
    
    p2 = tf_ci.add_paragraph()
    p2.text = "O'zbekiston sanoat va ishlab chiqarish korxonalarida elektr energiyasi sarfini sun'iy intellekt va aniq analitika orqali shaffof boshqarish, isrofgarchilikni yo'qotish va xarajatlarni 8–15% ga qisqartirish."
    p2.font.size = Pt(11.5)
    p2.font.color.rgb = WHITE
    p2.space_before = Pt(4)

    # Attribution Card (Lower right)
    card_attr = add_card(s1, Inches(8.5), Inches(4.5), Inches(3.8), Inches(1.8), bg_color=RGBColor(24, 66, 125), border_color=RGBColor(45, 95, 170))
    tb_ca = s1.shapes.add_textbox(Inches(8.7), Inches(4.65), Inches(3.4), Inches(1.5))
    tf_ca = tb_ca.text_frame
    tf_ca.word_wrap = True
    pa1 = tf_ca.paragraphs[0]
    pa1.text = "Loyiha muallifi va dasturchi:"
    pa1.font.size = Pt(10)
    pa1.font.color.rgb = RGBColor(186, 215, 255)

    pa2 = tf_ca.add_paragraph()
    pa2.text = "Shohjahon Abdullayev"
    pa2.font.name = FONT_HEADING
    pa2.font.bold = True
    pa2.font.size = Pt(15)
    pa2.font.color.rgb = WHITE
    pa2.space_before = Pt(2)

    pa3 = tf_ca.add_paragraph()
    pa3.text = "Platforma: nextgen-ai-87ff.vercel.app\nTelegram Bot: @nextgenuzz_bot"
    pa3.font.size = Pt(10)
    pa3.font.color.rgb = RGBColor(147, 197, 253)
    pa3.space_before = Pt(6)

    # Footer on cover
    tb_cf = s1.shapes.add_textbox(Inches(1.0), Inches(6.9), Inches(11.3), Inches(0.3))
    tf_cf = tb_cf.text_frame
    p_cf = tf_cf.paragraphs[0]
    p_cf.text = "O'zbekiston Respublikasi  •  Milliy texnologik startap taqdimoti  •  2026"
    p_cf.font.size = Pt(9)
    p_cf.font.color.rgb = RGBColor(147, 197, 253)

    set_speaker_notes(s1, 
        "HURMATLI HAKAMLAR, INVESTORLAR VA FORUM ISHTIROKCHILARI!\n\n"
        "Men Shohjahon Abdullayevman va bugun sizga O'zbekiston sanoati uchun muhim bo'lgan milliy texnologik yechim — NEXTGEN AI platformasini taqdim etaman.\n\n"
        "Bugungi kunda har bir sanoat korxonasining eng og'riqli xarajat moddalaridan biri bu — elektr energiyasidir. Bizning shiorimiz: 'Har bir kilovatt — aqlli qaror, samarali kelajak'.\n\n"
        "NEXTGEN AI — bu shunchaki monitoring tizimi yoki oddiy chatbot emas. Bu korxona rahbarlari, bosh muhandislari va energetiklariga elektr energiyasini tushunarli, shaffof va tejamkor boshqarish imkonini beruvchi korporativ intellektual platformadir."
    )

    # =========================================================================
    # SLIDE 02 — IJROIYA XULOSASI / EXECUTIVE SUMMARY
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    apply_background(s2, LIGHT_BG)
    add_header(s2, "Loyiha pasporti", "Ijroiya xulosasi: 30 soniyada NEXTGEN AI mohiyati", "Korxona elektr sarfini nazoratsiz 'qora quti'dan o'lchanadigan iqtisodiy foydaga aylantirish")
    add_footer(s2, 2)

    # 4 Key Pillars in Cards
    col_w = Inches(2.78)
    gap = Inches(0.2)
    top_y = Inches(1.85)
    h_card = Inches(3.2)

    pillars = [
        ("01. Shaffoflik", "To'liq ko'rinuvchanlik", "Hisoblagichlar va sexlar kesimida soatma-soat elektr sarfini vizuallashtirish. Oylik hisob-fakturani kutmasdan, real vaqtda sarf dinamikasini ko'rish.", PRIMARY_BLUE),
        ("02. Nazorat", "Anomaliyalarni aniqlash", "Kechki payt yoki dam olish kunlari uskunalar behuda ishlashi, qisqa tutashuvlar va yuklama me'yordan oshishini darhol aniqlash va xabar berish.", WARNING_AMBER),
        ("03. Intellekt", "Grounded AI Tahlilchi", "Sun'iy intellekt korxona sarf matrisasini tahlil qilib, rahbar va muhandisga o'zbek tilida aniq, faktlarga asoslangan optimallashtirish tavsiyalarini beradi.", PRIMARY_BLUE),
        ("04. Iqtisod", "8–15% Tejamkorlik", "Reaktiv quvvat jarimalari, samarasiz yuklama va tungi isroflarni bartaraf etish hisobiga oylik elektr xarajatlarini sezilarli darajada qisqartirish.", SUCCESS_GREEN)
    ]

    for idx, (step, title_p, desc_p, accent) in enumerate(pillars):
        x = Inches(0.8) + idx * (col_w + gap)
        add_card(s2, x, top_y, col_w, h_card)
        # Accent top bar in card
        c_bar = s2.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, top_y, col_w, Inches(0.08))
        c_bar.fill.solid()
        c_bar.fill.fore_color.rgb = accent
        c_bar.line.fill.background()

        tb = s2.shapes.add_textbox(x + Inches(0.2), top_y + Inches(0.2), col_w - Inches(0.4), h_card - Inches(0.4))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p_step = tf.paragraphs[0]
        p_step.text = step.upper()
        p_step.font.name = FONT_HEADING
        p_step.font.size = Pt(9.5)
        p_step.font.bold = True
        p_step.font.color.rgb = accent

        p_t = tf.add_paragraph()
        p_t.text = title_p
        p_t.font.name = FONT_HEADING
        p_t.font.size = Pt(14)
        p_t.font.bold = True
        p_t.font.color.rgb = DARK_NAVY
        p_t.space_before = Pt(4)

        p_d = tf.add_paragraph()
        p_d.text = desc_p
        p_d.font.name = FONT_BODY
        p_d.font.size = Pt(10.5)
        p_d.font.color.rgb = DARK_TEXT
        p_d.space_before = Pt(8)

    # Bottom Metric Highlight Band
    band = add_card(s2, Inches(0.8), Inches(5.25), Inches(11.733), Inches(1.35), bg_color=CARD_BG, border_color=PRIMARY_BLUE)
    
    m_items = [
        ("8–15%", "O'rtacha xarajat qisqarishi", "Ishlab chiqarish quvvatini pasaytirmagan holda"),
        ("100%", "Gallyutsinatsiyasiz hisob", "Faqat matematik formulalar asosida hisoblangan aniqlik"),
        ("< 2 daqiqa", "Ogohlantirish tezligi", "Anomal sarf yuzaga kelganda Telegram orqali xabar"),
        ("O'zbek tilida", "Mahalliy tilda to'liq qo'llab-quvvatlash", "Web interfeys, hisobotlar va Telegram bot")
    ]
    sub_w = Inches(11.733) / 4
    for idx, (val, lbl, note) in enumerate(m_items):
        mx = Inches(0.8) + idx * sub_w
        tb_m = s2.shapes.add_textbox(mx + Inches(0.15), Inches(5.35), sub_w - Inches(0.3), Inches(1.15))
        tf_m = tb_m.text_frame
        tf_m.word_wrap = True
        
        pm1 = tf_m.paragraphs[0]
        pm1.text = val
        pm1.font.name = FONT_HEADING
        pm1.font.size = Pt(18)
        pm1.font.bold = True
        pm1.font.color.rgb = PRIMARY_BLUE

        pm2 = tf_m.add_paragraph()
        pm2.text = lbl
        pm2.font.name = FONT_HEADING
        pm2.font.size = Pt(10)
        pm2.font.bold = True
        pm2.font.color.rgb = DARK_NAVY

        pm3 = tf_m.add_paragraph()
        pm3.text = note
        pm3.font.name = FONT_BODY
        pm3.font.size = Pt(8.5)
        pm3.font.color.rgb = SECONDARY_TEXT

    set_speaker_notes(s2,
        "VAQT: 45 SONIYA\n\n"
        "Hurmatli hakamlar, tasavvur qiling: O'zbekistondagi o'rtacha ishlab chiqarish korxonasi har oyda 30 milliondan 300 million so'mgacha elektr energiyasiga pul to'laydi. Ammo rahbar bu summaning qanchasi samarasiz yo'qotilganini bilmaydi.\n\n"
        "NEXTGEN AI 4 ta ustun ustiga qurilgan:\n"
        "1. To'liq shaffoflik: qaysi sex, qaysi uskuna qancha sarflayotgani ko'rinadi.\n"
        "2. Anomaliya nazorati: kechki isroflar va nosozliklar darhol tutiladi.\n"
        "3. Sun'iy intellekt tahlili: muhandisga o'zbek tilida tayyor tavsiyalar beriladi.\n"
        "4. O'lchanadigan natija: korxona ishlab chiqarishni to'xtatmasdan 8-15% xarajatini tejaydi.\n\n"
        "Eng muhimi — bizning AI hisob-kitoblarni o'zidan to'qimaydi. Barcha matematik tahlil deterministik SQL va statistik qatlamda bajariladi, LLM esa faqat tahlil qilib beradi."
    )

    # =========================================================================
    # SLIDE 03 — BOZORDAGI ASOSIY MUAMMO / THE PROBLEM
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    apply_background(s3, LIGHT_BG)
    add_header(s3, "Bozor tahlili", "Asosiy muammo: Korxonalarda elektr energiyasi 'qora quti' bo'lib qolmoqda", "Bugungi kunda sanoat korxonalari elektr xarajatlarini boshqarishda 3 ta tizimli qiyinchilikka duch kelmoqda")
    add_footer(s3, 3)

    col3_w = Inches(3.7)
    gap3 = Inches(0.3)
    top3_y = Inches(1.85)
    h3_card = Inches(4.7)

    prob_blocks = [
        ("Muammo 1", "Ko'r-ko'rona iste'mol va kechikkan hisob-kitob",
         "Oylik hisob-faktura faqat oy tugagandan so'ng keladi. Rahbar nima sababdan elektr to'lovi 20% ga oshib ketganini o'sha paytda aniqlay olmaydi.",
         ["Ko'rsatkichlar faqat oy oxirida ko'riladi", "Kunlik va soatlik iste'mol dinamikasi yo'q", "Reaktiv yondashuv: pul to'lanadi, sabab noma'lum", "Sexlar o'rtasida sarf bo'yicha mas'uliyat yo'q"],
         RGBColor(239, 68, 68)),
        
        ("Muammo 2", "Kechki isrofgarchilik va yashirin anomaliyalar",
         "Ish vaqtidan tashqari ochiq qolgan sovutgichlar, kompressorlar, havoni shamollatish tizimlari va noto'g'ri sozlangan uskunalar hisobiga ulkan isrof yuz beradi.",
         ["Ish to'xtagan vaqtda ham bazaviy yuklama yuqori", "Uskunalarning amortizatsiyasi va qizib ketishi", "Tungi rejimda elektrning asossiz sarflanishi", "Muhandislar nosozlikni faqat uskuna buzilgach biladi"],
         WARNING_AMBER),

        ("Muammo 3", "Analitik qurol va kadrlar yetishmovchiligi",
         "Mavjud ASKUE/ASUE tizimlari faqat 'quruq' raqamlarni yig'adi. Bosh energetikda millionlab qator ma'lumotlarni tahlil qilib xulosa chiqarishga vaqt va dastur yo'q.",
         ["Ma'lumotlar bor, lekin tushunarli tahlil yo'q", "Kadrlar yetishmovchiligi va qo'lda Excel yuritish", "Reaktiv quvvat va pik soat jarimalarini oldindan bilmaslik", "Rahbariyat uchun qaror qabul qilish mexanizmi yo'qligi"],
         PRIMARY_BLUE)
    ]

    for idx, (tag_p, title_p, desc_p, bullets, accent) in enumerate(prob_blocks):
        x = Inches(0.8) + idx * (col3_w + gap3)
        add_card(s3, x, top3_y, col3_w, h3_card)
        
        bar = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, top3_y, col3_w, Inches(0.08))
        bar.fill.solid()
        bar.fill.fore_color.rgb = accent
        bar.line.fill.background()

        tb = s3.shapes.add_textbox(x + Inches(0.25), top3_y + Inches(0.2), col3_w - Inches(0.5), h3_card - Inches(0.4))
        tf = tb.text_frame
        tf.word_wrap = True

        p_tag = tf.paragraphs[0]
        p_tag.text = tag_p.upper()
        p_tag.font.name = FONT_HEADING
        p_tag.font.size = Pt(10)
        p_tag.font.bold = True
        p_tag.font.color.rgb = accent

        p_t = tf.add_paragraph()
        p_t.text = title_p
        p_t.font.name = FONT_HEADING
        p_t.font.size = Pt(14)
        p_t.font.bold = True
        p_t.font.color.rgb = DARK_NAVY
        p_t.space_before = Pt(4)

        p_d = tf.add_paragraph()
        p_d.text = desc_p
        p_d.font.name = FONT_BODY
        p_d.font.size = Pt(10)
        p_d.font.color.rgb = DARK_TEXT
        p_d.space_before = Pt(8)

        p_b_head = tf.add_paragraph()
        p_b_head.text = "Oqibatlari:"
        p_b_head.font.name = FONT_HEADING
        p_b_head.font.size = Pt(10)
        p_b_head.font.bold = True
        p_b_head.font.color.rgb = DARK_NAVY
        p_b_head.space_before = Pt(12)

        for b in bullets:
            pb = tf.add_paragraph()
            pb.text = f"•  {b}"
            pb.font.name = FONT_BODY
            pb.font.size = Pt(9.5)
            pb.font.color.rgb = SECONDARY_TEXT
            pb.space_before = Pt(3)

    set_speaker_notes(s3,
        "VAQT: 60 SONIYA\n\n"
        "Nima uchun korxonalarga aynan bugun bunday tizim kerak? Keling, amaliyotdagi holatni ko'raylik.\n\n"
        "Birinchidan — Ko'r-ko'rona iste'mol. Zavod direktori oy oxirida 80 million so'mlik schyot-faktura oladi. O'tgan oyda 65 million edi. Nega oshdi? Qaysi sexda ko'p ishlatildi? Qaysi uskunada muammo bo'ldi? Hech kim aniq ayta olmaydi.\n\n"
        "Ikkinchidan — Kechki va dam olish kunlaridagi isrofgarchilik. Ishlab chiqarish to'xtagan, ammo transformator va kompressorlar o'chirilmagan, liniyada yo'qotishlar ketmoqda. Bu har oy millionlab so'm behuda havoga uchmoqda degani.\n\n"
        "Uchinchidan — Mavjud ASKUE hisoblagichlari bor, lekin ular faqat elektr ta'minoti korxonasiga hisob-kitob qilish uchun xizmat qiladi. Zavodning o'ziga bu ma'lumotlar tahlil qilingan holda taqdim etilmaydi. Mana shu bo'shliqni NEXTGEN AI to'ldiradi."
    )

    # =========================================================================
    # SLIDE 04 — O'ZBEKISTON UCHUN DOLZARBLIGI / WHY IT MATTERS IN UZBEKISTAN
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    apply_background(s4, LIGHT_BG)
    add_header(s4, "Davlat siyosati va bozor", "O'zbekiston uchun strategik ahamiyati: Yangi energiya realligi", "Elektr tariflarining erkinlashishi va energiya samaradorligi bo'yicha milliy vazifalar")
    add_footer(s4, 4)

    # Left Column: Legal and Policy Drivers
    card_law = add_card(s4, Inches(0.8), Inches(1.85), Inches(5.7), Inches(4.7))
    tb_l = s4.shapes.add_textbox(Inches(1.05), Inches(2.05), Inches(5.2), Inches(4.3))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True

    pl1 = tf_l.paragraphs[0]
    pl1.text = "DAVLAT DASTURLARI VA HUQUQIY POYDEVOR"
    pl1.font.name = FONT_HEADING
    pl1.font.size = Pt(10)
    pl1.font.bold = True
    pl1.font.color.rgb = PRIMARY_BLUE

    pl2 = tf_l.add_paragraph()
    pl2.text = "Prezident Farmoni (PF-57) va Vazirlar Mahkamasi Qarorlari"
    pl2.font.name = FONT_HEADING
    pl2.font.size = Pt(13)
    pl2.font.bold = True
    pl2.font.color.rgb = DARK_NAVY
    pl2.space_before = Pt(4)

    items_law = [
        ("Tabaqalashtirilgan tariflar islohoti (2024–2026)", 
         "Yuridik shaxslar va sanoat korxonalari uchun elektr energiyasi narxi erkinlashtirildi. 1 kWh narxi 900–1000 so'mga yetdi. Pik va tungi soatlarda differensial to'lovlar joriy etildi."),
        ("O'zbekiston – 2030 Milliy Strategiyasi", 
         "2030 yilgacha iqtisodiyot tarmoqlarida energiya sarfi sig'imini 30 foizga qisqartirish bo'yicha qat'iy davlat ko'rsatkichi belgilandi."),
        ("Majburiy energetik audit va hisobdorlik", 
         "Yirik sanoat va tijorat iste'molchilari uchun energiya samaradorligi me'yorlari va resurslarni oqilona sarflash nazorati kuchaytirilmoqda."),
        ("Eksport qiluvchi korxonalar uchun ESG va uglerod izi", 
         "Yevropa va xalqaro bozorlarga mahsulot yetkazib beruvchi mahalliy to'qimachilik va metallurgiya korxonalari uchun 'yashil' sertifikatlar talab qilinmoqda.")
    ]
    for h, d in items_law:
        ph = tf_l.add_paragraph()
        ph.text = f"•  {h}"
        ph.font.name = FONT_HEADING
        ph.font.size = Pt(10)
        ph.font.bold = True
        ph.font.color.rgb = DARK_NAVY
        ph.space_before = Pt(8)

        pd = tf_l.add_paragraph()
        pd.text = f"   {d}"
        pd.font.name = FONT_BODY
        pd.font.size = Pt(9.5)
        pd.font.color.rgb = SECONDARY_TEXT
        pd.space_before = Pt(2)

    # Right Column: 3 Key Facts / Stat Cards
    right_x = Inches(6.8)
    r_w = Inches(5.733)
    
    stat_cards = [
        ("900 – 1000 so'm / kWh", "Sanoat uchun yangi tarif chegarasi", 
         "Elektr narxining 2 baravardan ortiq oshishi korxona xarajatlar strukturasida energiyaning ulushini 15–25% ga yetkazdi.", PRIMARY_BLUE),
        ("30% ga kamaytirish", "O'zbekiston-2030 davlat maqsadi", 
         "Prezident qarorlariga ko'ra sanoatda har bir birlik mahsulotga to'g'ri keluvchi energiya intensivligini keskin pasaytirish shart.", SUCCESS_GREEN),
        ("50,000+ korxona", "O'zbekistondagi faol sanoat korxonalari", 
         "Davlat statistika qo'mitasi ma'lumotlariga ko'ra mamlakatda minglab korxonalar har oyda energiya xarajatlarini optimallashtirishga muhtoj.", DEEP_BLUE)
    ]

    for idx, (num, title_s, desc_s, clr) in enumerate(stat_cards):
        cy = Inches(1.85) + idx * Inches(1.6)
        add_card(s4, right_x, cy, r_w, Inches(1.45))
        
        cbar = s4.shapes.add_shape(MSO_SHAPE.RECTANGLE, right_x, cy, Inches(0.1), Inches(1.45))
        cbar.fill.solid()
        cbar.fill.fore_color.rgb = clr
        cbar.line.fill.background()

        tbs = s4.shapes.add_textbox(right_x + Inches(0.25), cy + Inches(0.12), r_w - Inches(0.4), Inches(1.2))
        tfs = tbs.text_frame
        tfs.word_wrap = True

        ps1 = tfs.paragraphs[0]
        ps1.text = num
        ps1.font.name = FONT_HEADING
        ps1.font.size = Pt(17)
        ps1.font.bold = True
        ps1.font.color.rgb = clr

        ps2 = tfs.add_paragraph()
        ps2.text = title_s
        ps2.font.name = FONT_HEADING
        ps2.font.size = Pt(10.5)
        ps2.font.bold = True
        ps2.font.color.rgb = DARK_NAVY
        ps2.space_before = Pt(2)

        ps3 = tfs.add_paragraph()
        ps3.text = desc_s
        ps3.font.name = FONT_BODY
        ps3.font.size = Pt(9)
        ps3.font.color.rgb = SECONDARY_TEXT
        ps3.space_before = Pt(2)

    set_speaker_notes(s4,
        "VAQT: 60 SONIYA\n\n"
        "Nima uchun bu mavzu aynan bugun davlat miqyosida dolzarb?\n\n"
        "O'zbekiston Respublikasi Prezidentining PF-57 farmoni va hukumat qarorlari bilan 2024-yildan boshlab energetika sohasida bozor mexanizmlariga o'tildi. Sanoat korxonalari uchun elektr energiyasi tarifi erkinlashtirildi va 1 kilovatt-soat narxi 900–1000 so'mgacha ko'tarildi.\n\n"
        "Ilgari elektr arzon bo'lgan paytda rahbarlar energiya isrofiga ko'z yumishgan bo'lsa, bugungi kunda bu korxona rentabelligini to'g'ridan-to'g'ri pasaytiruvchi omilga aylandi.\n\n"
        "Bundan tashqari, O'zbekiston-2030 strategiyasida energiya sig'imini 30 foizga kamaytirish davlat darajasidagi qat'iy maqsad qilib qo'yilgan. Demak, NEXTGEN AI davlat siyosatiga to'liq mos keladi va korxonalarga ushbu talablarni bajarishda eng samarali dasturiy qurol bo'lib xizmat qiladi."
    )

    # =========================================================================
    # SLIDE 05 — BIZNING YECHIM / OUR SOLUTION (5-Stage Architecture)
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    apply_background(s5, LIGHT_BG)
    add_header(s5, "Texnologik konsepsiya", "Bizning yechim: Ma'lumotdan intellektga 5 bosqichli zanjir", "Xom hisoblagich raqamlarini korxona rahbari va muhandisi uchun tayyor biznes harakatiga aylantirish")
    add_footer(s5, 5)

    stages = [
        ("01", "KORXONA MA'LUMOTLARI", "Hisoblagichlar, Excel/CSV fayllar va ASKUE protokollari orqali sarf ko'rsatkichlari yig'iladi.", PRIMARY_BLUE),
        ("02", "MA'LUMOTLARNI TOZALASH", "Yetishmayotgan qatorlar to'ldiriladi, birliklar (kW vs kWh) tekshiriladi va validatsiya qilinadi.", DEEP_BLUE),
        ("03", "ENERGIYA ANALITIKASI", "Pik soatlar, bazaviy yuklama, kunlik/oylik o'rtacha qiymatlar va dinamika hisoblanadi.", PRIMARY_BLUE),
        ("04", "AI & ANOMALIYA QATLAMI", "Z-score va statistik modellar orqali shubhali sakrashlar aniqlanadi, xarajatlar bashoratlari tuziladi.", WARNING_AMBER),
        ("05", "AMALIY BIZNES QARORI", "O'zbek tilida tayyor tavsiyalar, Telegram tezkor ogohlantirishlari va PDF hisobotlar taqdim etiladi.", SUCCESS_GREEN)
    ]

    col5_w = Inches(2.18)
    gap5 = Inches(0.2)
    top5_y = Inches(2.0)
    h5_card = Inches(4.5)

    for idx, (num, title_st, desc_st, clr) in enumerate(stages):
        x = Inches(0.8) + idx * (col5_w + gap5)
        add_card(s5, x, top5_y, col5_w, h5_card)

        # Number circle / box
        c_num = s5.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, top5_y, col5_w, Inches(0.7))
        c_num.fill.solid()
        c_num.fill.fore_color.rgb = clr
        c_num.line.fill.background()

        tb_num = s5.shapes.add_textbox(x, top5_y + Inches(0.12), col5_w, Inches(0.5))
        tf_num = tb_num.text_frame
        p_num = tf_num.paragraphs[0]
        p_num.alignment = PP_ALIGN.CENTER
        p_num.text = f"BOSQICH  {num}"
        p_num.font.name = FONT_HEADING
        p_num.font.size = Pt(11)
        p_num.font.bold = True
        p_num.font.color.rgb = WHITE

        tb = s5.shapes.add_textbox(x + Inches(0.15), top5_y + Inches(0.85), col5_w - Inches(0.3), h5_card - Inches(1.0))
        tf = tb.text_frame
        tf.word_wrap = True

        pt = tf.paragraphs[0]
        pt.text = title_st
        pt.font.name = FONT_HEADING
        pt.font.size = Pt(12)
        pt.font.bold = True
        pt.font.color.rgb = DARK_NAVY

        pd = tf.add_paragraph()
        pd.text = desc_st
        pd.font.name = FONT_BODY
        pd.font.size = Pt(10)
        pd.font.color.rgb = DARK_TEXT
        pd.space_before = Pt(8)

        # Bottom benefit
        pb = tf.add_paragraph()
        pb.text = "Natija:"
        pb.font.name = FONT_HEADING
        pb.font.size = Pt(9.5)
        pb.font.bold = True
        pb.font.color.rgb = clr
        pb.space_before = Pt(14)

        benefits = [
            "Yagona raqamli markaz",
            "100% toza ma'lumotlar",
            "Shaffof soatlik matrisa",
            "Anomal isrofni tutish",
            "8-15% xarajat qisqarishi"
        ]
        pbn = tf.add_paragraph()
        pbn.text = benefits[idx]
        pbn.font.name = FONT_BODY
        pbn.font.size = Pt(9.5)
        pbn.font.color.rgb = DARK_NAVY
        pbn.space_before = Pt(2)

    set_speaker_notes(s5,
        "VAQT: 60 SONIYA\n\n"
        "Biz bu muammoni qanday hal qilamiz? NEXTGEN AI 5 bosqichli intellektual zanjir asosida ishlaydi.\n\n"
        "1-bosqich: Korxona o'z ma'lumotlarini yuklaydi. Buni Excel orqali yoki avtomatik hisoblagich protokollari orqali qilish mumkin.\n"
        "2-bosqich: Dastur ma'lumotlarni tozalaydi. Birliklar adashmaganmi, uzilishlar bormi — hammasi tekshiriladi.\n"
        "3-bosqich: Energiya analitikasi. Qaysi soatda eng yuqori pik bo'ldi, qaysi sex ko'p sarfladi — matematik hisoblanadi.\n"
        "4-bosqich: Sun'iy intellekt va statistik anomaliya qatlami. Biz Z-score va statistik chegara algoritmlari bilan kutilmagan sarflarni aniqlaymiz.\n"
        "5-bosqich: Eng muhimi — amaliy harakat. Tizim rahbar va bosh energetikka o'zbek tilida aniq xulosa va tavsiyani yetkazadi.\n\n"
        "Natijada, 'quruq' raqamlar aniq tejamkorlik rejasiga aylanadi."
    )

    # =========================================================================
    # SLIDE 06 — NEXTGEN QANDAY ISHLAYDI / USER JOURNEY (9 Steps)
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    apply_background(s6, LIGHT_BG)
    add_header(s6, "Amaliyot jarayoni", "NEXTGEN qanday ishlaydi: Korxona uchun 9 qadamli oqim", "Tizimga ulanishdan tortib har oylik iqtisodiy samarani olishgacha bo'lgan to'liq yo'l")
    add_footer(s6, 6)

    # 3x3 Grid of Steps
    grid_w = Inches(3.7)
    grid_h = Inches(1.4)
    gap_x = Inches(0.3)
    gap_y = Inches(0.2)

    steps = [
        ("1. Profil yaratish", "Korxona tizimda o'z tashkilot profilini ro'yxatdan o'tkazadi va foydalanuvchilarni qo'shadi."),
        ("2. Hisoblagichlarni kiritish", "Sexlar, uskunalar va transformator punktlari bo'yicha hisoblagichlar biriktiriladi."),
        ("3. Ma'lumotlarni yuklash", "Elektr sarfi ko'rsatkichlari CSV/Excel orqali yoki to'g'ridan-to'g'ri integratsiya orqali kiritiladi."),
        ("4. Avtomatik validatsiya", "Tizim ma'lumotlar butunligini, o'lchov birliklarini va xatoliklarni soniyalar ichida tekshiradi."),
        ("5. Sarf tahlili va metrikalar", "Kunduzgi, tungi va pik soatlar kesimida sarf, maksimal quvvat va yuklama hisoblanadi."),
        ("6. Anomaliyalarni aniqlash", "Algoritm me'yordan ortiq sarflarni va kechki paytdagi asossiz yo'qotishlarni aniqlaydi."),
        ("7. Kelajak xarajatini bashorat qilish", "Trendlar asosida keyingi oy uchun kutilayotgan elektr iste'moli va to'lovi hisoblab chiqiladi."),
        ("8. Grounded AI Tahlilnomasi", "Sun'iy intellekt korxona uchun energiya tejash bo'yicha aniq, faktik tavsiyalarni shakllantiradi."),
        ("9. Telegram va PDF hisobotlar", "Boshqaruv xulosasi va ogohlantirishlar darhol rahbarning Telegramiga va elektron pochtasiga yuboriladi.")
    ]

    for idx, (st_t, st_d) in enumerate(steps):
        row = idx // 3
        col = idx % 3
        x = Inches(0.8) + col * (grid_w + gap_x)
        y = Inches(1.85) + row * (grid_h + gap_y)

        add_card(s6, x, y, grid_w, grid_h)

        # Number tag
        tb_n = s6.shapes.add_textbox(x + Inches(0.15), y + Inches(0.12), grid_w - Inches(0.3), Inches(0.3))
        tf_n = tb_n.text_frame
        p_n = tf_n.paragraphs[0]
        p_n.text = st_t
        p_n.font.name = FONT_HEADING
        p_n.font.size = Pt(11)
        p_n.font.bold = True
        p_n.font.color.rgb = PRIMARY_BLUE

        tb_d = s6.shapes.add_textbox(x + Inches(0.15), y + Inches(0.45), grid_w - Inches(0.3), grid_h - Inches(0.5))
        tf_d = tb_d.text_frame
        tf_d.word_wrap = True
        p_d = tf_d.paragraphs[0]
        p_d.text = st_d
        p_d.font.name = FONT_BODY
        p_d.font.size = Pt(9.5)
        p_d.font.color.rgb = DARK_TEXT

    set_speaker_notes(s6,
        "VAQT: 60 SONIYA\n\n"
        "Korxona tizimdan qanday foydalanadi? Jarayon nihoyatda oson va 9 ta mantiqiy qadamdan iborat.\n\n"
        "Boshlanishida korxona o'z profilini ochadi va hisoblagichlarini belgilaydi. Hech qanday murakkab serverlar o'rnatish shart emas. Excel faylni yuklash kifoya.\n\n"
        "Tizim ma'lumotlarni tekshiradi, sarf grafigini chizadi va sun'iy intellekt orqali anomaliyalarni ajratib ko'rsatadi.\n\n"
        "Eng muhimi, direktor yoki bosh energetik har kuni kompyuter qarshisida o'tirishi shart emas: muhim ogohlantirishlar va oylik bashorat to'g'ridan-to'g'ri Telegram orqali yuboriladi."
    )

    # =========================================================================
    # SLIDE 07 — MAHSULOT PLATFORMASI / THE PRODUCT (Real Screenshot + Features)
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    apply_background(s7, LIGHT_BG)
    add_header(s7, "Ishlab turgan tizim", "Mahsulot platformasi: Veb boshqaruv interfeysi", "nextgen-ai-87ff.vercel.app manzilida faol ishlab turgan zamonaviy korporativ panel")
    add_footer(s7, 7)

    # Left: Real screenshot of the dashboard
    screenshot_path = "presentations/assets/dashboard_vercel.png"
    if os.path.exists(screenshot_path):
        s7.shapes.add_picture(screenshot_path, Inches(0.8), Inches(1.85), width=Inches(6.8))
        # Label below screenshot
        tb_sc = s7.shapes.add_textbox(Inches(0.8), Inches(6.45), Inches(6.8), Inches(0.3))
        tf_sc = tb_sc.text_frame
        p_sc = tf_sc.paragraphs[0]
        p_sc.text = "Haqiqiy ishchi interfeys (Next.js 14 + Recharts + Grounded AI)  •  nextgen-ai-87ff.vercel.app"
        p_sc.font.size = Pt(8.5)
        p_sc.font.color.rgb = SECONDARY_TEXT
    else:
        # Fallback card if screenshot missing
        card_sc = add_card(s7, Inches(0.8), Inches(1.85), Inches(6.8), Inches(4.5))

    # Right: 4 Feature Callouts
    r_x = Inches(7.85)
    r_w = Inches(4.683)
    feat_h = Inches(1.05)
    f_gap = Inches(0.12)

    features = [
        ("Interaktiv Boshqaruv Paneli (Dashboard)", "Umumiy energiya sarfi (kWh), eng yuqori yuklama (kW), hisoblangan xarajat va aktiv anomaliyalar soni real vaqtda ko'rsatiladi."),
        ("Ko'p O'lchovli Analitika va Grafiklar", "Kunlik, haftalik va oylik dinamika, soatlik iste'mol grafigi hamda pik vaqtlar taqsimoti interaktiv tarzda aks etadi."),
        ("Excel / CSV Import va Validatsiya", "Korxona o'z hisoblagich jurnallarini bir tugma bilan yuklaydi. Tizim xatoliklarni avtomatik tuzatadi va bazaga yozadi."),
        ("AI Maslahatchi va Grounded Tahlil", "Foydalanuvchi tizimga savol berishi mumkin: 'Nega o'tgan hafta sarf 15% oshdi?' AI faqat haqiqiy bazadagi raqamlarga asoslanib javob beradi.")
    ]

    for idx, (f_t, f_d) in enumerate(features):
        fy = Inches(1.85) + idx * (feat_h + f_gap)
        add_card(s7, r_x, fy, r_w, feat_h)
        
        c_b = s7.shapes.add_shape(MSO_SHAPE.RECTANGLE, r_x, fy, Inches(0.08), feat_h)
        c_b.fill.solid()
        c_b.fill.fore_color.rgb = PRIMARY_BLUE
        c_b.line.fill.background()

        tb_f = s7.shapes.add_textbox(r_x + Inches(0.2), fy + Inches(0.1), r_w - Inches(0.35), feat_h - Inches(0.2))
        tf_f = tb_f.text_frame
        tf_f.word_wrap = True

        pf1 = tf_f.paragraphs[0]
        pf1.text = f_t
        pf1.font.name = FONT_HEADING
        pf1.font.size = Pt(11)
        pf1.font.bold = True
        pf1.font.color.rgb = DARK_NAVY

        pf2 = tf_f.add_paragraph()
        pf2.text = f_d
        pf2.font.name = FONT_BODY
        pf2.font.size = Pt(9)
        pf2.font.color.rgb = DARK_TEXT
        pf2.space_before = Pt(3)

    set_speaker_notes(s7,
        "VAQT: 60 SONIYA\n\n"
        "Ekranda ko'rib turganingiz — bu shunchaki dizayn maketi emas. Bu Vercel platformasida real ishlab turgan NEXTGEN AI veb platformasining skrinshoti.\n\n"
        "Platformada boshqaruv paneli orqali rahbar umumiy sarfni, joriy xarajatni va xavfli anomaliyalarni bir zumda ko'radi.\n\n"
        "Analitika bo'limida har bir soatlik grafik tahlil qilinadi. Import bo'limi orqali istalgan Excel faylni yuklash mumkin.\n\n"
        "Va eng qizig'i — AI xonasi. Rahbar 'Nega 3-sexda elektr ko'p sarflandi?' deb so'rasa, sun'iy intellekt bazadagi raqamlarni tekshirib: 'Chunki shanba kuni kompressor o'chirilmay qolgan' deb aniq manzilni ko'rsatadi."
    )

    # =========================================================================
    # SLIDE 08 — TELEGRAM EKOTIZIMI / TELEGRAM ECOSYSTEM (@nextgenuzz_bot)
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    apply_background(s8, LIGHT_BG)
    add_header(s8, "Mobil qulaylik", "NEXTGEN Telegram ekotizimi: @nextgenuzz_bot", "O'zbekiston biznesi uchun qulay mobil boshqaruv va tezkor xabardorlik kanali")
    add_footer(s8, 8)

    # Left Card: Why Telegram in Uzbekistan?
    card_why = add_card(s8, Inches(0.8), Inches(1.85), Inches(5.6), Inches(4.7))
    tb_w = s8.shapes.add_textbox(Inches(1.05), Inches(2.05), Inches(5.1), Inches(4.3))
    tf_w = tb_w.text_frame
    tf_w.word_wrap = True

    pw1 = tf_w.paragraphs[0]
    pw1.text = "NEGA TELEGRAM INTEGRATSIYASI TANLANDI?"
    pw1.font.name = FONT_HEADING
    pw1.font.size = Pt(10)
    pw1.font.bold = True
    pw1.font.color.rgb = PRIMARY_BLUE

    pw2 = tf_w.add_paragraph()
    pw2.text = "O'zbekistonda biznes jarayonlari Telegram orqali yuritiladi"
    pw2.font.name = FONT_HEADING
    pw2.font.size = Pt(13)
    pw2.font.bold = True
    pw2.font.color.rgb = DARK_NAVY
    pw2.space_before = Pt(4)

    t_reasons = [
        ("Darhol yetib boruvchi Push-xabarlar", "Kritik anomaliya yuz berganda xabar 2 soniyada bosh muhandis va rahbarning cho'ntagiga boradi. Veb-saytga kirishni kutish shart emas."),
        ("O'rganish uchun nol vaqt talab etiladi", "Har bir korxona rahbari va xodimi Telegramdan foydalanishni biladi. Qo'shimcha qiyin dasturiy ta'lim shart emas."),
        ("Ovozli va matnli so'rovlar", "Rahbar oddiy audio xabar bilan: 'Bugun qancha sarfladik?' deb so'rashi va AI tahlildan tezkor ovozli/matnli javob olishi mumkin."),
        ("Mobil ilova (Android APK) tarqatish", "Bot orqali korxona xodimlari to'g'ridan-to'g'ri NEXTGEN Android ilovasini yuklab olishi mumkin (/apk komandasi).")
    ]
    for rh, rd in t_reasons:
        prh = tf_w.add_paragraph()
        prh.text = f"✔  {rh}"
        prh.font.name = FONT_HEADING
        prh.font.size = Pt(10)
        prh.font.bold = True
        prh.font.color.rgb = DARK_NAVY
        prh.space_before = Pt(8)

        prd = tf_w.add_paragraph()
        prd.text = f"   {rd}"
        prd.font.name = FONT_BODY
        prd.font.size = Pt(9.5)
        prd.font.color.rgb = SECONDARY_TEXT
        prd.space_before = Pt(2)

    # Right Column: Bot Features & Mock Cards
    bot_cards = [
        ("@nextgenuzz_bot funksiyalari", [
            "/start — Xavfsiz avtorizatsiya va profilni bog'lash",
            "/stats — Bugungi va oylik elektr sarfi qisqacha hisoboti",
            "/anomalies — Oxirgi 24 soatdagi shubhali sarflar ro'yxati",
            "/forecast — Keyingi oy uchun hisoblangan elektr to'lovi",
            "/apk — Android mobil ilovani yuklab olish",
            "AI Maslahatchi — Istalgan savolga tezkor javob"
        ], PRIMARY_BLUE),
        ("Haqiqiy ishlab turgan holat", [
            "Aiogram 3.x zamonaviy asinxron freymvorkida yaratilgan",
            "Veb-platforma ma'lumotlar bazasi bilan to'liq sinxron",
            "Multi-tenant xavfsizlik: har bir xodim faqat o'z zavodini ko'radi",
            "O'zbek tilida to'liq interaktiv tugmalar (Inline keyboard)"
        ], SUCCESS_GREEN)
    ]

    for idx, (b_title, b_items, b_clr) in enumerate(bot_cards):
        by = Inches(1.85) + idx * Inches(2.4)
        add_card(s8, Inches(6.8), by, Inches(5.733), Inches(2.25))

        b_bar = s8.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.8), by, Inches(5.733), Inches(0.08))
        b_bar.fill.solid()
        b_bar.fill.fore_color.rgb = b_clr
        b_bar.line.fill.background()

        tb_bc = s8.shapes.add_textbox(Inches(7.0), by + Inches(0.18), Inches(5.3), Inches(1.95))
        tf_bc = tb_bc.text_frame
        tf_bc.word_wrap = True

        pbc1 = tf_bc.paragraphs[0]
        pbc1.text = b_title
        pbc1.font.name = FONT_HEADING
        pbc1.font.size = Pt(12)
        pbc1.font.bold = True
        pbc1.font.color.rgb = DARK_NAVY

        for item in b_items:
            pbi = tf_bc.add_paragraph()
            pbi.text = f"•  {item}"
            pbi.font.name = FONT_BODY
            pbi.font.size = Pt(9.5)
            pbi.font.color.rgb = DARK_TEXT
            pbi.space_before = Pt(3)

    set_speaker_notes(s8,
        "VAQT: 50 SONIYA\n\n"
        "O'zbekiston bozorining o'ziga xos haqiqati bor: agar siz korxonaga qanchalik zo'r veb-sayt bersangiz ham, xodimlar unga har kuni kirib o'tirmaydi. Lekin har bir muhandis va rahbar har 10 daqiqada Telegramni tekshiradi.\n\n"
        "Shuning uchun biz @nextgenuzz_bot ekotizimini yaratdik. Bu shunchaki xabarnoma emas, bu cho'ntakdagi energetika dispecheridir.\n\n"
        "Tunda zavodda qisqa tutashuv yoki uskunaning ochiq qolishi tufayli elektr sarfi sakrab ketsa — bot 2 soniyada ogohlantiradi. Shuningdek, /apk komandasi orqali korxona uchun tayyorlangan maxsus Android ilovani ham yuklash mumkin."
    )

    # =========================================================================
    # SLIDE 09 — SUN'IY INTELLEKT VA TEXNOLOGIK ARXITEKTURA / AI & TECH STACK
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    apply_background(s9, LIGHT_BG)
    add_header(s9, "Texnologik poydevor", "Sun'iy intellekt va arxitektura: Deterministik hisob + LLM", "Sun'iy intellekt gallyutsinatsiyasini nolga tushiruvchi ikki qatlamli gibrid arxitektura")
    add_footer(s9, 9)

    # Left: Two Layer Hybrid Architecture
    card_arch = add_card(s9, Inches(0.8), Inches(1.85), Inches(5.7), Inches(4.7))
    tb_a = s9.shapes.add_textbox(Inches(1.05), Inches(2.05), Inches(5.2), Inches(4.3))
    tf_a = tb_a.text_frame
    tf_a.word_wrap = True

    pa1 = tf_a.paragraphs[0]
    pa1.text = "GALLYUTSINATSIYASIZ SUN'IY INTELLEKT"
    pa1.font.name = FONT_HEADING
    pa1.font.size = Pt(10)
    pa1.font.bold = True
    pa1.font.color.rgb = PRIMARY_BLUE

    pa2 = tf_a.add_paragraph()
    pa2.text = "Ikki Qatlamli Ishonchli Model (Two-Layer Grounding)"
    pa2.font.name = FONT_HEADING
    pa2.font.size = Pt(13)
    pa2.font.bold = True
    pa2.font.color.rgb = DARK_NAVY
    pa2.space_before = Pt(4)

    layers = [
        ("1-Qatlam: Deterministik Matematika (SQL & Python)", 
         "Barcha raqamlar, jami kWh sarfi, pik vaqtlar, tarif hisoblari va Z-score anomaliya chegaralari qat'iy matematik formulalar bilan hisoblanadi. LLM bu hisoblarga aralashmaydi."),
        ("2-Qatlam: Grounded Generativ AI (Interpretatsiya)", 
         "Hisoblangan qat'iy natijalar tizimli kontekst (prompt) sifatida LLMga beriladi. AI faqat ushbu raqamlarni o'zbek tilida sharhlaydi va biznes tavsiyalari beradi."),
        ("Qat'iy xavfsizlik cheklovi (Guardrail)", 
         "Agar ma'lumotlar yetarli bo'lmasa, AI taxmin qilmaydi, balki to'g'ridan-to'g'ri 'Ma'lumot yetarli emas' deb javob beradi. Bu korporativ xavfsizlikni ta'minlaydi.")
    ]
    for lh, ld in layers:
        plh = tf_a.add_paragraph()
        plh.text = f"✔  {lh}"
        plh.font.name = FONT_HEADING
        plh.font.size = Pt(10)
        plh.font.bold = True
        plh.font.color.rgb = DARK_NAVY
        plh.space_before = Pt(8)

        pld = tf_a.add_paragraph()
        pld.text = f"   {ld}"
        pld.font.name = FONT_BODY
        pld.font.size = Pt(9.5)
        pld.font.color.rgb = SECONDARY_TEXT
        pld.space_before = Pt(2)

    # Right: Production Tech Stack Cards
    tech_cards = [
        ("Frontend: Next.js 14 & Tailwind CSS", "Server-Side Rendering (SSR), tezkor yuklanish, zamonaviy Recharts grafik kutubxonasi, to'liq moslashuvchan dizayn.", PRIMARY_BLUE),
        ("Backend: FastAPI & Python 3.11+", "Yuqori tezlikdagi asinxron REST API, qat'iy ma'lumotlar sxemasi (Pydantic), avtomatik OpenAPI/Swagger hujjatlari.", DEEP_BLUE),
        ("Ma'lumotlar bazasi: PostgreSQL / SQLite", "ACID tranzaksiyalari, ko'p ijarachilik (Multi-tenancy), korxona ma'lumotlarini qat'iy ajratish va indeksatsiya.", SUCCESS_GREEN),
        ("Bot & Mobil: Aiogram 3 & Android Native", "Asinxron Telegram boti, Webhook arxitekturasi, APK paket orqali to'g'ridan-to'g'ri mobil boshqaruv.", WARNING_AMBER)
    ]

    for idx, (t_name, t_desc, t_clr) in enumerate(tech_cards):
        ty = Inches(1.85) + idx * Inches(1.15)
        add_card(s9, Inches(6.8), ty, Inches(5.733), Inches(1.05))

        t_bar = s9.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.8), ty, Inches(0.08), Inches(1.05))
        t_bar.fill.solid()
        t_bar.fill.fore_color.rgb = t_clr
        t_bar.line.fill.background()

        tb_tc = s9.shapes.add_textbox(Inches(7.0), ty + Inches(0.1), Inches(5.35), Inches(0.85))
        tf_tc = tb_tc.text_frame
        tf_tc.word_wrap = True

        pt1 = tf_tc.paragraphs[0]
        pt1.text = t_name
        pt1.font.name = FONT_HEADING
        pt1.font.size = Pt(11)
        pt1.font.bold = True
        pt1.font.color.rgb = DARK_NAVY

        pt2 = tf_tc.add_paragraph()
        pt2.text = t_desc
        pt2.font.name = FONT_BODY
        pt2.font.size = Pt(9)
        pt2.font.color.rgb = DARK_TEXT
        pt2.space_before = Pt(2)

    set_speaker_notes(s9,
        "VAQT: 60 SONIYA\n\n"
        "Ko'pchilik investor va texnik mutaxassislar haqli savol berishadi: 'Sun'iy intellekt sanoatda xato qilsa-chi? Gallyutsinatsiya bo'lsa nima bo'ladi?'\n\n"
        "Biz bu muammoni arxitektura darajasida hal qildik. NEXTGEN AI — bu sof generativ model emas, bu gibrid tizimdir.\n\n"
        "Biz hisob-kitoblarni sun'iy intellektga topshirmaymiz. Barcha formulalar, kilovattlar, tariflar va Z-score anomaliya chegaralari 100% deterministik SQL va Python algoritmlari orqali hisoblanadi.\n\n"
        "Sun'iy intellekt faqatgina tayyor hisoblangan faktlarni o'zbek tilida professional izohlab berish uchun xizmat qiladi. Natijada xatolik ehtimoli 0 ga tushadi."
    )

    # =========================================================================
    # SLIDE 10 — XAVFSIZLIK VA KORPORATIV ISHONCHLILIK / ENTERPRISE SECURITY
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    apply_background(s10, LIGHT_BG)
    add_header(s10, "Kiberxavfsizlik", "Xavfsizlik va korporativ ishonchlilik", "Sanoat korxonalarining tijoriy sirlari va ma'lumotlarini kafolatli himoyalash")
    add_footer(s10, 10)

    # 4 Security Pillars
    col10_w = Inches(2.78)
    gap10 = Inches(0.2)
    top10_y = Inches(1.85)
    h10_card = Inches(4.7)

    sec_pillars = [
        ("Multi-Tenant Izolyatsiya", "Tashkilotlararo to'liq ajratish", 
         "Har bir korxona ma'lumotlari alohida virtual konteynerda saqlanadi. Hech bir mijoz boshqa korxonaning sarf ma'lumotlarini yoki tahlillarini ko'ra olmaydi.",
         ["Tashkilot ID bo'yicha qat'iy filtr", "Bazada ma'lumotlar aralashmaydi", "To'liq konfidensiallik"],
         PRIMARY_BLUE),
        
        ("Rolga Asoslangan Ruxsat (RBAC)", "Vazifalar bo'yicha kirish huquqi",
         "Tizim foydalanuvchilari 3 toifaga bo'linadi: Administrator (to'liq nazorat), Bosh energetik (tahlil va konfiguratsiya), Kuzatuvchi (faqat ko'rish).",
         ["Boshqaruv rollari matritsasi", "Parollarni argon2 bilan shifrlash", "Ruxsatsiz o'zgarishlar bloklanadi"],
         DEEP_BLUE),

        ("Audit Loglari va Nazorat", "Har bir harakat qayd etiladi",
         "Fayl qachon yuklandi, kim eksport qildi, qaysi ko'rsatkich o'zgardi — barcha amallar xronologik jurnalda saqlanadi va tahrirlanmaydi.",
         ["Vaqt belgisi bilan harakatlar jurnali", "Audit tekshiruvlariga tayyorlik", "Ichki xavfsizlik kafolati"],
         WARNING_AMBER),

        ("Lokal Server (On-Premise)", "Mustaqil ichki infratuzilma",
         "Strategik va yopiq korxonalar uchun tizimni internetga ulamasdan, to'g'ridan-to'g'ri korxonaning o'z serverlariga (On-premise) o'rnatish imkoniyati mavjud.",
         ["Davlat korxonalari talablariga mos", "Tashqi tarmoqqa bog'liqlik yo'q", "O'zbekiston qonunlariga muvofiqlik"],
         SUCCESS_GREEN)
    ]

    for idx, (s_t, s_sub, s_desc, s_points, s_clr) in enumerate(sec_pillars):
        x = Inches(0.8) + idx * (col10_w + gap10)
        add_card(s10, x, top10_y, col10_w, h10_card)

        s_bar = s10.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, top10_y, col10_w, Inches(0.08))
        s_bar.fill.solid()
        s_bar.fill.fore_color.rgb = s_clr
        s_bar.line.fill.background()

        tb = s10.shapes.add_textbox(x + Inches(0.2), top10_y + Inches(0.2), col10_w - Inches(0.4), h10_card - Inches(0.4))
        tf = tb.text_frame
        tf.word_wrap = True

        ps_t = tf.paragraphs[0]
        ps_t.text = s_t
        ps_t.font.name = FONT_HEADING
        ps_t.font.size = Pt(13)
        ps_t.font.bold = True
        ps_t.font.color.rgb = DARK_NAVY

        ps_sub = tf.add_paragraph()
        ps_sub.text = s_sub
        ps_sub.font.name = FONT_HEADING
        ps_sub.font.size = Pt(9.5)
        ps_sub.font.bold = True
        ps_sub.font.color.rgb = s_clr
        ps_sub.space_before = Pt(2)

        ps_d = tf.add_paragraph()
        ps_d.text = s_desc
        ps_d.font.name = FONT_BODY
        ps_d.font.size = Pt(9.5)
        ps_d.font.color.rgb = DARK_TEXT
        ps_d.space_before = Pt(8)

        ps_f = tf.add_paragraph()
        ps_f.text = "Himoya mexanizmlari:"
        ps_f.font.name = FONT_HEADING
        ps_f.font.size = Pt(9.5)
        ps_f.font.bold = True
        ps_f.font.color.rgb = DARK_NAVY
        ps_f.space_before = Pt(10)

        for p in s_points:
            pp = tf.add_paragraph()
            pp.text = f"✔  {p}"
            pp.font.name = FONT_BODY
            pp.font.size = Pt(9)
            pp.font.color.rgb = SECONDARY_TEXT
            pp.space_before = Pt(2)

    set_speaker_notes(s10,
        "VAQT: 50 SONIYA\n\n"
        "Ishlab chiqarish korxonalari uchun ularning energiya sarfi — bu tijorat siridir. Chunki elektr sarfiga qarab korxonaning qancha mahsulot ishlab chiqarayotganini bilib olish mumkin.\n\n"
        "Shuning uchun biz xavfsizlikni eng oliy darajaga qo'yganmiz.\n\n"
        "Birinchidan, har bir tashkilot to'liq izolyatsiyalangan. Ikkinchidan, rollarga bo'lingan kirish tizimi mavjud.\n\n"
        "Uchinchidan — yirik davlat yoki strategik korxonalar uchun biz tizimni to'g'ridan-to'g'ri korxonaning o'z ichki serverlariga (On-premise) o'rnatib bera olamiz. Hech qanday ma'lumot tashqi internetga chiqmaydi."
    )

    # =========================================================================
    # SLIDE 11 — BOZOR HAJMI VA MAQSADLI MIJOZLAR / MARKET OPPORTUNITY
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    apply_background(s11, LIGHT_BG)
    add_header(s11, "Bozor tahlili", "Bozor hajmi va maqsadli mijozlar", "O'zbekistonda energiya boshqaruviga eng yuqori ehtiyoji bo'lgan sanoat segmentlari")
    add_footer(s11, 11)

    # Left: TAM / SAM / SOM Framework
    card_mkt = add_card(s11, Inches(0.8), Inches(1.85), Inches(5.7), Inches(4.7))
    tb_m = s11.shapes.add_textbox(Inches(1.05), Inches(2.05), Inches(5.2), Inches(4.3))
    tf_m = tb_m.text_frame
    tf_m.word_wrap = True

    pm_t = tf_m.paragraphs[0]
    pm_t.text = "BOZOR HAJMI BAHOLANISHI (TAM / SAM / SOM)"
    pm_t.font.name = FONT_HEADING
    pm_t.font.size = Pt(10)
    pm_t.font.bold = True
    pm_t.font.color.rgb = PRIMARY_BLUE

    pm_sub = tf_m.add_paragraph()
    pm_sub.text = "O'zbekiston sanoat va tijorat sektori"
    pm_sub.font.name = FONT_HEADING
    pm_sub.font.size = Pt(13)
    pm_sub.font.bold = True
    pm_sub.font.color.rgb = DARK_NAVY
    pm_sub.space_before = Pt(4)

    mkt_levels = [
        ("TAM (Umumiy bozor): 50,000+ korxona", 
         "O'zbekistondagi barcha ro'yxatdan o'tgan sanoat, qayta ishlash va ishlab chiqarish korxonalari. Yillik potentsial bozor: $60M+."),
        ("SAM (Erishish mumkin bo'lgan bozor): 8,000+ korxona", 
         "Oylik elektr energiyasi to'lovi 20 million so'mdan ortiq bo'lgan, raqamlashtirishga tayyor to'qimachilik, oziq-ovqat va metallurgiya korxonalari. Yillik hajm: ~$12M."),
        ("SOM (Dastlabki 2 yillik maqsad): 250 korxona", 
         "Toshkent, Farg'ona vodiysi va Samarqanddagi faol ishlab chiqarish korxonalari. Yillik rejalashtirilgan SaaS tushumi: $450,000+.")
    ]
    for mh, md in mkt_levels:
        pmh = tf_m.add_paragraph()
        pmh.text = f"★  {mh}"
        pmh.font.name = FONT_HEADING
        pmh.font.size = Pt(10)
        pmh.font.bold = True
        pmh.font.color.rgb = DARK_NAVY
        pmh.space_before = Pt(8)

        pmd = tf_m.add_paragraph()
        pmd.text = f"   {md}"
        pmd.font.name = FONT_BODY
        pmd.font.size = Pt(9.5)
        pmd.font.color.rgb = SECONDARY_TEXT
        pmd.space_before = Pt(2)

    # Right: 4 Target Industry Verticals
    verticals = [
        ("To'qimachilik va tikuvchilik fabrikalari", "Uzluksiz 24/7 ish tartibi, yuzlab dastgohlar, kompressorlar. Elektr xarajatlari tannarxning 20% gacha qismini tashkil etadi.", PRIMARY_BLUE),
        ("Oziq-ovqat va qayta ishlash korxonalari", "Katta sovutish kameralari, qadoqlash liniyalari, pishirish sexlari. Tungi va kunduzgi rejimda sarf turlicha bo'ladi.", SUCCESS_GREEN),
        ("Qurilish materiallari va metallurgiya", "Kuchli elektr pechlari, prokat stanoklari, transformatorlar. Pik soatlarda jarimalarga tushish xavfi juda yuqori.", WARNING_AMBER),
        ("Yirik logistika va savdo majmualari", "Minglab kvadrat metrli sovutgichli omborlar, yoritish tizimlari va havoni shamollatish agregatlari.", DEEP_BLUE)
    ]

    for idx, (v_t, v_d, v_clr) in enumerate(verticals):
        vy = Inches(1.85) + idx * Inches(1.15)
        add_card(s11, Inches(6.8), vy, Inches(5.733), Inches(1.05))

        v_bar = s11.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.8), vy, Inches(0.08), Inches(1.05))
        v_bar.fill.solid()
        v_bar.fill.fore_color.rgb = v_clr
        v_bar.line.fill.background()

        tb_vc = s11.shapes.add_textbox(Inches(7.0), vy + Inches(0.1), Inches(5.35), Inches(0.85))
        tf_vc = tb_vc.text_frame
        tf_vc.word_wrap = True

        pvt1 = tf_vc.paragraphs[0]
        pvt1.text = v_t
        pvt1.font.name = FONT_HEADING
        pvt1.font.size = Pt(11)
        pvt1.font.bold = True
        pvt1.font.color.rgb = DARK_NAVY

        pvt2 = tf_vc.add_paragraph()
        pvt2.text = v_d
        pvt2.font.name = FONT_BODY
        pvt2.font.size = Pt(9)
        pvt2.font.color.rgb = DARK_TEXT
        pvt2.space_before = Pt(2)

    set_speaker_notes(s11,
        "VAQT: 60 SONIYA\n\n"
        "Bizning bozorimiz kimlar? O'zbekistonda 50 mingdan ortiq ishlab chiqarish korxonasi bor.\n\n"
        "Bizning birinchi navbatdagi nishonimiz — oyiga 20 million so'mdan ortiq elektr to'laydigan to'qimachilik fabrikalari, oziq-ovqat sexlari, qurilish materiallari zavodlari va yirik omborxonalar.\n\n"
        "Masalan, to'qimachilik fabrikasida elektr xarajati mahsulot tannarxining 20 foizigacha yetadi. Ular uchun har bir 5-10% tejamkorlik — bu yillik yuzlab million so'm toza foyda degani.\n\n"
        "Bizning 2 yillik maqsadimiz — O'zbekiston bo'ylab 250 ta faol korxonani platformaga ulashdir."
    )

    # =========================================================================
    # SLIDE 12 — RAQOBAT TAHLILI VA USTUNLIKLAR / COMPETITIVE ADVANTAGE
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    apply_background(s12, LIGHT_BG)
    add_header(s12, "Raqobat tahlili", "Raqobat tahlili: NEXTGEN AI ustunliklari", "Mavjud yechimlar va xorijiy analoglar bilan xolis taqqoslash")
    add_footer(s12, 12)

    # Comparison Matrix Card
    card_cmp = add_card(s12, Inches(0.8), Inches(1.85), Inches(11.733), Inches(4.7))
    tb_cmp = s12.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(11.333), Inches(4.3))
    tf_cmp = tb_cmp.text_frame
    tf_cmp.word_wrap = True

    pc_t = tf_cmp.paragraphs[0]
    pc_t.text = "BOZORDAGI YECHIMLAR TAQQOSLASH MATRITSASI"
    pc_t.font.name = FONT_HEADING
    pc_t.font.size = Pt(11)
    pc_t.font.bold = True
    pc_t.font.color.rgb = PRIMARY_BLUE

    # Table layout inside card
    # Columns: Mezon | An'anaviy ASKUE | Xorijiy tizimlar (Siemens/Schneider) | Oddiy Excel | NEXTGEN AI
    headers = ["Taqqoslash mezoni", "An'anaviy ASKUE", "Xorijiy tizimlar", "Qo'lda Excel yuritish", "NEXTGEN AI"]
    rows = [
        ("O'zbek tili va mahalliy tariflar", "❌  Yo'q (faqat rus/ingliz)", "❌  Yo'q (xorijiy standartlar)", "⚠️  Qisman formulalar", "✔  To'liq o'zbek tilida va mahalliy tariflar"),
        ("Sun'iy intellekt tavsiyalari", "❌  Yo'q (faqat raqam yig'adi)", "⚠️  Qisman (juda qimmat modul)", "❌  Yo'q", "✔  Grounded AI (aniq faktik tavsiyalar)"),
        ("Anomaliyalarni erta aniqlash", "❌  Yo'q", "✔  Mavjud", "❌  Kech aniqlanadi", "✔  Statistik Z-Score va tezkor xabarlar"),
        ("Telegram orqali boshqaruv", "❌  Yo'q", "❌  Yo'q", "❌  Yo'q", "✔  @nextgenuzz_bot orqali 24/7 nazorat"),
        ("Joriy etish tezligi va narxi", "Oylar talab qiladi, qimmat", "$20,000+ va uzoq integratsiya", "Arzon, ammo samarasiz", "1 kunda ishga tushadi, qulay oylik SaaS"),
        ("Hisobotlarni avtomatlashtirish", "Faqat jadval ko'rinishida", "Murakkab korporativ hisobotlar", "Qo'lda soatlab vaqt oladi", "1 tugma bilan PDF va Telegram hisobot")
    ]

    # Render as formatted text rows
    p_th = tf_cmp.add_paragraph()
    p_th.text = f"{'Mezon':<32} | {'Ananaviy ASKUE':<18} | {'Xorijiy dasturlar':<20} | {'Excel':<16} | {'NEXTGEN AI':<22}"
    p_th.font.name = "Consolas"
    p_th.font.size = Pt(9.5)
    p_th.font.bold = True
    p_th.font.color.rgb = DARK_NAVY
    p_th.space_before = Pt(8)

    p_div = tf_cmp.add_paragraph()
    p_div.text = "-" * 115
    p_div.font.name = "Consolas"
    p_div.font.size = Pt(8.5)
    p_div.font.color.rgb = BORDER_COLOR
    p_div.space_before = Pt(2)

    for r in rows:
        pr = tf_cmp.add_paragraph()
        pr.text = f"{r[0]:<32} | {r[1]:<18} | {r[2]:<20} | {r[3]:<16} | {r[4]:<22}"
        pr.font.name = "Consolas"
        pr.font.size = Pt(9)
        pr.font.color.rgb = DARK_TEXT
        pr.space_before = Pt(5)

    set_speaker_notes(s12,
        "VAQT: 60 SONIYA\n\n"
        "Bozorda raqobatchilar bormi? Albatta bor. Keling, ochiq taqqoslaylik.\n\n"
        "Birinchisi — ASKUE tizimlari. Ular O'zbekistonda bor, lekin ularning vazifasi tejamkorlik emas, elektr ta'minoti korxonasiga schyot yozishdir. U yerda tahlil ham, tavsiya ham yo'q.\n\n"
        "Ikkinchisi — Siemens yoki Schneider Electric kabi xorijiy korporativ dasturlar. Ular juda mukammal, lekin narxi o'n minglab dollar turadi, o'zbek tilida yo'q va bizning mahalliy tabaqalashtirilgan tariflarimizga moslashmagan.\n\n"
        "Uchinchisi — korxonalar hozir qilayotganidek, Excelda qo'lda yozish. Bu inson omili, kechikish va xatolarga to'la.\n\n"
        "NEXTGEN AI — mahalliy tariflarni tushunadigan, to'liq o'zbek tilida so'zlashadigan, Telegramga ulangan va 1 kunda ishga tushadigan qulay milliy yechimdir."
    )

    # =========================================================================
    # SLIDE 13 — BIZNES MODEL VA MONETIZATSIYA / BUSINESS MODEL
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    apply_background(s13, LIGHT_BG)
    add_header(s13, "Iqtisodiy model", "Biznes model va monetizatsiya", "B2B SaaS obuna va korxona hajmiga mos moslashuvchan tariflar")
    add_footer(s13, 13)

    col13_w = Inches(3.7)
    gap13 = Inches(0.3)
    top13_y = Inches(1.85)
    h13_card = Inches(4.7)

    plans = [
        ("Starter", "Kichik ishlab chiqarish", "500,000 so'm / oy", 
         "1–3 ta hisoblagichga ega kichik sexlar, novvoyxonalar va ustaxonalar uchun.",
         [
             "3 tagacha hisoblagich monitoringi",
             "Kunlik sarf va bazaviy grafiklar",
             "Excel / CSV yuklash imkoniyati",
             "Telegram bot orqali haftalik xabarlar",
             "Standart texnik qo'llab-quvvatlash"
         ], PRIMARY_BLUE, False),
        
        ("Pro (Tavsiya etiladi)", "O'rta sanoat korxonalari", "1,500,000 so'm / oy", 
         "To'qimachilik, oziq-ovqat va yig'uv fabrikalari uchun to'liq tahliliy paket.",
         [
             "15 tagacha hisoblagich monitoringi",
             "To'liq Grounded AI tahlilchi va tavsiyalar",
             "Z-Score anomaliyalarni 24/7 aniqlash",
             "Real vaqtda Telegram tezkor ogohlantirishlari",
             "Xarajatlarni keyingi oyga bashorat qilish",
             "Avtomatik oylik PDF boshqaruv hisoboti"
         ], SUCCESS_GREEN, True),

        ("Enterprise", "Yirik zavodlar va xoldinglar", "Shartnoma asosida", 
         "Yirik sanoat korxonalari, metallurgiya va ko'p filialli ishlab chiqarish majmualari.",
         [
             "Cheksiz miqdordagi hisoblagichlar",
             "Korxonaning o'z serveriga (On-premise) o'rnatish",
             "To'g'ridan-to'g'ri ASKUE va ERP API integratsiyasi",
             "Shaxsiy AI modeli va maxsus hisobotlar",
             "Alohida muhandis va 24/7 SLA xizmati"
         ], DEEP_BLUE, False)
    ]

    for idx, (p_name, p_target, p_price, p_desc, p_features, p_clr, is_rec) in enumerate(plans):
        x = Inches(0.8) + idx * (col13_w + gap13)
        add_card(s13, x, top13_y, col13_w, h13_card, bg_color=CARD_BG, border_color=PRIMARY_BLUE if is_rec else BORDER_COLOR)

        p_bar = s13.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, top13_y, col13_w, Inches(0.08))
        p_bar.fill.solid()
        p_bar.fill.fore_color.rgb = p_clr
        p_bar.line.fill.background()

        tb = s13.shapes.add_textbox(x + Inches(0.2), top13_y + Inches(0.2), col13_w - Inches(0.4), h13_card - Inches(0.4))
        tf = tb.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = p_name.upper()
        p1.font.name = FONT_HEADING
        p1.font.size = Pt(13)
        p1.font.bold = True
        p1.font.color.rgb = p_clr

        p2 = tf.add_paragraph()
        p2.text = p_price
        p2.font.name = FONT_HEADING
        p2.font.size = Pt(16)
        p2.font.bold = True
        p2.font.color.rgb = DARK_NAVY
        p2.space_before = Pt(2)

        p3 = tf.add_paragraph()
        p3.text = p_target
        p3.font.name = FONT_BODY
        p3.font.size = Pt(9.5)
        p3.font.color.rgb = SECONDARY_TEXT
        p3.space_before = Pt(2)

        p4 = tf.add_paragraph()
        p4.text = p_desc
        p4.font.name = FONT_BODY
        p4.font.size = Pt(9.5)
        p4.font.color.rgb = DARK_TEXT
        p4.space_before = Pt(6)

        p5 = tf.add_paragraph()
        p5.text = "Tarif imkoniyatlari:"
        p5.font.name = FONT_HEADING
        p5.font.size = Pt(10)
        p5.font.bold = True
        p5.font.color.rgb = DARK_NAVY
        p5.space_before = Pt(8)

        for feat in p_features:
            pf = tf.add_paragraph()
            pf.text = f"✔  {feat}"
            pf.font.name = FONT_BODY
            pf.font.size = Pt(9)
            pf.font.color.rgb = DARK_TEXT
            pf.space_before = Pt(2)

    set_speaker_notes(s13,
        "VAQT: 50 SONIYA\n\n"
        "Biz qanday daromad qilamiz? Bizning biznes modelimiz — klassik B2B SaaS (obuna) modelidir.\n\n"
        "Kichik sexlar uchun Starter tarifi oyiga 500 ming so'm. Bu korxona uchun bir kungi elektr xarajatidan ham kam.\n\n"
        "O'rta korxonalar uchun Pro tarifi — 1.5 million so'm. Bu yerda to'liq AI tahlil va Telegram ogohlantirishlar mavjud. Agar zavod oyiga 50 million so'm elektr to'lasa va tizim yordamida atigi 5% (2.5 million so'm) tejasa ham, dastur birinchi oydayoq o'z xarajatini 150% ga oqlaydi.\n\n"
        "Yirik sanoat korxonalari uchun esa Enterprise tarifi mavjud bo'lib, ular uchun shaxsiy server va maxsus integratsiyalar taqdim etiladi."
    )

    # =========================================================================
    # SLIDE 14 — RIVOJLANISH XARITASI (ROADMAP) / STRATEGIC ROADMAP
    # =========================================================================
    s14 = prs.slides.add_slide(blank_layout)
    apply_background(s14, LIGHT_BG)
    add_header(s14, "Strategik reja", "Rivojlanish xaritasi: 2026–2027 yillar", "MVP bosqichidan milliy va xalqaro miqyosdagi yetakchi platformaga aylanish bosqichlari")
    add_footer(s14, 14)

    phases = [
        ("1-BOSQICH (Bajarildi)", "MVP va Demo Platforma", "2026-yil Q1", [
            "Vercel veb platformasi ishga tushirildi",
            "FastAPI backend va ma'lumotlar bazasi tayyor",
            "@nextgenuzz_bot Telegram boti ulandi",
            "Android APK mobil ilovasi tayyorlandi",
            "Deterministik AI tavsiyalar tekshirildi"
        ], SUCCESS_GREEN),
        
        ("2-BOSQICH (Joriy)", "5 ta Korxonada Pilot Dasturi", "2026-yil Q2", [
            "To'qimachilik va oziq-ovqat sexlarida bepul pilot",
            "Real hisoblagich ma'lumotlari asosida test",
            "Tejamkorlik metrikalarini amalda isbotlash",
            "Energetik mutaxassislar fikrlari asosida takomillashtirish"
        ], PRIMARY_BLUE),

        ("3-BOSQICH (Tijoriy)", "O'zbekistonda Masshtablash", "2026-yil Q3–Q4", [
            "50+ to'lovchi korxonani platformaga ulash",
            "ASKUE va HET tizimlari bilan rasmiy API integratsiya",
            "Mobil ilovani Google Play Store'ga chiqarish",
            "Energiya auditi kompaniyalari bilan hamkorlik"
        ], DEEP_BLUE),

        ("4-BOSQICH (Xalqaro)", "Markaziy Osiyo Bozoriga Chiqish", "2027-yil", [
            "Qozog'iston va Qirg'iziston bozorlariga kengayish",
            "Ko'p tilli qo'llab-quvvatlash (qozoq, qirg'iz, rus, ingliz)",
            "Kompaniyalar uchun ESG uglerod izi sertifikatlari",
            "A seriya investitsiyalarini jalb qilish"
        ], WARNING_AMBER)
    ]

    col14_w = Inches(2.78)
    gap14 = Inches(0.2)
    top14_y = Inches(1.85)
    h14_card = Inches(4.7)

    for idx, (p_num, p_title, p_time, p_tasks, p_clr) in enumerate(phases):
        x = Inches(0.8) + idx * (col14_w + gap14)
        add_card(s14, x, top14_y, col14_w, h14_card)

        bar = s14.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, top14_y, col14_w, Inches(0.08))
        bar.fill.solid()
        bar.fill.fore_color.rgb = p_clr
        bar.line.fill.background()

        tb = s14.shapes.add_textbox(x + Inches(0.2), top14_y + Inches(0.2), col14_w - Inches(0.4), h14_card - Inches(0.4))
        tf = tb.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = p_num
        p1.font.name = FONT_HEADING
        p1.font.size = Pt(10)
        p1.font.bold = True
        p1.font.color.rgb = p_clr

        p2 = tf.add_paragraph()
        p2.text = p_title
        p2.font.name = FONT_HEADING
        p2.font.size = Pt(13)
        p2.font.bold = True
        p2.font.color.rgb = DARK_NAVY
        p2.space_before = Pt(3)

        p3 = tf.add_paragraph()
        p3.text = p_time
        p3.font.name = FONT_BODY
        p3.font.size = Pt(9.5)
        p3.font.color.rgb = SECONDARY_TEXT
        p3.space_before = Pt(2)

        p4 = tf.add_paragraph()
        p4.text = "Asosiy vazifalar:"
        p4.font.name = FONT_HEADING
        p4.font.size = Pt(10)
        p4.font.bold = True
        p4.font.color.rgb = DARK_NAVY
        p4.space_before = Pt(8)

        for task in p_tasks:
            pt = tf.add_paragraph()
            pt.text = f"•  {task}"
            pt.font.name = FONT_BODY
            pt.font.size = Pt(9)
            pt.font.color.rgb = DARK_TEXT
            pt.space_before = Pt(2)

    set_speaker_notes(s14,
        "VAQT: 50 SONIYA\n\n"
        "Biz bugun qayerdamiz va qayerga bormoqchimiz?\n\n"
        "1-bosqich to'liq yakunlandi: Bizda ishlayotgan veb-platforma, backend, Telegram bot va Android APK ilovasi tayyor.\n\n"
        "Bugungi kunda biz 2-bosqichdamiz: 5 ta sanoat korxonasida 30 kunlik bepul pilot dasturini boshlamoqdamiz. Maqsad — tizimning tejamkorlik natijalarini real ishlab chiqarishda isbotlash.\n\n"
        "Yil oxirigacha biz O'zbekistonda 50 ta to'lovchi korxonaga yetamiz. 2027-yilda esa Markaziy Osiyo bozoriga, xususan Qozog'iston va Qirg'izistonga chiqishni rejalashtirganmiz."
    )

    # =========================================================================
    # SLIDE 15 — KUTILAYOTGAN IQTISODIY VA IJTIMOIY SAMARA / EXPECTED IMPACT
    # =========================================================================
    s15 = prs.slides.add_slide(blank_layout)
    apply_background(s15, LIGHT_BG)
    add_header(s15, "Samaradorlik va ROI", "Kutilayotgan iqtisodiy va ekologik samara", "Korxona, energetika tizimi va davlat miqyosidagi o'lchanadigan natijalar")
    add_footer(s15, 15)

    # Left: Enterprise ROI
    card_roi = add_card(s15, Inches(0.8), Inches(1.85), Inches(5.7), Inches(4.7))
    tb_r = s15.shapes.add_textbox(Inches(1.05), Inches(2.05), Inches(5.2), Inches(4.3))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True

    pr1 = tf_r.paragraphs[0]
    pr1.text = "KORXONA DARAJASIDAGI FOYDA (ROI)"
    pr1.font.name = FONT_HEADING
    pr1.font.size = Pt(10)
    pr1.font.bold = True
    pr1.font.color.rgb = PRIMARY_BLUE

    pr2 = tf_r.add_paragraph()
    pr2.text = "O'rtacha ishlab chiqarish korxonasi misolida:"
    pr2.font.name = FONT_HEADING
    pr2.font.size = Pt(13)
    pr2.font.bold = True
    pr2.font.color.rgb = DARK_NAVY
    pr2.space_before = Pt(4)

    roi_items = [
        ("8 – 15% oylik tejamkorlik", "Oylik elektr to'lovi 80 mln so'm bo'lgan korxona har oyda 6.4 – 12 mln so'm tejaydi. Yillik iqtisod: 75 – 140 mln so'm."),
        ("Reaktiv quvvat jarimalarini bartaraf etish", "Kosines fi (cos φ) pasayib ketishi oqibatida qo'llaniladigan jarimalar va ortiqcha to'lovlar 0 ga tushiriladi."),
        ("Uskunalar resursini 15–20% ga uzaytirish", "Ortiqcha qizib ketish, quruq ishlash va ortiqcha zo'riqishlar oldi olinishi hisobiga ta'mirlash xarajatlari kamayadi."),
        ("Investitsiyaning oqlanishi (Payback period)", "NEXTGEN obuna narxi tejalgan mablag'ning atigi 10–15% qismini tashkil etadi. Tizim birinchi haftadayoq o'zini oqlaydi.")
    ]
    for rh, rd in roi_items:
        prh = tf_r.add_paragraph()
        prh.text = f"✔  {rh}"
        prh.font.name = FONT_HEADING
        prh.font.size = Pt(10)
        prh.font.bold = True
        prh.font.color.rgb = DARK_NAVY
        prh.space_before = Pt(8)

        prd = tf_r.add_paragraph()
        prd.text = f"   {rd}"
        prd.font.name = FONT_BODY
        prd.font.size = Pt(9.5)
        prd.font.color.rgb = SECONDARY_TEXT
        prd.space_before = Pt(2)

    # Right: National / Ecological Impact
    card_nat = add_card(s15, Inches(6.8), Inches(1.85), Inches(5.733), Inches(4.7))
    tb_n = s15.shapes.add_textbox(Inches(7.05), Inches(2.05), Inches(5.2), Inches(4.3))
    tf_n = tb_n.text_frame
    tf_n.word_wrap = True

    pn1 = tf_n.paragraphs[0]
    pn1.text = "MILLIY VA EKOLOGIK TA'SIR (ESG)"
    pn1.font.name = FONT_HEADING
    pn1.font.size = Pt(10)
    pn1.font.bold = True
    pn1.font.color.rgb = SUCCESS_GREEN

    pn2 = tf_n.add_paragraph()
    pn2.text = "O'zbekiston energetika tizimiga qo'shiladigan hissa:"
    pn2.font.name = FONT_HEADING
    pn2.font.size = Pt(13)
    pn2.font.bold = True
    pn2.font.color.rgb = DARK_NAVY
    pn2.space_before = Pt(4)

    nat_items = [
        ("Tarmoqdagi pik yuklamalarni yumshatish", "Pik soatlarda (17:00–21:00) korxonalarning asossiz yuklamalarini kamaytirish orqali umumiy tarmoq avariyalarining oldi olinadi."),
        ("Uglerod izini (CO2) qisqartirish", "Har 1,000 kWh tejalgan elektr energiyasi atmosferaga chiqariladigan taxminan 450–500 kg CO2 chiqindisini kamaytiradi."),
        ("O'zbekiston – 2030 strategiyasini qo'llab-quvvatlash", "Iqtisodiyotda energiya sig'imini 30% ga kamaytirish bo'yicha davlat dasturiga to'g'ridan-to'g'ri amaliy hissa qo'shadi."),
        ("Eksportbop korxonalar uchun yashil sertifikatlar", "Yevropa bozoriga eksport qiluvchi korxonalar uglerod solig'i (CBAM) to'lashdan tejaladi.")
    ]
    for nh, nd in nat_items:
        pnh = tf_n.add_paragraph()
        pnh.text = f"★  {nh}"
        pnh.font.name = FONT_HEADING
        pnh.font.size = Pt(10)
        pnh.font.bold = True
        pnh.font.color.rgb = DARK_NAVY
        pnh.space_before = Pt(8)

        pnd = tf_n.add_paragraph()
        pnd.text = f"   {nd}"
        pnd.font.name = FONT_BODY
        pnd.font.size = Pt(9.5)
        pnd.font.color.rgb = SECONDARY_TEXT
        pnd.space_before = Pt(2)

    set_speaker_notes(s15,
        "VAQT: 60 SONIYA\n\n"
        "Ushbu loyiha kimga qanday foyda keltiradi? Keling, aniq hisob-kitobni ko'raylik.\n\n"
        "Korxona uchun: Agar o'rtacha to'qimachilik fabrikasi oyiga 80 million so'm elektr to'lasa, NEXTGEN orqali 10% tejamkorlik erishilsa — bu har oy 8 million so'm, yiliga qariyb 100 million so'm toza tejamkorlik demakdir!\n\n"
        "Davlat va jamiyat uchun: Mamlakatimizda yuzlab korxonalar elektrni oqilona sarflasa, tarmoqdagi transformatorlar zo'riqishi kamayadi, avariyalar qisqaradi va minglab tonna CO2 chiqindisi kamayadi.\n\n"
        "Bu nafaqat biznes loyiha, bu O'zbekiston yashil iqtisodiyotiga qo'shiladigan real hissadir."
    )

    # =========================================================================
    # SLIDE 16 — YAKUNIY CHAQIRIQ / CALL TO ACTION (Hero Dark Blue)
    # =========================================================================
    s16 = prs.slides.add_slide(blank_layout)
    apply_background(s16, DEEP_BLUE)

    strip16 = s16.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.12))
    strip16.fill.solid()
    strip16.fill.fore_color.rgb = PRIMARY_BLUE
    strip16.line.fill.background()

    # Category Pill
    pill16 = add_card(s16, Inches(1.0), Inches(0.9), Inches(4.5), Inches(0.42), bg_color=RGBColor(26, 75, 140), border_color=PRIMARY_BLUE)
    tb_pill16 = s16.shapes.add_textbox(Inches(1.1), Inches(0.96), Inches(4.3), Inches(0.3))
    tf_p16 = tb_pill16.text_frame
    p_p16 = tf_p16.paragraphs[0]
    p_p16.text = "HAMKORLIK VA PILOT LOYIHA  |  2026"
    p_p16.font.name = FONT_HEADING
    p_p16.font.size = Pt(10)
    p_p16.font.bold = True
    p_p16.font.color.rgb = RGBColor(186, 215, 255)

    # Headline
    tb_h16 = s16.shapes.add_textbox(Inches(0.95), Inches(1.5), Inches(11.0), Inches(1.0))
    tf_h16 = tb_h16.text_frame
    p_h16 = tf_h16.paragraphs[0]
    p_h16.text = "NEXTGEN AI bilan energiyani aqlli boshqaring!"
    p_h16.font.name = FONT_HEADING
    p_h16.font.size = Pt(36)
    p_h16.font.bold = True
    p_h16.font.color.rgb = WHITE

    # Left: Pilot Program Invitation Card
    card_inv = add_card(s16, Inches(1.0), Inches(2.7), Inches(6.0), Inches(3.8), bg_color=RGBColor(24, 66, 125), border_color=RGBColor(45, 95, 170))
    tb_inv = s16.shapes.add_textbox(Inches(1.25), Inches(2.9), Inches(5.5), Inches(3.4))
    tf_inv = tb_inv.text_frame
    tf_inv.word_wrap = True

    pi1 = tf_inv.paragraphs[0]
    pi1.text = "BUGUNGI TAKLIFIMIZ:"
    pi1.font.name = FONT_HEADING
    pi1.font.size = Pt(11)
    pi1.font.bold = True
    pi1.font.color.rgb = RGBColor(147, 197, 253)

    pi2 = tf_inv.add_paragraph()
    pi2.text = "5 ta Sanoat Korxonasiga 30 Kunlik Bepul Pilot Dasturi"
    pi2.font.name = FONT_HEADING
    pi2.font.size = Pt(15)
    pi2.font.bold = True
    pi2.font.color.rgb = WHITE
    pi2.space_before = Pt(4)

    inv_points = [
        "Hisoblagich ma'lumotlarini bepul audit qilish va tizimga ulash",
        "Kechki isroflar va anomaliyalarni aniqlash hisoboti",
        "O'zbek tilidagi AI maslahatchi va Telegram botga to'liq kirish",
        "Korxona rahbariyati uchun 8–15% tejamkorlik yo'l xaritasi",
        "Hech qanday dastlabki to'lov yoki majburiyat talab etilmaydi"
    ]
    for pt in inv_points:
        ppt = tf_inv.add_paragraph()
        ppt.text = f"✔  {pt}"
        ppt.font.name = FONT_BODY
        ppt.font.size = Pt(10)
        ppt.font.color.rgb = RGBColor(224, 238, 255)
        ppt.space_before = Pt(5)

    # Right: Contact & Action Card
    card_act = add_card(s16, Inches(7.3), Inches(2.7), Inches(5.0), Inches(3.8), bg_color=RGBColor(24, 66, 125), border_color=PRIMARY_BLUE)
    tb_act = s16.shapes.add_textbox(Inches(7.55), Inches(2.9), Inches(4.5), Inches(3.4))
    tf_act = tb_act.text_frame
    tf_act.word_wrap = True

    pa1 = tf_act.paragraphs[0]
    pa1.text = "BOG'LANISH VA MUALLIF:"
    pa1.font.name = FONT_HEADING
    pa1.font.size = Pt(11)
    pa1.font.bold = True
    pa1.font.color.rgb = RGBColor(147, 197, 253)

    pa2 = tf_act.add_paragraph()
    pa2.text = "Shohjahon Abdullayev"
    pa2.font.name = FONT_HEADING
    pa2.font.size = Pt(16)
    pa2.font.bold = True
    pa2.font.color.rgb = WHITE
    pa2.space_before = Pt(4)

    pa3 = tf_act.add_paragraph()
    pa3.text = "NEXTGEN AI asoschisi va loyiha yetakchisi"
    pa3.font.size = Pt(10)
    pa3.font.color.rgb = RGBColor(186, 215, 255)
    pa3.space_before = Pt(2)

    c_details = [
        ("Veb platforma", "nextgen-ai-87ff.vercel.app"),
        ("Telegram Bot", "@nextgenuzz_bot"),
        ("Mobil ilova", "Telegram orqali /apk buyrug'i"),
        ("Hamkorlik", "Toshkent shahri, O'zbekiston")
    ]
    for clbl, cval in c_details:
        pc = tf_act.add_paragraph()
        pc.text = f"•  {clbl}:  {cval}"
        pc.font.name = FONT_BODY
        pc.font.size = Pt(10)
        pc.font.color.rgb = WHITE
        pc.space_before = Pt(6)

    # Footer on Slide 16
    tb_f16 = s16.shapes.add_textbox(Inches(1.0), Inches(6.85), Inches(11.3), Inches(0.3))
    tf_f16 = tb_f16.text_frame
    p_f16 = tf_f16.paragraphs[0]
    p_f16.text = "E'tiboringiz uchun tashakkur! Savollaringizga mamnuniyat bilan javob beraman."
    p_f16.font.size = Pt(10)
    p_f16.font.italic = True
    p_f16.font.color.rgb = RGBColor(186, 215, 255)

    set_speaker_notes(s16,
        "VAQT: 45 SONIYA\n\n"
        "HURMATLI FORUM ISHTIROKCHILARI VA KORXONA RAHBARLARI!\n\n"
        "Bugun biz shunchaki texnologiya haqida emas, O'zbekiston sanoatining ertangi raqobatbardoshligi haqida gaplashdik.\n\n"
        "Biz bugun zalda o'tirgan yoki bizni eshitayotgan 5 ta sanoat korxonasiga 30 kunlik to'liq bepul pilot dasturini taklif qilamiz. Biz sizning ma'lumotlaringizni tizimga ulaymiz, anomaliyalarni topamiz va aniq tejamkorlik rejasini taqdim etamiz.\n\n"
        "Shuningdek, biz bilan birga ushbu milliy startapni rivojlantirish istagida bo'lgan investorlar va mentorlar bilan ochiq muloqotga tayyormiz.\n\n"
        "Platformani hoziroq sinab ko'rishingiz mumkin: nextgen-ai-87ff.vercel.app yoki Telegramda @nextgenuzz_bot.\n\n"
        "E'tiboringiz uchun katta rahmat! Savollaringizga mamnuniyat bilan javob beraman."
    )

    # =========================================================================
    # SLIDE 17 (APPENDIX A) — TIZIMNING TO'LIQ TEXNIK ARXITEKTURASI
    # =========================================================================
    s17 = prs.slides.add_slide(blank_layout)
    apply_background(s17, LIGHT_BG)
    add_header(s17, "Texnik ilova (Appendix A)", "Tizimning to'liq arxitekturasi va komponentlar o'zaro aloqasi", "Frontend, API Gateway, Analitika Dvigateli, Xavfsizlik va Bot integratsiyasi")
    add_footer(s17, 17)

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
            "Multi-tenant ajratish (Har bir korxona uchun alohida tenant_id)",
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
        x = Inches(0.8) + col * Inches(5.95)
        y = Inches(1.85) + row * Inches(2.4)

        add_card(s17, x, y, Inches(5.75), Inches(2.25))

        bar = s17.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, Inches(5.75), Inches(0.08))
        bar.fill.solid()
        bar.fill.fore_color.rgb = ac_clr
        bar.line.fill.background()

        tb = s17.shapes.add_textbox(x + Inches(0.2), y + Inches(0.18), Inches(5.35), Inches(1.95))
        tf = tb.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = ac_t
        p1.font.name = FONT_HEADING
        p1.font.size = Pt(12)
        p1.font.bold = True
        p1.font.color.rgb = DARK_NAVY

        for item in ac_items:
            pi = tf.add_paragraph()
            pi.text = f"•  {item}"
            pi.font.name = FONT_BODY
            pi.font.size = Pt(9.5)
            pi.font.color.rgb = DARK_TEXT
            pi.space_before = Pt(3)

    set_speaker_notes(s17,
        "ILOVA A: TEXNIK ARXITEKTURA BO'YICHA SAVOLLAR UCHUN.\n\n"
        "Hakamlar yoki texnik ekspertlar arxitektura haqida so'raganda ushbu slayd ko'rsatiladi.\n\n"
        "Tizim 4 ta qatlamdan iborat: Mijoz interfeysi (Next.js + Bot), Xavfsiz FastAPI shlyuzi, Analitika va statistik hisoblash dvigateli hamda Grounded AI tahlilchisi.\n\n"
        "Har bir qatlam asinxron ishlaydi, ma'lumotlar bazasi ko'p ijarachilik (multi-tenancy) tamoyiliga tayanadi."
    )

    # =========================================================================
    # SLIDE 18 (APPENDIX B) — HISOBLASH METODOLOGIYASI VA MATEMATIK MODELLAR
    # =========================================================================
    s18 = prs.slides.add_slide(blank_layout)
    apply_background(s18, LIGHT_BG)
    add_header(s18, "Texnik ilova (Appendix B)", "Hisoblash metodologiyasi va matematik modellar", "Quvvat (kW), sarf (kWh), Z-Score anomaliya va differensial tarif formulalari")
    add_footer(s18, 18)

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
        x = Inches(0.8) + col * Inches(5.95)
        y = Inches(1.85) + row * Inches(2.4)

        add_card(s18, x, y, Inches(5.75), Inches(2.25))

        tb = s18.shapes.add_textbox(x + Inches(0.2), y + Inches(0.15), Inches(5.35), Inches(2.0))
        tf = tb.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = m_title
        p1.font.name = FONT_HEADING
        p1.font.size = Pt(11)
        p1.font.bold = True
        p1.font.color.rgb = DARK_NAVY

        p_form = tf.add_paragraph()
        p_form.text = m_formula
        p_form.font.name = "Consolas"
        p_form.font.size = Pt(10.5)
        p_form.font.bold = True
        p_form.font.color.rgb = PRIMARY_BLUE
        p_form.space_before = Pt(4)

        p_exp = tf.add_paragraph()
        p_exp.text = m_exp
        p_exp.font.name = FONT_BODY
        p_exp.font.size = Pt(9)
        p_exp.font.color.rgb = DARK_TEXT
        p_exp.space_before = Pt(4)

    set_speaker_notes(s18,
        "ILOVA B: ENERGETIK VA MATEMATIK HISOB-KITOBLAR BO'YICHA SAVOLLAR UCHUN.\n\n"
        "Ushbu slayd korxonaning bosh energetigi yoki texnik hay'at a'zolari formulalarni so'raganda qo'llaniladi.\n\n"
        "Biz kW (oniy quvvat) va kWh (sarflangan energiya) farqini qat'iy ajratamiz.\n\n"
        "Anomaliyalar statistik Z-score orqali aniqlanadi. Tariflar esa O'zbekiston energetika qoidalariga muvofiq pik, yarim pik va tungi soatlarga bo'lib hisoblanadi."
    )

    # =========================================================================
    # SLIDE 19 (APPENDIX C) — XATARLAR TAHLILI VA ULARNI YUMSHATISH
    # =========================================================================
    s19 = prs.slides.add_slide(blank_layout)
    apply_background(s19, LIGHT_BG)
    add_header(s19, "Texnik ilova (Appendix C)", "Xatarlar tahlili va ularni yumshatish choralari", "Texnik, operatsion, qonunchilik va xavfsizlik risklarini professional boshqarish")
    add_footer(s19, 19)

    risks = [
        ("1. Ma'lumotlar sifati pastligi (GIGO)", 
         "Xatar: Korxona hisoblagichlarida uzilishlar bo'lishi yoki Excel faylda noto'g'ri raqamlar kiritilishi.",
         "Yumshatish: Tizim ichiga avtomatlashtirilgan validatsiya, anomaliya filtrlari va yetishmayotgan qatorlarni statistik to'ldirish algoritmlari kiritilgan.",
         WARNING_AMBER),

        ("2. Korxonada Internet uzilishi", 
         "Xatar: Sanoat zonalarida internet vaqti-vaqti bilan uzilib qolishi mumkin.",
         "Yumshatish: Lokal kesh va oflayn rejim. Internet tiklanganda to'plangan ma'lumotlar avtomatik sinxronizatsiya qilinadi.",
         PRIMARY_BLUE),

        ("3. Xodimlarning yangi texnologiyani qabul qilmasligi", 
         "Xatar: Bosh muhandis yoki energetiklar murakkab dasturlarni o'rganishni istamasligi.",
         "Yumshatish: O'ta sodda veb-panel va har kimga tanish bo'lgan Telegram boti. Barcha hisobotlar tushunarli o'zbek tilida beriladi.",
         SUCCESS_GREEN),

        ("4. Kiberxavfsizlik va ma'lumotlar sizib chiqishi", 
         "Xatar: Korxonaning elektr iste'moli ma'lumotlarining tashqariga chiqishi.",
         "Yumshatish: Multi-tenant arxitektura, shifrlangan ma'lumotlar bazasi va strategik zavodlar uchun to'liq lokal On-Premise o'rnatish imkoniyati.",
         DEEP_BLUE)
    ]

    for idx, (r_t, r_desc, r_mit, r_clr) in enumerate(risks):
        row = idx // 2
        col = idx % 2
        x = Inches(0.8) + col * Inches(5.95)
        y = Inches(1.85) + row * Inches(2.4)

        add_card(s19, x, y, Inches(5.75), Inches(2.25))

        bar = s19.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, Inches(5.75), Inches(0.08))
        bar.fill.solid()
        bar.fill.fore_color.rgb = r_clr
        bar.line.fill.background()

        tb = s19.shapes.add_textbox(x + Inches(0.2), y + Inches(0.18), Inches(5.35), Inches(1.95))
        tf = tb.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = r_t
        p1.font.name = FONT_HEADING
        p1.font.size = Pt(11.5)
        p1.font.bold = True
        p1.font.color.rgb = DARK_NAVY

        p2 = tf.add_paragraph()
        p2.text = r_desc
        p2.font.name = FONT_BODY
        p2.font.size = Pt(9)
        p2.font.color.rgb = DARK_TEXT
        p2.space_before = Pt(3)

        p3 = tf.add_paragraph()
        p3.text = f"✔  Yechim: {r_mit}"
        p3.font.name = FONT_BODY
        p3.font.size = Pt(9)
        p3.font.bold = True
        p3.font.color.rgb = r_clr
        p3.space_before = Pt(4)

    set_speaker_notes(s19,
        "ILOVA C: XATARLAR VA XAVFSIZLIK BO'YICHA SAVOLLAR UCHUN.\n\n"
        "Investorlar ko'pincha loyihadagi xatarlar va ularni qanday boshqarishimiz haqida so'rashadi.\n\n"
        "Biz asosiy 4 ta xatarni tahlil qilganmiz:\n"
        "1. Yomon ma'lumotlar — avtomatik tozalash orqali hal qilinadi.\n"
        "2. Internet uzilishi — kesh va oflayn bufer orqali bartaraf etiladi.\n"
        "3. Kadrlar qabul qilmasligi — sodda Telegram interfeysi orqali yengiladi.\n"
        "4. Xavfsizlik — lokal On-premise o'rnatish imkoniyati orqali kafolatlanadi."
    )

    # =========================================================================
    # SLIDE 20 (APPENDIX D) — HAKAMLAR VA INVESTORLAR UCHUN ASOSIY Q&A
    # =========================================================================
    s20 = prs.slides.add_slide(blank_layout)
    apply_background(s20, LIGHT_BG)
    add_header(s20, "Texnik ilova (Appendix D)", "Hakamlar va investorlar uchun asosiy savol-javoblar", "Eng ko'p beriladigan 5 ta strategik savolga qisqa va qat'iy javoblar")
    add_footer(s20, 20)

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

    top20_y = Inches(1.85)
    card20_h = Inches(0.9)
    gap20 = Inches(0.08)

    for idx, (q, a) in enumerate(qa_list):
        y = top20_y + idx * (card20_h + gap20)
        add_card(s20, Inches(0.8), y, Inches(11.733), card20_h)

        bar = s20.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), y, Inches(0.08), card20_h)
        bar.fill.solid()
        bar.fill.fore_color.rgb = PRIMARY_BLUE
        bar.line.fill.background()

        tb = s20.shapes.add_textbox(Inches(1.05), y + Inches(0.08), Inches(11.3), card20_h - Inches(0.15))
        tf = tb.text_frame
        tf.word_wrap = True

        pq = tf.paragraphs[0]
        pq.text = q
        pq.font.name = FONT_HEADING
        pq.font.size = Pt(10.5)
        pq.font.bold = True
        pq.font.color.rgb = DARK_NAVY

        pa = tf.add_paragraph()
        pa.text = f"Javob: {a}"
        pa.font.name = FONT_BODY
        pa.font.size = Pt(9.5)
        pa.font.color.rgb = DARK_TEXT
        pa.space_before = Pt(2)

    set_speaker_notes(s20,
        "ILOVA D: TAQDIMOTDAN KEYINGI SAVOL-JAVOB VAQTI UCHUN.\n\n"
        "Hakamlar hay'ati va investorlar tomonidan berilishi mumkin bo'lgan eng asosiy 5 ta savolning qisqa konspekti ushbu slaydda jamlangan.\n\n"
        "Taqdimotchi ushbu javoblarni qisqa, dadil va dalillarga tayangan holda aytishi lozim."
    )

    # Save presentation
    prs.save(output_path)
    print(f"Presentation successfully saved to {output_path}")

if __name__ == "__main__":
    out_dir = os.path.dirname(os.path.abspath(__file__))
    out_pptx = os.path.join(out_dir, "NEXTGEN_AI_Presentation_UZ.pptx")
    build_presentation(out_pptx)
