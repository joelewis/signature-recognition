############################################################
#------------- Author: Joe Lewis---------------------------#
#------------- License: Not good enough to be Licenced :) -#
#------------- P.S Sorry I don't like Gists ---------------#
############################################################

import Image, ImageEnhance

def enhance_signature(img):
  bw = ImageEnhance.Color(img).enhance(0.0)
  bright = ImageEnhance.Brightness(bw).enhance(2.2)
  contrast = ImageEnhance.Contrast(bright).enhance(2.0)
  
  sign = contrast.convert("RGBA")
  datas = sign.getdata()

  #--- Algo to detect non-signatured areas and reduce its alpha to zero --#
  newData = []
  for item in datas:
    if item[0] >  200 and item[1] > 200 and item[2] > 200:
      newData.append((255, 255, 255, 0))
    else:
      newData.append(item)

  sign.putdata(newData)
  sign.save("signature_alpha.png", "PNG")
  
def get_boxed_signature():
  img = Image.open("signature_alpha.png")
  img = img.convert("RGBA")
  pixdata = img.load()
  
  start_pixel = [img.size[0], img.size[1]]
  end_pixel = [0,0]

  #--- Algo to detect the region of space containing signature --#
  for y in xrange(img.size[1]):
    for x in xrange(img.size[0]):
      if pixdata[x, y][0] < 200 and pixdata[x, y][1] < 200 and pixdata[x, y][2] < 200:
        if x < start_pixel[0]:
          start_pixel[0] = x
        if y < start_pixel[1]:
          start_pixel[1] = y
        if x > end_pixel[0]:
          end_pixel[0] = x
        if y > end_pixel[1]:
          end_pixel[1] = y
  
  crop_box = (start_pixel[0]-20, start_pixel[1]-20, end_pixel[0]+20, end_pixel[1]+20)
  signature = img.crop(crop_box)
  signature.save("signature_beta.png", "PNG")
  Image.open("signature_beta.png").show()
  
if __name__ == "__main__":
  filename = str(raw_input("Where is your signature click? "))
  img = Image.open(filename)
  enhance_signature(img)
  get_boxed_signature()
  
