import scrapy


class DivannewparsSpider(scrapy.Spider):
    name = "divannewpars"
    allowed_domains = ["https://divan.ru"]
    #start_urls = ["https://divan.ru/category/divany-i-kresla"]
    start_urls = ["https://www.divan.ru/samara/category/svet"]

    def parse(self, response):
        # offer_catalog = response.xpath('//div[@itemscope and @itemtype="https://schema.org/OfferCatalog"]')
        # card_name = offer_catalog.xpath('./div[1]/div[3]/div[1]/div[1]/div[1]/div[1]/div[1]/@class').get()
        cards =  response.xpath('//div[@itemscope and @itemprop="itemListElement" and @data-testid="product-card"]')

        for card in cards:
            card_name = card.xpath('(.//span[@itemprop="name"])/text()').get()
            price = card.xpath('(.//span[@data-testid="price"])[2]/text()').get()
            if price == None:
                price = card.xpath('(.//span[@data-testid="price"])[1]/text()').get()
            try:
                price = int(price.replace(" ", ""))
            except:

                price = f"Error in {price}"
            yield {
                'card_name': card_name,
                'price' : price,
                'url' : card.xpath('.//a[@target="_blank"]/@href').get(),

            }


