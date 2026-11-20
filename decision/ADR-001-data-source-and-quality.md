# ADR-001: Data Source and Quality Management

**Status:** Accepted

## Context

The project required movie, financial, cast and crew information for 127 expected TMDb identifiers. The supplied identifier file contained only 126 rows. Some records were duplicated, invalid, missing or unavailable through the TMDb API.

## Decision

TMDb was selected as the primary data source. The acquisition pipeline was designed to preserve the original input records, validate identifiers, retrieve movie details and credits, and separate problematic records for review.

## Alternatives Considered

- Manually removing invalid and duplicate identifiers before acquisition.
- Discarding unavailable records without maintaining an audit trail.
- Using unverified alternative sources to replace unavailable records.

## Implementation

- Audited all 126 supplied rows.
- Identified 117 unique valid identifiers.
- Retrieved 112 unique movies and 32,759 credit records.
- Identified six duplicate rows, two invalid identifiers, one missing identifier and five unavailable movie IDs.
- Stored raw API responses under `data/raw/`.
- Stored cleaned datasets under `data/processed/`.
- Preserved problematic records in `data/quarantine/`.
- Generated `id_audit.csv` to document the outcome of every supplied row.

## Trade-offs and Limitations

TMDb provides structured movie and credit information, but its financial figures and metadata are not independently verified. Five valid identifiers could not be retrieved, and the missing 127th identifier could not be investigated.

## What Survives the Next Rerun?

The acquisition, validation, audit and quarantine procedures remain reusable. New identifiers can be supplied and processed without manually changing the pipeline.