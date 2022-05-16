### Introduction

**Motivation** : We will take africa as an entity and try to scrape all the `Places to visit` within there.

**Procedure** : 
1. Go to https://www.tripadvisor.in/Attractions-g6-Activities-a_allAttractions.true-Africa.html , this is a consolidate list for all the places to visit in Africa. Pagination should be adopted as the list is as big as 43758 entities with each page being consisting of 30 entities
2. For every `Place to visit` entity page, there are various information that could be broken down into following structured manner : 
   1. Name
   2. Total Number of ratings followed by number of Ratings in: 
      1. Excellent
      2. Very Good
      3. Average
      4. Poor
      5. Teribble
   3. Reviews i.e., 4.5 out of 5
   4. Ranking to do in a specific city , #1 of 50 to do in Egypt
   5. Categoty for Type of Attraction/Place , i.e. Religious Site, Garden etc
   6. About : content / description about place
   7. Suggested Duration
   8. Breadcrumbs for Geographic Location
   9. The Area : Comprises of address to the location / Locality
   10. Nmber Best Nearby Restraunts
   11. Number of best Nearby Attractions