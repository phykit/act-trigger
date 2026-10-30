# Probe 4 (diagnostic only)

- Rate-limit headers: limit 36000, remaining 35188

- query `collection:USCOURTS courtcode:ca13`: HTTP 200, count 11057; sample ['USCOURTS-ca13-08-03216', 'USCOURTS-ca13-09-01417', 'USCOURTS-ca13-09-01416']
- query `collection:(USCOURTS) AND courtcode:(ca13)`: HTTP 200, count 11057; sample ['USCOURTS-ca13-08-03216', 'USCOURTS-ca13-09-01417', 'USCOURTS-ca13-09-01416']
- query `collection:USCOURTS courtname:"Court of Appeals for the Federal Circuit"`: HTTP 200, count 11057; sample ['USCOURTS-ca13-08-03216', 'USCOURTS-ca13-09-01417', 'USCOURTS-ca13-09-01416']
- query `packageid:USCOURTS-ca13*`: HTTP 200, count 0; sample []

- Query used below: `collection:USCOURTS courtcode:ca13`

## ca13 packages by year of dateIssued (search service)

| Year | packages |
|---|---|
| 2010 | None |
| 2011 | None |
| 2012 | None |
| 2013 | None |
| 2014 | None |
| 2015 | None |
| 2016 | None |
| 2017 | None |
| 2018 | None |
| 2019 | None |
| 2020 | None |
| 2021 | None |
| 2022 | None |
| 2023 | None |
| 2024 | None |
| 2025 | None |
| 2026 | None |

## Docket-text markers, packages issued Mar to Apr 2013: {}

## Docket-text markers, packages issued Mar to Apr 2023: {}

- Rate limit remaining at end: 35165 of 36000
