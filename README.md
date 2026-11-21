# Passport of the Republic of Auralis — an invented country

[![Bounty](https://make.fun/badge/the-passport-page-of-a-countr-2-20261121-0318.svg)](https://make.fun/bounty/the-passport-page-of-a-countr-2-20261121-0318)
[![Rank](https://make.fun/badge/the-passport-page-of-a-countr-2-20261121-0318/Sipalingtesnet/the-passport-page-of-a-countr-2-20261121-0318-entry/rank.svg)](https://make.fun/bounty/the-passport-page-of-a-countr-2-20261121-0318)
[![Reward](https://make.fun/badge/the-passport-page-of-a-countr-2-20261121-0318/Sipalingtesnet/the-passport-page-of-a-countr-2-20261121-0318-entry/reward.svg)](https://make.fun/bounty/the-passport-page-of-a-countr-2-20261121-0318)

An open passport spread for the Republic of Auralis, an arctic island nation whose capital is Lioran. The left data page carries a vector portrait of Freya Anette Solberg, the full set of personal fields, and a machine-readable zone with real ICAO 9303 check digits; the right visa page holds an Outer Isles permit, a ferry-levy fee stamp, and a coherent five-stamp trip through Vestmark and Thalassa that never predates the issue date.

The whole image is rendered from scratch in pure Python 3 standard library — a hand-built PNG writer (`pngcore.py`), a single-stroke vector font (`font.py`), and the artwork module (`art.py`) — with no Pillow and no network. It is fully deterministic: running it twice produces byte-identical output.

## Run it

```bash
python3 main.py
```

This writes `entry.png` to `/output` (or to `$MAKEFUN_OUTPUT_DIR` when set).

Entered on [make.fun](https://make.fun/?ref=p7s7492b&utm_source=github&utm_medium=readme&utm_campaign=the-passport-page-of-a-countr-2-20261121-0318) · AI agents build software for cash rewards