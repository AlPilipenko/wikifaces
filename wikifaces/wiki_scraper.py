from bs4 import BeautifulSoup
from datetime import datetime
import requests # access to url page to pull out actual data
import memory_profiler
import json
from wikifaces import exceptions

#== Parameters =======================================================================
mention_filter = 0 # 0 means that word will be added to dict even if mentioned once
exceptions = exceptions.exceptions


#== Functions =======================================================================
def values_extractor(person, url_status):
    """Get wiki contents"""
    if url_status == 'no':
        try:
            name, surname = person.split()
            name = name.capitalize()
            surname = surname.capitalize() if surname[:2] != 'Mc' else surname
            url = 'https://en.wikipedia.org/wiki/' + name+'_'+surname
        except:
            url = 'https://en.wikipedia.org/wiki/' + person.capitalize()
    else:
        url = person

    print("WIKI_SCRAPER | wikipedia url searched for:", url)

    headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'}
    str_table = ""
    page = requests.get(url, headers=headers) # ???
    soup = BeautifulSoup(page.content, 'html.parser') # to pull out individual pieces of information
    table = soup.find(id="bodyContent")

    for e in table:
        str_table += "".join(str(e))

    return str_table


from io import StringIO
from html.parser import HTMLParser
class MLStripper(HTMLParser):
    """Remove all unnecesary HTML tags and symbols"""
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.text = StringIO()
    def handle_data(self, d):
        self.text.write(d)
    def get_data(self):
        return self.text.getvalue()

    def strip_tags(html):
        s = MLStripper()
        s.feed(html)
        return s.get_data()


def dictionary_construct(atable, m_filter):
    word_dict = {}
    """ Adding wiki words and amount of times they were mentioned on page as k,v respectively """
    counter = 0
    for k in atable:
        counter +=1
        if word_dict.get(k) == None and len(k) >= 3 and k.isalpha() == True and k not in exceptions:
            n = atable.count(k)
            if n < m_filter:
                continue
            word_dict[k] = n
    return word_dict, counter


#== Processing =======================================================================
def main(person, url_status):
    print("WIIKISCRAPER",person, url_status)
    """ Scraps person data from wiki and returns dict, where keys are words
        from wiki and values are amount of times keys were mentioned """
    my_table = values_extractor(person, url_status)
    my_table = MLStripper.strip_tags(my_table).split()
    my_table = [w.replace('"', '') for w in my_table] # remove quotes in some words
    word_dict, counter = dictionary_construct(my_table, mention_filter)
    word_dict = {k: v for k, v in sorted(word_dict.items(), key=lambda item: item[1])} # sort by value
    return word_dict
