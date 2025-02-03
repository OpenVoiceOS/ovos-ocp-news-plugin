import pytz
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from ovos_utils.time import now_local
from ovos_ocp_rss_plugin import OCPRSSFeedExtractor
from ovos_utils.log import LOG
from pytz import timezone
from urllib.request import urlopen

TSF_URL = "https://www.tsf.pt/stream"
GPB_URL = "http://feeds.feedburner.com/gpbnews"  # DEPRECATED / DEAD
GR1_URL = "https://www.raiplaysound.it"
FT_URL = "https://www.ft.com"
ABC_URL = "https://www.abc.net.au/news"
GEORGIA_TODAY = "https://www.gpb.org/podcasts/georgia-today"
GEORGIA_TODAY2 = "https://www.gpb.org/radio/programs/georgia-today"
NPR_RSS = "https://www.npr.org/rss/podcast.php"  # DEPRECATED
NPR = "https://www.npr.org/podcasts/500005/npr-news-now"
ALASKA_NIGHTLY = "https://www.npr.org/podcasts/828054805/alaska-news-nightly"
KHNS = "https://www.npr.org/podcasts/381444103/k-h-n-s-f-m-local-news"
KGOU_PM = "https://www.npr.org/podcasts/1111549375/k-g-o-u-p-m-news-brief"
KGOU_AM = "https://www.npr.org/podcasts/1111549080/k-g-o-u-a-m-news-brief"
KBBI = "https://www.npr.org/podcasts/1052142404/k-b-b-i-newscast"
ASPEN = "https://www.npr.org/podcasts/1100476310/aspen-public-radio-newscast"
SONOMA = "https://www.npr.org/podcasts/1090302835/first-news"
NHNR = "https://www.npr.org/podcasts/1071428476/n-h-news-recap"
NSPR = "https://www.npr.org/podcasts/1074915520/n-s-p-r-headlines"
WSIU = "https://www.npr.org/podcasts/1038076755/w-s-i-u-news-updates"
SDPB = "https://www.npr.org/podcasts/1031233995/s-d-p-b-news"
KVCR = "https://www.npr.org/podcasts/1033362253/the-midday-news-report"


def tsf():
    """Custom inews fetcher for TSF news."""
    uri = None
    i = 0
    status = 404
    date = now_local(timezone('Portugal'))
    feed = (f'{TSF_URL}/audio/{date.year}/{date.month:02d}/'
            'noticias/{day:02d}/not{hour:02d}.mp3')
    while status != 200 and i < 6:
        uri = feed.format(hour=date.hour, year=date.year,
                          month=date.month, day=date.day)
        status = requests.get(uri).status_code
        date -= timedelta(hours=1)
        i += 1
    if status != 200:
        return None
    return {"uri": uri,
            "title": "TSF Radio Noticias",
            "author": "TSF"}


def georgia_today():
    """Custom news fetcher for Georgia Today."""
    # https://www.gpb.org/radio/programs/georgia-today
    url = "https://gpb-rss.streamguys1.com/gpb/georgia-today-npr-one.xml"
    return OCPRSSFeedExtractor.get_rss_first_stream(url)


def gpb():
    """Custom news fetcher for GPB news."""
    LOG.debug("requested GBP feed has been deprecated, automatically mapping to Georgia Today")
    return georgia_today()


def npr():
    url = f"{NPR_RSS}?id=500005"
    feed = OCPRSSFeedExtractor.get_rss_first_stream(url)
    if feed:
        uri = feed["uri"].split("?")[0]
        return {"uri": uri,
                "title": "NPR News Now",
                "author": "NPR",
                "image": "https://media.npr.org/assets/img/2018/08/06/nprnewsnow_podcasttile_sq.webp"}


def alaska_nightly():
    url = "https://alaskapublic-rss.streamguys1.com/content/alaska-news-nightly-archives-alaska-public-media-npr.xml"
    feed = OCPRSSFeedExtractor.get_rss_first_stream(url)
    if feed:
        uri = feed["uri"].split("?")[0]
        return {"uri": uri, "title": "Alaska News Nightly",
                "author": "Alaska Public Media",
                "image": "https://media.npr.org/images/podcasts/primary/icon_828054805-1ce50401d43f15660a36275a8bf2ff454de62b2f.png"}


