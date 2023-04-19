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

    def find_path(self, start_page):       
        self.PARAMS['page'] = start_page
        error = 'error' in self.get_page(random=False)  
        start_time = time.time()
        found, visited = self.__bfs_wikipedia(start_page, 'Rome')
        end_time = time.time()  
        total_checked = len(visited) 
        time_passed = round(end_time - start_time)
        return found, total_checked, time_passed, error 
        
                    
    def get_page(self, random):
        params = self.PARAMS
        if random:
            params = self.RAND_PARAMS
        response = requests.get(self.URL, params)
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
                        links = self.get_page(random=False)                                                                     
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
