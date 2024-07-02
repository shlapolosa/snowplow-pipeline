from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from confluent_kafka import Consumer, KafkaError, KafkaException
import json
import asyncio
import logging
import os

# Configure logging to output to the console
logging.basicConfig(level=logging.INFO)

app = FastAPI()

# Kafka Consumer configuration
kafka_config = {
    'bootstrap.servers': "kafka:29092",
    'group.id': 'python-consumer',
    'auto.offset.reset': 'earliest'
}

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>WebSocket Test</title>
    </head>
    <body>
        <h1>WebSocket Test</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages');
                var message = document.createElement('li');
                var content = document.createTextNode(event.data);
                message.appendChild(content);
                messages.appendChild(message);
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText");
                ws.send(input.value);
                input.value = '';
                event.preventDefault();
            }
        </script>
    </body>
</html>
"""

# WebSocket manager to handle multiple clients
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logging.info(f"Client connected: {websocket.client}")

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        logging.info(f"Client disconnected: {websocket.client}")

    async def send_message(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception as e:
                logging.error(f"Error sending message to {connection.client}: {e}")

manager = ConnectionManager()

@app.get("/")
async def get():
    return HTMLResponse(html)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_message(f"Echo: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        logging.error(f"WebSocket error: {e}")
        manager.disconnect(websocket)

async def kafka_consumer_loop():
    logging.info("Starting Kafka consumer loop...")
    retries = 0
    max_retries = 5
    while True:
        try:
            logging.info("Attempting to connect to Kafka...")
            kafka_consumer = Consumer(kafka_config)
            kafka_consumer.subscribe(['snowplow_json_event'])
            logging.info("Successfully connected to Kafka and subscribed to topic 'snowplow_json_event'.")
            break
        except KafkaException as e:
            retries += 1
            logging.error(f"Kafka connection error: {e}")
            if retries >= max_retries:
                logging.critical("Max retries reached. Exiting Kafka consumer loop.")
                return
            logging.info(f"Retrying Kafka connection in 5 seconds... (Attempt {retries}/{max_retries})")
            await asyncio.sleep(5)  # Wait before retrying

    while True:
        try:
            logging.info("Polling for messages...")
            msg = kafka_consumer.poll(1.0)
            if msg is None:
                await asyncio.sleep(1)
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    logging.error(f"Kafka message error: {msg.error()}")
                    break

            event = msg.value().decode('utf-8')
            logging.info(f"Received message from Kafka: {event}")
            await manager.send_message(event)
        except KafkaException as e:
            logging.error(f"Kafka polling error: {e}")
            await asyncio.sleep(5)  # Wait before retrying
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            await asyncio.sleep(5)  # Wait before retrying

if __name__ == "__main__":
    import uvicorn
    import signal
    from multiprocessing import Process

    def start_kafka_loop():
        logging.info("Starting Kafka process...")
        asyncio.run(kafka_consumer_loop())

    kafka_process = Process(target=start_kafka_loop)
    kafka_process.start()

    def shutdown(sig, frame):
        logging.info("Shutting down...")
        kafka_process.terminate()
        kafka_process.join()
        logging.info("Shutdown complete")
        os._exit(0)

    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    try:
        uvicorn.run(app, host="0.0.0.0", port=8000)
    finally:
        shutdown(None, None)
