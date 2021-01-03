# site-downloader

CLI tool to download a specific website for offline viewing. This works best for sites such as
documentation or news articles where pages link to each other with relative paths under same domain and no Javascript.

This project currently is a **Work In Progress**.

## Development

```bash
pip install -r requirements.txt

./main.py # download a site

./tests/server.py # run server at local host
# or
python3 -m http.server --directory <DIR>
```