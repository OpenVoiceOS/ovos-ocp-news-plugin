import unittest

from ovos_plugin_manager.ocp import StreamHandler


class TestOCPExtractor(unittest.TestCase):

    def test_news(self):
        parser = StreamHandler()
        news_urls = [
            "https://www.raiplaysound.it",
            "https://www.tsf.pt/stream",
            "https://www.abc.net.au/news",
            "https://www.ft.com",
            "http://feeds.feedburner.com/gpbnews",  # deprecated, mapped to GeorgiaToday
            "https://www.npr.org/rss/podcast.php",
            "https://www.npr.org/podcasts/500005/npr-news-now",
            "https://www.npr.org/podcasts/828054805/alaska-news-nightly",
            "https://www.npr.org/podcasts/381444103/k-h-n-s-f-m-local-news",
            "https://www.npr.org/podcasts/1111549375/k-g-o-u-p-m-news-brief",
            "https://www.npr.org/podcasts/1111549080/k-g-o-u-a-m-news-brief",
            "https://www.npr.org/podcasts/1100476310/aspen-public-radio-newscast",
            "https://www.npr.org/podcasts/1090302835/first-news",
            "https://www.npr.org/podcasts/1071428476/n-h-news-recap",
            "https://www.npr.org/podcasts/1074915520/n-s-p-r-headlines",
            "https://www.npr.org/podcasts/1038076755/w-s-i-u-news-updates",
            "https://www.npr.org/podcasts/1031233995/s-d-p-b-news",
            "https://www.npr.org/podcasts/1033362253/the-midday-news-report"

        ]
        for url in news_urls:
            print(f"#### {url}")
            meta = parser.extract_stream(url) or {}
            print(meta)
            self.assertTrue(bool(meta.get("uri")))
            meta = parser.extract_stream(f"news//{url}") or {}
            self.assertTrue(bool(meta.get("uri")))


if __name__ == '__main__':
    unittest.main()