def kbbi():
    url = "https://www.kbbi.org/podcast/kbbi-newscast/rss.xml"
    feed = OCPRSSFeedExtractor.get_rss_first_stream(url)
    if feed:
        uri = feed["uri"].split("?")[0]
        return {"uri": uri, "title": "KBBI Newscast",
                "author": "KBBI",
                "image": "https://media.npr.org/images/podcasts/primary/icon_1052142404-2839f62f7db7bf2ec753fca56913bd7a1b52c428.png"}


def kgou_am():
    url = "https://www.kgou.org/podcast/kgou-am-newsbrief/rss.xml"
    feed = OCPRSSFeedExtractor.get_rss_first_stream(url)
    if feed:
        uri = feed["uri"].split("?")[0]
        return {"uri": uri, "title": "KGOU AM NewsBrief",
                "author": "KGOU",
                "image": "https://media.npr.org/images/podcasts/primary/icon_1111549080-ebbfb83b98c966f38237d3e6ed729d659d098cb9.png?s=300&c=85&f=webp"}


def kgou_pm():
    url = "https://www.kgou.org/podcast/kgou-pm-newsbrief/rss.xml"
    feed = OCPRSSFeedExtractor.get_rss_first_stream(url)
    if feed:
        uri = feed["uri"].split("?")[0]
        return {"uri": uri, "title": "KGOU PM NewsBrief",
                "author": "KGOU",
                "image": "https://media.npr.org/images/podcasts/primary/icon_1111549375-c22ef178b4a5db87547aeb4c3c14dc8a8b1bc462.png"}


def khns():
    url = "https://www.khns.org/feed"
    feed = OCPRSSFeedExtractor.get_rss_first_stream(url)
    if feed:
        uri = feed["uri"].split("?")[0]
        return {"uri": uri, "title": "KHNS-FM Local News",
                "author": "KHNS",
                "image": "https://media.npr.org/images/podcasts/primary/icon_1111549375-c22ef178b4a5db87547aeb4c3c14dc8a8b1bc462.png"}


def aspen():
    url = "https://www.aspenpublicradio.org/podcast/aspen-public-radio-n/rss.xml"
    feed = OCPRSSFeedExtractor.get_rss_first_stream(url)
    if feed:
        uri = feed["uri"].split("?")[0]
        return {"uri": uri, "title": "Aspen Public Radio Newscast",
                "author": "Aspen Public Radio",
                "image": "https://media.npr.org/images/podcasts/primary/icon_1100476310-9b43c8bf959de6d90a5f59c58dc82ebc7b9b9258.png"}


def sonoma():
    url = "https://feeds.feedblitz.com/krcbfirstnews%26x%3D1"
    feed = OCPRSSFeedExtractor.get_rss_first_stream(url)
    if feed:
        uri = feed["uri"].split("?")[0]
        return {"uri": uri, "title": "First News",
                "author": "KRCB-FM",
                "image": "https://media.npr.org/images/podcasts/primary/icon_1090302835-6b593e71a8d60b373ec735479dfbdd9e7f2e8cfe.png"}


def nhnr():
    url = "https://nhpr-rss.streamguys1.com/news_recap/nh-news-recap-nprone.xml"
    feed = OCPRSSFeedExtractor.get_rss_first_stream(url)
    if feed:
        uri = feed["uri"].split("?")[0]
        return {"uri": uri, "title": "N.H. News Recap",
                "author": "New Hampshire Public Radio",
                "image": "https://media.npr.org/images/podcasts/primary/icon_1071428476-7bd7627d52d6c3fc7082a1524b1b10a49dde7444.png"}


def nspr():
    url = "https://www.mynspr.org/podcast/nspr-headlines/rss.xml"
    feed = OCPRSSFeedExtractor.get_rss_first_stream(url)
    if feed:
        uri = feed["uri"].split("?")[0]
        return {"uri": uri, "title": "NSPR Headlines",
                "author": "North State Public Radio",
                "image": "https://media.npr.org/images/podcasts/primary/icon_1074915520-8d70ce2af1d6db7fab8a42a9b4eb55dddb6eb69a.png"}


