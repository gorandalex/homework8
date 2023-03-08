import connect
from pprint import pprint
from models import Quote, Author
import re
import redis
from redis_lru import RedisLRU


client = redis.StrictRedis(
    host="localhost", 
    port=6379, 
    password=None,
    charset="utf-8"
    )

cache = RedisLRU(client)


def command_error() -> str:
    return f'Невірна команда. Введіть команду "help" для списку команд, та спробуйте ще раз, або введіть команду "exit" для виходу.'


def show_exit():
    return 'Good bye!'


def show_help():
    pprint(
        """
        'help': "Список команд",
        'name': "Пошук за прізвищем та ім'ям автора",
        'tag': "Пошук по тегах"
        'exit': "Вихід"
        """
        )
    
@cache    
def find_by_name(name: str = '') -> str:
    regex = re.compile(f'.*{name}.*')
    authors = Author.objects(fullname=regex)
        
    if not authors:
        return 'Автора не знайдено'
    else:
        authors_filter = []
        for author in authors:
            authors_filter.append(author.id)
    
    quotes = ''
    for quote in Quote.objects(author__in=authors_filter):
        quotes += quote.quote + '\n'
        
    if not quotes:
        return 'Фраз не знайдено'
    
    return quotes
            
    
@cache    
def find_by_tags(tag: str = '') -> str:
    quotes = ''
    for _tag in tag.split(','):
        regex = re.compile(f'.*{_tag}.*')
    
        for quote in Quote.objects(tags=regex):
            quotes += quote.quote + '\n'
        
    if not quotes:
        return 'Фраз не знайдено'
    
    return quotes
    

    