import qrcode

img = qrcode.make("Hello, QR Code!")
img.save("simple_qrcode.png")
