# StreamVault Data Findings and Quality Assessment

## 1. Executive Summary

The original assignment specified 127 TMDb identifiers. However, the supplied `id_list.csv` contains only 126 rows. After validation and retrieval, 112 unique movies were successfully collected, together with 32,759 cast and crew records.

The analysis identified missing, invalid, duplicate and unavailable identifiers. All 126 supplied rows were accounted for in the audit, but the absent 127th identifier could not be investigated because it was not provided.

The data preparation and validation pipelines were improved to support identifier normalization, schema validation, numeric checks, duplicate detection and standardized movie and credits datasets.

## 2. Identifier Audit

| Record status | Count |
|---|---:|
| Successfully retrieved unique movies | 112 |
| Unavailable IDs (404 responses) | 5 |
| Duplicate ID rows | 6 |
| Invalid IDs | 2 |
| Missing ID rows | 1 |
| **Total supplied rows** | **126** |

### Key findings

- Six duplicate rows involved IDs 155, 680, 278, 603, 1891 and 550.
- Two invalid identifiers were `-1` and `tt0468569`.
- One row contained a missing identifier.
- Five unique valid IDs returned HTTP 404 responses from both the movie details and credits endpoints: 8471293, 9412887, 8471294, 9412888 and 7733901.
- The input contained 117 unique valid identifiers before retrieval.

The identifier processing pipeline normalizes numeric identifiers before duplicate detection. This ensures that equivalent representations, such as `155` and `155.0`, are treated as the same identifier.

Invalid, missing, duplicate and unavailable records are tracked through the audit and quarantine processes rather than silently discarded.

## 3. Retrieved Dataset

| Dataset | Records |
|---|---:|
| Movie records | 112 |
| Credit records | 32,759 |
| Unique movies represented in credits | 112 |
| Movies with collection information | 96 |
| Movies without collection information | 16 |
| Unique TMDb collections | 32 |

The prepared movie dataset contains 25 columns, including movie identifiers, titles, release dates, financial information, ratings, popularity, production details and collection information.

The credits dataset contains seven standardized fields:

- `movie_id`
- `person_id`
- `name`
- `job`
- `character`
- `department`
- `order`

Cast and crew records are represented in a consistent structure to support talent-level analysis.

A separate analysis dataset contains 22 fields, including derived release year, candidate classification, gross-minus-budget and revenue-to-budget metrics.

## 4. Data Validation Findings

The validation pipeline checks required schemas, duplicate movie identifiers, movie identity fields, numeric fields and financial values.

| Validation check | Latest result |
|---|---:|
| Movie schema contract | Passed |
| Credits schema contract | Passed |
| Invalid budget values | 0 |
| Invalid revenue values | 0 |
| Invalid vote average values | 0 |
| Invalid vote count values | 0 |
| Invalid popularity values | 0 |
| Negative financial records | 0 |
| Invalid movie records quarantined | 0 |
| Missing budgets | 0 |
| Missing revenues | 0 |

The pipeline converts invalid numeric values to missing values and identifies records requiring quarantine. It also checks for missing movie identifiers and titles.

The analysis pipeline separately checks release dates and reports invalid or missing dates. The latest analysis run reported zero missing or invalid release dates.

No invalid numeric or financial records were identified in the latest validation run. However, successful validation does not independently establish the accuracy or completeness of TMDb's reported information.

## 5. Coverage Limitations

The retrieved films span 1966 to 2019. There are 71 films released from 2000 onward.

No films released after 2019 were present in the successfully retrieved dataset. Consequently, the analysis may not reflect more recent film performance, audience preferences or franchise developments.

The 2000-onward analysis provides a more recent comparison window within the available data, but it does not solve the absence of post-2019 titles.

## 6. Classification Limitations

Franchise membership was determined using TMDb collection information.

- Films with a collection ID were classified as franchise films and grouped by collection.
- Films without a collection ID were treated as standalone candidates.

The 16 films without collection information are operationally treated as standalone films. This does not prove that every one is an independent film or has no sequel or franchise relationship.

Additionally, the analysis only represents films available in the supplied identifier list. A collection may contain other titles that were not included in the source data.

