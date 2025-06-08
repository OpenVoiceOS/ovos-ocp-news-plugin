from ovos_plugin_manager.templates.ocp import OCPStreamExtractor
from ovos_ocp_news_plugin.extractors import URL_MAPPINGS
from ovos_utils import classproperty

class OCPNewsExtractor(OCPStreamExtractor):
    def __init__(self, ocp_settings=None):
        super().__init__(ocp_settings)
        self.settings = self.ocp_settings.get("news", {})

    @classproperty
    def supported_seis(cls):
        """
        skills may return results requesting a specific extractor to be used

        plugins should report a StreamExtractorIds (sei) that identifies it can handle certain kinds of requests

        any streams of the format "{sei}//{uri}" can be handled by this plugin
        """
        return ["news"]

    def validate_uri(self, uri):
        """ return True if uri can be handled by this extractor, False otherwise"""
        return any([uri.startswith(sei) for sei in self.supported_seis]) or \
               any([uri.startswith(url) for url in URL_MAPPINGS.keys()])

    def extract_stream(self, uri, video=True):
        """ return the real uri that can be played by OCP """
        meta = {}
        if uri.startswith("news//"):
            uri = meta["uri"] = uri[6:]

        for url, extractor in URL_MAPPINGS.items():
            if uri.startswith(url):
                return extractor()

        return meta  # dropped the news// sei if present
