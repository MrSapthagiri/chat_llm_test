import scrapy

class ExampleSpider(scrapy.Spider):
    """
    Example spider to demonstrate how to use the scrapy pipeline for data storage.
    This spider scrapes quotes from quotes.toscrape.com.
    """
    name = 'example_quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']
    
    def parse(self, response):
        """
        Parse the response and extract quotes.
        
        Args:
            response: The response object
            
        Yields:
            dict: Extracted quote data
        """
        # Extract quotes from the page
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('small.author::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall(),
                'url': response.url
            }
        
        # Follow pagination links
        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)