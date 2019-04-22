import scrapy
from ..items import NovelItem, ChapterItem, CategoryItem


class BiqukanSpider(scrapy.Spider):
    name = 'biquge'
    domain = "http://m.biqukan.com"

    def start_requests(self):
        urls = ["https://m.biqukan.com/sort/1_1/",
                "https://m.biqukan.com/sort/2_1/",
                "https://m.biqukan.com/sort/3_1/",
                "https://m.biqukan.com/sort/4_1/",
                "https://m.biqukan.com/sort/5_1/",
                "https://m.biqukan.com/sort/6_1/",
                "https://m.biqukan.com/sort/7_1/",
                "https://m.biqukan.com/top/",
                "https://m.biqukan.com/full/1/"]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        hots = response.css(".wrap .hot .item .image a::attr('href')").getall()
        blocks = response.css(".wrap .block ul li a::attr('href')").getall()
        hrefs = []
        hrefs.extend(hots or [])
        hrefs.extend(blocks or [])
        if len(hrefs) > 0:
            for href in hrefs:
                self.log("summary url=%s" % href)
                # follow 绝对地址
                yield response.follow(self.domain + href,
                                      callback=self.parse_summary, meta={'page_no': 1})

    def parse_summary(self, response):
        '''解析小说简介及相关信息'''
        page_no = response.meta['page_no']
        if page_no == 1:
            novel = NovelItem()
            novel.title = response.css('.name::text').get()
            novel.author = response.xpath(
                '//div[@class="book_box"]//span[1]/text()').get()
            novel.cate_name = response.xpath(
                '//div[@class="book_box"]//span[1]/text()').get()

            novel.words_count = response.xpath(
                '//div[@class="book_box"]//dd[2]//span[1]/text()').get()
            novel.summary = response.css(".book_about dd::text").get()
            self.log("novel title= %s" % novel.title)
            yield novel
        hrefs = response.xpath(
            "//div[@class='book_last'][2]/dl/dd/a/@href").getall()

        title = response.css('.name::text').get()
        for i, href in enumerate(hrefs):
            # 相对地址
            meta = {'title': title, 'cindex': page_no * 20 + i}
            yield response.follow(href, callback=self.parse_content, meta=meta)
        next_page = response.css(".right a")
        # 最后一页没有下一页 attrib 是该元素属性字典
        if next_page and 'href' in next_page.attrib:
            # 自动解析a 标签href #::attr(href)
            yield response.follow(next_page, callback=self.parse_capter_url,
                                  meta={'page_no': page_no + 1})

    # def parse_capter_url(self, response):
    #    '''解析章节链接'''
    #    hrefs = response.xpath(
    #        "//div[@class='book_last'][2]/dl/dd/a/@href").getall()
    #    for href in hrefs:
    #        # 相对地址
    #        yield response.follow(href, callback=self.parse_content)
    #    next_page = response.css(".right a")
    #    # 自动解析a 标签href #::attr(href)
    #    yield response.follow(next_page, callback=self.parse_capter_url)

    def parse_content(self, response):
        '''解析文章'''
        capter = ChapterItem()
        capter.cindex = response.meta['cindex']
        capter.novel_name = response.meta['title']
        capter.title = response.css(".header .title::text").get()
        lines = response.css("#chaptercontent::text").getall()
        if not lines:
            return None
        # 去除第一行和后两行垃圾
        # if lines[0].strip()
        capter.content = "\r\n".join(lines)
        yield capter
