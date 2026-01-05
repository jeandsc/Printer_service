import pika
import ssl

class RabbitClient:
    def __init__(self, url):
        self.url = url
        self.connection = None
        self.channel = None
        self.connect()
    def connect(self):
        """Estabelece conexão e canal com timeout e SSL."""
        try:
            context = ssl.create_default_context()
            params = pika.URLParameters(self.url)
            params.ssl_options = pika.SSLOptions(context)
            params.socket_timeout = 5        # evita travamentos
            params.connection_attempts = 3   # tenta 3x
            params.retry_delay = 2           # segundos entre tentativas

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

    def create_channel(self):
        """Cria canal se não existir ou estiver fechado."""
        try:
            if not self.connection or self.connection.is_closed:
                if not self.connect():
                    return None
            if not self.channel or self.channel.is_closed:
                self.channel = self.connection.channel()
            return self.channel
        except Exception as e:
            print("Erro ao criar canal:", e)
            return None

    def reconnect(self):
        """Fecha conexão e tenta reconectar."""
        self.close()
        return self.connect()

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
        """Publica mensagem, declara fila se necessário."""
        if not self.is_connected():
            if not self.connect():
                print("Não foi possível conectar para publicar.")
                return False
        try:
            self.channel.queue_declare(queue=queue, durable=True)
            self.channel.basic_publish(exchange="", routing_key=queue, body=message)
            return True
        except Exception as e:
            print("Erro ao publicar:", e)
            return False
