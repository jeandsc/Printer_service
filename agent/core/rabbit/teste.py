from core.rabbit.rabbit_client import RabbitClient  # seu arquivo com a classe
import time

# Substitua com a URL do seu CloudAMQP
URL = "amqps://ykcdgrfj:OCn_ZAIrZxkwvRpWUY2ZUGKLUiQPDBAm@kangaroo.rmq.cloudamqp.com/ykcdgrfj"
QUEUE = "fila_teste"

def main():
    client = RabbitClient(URL)

    # Tenta conectar
    if not client.connect():
        print("Falha na conexão. Verifique URL, vhost e rede.")
        return

    print("Conectado com sucesso!")

    # Envia mensagens de teste
    for i in range(5):
        msg = f"mensagem {i}"
        if client.publish(QUEUE, msg):
            print(f"Mensagem enviada: {msg}")
        else:
            print(f"Falha ao enviar: {msg}")
        time.sleep(1)  # só pra não bombardear o servidor

    # Fecha conexão
    client.close()
    print("Conexão fechada.")

if __name__ == "__main__":
    main()
