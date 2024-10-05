#!/usr/bin/env python
import pika
import sys

# Соединение с RabbitMQ
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# Объявление точки доступа (exchange) типа direct
channel.exchange_declare(exchange='direct_logs', exchange_type='direct')

# Создание временной очереди
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

# Получение уровней логов, которые нужно отслеживать, из командной строки
severities = sys.argv[1:]
if not severities:
    sys.stderr.write(f"Usage: {sys.argv[0]} [info] [warning] [error]\n")
    sys.exit(1)

# Привязка очереди к exchange с binding key, равным уровням логов
for severity in severities:
    channel.queue_bind(exchange='direct_logs', queue=queue_name, routing_key=severity)

print(' [*] Waiting for logs. To exit press CTRL+C')

# Функция callback для обработки сообщений
def callback(ch, method, properties, body):
    print(f" [x] {method.routing_key}:{body.decode()}")

# Ожидание сообщений из очереди
channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()
