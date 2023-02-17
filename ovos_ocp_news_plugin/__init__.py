import pytz
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from datetime import timedelta
from lingua_franca.time import now_local
from ovos_ocp_rss_plugin import OCPRSSFeedExtractor
from ovos_plugin_manager.templates.ocp import OCPStreamExtractor
from ovos_utils.log import LOG
from pytz import timezone
from urllib.request import urlopen


class OCPNewsExtractor(OCPStreamExtractor):
    TSF_URL = "https://www.tsf.pt/stream"
    GPB_URL = "http://feeds.feedburner.com/gpbnews"
    GR1_URL = "https://www.raiplaysound.it"
    FT_URL = "https://www.ft.com"
    ABC_URL = "https://www.abc.net.au/news"

    NPR_RSS = "https://www.npr.org/rss/podcast.php"
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

    def __init__(self, ocp_settings=None):
        super().__init__(ocp_settings)
        self.settings = self.ocp_settings.get("news", {})

    @property
    def supported_seis(self):
        """
        skills may return results requesting a specific extractor to be used

        plugins should report a StreamExtractorIds (sei) that identifies it can handle certain kinds of requests

        any streams of the format "{sei}//{uri}" can be handled by this plugin
        """
        return ["news"]

    def validate_uri(self, uri):
        """ return True if uri can be handled by this extractor, False otherwise"""
        return any([uri.startswith(sei) for sei in self.supported_seis]) or \
               any([uri.startswith(url) for url in [
                   self.TSF_URL, self.GPB_URL, self.NPR_RSS,
                   self.GR1_URL, self.FT_URL, self.ABC_URL,
                   self.NPR, self.ASPEN, self.ALASKA_NIGHTLY,
                   self.KVCR, self.KBBI, self.KHNS, self.KGOU_AM, self.KGOU_PM,
                   self.NSPR, self.WSIU, self.SONOMA, self.SDPB, self.NHNR
               ]])

    def extract_stream(self, uri, video=True):
        """ return the real uri that can be played by OCP """
        meta = {}
        if uri.startswith("news//"):
            uri = meta["uri"] = uri[6:]

        if uri.startswith(self.TSF_URL):
            return self.tsf()
        elif uri.startswith(self.GPB_URL):
            return self.gpb()
        elif uri.startswith(self.GR1_URL):
            return self.gr1()
        elif uri.startswith(self.FT_URL):
            return self.ft()
        elif uri.startswith(self.ABC_URL):
            return self.abc()
        elif uri.startswith(self.ALASKA_NIGHTLY):
            return self.alaska_nightly()
        elif uri.startswith(self.KBBI):
            return self.kbbi()
        elif uri.startswith(self.KHNS):
            return self.khns()
        elif uri.startswith(self.KGOU_AM):
            return self.kgou_am()
        elif uri.startswith(self.KGOU_PM):
            return self.kgou_pm()
        elif uri.startswith(self.ASPEN):
            return self.aspen()
        elif uri.startswith(self.SONOMA):
            return self.sonoma()
        elif uri.startswith(self.SDPB):
            return self.sdpb()
        elif uri.startswith(self.NHNR):
            return self.nhnr()
        elif uri.startswith(self.NSPR):
            return self.nspr()
        elif uri.startswith(self.WSIU):
            return self.wsiu()
        elif uri.startswith(self.KVCR):
            return self.kvcr()
        elif uri.startswith(self.NPR_RSS) or uri.startswith(self.NPR):
            return self.npr()
        return meta  # dropped the news// sei if present

    @classmethod
    def tsf(cls):
        """Custom inews fetcher for TSF news."""
        uri = None
        i = 0
        status = 404
        date = now_local(timezone('Portugal'))
        feed = (f'{cls.TSF_URL}/audio/{date.year}/{date.month:02d}/'
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

    @classmethod
    def gpb(cls):
        """Custom news fetcher for GPB news."""
        # https://www.gpb.org/radio/programs/georgia-today
        LOG.debug("requested GBP feed has been deprecated, automatically mapping to Georgia Today")
        url = "https://gpb-rss.streamguys1.com/gpb/georgia-today-npr-one.xml"
        return OCPRSSFeedExtractor.get_rss_first_stream(url)

    @classmethod
    def npr(cls):
        url = f"{cls.NPR_RSS}?id=500005"
        feed = OCPRSSFeedExtractor.get_rss_first_stream(url)
        if feed:
            uri = feed["uri"].split("?")[0]
            return {"uri": uri,
                    "title": "NPR News Now",
                    "author": "NPR",
                    "image": "https://media.npr.org/assets/img/2018/08/06/nprnewsnow_podcasttile_sq.webp"}

    @classmethod
    def alaska_nightly(cls):
        url = "https://alaskapublic-rss.streamguys1.com/content/alaska-news-nightly-archives-alaska-public-media-npr.xml"
        feed = OCPRSSFeedExtractor.get_rss_first_stream(url)
        if feed:
            uri = feed["uri"].split("?")[0]
            return {"uri": uri, "title": "Alaska News Nightly",
                    "author": "Alaska Public Media",
                    "image": "https://media.npr.org/images/podcasts/primary/icon_828054805-1ce50401d43f15660a36275a8bf2ff454de62b2f.png"}

    @classmethod
    def kbbi(cls):
        url = "https://www.kbbi.org/podcast/kbbi-newscast/rss.xml"
        feed = OCPRSSFeedExtractor.get_rss_first_stream(url)
        if feed:
            uri = feed["uri"].split("?")[0]
            return {"uri": uri, "title": "KBBI Newscast",
                    "author": "KBBI",
                    "image": "https://media.npr.org/images/podcasts/primary/icon_1052142404-2839f62f7db7bf2ec753fca56913bd7a1b52c428.png"}

    @classmethod
    def kgou_am(cls):
        url = "https://www.kgou.org/podcast/kgou-am-newsbrief/rss.xml"
        feed = OCPRSSFeedExtractor.get_rss_first_stream(url)
        if feed:
            uri = feed["uri"].split("?")[0]
            return {"uri": uri, "title": "KGOU AM NewsBrief",
                    "author": "KGOU",
                    "image": "https://media.npr.org/images/podcasts/primary/icon_1111549080-ebbfb83b98c966f38237d3e6ed729d659d098cb9.png?s=300&c=85&f=webp"}

    @classmethod
    def kgou_pm(cls):
        url = "https://www.kgou.org/podcast/kgou-pm-newsbrief/rss.xml"
        feed = OCPRSSFeedExtractor.get_rss_first_stream(url)
        if feed:
            uri = feed["uri"].split("?")[0]
            return {"uri": uri, "title": "KGOU PM NewsBrief",
                    "author": "KGOU",
                    "image": "https://media.npr.org/images/podcasts/primary/icon_1111549375-c22ef178b4a5db87547aeb4c3c14dc8a8b1bc462.png"}

    @classmethod
    def khns(cls):
        url = "https://www.khns.org/feed"
        feed = OCPRSSFeedExtractor.get_rss_first_stream(url)
        if feed:
            uri = feed["uri"].split("?")[0]
            return {"uri": uri, "title": "KHNS-FM Local News",
                    "author": "KHNS",
                    "image": "https://media.npr.org/images/podcasts/primary/icon_1111549375-c22ef178b4a5db87547aeb4c3c14dc8a8b1bc462.png"}

    @classmethod
    def aspen(cls):
        url = "https://www.aspenpublicradio.org/podcast/aspen-public-radio-n/rss.xml"
        feed = OCPRSSFeedExtractor.get_rss_first_stream(url)
        if feed:
            uri = feed["uri"].split("?")[0]
            return {"uri": uri, "title": "Aspen Public Radio Newscast",
                    "author": "Aspen Public Radio",
                    "image": "https://media.npr.org/images/podcasts/primary/icon_1100476310-9b43c8bf959de6d90a5f59c58dc82ebc7b9b9258.png"}

    @classmethod
    def sonoma(cls):
        url = "https://feeds.feedblitz.com/krcbfirstnews%26x%3D1"
        feed = OCPRSSFeedExtractor.get_rss_first_stream(url)
        if feed:
            uri = feed["uri"].split("?")[0]
            return {"uri": uri, "title": "First News",
                    "author": "KRCB-FM",
                    "image": "https://media.npr.org/images/podcasts/primary/icon_1090302835-6b593e71a8d60b373ec735479dfbdd9e7f2e8cfe.png"}

    @classmethod
    def nhnr(cls):
        url = "https://nhpr-rss.streamguys1.com/news_recap/nh-news-recap-nprone.xml"
        feed = OCPRSSFeedExtractor.get_rss_first_stream(url)
        if feed:
            uri = feed["uri"].split("?")[0]
            return {"uri": uri, "title": "N.H. News Recap",
                    "author": "New Hampshire Public Radio",
                    "image": "https://media.npr.org/images/podcasts/primary/icon_1071428476-7bd7627d52d6c3fc7082a1524b1b10a49dde7444.png"}

    @classmethod
    def nspr(cls):
        url = "https://www.mynspr.org/podcast/nspr-headlines/rss.xml"
        feed = OCPRSSFeedExtractor.get_rss_first_stream(url)
        if feed:
            uri = feed["uri"].split("?")[0]
            return {"uri": uri, "title": "NSPR Headlines",
                    "author": "North State Public Radio",
                    "image": "https://media.npr.org/images/podcasts/primary/icon_1074915520-8d70ce2af1d6db7fab8a42a9b4eb55dddb6eb69a.png"}

    @classmethod
    def wsiu(cls):
        url = "https://www.wsiu.org/podcast/wsiu-news-updates/rss.xml"
        feed = OCPRSSFeedExtractor.get_rss_first_stream(url)
        if feed:
            uri = feed["uri"].split("?")[0]
            return {"uri": uri,
                    "title": "WSIU News Updates",
                    "author": "WSIU Public Radio",
                    "image": "https://media.npr.org/images/podcasts/primary/icon_1038076755-aa4101ea9d54395c83b03d7dc7ac823047682192.jpg"}

    @classmethod
    def sdpb(cls):
        url = "https://listen.sdpb.org/podcast/sdpb-news/rss.xml"
        feed = OCPRSSFeedExtractor.get_rss_first_stream(url)
        if feed:
            uri = feed["uri"].split("?")[0]
            return {"uri": uri,
                    "title": "SDPB News",
                    "author": "SDPB Radio",
                    "image": "https://media.npr.org/images/podcasts/primary/icon_1031233995-ae5c8fd4e932033b3b8e079cdc133703c2ef427c.jpg"}

    @classmethod
    def kvcr(cls):
        url = "https://www.kvcrnews.org/podcast/kvcr-midday-news-report/rss.xml"
        feed = OCPRSSFeedExtractor.get_rss_first_stream(url)
        if feed:
            uri = feed["uri"].split("?")[0]
            return {"uri": uri,
                    "title": "The Midday News Report",
                    "author": "KVCR",
                    "image": "https://media.npr.org/images/podcasts/primary/icon_1033362253-566d4a69caee465ebe1adf7d2949ae0c745e97b8.png"}

    @classmethod
    def gr1(cls):
        json_path = f"{cls.GR1_URL}/programmi/gr1.json"
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
        grjson_path = f"{cls.GR1_URL}{path}"
        resp = requests.get(grjson_path, headers=headers).json()
        uri = resp['downloadable_audio']['url']
        return {"uri": uri, "title": "Radio Giornale 1", "author": "Rai GR1"}

    @classmethod
    def ft(cls):
        page = urlopen(f"{cls.FT_URL}/newsbriefing")
        # Use bs4 to parse website and get mp3 link
        soup = BeautifulSoup(page, features='html.parser')
        result = soup.find('time')
        target_div = result.parent.find_next('div')
        target_url = 'http://www.ft.com' + target_div.a['href']
        mp3_page = urlopen(target_url)
        mp3_soup = BeautifulSoup(mp3_page, features='html.parser')
        uri = mp3_soup.find('source')['src']
        return {"uri": uri, "title": "FT news briefing", "author": "Financial Times"}

    @classmethod
    def abc(cls):
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
