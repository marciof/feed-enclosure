# General

- Need to find alternatives to Liferea? It removed the external downloaders option, and may remove more or go unmaintained? Check which have support for plugins: Akregator, RSS Guard, Thundebird.
- Need to find alternatives to Media Downloader? GUI isn't very intuitive. Check which have support for automatic downloading: Parabolic.
- Replace entire `feed_enclosure` with `ext_cmd`?
  - It'll either work with https://github.com/mhogomchungu/media-downloader or with yt-dlp via command line (via shell scripting or a Python wrapper)
  - Could https://codeberg.org/lwindolf/lzone.de work instead? Using Web APIs such as Native Messaging?
  - Confirm with author and fix `ext_cmd` to be API compliant.
- `shellcheck` scripts
- Helper script for getting an RSS feed URL from a YouTube channel/playlist.

# Syncing

- emojis break Dropbox upload on Linux? See yt-dlp option `--restrict-filenames` for videos like this: https://www.youtube.com/v/8rB4Y-uE1ng
- Sync VLC last video position between devices.
- Syncthing for faster efficient syncing within the local network between devices? Double check Dropbox.

# Videos

- Skip livestreams option.
- Embed metadata, subtitles and thumbnails in downloaded videos.
- Skip YouTube shorts (vertical videos) option.
- Skip video if mtime is more than 1 year in the past (eg. Last Week Tonight uploading old episodes) option.
- Parse video episodes from [The Impact](https://tvw.org/shows/the-impact/) (plus [its others shows](https://tvw.org/shows/)) into a feed for downloading, instead of the audio-only podcasts.
- RSS feed from Instagram feed, for https://www.instagram.com/therapyjeff/
- Make it possible to watch a video as it's being downloaded before it finishes.
- Video summarizing option? TL;DW Too Long; Didn't watch, https://tldw.tube/, https://news.ycombinator.com/item?id=43021044

# Media Downloader

- Does it handle offline/errors and retries/resumes?
- How to reliably set default options?
- How long does the batch downloader list can get?
- Backup settings: `~/.var/app/io.github.mhogomchungu.media-downloader/data/media-downloader/`

# Liferea

- Feed fetch spacing option like RSS Guard.
- OPML automatic backup (via Liferea plugins?)
- Notification tray icon flashes too much, too quickly with new feed items, and is distracting (KDE Plasma 6).

# PWA?

Pros:

- Available anywhere, no installation, always up to date on the browser.
- Also available as a CLI via Nodejs.

Cons:

- Need to potentially write/rewrite a lot (feed parsing, HTTP caching, feed checking intervals, database, downloader, resumable downloads, download jobs, UI/UX).
  - Maybe can reuse some Python libraries and run them in the browser?
  - Open feasibility question about tools such as `ffmpeg` used by programs like `yt-dlp`, as well as performance.
  - Too much complexity and bloat?
- Can't write videos to a folder automatically (yet?).
  - Can use Chrome on desktop?
- CORS is a blocker.
  - Can use a localhost proxy web server?
  - Too much complexity and bloat?

Prototyping?

- Feature YouTube support (CORS).
- Feature audio/video merging on device (ffmpeg WASM).
- See: https://github.com/prettydiff/share-file-systems
- See: https://web.dev/file-system-access/
- See: https://web.dev/browser-fs-access/
- See: https://googlechromelabs.github.io/text-editor/
- See: https://developer.mozilla.org/en-US/docs/Web/API/File_System_Access_API
- See: https://developer.mozilla.org/en-US/docs/Web/API/HTMLInputElement/webkitdirectory
- See: https://github.com/GoogleChromeLabs/browser-fs-access
- See: https://bugs.chromium.org/p/chromium/issues/detail?id=1011535 
