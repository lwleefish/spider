import scrapy
from ..items import NovelItem, ChapterItem, CategoryItem


class BiqukanSpider(scrapy.Spider):
    name = 'biquge'
    domain = "http://m.biqukan.com"
    cates = ["玄幻", "修真", "都市", "穿越", "网游", "科幻", "其他",
                   "排行榜", "全本"]

    def start_requests(self):
        urls = [  # "https://m.biqukan.com/sort/1_1/",
            # "https://m.biqukan.com/sort/2_1/",
            # "https://m.biqukan.com/sort/3_1/",
            # "https://m.biqukan.com/sort/4_1/",
            # "https://m.biqukan.com/sort/5_1/",
            # "https://m.biqukan.com/sort/6_1/",
            # "https://m.biqukan.com/sort/7_1/",
            # "https://m.biqukan.com/top/",
            "https://m.biqukan.com/full/1/"]
        for i, url in enumerate(urls):
            yield scrapy.Request(url=url, callback=self.parse,
                                 meta={"cate": self.cates[i]})
            break

    def parse(self, response):
        cate = response.meta.get("cate")
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
                                      callback=self.parse_summary, 
                                      meta={'page_no': 1, "cate": cate})
                break

    def cut_word(self, msg):
        if '：' in msg:
            msg = msg.split('：')[1]
        return msg

    def parse_summary(self, response):
        '''解析小说简介及相关信息'''
        page_no = response.meta['page_no']
        cate = response.meta.get("cate")
        title = response.css('.name::text').get()
        self.log("The title is %s and page_no is %d" % (title, page_no))
        if page_no == 1:
            novel = NovelItem()
            novel["name"] = title
            author = response.xpath(
                '//div[@class="book_box"]//span[1]/text()').get()
            novel["author"] = self.cut_word(author)
            novel["cate_name"] = cate
            counts = response.xpath(
                '//div[@class="book_box"]//dd[2]//span[2]/text()').get()
            novel["words_count"] = int(self.cut_word(counts))
            novel["summary"] = response.css(".book_about dd::text").get()
            self.log("novel title= %s" % novel["name"])
            yield novel
        hrefs = response.xpath(
            "//div[@class='book_last'][2]/dl/dd/a/@href").getall()

        for i, href in enumerate(hrefs):
            # 相对地址
            meta = {'title': title, 'cindex': page_no * 20 + i}
            yield response.follow(href, callback=self.parse_content, meta=meta)
            break
        next_page = response.css(".right a")
        # 最后一页没有下一页 attrib 是该元素属性字典
        if next_page and len(next_page) > 0 and 'href' in next_page[0].attrib:
            # 自动解析a 标签href #::attr(href)
            yield response.follow(next_page[0], callback=self.parse_summary,
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
        capter["cindex"] = response.meta['cindex']
        capter["novel_name"] = response.meta['title']
        capter["title"] = response.css(".header .title::text").get()
        lines = response.css("#chaptercontent::text").getall()
        if not lines:
            return None
        # 去除第一行和后两行垃圾
        # if lines[0].strip()
        capter["content"] = "\n".join(lines)
        yield capter
