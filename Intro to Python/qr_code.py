from sys import path
import qrcode

website_link = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'

qr = qrcode.QRCode(version=1, box_size=5, border=5)


qr.add_data(website_link)

img = qr.make_image(fill_color='black', back_color='white')

img.save("qr.png")  # type: ignore
