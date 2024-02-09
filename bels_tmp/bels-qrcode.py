# qr code generator with individual subject lines using qrcode
import qrcode as qr
from PIL import Image, ImageFont, ImageDraw
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('room', type=int, help="room number for labels")
parser.add_argument('num', type=int, help="number of benches to make labels for")
args = parser.parse_args()

email = "bsoe-bels@rt.ucsc.edu"
subject = "BENCH #{i} BE-{room}"

for i in range(int(args.num)):
    i += 1
    subject_i = subject.format(i=i, room=args.room)
    mailto = f"mailto:{email}?subject={subject_i}"
    img = qr.make(mailto)
    img = img.crop((35,35,410,410))
    print(f"QR code {i} has been created")
    img = img.convert("RGBA")

    bg_img = Image.open("bels.png")
    bg_img = bg_img.convert("RGBA")
    draw = ImageDraw.Draw(bg_img)
    font = ImageFont.truetype("Roboto-Regular.ttf", 100)
    pos1 = (870, 190) # bench number for double digits
    pos2 = (655, 290)
    color = (0, 60, 108)
    draw.text(pos1, f"{i}", fill=color, font=font)
    draw.text(pos2, f"{args.room}", fill=color, font=font)

    bg_width, bg_height = bg_img.size
    qr_width, qr_height = img.size
    position = 1097, 250

    bg_img.paste(img, position, img)
    bg_img.save(f"result_{i}.png")



