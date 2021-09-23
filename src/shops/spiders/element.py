from scrapy import Spider
from scrapy.http import XmlRpcRequest
from shops.items import ProductItem


class ElementSpider(Spider):
    name = "element_spider"
    allowed_domains = ["5element.by"]
    start_urls = [
        "https://5element.by/catalog/1383-noutbuki",
        "https://5element.by/catalog/1141-stiralnye-mashiny",
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield XmlRpcRequest(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        for product in response.css("div.spec-product"):
            yield ProductItem(
                name=product.css("a.product-link::attr(data-name)").get(),
                code=product.css("div.product-middle-patio-code::text")
                .get()
                .lstrip("Код: "),
                price=product.css("div.price-block span._price::text").get(),
            )
