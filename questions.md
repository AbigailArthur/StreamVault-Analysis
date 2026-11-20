# StreamVault Questions, Decisions and Outstanding Issues

## 1. Questions for the Client

These questions identify information needed to strengthen the analysis and support the final licensing decision.

| Area | Question for the Client | What We Did / Solution Applied | What Remains |
|---|---|---|---|
| Budget | Is the $14 million budget inclusive of all licensing and transaction costs? | Compared historical production budgets and revenues to assess candidate performance. | Obtain actual licensing quotes and confirm the available acquisition budget. |
| Rights | Which territories is StreamVault targeting? | Identified and ranked potential franchise and standalone candidates. | Confirm rights availability and pricing for each territory. |
| Licensing terms | What licensing duration and exclusivity does StreamVault prefer? | Prepared a shortlist of promising candidates for further consideration. | Obtain licensing terms and compare their commercial implications. |
| Bundle strategy | Must franchise titles be acquired as complete collections? | Grouped franchise films using TMDb collection IDs and compared them against standalone films. | Confirm whether complete bundles or individual titles can be licensed. |
| Audience demand | Which genres, titles and franchises perform best with StreamVault's audience? | Used TMDb ratings and popularity as historical screening indicators. | Obtain StreamVault's internal viewing and audience data. |
| Performance | Are viewing hours, completion rates and retention metrics available? | Used historical revenue-to-budget ratios, ratings and popularity to rank candidates. | Incorporate platform engagement metrics to assess actual streaming demand. |
| Availability | Are there preferred distributors or existing licensing relationships? | Produced a shortlist of candidates for potential negotiations. | Verify distributors, current rights holders and title availability. |
| Data coverage | Can the missing 127th identifier and newer title data be supplied? | Audited all 126 supplied rows, identified the missing identifier and created a separate 2000-onward comparison. | Obtain the missing identifier and updated film records, particularly post-2019 releases. |

## 2. Analytical Questions and Solutions Applied

| Analytical question or challenge | What We Did / Solution Applied | Remaining limitation |
|---|---|---|
| How do we handle duplicate movie IDs? | Identified six duplicate rows and preserved them in the audit and quarantine records. | Confirm whether the source list can be corrected. |
| How do we handle invalid and missing IDs? | Identified two invalid IDs and one missing ID. Preserved them in the audit and quarantine records. | Obtain corrected identifiers where possible. |
| What happens when TMDb cannot retrieve a movie? | Identified five IDs returning 404 responses from both endpoints and recorded them as unavailable. | Confirm whether alternative records or sources exist. |
| How do we ensure all supplied records are accounted for? | Created an identifier audit and accounted for all 126 supplied rows. | The 127th expected identifier was not supplied, so it could not be audited. |
| How should franchise films be identified? | Used TMDb collection IDs to group films into franchise candidates. | Collection metadata may be incomplete and may not represent every title in a franchise. |
| How should films without collection IDs be treated? | Classified the 16 films without collection information as standalone candidates. | Verify whether any are associated with franchises outside TMDb collection metadata. |
| How do we prevent large franchises from dominating the comparison? | Used median film-level metrics rather than relying only on aggregate franchise revenue and budget. | Median historical performance still does not establish licensing value. |
| How do we account for changes in film performance over time? | Ran separate all-years and 2000-onward analyses and generated a shortlist stability comparison. | The latest available release year is 2019, so recent market developments are not represented. |
| How should candidate performance be ranked? | Applied a weighted score: 50% revenue-to-budget return, 25% rating and 25% popularity. | The ranking is a screening method, not a prediction of licensing ROI. |
| Why were cast and director scores assigned zero weight? | Examined candidate-level talent counts and added individual actor/director historical performance metrics. Kept their ranking weights at zero because the available sample does not establish independent predictive value. | Talent findings can support qualitative negotiations but should not be treated as proof of future performance. |
| How do we identify potentially valuable actors and directors? | Calculated individual film counts, median revenue-to-budget ratios, share of films above budget and median ratings. Used at least two films as a preliminary screening threshold. | Small samples and shared franchise appearances limit the strength of these signals. |
| How do we select the final candidates? | Ranked franchise and standalone candidates separately and selected the top three franchise candidates and five standalone candidates in each period. | Final acquisition decisions require rights, pricing and audience-demand evidence. |
| What happens when the recommendation changes between periods? | Generated a shortlist stability comparison to identify candidates appearing in both periods and those appearing in only one. | Kwame should consider the time-window differences before approving a shortlist. |
| Can historical revenue-to-budget ratios determine the licensing budget allocation? | Used the ratios to screen historical performance and compare candidate groups. | No defensible dollar allocation can be made without licensing prices, rights terms and expected platform contribution. |

