from typing import List

import re
import requests
from statistics import mean
from bs4 import BeautifulSoup
from requests.models import Response


def find_model_in_title(model: str):
    return re.compile(r'\b({0})\b'.format(model), flags=re.IGNORECASE).search


def search_camera(model: str):
    prices: List[float] = []
    m = model.replace(" ", "+")
    ebay_url: str = "https://www.ebay.fr/sch/15230/i.html?_from=R40&_nkw=" + m + "&LH_Sold=1&LH_Complete=1&LH_PrefLoc=1"

    try:
        r: Response = requests.get(ebay_url)
        data = r.text
        soup = BeautifulSoup(markup=data, features="html.parser")

        listings = soup.find_all('li', attrs={'class': 's-item'})
        for listing in listings:
            html_el = listing.find('span', attrs={'class': 's-item__price'})

            if str(html_el) != 'None':
                title_html_elt = listing.find('h3', attrs={'class': 's-item__title'})
                title: str = title_html_elt.text
                has_model_in_title = find_model_in_title(model)(title)

                if type(has_model_in_title) is re.Match:
                    html_el = html_el.find('span', attrs={'class': 'POSITIVE'})
                    price: str = html_el.text
                    price = price.replace('EUR', '').strip().replace(',', '.').replace(r'\s+', '')
                    prices.append(float(price))
    except ValueError:
        return {"error": "this method cannot be perform"}

    if len(prices) > 0:
        average_price = round(mean(prices), 2)
        return {"average_price": average_price, "based_on": len(prices)}
    else:
        return {}
