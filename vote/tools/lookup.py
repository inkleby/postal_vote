# -*- coding: utf-8 -*-

'''
Wikipedia communication functions
'''
import requests
import wikipedia
from Levenshtein import jaro_winkler

wikipedia.set_rate_limiting(True)


def get_images_from_url(url):
    
    title = url.split("/")[-1]
    try:
        page = wikipedia.page(title)
        images = page.images
    except (wikipedia.exceptions.PageError,requests.exceptions.ConnectionError):
        return ""
    
    images = [x for x in images if "Commons-logo.svg" not in x]
    if images:
        return images[0]
    else:
        return ""

def get_description(search_for,exclude=None,important=None):
    """
    gets the description of the object
    """
    print "wiking"
    if type(search_for) == str:
        search_for = unicode(search_for,errors="ignore")

    try:
        options = wikipedia.search(search_for)
    except requests.exceptions.ConnectionError:
        return None, None
    
    if not options:
        return None, None
    options.sort(key=lambda x: word_match(search_for,x),reverse=True)
    
    if options[0] == exclude: #stop returning 'moon' when we want something on the moon
        options.pop(0)
    
    if len(options) == 0:
        return None, None
    
    if important:
        if important.lower() not in options[0].lower():
            return None,None
        
    o = options[0]
    if jaro_winkler(o,search_for) == 0:
        return None, None
    
    try:
        url = wikipedia.page(options[0]).url
        summary = wikipedia.summary(options[0],sentences=5)
        return url, summary
    except (wikipedia.DisambiguationError, wikipedia.exceptions.PageError):
        return None, None

def word_match(a,b):
    """
    how many words in common between two phrases?
    similarity test
    (would be improved by a keying function)
    """
    bad_words = set(["of","and","in"])
    al = a.replace("("," ").replace(")"," ").replace('"'," ").lower()
    bl = b.replace("("," ").replace(")"," ").replace('"'," ").lower()
    a_words = set(al.split(" ")).difference(bad_words)
    b_words = set(bl.split(" ")).difference(bad_words)
    return len(a_words.intersection(b_words))


def find_wiki_page(search_for):
    """
    returns a wikipedia page object for a given search
    """
    if type(search_for) == str:
        search_for = unicode(search_for,errors="ignore")

    
    options = wikipedia.search(search_for)[:-2]
    
    if not options:
        return None
    options.sort(key=lambda x: word_match(search_for,x),reverse=True)
    try:
        page = wikipedia.page(options[0])
        return page.url
    except wikipedia.DisambiguationError:
        return None

def wrap_link(item):
    """
    replaces reference to item with link - elsewise just returns original item
    """
    link = find_wiki_page(item.strip())
    if link:
        return u'<a href="{0}" target="_blank">{1}</a>'.format(link,item.strip())
    else:
        return item
    

if __name__ == "__main__":
    print get_images_from_url(u"https://en.wikipedia.org/wiki/Charles_Babbage")
