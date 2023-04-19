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

    def page_error(self, page):       
        self.PARAMS['page'] = page
        return 'error' in self.get_page(random=False)

          
    def get_page(self, random):
        params = self.PARAMS
        if random:
            params = self.RAND_PARAMS
        response = requests.get(self.URL, params)
        return response.json()     

    def bfs_wikipedia(self, start_page, target_page):
        visited = set()
        queue = deque([(start_page, [start_page])])        
        found = False
        
        while queue and not found:
            page, path = queue.popleft()  
            yield path, visited
            if page not in visited:
                visited.add(page)
                if page == target_page:
                    found = True
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
                       
         
