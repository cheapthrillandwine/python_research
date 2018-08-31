import base64

from icrawler import ImageDownloader
from icrawler.builtin import GoogleImageCrawler
from six.moves.urllib.parse import urlparse


class PrefixNameDownloader(ImageDownloader):

    def get_filename(self, task, default_ext):
        filename = super(PrefixNameDownloader, self).get_filename(
            task, default_ext)
        return filename


class Base64NameDownloader(ImageDownloader):

    def get_filename(self, task, default_ext):
        url_path = urlparse(task['file_url'])[2]
        if '.' in url_path:
            extension = url_path.split('.')[-1]
            if extension.lower() not in [
                    'jpeg', 'png', 'bmp', 'tiff', 'gif', 'ppm', 'pgm'
            ]:
            # if extension.lower() not in ['jpg']:
                extension = default_ext

        else:
            extension = default_ext
        # works for python 3
        filename = base64.b64encode(url_path.encode()).decode()
        return '{}.{}'.format(filename, extension)


google_crawler = GoogleImageCrawler(
    downloader_cls=PrefixNameDownloader,
    # downloader_cls=Base64NameDownloader,
    downloader_threads=4,
    storage={'root_dir': 'large_bus'})
google_crawler.crawl('バス　正面', max_num=50, offset=0)
