from scrapy import Spider
from scrapy.http import XmlRpcRequest

from shops.items import ProductItem


class VekSpider(Spider):
    name = "vek_spider"
    allowed_domains = ["www.21vek.by"]
    start_urls = ["https://www.21vek.by/notebooks", "https://www.21vek.by/tv"]

    def start_requests(self):
        for url in self.start_urls:
            yield XmlRpcRequest(
                url=url, callback=self.parse_pages, cb_kwargs={"url": url}
            )

    def parse_pages(self, response, **kwargs):
        max_page = int(
            response.xpath("//div[@id='j-paginator']//a[last()-1]/@name").get()
        )
        for page in range(1, max_page):
            yield XmlRpcRequest(url=f"{kwargs['url']}/page:{page}", callback=self.parse)

    def parse(self, response, **kwargs):
        for product in response.xpath("//ul[@class='b-result']/li"):
            price = product.css("span.g-item-data::attr(content)").get()
            if price:
                yield ProductItem(
                    name=product.css("span.result__name::text").get(),
                    code=product.css("span.g-code::text").get().lstrip("код "),
                    price=price,
                )
