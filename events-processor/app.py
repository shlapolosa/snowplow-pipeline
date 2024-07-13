import snowplow_analytics_sdk.event_transformer
import snowplow_analytics_sdk.snowplow_event_transformation_exception
import logging
from quixstreams import Application
from quixstreams.models.serializers import Deserializer

class SnowplowThriftDeserializer(Deserializer):
    def __call__(self, value, ctx=None):
        try:
            # Decode the value from bytes to a string
            decoded_value = value.decode('utf-8')
            # Transform Thrift-encoded message to JSON
            json_data = snowplow_analytics_sdk.event_transformer.transform(decoded_value)
            logging.debug("Transformed Thrift to JSON: %s", json_data)
            # Ensure json_data is a dict (which is iterable in the context needed)
            if isinstance(json_data, dict):
                return [json_data]
            else:
                logging.error(f"Unexpected data type after transformation: {type(json_data)}")
                return None
        except Exception as e:
            logging.error(f"Failed to deserialize message: {e}")
            return None

def main():
    logging.info("START")
    app = Application(
        broker_address="kafka:29092,kafka.confluent.svc.cluster.local:9092",
        loglevel="DEBUG",
        auto_offset_reset="latest",
        consumer_group="event_processor"
    )

    # Define input topic with custom deserializer
    input_topic = app.topic("snowplow_enriched_good", value_deserializer=SnowplowThriftDeserializer())
    output_topic = app.topic("snowplow_json_event", value_serializer="json")

    def to_json(msg):
        logging.debug("Raw Message After: %s", msg)
        return msg  # Already transformed to JSON by the custom deserializer

    # Create DataFrame for input topic
    sdf = app.dataframe(input_topic)
    sdf = sdf.filter(lambda msg: msg is not None)  # Filter out None values if deserialization fails
    sdf = sdf.apply(to_json)
    sdf = sdf.to_topic(output_topic)

    app.run(sdf)

if __name__ == "__main__":
    logging.basicConfig(level="DEBUG")
    main()
