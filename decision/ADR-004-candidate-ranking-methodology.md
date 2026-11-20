# ADR-004: Candidate Ranking Methodology

**Status:** Accepted

## Context

The project needed a transparent and repeatable method for ranking franchise bundles and standalone films using historical performance indicators.

The analysis also explored cast, director and producer information to determine whether talent characteristics could support candidate selection.

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

Candidates are ranked separately within their respective categories: franchise and standalone.

Franchise collections containing fewer than two represented films are excluded from the final franchise shortlist.

Candidate records are joined to candidate-level talent metrics using `candidate_id` and `candidate_type`, with one-to-one merge validation to prevent incorrect or duplicated matches.

Cast and director indicators are retained as descriptive measures but do not influence the weighted ranking because their assigned weights are zero.

## Alternatives Considered

- Ranking candidates using historical revenue alone.
- Using equal weights across all metrics.
- Including cast and director counts in the final score.
- Comparing total franchise revenue directly against individual standalone film revenue.
- Joining candidate and talent records using candidate names instead of stable identifiers.

## Implementation

- Calculated candidate-level median return, rating and popularity metrics.
- Converted the metrics into percentile-based scores.
- Applied the selected weights to produce composite candidate scores.
- Calculated cast and director counts relative to represented film counts.
- Retained producer counts and talent names as supporting descriptive information.
- Merged candidate and talent datasets using `candidate_id` and `candidate_type`.
- Validated merge uniqueness and matching records.
- Generated separate rankings and shortlists for both time windows.
- Analysed individual actors, directors and producers using the standardized TMDb credits dataset.
- Generated `shortlist_stability.csv` to identify candidates appearing in both analysis windows.

## Trade-offs and Limitations

The weights represent analytical judgement rather than statistically validated predictors of licensing success.

TMDb popularity is a platform indicator, not historical streaming demand.

Because scores are calculated within candidate categories, franchise scores should not be directly compared with standalone scores.

Talent indicators are descriptive and do not establish that an individual's involvement caused a film's financial performance.

The ranking does not account for actual licensing prices, rights availability, territory restrictions or StreamVault audience demand.

## What Survives the Next Rerun?

The percentile-based ranking pipeline, configurable weights, identifier-based candidate merging and shortlist stability analysis remain reusable.

The weights can be reviewed when StreamVault provides licensing costs, audience engagement data and additional commercial information.