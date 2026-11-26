# The World in One Picture — 25 November 2026

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/Tigapandax/news-image-20261125-akun1/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/Tigapandax/news-image-20261125-akun1/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

One navy broadsheet that squeezes Wednesday 25 November 2026 into a
single image: tankers burning in the Strait of Hormuz, Ukrainian drones
hitting Russian refineries, Asian markets sliding while the Dow closes
above 50,000 for the first time — plus Egypt, Sudan, Huawei, COP31 and
the rest of the day, down in the ticker.

Bounty: https://make.fun/c/news-image-20261125

## The idea

A front page, not a collage. The biggest story of the day (Hormuz) gets
the full-width lead panel; four more stories share two columns below it;
three shorter items sit in a row of tiles; everything else that still
mattered runs along the "Also today" strip at the bottom.

## What is inside the picture

- **Lead — Strait of Hormuz:** sea mines set two tankers ablaze; Houthi
  rebels say they also struck the Ras Tanura refinery.
- **Ukraine:** Ukrainian drones set two Rosneft refineries (Syzran and
  Kuibyshev) on fire; Russian strikes kill two people in Odesa.
- **Markets:** KOSPI −6.2% and Nikkei −2.8%, while the Dow closes above
  50,000 for the first time in history.
- **Tech:** Huawei found guilty on 10 of 12 counts by a Brooklyn jury.
- **Egypt:** a fuel tanker fire near Cairo kills at least 31 people.
- **Sudan:** an RSF drone strike kills 19 civilians.
- **Climate:** Pope Leo XIV laments the failure of COP31; Australia signs
  a treaty with Solomon Islands.
- **Also today:** Shenzhou-24 docks with Tiangong, Cartagena supermarket
  hostages are freed, the Bogor mine toll reaches six, and the Macy's
  parade is delayed by a storm.

## Build the poster

```sh
python3 draw.py
```

This paints `entry.png` (1024×1008 px) with Pillow. Nothing else is
needed at build time.

## Run the entry

```sh
python3 main.py
```

`main.py` uses only the standard library. It copies `entry.png` into
`$MAKEFUN_OUTPUT_DIR` (or `/output` when the variable is unset).

## Files

- `draw.py` — paints the poster with Pillow (build time only).
- `main.py` — ships the finished `entry.png` as the entry (stdlib only).
- `entry.png` — the rendered poster, 1024×1008 px.
- `LICENSE` — MIT.
