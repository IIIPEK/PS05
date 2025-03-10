import scrapy
from divanru import DivanRu
from selenium import webdriver

class DivannewparsSpider(scrapy.Spider):
    name = "divannewpars"
    allowed_domains = ["https://divan.ru"]
    #start_urls = ["https://divan.ru/category/divany-i-kresla"]
    start_urls = ["https://www.divan.ru/samara/category/svet"]

    def __init__(self, *args, **kwargs):
        super(DivannewparsSpider, self).__init__(*args, **kwargs)
        self.driver = webdriver.Chrome()  # Selenium для загрузки категорий
        self.divan = DivanRu(self.driver, "https://divan.ru")
        self.divan.get_category()  # Загружаем категории
        self.start_urls = [url[0] for url in self.divan.categories]
        self.category_names = [url[1] for url in self.divan.categories]
        self.driver.quit()

    def parse(self, response):
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
                'start_url': response.url,
                'card_name': f'{card_name}',
                'price' : price,
                'url' :  response.urljoin(card.xpath('.//a[@target="_blank"]/@href').get()),
            }


