# ADR-004: Candidate Ranking Methodology

**Status:** Accepted

## Context

The project needed a transparent and repeatable method for ranking franchise bundles and standalone films using historical performance indicators.

The analysis also explored cast and director information to determine whether talent characteristics could improve candidate selection.

## Decision

A weighted percentile-based ranking approach was adopted.

The final ranking weights are:

| Metric | Weight |
|---|---:|
| Historical revenue-to-budget ratio | 50% |
| TMDb rating | 25% |
| TMDb popularity | 25% |
| Cast score | 0% |
| Director score | 0% |
| **Total** | **100%** |

Candidates are ranked within their respective categories: franchise and standalone. Franchise collections containing fewer than two represented films are excluded from the final franchise shortlist.

## Alternatives Considered

- Ranking candidates using historical revenue alone.
- Using equal weights across all metrics.
- Including cast and director counts in the final score.
- Comparing total franchise revenue directly against individual standalone film revenue.

## Implementation

- Calculated candidate-level median return, rating and popularity metrics.
- Converted the metrics into percentile-based scores.
- Applied the selected weights to produce composite candidate scores.
- Generated separate rankings and shortlists for both time windows.
- Analysed cast, directors and producers using TMDb credits.
- Assigned zero weight to cast and director scores because their counts did not provide sufficiently useful discrimination between candidate types.
- Generated `shortlist_stability.csv` to identify candidates appearing in both analysis windows.

## Trade-offs and Limitations

The weights represent analytical judgement rather than statistically validated predictors of licensing success.

TMDb popularity is a current platform indicator, not historical streaming demand.

Because scores are calculated within candidate categories, franchise scores should not be directly compared with standalone scores.

The ranking does not account for actual licensing prices, rights availability, territory restrictions or StreamVault audience demand.

## What Survives the Next Rerun?

The percentile-based ranking pipeline, configurable weights and shortlist stability analysis remain reusable.

The weights can be reviewed when StreamVault provides licensing costs, audience engagement data and additional commercial information.