from datetime import datetime
from bson import json_util
import random

import pika
import faker

import connect

from models import Contact
from main import TYPE_MESSAGE

fake_data = faker.Faker()


def start_channel():
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host='localhost',
        port=5672,
        credentials=credentials
        )
    )
    channel = connection.channel()

    for contact_type_message in TYPE_MESSAGE.values():
        name_exchage = contact_type_message + '_exchange'
        name_queue = contact_type_message + '_queue'
        channel.exchange_declare(exchange=name_exchage, exchange_type='direct')
        channel.queue_declare(queue=name_queue, durable=True)
        channel.queue_bind(exchange=name_exchage, queue=name_queue)
        
    return connection, channel


def create_contact():
    count_contact = 10
    
    while count_contact > 0:
        contact = Contact(fullname=fake_data.name(), email=fake_data.email(),
                        phone=fake_data.phone_number(), message_type=random.choice(("SMS", "EMAIL")))
        contact.save()
        count_contact -= 1
        


if __name__ == '__main__':
#    create_contact()
    connection, channel = start_channel()
    contacts = Contact.objects(is_send=False)
    for contact in contacts:
                
        message = {
            'id': contact.id,
            'message_text': fake_data.text(),
            'created_at': datetime.now().isoformat()
        }
        
        contact_type_message = TYPE_MESSAGE.get(contact.message_type, 'sms')
        name_exchage = contact_type_message + '_exchange'
        name_queue = contact_type_message + '_queue'
        
        channel.basic_publish(
            exchange=name_exchage,
            routing_key=name_queue,
            body=json_util.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            )
        )
        print(f'Sent message {message}')
        
    connection.close()