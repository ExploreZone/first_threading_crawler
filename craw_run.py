#encoding:utf-8
import sys
import Queue
from Scraper import *
import time
import sys
import urlparse
import bs4
import threading

test_obj = Scraper(single_page=True, workers_num=15)
test_obj.feed(['http://freebuf.com'])
time.sleep(5)

z = test_obj.get_result_urls_queue()

while True:

    try :

        print z.get(timeout=4)

    except:
        print "error"
        break
        
