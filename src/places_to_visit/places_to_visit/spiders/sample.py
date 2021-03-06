import scrapy
from scrapy import Request
from scrapy.crawler import CrawlerProcess
from scrapy.shell import inspect_response
from pprint import pprint
from ..items import PlacesToVisitItem
import pandas as pd
import json

class PlacesToVisit(scrapy.Spider):
    name = "places_to_visit"
    base_url = "https://www.tripadvisor.in"
    country_urls = {
        "africa":"https://www.tripadvisor.in/Attractions-g6-Activities-a_allAttractions.true-Africa.html",
        #"northamerica":"https://www.tripadvisor.in/Attractions-g19-Activities-a_allAttractions.true-North_America.html",
        "northamerica":"https://www.tripadvisor.in/Attractions-g19-Activities-a_allAttractions.true-oa184140-North_America.html"
    }

    def __init__(self, country, from_err=False,*args, **kwargs):
        self.country  = country
        self.error = open("/home/somi/ampba/dcpp/the-art-of-travel/src/places_to_visit/err.json", "a+")
        self.from_err = from_err

    def start_requests(self):
        if not self.from_err:
            page_urls = (f"https://www.tripadvisor.in/Attractions-g19-Activities-a_allAttractions.true-oa{num}-North_America.html" for num in range(184140,337450,30))
            for page_url in page_urls: 
                yield Request(
                    page_url,
                    callback=self.parse,
                    meta= {"page_url": page_url},
                    errback=self.err_handler,
                )
        else :
            errors = []
            with open('/home/somi/ampba/dcpp/the-art-of-travel/src/places_to_visit/err_parse.json') as f:
                for line in f:
                    errors.append(json.loads(line))
            
            for error in errors : 
                yield Request(
                    error["url"],
                    callback=self.parse,
                    meta= {"page_url": error["url"]},
                    errback=self.err_handler,
                )

    def parse(self, response):

        # print page position
        page_position = " ".join(
            response.css(
                "section[data-automation='WebPresentation_PaginationLinksList'] span > :nth-child(2) > div > div::text"
            ).getall()
        )
        self.logger.info(page_position)

        # At a time there should be 30 destinations present in a page
        place_to_visit_cards = [
            x
            for x in response.css(
                "section[data-automation='WebPresentation_SingleFlexCardSection']"
            )
        ]

        for card in place_to_visit_cards:
            card_link = card.css("div.eXwvx > div > a::attr(href)").get()
            yield Request(
                url=f"{self.base_url}{card_link}",
                callback=self.place_page,
                meta={"page_url": f"{self.base_url}{card_link}"},
                errback=self.err_handler,
            )

        # next_page_link = response.css("a[aria-label='Next page']::attr(href)").get()
        # if next_page_link:
        #     yield Request(
        #         url=f"{self.base_url}{next_page_link}",
        #         callback=self.parse,
        #     )

    def place_page(self, response):
        # inspect_response(response, self)

        item = PlacesToVisitItem()

        item["place_name"] = response.css("div.Xewee > h1::text").get()
        if item["place_name"]:
            item["about"] = response.css(
                "div[data-automation='WebPresentation_AttractionAboutSectionGroup'] span > :nth-child(2) div::text"
            ).get()
            item["suggested_duration"] = response.css(
                "div[data-automation='WebPresentation_AttractionAboutSectionGroup'] span > :nth-child(3) > :nth-child(2)::text"
            ).get()

            item["breadcrumbs"] = " > ".join(
                response.css("div[data-automation='breadcrumbs'] div *::text").getall()
            )

            item["ranking_of_place"] = response.css(
                "div.dcksS:nth-child(2) div::text"
            ).get()
            item["place_category"] = response.css(
                "div.dcksS:nth-child(3) *::text"
            ).get()

            item["area"] = response.css(
                "div[data-automation='WebPresentation_PoiLocationSectionGroup'] > div > :nth-child(2) > :nth-child(1) > span button span::text"
            ).get()
            item["nearby_restraunts"] = response.css(
                "div[data-automation='WebPresentation_PoiLocationSectionGroup'] div > :nth-child(2) > :nth-child(3) > :nth-child(1) > :nth-child(3) > div::text"
            ).get()
            item["nearby_attractions"] = response.css(
                "div[data-automation='WebPresentation_PoiLocationSectionGroup'] div > :nth-child(2) > :nth-child(3) > :nth-child(2) > :nth-child(3) > div::text"
            ).get()

            item["average_reviews"] = response.css(
                "section div[id='tab-data-qa-reviews-0'] > div > :nth-child(3) > span > div > :nth-child(1) > :nth-child(1)::text"
            ).get()
            item["total_reviews_count"] = response.css(
                "section div[id='tab-data-qa-reviews-0'] > div > :nth-child(3) > span > div > :nth-child(1) > :nth-child(2) > span::text"
            ).get()
            item["excellent_reviews_count"] = response.css(
                "section div[id='tab-data-qa-reviews-0'] > div > :nth-child(3) > span > div > :nth-child(2) > div > :nth-child(1) > :nth-child(2) > div div div::text"
            ).get()
            item["very_good_reviews_count"] = response.css(
                "section div[id='tab-data-qa-reviews-0'] > div > :nth-child(3) > span > div > :nth-child(2) > div > :nth-child(2) > :nth-child(2) > div div div::text"
            ).get()
            item["average_reviews_count"] = response.css(
                "section div[id='tab-data-qa-reviews-0'] > div > :nth-child(3) > span > div > :nth-child(2) > div > :nth-child(3) > :nth-child(2) > div div div::text"
            ).get()
            item["poor_reviews_count"] = response.css(
                "section div[id='tab-data-qa-reviews-0'] > div > :nth-child(3) > span > div > :nth-child(2) > div > :nth-child(4) > :nth-child(2) > div div div::text"
            ).get()
            item["terrible_reviews_count"] = response.css(
                "section div[id='tab-data-qa-reviews-0'] > div > :nth-child(3) > span > div > :nth-child(2) > div > :nth-child(5) > :nth-child(2) > div div div::text"
            ).get()

        else:
            item["place_name"] = response.css("h1[id='HEADING']::text").get()
            item["about"] = response.css(
                "div[data-component='@ta/attractions.company-profile'] > :nth-child(1) > :nth-child(1) > :nth-child(3) span::text"
            ).get()
            item["suggested_duration"] = ""
            item["breadcrumbs"] = " > ".join(
                [
                    x
                    for x in response.css("ul.breadcrumbs *::text").getall()
                    if x != "\xa0"
                ]
            )
            item["ranking_of_place"] = " ".join(
                response.css(
                    "div[data-component='@ta/attractions.company-profile'] > :nth-child(1) > :nth-child(1) > :nth-child(1) > :nth-child(3) > span *::text"
                ).getall()
            )
            item["place_category"] = " ".join(
                response.css(
                    "div[data-component='@ta/attractions.company-profile'] > :nth-child(1) > :nth-child(1) > :nth-child(1) > :nth-child(4) > span *::text"
                ).getall()
            )
            item["area"] = response.css(
                "span[class='ui_icon map-pin hpRrf'] +::text"
            ).get()
            item["nearby_attractions"] = ""
            item["nearby_restraunts"] = ""
            item["average_reviews"] = ""
            item["total_reviews_count"] = response.css(
                "div[id='REVIEWS'] > div > :nth-child(1) > :nth-child(2) > span::text"
            ).get()
            item["excellent_reviews_count"] = response.css(
                "div[data-test-target='reviews-tab'] > :nth-child(1) > :nth-child(1) > :nth-child(1) > :nth-child(1) ul > :nth-child(1) > span::text"
            ).get()
            item["very_good_reviews_count"] = response.css(
                "div[data-test-target='reviews-tab'] > :nth-child(1) > :nth-child(1) > :nth-child(1) > :nth-child(1) ul > :nth-child(2) > span::text"
            ).get()
            item["average_reviews_count"] = response.css(
                "div[data-test-target='reviews-tab'] > :nth-child(1) > :nth-child(1) > :nth-child(1) > :nth-child(1) ul > :nth-child(3) > span::text"
            ).get()
            item["poor_reviews_count"] = response.css(
                "div[data-test-target='reviews-tab'] > :nth-child(1) > :nth-child(1) > :nth-child(1) > :nth-child(1) ul > :nth-child(4) > span::text"
            ).get()
            item["terrible_reviews_count"] = response.css(
                "div[data-test-target='reviews-tab'] > :nth-child(1) > :nth-child(1) > :nth-child(1) > :nth-child(1) ul > :nth-child(5) > span::text"
            ).get()

        item["page_url"] = response.meta["page_url"]

        yield item

    def err_handler(self, failure):
        err_msg = {
            "url" : failure.request.url,
            "msg" : self.logger.error(repr(failure))
        }
        self.error.write(json.dumps(err_msg) + "\n")
        self.logger.error('Failure type: %s, URL: %s', failure.type,failure.request.url)