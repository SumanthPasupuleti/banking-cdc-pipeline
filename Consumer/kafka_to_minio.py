import boto3
from kafka import KafkaConsumer
import json
import pandas as pd
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

TOPICS = [
    "banking-mysql.banking.customers",
    "banking-mysql.banking.accounts",
    "banking-mysql.banking.transactions",
]

consumer = KafkaConsumer(
    *TOPICS,
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    group_id=os.getenv("KAFKA_GROUP"),
    value_deserializer=lambda x: json.loads(x.decode("utf-8")),
)

s3 = boto3.client(
    "s3",
    region_name=os.getenv("AWS_REGION"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)
bucket = os.getenv("S3_BUCKET")


if bucket not in existing_buckets:
    s3.create_bucket(
        Bucket=bucket,
        CreateBucketConfiguration={"LocationConstraint": os.getenv("AWS_REGION")}
    )
    print(f"✅ Created bucket: {bucket}")

def write_to_minio(table_name, records):
    if not records:
        return
    df = pd.DataFrame(records)
    date_str = datetime.now().strftime("%Y-%m-%d")
    time_str = datetime.now().strftime("%H%M%S%f")
    file_path = f"{table_name}_{date_str}_{time_str}.parquet"
    df.to_parquet(file_path, engine="fastparquet", index=False)
    s3_key = f"{table_name}/date={date_str}/{table_name}_{time_str}.parquet"
    s3.upload_file(file_path, bucket, s3_key)
    os.remove(file_path)
    print(f"✅ Uploaded {len(records)} records to s3://{bucket}/{s3_key}")

batch_size = 50
buffer = {topic: [] for topic in TOPICS}

print("✅ Connected to Kafka. Listening for messages...")

try:
    for message in consumer:
        topic = message.topic
        event = message.value or {}
        payload = event.get("payload", {})
        record = payload.get("after")

        if record and topic in buffer:
            buffer[topic].append(record)
            print(f"[{topic}] -> {record}")

        if topic in buffer and len(buffer[topic]) >= batch_size:
            table_name = topic.split(".")[-1]
            write_to_minio(table_name, buffer[topic])
            buffer[topic] = []

except KeyboardInterrupt:
    print("\nInterrupted by user. Flushing remaining records...")

finally:
    for topic, records in buffer.items():
        if records:
            table_name = topic.split(".")[-1]
            write_to_minio(table_name, records)
    consumer.close()
    print("✅ Consumer closed.")