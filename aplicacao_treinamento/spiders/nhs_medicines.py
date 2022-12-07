import scrapy

class NhsMedicinesSpider(scrapy.Spider):

    name = 'nhs_medicines'
    allowed_domains = ['www.nhs.uk']
    start_urls = ['https://www.nhs.uk/medicines/']

    def parse(self, response):
        medicines = response.xpath('//article//div/ul/li/a')

        for medicine in medicines:
            medicine_name = " ".join(medicine.xpath('.//text()').get().split())
            url = medicine.xpath('.//@href').get()

            yield response.follow(url=url, callback=self.parse_medicine, meta={'medicine':medicine_name})

    def parse_medicine(self, response):
        article = response.xpath('//article')
        links = article.xpath('.//ul[@class="nhsuk-hub-key-links beta-hub-key-links"]')
        about_section = article.xpath('.//section[starts-with(@id,"about")]')

        about = ""
        key_facts = ""
        who_can_take = ""
        how_to_take = ""
        side_effects = ""
        how_to_cope = ""
        pregnancy = ""
        cautions = ""

        if(links):
            about_url = links.xpath('.//a[contains(@href,"about")]/@href').get()
            who_can_take_url = links.xpath('.//a[contains(@href,"who-can-and-cannot")]/@href').get()
            how_to_take_url = links.xpath('.//a[contains(@href,"how-and-when")]/@href').get()
            side_effects_url = links.xpath('.//a[contains(@href,"side-effects")]/@href').get()
            pregnancy_url = links.xpath('.//a[contains(@href,"pregnancy")]/@href').get()
            cautions_url = links.xpath('.//a[contains(@href,"other-medicines")]/@href').get()

            if(about_url != None):
                response.follow(url=about_url)
                article = response.xpath('//article')
                about = " ".join(article.xpath('.//section[1]//text()').getall())
                key_facts = " ".join(article.xpath(
                    './/section//section//h2[contains(text(),"Key facts")]/../ul//text()')
                                     .getall())

            if (who_can_take_url != None):
                response.follow(url=who_can_take_url)
                article = response.xpath('//article')
                who_can_take = " ".join(article.xpath('.//section//text()').getall())

            if (how_to_take_url != None):
                response.follow(url=how_to_take_url)
                article = response.xpath('//article')
                how_to_take = " ".join(article.xpath('.//section//text()').getall())

            if (side_effects_url != None):
                response.follow(url=side_effects_url)
                article = response.xpath('//article')
                side_effects = " ".join(article.xpath('.//section//text()').getall())

            if (pregnancy_url != None):
                response.follow(url=pregnancy_url)
                article = response.xpath('//article')
                pregnancy = " ".join(article.xpath('.//section//text()').getall())

            if (cautions_url != None):
                response.follow(url=cautions_url)
                article = response.xpath('//article')
                cautions = " ".join(article.xpath('.//section//text()').getall())

        elif(about_section):
            about = " ".join(article.xpath(
                './/section[starts-with(@id,"about")]//div//text()')
                             .getall())
            key_facts = " ".join(article.xpath(
                './/section[starts-with(@id,"key-facts")]//div//text()')
                                 .getall())
            who_can_take = " ".join(article.xpath(
                './/section[starts-with(@id,"who-can-and-cannot")]//div//text()')
                                    .getall())
            how_to_take = " ".join(article.xpath(
                './/section[starts-with(@id,"how-and-when")]//div//text()')
                                   .getall())
            side_effects = " ".join(article.xpath(
                './/section[starts-with(@id,"side-effects")]//div//text()')
                                    .getall())
            how_to_cope = " ".join(article.xpath(
                './/section[starts-with(@id,"how-to-cope")]//div//text()')
                                   .getall())
            pregnancy = " ".join(article.xpath(
                './/section[contains(@id,"pregnancy")]//div//text()')
                                 .getall())
            cautions = " ".join(article.xpath(
                './/section[contains(@id,"other-medicines")]//div//text()')
                                .getall())

        else:
            article = response.xpath('//article')
            about = " ".join(article.xpath('.//section//text()').getall())

        yield {
            'name': response.meta.get('medicine'),
            'about': " ".join(about.split()),
            'key_facts': " ".join(key_facts.split()),
            'who_can_take': " ".join(who_can_take.split()),
            'how_to_take': " ".join(how_to_take.split()),
            'side_effects': " ".join(side_effects.split()),
            'how_to_cope': " ".join(how_to_cope.split()),
            'pregnancy': " ".join(pregnancy.split()),
            'cautions': " ".join(cautions.split())
        }
