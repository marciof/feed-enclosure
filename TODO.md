# Feeds

- Need to find alternatives to Liferea? It removed the external downloader tool option (on v1.15.9), and may remove more, make things more complicated, or go unmaintained? Preferably with support for plugins and OPML.
  - [RSS Guard](https://github.com/martinrotter/rssguard/issues/1952#issuecomment-4609281030)
  - [Akregator](https://github.com/KDE/akregator/)
  - [Alligator](https://github.com/kde/alligator)
  - [Thunderbird](https://reviewers.addons.thunderbird.net/en-us/thunderbird/tag/rss) (see also [custom CSS](https://reddit.com/r/Thunderbird/comments/1fhyvvq/kind_of_loving_thunderbird_as_an_rss_reader_right/lo3dpgu/))
  - local proxy (as done previously) as a hook for detecting enclosures, and optionally downloading and passing on as a stream to the upstream app.
    - https://github.com/yt-dlp/yt-dlp/wiki/FAQ#how-do-i-stream-directly-to-media-player
    - https://github.com/fastapi/fastapi
    - https://github.com/Kludex/starlette
  - https://freenet.org/apps/
- Helper script for getting an RSS feed URL from a YouTube channel/playlist.
  - https://codemadness.org/sfeed.html
  - check what/how Liferea does it

## Liferea

- Look into sandboxing an old fixed version that still has support for custom external download tools? https://github.com/89luca89/distrobox
- Not always updating some feeds even when it has new content  (eg. TVW The Impact).
- Calls the conversion filter with an empty stdin, when it decides incorrectly that a feed (eg. TVW The Impact) has no new content.
- Feed fetch spacing option like RSS Guard. https://github.com/lwindolf/liferea/issues/1555
- OPML automatic backup (via plugins?).

# Videos

- Need to find other GUI alternatives?
  - Parabolic, but see https://github.com/NickvisionApps/Parabolic/issues/1855
  - VidBee https://github.com/nexmoe/VidBee
  - https://fmhy.net/social-media-tools#youtube-downloaders
- yt-dlp extensibility:
  - Plugins: https://github.com/yt-dlp/yt-dlp#plugins
  - `--exec` / post-processing: https://github.com/yt-dlp/yt-dlp#post-processing-options
- Embed subtitles in downloaded videos.
- Skip YouTube shorts (vertical videos) option.
- Skip video if mtime is more than 1 year in the past (eg. Last Week Tonight uploading old episodes) option.
- Make it possible to watch a video as it's being downloaded before it finishes.
- Video summarizing option? TL;DW Too Long; Didn't watch, https://tldw.tube/, https://news.ycombinator.com/item?id=43021044
- How to skip non-English videos? Eg. French/German Withings

## Instagram

- RSS feed from Instagram feed (for https://www.instagram.com/therapyjeff/)
  - eg. `a[href*="/reel/"][role=link]`
- via browser impersonation? might need to run JavaScript
  - https://github.com/CloakHQ/CloakBrowser + Playwright / Puppeteer
  - stealth browser as a localhost proxy?
- via HTTP impersonation? might be more complex to parse w/o JavaScript
  - https://github.com/lexiforest/curl-impersonate
  - https://github.com/jpjacobpadilla/Stealth-Requests
- via external tool/library/API?
  - https://github.com/instaloader/instaloader
  - https://imginn.com/therapyjeff/
  - https://www.picnob.com/profile/therapyjeff/
  - https://greasyfork.org/en/scripts/561325-bypass-instagram-login-redirects/code
- etc
  - https://en.wikipedia.org/wiki/Model_Context_Protocol
  - https://www.mitmproxy.org

## Youwee

- Sort download queue from recent to old.
- App is too sluggish/slow?
- Disable previews altogether in the YouTube section?
- Follow dark/light mode from OS? CLI option to change mode?
- Show timestamp when download was added/finished in the queue.
- Change number of parallel downloads during downloading.

## VLC

- Embed video metadata in screenshots?

# Syncing

- Do filenames with emojis break Dropbox syncing? See also https://github.com/woodgern/confusables
- Sync VLC last video position between devices.
- Syncthing for faster efficient syncing within the local network between devices? Double check Dropbox.

# Device

- Zero Terminal v3: https://n-o-d-e.net/zeroterminal3.html
- M5Stack Tab5: https://shop.m5stack.com/products/m5stack-tab5-iot-development-kit-esp32-p4

# Requirements

## Use Cases

Minimum:

- Automatic update of feeds (eg. RSS, Atom).
- Automatic download of enclosures.
  - Including non-attachments (eg. YouTube URLs).
  - Including JavaScript-heavy websites (eg. Instagram).
- Extensibility (eg. adding websites/feeds without built-in support).
- Data portability.
  - Ideally OPML as storage, but import/export at a minimum.
- Video metadata (eg. chapters, subtitles).

Optional:

- Download URLs one-off.
- Synchronization (either built-in or third-party, eg. Dropbox).

## Platforms

- Linux
- Windows: 10 64-bit, 11 64-bit
- Android

# Prior Work

(Last checked: 2026-07-16)

## Candidates

- https://antennapod.org
  - Very close to the requirements.
  - Audio-oriented (eg. [TVW shows](https://tvw.org/shows/) don't have video).
  - [OPML support is only for import/export, not subscriptions storage.](https://antennapod.org/documentation/general/backup)
  - No plugin support.
  - [Doesn't run on Linux/Windows.](https://antennapod.org/download/)
- https://fluidcastapp.com
  - Very close to the requirements.
  - Not open source.
  - Audio-oriented (eg. [TVW shows](https://tvw.org/shows/) don't have video).
  - OPML support is only for import/export, not subscriptions storage.
  - No plugin support.
  - No Atom feed support.
- https://grayjay.app
  - Very close to the requirements.
  - [Desktop app still in development?](https://grayjay.app/desktop/)
  - [No YouTube playlist update support.](https://github.com/futo-org/grayjay-android/issues/857)
  - [No OPML support.](https://github.com/futo-org/grayjay-android/issues/1524)
- https://github.com/jmbannon/ytdl-sub
  - Very close to the requirements.
  - [Doesn't run on phones/Android.](https://ytdl-sub.readthedocs.io/en/latest/guides/install/index.html)
  - [No OPML support.](https://ytdl-sub.readthedocs.io/en/latest/search.html?q=opml)
- https://github.com/flexget/flexget
  - Very close to the requirements.
  - [Doesn't run on phones/Android.](https://www.flexget.com/InstallWizard)
  - [No OPML support.](https://github.com/search?q=repo%3AFlexget%2FFlexget%20%22opml%22&type=code)
  - [GUI still in development.](https://flexget.com/Web-UI)

## Alternatives

- https://github.com/mxpv/podsync
  - [Doesn't run on phones/Android.](https://github.com/mxpv/podsync#-features)
  - [Last release is from 2025.](https://github.com/mxpv/podsync/releases)
- https://github.com/Sn8z/Poddr
  - [Doesn't run on phones/Android.](https://github.com/Sn8z/Poddr#downloads)
  - [Last release is from 2025.](https://github.com/Sn8z/Poddr/releases)
  - App is sluggish ([due to Electron?](https://github.com/Sn8z/Poddr/blob/main/electron-builder.yml)).
- https://github.com/tubearchivist/tubearchivist
  - [Doesn't run on phones/Android.](https://github.com/tubearchivist/tubearchivist/releases)
  - [It's made for archival and media server.](https://github.com/tubearchivist/tubearchivist#core-functionality)
  - [System requirements are too resource intensive.](https://github.com/tubearchivist/tubearchivist/releasesS)
- https://github.com/kieraneglin/pinchflat
  - [Doesn't run on phones/Android.](https://github.com/kieraneglin/pinchflat#installation)
  - [Last release is from 2025.](https://github.com/kieraneglin/pinchflat/releases)
  - [No OPML import support?](https://github.com/search?q=repo%3Akieraneglin%2Fpinchflat%20opml&type=code)
- https://github.com/deniscerri/ytdlnis
  - [No OPML support.](https://github.com/search?q=repo%3Adeniscerri%2Fytdlnis%20opml&type=code)
  - [No RSS feed support.](https://github.com/search?q=repo%3Adeniscerri%2Fytdlnis+%2F%5Cbrss%5Cb%2F&type=code)
  - [Sloppy documentation?](https://ytdlnis.org/docs/guides/home#i-have-many-urls-that-i-need-to-download) (eg. "that _i_ need")
- https://github.com/junkfood02/Seal
  - [No OPML support.](https://github.com/search?q=repo%3AJunkFood02%2FSeal%20opml&type=code)
  - [Last release is from 2024.](https://github.com/JunkFood02/Seal/releases)
  - [No RSS feed support.](https://github.com/search?q=repo%3AJunkFood02%2FSeal%20rss&type=code)
- https://github.com/RSS-Bridge/rss-bridge
  - RSS bridge only.
- https://stacher.io/
  - Not open source.
