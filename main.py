import sys
import csv
from categorize import openai, categorize


if __name__ == "__main__":
    with open('data/test.csv', 'r') as f:
        reader = csv.reader(f)
        headers = next(reader)
        name_idx = headers.index('product_name')
        description_idx = headers.index('product_description')
        for row in reader:
            name = row[name_idx]
            description = row[description_idx]
            text = name + ' '  + description
            crumb_data = categorize.get_matching_categories(text)
