import requests
from requests.exceptions import RequestException
import bs4
from bs4 import BeautifulSoup
import logging
import time
import json


LOG = logging.getLogger('digicord.crawler')
COURTESY_MS = 2000 # Time in ms between HTTP GET requests


def simple_get(url:str) -> bytes:
    """Perform HTTP GET request at url and check for good response
    Parameters
    ----------
    url: str
        URL to HTTP GET from
    Returns
    -------
    byte:
        Raw content from the request, or None if fail
    Raises
    ------
    RequestException
        If the request does not complete properly
    """
    try:
        LOG.debug(f'Requesting GET to {url}.')
        response = requests.get(url)
        # Only return response content if response is OK
        if (response.status_code == 200):
            return response.content
        raise RequestException(f'Returned {response.status_code}')
    except RequestException as e:
        LOG.error(f'{url}: {str(e)}.')
        return None


def parse_name(row:list) -> str:
    """Parse the Digimon name from a given row
    Parameters
    ----------
    row: list
        Contents of a row from an HTML table
    Returns
    -------
    str:
        Name of the Digimon
    """
    return row[1].a.text


def parse_species_number(row:list) -> int:
    """Parse the Digimon number from a given row
    Parameters
    ----------
    row: list
        Contents of a row from an HTML table
    Returns
    -------
    int:
        Number of the Digimon
    """
    return int(row[0].text)


def parse_stage(row:list) -> str:
    """Parse the Digimon stage from a given row
    Parameters
    ----------
    row: list
        Contents of a row from an HTML table
    Returns
    -------
    str:
        Stage of the Digimon
    """
    return row[2].text


def parse_sprite_url(row:list) -> str:
    """Parse the Digimon sprite URL from a given row
    Parameters
    ----------
    row: list
        Contents of a row from an HTML table
    Returns
    -------
    str:
        URL of Digimon sprite image
    """
    return row[1].img['src']


def parse_page_url(row:list) -> str:
    """Parse the Digimon page URL from a given row
    Parameters
    ----------
    row: list
        Contents of a row from an HTML table
    Returns
    -------
    str:
        URL of Digimon page
    """
    return row[1].a['href']


def parse_field_image(page:BeautifulSoup) -> str:
    """Parse the Digimon field URL from the Digimon specific page
    Parameters
    ----------
    page: BeautifulSoup
        HTML contents of the Digimon page
    Returns
    -------
    str:
        URL of Digimon field image
    """
    return page.table.img['src']


def parse_digivolutions(page:BeautifulSoup) -> dict:
    """Parse the digivolution info from the Digimon specific page
    Parameters
    ----------
    page: BeautifulSoup
        HTML contents of the Digimon page
    Returns
    -------
    str:
        URL of Digimon field image
    """
    tables                  = page.findAll('table')
    digivolutions           = dict()
    digivolutions['from']   = parse_digivolutions_from(tables[1])
    digivolutions['to']     = parse_digivolutions_to(tables[2])
    return digivolutions


def parse_digivolutions_from(table:bs4.element.Tag) -> list:
    """Parse the Digivolves From info from the Digimon specific page
    Parameters
    ----------
    table: bs4.element.Tag
        HTML contents of the Digivolves From table
    Returns
    -------
    list:
        List of Digimon that can evolve into the this Digimon
    """
    from_list   = list()
    if (not check_empty_table(table)):
        row = table.findAll('tr')[1]
        for d in table.findAll('div'):
            from_list.append(d.text)
    return from_list


def parse_digivolutions_to(table:bs4.element.Tag) -> list:
    """Parse the Digivolves Into table from the Digimon specific page
    Parameters
    ----------
    table: bs4.element.Tag
        HTML contents of the Digivolves Into table
    Returns
    -------
    list:
        List of Digimon that this Digimon can evolve into and
        level requirements
    """
    to_list = list()
    if (not check_empty_table(table)):
        # Skip title row
        for row in table.findAll('tr')[1:]:
            digimon = dict()
            row = list(row.children)
            digimon['name']     = row[0].text
            digimon['level']    = list(row[1].children)[1]
            to_list.append(digimon)
    return to_list


def check_empty_table(table:bs4.element.Tag) -> bool:
    """Check if the table is empty (I.e. only contains "N/A")
    Parameters
    ----------
    table: bs4.element.Tag
        HTML contents of the Digivolves table
    Returns
    -------
    bool:
        True if the table is empty, else False
    """
    return table.findAll('td')[1].text == 'N/A'


if __name__ == '__main__':
    """Scrape/crawl from base_url and store info into JSON file
    """
    # Initialize empty database list
    database = []
    logging.basicConfig(level=logging.DEBUG)
    base_url = 'http://digidb.io/digimon-list/'
    LOG.info(f'Starting crawling at {base_url}')
    # Fetch base url content
    base_page = simple_get(base_url)
    if (base_page == None):
        LOG.error(f'Failed to GET from {base_url}')
        exit(1)
    base_page = BeautifulSoup(base_page, 'html.parser')
    # Iterate through rows in the main table
    for row in base_page.tbody.findAll('tr'):
        digimon = dict()
        row = list(row.children)
        # Parse fields from row
        digimon['name']             = parse_name(row)
        digimon['species_number']   = parse_species_number(row)
        digimon['stage']            = parse_stage(row)
        digimon['sprite_url']       = parse_sprite_url(row)
        digimon['page_url']         = parse_page_url(row)
        # Request Digimon specific page after waiting
        time.sleep(COURTESY_MS / 1000)
        digimon_page                = simple_get(digimon['page_url'])
        if (digimon_page == None):
            LOG.error(f'Failed to GET from {page_url}')
            continue
        digimon_page                = BeautifulSoup(digimon_page, 'html.parser')
        digimon['field_url']        = parse_field_image(digimon_page)
        digimon['digivolutions']    = parse_digivolutions(digimon_page)
        database.append(digimon)
    LOG.info('Saving database to JSON')
    with open('database.json', 'w+') as f:
        json.dump(database, f, indent=4)
    LOG.info('Done crawling')

