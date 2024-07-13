from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from confluent_kafka import Consumer, KafkaError, KafkaException
import json
import asyncio
import logging
import os

logging.basicConfig(level=logging.INFO)

app = FastAPI()

kafka_config = {
    'bootstrap.servers': "kafka:29092,kafka.confluent.svc.cluster.local:9092",
    'group.id': 'websocket',
    'enable.auto.commit': 'false',
    'auto.offset.reset': 'smallest'

}

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>WebSocket Test</title>
        <style>
            #drawingArea {
                width: 500px;
                height: 300px;
                border: 1px solid black;
                position: relative;
            }
            .dot {
                width: 5px;
                height: 5px;
                border-radius: 50%;
                position: absolute;
            }
            .move {
                background-color: black;
            }
            .click {
                background-color: red;
            }
        </style>
    </head>
    <body>
        <h1>WebSocket Test</h1>
        <div id="drawingArea"></div>
        <script>
            // Derive the WebSocket URL from the current location
            var ws_scheme = window.location.protocol === "https:" ? "wss" : "ws";
            var ws_url = ws_scheme + "://" + window.location.host + "/consumer/ws";
            var ws = new WebSocket(ws_url);
            ws.onmessage = function(event) {
                var eventData = JSON.parse(event.data);
                if (eventData.event_name === "mouse_move") {
                    var pos = eventData.unstruct_event_com_example_company_mouse_move_1;
                    drawDot(pos.posx, pos.posy, 'move');
                } else if (eventData.event_name === "mouse_click") {
                    var pos = eventData.unstruct_event_com_example_company_mouse_click_1;
                    drawDot(pos.posx, pos.posy, 'click');
                }
            };

            function drawDot(x, y, type) {
                var drawingArea = document.getElementById('drawingArea');
                var dot = document.createElement('div');
                dot.className = `dot ${type}`;
                dot.style.left = x + 'px';
                dot.style.top = y + 'px';
                drawingArea.appendChild(dot);
            }
        </script>
    </body>
</html>
"""

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

@app.get("/consumer")
async def get():
    return HTMLResponse(html)

@app.websocket("/consumer/ws")
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
            kafka_consumer = Consumer(kafka_config,logger=logging)

            def print_assignment(consumer, partitions):
                print('Assignment:', partitions)

            kafka_consumer.subscribe(['snowplow_json_event'],on_assign=print_assignment)

            logging.info("Successfully connected to Kafka and subscribed to topic 'snowplow_json_event'.")
            break
        except KafkaException as e:
            retries += 1
            logging.error(f"Kafka connection error: {e}")
            if retries >= max_retries:
                logging.critical("Max retries reached. Exiting Kafka consumer loop.")
                return
            logging.info(f"Retrying Kafka connection in 5 seconds... (Attempt {retries}/{max_retries})")
            await asyncio.sleep(5)

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
            await asyncio.sleep(5)
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            await asyncio.sleep(5)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(kafka_consumer_loop())

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
