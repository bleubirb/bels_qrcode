# qr code generator with individual subject lines using qrcode
import qrcode as qr
from PIL import Image, ImageFont, ImageDraw
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("room", type=int, help="room number for labels")
parser.add_argument("num", type=int, help="number of benches to make labels for")
args = parser.parse_args()

email = "bsoe-bels@rt.ucsc.edu"
subject = "BENCH #{i} BE-{room}"

tags_per_page = 12

pages = []

# https://papersizes.online/paper-size/a4/pixels/ (300 DPI for A4 paper)
pg_width = 2480
pg_height = 3508

for pg in range(int(args.num) // tags_per_page + 1):
    tmp_pg = Image.new("RGBA", (pg_width, pg_height), (255, 255, 255, 255))
    pg_imgs = []

    for i in range(pg * tags_per_page, min((pg + 1) * tags_per_page, args.num)):
        i += 1
        subject_i = subject.format(i=i, room=args.room)
        mailto = f"mailto:{email}?subject={subject_i}"
        img = qr.make(mailto)
        img = img.crop((35, 35, 410, 410))
        print(f"QR code {i} has been created")
        img = img.convert("RGBA")

        bg_img = Image.open("bels.png")
        bg_img = bg_img.convert("RGBA")
        draw = ImageDraw.Draw(bg_img)
        font = ImageFont.truetype("Roboto-Regular.ttf", 100)
        pos1 = (870, 190)  # bench number for double digits
        pos2 = (655, 290)
        color = (0, 60, 108)
        draw.text(pos1, f"{i}", fill=color, font=font)
        draw.text(pos2, f"{args.room}", fill=color, font=font)

        bg_width, bg_height = bg_img.size
        qr_width, qr_height = img.size
        position = 1097, 250

        bg_img.paste(img, position, img)
        bg_img = bg_img.resize(
            (int(pg_width / 2), int(bg_height * (pg_width / 2) / bg_width))
        )
        # bg_img.save(f"result_{i}.png")
        pg_imgs.append(bg_img)

    for i, img in enumerate(pg_imgs):
        x = (i % 2) * (pg_width // 2)
        y = (i // 2) * (pg_height // 6)
        tmp_pg.paste(img, (x, y))
    # tmp_pg.save(f"page_{pg}.png")
    pages.append(tmp_pg)

pages[0].save(
    "bels_qr_codes.pdf", "PDF", resolution=300.0, save_all=True, append_images=pages[1:]
)
