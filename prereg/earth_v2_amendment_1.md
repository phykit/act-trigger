# Earth v2, amendment 1: which side a Federal Circuit party is on

Registered 31 October 2026, before any run under Earth v2. It amends item 3 of `earth_v2_prereg.md` (SHA-256 f31acf8b9450f8bb24251d37e5e99addf30e1ec838030dc8aabfd611f644f510), which is left unchanged; every other provision stands.

## Reason

The completed parties file (`data/appeals/govinfo_cafc_parties.csv`) showed two things that item 3 got wrong.

1. GovInfo lists a party that cross-appeals only as "Cross-Appellant", never also as "Appellee". In every case examined, that party is the appellant's opponent, for example Limelight in Akamai v. Limelight and MobileMedia in Apple v. MobileMedia. Item 3 put cross-appellants on the appellant's side, which would have placed the two litigants on the same side.
2. In appeals from the International Trade Commission, the private company that won below is listed as "Intervenor" and defends the Commission's decision, for example Suprema and Mentalix in Cross Match v. ITC, and Nintendo in Motiva v. ITC. Item 3 excluded intervenors, which would have dropped that company from the ruling.

## Change

Item 3's side rule becomes:

1. One side is the parties listed as appellant, petitioner or applicant.
2. The other side is the parties listed as appellee, cross-appellee, respondent, cross-appellant, cross-applicant, cross-petitioner or intervenor.
3. Parties listed as "Not party", amicus curiae or movant are not matched.
4. In a ruling formed from several consolidated dockets, a name listed on both sides keeps the side it has in the first docket, in docket-number order.

Nothing else changes, and no Earth v2 result has been computed.
