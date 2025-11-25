import scrapy
from debugpy.adapter.sessions import report_sockets
from sympy.physics.units import length
from torch._dynamo import callback


class MoviespiderSpider(scrapy.Spider):
    name = "moviespider"
    allowed_domains = ["phimmoi15.net"]
    start_urls = ["https://phimmoi15.net/phim-le/"]

    def parse(self, response):
        # pass
        movies = response.css('ul.last-film-box li')
        for movie in movies:
            url = movie.css('a.movie-item::attr(href)').get()
            name = movie.css('div.movie-title-1::text').get()
            img = movie.css('div.public-film-item-thumb::attr(data-wpfc-original-src)').get()
            other_name = movie.css('span.movie-title-2::text').get()
            if name:
                name = name.strip()
            if other_name:
                other_name = other_name.strip()
            next_page = response.css('ul.pagination-lg li a::attr(href)').getall()
            if url:
                yield response.follow(url,
                                      callback=self.parse_movie_page,
                                      meta={'img': img,
                                            'name': name,
                                            'other_name': other_name,
                                            'url' : url})
            if next_page:
                next_page_url = next_page[-1]
                yield response.follow(next_page_url, callback=self.parse)

    def parse_movie_page(self, response):
        tags = response.css('div.block-tags::text')[-1].get().strip()
        raw_content = response.css('div#film-content ::text').getall()
        content = [text.strip() for text in raw_content if text.strip()]
        num_of_dl =response.css('dl.movie-dl dd').getall()
        if(len(num_of_dl) == 12):
            year = response.css('dd.movie-dd')[4]
            year = year.css('a::text').get().strip()
            genres = response.css('dd.movie-dd')[9]
            genres = genres.css('a::text').getall()
            rating = response.css('span.imdb::text').get()
            yield {
                'name': response.meta['name'],
                'other_name': response.meta['other_name'],
                'content': content,
                'genres' : genres,
                'rating' : rating,
                'year' : year,
                'img': response.meta['img'],
                'url': response.meta['url'],
                'tags': tags,
            }
        else :
            pass