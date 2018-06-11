import threading
import Queue
from ScraperWorkerBase import *
class Scraper(object):
    def __init__(self, single_page=True, workers_num=8, worker_class=ScraperWorkerBase):
        self.count = 0
        self.workers_num = workers_num
        """get worker_class"""
        self.worker_class = worker_class
        """check if the workers should die"""
        self.all_dead = False
        """store the visited pages"""
        self.visited = set()
        """by ScraperWorkerBase 's extension result queue"""
        self.result_urls_queue = Queue.Queue()
        self.result_elements_queue = Queue.Queue()
        """

        if single_page == True, 

        the task_queue should store the tasks (unhandled)

        """
        self.task_queue = Queue.Queue()
        self.single_page = single_page
        if self.single_page == False:

            self.__init_workers()

        else:

            self.__init_single_worker()

    def __check_single_page(self):

        if self.single_page == True:
            raise StandardError('[!] Single page won\'t allow you use many workers')

    """init worker(s)"""

    def __init_single_worker(self):

        ret = threading.Thread(target=self._single_worker)

        ret.start()

    def __init_workers(self):

        self.__check_single_page()

        for a in range(self.workers_num):
            ret = threading.Thread(target=self._worker)

            ret.start()

    """return results"""

    def get_result_urls_queue(self):

        return self.result_urls_queue

    def get_result_elements_queue(self):

        return self.result_elements_queue

    """woker function"""

    def _single_worker(self):

        if self.all_dead != False:
            self.all_dead = False

        scraper = None

        while not self.all_dead:

            try:

                url = self.task_queue.get(block=True)

                print 'Workding', url
                try:
                    if url in self.visited:
                        continue
                except:
                    pass
                if url in self.visited:
                    continue
                else:
                    pass
                self.count = self.count + 1
                print 'Having process', self.count, 'Pages'
                scraper = self.worker_class(url)
                self.visited.add(url)
                urlset, result_entity = scraper.execute()
                for i in urlset:
                    # self.task_queue.put(i)
                    self.result_urls_queue.put(i)
                if result_entity != None:
                    pass
                else:
                    self.result_elements_queue.put(result_entity)
            except:
                break
            finally:
                break
    def _worker(self):
        if self.all_dead != False:
            self.all_dead = False
        scraper = None
        while not self.all_dead:
            try:
                if self.count != 0:
                    if self.task_queue.qsize() == 0:
                        break

                url = self.task_queue.get(block=True)
                try:
                    if url in self.visited:
                        continue
                except:
                    pass
                print "Workding", url
                self.count = self.count + 1
                print 'Having process', self.count, 'Pages'
                scraper = self.worker_class(url)
                self.visited.add(url)
                urlset, result_entity = scraper.execute()
                for i in urlset:
                    if i in self.visited:
                        continue
                    else:
                        pass
                    self.task_queue.put(i)
                    self.result_urls_queue.put(i)
                # print "end"
                if self.task_queue.qsize() == 0:
                    self.kill_workers()
                if result_entity != None:
                    pass
                else:
                    self.result_elements_queue.put(result_entity)
            except:
                break
            # finally:
            #     pass
    """scraper interface"""
    def kill_workers(self):
        if self.all_dead == False:
            self.all_dead = True
        else:
            pass
    def feed(self, target_urls=[]):
        if isinstance(target_urls, list):
            for target_url in target_urls:
                self.task_queue.put(target_url)
        elif isinstance(target_urls, str):
            self.task_queue.put(target_urls)
        else:
            pass
        # return url result
        return (self.get_result_urls_queue(), self.get_result_elements_queue())