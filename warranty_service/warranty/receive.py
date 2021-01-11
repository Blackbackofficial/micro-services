import pika
import requests


def startRabbit():
    parameters = pika.URLParameters(
        'amqps://waxtnnui:GqR1g_QZtwn9BuHIo0WhrWZ3pcxDpOzi@crow.rmq.cloudamqp.com/waxtnnui')
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue='warranty')

    def callback(ch, method, properties, receive):
        receive = receive.decode()
        requests.post('http://127.0.0.1:8200/api/v1/warranty/{}'.format(receive))

    channel.basic_consume(queue='warranty', on_message_callback=callback, auto_ack=True)
    channel.start_consuming()


if __name__ == '__main__':
    try:
        startRabbit()
    except KeyboardInterrupt:
        print('Interrupted')

