import pymongo
import pika
import json
from datetime import datetime

# MongoDB connection parameters
MONGO_URI = 'mongodb://localhost:27017/'
MONGO_DB = 'mqtt_data'
MONGO_COLLECTION = 'statuses'

# connection to MongoDB
client = pymongo.MongoClient(MONGO_URI)
db = client[MONGO_DB]
collection = db[MONGO_COLLECTION]

def callback(ch, method, properties, body):
    message = json.loads(body)
    message['timestamp'] = datetime.utcnow()

    collection.insert_one(message)
    print(f"Stored message: {message}")

def main():
    RABBITMQ_HOST = 'localhost'

    connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
    channel = connection.channel()

    channel.queue_declare(queue='mqtt_queue')

    channel.basic_consume(queue='mqtt_queue', on_message_callback=callback, auto_ack=True)

    print("Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()

if __name__ == "__main__":
    main()
