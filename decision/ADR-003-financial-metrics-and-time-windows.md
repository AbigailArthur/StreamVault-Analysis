# ADR-003: Financial Metrics and Time-Window Selection

**Status:** Accepted

## Context

The project needed to compare historical performance between franchise bundles and standalone films while accounting for differences in release periods and candidate sizes.

The available dataset covered films released between 1966 and 2019.

## Decision

Two analysis windows were adopted:

1. All years: includes every successfully retrieved movie.
2. 2000 onward: provides a more recent comparison window within the available dataset.

Median film-level metrics were selected as the primary comparison measures to reduce the influence of unusually high-performing films.

The following metrics were calculated:

- Median production budget.
- Median box-office revenue.
- Median revenue-to-budget ratio.
- Median gross revenue minus production budget.

## Alternatives Considered

- Using only the all-years dataset.
- Using only films released from 2000 onward.
- Comparing franchise and standalone candidates using total revenue alone.
- Using average financial performance instead of median performance.

## Implementation

- Created separate comparison datasets for both time windows.
- Grouped franchise films by collection and evaluated standalone films individually.
- Calculated candidate-level median film budget, revenue and return ratio.
- Generated comparison summaries and candidate metrics for both periods.
- Created a shortlist stability analysis to identify candidates appearing in both time windows.

## Trade-offs and Limitations

Median metrics reduce the influence of extreme values but do not eliminate weaknesses in historical financial data.

Revenue-to-budget ratio measures historical box-office revenue relative to production budget. It is not net profit or licensing ROI.

The 2000-onward analysis still excludes releases after 2019 because no newer titles were available in the supplied dataset.

## What Survives the Next Rerun?

Both analysis windows, the median-based comparison approach and the shortlist stability assessment remain reusable. Newer records can be incorporated without changing the overall methodology.