import scrapy


class RophimMovieScraperSpider(scrapy.Spider):
    name = "rophim_movie_scraper"
    allowed_domains = ["www.rophim.li"]
    start_urls = ["https://www.rophim.li/phim-le"]

    def parse(self, response):
        pass
