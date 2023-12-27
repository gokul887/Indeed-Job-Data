# indeed_job_scraping.py

## Included File

`indeed_job_scraping.py`

## Motivation

Simplifies the process of searching for software internships.

## Current Working

- Takes 20 pages of relevant data from Indeed for software intern jobs.
- Extracts HTML from the page and uses Beautiful Soup to find relevant data.
- Builds a MySQL database with the job data:
    - Job title
    - Company
    - Location
    - Company rating
    - Salary
    - Indeed URL (as scraping the job description is not permitted)
