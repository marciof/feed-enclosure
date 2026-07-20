# Prior Work

_(Last checked: see versions below.)_

## Candidates

https://github.com/AntennaPod/AntennaPod _v3.11.4_

- Audio-oriented (eg. [TVW shows](https://tvw.org/shows/) don't have video).
- [OPML support is only for import/export, not subscriptions storage.](https://antennapod.org/documentation/general/backup)
- No plugin support.
- [Doesn't run on Linux/Windows.](https://antennapod.org/download/)

https://fluidcastapp.com _v1.2.1 Android_

- Not open source.
- Audio-oriented (eg. [TVW shows](https://tvw.org/shows/) don't have video).
- OPML support is only for import/export, not subscriptions storage.
- No plugin support.
- No Atom feed support.

https://grayjay.app _v381 Android_

- [Desktop app still in development?](https://grayjay.app/desktop/)
- [No YouTube playlist update support.](https://github.com/futo-org/grayjay-android/issues/857)
- [No OPML support.](https://github.com/futo-org/grayjay-android/issues/1524)

https://github.com/jmbannon/ytdl-sub _v2026.07.16_

- [Doesn't run on phones/Android.](https://ytdl-sub.readthedocs.io/en/latest/guides/install/index.html)
- [No OPML support.](https://ytdl-sub.readthedocs.io/en/latest/search.html?q=opml)

https://github.com/flexget/flexget _v3.19.28_

- [Doesn't run on phones/Android.](https://www.flexget.com/InstallWizard)
- [No OPML support.](https://github.com/search?q=repo%3AFlexget%2FFlexget%20%22opml%22&type=code)
- [GUI still in development.](https://flexget.com/Web-UI)
- [Changelogs are a list of commits.](https://flexget.com/ChangeLog)

https://github.com/gpodder/gpodder _Git/e05f630f_

- [Doesn't run on phones/Android.](https://gpodder.github.io/#downloads)
- [Last release is from 2024.](https://github.com/gpodder/gpodder/releases)
    - Requires [running from Git sources](https://gpodder.github.io/docs/run-from-git.html) to get [QoL updates](https://github.com/gpodder/gpodder/commit/459f252a430d2c47714c2e87c8197f2964fb3083).
- [Requires manual management of the yt-dlp dependency.](https://gpodder.github.io/docs/extensions/youtubedl.html)
- Requires a manual [custom command](https://gpodder.github.io/docs/extensions/commandondownload.html) to avoid sub-folders per podcast.
    - [It's device syncing specific.](https://gpodder.github.io/docs/user-manual.html#devices-preferences)
    - Eg. `mv -- "$filename" ~/Downloads/`
- Requires creating an extension for unsupported websites.
    - [External service to fix feeds.](https://gpodder.github.io/docs/user-manual.html#using-pipesdigital-to-fix-feeds)
    - [Built-in extensions.](https://gpodder.github.io/docs/extensions.html#default-extensions-included-with-gpodder)

## Alternatives

https://github.com/nickvisionapps/parabolic _v2026.5.0_

- Video download-oriented.
- [Nice UI/UX.](https://github.com/nickvisionapps/parabolic#-screenshots)
- No OPML support.
- [Doesn't run on phones/Android.](https://github.com/nickvisionapps/parabolic#-installation)
- [No (CLI) support for automation.](https://github.com/NickvisionApps/Parabolic/issues/1855)

https://github.com/vanloctech/youwee/ _v0.20.0_

- Video download-oriented.
  - [Supports following channels for automatic downloads.](https://youwee.app/docs/channels)
- No OPML support.
  - [Supports plugins.](https://youwee.app/docs/plugins)
  - [Supports workflows.](https://youwee.app/docs/workflows)
- [Doesn't run on phones/Android.](https://github.com/vanloctech/youwee/#installation)
- App is sluggish ([due to Tauri?](https://github.com/vanloctech/youwee/tree/main/src-tauri)).
- [Uses](https://github.com/vanloctech/youwee/blob/main/bun.lock) [Bun](https://bun.com), which seems [problematic](https://web.archive.org/web/20220824093845/https://twitter.com/oven_sh/status/1562248121656102914#:~:text=grind).
- [Doesn't disclose sponsors?](https://github.com/vanloctech/youwee/commit/cbf78202d200bf6e666bd2bb6911ec43360a40ff)

https://github.com/mhogomchungu/media-downloader/ _v5.6.3_

- Video download-oriented.
  - [Supports subscriptions.](https://github.com/mhogomchungu/media-downloader/wiki/Frequently-Asked-Questions#9-how-do-i-add-subscriptions)
- No OPML support.
  - [Supports plugins.](https://github.com/mhogomchungu/media-downloader/#extensions)
- [Doesn't run on phones/Android.](https://github.com/mhogomchungu/media-downloader#binary-packages)
- [UI is confusing to use.](https://github.com/mhogomchungu/media-downloader#screenshots)
- [Typos in the documentation?](https://github.com/mhogomchungu/media-downloader/wiki/Frequently-Asked-Questions#9-how-do-i-add-subscriptions) (eg. "do _i_ add")

https://github.com/jely2002/youtube-dl-gui _v3.2.1_

- Video download-oriented.
- No OPML support.
- [Doesn't run on phones/Android.](https://github.com/jely2002/youtube-dl-gui#download)
- Not very private? ([Uses Sentry.](https://github.com/jely2002/youtube-dl-gui/blob/main/src/sentry.ts))
- No (CLI) support for automation.

https://github.com/axcore/tartube _v2.5.231_

- Video download-oriented.
  - [Supports subscriptions.](https://github.com/axcore/tartube#6215-importing-from-youtube)
- No OPML support.
- [Doesn't run on phones/Android.](https://github.com/axcore/tartube#3-downloads)
- No plugin support.
- [UI is confusing to use.](https://github.com/axcore/tartube/blob/master/screenshots/)

https://github.com/mxpv/podsync _v2.8.0_

- [Doesn't run on phones/Android.](https://github.com/mxpv/podsync#-features)
- [Last release is from 2025.](https://github.com/mxpv/podsync/releases)

https://github.com/Sn8z/Poddr _v2.1.0_

- [Doesn't run on phones/Android.](https://github.com/Sn8z/Poddr#downloads)
- [Last release is from 2025.](https://github.com/Sn8z/Poddr/releases)
- App is sluggish ([due to Electron?](https://github.com/Sn8z/Poddr/blob/main/electron-builder.yml)).

https://github.com/tubearchivist/tubearchivist _v0.5.10_

- [Doesn't run on phones/Android.](https://github.com/tubearchivist/tubearchivist/releases)
- [It's made for archival and media server.](https://github.com/tubearchivist/tubearchivist#core-functionality)
- [System requirements are too resource intensive.](https://github.com/tubearchivist/tubearchivist/releasesS)

https://github.com/kieraneglin/pinchflat _v2025.9.26_

- [Doesn't run on phones/Android.](https://github.com/kieraneglin/pinchflat#installation)
- [Last release is from 2025.](https://github.com/kieraneglin/pinchflat/releases)
- [No OPML import support?](https://github.com/search?q=repo%3Akieraneglin%2Fpinchflat%20opml&type=code)

https://github.com/deniscerri/ytdlnis _v1.8.9.1_

- [No OPML support.](https://github.com/search?q=repo%3Adeniscerri%2Fytdlnis%20opml&type=code)
- [No RSS feed support.](https://github.com/search?q=repo%3Adeniscerri%2Fytdlnis+%2F%5Cbrss%5Cb%2F&type=code)
- [Typos in the documentation?](https://ytdlnis.org/docs/guides/home#i-have-many-urls-that-i-need-to-download) (eg. "that _i_ need")

https://github.com/junkfood02/Seal _v1.13.1_

- [No OPML support.](https://github.com/search?q=repo%3AJunkFood02%2FSeal%20opml&type=code)
- [Last release is from 2024.](https://github.com/JunkFood02/Seal/releases)
- [No RSS feed support.](https://github.com/search?q=repo%3AJunkFood02%2FSeal%20rss&type=code)

https://github.com/RSS-Bridge/rss-bridge _v2025-08-05_

- RSS bridge only.

https://stacher.io/ _v7.1.11_

- Not open source.
