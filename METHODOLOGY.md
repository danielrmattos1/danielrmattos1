# Methodology

This document explains exactly how GROUNDTRUTH turns team strength into match
predictions. Nothing here is hidden behind the interface — the goal is a model
you can inspect, challenge, and reproduce.

## 1. Team strength: Elo

Every team carries a **World Football Elo** rating. The convention: a 100-point
gap corresponds to about a **64% win expectancy** for the stronger side at a
neutral venue, where "win expectancy" is the expected share of points
(a win counts 1, a draw 0.5).

Ratings are seeded from public World Football Elo figures for the leading sides
and reasonable estimates for the rest. Every rating is editable, and the app
updates them from real results (Section 5).

Home advantage adds **+65 Elo** to a host nation in its own matches. At the 2026
World Cup only the three hosts (Mexico, Canada, USA) play true home games; all
other group matches are treated as neutral.

## 2. From Elo to expected goals

The effective rating gap `dr` is converted to a goal **supremacy**:

```
S = dr / 165      (clamped to ±2.8)
```

With a baseline of `T = 2.6` total expected goals, each side's expected goals
(xG) are:

```
xG_home = (T + S) / 2
xG_away = (T − S) / 2      (floored at 0.05)
```

The divisor **165** is not arbitrary. It is calibrated by simulation so that the
resulting goal model reproduces the Elo win-expectancy curve almost exactly:

| Rating gap | Target win expectancy | Model win expectancy |
|-----------:|----------------------:|---------------------:|
| 0          | 0.500                 | 0.500                |
| 100        | 0.640                 | 0.640                |
| 200        | 0.760                 | 0.767                |
| 300        | 0.853                 | 0.871                |

The draw rate at an even matchup lands near 27%, in line with international
football.

## 3. From expected goals to a scoreline distribution

Goals for each side are modelled as **independent Poisson processes**. The
probability of a scoreline `(i, j)` is:

```
P(i, j) = Poisson(i; xG_home) × Poisson(j; xG_away)
```

evaluated over a 0–10 × 0–10 grid. A **Dixon–Coles** correction with
`ρ = −0.05` adjusts the four lowest-scoring cells (0-0, 1-0, 0-1, 1-1) so the
model matches how real football clusters around tight results.

Everything else is read directly from this single normalized matrix:

- **Win / draw / loss** — sum the cells where `i > j`, `i = j`, `i < j`.
- **Most likely scorelines** — the highest-probability cells.
- **Over/Under 2.5** — sum cells where `i + j ≥ 3`.
- **Both teams to score** — sum cells where `i ≥ 1` and `j ≥ 1`.
- **Clean-sheet probabilities** — sum the relevant row/column.

Because every output comes from the same matrix, the numbers are always mutually
consistent.

## 4. Match-statistics projection

Beyond the scoreline, the app projects possession, shots, shots on target,
corners, fouls and cards. These are **heuristic projections** derived from xG and
the strength gap — they are clearly labelled as such, because there is no public
per-match shot/foul feed driving them. The mappings (shots scale with xG,
possession with the rating gap, the weaker side commits more fouls and collects
more cards) are tuned to reproduce realistic, internally consistent numbers.

## 5. Learning from results

When a real match finishes, both teams' ratings update with the **official World
Football Elo formula**:

```
R_new = R_old + K · G · (W − We)
```

- `We` — expected result from the rating gap (plus +100 home advantage in the
  update convention): `We = 1 / (1 + 10^(−dr/400))`.
- `W` — actual result for the team (1 win, 0.5 draw, 0 loss).
- `K` — match weight: World Cup finals 60, major tournament 50, qualifier 40,
  other tournament 30, friendly 20.
- `G` — goal-difference index: 1 for a 0–1 goal margin, 1.5 for 2, and
  `(11 + margin) / 8` for 3+.

The update is zero-sum, so a result moves the two teams by equal and opposite
amounts. This is what lets predictions self-correct: a favourite that draws
loses rating to the underdog, and every later prediction reflects it.

## 6. Tournament simulation

The Monte-Carlo simulator samples actual goal counts from each team's Poisson
distribution, settles knockout draws on a lightly Elo-weighted penalty shootout,
and replays the full bracket many thousands of times. Counting how often each
team survives yields advancement and title probabilities. Group qualification
odds work the same way, with already-played results locked in as fixed inputs.

## Limitations

- The model knows strength and results, not tactics, weather, or motivation. The
  Scout feature exists to fold in a little of that, as a bounded manual nudge.
- Exact scorelines are inherently the noisiest output; treat them as the single
  most likely point on a wide distribution, not a forecast.
- Auto-fetched results should always be eyeballed before sharing; manual entry
  is the authority.

---
© 2026 Matin Shahin.
