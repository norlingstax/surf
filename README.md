# 🏄‍♂️ Surf Condition Dashboard & Scraper

**Domain:** Data Analytics / Web Scraping / Visualization

##  Overview

As a data analyst for a Surf School located near Bordeaux, this project aims to automate the collection and visualization of sea conditions. The goal is to identify the **best moment to practice surfing** during the upcoming week based on specific meteorological criteria.

The project is divided into two main components:
1.  **Python ETL Pipeline:** A custom library (`surf_scrap`) to scrape weather forecasts (waves, wind, direction) from *surf-report.com* and export them to a CSV dataset.
2.  **R Dashboard:** A dynamic `flexdashboard` that reads the generated data, visualizes trends, and computes KPIs to recommend the optimal surf session.

## Architecture

The workflow consists of the following steps:
1.  **Scraping (Python):** The `surf_scrap` library extracts 7-day forecast data.
2.  **Storage:** Data is cleaned (date parsing, numeric conversion) and saved as a CSV file.
3.  **Visualization (R):** An R Markdown script processes the CSV to generate a dashboard with KPIs.

## Prerequisites

### Python Environment
* Python 3.8+


### R Environment
* R & RStudio
* Packages: `flexdashboard`, `tidyverse` (dplyr, ggplot2), `readr`, `gauge`

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
Open RStudio and install the required packages:
```
install.packages(c("flexdashboard", "tidyverse", "readr"))
```
## Usage

### Step 1: Extract Data (Python)
Use the main.py script to scrape the latest data for your specific surf spot.

Example usage in main.py:

```bash
import surf_scrap

# URL for Moliets (or Carcans, Lacanau, etc.)
target_url = "[https://www.surf-report.com/meteo-surf/moliets-plage-centrale-s102799.html](https://www.surf-report.com/meteo-surf/moliets-plage-centrale-s102799.html)"
output_path = "data/surf_forecast.csv"

# Run the scraper
surf_scrap.get_forecast(target_url, output_path)
```

Run the script from your terminal:

```Bash
python main.py
```
Output: A file named surf_forecast.csv will be created in the data/ folder.

### Step 2: Generate Dashboard (R)
1. Open dashboard.Rmd in RStudio.
2. Ensure the path to data/surf_forecast.csv is correct in the R chunk.
3. Click the "Knit" button to generate the HTML dashboard.

####  Dashboard Features
The R dashboard provides the following insights:

- Wave Trend: A line graph showing mean wave height over the next 7 days.
- Wind Analysis: A visualization of wind speed fluctuations.
- Detailed Forecast: A table listing Day, Hour, Wave Size, and Wind Direction.
- The "Best Moment": An algorithmic recommendation box highlighting the best day/hour to surf.
- Quality Gauge: A visual grade (0-100) of the sea quality for that best moment.

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
│
├── main.py                    # Script to execute the scraping
├── dashboard.Rmd              # R Flexdashboard source code
├── README.md                  # Project documentation
└── requirements.txt           # Python dependencies
