# 🏄‍♂️ Surf Condition Dashboard & Scraper

**Domain:** Data Analytics / Web Scraping / Visualization

##  Overview

This project aims to automate the collection and visualization of sea conditions. The goal is to identify the **best moment to practice surfing** during the upcoming week based on specific meteorological criteria.

The project is divided into two main components:
1.  **Python ETL Pipeline:** A custom library (`surf_scrap`) to scrape weather forecasts (waves, wind, direction) from *surf-report.com* and export them to a CSV dataset.
2.  **R Dashboard:** A dynamic `flexdashboard` that reads the generated data, visualizes trends, and computes KPIs to recommend the optimal surf session.

## Architecture

The workflow consists of the following steps:
1.  **Scraping (Python):** The `surf_scrap` library extracts 7-day forecast data.
2.  **Storage:** Data is cleaned (date parsing, numeric conversion) and saved as a CSV file.
3.  **Visualization (R):** An R  script run the main Python script and generate a dashboard.

## Prerequisites

### Python Environment
* Python 3.8+


### R Environment
* R & RStudio 

## Installation & Setup

### 1. Clone the Repository
```bash
git clone 
cd surf-dashboard
```

### 2. Python Setup
* Install the dependencies and the custom scraping library.

```bash
# Install required packages
pip install requirements.txt
```

### 3. R Setup
You'll need the following packages:
- shiny
- flexdashboard
- tidyverse
- lubridate
- here
- plotly

## Usage

Run `run_surf_dashboard.R`, it will launch the scrapping pipeline and open a nice user interface built with flexdashboard

## Dashboard Features
The R dashboard provides the following insights:

- Wave Trend: A line graph showing mean wave height over the next 7 days.
- Wind Analysis: A visualization of wind speed fluctuations.
- Detailed Forecast: A table listing Day, Hour, Wave Size, and Wind Direction.
- The "Best Moment": An algorithmic recommendation box highlighting the best day/hour to surf.
- Quality Gauge: A visual grade (0-100) of the sea quality for that best moment.V

#### "Best Moment" Logic
The recommendation engine prioritizes:
- Wave Height: > 1.0m
- Wind Direction: Coming from the North (Offshore/Cross-shore for this region).
- Wind Speed: Up to 50 km/h.

## Project Structure

```text
surf-dashboard/
│
├── data/
│   └── surf_forecast.csv      # Generated output file
│
├── surf_scrap/                # Python Library
│   ├── __init__.py            # Main scraping logic
│   └── scrap.py
│
├── main.py
│                  
├── r_script/
│    ├── run_surf_dashboard.R  # script to run
│    ├── surf_dashboard.Rmd    # flexdashboard code
│    └── style.css             # customized colors & shape
│            
├── README.md                  # Project documentation
└── requirements.txt           # Python dependencies
