from bs4 import BeautifulSoup
import requests
import re
import queue
def get_wiki_article_links(url):
    try:
        response = requests.get(url,timeout=2)
        soup = BeautifulSoup(response.content,"html.parser")
        body = soup.find(id="bodyContent")
        links = []
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

    paths = []
    linknum = 0
    while not q.empty():
        current_url, path = q.get() 
        current_depth = len(path) - 1
        if current_url == url2:
            paths.append(path)
            break 
        if current_depth >= depth_limit:
            continue
        print("depth:",current_depth, path)
        print('\033[1A', end='\x1b[2K')
        links = get_wiki_article_links(current_url)
        for link in links:
            if link == url2:
                paths.append(path + [link])
                return paths
            else:
                q.put((link, path + [link])) 


url1 = 'https://en.wikipedia.org/wiki/Six_degrees_of_separation'
url2 = 'https://en.wikipedia.org/wiki/American_Broadcasting_Company'
depth_limit = 5

paths = find_paths(url1, url2, depth_limit)

if paths:
    for path in paths:
        print(' => '.join(path))
else:
    print('no path')
