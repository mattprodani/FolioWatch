# FolioWatch
</hr >

## Description
A python-based personal investment manager designed to pull information from various sources and provide an update on the portfolio before opening.
The full model uses more sources than the basic model in this repo.
Example PDF report: [REPORT](reports/example_report.pdf)
</hr >

## Features
* Custom data-scraping API
* Custom Schwab API with trading functionality
* Report Generation Based on Parsed Data
* Sending email with HTML and PDF attachment from one script.

</hr>

## To-Do:
- [x] Export research to HTML
- [x] Portfolio data export
- [x] PDF and html report creation
- [x] Pipeline to connect sourcing data and report
- [x] E-mail for report
- [ ] Docker container
- [ ] Automatic trading and rebalancing

</hr >

## Requirements
```
pandas
bs4
requests
playwright
playwright_stealth
pyotp
vipaccess
plotly
kaleido
weasyprint
jinja2
```


