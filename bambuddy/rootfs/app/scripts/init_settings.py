import os
import sqlite3
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("init_mqtt")

DB_PATH = "/share/bambuddy/data/bambuddy.db"

def upsert_setting(cursor, key, value):
    if value is None:
        return
    
    # Check if exists
    cursor.execute("SELECT id FROM settings WHERE key = ?", (key,))
    row = cursor.fetchone()
    
    if row:
        logger.info(f"Updating setting {key}")
        cursor.execute("UPDATE settings SET value = ?, updated_at = CURRENT_TIMESTAMP WHERE key = ?", (str(value), key))
    else:
        logger.info(f"Inserting setting {key}")
        cursor.execute("INSERT INTO settings (key, value, created_at, updated_at) VALUES (?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)", (key, str(value)))

def main():
    if not os.path.exists(DB_PATH):
        logger.info("Database not found, skipping MQTT initialization")
        return

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Create table if it doesn't exist (e.g. first run)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS settings (
                id INTEGER PRIMARY KEY,
                key TEXT UNIQUE,
                value TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

        settings_to_sync = {
            "mqtt_enabled": os.environ.get("MQTT_ENABLED"),
            "mqtt_broker": os.environ.get("MQTT_BROKER"),
            "mqtt_port": os.environ.get("MQTT_PORT"),
            "mqtt_username": os.environ.get("MQTT_USERNAME"),
            "mqtt_password": os.environ.get("MQTT_PASSWORD"),
            "mqtt_topic_prefix": os.environ.get("MQTT_TOPIC_PREFIX"),
            "mqtt_use_tls": os.environ.get("MQTT_USE_TLS"),
            "ha_enabled": os.environ.get("HA_ENABLED_CONFIG"),
            "ha_url": os.environ.get("HA_URL_CONFIG"),
            "ha_token": os.environ.get("HA_TOKEN_CONFIG"),
        }

        for key, value in settings_to_sync.items():
            if value and value != "":
                # Convert "true"/"false" strings to expected format if needed
                if value.lower() == "true":
                    upsert_setting(cursor, key, "true")
                elif value.lower() == "false":
                    upsert_setting(cursor, key, "false")
                else:
                    upsert_setting(cursor, key, value)

        conn.commit()
        conn.close()
        logger.info("MQTT and HA settings synchronized successfully")
    except Exception as e:
        logger.error(f"Failed to synchronize settings: {e}")

if __name__ == "__main__":
    main()
