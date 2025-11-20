import qrcode

url = "http://192.168.190.188:5001/"
img = qrcode.make(url)
img.save("./Qr_codes/Wattendance_qr.png")
