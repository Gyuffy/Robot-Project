import qrcode

data = "Customized QR Code!"

qr = qrcode.QRCode(
    version=None,
    box_size=10,
    border=5,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
)

qr.add_data(data)
qr.make(fit=True)

img = qr.make_image(fill_color="blue", back_color="yellow")
img.save("custom_qr_code.png")
