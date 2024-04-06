import qrcode
import image

qr = qr.code.QRCode(
    version = 15,
    box_size = 10'
    border = 5
)
data = any url of your choice

qr.add_data(data)
qr.make(fit=True)
img = qr.make_image(fill="black",black_color="white")
img.save("QR.png")
