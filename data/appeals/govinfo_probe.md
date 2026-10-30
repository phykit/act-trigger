# GovInfo and supremecourt.gov probe (diagnostic only)

- GOVINFO_API_KEY present: yes (length 40).

## 1. /published USCOURTS cafc 2024 Q1: HTTP 400

- count None; first page 0 packages.

### first two packages

```
[]
```

## 1b. /collections fallback: HTTP 400

### response

```
{
 "validationMessages": [
  "Supply a valid court code. These typically follow a pattern of two-digit state code, optional cardinal direction (n|e|s|w), and court type abbreviation (d/b/a)."
 ]
}
```

## 3. USCOURTS cafc package counts by calendar year (dateIssued)

| Year | HTTP | count |
|---|---|---|
| 2012 | 400 | None |
| 2013 | 400 | None |
| 2014 | 400 | None |
| 2015 | 400 | None |
| 2016 | 400 | None |
| 2017 | 400 | None |
| 2018 | 400 | None |
| 2019 | 400 | None |
| 2020 | 400 | None |
| 2021 | 400 | None |
| 2022 | 400 | None |
| 2023 | 400 | None |
| 2024 | 400 | None |
| 2025 | 400 | None |

## 4. GovInfo collections (HTTP 200): ANNUALREP, BILLS, BILLSTATUS, BILLSUM, BUDGET, CCAL, CDIR, CDOC, CFR, CHRG, CMR, COMPS, CPD, CPRT, CREC, CRECB, CRI, CRPT, CZIC, ECFR, ECONI, ERIC, ERP, FR, GAOREPORTS, GOVMAN, GOVPUB, GPO, HJOURNAL, HMAN, HOB, LSA, PAI, PLAW, PPP, SERIALSET, SJOURNAL, SMAN, STATUTE, USCODE, USCOURTS, USREPORTS

- USREPORTS published 2005 to 2025: HTTP 200, count 47
### USREPORTS sample

```
[
 {
  "congress": null,
  "dateIssued": "2025-01-01",
  "docClass": "USREPORTS",
  "lastModified": "2026-09-28T17:36:01Z",
  "packageId": "USREPORTS-584",
  "packageLink": "https://api.govinfo.gov/packages/USREPORTS-584/summary",
  "title": "United States Reports, Volume 584"
 },
 {
  "congress": null,
  "dateIssued": "2025-01-01",
  "docClass": "USREPORTS",
  "lastModified": "2026-09-28T17:35:02Z",
  "packageId": "USREPORTS-585",
  "packageLink": "https://api.govinfo.gov/packages/USREPORTS-585/summary",
  "title": "United States Reports, Volume 585"
 },
 {
  "congress": null,
  "dateIssued": "2025-01-01",
  "docClass": "USREPORTS",
  "lastModified": "2026-07-14T11:38:58Z",
  "packageId": "USREPORTS-583",
  "packageLink": "https://api.govinfo.gov/packages/USREPORTS-583/summary",
  "title": "United States Reports, Volume 583"
 }
]
```

## 5. supremecourt.gov from the runner

- slipopinion/05: HTTP 200, 244248 bytes, 0 opinion PDF links; first []
- slipopinion/10: HTTP 200, 244248 bytes, 0 opinion PDF links; first []
- slipopinion/15: HTTP 200, 244248 bytes, 0 opinion PDF links; first []
- slipopinion/20: HTTP 200, 107745 bytes, 0 opinion PDF links; first []
- slipopinion/23: HTTP 200, 100398 bytes, 0 opinion PDF links; first []
- slipopinion/24: HTTP 200, 103491 bytes, 0 opinion PDF links; first []
- /opinions/boundvolumes.aspx: HTTP 200, 43435 bytes, 4 pdf links
- /opinions/USReports.aspx: HTTP 200, 244248 bytes, 625 pdf links

