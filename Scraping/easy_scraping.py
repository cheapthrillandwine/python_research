# scraping for Google
from icrawler.builtin import GoogleImageCrawler

crawler = GoogleImageCrawler(storage={"root_dir": "small"})
crawler.crawl(keyword="小型車　正面", offset=0, max_num=100)
#
# # in case of using filter
# filters = dict(
#     # size='large',
#     # size='medium',
#     # size='icon',
#     # size=>(640,480)
#     size=(300,300),
#     # color='',
#     # license=“noncommercial”, # (labeled for noncommercial reuse)
#     # license=“commercial”, # (labeled for reuse)
#     lisence='noncommercial,modify' # (labeled for noncommercial reuse with modification)
#     # lisecne=“commercial,modify”, # (labeled for reuse with modification)
#     # date=((2017, 1, 1), (2017, 11, 30))
# )
# crawler.crawl(keyword='motorbike',
#                     filters=filters,
#                     offset=0,
#                     max_num=100,
#                     min_size=(300,300),
#                     max_size=None,
#                     file_idx_offset=0
# )

# # scraping for Baidu
# from icrawler.builtin import BaiduImageCrawler
#
# baidu_crawler = BaiduImageCrawler(storage={'root_dir': 'your_image_dir'})
# baidu_crawler.crawl(keyword='cat', offset=0, max_num=1000,
#                     min_size=(200,200), max_size=None)

# scraping for Bing
# from icrawler.builtin import BingImageCrawler
#
# bing_crawler = BingImageCrawler(downloader_threads=4,
#                                 storage={'root_dir': 'motorbike_new'})
# bing_crawler.crawl(keyword='motorbike', filters=None, offset=0, max_num=100,    min_size=(300,300), max_size=None)
