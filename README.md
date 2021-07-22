# Status Page Checker


## Usage
```
python3 status_page_check.py
docker run status-page-check
```

## Only failed services
```
python3 status_page_check.py --failed
docker run status-page-check --failed
```

## Summary
```
python3 status_page_check.py --summary
python3 status_page_check.py --summary --failed
python3 status_page_check.py --summary --page gcp
```
## Filters
```
python3 status_page_check.py --filter "API Gateway"
python3 status_page_check.py --page GCP
python3 status_page_check.py --page GCP --filter sql
```

## Build

```
docker build . -t status-page-check
```
