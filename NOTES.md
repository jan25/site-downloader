# Idea

Simple Web crawler to download sites. This should work especiallywell for static web sites such as documentation sites or online books.

# Features

```bash
ds --starturl="https://en.wikipedia.org/wiki/Elon_Musk" --domain="wikipedia.org" --depth=3 --target="musk"


```

## Flags
* `--starturl`
    * Root URL to start downloading web pages
* `--domain`
    * Optional domain condition to only crawl webpages when domain is matched
    * Default is to download all web pages
    * If not supplied replace cross domain pages under same domain?
* `--depth`
    * Optional depth to crawl from starturl
    * Default is 5
* `--target`
    * Optional target directory to put html files
    * Default is .
* `--verbose`
    * Optional Verbose mode to print crawl status to stdout
    * Default is false
    * Print verbose mode in tree format?


## Useful links

* https://stackoverflow.com/a/41654240
