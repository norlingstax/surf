import requests
from bs4 import BeautifulSoup
import pandas as pd
import os


def get_forecast(url, output_file):
    """
    Scrapes surf forecast from surf-report.com and saves it to a CSV file.

    Parameters:
    url (str): The URL of the surf spot (e.g., "https://www.surf-report.com/meteo-surf/...")
    output_file (str): The full path including filename where the CSV should be saved (e.g., "data/my_surf_data.csv")
    """

    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Edg/140.0.0."
    headers = {'User-Agent': user_agent}

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
                        'date': date_text,
                        'hour': time_text,
                        'wave_height': wave_text,
                        'wind_speed': wind_speed,
                        'wind_direction': wind_direction
                    })

            df = pd.DataFrame(data_list)

            folder_path = os.path.dirname(output_file)

            # Create folder if it doesn't exist (only if a folder path is provided)
            if folder_path and not os.path.exists(folder_path):
                os.makedirs(folder_path)

            df.to_csv(output_file, index=False, encoding='utf-8-sig')

    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")