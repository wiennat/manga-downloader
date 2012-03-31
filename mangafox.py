#!/usr/bin/python

import re

from manga import Manga, App

class MangaFox(Manga):

    SERIES_URL = '%(baseurl)s/manga/%(series)s/?no_warning=1'
    CHAPTER_URL = '%(baseurl)s/manga/%(series)s/v%(volume)02d/c%(chapter)s/'
    PAGE_URL = '%(baseurl)s/manga/%(series)s/v%(volume)02d/c%(chapter)s/%(page)d.html'

    CHAPTER_PATTERN = '%(series)s-v%(volume)02d-c%(chapter)s.cbz'
    PAGE_PATTERN = '%(series)s-v%(volume)02d-c%(chapter)s-%(page)02d'

    CHAPTER_CRE = re.compile(r'/manga/[^/]+/v(\d+)/c([0-9.]+)/')

    def __init__(self):
        Manga.__init__(self, 'http://www.mangafox.com')

    def _list_chapters(self, doc):
        chapters = []
        for l in doc.xpath("//div[@id='chapters']/ul[@class='chlist']/li/div//a[@class='tips']"):
            u = l.attrib['href']
            m = self.CHAPTER_CRE.search(u)
            if not m:
                print 'unsupported url', u
                continue
            chapters.append({'volume': int(m.group(1)),
                             'chapter': m.group(2)})
        return chapters

    def _list_pages(self, doc):
        pages = doc.xpath("//div[@id='top_center_bar']/form/div/div/select/option")
        pages = filter(lambda i: i.text != 'Comments', pages)
        pages = [int(i.text) for i in pages]
        return pages

    def _download_page(self, doc):
        url = doc.xpath("//img[@id='image']")[0].attrib['src']
        return url

class MangaFoxApp(App):
    def __init__(self):
        App.__init__(self, chapter_func=str)
        if self.options.volume:
            self.data.update({'volume': int(self.options.volume)})
        self.manga = MangaFox()

    def _parse_args(self, parser):
        App._parse_args(self, parser)
        parser.add_option('--volume', dest='volume', default='',
                          help='Volume')

    def _filter_chapter(self, data):
        if 'volume' in self.data and data['volume'] != self.data['volume']:
            return True
        return App._filter_chapter(self, data)

if __name__ == '__main__':
    app = MangaFoxApp()
    app.run()