def wsiu():
    url = "https://www.wsiu.org/podcast/wsiu-news-updates/rss.xml"
    feed = OCPRSSFeedExtractor.get_rss_first_stream(url)
    if feed:
        uri = feed["uri"].split("?")[0]
        return {"uri": uri,
                "title": "WSIU News Updates",
                "author": "WSIU Public Radio",
                "image": "https://media.npr.org/images/podcasts/primary/icon_1038076755-aa4101ea9d54395c83b03d7dc7ac823047682192.jpg"}


def sdpb():
    url = "https://listen.sdpb.org/podcast/sdpb-news/rss.xml"
    feed = OCPRSSFeedExtractor.get_rss_first_stream(url)
    if feed:
        uri = feed["uri"].split("?")[0]
        return {"uri": uri,
                "title": "SDPB News",
                "author": "SDPB Radio",
                "image": "https://media.npr.org/images/podcasts/primary/icon_1031233995-ae5c8fd4e932033b3b8e079cdc133703c2ef427c.jpg"}


def kvcr():
    url = "https://www.kvcrnews.org/podcast/kvcr-midday-news-report/rss.xml"
    feed = OCPRSSFeedExtractor.get_rss_first_stream(url)
    if feed:
        uri = feed["uri"].split("?")[0]
        return {"uri": uri,
                "title": "The Midday News Report",
                "author": "KVCR",
                "image": "https://media.npr.org/images/podcasts/primary/icon_1033362253-566d4a69caee465ebe1adf7d2949ae0c745e97b8.png"}


def gr1():
    json_path = f"{GR1_URL}/programmi/gr1.json"
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    }
    resp = requests.get(json_path, headers=headers).json()
    path = resp['block']['cards'][0]['path_id']
    grjson_path = f"{GR1_URL}{path}"
    resp = requests.get(grjson_path, headers=headers).json()
    uri = resp['downloadable_audio']['url']
    return {"uri": uri, "title": "Radio Giornale 1", "author": "Rai GR1"}


def ft():
    page = urlopen(f"{FT_URL}/newsbriefing")
    # Use bs4 to parse website and get mp3 link
    soup = BeautifulSoup(page, features='html.parser')
    result = soup.find('time')
    target_div = result.parent.find_next('div')
    target_url = 'http://www.ft.com' + target_div.a['href']
    mp3_page = urlopen(target_url)
    mp3_soup = BeautifulSoup(mp3_page, features='html.parser')
    uri = mp3_soup.find('source')['src']
    return {"uri": uri, "title": "FT news briefing", "author": "Financial Times"}


def abc():
    """Custom news fetcher for ABC News Australia briefing"""
    # Format template with (hour, day, month)
    url_temp = ('https://abcmedia.akamaized.net/news/audio/news-briefings/'
                'top-stories/{}{}/NAUs_{}00flash_{}{}_nola.mp3')
    now = pytz.utc.localize(datetime.utcnow())
    syd_tz = pytz.timezone('Australia/Sydney')
    syd_dt = now.astimezone(syd_tz)
    hour = syd_dt.strftime('%H')
    day = syd_dt.strftime('%d')
    month = syd_dt.strftime('%m')
    year = syd_dt.strftime('%Y')
    url = url_temp.format(year, month, hour, day, month)

    # If this hours news is unavailable try the hour before
    response = requests.get(url)
    if response.status_code != 200:
        hour = str(int(hour) - 1)
        url = url_temp.format(year, month, hour, day, month)

    return {"uri": url,
            "title": "ABC News Australia",
            "author": "Australian Broadcasting Corporation"}


URL_MAPPINGS = {
    TSF_URL: tsf,
    GPB_URL: gpb,
    GR1_URL: gr1,
    FT_URL: ft,
    ABC_URL: abc,
    NPR: npr,
    NPR_RSS: npr,
    ASPEN: aspen,
    ALASKA_NIGHTLY: alaska_nightly,
    KHNS: khns,
    KGOU_PM: kgou_pm,
    KGOU_AM: kgou_am,
    KBBI: kbbi,
    SONOMA: sonoma,
    NHNR: nhnr,
    NSPR: nspr,
    WSIU: wsiu,
    SDPB: sdpb,
    KVCR: kvcr,
    GEORGIA_TODAY: georgia_today,
    GEORGIA_TODAY2: georgia_today
}
