import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst
import signal
from kafka import KafkaConsumer

# Initialize GStreamer
Gst.init(None)

# Create a GStreamer pipeline
pipeline = Gst.Pipeline.new("mypipeline")

# Create elements
kafka_consumer = Gst.ElementFactory.make("kafkameta", "kafkaconsumer")

if not pipeline or not kafka_consumer:
    print("Error creating pipeline elements.")
    exit(1)

# Add elements to the pipeline
pipeline.add(kafka_consumer)

# Set up the Kafka consumer
consumer = KafkaConsumer(
    'TutorialTopic',
    bootstrap_servers='localhost:9092',
    group_id='my-group',
    auto_offset_reset='earliest',
    enable_auto_commit=True
)

# Handle Ctrl+C to stop the pipeline
def sigint_handler(signum, frame):
    print("Stopping pipeline...")
    pipeline.set_state(Gst.State.NULL)
    Gtk.main_quit()

signal.signal(signal.SIGINT, sigint_handler)

# Function to intercept and print Kafka messages
def intercept_kafka_messages():
    for message in consumer:
        print(f"Received Kafka message: {message.value.decode('utf-8')}")

# Run the GStreamer main loop in a separate thread
Gst.main_thread_enter()

# Start Kafka message interception in a separate thread
import threading
interception_thread = threading.Thread(target=intercept_kafka_messages)
interception_thread.start()

# Set the pipeline to the "playing" state
pipeline.set_state(Gst.State.PLAYING)

# Join the interception thread to wait for it to finish
interception_thread.join()
