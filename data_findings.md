# StreamVault Data Findings and Quality Assessment

## 1. Executive Summary

The original assignment specified 127 TMDb identifiers. However, the supplied `id_list.csv` contains only 126 rows. After validation and retrieval, 112 unique movies were successfully collected, together with 32,759 cast and crew records.

The analysis identified missing, invalid, duplicate and unavailable identifiers. All 126 supplied rows were accounted for in the audit, but the absent 127th identifier could not be investigated because it was not provided.

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

The audit and quarantine files preserve the problematic records for review rather than silently discarding them.

## 3. Retrieved Dataset

| Dataset | Records |
|---|---:|
| Movie records | 112 |
| Credit records | 32,759 |
| Unique movies represented in credits | 112 |
| Movies with collection information | 96 |
| Movies without collection information | 16 |
| Unique TMDb collections | 32 |

The retrieved movie dataset contains 18 columns, including release date, runtime, budget, revenue, rating, popularity and collection information.

## 4. Data Validation Findings

The validation process checked financial fields, movie attributes and release dates.

| Validation check | Result |
|---|---:|
| Missing budgets | 0 |
| Missing revenues | 0 |
| Negative budgets | 0 |
| Negative revenues | 0 |
| Missing runtime values | 0 |
| Zero runtime values | 0 |
| Invalid release dates | 0 |

No missing or negative values were detected in the retrieved budget and revenue fields. However, this does not independently establish that TMDb's financial figures are accurate or complete.

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
| 7 | Six duplicate identifier rows | Medium | Compared identifier values and identified repeated IDs | Preserved duplicate rows in the audit while preventing them from inflating the unique movie analysis | Could have overstated movie counts and distorted analysis if duplicates were treated as separate films |
| 8 | Two invalid identifiers and one missing identifier | Medium | Applied identifier validation before API retrieval | Preserved all three records in the quarantine output | Prevented retrieval of the affected records and reduced source coverage |

### Overall Risk Interpretation

The most important unresolved risks are the absence of commercial licensing information, the missing source identifier and the lack of post-2019 titles.

The technical data-quality issues were handled through validation, duplicate detection, API error tracking and quarantine. However, the commercial information gaps cannot be resolved using TMDb data alone. StreamVault should obtain licensing quotes, rights information and internal audience-demand evidence before making a final investment decision.

## 9. Conclusion

The data preparation process produced a usable dataset of 112 movies and 32,759 credit records. Identifier issues were documented, quarantined and preserved for transparency.

The dataset supports a historical comparison of franchise bundles and standalone films across two release windows. However, the results should be treated as screening evidence rather than a final licensing investment decision.

Before committing the $14 million budget, StreamVault should obtain current licensing quotes, rights availability, title-level rights terms, more recent performance data and internal audience demand information.