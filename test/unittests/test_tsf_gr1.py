"""
Regression tests for:
  - https://github.com/OpenVoiceOS/ovos-ocp-news-plugin/issues/9 (TSF no longer works)
  - https://github.com/OpenVoiceOS/ovos-ocp-news-plugin/issues/7 (GR1 does not work)

Both fixtures under test/fixtures were recorded from real live responses
(TSF's noticiarios listing page, Rai's gr1.json / episode json), not
synthesized, per the "record a real response" requirement.
"""
import json
import os
import unittest
from unittest.mock import patch, MagicMock

from ovos_ocp_news_plugin.extractors import tsf, gr1

FIXTURES = os.path.join(os.path.dirname(__file__), "..", "fixtures")


def _read(name):
    with open(os.path.join(FIXTURES, name), encoding="utf-8") as f:
        return f.read()


class TestTSF(unittest.TestCase):
    def test_tsf_parses_latest_bulletin_from_noticiarios_page(self):
        """The old tsf.pt/stream/audio/.../notHH.mp3 URL scheme 404s
        (verified live). TSF now serves bulletins from a CDN with
        unpredictable hashed filenames listed on /noticiarios."""
        html = _read("tsf_noticiarios.html")
        fake_resp = MagicMock(status_code=200, text=html)
        with patch("ovos_ocp_news_plugin.extractors.requests.get",
                   return_value=fake_resp) as mocked_get:
            result = tsf()
        self.assertIsNotNone(result)
        self.assertTrue(result["uri"].startswith("https://"))
        self.assertTrue(result["uri"].endswith("/mp3/audio.mp3"))
        self.assertEqual(result["author"], "TSF")
        # must not hit the old dead scheme
        self.assertNotIn("tsf.pt/stream", result["uri"])
        mocked_get.assert_called_once()

    def test_tsf_returns_none_on_empty_page(self):
        fake_resp = MagicMock(status_code=200, text="<html></html>")
        with patch("ovos_ocp_news_plugin.extractors.requests.get",
                   return_value=fake_resp):
            result = tsf()
        self.assertIsNone(result)


class TestGR1(unittest.TestCase):
    def test_gr1_resolves_relinker_to_playable_url(self):
        """The raw Rai relinker URL 403s ("Access Denied") unless fetched
        with a browser User-Agent (verified live), which is what was
        causing the reported CPU spin - the media backend got stuck on
        the HTML error page. gr1() must resolve it to the final URL."""
        programma = json.loads(_read("gr1_programma.json"))
        episode = json.loads(_read("gr1_episode.json"))
        relinker_url = episode["downloadable_audio"]["url"]
        resolved_url = ("https://StreamCdnR19-cdnraivodostr3.msvdn.net/ostr3/"
                         "podcastcdn/Rai/audiocut/gr1_audiocut/30115436_1800.mp4/"
                         "playlist.m3u8")

        programma_resp = MagicMock(status_code=200)
        programma_resp.json.return_value = programma
        episode_resp = MagicMock(status_code=200)
        episode_resp.json.return_value = episode
        relinker_resp = MagicMock(status_code=200, url=resolved_url)

        def fake_get(url, *args, **kwargs):
            if url.endswith("gr1.json"):
                return programma_resp
            if url == relinker_url:
                return relinker_resp
            return episode_resp

        with patch("ovos_ocp_news_plugin.extractors.requests.get",
                   side_effect=fake_get):
            result = gr1()

        self.assertEqual(result["uri"], resolved_url)
        self.assertNotEqual(result["uri"], relinker_url)
        self.assertEqual(result["author"], "Rai GR1")

    def test_gr1_falls_back_to_relinker_url_if_resolution_fails(self):
        programma = json.loads(_read("gr1_programma.json"))
        episode = json.loads(_read("gr1_episode.json"))
        relinker_url = episode["downloadable_audio"]["url"]

        programma_resp = MagicMock(status_code=200)
        programma_resp.json.return_value = programma
        episode_resp = MagicMock(status_code=200)
        episode_resp.json.return_value = episode
        denied_resp = MagicMock(status_code=403, url=relinker_url)

        def fake_get(url, *args, **kwargs):
            if url.endswith("gr1.json"):
                return programma_resp
            if url == relinker_url:
                return denied_resp
            return episode_resp

        with patch("ovos_ocp_news_plugin.extractors.requests.get",
                   side_effect=fake_get):
            result = gr1()

        self.assertEqual(result["uri"], relinker_url)


if __name__ == '__main__':
    unittest.main()
