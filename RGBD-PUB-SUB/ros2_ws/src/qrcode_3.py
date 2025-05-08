import qrcode
from PIL import Image
import qrcode.constants
import cv2

user_input = input("QR코드로 변환할 문자열을 입력하세요: ")

qr = qrcode.QRCode(
    version=None,
    error_correction=qrcode.constants.ERROR_CORRECT_M,
    box_size=10,
    border=4,
)
qr.add_data(user_input)
qr.make(fit=True)

img = qr.make_image(fill_color="black", back_color="white")

img.show()

save_input = input("QR코드를 파일로 저장하시겠습니까? (y/n): ").strip().lower()
if save_input == "y":
    img.save("user_input_qr.png")
    print("user_input_qr.png 파일로 저장되었습니다.")
    imgimg = cv2.imread("user_input_qr.png")
    cv2.imshow("image", imgimg)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("파일로 저장하지 않았습니다.")
