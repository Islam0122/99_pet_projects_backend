import qrcode

url = "http://127.0.0.1:5001/"
img = qrcode.make(url)
img.save("./Qr_codes/Wattendance_qr.png")
