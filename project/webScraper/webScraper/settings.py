# Scrapy settings for webScraper project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'webScraper'

MONGODB_HOST = 'localhost'
MONGODB_POST = 27017
MONGODB_DATABASE = 'default'
MONGODB_COLLECTION = 'products'

SPIDER_MODULES = ['webScraper.spiders']
NEWSPIDER_MODULE = 'webScraper.spiders'

ITEM_PIPELINES = [
    'scrapy_mongodb.MongoDBPipeline',
]

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'webScraper (+http://www.yourdomain.com)'
