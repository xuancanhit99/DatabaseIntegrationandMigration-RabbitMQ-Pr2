#!/usr/bin/env python
import pika
import sys

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# Объявление точки доступа (exchange) типа direct
channel.exchange_declare(exchange='direct_logs', exchange_type='direct')

# Получение уровня логов из командной строки
severity = sys.argv[1] if len(sys.argv) > 1 else 'info'
message = ' '.join(sys.argv[2:]) or 'Hello World!'

# Отправка сообщения в exchange с routing key, равным уровню логов
channel.basic_publish(
    exchange='direct_logs', routing_key=severity, body=message)
print(" [x] Sent %r:%r" % (severity, message))
connection.close()