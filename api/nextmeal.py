import requests, json, mechanize, httplib, urllib2
from bs4 import BeautifulSoup

def get_next_meal(username, password):
    """Get menu for next meal from Go Gordon"""

    url = 'https://go.gordon.edu/departments/dining'

    # Initialize browser
    browser = mechanize.Browser()
    browser.set_handle_robots(False)

    # Add page authentication
    browser.add_password(url, username, password)

    # Get page
    try:
        browser.open(url)
    except urllib2.HTTPError as err:
        if err.code == httplib.UNAUTHORIZED:
            raise ValueError("Username and password do not match.",
                httplib.UNAUTHORIZED)
        else:
            raise ValueError("HTTPError: Next meal is unavailable.",
                httplib.INTERNAL_SERVER_ERROR)

    except Exception as err:
        raise ValueError("Next meal is unavailable.",
            httplib.INTERNAL_SERVER_ERROR)
    else:
        page = BeautifulSoup(browser.response().read())

        next_meal = page           \
            .find_all('table')[-1] \
            .find_all('tr')[-1]    \
            .find_all('td')[-1]    \
            .text

        # Remove extraneous whitespace
        next_meal = next_meal    \
            .strip()             \
            .replace('\n\r', '')

        return { 'data': next_meal }
