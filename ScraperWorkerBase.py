import sys
import urlparse
import urllib
import requests
import bs4
import re
class ScraperWorkerBase(object):
    """
    No needs to learn how is work,
    rewrite parse_page using self.soup(Beautiful), and return result,
    you can get the result by using

        (inpage_urls, your_own_result) urlscraper.execute()

    But this class is default for scraper to use,
    To enhance its function , you can completement this class
    like:

    class MyWorker(ScraperWorkerBase):

        def parse_page(self):
            all_tags = self.soup.find_all('img')
            for i in all_tags:
                print i

    """

    def __init__(self, url=''):
        self.target_url = url
        self.domain = urlparse.urlparse(self.target_url)[1]
        self.domain = self.domain.split('.')
        self.domain = self.domain[1] + "." + self.domain[2]
        # print self.domain
        # exit()
        self.response = None
        self.soup = None

        self.url_in_site = []
        self.url_out_site = []

    """override this method to get html data via any way you want or need"""

    def __get_html_data(self):
        try:
            self.response = requests.get(self.target_url, timeout=5)
            # print "success open it"
        except:
            print "open fail.", self.target_url
            return ""

        print "[-] Got response"
        return self.response.text

    def __get_soup(self):
        text = self.__get_html_data()
        if text == '':
            return []

        return bs4.BeautifulSoup(text, "lxml")

    def __get_all_url(self):
        url_lists = []

        self.soup = self.__get_soup()
        if isinstance(self.soup, type(None)):
            return []

        all_tags = self.soup.findAll("a")
        for a in all_tags:
            try:
                # print a['href']
                url_lists.append(a["href"])
            except:
                pass

        return url_lists

    def get_urls_inpage(self):
        ret_list = self.__get_all_url()

        if ret_list == []:
            return ([], [])
        else:
            for url in ret_list:
                o = urlparse.urlparse(url)

                if self.domain in o[1]:
                    self.url_in_site.append(o.geturl())
                else:
                    self.url_out_site.append(o.geturl())

        inurlset = set(self.url_in_site)

        outurlset = set(self.url_out_site)

        return inurlset, outurlset

    def execute(self):
        inpage_url, undefined_result = self.get_urls_inpage()
        # undefined_result = self.parse_page()

        return inpage_url, undefined_result

    """You can override this method to define your own needs"""

    def parse_page(self):
        pass