"""
Helper functions for handling external links.

External links are links to member station coverage of books.  They are
submitted via a Google Form, such as this one, from the 2017 edition of
the Concierge:
https://docs.google.com/forms/d/11VfB7WeBIg1YQKNzfVzbU5rae53PJ02d4Xm4e9yIajA/edit

"""

import csv
from HTMLParser import HTMLParser
import json
import logging
import os
import sys

from csvkit.py2 import CSVKitDictReader, CSVKitDictWriter
import requests
from requests.exceptions import RequestException

import app_config


logging.basicConfig(format=app_config.LOG_FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel(app_config.LOG_LEVEL)


# Configure some default values.  This is mostly to keep line lengths
# down when specifying these values as defaults for function arguments.
DEFAULT_BOOKS_CSV = os.path.join('data', 'books.csv')
DEFAULT_EXTERNAL_LINKS_CSV = os.path.join('data', 'external_links.csv')
DEFAULT_EXTERNAL_LINKS_OUTPUT_CSV = os.path.join('data',
    'external_links_to_merge.csv')
DEFAULT_EXTERNAL_LINKS_JSON = os.path.join('data',
    'external_links_by_isbn.json')
DEFAULT_ISBN_KEY = app_config.EXTERNAL_LINKS_COLUMNS['isbn']
DEFAULT_STATION_KEY = app_config.EXTERNAL_LINKS_COLUMNS['station_name']
DEFAULT_URL_KEY = app_config.EXTERNAL_LINKS_COLUMNS['url']


def get_external_links_csv(output_path=DEFAULT_EXTERNAL_LINKS_CSV):
    """
    Download CSV for links to coverage of books from member stations.

    Note that the first worksheet of the spreadsheet tied to the Google Form
    needs to be published to the web as CSV in order for this to work.

    """
    csv_url = ('https://docs.google.com/spreadsheets/d/e/%s/pub'
               '?output=csv') % (
                   app_config.EXTERNAL_LINKS_GOOGLE_DOC_KEY)
    r = requests.get(csv_url)
    if r.headers['content-type'] != 'text/csv':
        logger.error(('Unexpected Content-type: %s. Are you sure the '
                      'spreadsheet is published as csv?') %
                     r.headers['content-type'])
        sys.exit(1)

    with open(output_path, 'wb') as writefile:
        writefile.write(r.content)


class TitleHTMLParser(HTMLParser):
    """
    Simple HTML parser that just gets the title.

    After parsing the HTML, the document's title will be available as a
    `title` attribute of the parser object.

    This isn't how I would usually parse HTML, but I didn't want to add a
    dependency just to get the titles.

    """
    def feed(self, data):
        self._in_title = False
        # This is an old-style class, so we can't call `super()`
        HTMLParser.feed(self, data)

    def handle_starttag(self, tag, attrs):
        if tag != 'title':
            self._in_title = False
            return

        self.title = ""
        self._in_title = True

    def handle_endtag(self, tag):
        self._in_title = False

    def handle_data(self, data):
        if self._in_title:
            self.title += data


def get_link_title(url):
    """
    Returns the title of a remote HTML document.

    Args:
        url (str): URL of HTML document.

    Returns:
        str: Title from HTML document's `<title>` tag.

    """
    r = requests.get(url)
    parser = TitleHTMLParser()
    parser.feed(r.text)
    return parser.title


def get_link_html(url, station_name):
    """
    Returns HTML for a link for member station content.

    Args:
        url (str): URL of station coverage of a book.
        station_name (str): Name of station.

    Returns:
        str: String containing HTML linking to the content.

    """
    return '<a href="%s">%s: %s</a>' % (
            url,
            station_name,
            get_link_title(url)
        )


def parse_external_links_csv(csv_path=DEFAULT_EXTERNAL_LINKS_CSV,
                             json_path=DEFAULT_EXTERNAL_LINKS_JSON,
                             isbn_key=DEFAULT_ISBN_KEY,
                             station_key=DEFAULT_STATION_KEY,
                             url_key=DEFAULT_URL_KEY):
    """
    Convert external links CSV to a JSON lookup table.

    Convert external links CSV of a JSON lookup table that goes from ISBN
    to HTML links.  This can then be joined with the book data.

    Args:
        csv_path (str): Path to input CSV file.
        json_path (str): Path to output JSON file.
        isbn_key (str): Column name in the CSV data for the column that
            contains the book's ISBN.
        station_key (str): Column name in the CSV data for the column that
            contains the book's station.
        url_key (str): Column name in the CSV data for the column that
            contains the URL to the member station coverage.

    """
    external_links_by_isbn = {}

    with open(csv_path) as f:
        reader = csv.DictReader(f)

        for row in reader:
            isbn = row[isbn_key]
            # TODO: Ignore rows where flag is not set
            if not isbn:
                continue

            url = row[url_key]
            station_name = row[station_key]

            try:
                link_html = get_link_html(url, station_name)
            except RequestException:
                continue
            links = external_links_by_isbn.setdefault(isbn, [])
            links.append(link_html)

        with open(json_path, 'wb') as writefile:
            writefile.write(json.dumps(external_links_by_isbn))


def lookup_links_by_isbn(isbn, lookup):
    """
    Retrieve links for a book by ISBN.

    Allow a little flexibility with the ISBN format.

    Args:
        isbn (str): ISBN code for a book.
        lookup (dict): Lookup table where keys are ISBNs and values are lists
            of HTML links.

    """
    try:
        return lookup[isbn]
    except KeyError:
        try:
            return lookup[isbn.lstrip('0')]
        except KeyError:
            pass

    raise KeyError("ISBN %s not found" % (isbn))


def merge_external_links(books_csv_path=DEFAULT_BOOKS_CSV,
                         links_json_path=DEFAULT_EXTERNAL_LINKS_JSON,
                         output_csv_path=DEFAULT_EXTERNAL_LINKS_OUTPUT_CSV):
    """
    Create a CSV file containing external links.

    Create a CSV file containing external links that can be copied into the
    books Google Spreadsheet.

    Args:
        books_csv_path (str): Path to CSV file containing data from the books
            Google Spreadsheet.
        links_json_path (str): Path to JSON file created by
            `parse_external_links_csv()`.
        output_csv_path (str): Path to output CSV file.

    """
    fieldnames = [
        # Only include enough fields to identify the book
        'title',
        'isbn',
        'external_links_html',
    ]
    with open(links_json_path) as jsonf:
        lookup = json.load(jsonf)
        matched = set()

        with open(books_csv_path) as readfile:
            reader = CSVKitDictReader(readfile, encoding='utf-8')
            reader.fieldnames = [name.strip().lower()
                                 for name in reader.fieldnames]

            with open(output_csv_path, 'wb') as fout:
                writer = CSVKitDictWriter(fout, fieldnames=fieldnames)
                writer.writeheader()

                for book in reader:
                    output_book = {
                        'title': book['title'],
                        'isbn': book['isbn'],
                        'external_links_html': '',
                    }

                    if book['isbn']:
                        try:
                            links = lookup_links_by_isbn(book['isbn'], lookup)
                            output_book['external_links_html'] = ','.join(links)
                            matched.add(book['isbn'])
                        except KeyError:
                            # No matching member station coverage.  This is OK.
                            pass

                    writer.writerow(output_book)

            # Do an audit to see if there are any ISBNs in the member station
            # responses that didn't match books.
            for isbn in lookup:
                if isbn not in matched:
                    logger.warn("No matching book found for ISBN %s" % (isbn))
