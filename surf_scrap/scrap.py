import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from datetime import datetime


def get_forecast(url, output_file):
    """
    Scrapes surf forecast from surf-report.com and saves it to a CSV file.

    Parameters:
    url (str): The URL of the surf spot (e.g., "https://www.surf-report.com/meteo-surf/...")
    output_file (str): The full path including filename where the CSV should be saved (e.g., "data/my_surf_data.csv")
    """

    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Edg/140.0.0."
    headers = {'User-Agent': user_agent}

    month_map = {
        'Janvier': '01', 'Février': '02', 'Mars': '03', 'Avril': '04',
        'Mai': '05', 'Juin': '06', 'Juillet': '07', 'Août': '08',
        'Septembre': '09', 'Octobre': '10', 'Novembre': '11', 'Décembre': '12'
    }

    # Get current year (because the website doesn't provide it)
    current_year = datetime.now().year

    try:
        page = requests.get(url, headers=headers)
        page.raise_for_status()  # Check for HTTP errors
        soup = BeautifulSoup(page.content, 'html.parser')

        data_list = []

        forecast_tabs = soup.find_all('div', class_='forecast-tab')

        if not forecast_tabs:
            print("Warning: No forecast data found. Check the URL.")
            return

        for tab in forecast_tabs:
            title_div = tab.find('div', class_='title')

            if title_div:
                date_text = title_div.find('b').get_text(strip=True)
                content_div = tab.find('div', class_='content')
                lines = content_div.find_all('div', class_='line')

                for line in lines:
                    time_cell = line.find('div', class_='cell date with-border')
                    time_text = None

                    if time_cell and 'entetes' not in time_cell.get('class', []):
                        time_text = time_cell.get_text(strip=True)

                    if not time_text:
                        continue

                    # Wave Height
                    wave_cell = line.find('div', class_='cell large waves with-border')
                    wave_text = wave_cell.get_text(strip=True) if wave_cell else "N/A"

                    # Wind Speed
                    wind_speed_div = line.find('div', class_=lambda x: x and 'wind-color' in x)
                    wind_speed = wind_speed_div.get_text(strip=True) if wind_speed_div else "N/A"

                    # Wind Direction
                    wind_dir_div = line.find('div', class_='wind img')
                    wind_direction = "N/A"
                    if wind_dir_div:
                        img = wind_dir_div.find('img')
                        if img and 'alt' in img.attrs:
                            wind_direction = img['alt']

                    data_list.append({
                        'date_raw': date_text,
                        'hour': time_text,
                        'wave_height': wave_text,
                        'wind_speed': wind_speed,
                        'wind_direction': wind_direction
                    })

            df = pd.DataFrame(data_list)

            def parse_french_date(row):
                # Example row['date_raw']: "Vendredi 9 Janvier"
                parts = row['date_raw'].split()
                # parts is now ['Vendredi', '9', 'Janvier']

                if len(parts) >= 3:
                    day = parts[1]
                    month_str = parts[2]
                    month_num = month_map.get(month_str, '01')  # Default to 01 if not found

                    # Construct string: "2025-01-09 06:00"
                    # Note: We zfill(2) the day to turn "9" into "09"
                    return f"{current_year}-{month_num}-{day.zfill(2)} {row['hour']}"
                return None

            df['temp_timestamp'] = df.apply(parse_french_date, axis=1)

            df['datetime'] = pd.to_datetime(df['temp_timestamp'], format='%Y-%m-%d %H:%M', errors='coerce')

            df = df.drop(columns=['temp_timestamp'])

            df['min_waves_height']= df['wave_height'].str.extract(r'^(\d+(?:\.\d+)?)')
            df['max_waves_height']=df['wave_height'].str.extract(r'-(\d+(?:\.\d+)?)')

            df['min_waves_height'] = pd.to_numeric(df['min_waves_height'], errors='coerce')
            df['max_waves_height'] = pd.to_numeric(df['max_waves_height'], errors='coerce')

            df['moy_waves_height']=(df['min_waves_height']+df['max_waves_height'])/2

            folder_path = os.path.dirname(output_file)

            # Create folder if it doesn't exist (only if a folder path is provided)
            if folder_path and not os.path.exists(folder_path):
                os.makedirs(folder_path)

            df.to_csv(output_file, index=False, encoding='utf-8-sig')

    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")