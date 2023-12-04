import requests
from bs4 import BeautifulSoup
import csv
import json

def web_scrape_data(url):
    try:
        # Send a GET request to the URL using the chosen proxy
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.59 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=1.5)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content
            soup = BeautifulSoup(response.content, 'html.parser')

            # Find the script tag containing the JSON data
            script_tag = soup.find('script', {'type': 'application/ld+json'})

            # Check if the script tag is found
            if script_tag:
                # Extract the JSON data from the script tag
                json_data = json.loads(script_tag.string)

                # Extract the required information
                description = json_data.get('description', '')
                image_url = json_data.get('image', '')

                # Check if either image or description is not found
                if not image_url or not description:
                    return 1, 1
                else:
                    # Return the results
                    return image_url, description
            else:
                print("Script tag not found.")
                return None, None
        else:
            #print(f"Request failed for URL {url} with status code: {response.status_code}")
            return None, None
    except requests.exceptions.Timeout:
        #print(f"Request timed out for URL: {url}")
        return None, None
    except Exception as e:
        #print(f"An unexpected error occurred for URL: {url}")
        return None, None


def update_tsv():
    # Set a larger field size limit
    csv.field_size_limit(500000)

    with open("missing_info1.tsv", 'r', encoding='utf-8', newline='') as infile, \
         open("1st_redo.tsv", 'w', encoding='utf-8', newline='') as outfile:
        reader = csv.reader(infile, delimiter='\t')
        writer = csv.writer(outfile, delimiter='\t')

        all_rows = list(reader)
        all_rows.reverse()

        # Write header to the output file
        header = next(reader)
        writer.writerow(header + ['Image URL', 'Description'])

        # Process each row
        for row in reader:
            url = "https://www.imdb.com/title/" + str(row[0])

            # Scrape data from the URL
            img_url, description = web_scrape_data(url)


            # Update the row with scraped data
            if img_url != 1 and description != 1:
                writer.writerow(row + [img_url, description])


update_tsv()