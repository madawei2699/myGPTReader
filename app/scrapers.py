import re
import requests
import lxml.html
from lxml.html.clean import clean_html
def _parse_url_or_html(url_or_html: str) -> lxml.html.Element:
    """
    Given URL or HTML, return lxml.html.Element
    """
    # coerce to HTML
    orig_url = None
    if url_or_html.startswith("http"):
        orig_url = url_or_html
        url_or_html = requests.get(url_or_html).text
    # collapse whitespace
    url_or_html = re.sub("[ \t]+", " ", url_or_html)
    doc = lxml.html.fromstring(url_or_html)
    if orig_url:
        doc.make_links_absolute(orig_url)
    cleaned_html = clean_html(doc)
    html_string = lxml.html.tostring(cleaned_html, encoding="unicode")
    return html_string