import pyqrcode
import png
from pyqrcode import QRCode
from PIL import Image, ImageFont, ImageDraw
import os
s = "https://patients-db-system.herokuapp.com/lab"
  
url = pyqrcode.create(s)
  
url.png('myqr.png', scale = 6)

logo_file = "myqr.png"
logoIm = Image.open(logo_file)
im = Image.open("2.jpg")
logoIm = logoIm.resize((350, 350))
logoWidth, logoHeight = logoIm.size
print(logoWidth,logoHeight)
im.paste(logoIm, (610, 120))
im.save(os.path.join("qr.jpg"))
im = Image.open("qr.jpg")
draw = ImageDraw.Draw(im)

extra_bold = ImageFont.truetype('Raleway-ExtraBold.ttf', size=45)
black = ImageFont.truetype('Raleway-Black.ttf', size=25)
light = ImageFont.truetype('Raleway-Light.ttf', size=20)


(x, y) = (50, 90)
message = "JANE DOE"
color = 'rgb(58,175,169)' 
draw.text((x, y), message, fill=color, font=extra_bold)


(x, y) = (50, 170)
name = 'Patient - 1A1012'
color = 'rgb(23,37,40)' 
draw.text((x, y), name, fill=color, font=black)

(x, y) = (50,400)
name = 'Mobile - 9988776655'
color = 'rgb(23,37,40)'
draw.text((x, y), name, fill=color, font=light)
(x, y) = (50,430)
name = 'Address - Anywhere street, cityname, 111111'
color = 'rgb(23,37,40)'
draw.text((x, y), name, fill=color, font=light)

im.save('greeting_card.png')
