# General

- Subscribe to mailing lists so I'm up to date with new features and breaking changes.
- Need to find alternatives to Liferea? It removed the external downloaders option, and may remove more or go unmaintained? Check which have support for plugins: Akregator, RSS Guard, Thundebird.
- Replace entire `feed_enclosure` with `ext_cmd`?
  - It'll either work with a GUI media downloader app, or directly with yt-dlp via command line?
    - https://github.com/yt-dlp/yt-dlp#developing-plugins
    - https://yt-dlp-yt-dlp.mintlify.app/guides/post-processing
  - Could https://codeberg.org/lwindolf/lzone.de work instead? Using Web APIs such as Native Messaging?
  - Candidates (need to support OPML for data portability, and some form of plugin/extension to download enclosures):
    - [RSS Guard](https://github.com/martinrotter/rssguard/issues/1952#issuecomment-4609281030)
    - [Akregator](https://github.com/KDE/akregator/)
    - [Alligator](https://github.com/kde/alligator)
    - [Thunderbird](https://reviewers.addons.thunderbird.net/en-us/thunderbird/tag/rss) (see also [custom CSS](https://reddit.com/r/Thunderbird/comments/1fhyvvq/kind_of_loving_thunderbird_as_an_rss_reader_right/lo3dpgu/))
  - New project structure?
    - `converters/` (anything -> feed, eg. TVW show page HTML -> RSS)
    - `relays/` (data passing glue logic, eg. Liferea plugin)
    - `wrappers/` (helper scripts, eg. Youwee CLI script)
  - Headless workflow alternative as well? With simple GUI options?
    - https://github.com/chriskiehl/Gooey
    - https://github.com/PySimpleGUI/PySimpleGUI
    - https://github.com/alfiopuglisi/guietta
    - https://tools.suckless.org/dmenu/
- Helper script for getting an RSS feed URL from a YouTube channel/playlist.
  - https://codemadness.org/sfeed.html
  - check what/how Liferea does it

# Syncing

- Do filenames with emojis break Dropbox syncing? See also https://github.com/woodgern/confusables
- Sync VLC last video position between devices.
- Syncthing for faster efficient syncing within the local network between devices? Double check Dropbox.

# Videos

- Need to find other GUI alternatives?
  - Parabolic, but see https://github.com/NickvisionApps/Parabolic/issues/1855
- Embed subtitles in downloaded videos.
- Skip YouTube shorts (vertical videos) option.
- Skip video if mtime is more than 1 year in the past (eg. Last Week Tonight uploading old episodes) option.
- RSS feed from Instagram feed (for https://www.instagram.com/therapyjeff/)
  - https://github.com/CloakHQ/CloakBrowser
  - https://github.com/jpjacobpadilla/Stealth-Requests
  - https://github.com/lexiforest/curl_cffi
  - https://github.com/microsoft/playwright-python
  - https://github.com/instaloader/instaloader
- Make it possible to watch a video as it's being downloaded before it finishes.
- Video summarizing option? TL;DW Too Long; Didn't watch, https://tldw.tube/, https://news.ycombinator.com/item?id=43021044

## Youwee

- Sort download queue from recent to old.
- App is too sluggish/slow?
- Disable previews altogether in the YouTube section?
- Follow dark/light mode from OS?
- Show timestamp when download was added/finished in the queue.
- Change number of parallel downloads during downloading.

# Liferea

- Feed fetch spacing option like RSS Guard.
- OPML automatic backup (via Liferea plugins?)
- Find Wayland alternative to `kdocker` for tray icon?
  - [v2 removed Trayicon plugin](https://github.com/lwindolf/liferea/releases/tag/v2.0-RC1)
  - https://github.com/Druco/WKDocker/

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
