import os, glob
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import cv2, random

# サイズの指定
image_size = 28 # MNISTと同サイズ

#
ttf_list = glob.glob("C:/Windows/Fonts/*.ttf")
ttf_list += glob.glob("~/Windows/Fonts/*.ttf")

print("font count=", len(ttf_list))

# 中央に文字を描画
def draw_text(img, font, text):
    dr = ImageDraw.Draw(img)
    img_sz = np.array(img.size)
    fo_sz = np.array(font.getsize(text))
    xy = (img_sz - fo_sz) / 2
    # print(img_sz,  fo_sz)
    dr.text(xy, text, font=font, fill=(255))

# サンプル画像を出力するフォルダ
if not os.path.exists("images/numbers"): os.makedirs("images/numbers")

# データの水増し
def gen_image(base_img, no, font_name):
    for ang in range(-20, 20, 2):
        sub_img = base_img.rotate(ang)
        data = np.asarray(sub_img)
        X.append(data)
        Y.append(no)
        w = image_size
        # 少しずつ拡大する
        for r in range(8,15,3):
            size = round((r/10) * image_size)
            img2 = cv2.resize(data, (size,size), cv2.INTER_AREA)
            data2 = np.asarray(img2)
            if image_size > size:
                x = (image_size - size) // 2
                data = np.zeros((image_size, image_size))
                data[x:x+size, x:x+size] = data2
            else:
                x = (size - image_size) // 2
                data = data2[x:x+w, x:x+w]
            X.append(data)
            Y.append(no)
            if random.randint(0, 400) == 0:
                fname = "images/numbers/n-{0}-{1}-{2}.PNG".format(
                    font_name, no, ang, r)
                cv2.imwrite(fname, data)
# 画像に描画
X = []
Y = []
for path in ttf_list:
    font_name = os.path.basename(path)
    try:
        fo = ImageFont.truetype(path, size=100)
    except:
        continue
    for no in range(10):
        img = Image.new("L", (200, 200))
        draw_text(img, fo, str(no))
        # フォントの描画範囲を得る
        ima = np.asarray(img)
        blur = cv2.GaussianBlur(ima, (5,5), 0)
        th = cv2.adaptiveThreshold(blur, 255, 1, 1, 11, 2)
        contours = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[1]
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            if w < 10 or h < 10: continue
            num = ima[y:y+h, x:x+w] # 部分画像を得る
            ww = w if w > h else h
            wx = (ww - w) // 2
            wy = (ww - h) // 2
            spc = np.zeros((ww, ww))
            spc[wy:wy+h, wx:wx+w] = num
            num = cv2.resize(spc, (image_size, image_size), cv2.INTER_AREA)
            # 標準の形状をデータに追加
            X.append(num)
            Y.append(no)
            # 少しずつ回転する
            base_img = Image.fromarray(np.uint8(num))
            gen_image(base_img, no, font_name)

X = np.array(X)
Y = np.array(Y)
np.savez("images/font_draw.npz", x=X, y=Y)
print("ok", len(Y))
