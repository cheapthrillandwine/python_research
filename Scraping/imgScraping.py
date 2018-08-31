from flickrapi import FlickrAPI
from urllib.request import urlretrieve
from pprint import pprint
import os, time, sys

# API キーの情報

key = "13074acf562bad0fdd56181d36e2fe81"
secret = "3f80fde66f28f19d"

# 重要：リクエストを送るタイミングが短すぎると画像取得先のサーバを逼迫してしまうか、
# スパムとみなされてしまう可能性があるので、待ち時間を 1 秒間設ける。
wait_time = 1

# コマンドライン引数の 1 番目の値を取得
foodname = sys.argv[1]
# 画像を保存するディレクトリを指定
savedir = "./" + foodname

# FlickrAPI にアクセス

# FlickrAPI(キー、シークレット、データフォーマット{json で受け取る})
flickr = FlickrAPI(key, secret, format='parsed-json')
result = flickr.photos.search(
    # 検索キーワード
    text = foodname,
    # 取得するデータ件数
    per_page = 100,
    # 検索するデータの種類(ここでは、写真)
    media = 'photos',
    # データの並び順(関連順)
    sort = 'relevance',
    # UI コンテンツを表示しない
    safe_search = 1,
    # 取得したいオプションの値(url_q->画像のアドレスが入っている情報、licence -> ライセンス情報)
    extras = 'url_q, licence'
)
# 結果を表示
photos = result['photos']
pprint(photos)
# 追記
for photo in photos['photo']:
    url_q = photo['url_q']
    # filepath = savedir + '/' + photo['id'] + '.jpg'
    filepath = savedir + '/' + photo['id'] + '.jpg'
    # ファイルが重複していたらスキップする
    if os.path.exists(filepath): continue
    # データをダウンロードする
    urlretrieve(url_q, filepath)
    # 重要：サーバを逼迫しないように 1 秒待つ
    time.sleep(wait_time)
