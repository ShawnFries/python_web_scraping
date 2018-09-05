import requests
import re
import sys
from random import choice
import time
from requests import get
from bs4 import BeautifulSoup
from collections import Counter
from string import punctuation
import urllib2
import cfscrape


PAGE_URL_PREFIX = 'https://www.glassdoor.com/Job/providence-data-scientist-jobs-SRCH_IL.0,10_IC1151289_KO11,25'
PAGE_URL_SUFFIX = '.htm?minRating=4.0&minSalary=48000'
HEADER = {
    'User-Agent': choice(['Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14',
                 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
                 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
                 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0']),
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
}
BASE_URL_PREFIX = 'https://www.glassdoor.com'

page_url_index = 1
page_url = PAGE_URL_PREFIX + str(page_url_index) + PAGE_URL_SUFFIX
while page_url_index < 50:
    request = urllib2.Request(page_url, headers=HEADER)
    html = urllib2.urlopen(request).read()
    bs = BeautifulSoup(html)
    count_matches = 0
    for div in bs.findAll('div', attrs={'class': 'easyApply'}):
        job_url = div.find_next('a', href=True) # find <a> that appears after <div> since it isn't contained inside
        if job_url.has_attr('href') and 'partner' in job_url['href'] and 'jobListing' in job_url['href']:
            posting_url = BASE_URL_PREFIX + job_url['href']
            request = urllib2.Request(posting_url, headers=HEADER)
            html = urllib2.urlopen(request).read()
            bs = BeautifulSoup(html)
            desires_phd = False
            accepts_bachelors = False
            
            for li in bs.findAll('li'):
                if li.string is None:
                    continue
                bullet_point_text = li.string.lower()
                if 'phd' in bullet_point_text or 'ph.d' in bullet_point_text:
                    desires_phd = True
                if 'bachelor' in bullet_point_text or 'bs' in bullet_point_text or 'b.s' in bullet_point_text or 'ba' in bullet_point_text or 'b.a' in bullet_point_text:
                    accepts_bachelors = True
                    break
            
            am_qualified_for_job = not desires_phd or accepts_bachelors
            if am_qualified_for_job: 
                count_matches += 1
                print(posting_url)
    if page_url_index > 10 and count_matches == 0: # so we don't go forever..
        break
    page_url_index += 1
    page_url = PAGE_URL_PREFIX + str(page_url_index) + PAGE_URL_SUFFIX