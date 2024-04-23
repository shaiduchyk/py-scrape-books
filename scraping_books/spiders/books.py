import scrapy
from scrapy.http import Response


class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    def parse(self, response: Response, **kwargs):
        for product_url in response.css("h3 a::attr(href)").getall():
            product_url = response.urljoin(product_url)
            yield scrapy.Request(product_url, callback=self.parse_product)

        next_page = response.css("li.next a::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_product(self, response):
        yield {
            "title": response.css("h1::text").get(),
            "price": response.css(".price_color::text").get(),
            "amount_in_stock": int(
                response.css("p.instock.availability").re(r"\d+")[0]
            ),
            "rating": response.css(
                "p.star-rating::attr(class)"
            ).get().split()[-1],
            "category": response.css(
                "ul.breadcrumb li:nth-child(3) a::text"
            ).get(),
            "description": response.css(
                "#product_description + p::text"
            ).get(),
            "upc": response.css(
                ".table-striped th:contains('UPC') + td::text"
            ).get()
        }
