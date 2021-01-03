import logging
import os
from bs4 import BeautifulSoup
from urllib.parse import urljoin, quote, urlparse
import requests

def get_path(url):
    '''
    Gets path from the URL.
    '''
    parsed = urlparse(url)
    return parsed.path

def find_and_save(session, target_dir, base_url, soup, tag='img', inner='src'):
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    for res in soup.findAll(tag):
        if not res.has_attr(inner): continue

        try:
            filename = os.path.basename(res.get(inner))
            fileurl = urljoin(base_url, res.get(inner))
            filepath = os.path.join(target_dir, get_path(filename))
            res[inner] = os.path.join(os.path.basename(target_dir), get_path(filename))
            logging.info(f'Downloading {filepath} from {fileurl}')
            with open(filepath, 'wb') as f:
                filebin = session.get(fileurl)
                f.write(filebin.content)
        except Exception as e:
            logging.error("Failed to save asset %r" % e)
    
    return soup

def save_page(html_str, base_url, target_dir):
    soup = BeautifulSoup(html_str)
    with requests.Session() as session:
        soup = find_and_save(session, target_dir, base_url, soup, 'img', inner='src')
        soup = find_and_save(session, target_dir, base_url, soup, 'link', inner='href')
        soup = find_and_save(session, target_dir, base_url, soup, 'script', inner='src')    

    filepath = os.path.join(target_dir, 'index.html')
    with open(filepath, 'w') as f:
        f.write(soup.prettify())

def download(html, base_url, path, target_dir):
    '''
    html: request_html.HTML object

    Downloads html and references css, img files.
    '''
    logging.debug(f"Downloading to {target_dir}")

    final_target_dir = f'{target_dir}{path}' # path contains / as first char if exists
    save_page(html.html, base_url, final_target_dir)