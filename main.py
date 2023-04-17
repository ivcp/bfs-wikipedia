import requests
from collections import deque
import time

# subject = 'Python (programming language)'
# target= 'Human'


 
# response = requests.get(url, params=params)
# data = response.json()
 
# queue = deque([(subject, [subject])])
# page, path = queue.popleft()

# for link in data['parse']['links']:
#     if not link['ns']:
#         queue.append((link['*'], path + [link['*']]))

url = 'https://en.wikipedia.org/w/api.php'
params = {
        'action': 'parse',        
        'prop': 'links',
        'format': 'json',
        
    }

def bfs_wikipedia(start_page, target_page):
    print(f"finding path from {start_page} to {target_page}")
    visited = set()
    queue = deque([(start_page, [start_page])])
    
    found = []

    while queue and not found:
        page, path = queue.popleft()
        print(f"checking - {page}")
        
        
        if page not in visited:
            visited.add(page)

            if page == target_page:
                found.extend(path)

            else:
                try:
                    params['page'] = page                
                    response = requests.get(url, params=params)
                    data = response.json()                                
                    for link in data['parse']['links']:
                        if not link['ns']:
                            if link['*'] not in visited:
                                if link['*'] == target_page:
                                    queue.appendleft((link['*'], path + [link['*']]))   
                                else: 
                                    queue.append((link['*'], path + [link['*']]))   
                
                except Exception:                
                    pass

          
    return found
            
start = time.time()
print(bfs_wikipedia("Fly", "Canada"))
end = time.time()
print(f"Time elapsed: {round(((end - start)/60), 2)}")

