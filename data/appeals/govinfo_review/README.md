# Review of GovInfo as the Federal Circuit source (31 October 2026)

Inputs: `data/appeals/govinfo_cafc_index.csv` (GovInfo index job of 31 October 2026: 10,519 dockets, 11,057 entries), and the two retired CourtListener lists `cafc_precedential_run6_cafc_truncated.csv` (980 items, 3 January 2012 to 1 October 2013) and `cafc_precedential_run8_cafc_429.csv` (453 items, 3 October 2014 to 12 November 2015). The comparison uses dockets, dates and labels only; no prices or results were read.

## Findings

1. **Coverage begins in early 2013.** GovInfo holds nine clean precedential opinions for 2012. Of the CourtListener items it holds on the same docket and date, the share is under 25% to January 2013, 62 to 64% in February and March 2013, and 79 to 90% from April 2013. That is the same level as in 2015, when the remainder is explained in item 4. The registered start of 1 January 2012 cannot be met from GovInfo.
2. **The precedential marker can be read throughout.** To 2018 it appears as "(Precedential Opinion)" or "(Precedential Per Curiam Opinion)"; from 2019 it appears as "Precedential Opinion." in the "OPINION filed for the court by ..." entry. Both forms are parsed. Entries with no marker are almost all summary affirmances under Federal Circuit Rule 36 ("FCR 36"), which are not opinions.
3. **CourtListener's "Published" status includes Rule 36 judgments.** Between January and October 2015, 182 of the 416 CourtListener items are Rule 36 affirmances on GovInfo. Earth v1's universe, as implemented, therefore mixed summary affirmances with precedential opinions, contrary to the words of Earth v1 item 2. This bears on run 8, whose totals the analyst has seen.
4. **GovInfo's precedential opinions appear in full in CourtListener's list for January to October 2015** (161 of 161 after de-duplication), and 210 of CourtListener's items match a GovInfo precedential entry on the same day. The CourtListener items GovInfo lacks are:
   - mandamus petitions, which GovInfo holds only 11 times in total (for example, In re Apple, 2015; In re TC Heartland, 2016);
   - en banc and other precedential orders (Halo, Lexmark, In re Tam, GEA, Ultratec);
   - one District of Columbia Circuit case that CourtListener files under the Federal Circuit;
   - five that GovInfo marks non-precedential.
5. **Day 0.** Where both sources hold an opinion, the GovInfo issue date equals CourtListener's filing date on 210 of 215 matches.
6. **Duplicates.** A consolidated appeal appears once in each of its dockets (Akamai v. Limelight appears four times on 13 May 2015). About 200 errata and corrected entries carry the word "Precedential". Both need a counting rule.
7. **Captions.** GovInfo's title is the abbreviated caption of the lead docket. For example, the 14 November 2014 Ultramercial opinion is titled "Ultramercial, Inc. v. WildTangent, Inc.", whereas CourtListener calls it "Ultramercial, Inc. v. Hulu, LLC". Party matching should therefore use the package's list of parties, not the title.
8. **Spot check.** Twenty well-known precedential opinions from 2014 to 2021 were checked: 19 are present, on the expected day and marked precedential. The one missing is In re TC Heartland (2016), a mandamus petition (item 4).
9. **Counts.** De-duplicated precedential opinions number between 144 (2013) and 247 (2019) a year. The Federal Circuit's own annual totals were not found for comparison; Gibson Dunn's count covers patent cases only (76 between August 2020 and July 2021).

Files: `overlap_run6.csv` and `overlap_run8.csv` (how each CourtListener item was matched), `govinfo_prec_clean.csv` (de-duplicated GovInfo precedential opinions, a draft rule only).
