import requests
from collections import deque
import time
from requests.exceptions import HTTPError




url = 'https://en.wikipedia.org/w/api.php'
params = {
        'action': 'parse',        
        'prop': 'links',
        'format': 'json',        
    }

rand_params = {
    'action': 'query',
    'format': 'json',
    'list': 'random',    
    'rnnamespace': 0
}

def get_page(params):
    response = requests.get(url, params=params)
    return response.json()        


def bfs_wikipedia(start_page, target_page):
    print(f"finding path from {start_page} to {target_page}")
    visited = set()
    queue = deque([(start_page, [start_page])])
    
    found = []

    while queue and not found:
        page, path = queue.popleft()
        #print(f"checking - {page}")
        
        
        if page not in visited:
            visited.add(page)

            if page == target_page:
                found.extend(path)

            else:
                try:
                    params['page'] = page                
                    links = get_page(params)                                                
                    for link in links['parse']['links']:
                        if not link['ns']:
                            if link['*'] not in visited:
                                if link['*'] == target_page:
                                    queue.appendleft((link['*'], path + [link['*']]))   
                                else: 
                                    queue.append((link['*'], path + [link['*']]))   
            
                except HTTPError as e:                
                    print(e.response.text)
               
                except Exception as e:
                    pass

          
    return found



def main():
    start_page = get_page(rand_params)['query']['random'][0]['title']

    start = time.time()
    print(' --> '.join(bfs_wikipedia(start_page, 'Rome')))
    end = time.time()    
    print(f"Time (s): {round(end - start, 2)}")

main()

