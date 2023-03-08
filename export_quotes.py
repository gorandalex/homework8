import json
from models import Quote, Author

import connect

with open("quotes.json", "r", encoding='utf-8') as file:
    file_data = json.load(file)
    for record in file_data:
        for author in Author.objects(fullname=record['author']):
            author_id = author.id
            break
        quote = Quote(
            tags=record['tags'],
            quote=record['quote'],
            author=author_id
        )
        quote.save()

