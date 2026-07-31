# OCP News Plugin

This plugin lets [OCP](https://github.com/OpenVoiceOS/ovos-media) play news feeds from several providers. It resolves a news request to the real stream URL and hands it to OCP for playback.

## Install

```bash
pip install ovos-ocp-news-plugin
```

## Usage

OCP loads this plugin through the `opm.ocp.extractor` entry point. It handles two kinds of stream requests:

- A URI with the `news//` prefix, for example `news//georgia-today`.
- A URI that starts with one of the news provider URLs the plugin recognizes (for example a TSF or NPR feed URL).

No manual setup is needed beyond installing the plugin. OCP settings for this plugin live under the `news` key in `mycroft.conf`. The plugin defines no settings of its own.

## Related projects

- [OpenVoiceOS/ovos-media](https://github.com/OpenVoiceOS/ovos-media): the OCP media player that loads this extractor.
- [OpenVoiceOS/ovos-ocp-rss-plugin](https://github.com/OpenVoiceOS/ovos-ocp-rss-plugin): extracts streams from RSS and podcast feeds. Several news sources here resolve through it.
- [OpenVoiceOS/ovos-ocp-m3u-plugin](https://github.com/OpenVoiceOS/ovos-ocp-m3u-plugin): extracts streams from M3U playlists.
- [OpenVoiceOS/ovos-ocp-audio-plugin](https://github.com/OpenVoiceOS/ovos-ocp-audio-plugin): a sibling OCP stream extractor plugin.

## License

Apache-2.0
