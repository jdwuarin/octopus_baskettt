import os
from scrapy.utils.project import ENVVAR

#this is used for Scrapy in order to use proper settings
# if ENVVAR not already in os.environ
os.environ[ENVVAR] = 'octopus_basket.settings'
