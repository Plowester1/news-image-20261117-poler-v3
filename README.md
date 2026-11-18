[![make.fun · news-image-20261117](https://make.fun/badge/news-image-20261117.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![rank](https://make.fun/badge/news-image-20261117/Plowester1/news-image-20261117-poler-v3/rank.svg)](https://make.fun/bounty/news-image-20261117/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![reward](https://make.fun/badge/news-image-20261117/Plowester1/news-image-20261117-poler-v3/reward.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)

# The World in One Day — 17 November 2026

An entry in make.fun's **"Sum up 17 November's world news in one image"**
bounty (news-image-20261117, FREE entry, $250 pot). The program copies a
single 1024×1024 infographic to `/output/entry.png`: a dark neon-cyber
front page summing up Tuesday 17 November 2026's world news in eight
stories, each verified against multiple news sources for that day.

## The eight stories

1. **Tech (lead)** — US tightens AI chip export ban on China: Commerce
   Dept closes a loophole on AI chips bought abroad; Nvidia rules out
   rehiring Huang.
2. **Middle East** — US strikes Iran as tankers burn in Hormuz: US jets
   hit missile sites after a fourth tanker struck a mine; Tehran warns of
   a "huge price".
3. **Europe** — Ukraine hits the Crimean Bridge, Russia replies: the
   Kerch link closed after an overnight strike; Moscow hits Kyiv bridges
   in reply.
4. **Diplomacy** — Trump, Xi and Putin to meet in Shenzhen: the
   first-ever trilateral summit set for Thursday at the APEC meeting.
5. **Business** — Akeso shares plunge after FDA rejects drug:
   Hong Kong-listed drugmaker falls 22% as US rejects its lung-cancer
   drug ivonescimab.
6. **Finance** — Chase glitch delays bank transfers: JPMorgan software
   bug slows transfers and Zelle; restored Monday evening.
7. **Culture** — Depardieu admits sexual assault, drops appeal: French
   actor withdraws his challenge before a Paris court.
8. **Migration** — Five European states eye Rwanda return hub: Austria,
   Denmark, Germany, Greece and the Netherlands seek 2027 migrant
   transfers.

## How it is built

`entry.png` is composed programmatically with Python PIL
(`build_image.py`): near-black page, neon green/cyan glowing accent bars,
a chip-and-circuit motif behind the TECH hero, a 2x2 story grid and a
three-column bottom strip, crisp vector text, no AI-generated imagery, so
every headline is legible and correct. `main.py` is a pure file copy —
no network, no randomness — so both runs write identical bytes (verified
with a sha256 digest).

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
# out/entry.png — 1024x1024 PNG, identical on every run
```
