from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from quixstreams import Application
from quixstreams.kafka.configuration import ConnectionConfig

import json
import asyncio
import logging
import os

logging.basicConfig(level=logging.INFO)

app = FastAPI()

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
                var messages = JSON.parse(event.data);
                console.log('WebSocket message received:', messages);  // Log the received messages
                messages.forEach(function(eventData) {
                    if (eventData.event_name === "mouse_move") {
                        var pos = eventData.unstruct_event_com_example_company_mouse_move_1;
                        drawDot(pos.posx, pos.posy, 'move');
                    } else if (eventData.event_name === "mouse_click") {
                        var pos = eventData.unstruct_event_com_example_company_mouse_click_1;
                        drawDot(pos.posx, pos.posy, 'click');
                    }
                });
            };

            function drawDot(x, y, type) {
                console.log('Received x: ' + x + ', y: ' + y);  // Log the coordinates
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

        # Define the ConnectionConfig with security parameters
    connection_config = ConnectionConfig(
        bootstrap_servers="pkc-12576z.us-west2.gcp.confluent.cloud:9092,kafka:29092,kafka.confluent.svc.cluster.local:9092",
        security_protocol="SASL_SSL",
        sasl_mechanism="PLAIN",
        sasl_username="UJXR2AHHSOHL2O4K",
        sasl_password="L4piWdT0pE4t+LiP5xLrkfWxmhePL8jdk0LaSX2N5cSevSBF1EHjr2oygqJX64FC"
    )

    kafka_app = Application(
        broker_address=connection_config,
        loglevel="DEBUG",
        consumer_group="websocket",
        auto_offset_reset="latest",
    )

    with kafka_app.get_consumer() as consumer:
        consumer.subscribe(["snowplow_json_event"])

        while True:
            msg = consumer.poll(1.0)
            
            if msg is None:
                await asyncio.sleep(1)
                continue
            if msg.error():
                logging.error(f"Consumer error: {msg.error()}")
                continue
            
            value = json.loads(msg.value().decode('utf-8'))
            await manager.send_message(json.dumps(value))
            offset = msg.offset()

            logging.info(f"{offset}  {value}")
            consumer.store_offsets(msg)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(kafka_consumer_loop())

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
