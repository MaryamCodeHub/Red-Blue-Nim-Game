import requests
from bs4 import BeautifulSoup
import csv

# URL of the Amazon page to scrape
url = 'https://www.amazon.com/'

# User-Agent header to mimic a browser request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Send a GET request to the URL
response = requests.get(url, headers=headers)

# Parse the HTML content
soup = BeautifulSoup(response.content, 'html.parser')

# Extract product names
product_names = []
for product in soup.find_all('span', {'class': 'a-size-medium'}):
    product_names.append(product.text.strip())

# Print number of products found
print(f'Found {len(product_names)} products.')

# Define CSV filename
csv_filename = 'amazon_products.csv'

# Write data to CSV file
with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Product Name'])  # Write header row
    for name in product_names:
        writer.writerow([name])

print(f'Data has been scraped and saved to {csv_filename}.')
                 