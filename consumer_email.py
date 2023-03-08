from bson import json_util
import pika

import connect
from models import Contact


def main():
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host='localhost',
            port=5672,
            credentials=credentials
            )
        )

    def send_email(ch, method, properties, body):
        contact_data = json_util.loads(body)
        contact = Contact.objects(id=contact_data['id'])[0]
        print(f'Email send for {contact.fullname}')

    channel = connection.channel()

    name_queue = 'email_queue'
    channel.queue_declare(queue=name_queue, durable=True)
    
    
    channel.basic_consume(
        queue=name_queue,
        on_message_callback=send_email,
        auto_ack=True
        )
    channel.start_consuming()
    

    
    
if __name__ == '__main__':
    main()