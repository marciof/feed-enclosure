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
- Helper script for getting an RSS feed URL from a YouTube channel/playlist.
  - https://codemadness.org/sfeed.html
  - check what/how Liferea does it

## Prior Work

- https://github.com/flexget/flexget
  - Very close to the requirements.
  - Doesn't run on phones/Android.
- https://github.com/jmbannon/ytdl-sub
  - Very close to the requirements.
  - Doesn't run on phones/Android.
- https://github.com/mxpv/podsync
  - Doesn't run on phones/Android.
  - Last release is from 2025 (as of 2026-07-15).
- https://github.com/Sn8z/Poddr
  - Doesn't run on phones/Android.
  - Last release is from 2025 (as of 2026-07-15).
  - Too slow, even on a powerful HP Z2 Mini G5 Workstation.
- https://github.com/tubearchivist/tubearchivist
  - Doesn't run on phones/Android.
  - It's made for archival and as a media server.
  - System requirements indicate it's too resource intensive.
- https://github.com/kieraneglin/pinchflat
  - Doesn't run on phones/Android.
- https://github.com/deniscerri/ytdlnis
  - No OPML support.
  - No RSS feed support.
- https://github.com/junkfood02/Seal
  - No OPML support.
  - No RSS feed support.

## Liferea

- Look into sandboxing an old fixed version that still has support for custom external download tool. https://github.com/89luca89/distrobox
- Not always updating The Impact even when it has new content.
- Calls the conversion filter with an empty stdin, when it decides a feed (eg. The Impact) has no new content.
- Feed fetch spacing option like RSS Guard. https://github.com/lwindolf/liferea/issues/1555
- OPML automatic backup (via plugins?)

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
