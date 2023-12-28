from html.parser import HTMLParser
from io import StringIO
from urllib.request import urlopen
from urllib.parse import urljoin
from html5lib import parse, treebuilders
from bs4 import BeautifulSoup, SoupStrainer


URLs = ('http://python.org', )


def output(x):
    print("\n".join(sorted(set(x))))


def simpleBS(url, f):
    output(urljoin(url, x['href']) for x in BeautifulSoup(f).findAll('a'))


def fasterBS(url, f):
    output(urljoin(url, x['href']) for x in BeautifulSoup(f, parse_only=SoupStrainer('a')).findAll('a'))


def htmlparser(url, f):
    class AnchorParser(HTMLParser):
        def handle_starttag(self, tag, attrs):
            if tag != 'a':
                return
            if not hasattr(self, 'data'):
                self.data = []
            for attr in attrs:
                if attr[0] == 'href':
                    self.data.append(attr[1])


def process(url, data):
    print('\n*** simple BS')
    simpleBS(url, data)
    # data.seek(0)
    print('\n*** faster BS')
    fasterBS(url, data)
    # data.seek(0)
    print('\n*** HTMLParser')
    htmlparser(url, data)
    # data.seek(0)


def main():
    for url in URLs:
        f = urlopen(url)
        data = f.read()
        f.close()
        process(url, data)


if __name__ == "__main__":
    main()
