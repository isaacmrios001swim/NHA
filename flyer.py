"""
New Heights Aquatics — single-page promotional flyer (PDF).
Generates flyer.pdf in this folder.
"""
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor, Color
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.graphics.shapes import Drawing
from reportlab.graphics import renderPDF

# ---------- Brand palette ----------
NAVY = HexColor("#0b2545")
OCEAN = HexColor("#0b7fc5")
SKY = HexColor("#4fb3df")
POOL = HexColor("#e6f4fb")
ORANGE = HexColor("#f58220")
ORANGE_LIGHT = HexColor("#ffb070")
WHITE = HexColor("#ffffff")
INK = HexColor("#1a2233")
MUTE = HexColor("#5b6478")
LINE = HexColor("#e6e9ef")
SOFT = HexColor("#f6f9fc")

PAGE_W, PAGE_H = letter           # 612 x 792 pt
M = 36                            # outer margin

OUTPUT = "flyer.pdf"


def draw_wave(c, y, color, height=40, flip=False):
    """Decorative wave band across the page width."""
    c.setFillColor(color)
    p = c.beginPath()
    if not flip:
        p.moveTo(0, y)
        p.curveTo(PAGE_W * 0.25, y + height, PAGE_W * 0.75, y - height, PAGE_W, y)
        p.lineTo(PAGE_W, 0)
        p.lineTo(0, 0)
    else:
        p.moveTo(0, y)
        p.curveTo(PAGE_W * 0.25, y - height, PAGE_W * 0.75, y + height, PAGE_W, y)
        p.lineTo(PAGE_W, PAGE_H)
        p.lineTo(0, PAGE_H)
    p.close()
    c.drawPath(p, fill=1, stroke=0)


def draw_bubble(c, x, y, r, color, alpha=0.5):
    """Soft bubble accent."""
    c.saveState()
    col = Color(color.red, color.green, color.blue, alpha=alpha)
    c.setFillColor(col)
    c.circle(x, y, r, fill=1, stroke=0)
    c.restoreState()


def rounded_box(c, x, y, w, h, r, fill=None, stroke=None, lw=0):
    """A rounded rectangle helper."""
    if fill is not None:
        c.setFillColor(fill)
    if stroke is not None:
        c.setStrokeColor(stroke)
    c.setLineWidth(lw)
    c.roundRect(x, y, w, h, r, fill=1 if fill else 0, stroke=1 if stroke else 0)


def draw_qr(c, x, y, size, url):
    """Render a QR code of the given size (pt) at (x, y) bottom-left."""
    qr = QrCodeWidget(url, barLevel="M")
    bx, by, bx2, by2 = qr.getBounds()
    qr_w = bx2 - bx
    qr_h = by2 - by
    d = Drawing(size, size,
                transform=[size / qr_w, 0, 0, size / qr_h, -bx, -by])
    d.add(qr)
    renderPDF.draw(d, c, x, y)


def center_text(c, text, x_center, y, font, size, color):
    c.setFont(font, size)
    c.setFillColor(color)
    w = c.stringWidth(text, font, size)
    c.drawString(x_center - w / 2, y, text)


def left_text(c, text, x, y, font, size, color):
    c.setFont(font, size)
    c.setFillColor(color)
    c.drawString(x, y, text)


