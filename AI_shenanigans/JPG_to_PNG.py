import os
from posixpath import dirname
import img2pdf

pics_current_folder = (
    "C:\\Users\\carly\\Pictures\\Projects\\Cross Stitch & Needlepoint\\At The Office"
)

pdf_ultimate_destination = "C:\\Users\\carly\\Documents\\Cross Stitch PDFs\\Annie\'s Fashion Doll Club - Office Furniture.pdf"

# convert all files ending in .jpg inside a directory
dirname = pics_current_folder
imgs = []
for fname in os.listdir(dirname):
    if not fname.endswith(".jpg"):
        continue
    path = os.path.join(dirname, fname)
    if os.path.isdir(path):
        continue
    imgs.append(path)
with open(
    pdf_ultimate_destination,
    "wb",
) as f:
    data = img2pdf.convert(imgs)
    if data is None:
        raise RuntimeError("img2pdf.convert returned None")
    f.write(data)