## 3. Technical and Reproducibility Questions

| Question or challenge | What We Did / Solution Applied | Remaining limitation |
|---|---|---|
| Can the analysis run without manual data editing? | Built an automated pipeline covering acquisition, preparation, validation, feature engineering, comparison, candidate analysis, talent analysis and ranking. | Adjoa should verify the process from a clean clone. |
| Can the project retrieve data for approximately 500 IDs? | Centralized API configuration, used automated acquisition and processing scripts, and avoided a fixed candidate count in the analysis design. | A full 500-ID run still needs to be tested to confirm runtime, API limits and memory use. |
| How are API failures handled? | Recorded failed requests and preserved problematic source records in audit and quarantine outputs. | Future API failures or unavailable records may change the final candidate pool. |
| How can another analyst configure the project? | Centralized paths and settings in `config.py` and provided `.env.example` for the TMDb access token. | Adjoa must provide her own valid TMDb token. |
| How can another analyst reproduce the analysis? | Provided `requirements.txt`, setup instructions and a single entry point through `python main.py`. | A clean-clone test on another computer remains necessary. |
| Will results remain identical when rerun later? | Preserved the pipeline logic and generated analysis outputs from the retrieved data. | TMDb is a live source; ratings, popularity and other API data may change over time. |
| How are analytical decisions documented? | Created four Architecture Decision Records covering data quality, franchise classification, financial metrics and ranking methodology. | Future changes to assumptions should be recorded in updated decision notes. |

## 4. Key Decisions Made Without Client Feedback

Because no follow-up clarification was received from Kwame, the following working assumptions were applied:

1. TMDb was used as the primary source for movie details and credits.
2. TMDb collection IDs were used to identify franchise groups.
3. Movies without collection information were treated as standalone candidates for operational analysis.
4. Both all-years and 2000-onward comparisons were required.
5. Median film-level financial ratios were used to compare franchise and standalone performance.
6. Candidate ranking used 50% return ratio, 25% rating and 25% popularity.
7. Cast and director scores received zero ranking weight because their independent predictive value could not be established from the available data.
8. At least two films were required for an individual actor or director to appear as an eligible preliminary talent signal.
9. Historical revenue-to-budget ratios were treated as screening indicators, not licensing ROI.
10. No specific dollar allocation of the $14 million budget was recommended because licensing costs and rights information were unavailable.

These decisions are documented in the corresponding ADR files and should be revisited if the client supplies additional information.

## 5. Outstanding Actions Before Final Licensing Approval

- Obtain the missing 127th identifier.
- Obtain updated title data, particularly for films released after 2019.
- Confirm the actual licensing budget and transaction costs.
- Obtain territory, exclusivity, duration and rights availability information.
- Obtain licensing quotes for shortlisted titles and collections.
- Obtain StreamVault audience-demand and engagement data.
- Validate the recommendations against actual commercial terms.
- Complete a clean-clone rerun and a larger-scale test using approximately 500 IDs.

## 6. Final Position

The analysis provides a repeatable historical screening process for comparing franchise bundles and standalone films. It identifies promising candidates and documents the assumptions and limitations behind the recommendations.

The current results are sufficient to guide further investigation and licensing negotiations, but they are not sufficient to authorize a final $14 million acquisition decision without commercial rights, pricing and audience-demand evidence.