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
sys.path.append('/Users/john-davidwuarin/Dropbox/Workspace_Python/octopus')

os.environ['DJANGO_SETTINGS_MODULE'] = 'octopus.settings'

BOT_NAME = 'webScraper'

SPIDER_MODULES = ['webScraper.spiders']
NEWSPIDER_MODULE = 'webScraper.spiders'

ITEM_PIPELINES = [
    'webScraper.pipelines.Tesco_postgres_pipeline',
    'webScraper.pipelines.all_recipes_postgres_pipeline',
]

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'webScraper (+http://www.yourdomain.com)'
