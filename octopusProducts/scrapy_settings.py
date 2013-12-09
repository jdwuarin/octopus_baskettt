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
PROJECT_DIR = PROJECT_DIR.replace('webScraper/webScraper',"")
sys.path.append(os.path.join(PROJECT_DIR))

os.environ['DJANGO_SETTINGS_MODULE'] = 'octopus.settings'

BOT_NAME = 'webScraper'

SPIDER_MODULES = ['webScraper.webScraper.spiders.tesco_basket_spider']

ITEM_PIPELINES = {
    'webScraper.webScraper.pipelines.Tesco_postgres_pipeline' : 1, 
    'webScraper.webScraper.pipelines.All_recipes_postgres_pipeline' : 2 ,
    'webScraper.webScraper.pipelines.Ingredient_produt_matching_pipeline' : 3,
    'webScraper.webScraper.pipelines.Tesco_basket_porting_pipeline' : 4,
}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'webScraper (+http://www.yourdomain.com)'
