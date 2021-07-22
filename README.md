# Status Page Checker


## Usage
```
python3 status-page-check.py
docker run status-page-check
```

## Only failed services
```
python3 status-page-check.py --failed
docker run status-page-check --failed
```

## Summary
```
python3 status-page-check.py --summary
python3 status-page-check.py --summary --failed
python3 status-page-check.py --summary --page gcp
```
## Filters
```
python3 status-page-check.py --filter "API Gateway"
python3 status-page-check.py --page GCP
python3 status-page-check.py --page GCP --filter sql
```

## Build

```
docker build . -t status-page-check
```
