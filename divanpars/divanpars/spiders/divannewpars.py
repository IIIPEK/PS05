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
        # pagination  (//a[@data-testid='item' and contains(@href, '/category/divany-i-kresla/') and contains(@class,"PaginationLink")])[last()]

    def parse(self, response):
        print(f"Обработка ********************* {response.url}")
        if "/page-" not in response.url:
            last_page = response.xpath(
                "(//a[@data-testid='item' and contains(@class,'PaginationLink')])[last()]/text()").get()

            if last_page:
                last_page = int(last_page)  # Преобразуем в число
                category_url = response.url  # Базовый URL категории

                # Создаем запросы только для страниц от 2 до последней
                for page in range(2, last_page + 1):
                    next_page_url = f"{category_url}/page-{page}"
                    yield scrapy.Request(url=next_page_url, callback=self.parse)

        cards = response.xpath('//div[@itemscope and @itemprop="itemListElement" and @data-testid="product-card"]')
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


