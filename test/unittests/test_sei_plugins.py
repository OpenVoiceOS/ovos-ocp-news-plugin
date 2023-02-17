import unittest

from ovos_plugin_manager.ocp import StreamHandler
from ovos_ocp_news_plugin.extractors import URL_MAPPINGS


class TestOCPExtractor(unittest.TestCase):

    def test_news(self):
        parser = StreamHandler()
        for url in URL_MAPPINGS:
            print(f"#### {url}")
            meta = parser.extract_stream(url) or {}
            print(meta)
            self.assertTrue(bool(meta.get("uri")))
            meta = parser.extract_stream(f"news//{url}") or {}
            self.assertTrue(bool(meta.get("uri")))


if __name__ == '__main__':
    unittest.main()
