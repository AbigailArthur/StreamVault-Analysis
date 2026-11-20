# ADR-002: Franchise and Standalone Classification

**Status:** Accepted

## Context

The project needed a consistent way to compare franchise bundles against standalone films. The dataset contained 112 successfully retrieved movies, of which 96 had TMDb collection information and 16 did not.

## Decision

TMDb collection membership was selected as the operational classification rule.

- Movies with a collection ID are classified as franchise films.
- Movies without a collection ID are classified as standalone candidates.
- Franchise films are grouped by collection ID to form bundle candidates.
- Standalone films are treated as individual candidates.

## Alternatives Considered

- Manually classifying franchises based on movie titles.
- Treating every movie as an individual candidate.
- Grouping films using production companies or shared cast members.

## Implementation

- Identified 32 unique TMDb collections.
- Grouped the 96 collection-linked films into franchise candidates.
- Treated the remaining 16 films as standalone candidates.
- Compared franchise bundles and standalone films across all years and from 2000 onward.
- Excluded franchise collections containing only one represented film from the final franchise shortlist.

## Trade-offs and Limitations

TMDb collection metadata provides a consistent and reproducible classification method. However, some films may belong to franchises without having a collection ID.

The analysis also represents only titles included in the supplied dataset. A collection may have additional films that were not provided.

Therefore, the classification is an operational assumption rather than a definitive statement about every film's franchise relationship.

## What Survives the Next Rerun?

The collection-based classification and grouping logic remain reusable. Newly supplied movies can be classified automatically using their TMDb collection information.