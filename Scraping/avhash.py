from PIL import Image
import numpy as np

# 画像データをAverage Hashに変換
def average_hash(fname, size = 16):
    img = Image.open(fname) # 画像データ開く
    img = img.convert('L') # グレースケールに変換
    img = img.resize((size, size), Image.ANTIALIAS) # リサイズ
    pixel_data = img.getdata() # ピクセルデータを得る
    pixels = np.array(pixel_data) # Numpyの配列に変換
    pixels = pixels.reshape((size, size)) # 二次元の配列に変換
    avg = pixels.mean() # 算術平均を計算
    diff = 1 * (pixels > avg) # 平均より大きければ値を1、平均以下で0に変換
    return diff

# 二進数とみなしてハッシュ値に変換
def np2hash(n):
    bhash = []
    for n1 in ahash.tolist():
        s1 = [str(i) for i in n1]
        s2 = "".join(s1)
        i = int(s2, 2) # 二進数を整数に
        bhash.append("%04x" % i)
    return "".join(bhash)

# Average Hashを表示
ahash = average_hash(r'imgs/gauge_rectangle1.jpg')
ahash2 = average_hash(r'imgs/gauge_round1.jpg')
print(ahash)
print(np2hash(ahash))
print(ahash2)
print(np2hash(ahash2))
