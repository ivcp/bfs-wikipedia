import requests
from collections import deque
import time
from requests.exceptions import HTTPError


class Search:
    URL = 'https://en.wikipedia.org/w/api.php'
    PARAMS = {
            'action': 'parse',        
            'prop': 'links',
            'format': 'json',        
        }
    RAND_PARAMS = {
        'action': 'query',
        'format': 'json',
        'list': 'random',    
        'rnnamespace': 0
    }

    def __init__(self, start_page):
        self.start_page = start_page
        self.PARAMS['page'] = start_page
        self.error = 'error' in self.__get_page(self.PARAMS)  
        self.__start_time = time.time()
        self.found, self.visited = self.__bfs_wikipedia(start_page, 'Rome')
        self.__end_time = time.time()  
        self.total_checked = len(self.visited) 
        self.time_passed = round( self.__end_time - self.__start_time)
        
                

    def __get_page(self, params):
        response = requests.get(self.URL, params=params)
        return response.json()     

    def __bfs_wikipedia(self, start_page, target_page):
        visited = set()
        queue = deque([(start_page, [start_page])])        
        found = []

        while queue and not found:
            page, path = queue.popleft()  
            if page not in visited:
                visited.add(page)
                if page == target_page:
                    found.extend(path)
                else:
                    try:
                        self.PARAMS['page'] = page                
                        links = self.__get_page(self.PARAMS)                                                                     
                        for link in links['parse']['links']:
                            if not link['ns']:
                                if link['*'] not in visited:
                                    if link['*'] == target_page:
                                        queue.appendleft((link['*'], path + [link['*']]))   
                                    else: 
                                        queue.append((link['*'], path + [link['*']]))   
                    except HTTPError as e:                
                        print(e.response.text)                
                    except Exception:
                        pass         
                       
        return found, visited   
