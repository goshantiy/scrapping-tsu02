from bs4 import BeautifulSoup
import requests
import re
import queue
import time
def get_wiki_article_links(url):
    links = []
    try:
        response = requests.get(url,timeout=2)
        soup = BeautifulSoup(response.content,"html.parser")
        body = soup.find(id="bodyContent")
       
        for url in body.find_all('a', href = True):
            href = url['href']
            if re.match(r"^.*/wiki/(?!.*\.jpg$).*", href):
                    links.append("https://en.wikipedia.org"+href)
    except requests.exceptions.RequestException:
        print("timeout")
    return links

def find_paths(url1, url2, depth_limit):
    q = queue.Queue() 
    q.put((url1, [url1]))  
    while not q.empty():
        current_url, path = q.get() 
        current_depth = len(path) - 1
        if current_depth >= depth_limit:
            continue
        print("depth:",current_depth, path)
        links = get_wiki_article_links(current_url)
        if links:
            for link in links:
                if(url2==link):
                    return path + [link]
                q.put((link, path + [link])) 

# url1 = 'https://en.wikipedia.org/wiki/Six_degrees_of_separation'
# url2 = 'https://en.wikipedia.org/wiki/American_Broadcasting_Company'
url1 = 'https://en.wikipedia.org/wiki/Six_degrees_of_separation'
url2 = 'https://en.wikipedia.org/wiki/Blue_Network'
depth_limit = 5
start_time = time.time()

path = find_paths(url1, url2, depth_limit)

if path:
    print("--- seconds ---",(time.time() - start_time))
else:
    print('no path')
