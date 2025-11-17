import scrapy

'''
dataset: Name - Other Name - Description - Year - Rating score - Number of Rating - Image
'''
class AnimeMovieScraperSpider(scrapy.Spider):
    name = "anime_movie_scraper"
    allowed_domains = ["animehay.life"]
    start_urls = ["https://animehay.life/"]

    def parse(self, response):
        anime_films = response.css('div.movie-item')

        for anime in anime_films:
            film_url = anime.css('a::attr(href)')[-1].get()
            if film_url:
                yield scrapy.Request(url=film_url, callback=self.parse_anime_details)

        next_page = response.css('div.pagination a.active_page + a::attr(href)').get()
        # selector "a.active_page + a" = thẻ <a> ngay sau thẻ đang active
        if next_page:
            yield response.follow(next_page, callback=self.parse)


    def parse_anime_details(self, response):
        anime_details = response.css('div.info-movie')

        # Ten Phim
        ten_phim = anime_details.css('h1.heading_movie::text').get().strip()

        # Format Ten Khac
        ten_khac_list = anime_details.css('div.last div.name_other div::text').getall()
        if len(ten_khac_list) > 1:
            ten_khac = ten_khac_list[-1].strip()
        else:
            ten_khac = ''

        # Format Noi Dung
        # Noi dung tren div va tren p
        noi_dung_list = anime_details.css('div.desc.ah-frame-bg div::text, div.desc.ah-frame-bg p::text').getall()

        for i in range(len(noi_dung_list)):
            noi_dung_list[i] = noi_dung_list[i].strip()
        noi_dung = ' '.join(noi_dung_list).strip()

        # Format The Loai
        the_loai_list = anime_details.css('div.list_cate a::text').getall()
        for i in range(len(the_loai_list)):
            the_loai_list[i] = the_loai_list[i].strip()
            if the_loai_list[i] == 'CN Animation':
                return
        # Rating va Danh Gia
        rating_score = anime_details.css('div.score div::text')[1].get().strip()
        rating, danh_gia_string = float(rating_score.split('||')[0]), rating_score.split('||')[1]
        danh_gia = int(danh_gia_string.split()[0])

        # Nam Phat Hanh
        nam_phat_hanh =  int(anime_details.css('div.update_time div ::text')[1].get().strip())

        # Hinh cua phim
        image = anime_details.css('div.first img::attr(src)').get()
        yield{
            'Tên Phim': ten_phim,
            'Tên Khác': ten_khac,
            'Nội Dung': noi_dung,
            'Thể Loại': the_loai_list,
            'Rating': rating,
            'Số lượng đánh giá': danh_gia,
            'Năm Phát Hành': nam_phat_hanh,
            'Image': image,
        }
