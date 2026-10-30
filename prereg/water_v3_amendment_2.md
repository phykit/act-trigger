# Water v3, amendment 2: how the official opinion is located

Registered 30 October 2026, before coder 3 has produced any valid coding. It refines item 1 of `water_v3_amendment_1.md` (SHA-256 7f838f8f7cc431f311555b655fc1200c18794ae38e5ef8923cb3bd71df769039) after the source check committed at `data/water/opinion_sources/`. That amendment and `water_v3_prereg.md` are otherwise unchanged.

## Reason

The source check showed two things that amendment 1 did not anticipate:
- Once the bound version of an opinion is ready, the Court replaces the slip opinion on its opinions page with a link to a preliminary print or a bound volume of the United States Reports. That link anchors to the case's first page.
- For volumes 585 and 586, GovInfo records each case's decision date only as a year, so a test for an exact date match cannot succeed.

## Change

Item 1 of amendment 1 becomes:

1. The Court's own opinions page for the October Term containing the decision date (supremecourt.gov, terms 2017 onwards). The row is identified by its docket number (in the file name or in the row's docket cell) and, where shown, its date.
   - If the row links the slip opinion, that PDF is used.
   - If the row links a preliminary print or bound volume, the pages are used from the case's anchor to the page before the next case's anchor in the same file, up to 120 pages.
   - If that file cannot be retrieved, the GovInfo United States Reports granule for the citation the row gives (for example 587 U.S. 299 is granule USREPORTS-587-299) is used.

Items 2 (GovInfo by caption and exact decision date) and 3 (CourtListener) of amendment 1 are unchanged. The source recorded for each event names the file and the page range, or the granule.

## What this does not change

Everything listed under the same heading in amendment 1 is unaffected. The document is still the Court's own text of the same judgment.
