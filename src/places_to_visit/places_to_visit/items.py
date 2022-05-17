# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Field, Item


class PlacesToVisitItem(Item):
    # define the fields for your item here like:
    place_name = Field()
    about = Field()
    suggested_duration = Field()
    breadcrumbs = Field()
    ranking_of_place = Field()
    place_category = Field() 
    area = Field()
    nearby_restraunts = Field()
    nearby_attractions = Field()
    average_reviews = Field()
    total_reviews_count = Field()
    excellent_reviews_count = Field()
    very_good_reviews_count = Field()
    average_reviews_count = Field()
    poor_reviews_count = Field()
    terrible_reviews_count = Field()
    page_url = Field()
    
