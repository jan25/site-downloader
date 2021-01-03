#!/usr/bin/env python3
import logging
from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED, ALL_COMPLETED
from requests_html import HTMLSession
import os
from queue import Queue, Empty
from urllib.parse import urlparse, urlunsplit, urljoin
from files import download


logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)

# TODO: Convert these to named args from cli
START_URL = "https://en.wikipedia.org/wiki/Elon_Musk"
DEPTH = 2
TARGET_DIR = "./musk"
VERBOSE = True
QUEUE_TIMEOUT = 10 # seconds

q = Queue()
session = HTMLSession()

class Link:
    def __init__(self, url, depth=0):
        self.url = url
        self.depth = depth
        self.html = None # HTML Object

    def set_html(self, html):
        self.html = html

def sanitise_url(url):
    '''
    Remove query and fragment parts from the URL.
    '''
    parsed = urlparse(url)
    return urlunsplit((parsed.scheme, parsed.netloc, parsed.path, '', ''))

def get_base_url(url):
    '''
    Gets base form of the URL.
    '''
    parsed = urlparse(url)
    return urlunsplit((parsed.scheme, parsed.netloc, '', '', ''))

def get_path(url):
    '''
    Gets path from the URL.
    '''
    parsed = urlparse(url)
    return parsed.path

def fetch(link):
    url, depth = link.url, link.depth
    if depth == DEPTH:
        return

    print(f'fetching {url} at depth {depth}')
    try:
        r = session.get(url)
        content_type = r.headers.get('Content-Type')
        if 'html' not in content_type: return

        link.set_html(r.html)
    except Exception as e:
        # TODO Add logging
        raise Exception("fetch for %s something went wrong %r", url, e)

    handle_post_fetch(link)

def handle_post_fetch(link):
    print(f'Handling post fetch', link.url)
    base_url = get_base_url(link.url)

    try:
        download(link.html, base_url, get_path(link.url), TARGET_DIR)
    except Exception as e:
        raise Exception("Failed to download site %r", e)

    try:

        for url in link.html.links:
            sanitised_url = sanitise_url(url)
            if get_base_url(sanitised_url) not in {'', base_url}: continue
            
            parsed = urlparse(sanitised_url)
            if not parsed.netloc:
                assert parsed.scheme == ''
                sanitised_url = urljoin(base_url, sanitised_url)
            
            print(f'Adding {sanitised_url} to queue')
            q.put(Link(sanitised_url, link.depth + 1))
    except Exception as e:
        raise Exception("Handling post fetch failed %r", e)

def main():
    q.put(Link(sanitise_url(START_URL)))

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = set()
        chunk_size = 10

        # TODO: Prove correctness of this
        while True:
            try:
                for _ in range(chunk_size):
                    link = q.get(timeout=QUEUE_TIMEOUT)
                    futures.add(executor.submit(fetch, link))

                done, _ = wait(futures, timeout=0.5, return_when=FIRST_COMPLETED)

                for future in done:
                    futures.remove(future)

            except Empty as e:
                print('empty queue after waiting')
                break
            except Exception as e:
                print('unexpected exception %r', e)

        try:
            wait(futures, return_when=ALL_COMPLETED)
        except Exception as e:
            print('waiting on futures to finish failed %r', e)


if __name__ == '__main__':
    main()
