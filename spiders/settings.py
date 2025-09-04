# Scrapy settings for this project

BOT_NAME = 'chat_llm_test'

SPIDER_MODULES = ['spiders']
NEWSPIDER_MODULE = 'spiders'

# Obey robots.txt rules
ROBOTS_TXT_OBEY = True

# Configure item pipelines
ITEM_PIPELINES = {
    'pipelines.scrapy_pipeline.ScrapyPipeline': 300,
}

# Configure maximum concurrent requests
CONCURRENT_REQUESTS = 8

# Configure a delay for requests for the same website
DOWNLOAD_DELAY = 1

# Disable cookies
COOKIES_ENABLED = False

# Set default User-Agent
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'