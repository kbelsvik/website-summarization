from hanzo.warctools import WarcRecord
from nltk.tokenize import sent_tokenize, word_tokenize
from urllib.parse import urlparse
import bs4
import re

def extract_text(html):
    # remove meta data
    soup = bs4.BeautifulSoup(html.split("\r\n\r\n", 1)[-1].lower(),'lxml')
    
    # remove scripts
    for script in soup(["script", "style"]):
        script.extract()
        
    # extract all text without tags
    text = soup.getText()
    #text = re.sub('\n\s*\n', '\n', text)
    return text

def read_record(path, num_pages=10):
    warcr = WarcRecord.open_archive(path, gzip= 'auto')
    i = 0
    documents = []
    urls = []
    for record in warcr:
        if i >= num_pages:
            break
        if record.type == b'response' and record.content[0] == b'application/http; msgtype=response':
            url = ""
            for (h, v) in record.headers:
                if h == b'WARC-Target-URI':
                    url = str(v, errors = "ignore")
            # domain = re.sub(r'^(www\.)?','',urlparse(url.decode("ISO-8859-1"))[1].lower())
            # urls.append(url.decode("ISO-8859-1").lower())
            urls.append(url)
            # documents.append(extract_text(record.content[1].decode("ISO-8859-1")))
            documents.append(extract_text(str(record.content[1], errors = "ignore")))
            i += 1
    return documents, urls

def parse_sentences(document):
    sentences = sent_tokenize(document)
    sent_tokens = [word_tokenize(sentence) for sentence in sentences]
    return sent_tokens