def main():
    c = canvas.Canvas(OUTPUT, pagesize=letter)
    c.setTitle("New Heights Aquatics — Flyer")

    # ---------- Background ----------
    c.setFillColor(POOL)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)

    # White paper card with margin
    rounded_box(c, M, M, PAGE_W - 2 * M, PAGE_H - 2 * M, 18, fill=WHITE)

    # Decorative bubbles
    draw_bubble(c, PAGE_W - 70, PAGE_H - 90, 60, ORANGE, alpha=0.14)
    draw_bubble(c, 80, 120, 70, OCEAN, alpha=0.10)
    draw_bubble(c, PAGE_W - 110, 150, 40, SKY, alpha=0.18)
    draw_bubble(c, 90, PAGE_H - 250, 30, ORANGE, alpha=0.18)

    # ---------- Top header band ----------
    band_h = 110
    band_y = PAGE_H - M - band_h
    c.saveState()
    # navy → ocean gradient simulation: navy block + ocean wave overlay
    c.setFillColor(NAVY)
    p = c.beginPath()
    p.moveTo(M, band_y)
    p.lineTo(M, band_y + band_h)
    p.lineTo(PAGE_W - M, band_y + band_h)
    p.lineTo(PAGE_W - M, band_y)
    p.curveTo(PAGE_W * 0.7, band_y - 22, PAGE_W * 0.3, band_y + 22, M, band_y)
    p.close()
    # clip to white paper rounded corners
    clip = c.beginPath()
    clip.roundRect(M, M, PAGE_W - 2 * M, PAGE_H - 2 * M, 18)
    c.clipPath(clip, stroke=0, fill=0)
    c.drawPath(p, fill=1, stroke=0)
    c.restoreState()

    # NHA logo + name (measure NHA width so the text doesn't overlap it)
    nha_font = "Helvetica-Bold"
    nha_size = 46
    nha_x = M + 26
    nha_baseline = band_y + band_h - 58
    left_text(c, "NHA", nha_x, nha_baseline, nha_font, nha_size, ORANGE)
    nha_w = c.stringWidth("NHA", nha_font, nha_size)
    label_x = nha_x + nha_w + 18  # always start labels clear of NHA
    label_top_y = band_y + band_h - 40
    label_sub_y = band_y + band_h - 62
    left_text(c, "NEW HEIGHTS AQUATICS",
              label_x, label_top_y, "Helvetica-Bold", 15, WHITE)
    left_text(c, "Swim lessons for every level",
              label_x, label_sub_y, "Helvetica", 11, ORANGE_LIGHT)

    # Top-right BOOK NOW! pill
    tag = "BOOK NOW!"
    tag_font = "Helvetica-Bold"
    tag_size = 11
    tw = c.stringWidth(tag, tag_font, tag_size)
    pill_w = tw + 22
    pill_h = 24
    pill_x = PAGE_W - M - 26 - pill_w
    pill_y = band_y + band_h - 28 - pill_h / 2
    rounded_box(c, pill_x, pill_y, pill_w, pill_h, pill_h / 2, fill=ORANGE)
    c.setFillColor(WHITE)
    c.setFont(tag_font, tag_size)
    c.drawString(pill_x + 11, pill_y + 7, tag)

    # QR code linking to the website, centered directly under the BOOK NOW pill
    qr_url = "https://newheightsaquatics.com"
    qr_size = 56
    qr_pad = 6
    card_size = qr_size + qr_pad * 2
    qr_card_x = pill_x + (pill_w - card_size) / 2
    qr_card_y = pill_y - 4 - card_size
    rounded_box(c, qr_card_x, qr_card_y, card_size, card_size, 8, fill=WHITE)
    draw_qr(c, qr_card_x + qr_pad, qr_card_y + qr_pad, qr_size, qr_url)

    # ---------- Hero ----------
    hero_y = band_y - 46
    center_text(c, "Build swim skills with us!", PAGE_W / 2, hero_y,
                "Helvetica-Bold", 30, NAVY)
    center_text(c,
                "Private lessons, special needs lessons, and pool time tailored to your swimmer.",
                PAGE_W / 2, hero_y - 22,
                "Helvetica", 12, MUTE)

    # Trust badges
    badges = [
        "✓ Red Cross lifeguard certified",
        "✓ 10+ years experience",
        "✓ Flexible weekly scheduling",
    ]
    badge_y = hero_y - 56
    full = "    ".join(badges)
    center_text(c, full, PAGE_W / 2, badge_y, "Helvetica-Bold", 10, OCEAN)

    # ---------- Skills bullets ----------
    skills_y = badge_y - 10
    rounded_box(c, M + 30, skills_y - 70, PAGE_W - 2 * M - 60, 60, 12, fill=POOL)
    center_text(c, "WE TEACH", PAGE_W / 2, skills_y - 22,
                "Helvetica-Bold", 9, ORANGE)
    skills_text = "Beginner Lessons  •  Stroke Development & Swim Team Prep  •  Water Polo Skills"
    center_text(c, skills_text, PAGE_W / 2, skills_y - 42,
                "Helvetica-Bold", 12, NAVY)

    # ---------- Two program cards ----------
    cards_top = skills_y - 95
    card_w = (PAGE_W - 2 * M - 24 - 50) / 2
    card_h = 170
    card_y = cards_top - card_h
    gap = 24

    # --- Card 1: Mobile Lessons ---
    cx1 = M + 25
    rounded_box(c, cx1, card_y, card_w, card_h, 14, fill=WHITE, stroke=LINE, lw=1)
    # Orange accent bar at top of card
    c.setFillColor(ORANGE)
    c.rect(cx1, card_y + card_h - 6, card_w, 6, fill=1, stroke=0)
    left_text(c, "MOBILE LESSONS", cx1 + 18, card_y + card_h - 30,
              "Helvetica-Bold", 11, ORANGE)
    left_text(c, "We come to you", cx1 + 18, card_y + card_h - 50,
              "Helvetica-Bold", 16, NAVY)
    # Big price
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 34)
    c.drawString(cx1 + 18, card_y + card_h - 92, "$1")
    c.setFillColor(MUTE)
    c.setFont("Helvetica", 11)
    c.drawString(cx1 + 56, card_y + card_h - 88, "per minute")
    # Description (wrap manually)
    desc_lines = [
        "Session length is flexible —",
        "starting at 30 minutes.",
    ]
    for i, line in enumerate(desc_lines):
        left_text(c, line, cx1 + 18, card_y + card_h - 115 - i * 14,
                  "Helvetica", 10, INK)

    # --- Card 2: Wilson HS pool ---
    cx2 = cx1 + card_w + gap
    rounded_box(c, cx2, card_y, card_w, card_h, 14, fill=WHITE, stroke=LINE, lw=1)
    c.setFillColor(OCEAN)
    c.rect(cx2, card_y + card_h - 6, card_w, 6, fill=1, stroke=0)
    left_text(c, "NO POOL? NO PROBLEM!", cx2 + 18, card_y + card_h - 30,
              "Helvetica-Bold", 11, OCEAN)
    left_text(c, "Come swim with us", cx2 + 18, card_y + card_h - 50,
              "Helvetica-Bold", 16, NAVY)
    bullets = [
        "Wilson High School Pool",
        "16455 Wedgeworth Dr",
        "Hacienda Heights, CA 91745",
        "Pool kept at 82° all year",
        "Select dates & times available",
    ]
    for i, line in enumerate(bullets):
        c.setFillColor(ORANGE)
        c.circle(cx2 + 24, card_y + card_h - 76 - i * 16, 2.5, fill=1, stroke=0)
        left_text(c, line, cx2 + 34, card_y + card_h - 80 - i * 16,
                  "Helvetica", 10, INK)

    # ---------- Specials & rewards ----------
    spec_top = card_y - 28
    center_text(c, "Save when you commit or refer a friend", PAGE_W / 2, spec_top,
                "Helvetica-Bold", 16, NAVY)

    promo_y = spec_top - 18
    promo_h = 80
    promo_w = (PAGE_W - 2 * M - 24 - 50) / 2

    # Promo 1: 10% off
    px1 = M + 25
    py1 = promo_y - promo_h
    # gradient feel: navy block with orange "badge"
    rounded_box(c, px1, py1, promo_w, promo_h, 14, fill=NAVY)
    # Orange badge
    badge_w = 90
    rounded_box(c, px1 + 14, py1 + promo_h - 26, badge_w, 22, 11, fill=ORANGE)
    center_text(c, "10% OFF", px1 + 14 + badge_w / 2, py1 + promo_h - 19,
                "Helvetica-Bold", 11, WHITE)
    left_text(c, "Multi-lesson discount", px1 + 14, py1 + promo_h - 44,
              "Helvetica-Bold", 13, WHITE)
    left_text(c, "Book 5+ lessons up front and save 10%.",
              px1 + 14, py1 + promo_h - 58, "Helvetica", 10, ORANGE_LIGHT)

    # Promo 2: Free lesson
    px2 = px1 + promo_w + gap
    rounded_box(c, px2, py1, promo_w, promo_h, 14, fill=OCEAN)
    badge2 = "FREE LESSON"
    bw2 = 110
    rounded_box(c, px2 + 14, py1 + promo_h - 26, bw2, 22, 11, fill=ORANGE)
    center_text(c, badge2, px2 + 14 + bw2 / 2, py1 + promo_h - 19,
                "Helvetica-Bold", 11, WHITE)
    left_text(c, "Referral bonus", px2 + 14, py1 + promo_h - 44,
              "Helvetica-Bold", 13, WHITE)
    left_text(c, "Refer a friend who books multiple lessons —",
              px2 + 14, py1 + promo_h - 58, "Helvetica", 10, POOL)
    left_text(c, "you get a lesson on us!", px2 + 14, py1 + promo_h - 70,
              "Helvetica", 10, POOL)

    # ---------- Footer / contact band ----------
    foot_h = 80
    foot_y = M
    # Navy footer band
    c.saveState()
    clip = c.beginPath()
    clip.roundRect(M, M, PAGE_W - 2 * M, PAGE_H - 2 * M, 18)
    c.clipPath(clip, stroke=0, fill=0)
    c.setFillColor(NAVY)
    p = c.beginPath()
    p.moveTo(M, foot_y + foot_h)
    p.curveTo(PAGE_W * 0.3, foot_y + foot_h + 22, PAGE_W * 0.7, foot_y + foot_h - 22, PAGE_W - M, foot_y + foot_h)
    p.lineTo(PAGE_W - M, foot_y)
    p.lineTo(M, foot_y)
    p.close()
    c.drawPath(p, fill=1, stroke=0)
    c.restoreState()

    center_text(c, "GET IN TOUCH", PAGE_W / 2, foot_y + foot_h - 22,
                "Helvetica-Bold", 10, ORANGE)
    center_text(c, "newheightsaquatics@gmail.com  •  (626) 277-8767",
                PAGE_W / 2, foot_y + foot_h - 40,
                "Helvetica-Bold", 14, WHITE)
    center_text(c, "newheightsaquatics.com",
                PAGE_W / 2, foot_y + foot_h - 58,
                "Helvetica", 11, ORANGE_LIGHT)

    c.showPage()
    c.save()
    print(f"Wrote {OUTPUT}")


if __name__ == "__main__":
    main()
