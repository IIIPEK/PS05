import scrapy


class DivannewparsSpider(scrapy.Spider):
    name = "divannewpars"
    allowed_domains = ["https://divan.ru"]
    start_urls = ["https://divan.ru/category/divany-i-kresla"]

    def parse(self, response):
        offer_catalog = response.xpath('//div[@itemscope and @itemtype="https://schema.org/OfferCatalog"]')
        card_name = offer_catalog.xpath('./div[1]/div[3]/div[1]/div[1]/div[1]/div[1]/div[1]/@class').get()
        cards =  response.xpath('//div[@itemscope and @itemprop="itemListElement" and @data-testid="product-card"]')

        for card in cards:
            card_name = card.xpath('./div[1]/div[3]/div[1]/div[1]/div[1]/div[1]/div[1]/@class').get()
            yield {
                'card_name': card.xpath('(//span[@itemprop="name"])/text()').get(),
                'price' : int(card.xpath('(//span[@data-testid="price"])[2]/text()').get().replace(" ",""))
            }

        print(card_name)
