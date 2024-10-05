#!/usr/bin/env python
import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# Объявляем точку доступа типа fanout
channel.exchange_declare(exchange='logs', exchange_type='fanout')

# Создаем временную очередь с автоматическим удалением
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

# Связываем очередь с точкой доступа 'logs'
channel.queue_bind(exchange='logs', queue=queue_name)

print(' [*] Waiting for logs. To exit press CTRL+C')

# Функция callback для обработки сообщений
def callback(ch, method, properties, body):
    print(" [x] %r" % body)

channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()