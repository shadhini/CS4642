
# coding: utf-8

# In[1]:


import scrapy


# In[2]:


class CategorizedBizNewsSpider(scrapy.Spider):
    name = "biz_news_categorized" # name of the spider
    
    # returns an iterable of Requests which the Spider will begin to crawl from
    def start_requests(self):
        urls = [
            'http://www.hirunews.lk/business/all-analysis.php',
            'http://www.hirunews.lk/business/all-features.php',
        ]
    
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
        
    # method that will be called to handle response downloaded for each of the requests made
    def parse(self, response):
        for news_item in response.css('div.rp-mian'):
            
            if "http://www.hirunews.lk/business/all-analysis.php" in response.url:
                category = "analysis"
            elif "http://www.hirunews.lk/business/all-features.php" in response.url:
                category = "features"
            else:
                category = "None"
            date = news_item.css('div.time::text').extract_first()
            title = news_item.css('div.lts-cntp a::text').extract_first()
            short_description = news_item.css('div.lts-txt2::text').extract_first()
            views = news_item.css('div.commnet a::text')[2].extract()
            
            yield {
                "date": date,
                "category": category,
                "title": title,
                "short-description": short_description,
                "views": views,
            }
        try:
            next_index = response.css('div.pagi_2 a::attr(title)').extract().index("next page")
            next_page = response.css('div.pagi_2 a::attr(href)')[next_index].extract()

            if next_page is not None:
                yield response.follow(next_page, callback=self.parse)
                
        except ValueError:
            print ("Crawling Finished")

