FROM python:3

# Install necessary tools
RUN apt-get update && apt-get install -y wget tar

# Install Kafka tools
RUN wget https://archive.apache.org/dist/kafka/2.6.0/kafka_2.13-2.6.0.tgz && \
    tar -xvzf kafka_2.13-2.6.0.tgz && \
    cp kafka_2.13-2.6.0/bin/kafka-consumer-groups.sh /usr/local/bin/kafka-consumer-groups && \
    cp kafka_2.13-2.6.0/bin/kafka-run-class.sh /usr/local/bin/ && \
    cp -r kafka_2.13-2.6.0/libs /usr/local/kafka-libs && \
    rm -rf kafka_2.13-2.6.0* 

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
CMD [ "python", "-u", "./app.py" ]
