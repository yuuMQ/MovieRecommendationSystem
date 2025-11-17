import scrapy


class PhimmoiMovieScraperSpider(scrapy.Spider):
    name = "phimmoi_movie_scraper"
    allowed_domains = ["phimmoi.sale"]
    start_urls = ["https://phimmoi.sale/phim-le?fbclid=IwY2xjawN5eGFleHRuA2FlbQIxMABicmlkETE2V3pKYXJ1MFZ5NXUzSEpzc3J0YwZhcHBfaWQQMjIyMDM5MTc4ODIwMDg5MgABHju6duT57UlhylVlO_o6ZPP57hZR7kPCdFhk4SB9AMXneozaFWv3io-wBxxg_aem_elMQRWf4eW5q4X8zGueqfQ"]

    def parse(self, response):
        pass
