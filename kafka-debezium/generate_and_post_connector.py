import os
import json
import requests
from dotenv import load_dotenv

# -----------------------------
# Load environment variables
# -----------------------------
load_dotenv()

# -----------------------------
# MySQL Debezium Connector Config
# -----------------------------
connector_config = {
    "name": "mysql-connector",
    "config": {
        "connector.class": "io.debezium.connector.mysql.MySqlConnector",
        "database.hostname": os.getenv("DB_HOST", "mysql"),  # mysql container name
        "database.port": os.getenv("DB_PORT", "3306"),
        "database.user": os.getenv("DB_USER", "newuserpostgres"),
        "database.password": os.getenv("DB_PASSWORD", "newsecurepassword123"),
        "database.server.id": "1",
        "database.server.name": "banking-mysql",
        "database.include.list": "banking",
        "database.allowPublicKeyRetrieval": "true",
        "database.snapshot.locking.mode": "none",
        "table.include.list": "banking.customers,banking.accounts,banking.transactions",
        "topic.prefix": "banking-mysql",
        "snapshot.mode": "schema_only",
        "schema.history.internal.kafka.bootstrap.servers": "kafka:9092",
        "schema.history.internal.kafka.topic": "schema-changes.banking-mysql",
        "tombstones.on.delete": "false",
        "decimal.handling.mode": "double"
    }
}

# -----------------------------
# Deploy to Debezium Connect
# -----------------------------
url = "http://localhost:8083/connectors"
headers = {"Content-Type": "application/json"}

response = requests.post(url, headers=headers, data=json.dumps(connector_config))

# -----------------------------
# Status Check
# -----------------------------
if response.status_code == 201:
    print("✅ MySQL Debezium Connector CREATED!")
    print("📊 Topics created:")
    print("   - banking-mysql.banking.customers")
    print("   - banking-mysql.banking.accounts") 
    print("   - banking-mysql.banking.transactions")
elif response.status_code == 409:
    print("⚠️  Connector already exists. Checking status...")
    status_url = "http://localhost:8083/connectors/mysql-connector/status"
    status = requests.get(status_url).json()
    print(f"   Status: {status}")
else:
    print(f"❌ Error {response.status_code}: {response.text}")

print("\n🔍 Next: Run data generator + watch Kafka stream!")