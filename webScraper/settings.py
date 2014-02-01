# Scrapy settings for webScraper project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

#these lines are useful for the Django integration
import sys
import os


# adding this to the sys.path variable
# and not the PYTHONPATH environment variable
# because as of entering this, we are already
# in the python runtime.
# Path to be changed on server to its final value

PROJECT_DIR = os.path.dirname(__file__)
PROJECT_DIR = PROJECT_DIR.replace('webScraper',"")
sys.path.append(os.path.join(PROJECT_DIR))

os.environ['DJANGO_SETTINGS_MODULE'] = 'octopus.settings'

BOT_NAME = 'webScraper'

RETRY_TIMES = 20

DOWNLOAD_DELAY = 0.2

SPIDER_MODULES = ['webScraper.spiders']

ITEM_PIPELINES = {
    'webScraper.pipelines.TescoPostgresPipeline': 1,
    'webScraper.pipelines.FoodComPostgresPipeline': 2,
    'webScraper.pipelines.AbstractProductProductMatchingPipeline': 3,
}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'webScraper (+http://www.yourdomain.com)'
