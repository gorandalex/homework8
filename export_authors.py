import json
from models import Author

import connect

with open("authors.json", "r", encoding='utf-8') as file:
    file_data = json.load(file)
    for record in file_data:
        author = Author(fullname=record['fullname'], born_date=record['born_date'],
                        born_location=record['born_location'], description=record['description'])
        author.save()

