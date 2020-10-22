# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from wiki.items import WikiItem


class WikiSpider(Spider):
    name = 'bestbuy_spider'
    start_urls = ['https://www.bestbuy.com/site/all-laptops/pc-laptops/pcmcat247400050000.c?id=pcmcat247400050000']
    allowed_urls = ['https://www.bestbuy.com']

    for url in start_urls:
        yield Request(url=url, callback=self.parse)

    def parse(self, response):
        num_pages = int(response.xpath('//ol[@class="paging-list"]/li')[-1].xpath('./a/text()').extract_first())
        url_list = [f'https://www.bestbuy.com/site/all-laptops/pc-laptops/pcmcat247400050000.c?cp={i+1}&id=pcmcat247400050000'
                    for i in range(num_pages)]
        for url in url_list[:2]:
            # For debugging
            # print('='*55)
            # print(url)
            # print('='*55)
            # Just like request.get(url) which gives a response object
            yield Request(url=url, callback=self.parse_result_page)
    def parse_result_page(self, response):
        products = response.xpath('//h4[@class="sku-header"]/a/@href').extract()

        product_urls = [f'https://www.bestbuy.com{url}' for url in products]

        for url in product_urls[:5]:
            # For debugging
            print('='*55)
            print(url)
            print('='*55)
            yield Request(url=url, callback=self.parse_product_page)

    def parse_product_page(self, response):
        product_name = response.xpath('//h1[@class="heading-5 v-fw-regular"]/text()').extract_first()
        try:
            answered_qs = response.xpath('//li[@class="ugc-qna-stats ugc-stat"]//text()').extract_first()
            answered_qs = int(re.findall('\d+', answered_qs)[0])
        except:
            print('*****No Answered Questions!!!*****')
            print(f'Offending URL: {response.url}')
            answered_qs = 0
        try:
            sku = int(response.xpath('//div[@class="sku product-data"]/span[2]/text()').extract_first().strip())
        except:
            print('*****Couldn\'t find SKU!*****')
            print(f'Offending URL: {response.url}')
            sku = None
        try:
            price = response.xpath('//div[@class="priceView-hero-price priceView-customer-price"]/span[1]/text()').extract_first()
        except:
            print('*****Couldn\'t find price!*****')
            print(f'Offending URL: {response.url}')
            price = None
        domain, second_half = response.url.split('/site')
        second_half = '/site/reviews' + second_half
        middle_part, _ = second_half.split('.p')
        review_url = domain + middle_part
        meta = {'product_name': product_name, 'answered_qs': answered_qs,
                'sku': sku, 'price': price}
        yield Request(url=review_url, callback=self.parse_review_page, meta=meta)
    def parse_review_page(self, response):
        # print('='*55)
        # print(response.meta)
        # print('='*55)
        reviews = response.xpath('//ul[@class="reviews-list"]/li')
        for review in reviews:
            user_name = review.xpath('.//div[@class="ugc-author v-fw-medium body-copy-lg"]//text()').extract_first()
            try:
                review_rating = review.xpath('.//div[@class="c-ratings-reviews-v4 c-ratings-reviews-v4-size-small false undefined"]/p/text()').extract_first()
                review_rating = int(re.findall('\d+', review_rating)[0])
            except:
                print('*****No review rating!!!*****')
                print(f'Offending URL: {response.url}')
                review_rating = None
            review_text = review.xpath('.//p[@class="pre-white-space"]//text()').extract_first()
            review_title = review.xpath('.//h4[@class="review-title c-section-title heading-5 v-fw-medium  "]/text()').extract_first()
            try:
                num_helpful = review.xpath('.//button[@data-track="Helpful"]/text()').extract_first()
                num_helpful = int(re.findall('\d+', num_helpful)[0])
            except:
                print('*****No helpful!!!*****')
                print(f'Offending URL: {response.url}')
                num_helpful = None
            try:
                num_unhelpful = review.xpath('.//button[@data-track="Unhelpful"]/text()').extract_first()
                num_unhelpful = int(re.findall('\d+', num_unhelpful)[0])
            except:
                print('*****No unhelpful!!!*****')
                print(f'Offending URL: {response.url}')
                num_unhelpful = None
            item = BestbuyItem()
            item['user_name'] = user_name
            item['review_rating'] = review_rating
            item['review_text'] = review_text
            item['review_title'] = review_title
            item['num_helpful'] = num_helpful
            item['num_unhelpful'] = num_unhelpful
            item['product_name'] = response.meta['product_name']
            item['answered_qs'] = response.meta['answered_qs']
            item['sku'] = response.meta['sku']
            item['price'] = response.meta['price']
            yield item















