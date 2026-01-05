import pika
import ssl
import json

class RabbitClient:
    def __init__(self, url):
        self.url = url
        self.connection = None
        self.channel = None
        self.connect()

    def connect(self):
        try:
            context = ssl.create_default_context()
            params = pika.URLParameters(self.url)
            params.ssl_options = pika.SSLOptions(context)
            params.socket_timeout = 5
            params.connection_attempts = 3
            params.retry_delay = 2

            self.connection = pika.BlockingConnection(params)
            self.channel = self.connection.channel()
            return True
        except Exception as e:
            print("Erro ao conectar:", e)
            self.connection = None
            self.channel = None
            return False

    def is_connected(self):
        return (
            self.connection is not None and self.connection.is_open
            and self.channel is not None and self.channel.is_open
        )

    def close(self):
        try:
            if self.channel and self.channel.is_open:
                self.channel.close()
        except Exception:
            pass
        try:
            if self.connection and self.connection.is_open:
                self.connection.close()
        except Exception:
            pass
        self.channel = None
        self.connection = None

    def publish(self, queue, message):
        if not self.is_connected():
            if not self.connect():
                return False
        try:
            self.channel.queue_declare(queue=queue, durable=True)
            self.channel.basic_publish(
                exchange="",
                routing_key=queue,
                body=message
            )
            return True
        except Exception as e:
            print("Erro ao publicar:", e)
            return False

    # -------------------------
    # CONSUMIDOR
    # -------------------------
    def consume_added(self, queue, handler):
        if not self.is_connected():
            if not self.connect():
                print("Não foi possível conectar para consumir.")
                return

        self.channel.queue_declare(queue=queue, durable=True)
        self.channel.basic_qos(prefetch_count=1)

        def callback(ch, method, properties, body):
            try:
                events = json.loads(body)
                print(type(events))
            except Exception:
                ch.basic_ack(method.delivery_tag)
                return

            if not isinstance(events, list):
                events = [events]

            for event in events:
                if event.get("type") == "added":
                    handler(event)

            ch.basic_ack(method.delivery_tag)

        self.channel.basic_consume(
            queue=queue,
            on_message_callback=callback
        )

        print("Consumindo eventos ADDED...")
        self.channel.start_consuming()