## 7. Financial Data Limitations

TMDb budget and revenue figures represent historical production budgets and reported box-office revenue.

The following distinctions are important:

- Revenue minus budget is not net profit.
- Revenue-to-budget ratio is not licensing return on investment.
- Historical box-office performance does not establish future streaming demand.
- Production budgets do not indicate current licensing prices or affordability.

The dataset does not contain licensing fees, rights availability, territories, exclusivity, licensing windows or StreamVault audience demand.

Therefore, the analysis can identify historically promising candidates but cannot independently establish which titles can be acquired within the $14 million licensing budget.

## 8. Ranked Risk Assessment and Actions

| Rank | Data issue / risk | Severity | How it was detected | Action taken | Impact on analysis and recommendation |
|---|---|---|---|---|---|
| 1 | Missing licensing prices, rights information and StreamVault demand data | Critical | Confirmed by reviewing the fields available in the supplied dataset and TMDb responses | Documented as an unresolved commercial data gap | Prevents reliable licensing ROI calculations, affordability assessment and a defensible allocation of the $14 million budget |
| 2 | Missing 127th identifier | High | Compared the 127 identifiers specified in the brief with the 126 rows in `id_list.csv` | Recorded the discrepancy; did not invent or substitute an identifier | The analysis may not cover the complete intended candidate population |
| 3 | No titles released after 2019 | High | Examined the minimum and maximum valid release years | Used both all-years and 2000-onward analysis windows and disclosed the coverage limitation | Recommendations may not reflect recent releases, audience preferences or current franchise performance |
| 4 | TMDb financial figures are not independently verified | High | Reviewed the source and meaning of budget and revenue fields | Retained the figures but documented their limitations | Historical revenue-to-budget ratios may not represent actual profitability or future licensing value |
| 5 | Five valid IDs returned HTTP 404 responses | Medium | Sent requests to both TMDb movie-details and credits endpoints and recorded the responses | Preserved the failed records in the audit and quarantine outputs | Reduced the successfully analysed candidate pool by five unique movies |
| 6 | Incomplete franchise representation | Medium | Compared collection information among retrieved movies and considered the supplied-list limitation | Grouped only available collection-linked titles and disclosed that collections may be incomplete | Franchise-level results may not represent the performance of every film in a collection |
| 7 | Six duplicate identifier rows | Medium | Compared identifier values and identified repeated IDs | Normalized identifiers before duplicate detection and preserved duplicate rows in the audit | Prevented duplicate records from inflating movie counts or distorting analysis |
| 8 | Two invalid identifiers and one missing identifier | Medium | Applied identifier validation before API retrieval | Preserved problematic records in the audit and quarantine outputs | Prevented retrieval of the affected records and reduced source coverage |
| 9 | Inconsistent raw movie and credits structures | Low | Compared the retrieved API structures with the required analytical schemas | Implemented schema validation, identifier normalization and standardized movie and credits outputs | Improved consistency and reliability across downstream analysis pipelines |

### Overall Risk Interpretation

The most important unresolved risks are the absence of commercial licensing information, the missing source identifier and the lack of post-2019 titles.

The technical data-quality issues were addressed through identifier normalization, schema validation, duplicate detection, numeric checks, API error tracking and quarantine procedures.

The standardized credits structure also improves consistency in identifying cast, directors and producers for individual talent analysis.

However, the commercial information gaps cannot be resolved using TMDb data alone. StreamVault should obtain licensing quotes, rights information and internal audience-demand evidence before making a final investment decision.

## 9. Conclusion

The data preparation process produced a usable dataset of 112 movies and 32,759 credit records. Identifier issues were documented, validated and preserved through the audit and quarantine processes.

The improved pipelines provide standardized movie and credits datasets, stronger schema checks and more consistent financial and talent analysis inputs.

The dataset supports a historical comparison of franchise bundles and standalone films across two release windows. However, the results should be treated as screening evidence rather than a final licensing investment decision.

Before committing the $14 million budget, StreamVault should obtain current licensing quotes, rights availability, title-level rights terms, more recent performance data and internal audience-demand information.