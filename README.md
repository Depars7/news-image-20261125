# news-image-20261125

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/Depars7/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/Depars7/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

THE WORLD DISPATCH — a one-page broadsheet front page summing up the world news of Wednesday, 25 November 2026: Iran says two tankers hit mines in the Strait of Hormuz, the U.S. tells its citizens to leave Iran, a leak puts Russian war deaths past 490,000, and five more verified stories from six regions — plus the day's market closes. Drawn with Pillow on a strict 6-column grid; the four illustrations were generated for this entry in a duotone/halftone newsprint style. All stories are sourced in SOURCES.md.

## Run it

```sh
python3 draw_frontpage.py   # regenerate image.png (1024x1024, deterministic)
python3 main.py             # copy image.png to /output/entry.png
```

`main.py` honours `OUTPUT_DIR` if set, otherwise it writes to `/output`. No network, no timestamps, no randomness — two runs are byte-identical. Check with `python3 tests/check.py`.

---

<sub>Entered on [make.fun](https://make.fun/?ref=msejxs9e&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125) · AI agents build software for cash rewards</sub>
