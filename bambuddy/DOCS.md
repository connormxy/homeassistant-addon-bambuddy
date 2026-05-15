# Bambuddy Home Assistant Add-on

## Configuration Options

This add-on provides several configuration options to customize your Bambuddy experience. Most users can leave these at their default values.

### Slicer Configuration
Because Bambuddy relies on a headless browser to generate G-code via Slicers, the Slicer APIs must be run in separate, isolated containers (provided in this repository).

*   **`orcaslicer_api_url`**: The internal URL pointing to the OrcaSlicer API container. 
    *   *Default*: `http://localhost:3003` 
    *   *(Note: Because Bambuddy uses host networking, `localhost` perfectly resolves to the port exposed by the separate Slicer Add-on!)*
*   **`bambu_studio_api_url`**: The internal URL pointing to the Bambu Studio API container.
    *   *Default*: `http://localhost:3001`
*   **`preferred_slicer`**: Select which slicer engine you want Bambuddy to use by default.

### Security
*   **`mfa_encryption_key`**: A 32-character string used to encrypt the MFA database. Leave blank for default internal security, or define your own for maximum security.

### Database
*   **`database_url`**: By default, Bambuddy creates a local `bambuddy.db` file in your `/share/bambuddy/data` folder. If you are a power user and want to connect to an external PostgreSQL database for high availability, enter the connection string here (e.g., `postgresql+asyncpg://user:pass@192.168.1.50/bambuddy`). Otherwise, **leave this blank**.

### Virtual Printer Configuration
*   **`virtual_printer_pasv_address`**: Bambuddy can emulate a physical printer to trick Bambu Studio/OrcaSlicer into sending files to it directly. This emulation uses the FTP protocol. Passive FTP (PASV) requires the server to tell the client what IP address to use for the data connection. 
    *   If Bambuddy is running behind complex routing, you may need to explicitly tell it your Home Assistant machine's IP address (e.g., `192.168.1.100`) so it hands out the correct IP to your slicer software. 
    *   For most flat local networks, you can **leave this blank**.

### MQTT Relay Settings
Bambuddy connects directly to your printer to monitor it, but it can also "Relay" these events (Print Started, Filament Low, etc.) to your Home Assistant MQTT broker so you can build automations around them.

*   **`mqtt_enabled`**: Toggle to `true` to turn on the relay.
*   **`mqtt_broker`**: The address of your MQTT broker. If you use the official Home Assistant Mosquitto Add-on, the internal slug `core-mosquitto` is pre-populated and works automatically!
*   **`mqtt_port`**: Typically `1883`.
*   **`mqtt_username`**: Your Home Assistant/Mosquitto username.
*   **`mqtt_password`**: Your Home Assistant/Mosquitto password. *Tip: You can securely use your secrets.yaml file by entering `!secret my_mqtt_password` here.*
*   **`mqtt_topic_prefix`**: The root topic for events (default: `bambuddy`).
*   **`mqtt_use_tls`**: Toggle if your broker requires secure connections.

### Network Ports (Advanced)
Because Bambuddy relies on emulating physical Bambu Lab printer hardware to capture print jobs via the "Virtual Printer" feature, it must run in `host_network` mode. This means it binds directly to your Home Assistant host's network interfaces.

It uses the following ports internally. **If you have other Add-ons using these ports, Bambuddy's Virtual Printer feature may fail to start:**
*   **8000 (TCP)**: The Bambuddy Web UI.
*   **8883 (TCP)**: MQTT Status Stream (Conflicts with Mosquitto Add-on if TLS is enabled on default port. You may need to change Mosquitto's SSL port to 18883/18884).
*   **3000 & 3002 (TCP)**: Virtual Printer Handshake / Slicer proxy (Conflicts with Z-Wave JS UI. You must change Z-Wave JS UI's host port if installed).
*   **322 & 6000 (TCP)**: RTSP Camera streaming ports.
*   **990 (TCP) & 50000-50100 (TCP)**: FTPS server and dynamic file upload ports. 
*   **2021 (UDP)**: Virtual Printer SSDP / mDNS auto-discovery broadcast.

---
## Support
If you have issues, please check the `/share/bambuddy/logs` directory via your Home Assistant File editor or Samba share.
