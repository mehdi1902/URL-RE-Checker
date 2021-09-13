from find import *

def test_download_site_valid():
	# Testing a valid website
    url = 'http://www.brainjar.com/java/host/test.html'
    content, info = download_site(url, decode=False)
    assert content.status == 200
    assert len(content.data) > 0


def test_download_site_invalid():
    # Testing an invalid website
    url = 'http://www.brainjarsssssss.com/java/host/test.html'
    content, info = download_site(url, decode=False)
    assert content.status == 404


def test_match_site():
    pool = urllib3.PoolManager()
    url = 'https://webscraper.io/test-sites/tables'
    matched, info = match_site(url, [r'@\w{10,}', r'\d{6,}'])
    assert (matched == {'@\\w{10,}': ['@webscraper', '@webscraper'], '\\d{6,}': ['604046']})

