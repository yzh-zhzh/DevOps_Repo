# Smart Fire Alarm System 🔥

An IoT-based fire detection and alert system with real-time monitoring, automated emergency response, and web interface.

![System Overview](./images/system-overview.png)

## 📋 Table of Contents

- [Features](#features)
- [Hardware Components](#hardware-components)
- [System Architecture](#system-architecture)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Web Interface](#web-interface)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)

## ✨ Features

- **Multi-sensor Fire Detection** - Temperature, smoke (IR + LDR), and humidity monitoring
- **Automated Emergency Response** - Sprinkler activation and water flow control
- **Real-time Notifications** - Email and Telegram alerts
- **Web Dashboard** - Live monitoring and user management
- **Manual Override** - Keypad-based emergency shutdown with passcode
- **Video Recording** - Automatic incident documentation
- **RFID Access Control** - Secure system activation

![Hardware Setup](./images/hardware-setup.png)

## 🔧 Hardware Components

| Component | Quantity | Purpose |
|-----------|----------|---------|
| Raspberry Pi 4 | 1 | Main controller |
| DHT22 Sensor | 1 | Temperature/Humidity |
| IR Sensor | 1 | Smoke detection |
| LDR | 1 | Light level monitoring |
| Moisture Sensor | 1 | Water confirmation |
| Servo Motor | 1 | Sprinkler positioning |
| DC Motor | 1 | Water pump |
| RFID Reader | 1 | Access control |
| LCD Display (16x2) | 1 | Status display |
| 4x4 Keypad | 1 | Manual input |
| Buzzer | 1 | Audio alerts |
| LED | 1 | Visual indicators |
| Camera Module | 1 | Recording |

![Hardware Components](./images/hardware-components.png)

## 🏗️ System Architecture

```
Sensors → Raspberry Pi → Emergency Response
   ↓           ↓              ↓
 Data      Processing     Actuators
Collection   & Logic      & Alerts
```

### Core Components:
- **Fire Detection Engine** - Multi-parameter detection logic
- **Emergency Response System** - Automated sprinkler and alerts
- **Web Interface** - Real-time dashboard and user management
- **Manual Override** - Emergency shutdown capability

![System Architecture](./images/architecture-diagram.png)

## 🚀 Installation

### Prerequisites
- Raspberry Pi 4 with Raspbian OS
- Python 3.8+
- Internet connection

### Quick Setup

```bash
# Clone repository
git clone https://github.com/yourusername/smart-fire-alarm-system.git
cd smart-fire-alarm-system

# Initialize submodules
git submodule init
git submodule update

# Install dependencies
pip3 install flask picamera2 RPi.GPIO requests

# Configure system
cp config.json.template config.json
nano config.json

# Run system
python3 src/main.py
```

### Hardware Setup
1. Connect sensors according to pin configuration
2. Ensure proper power supply for motors
3. Test individual components before integration

![Installation Guide](./images/installation-guide.png)

## ⚙️ Configuration

Edit `src/config.json`:

```json
{
  "location": "Your Location",
  "recipient_email": "alert@example.com",
  "telegram_bot_token": "YOUR_BOT_TOKEN",
  "telegram_chat_id": "YOUR_CHAT_ID"
}
```

### Key Settings:
- **Temperature Threshold**: Default 40°C (configurable in code)
- **Smoke Detection**: IR + LDR combination
- **Manual Override Code**: Default "1234"
- **Recording Duration**: 10 seconds per incident

## 📱 Usage

### Starting the System
```bash
# Main fire detection system
python3 src/main.py

# Web dashboard (separate terminal)
python3 src/app.py
```

### Emergency Response Sequence
1. **Fire Detected** → Visual/audio alerts activate
2. **Sprinkler System** → Servo positions, DC motor pumps water
3. **Notifications** → Email and Telegram alerts sent
4. **Recording** → Camera starts documenting incident
5. **Manual Override** → "*" + passcode + "#" to shutdown

### RFID Access
- Present RFID card to activate system
- System monitors continuously when activated

![Usage Flow](./images/usage-flow.png)

## 🌐 Web Interface

Access the dashboard at `http://raspberry-pi-ip:5000`

### Features:
- **Real-time Data** - Temperature, humidity readings
- **User Profiles** - Resident information and emergency contacts
- **System Status** - Current operational state
- **Firebase Authentication** - Secure user management

### Pages:
- **Dashboard** (`/`) - Live sensor data
- **Profile** (`/profile`) - User information
- **Registration** - New user signup
- **Login** - User authentication

![Web Dashboard](./images/web-dashboard.png)

## 🧪 Testing

### Run Tests
```bash
# Fire detection tests
python3 -m pytest src/test_Fire_detection.py -v

# Manual testing
python3 src/Fire_detection.py  # Test detection logic
python3 src/RFID.py           # Test RFID reader
```

### Test Scenarios:
- Smoke detection (IR + LDR)
- Temperature thresholds
- Manual override functionality
- Notification delivery

![Testing Results](./images/testing-results.png)

## 🔧 Troubleshooting

### Common Issues

**Fire Detection Not Working**
```bash
# Check sensor connections
python3 -c "from hal import hal_temp_humidity_sensor as temp; temp.init(); print(temp.read_temp_humidity())"
```

**Web Interface Not Accessible**
```bash
# Check if Flask is running
ps aux | grep python3
netstat -tlnp | grep :5000
```

**Notifications Not Sending**
- Verify internet connection
- Check email/Telegram credentials in config.json
- Test with minimal notification script

**Camera Not Recording**
```bash
# Check camera module
vcgencmd get_camera
```

### Log Files
Check system logs for detailed error information:
```bash
tail -f /var/log/syslog | grep python
```

## 📊 API Endpoints

- `GET /` - Main dashboard
- `GET /data` - JSON sensor data
- `GET /profile` - User profile page

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/new-feature`)
3. Commit changes (`git commit -am 'Add new feature'`)
4. Push to branch (`git push origin feature/new-feature`)
5. Create Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Team

### Colin Wee


---
## Smoke Detection
- Developed and integrated the IR sensor.
- Developed and integrated the LDR sensor.
- Implemented logic to require both sensors to detect smoke, reducing false positives.
- Created `pytest` tests for smoke detection module.

## Fire Detection
- Integrated the temperature sensor.
- Combined temperature sensor inputs with the smoke detection logic.
- Fire is detected when temperature > 40°C or when smoke is detected.
- Created `pytest` tests for the fire detection module.

## RFID System
- Integrated the RFID module.
- Programmed the function to return `True` upon card detection (acts as activation system).
- Created `pytest` tests for RFID functionality.

## System Integration
- Integrated all hardware code.
- Merged all team members’ code bases.
- Connected output modules with input modules on the Raspberry Pi.

## Main Program (`main.py`)
- Programmed RFID detection to activate all sensors.
- Utilized threading to enable all sensors to detect in the background.
- Upon fire detection:
  - Intercept signal sent.
  - DC motor, servo motor, and buzzer are activated.
  - Ultrasound sensor activated to detect presence in the room.
  - Moisture sensor activated to ensure sprinkler functionality.
  - Camera module activated to relay images to the website.
  - Notifications sent via Telegram and email.
- Keypad functionality:
  - Entering ‘1234’ acts as a kill switch, turning off all systems.
  - All sensors resume detection after reset.

## Documentation
- Edited SRS document (v1):
  - Refined requirements.
  - Created software architecture diagram (v1).

---
### 🔹 **Meenakshi Ramasubramanian**

#### 📄 Software Requirements Specification (SRS)
- Designed the **System Architecture Diagram** to visualize interactions between hardware, backend, and frontend components.
- Created **Use Case Diagrams** to define system functionalities and user interactions.
- Defined **Functional and Non-functional Requirements** to guide development and ensure system performance and reliability.

#### 🚀 Sprint Planning & Management
- Served as **Sprint Manager**, responsible for coordinating stand-ups, tracking sprint progress, and ensuring timely task completion.
- Actively participated in **Sprint Planning**, including task breakdown, priority setting, and timeline estimation.
- Facilitated effective collaboration and integration of hardware and software tasks across team members.

#### 💻 Website Development (Frontend & Backend)
- **Frontend:**
  - Built interactive web pages using **HTML**, **CSS**, and **JavaScript**.
  - Designed and implemented the UI for user registration, login, live camera feed, and fire alert dashboard.
- **Backend:**
  - Utilized **Flask** to create backend APIs for handling sensor data, user inputs, and triggering alerts.
  - Structured and handled data using **JSON** for communication between components.
- **Authentication & Database:**
  - Integrated **Firebase Authentication** for secure user login and registration.
  - Created and maintained a **Firebase Realtime Database** to store user credentials and fire detection logs.

#### 🔌 Hardware Integration
- Developed the **camera functionality** using **Raspberry Pi** and **Picamera2**.
  - Configured the system to capture **live CCTV footage** when a fire or gas alert is triggered.
  - Integrated the live video stream into the website for real-time monitoring.
- Established **hardware-to-software communication** through APIs, linking sensor data with the alert system on the website.

---

### **Phoo Pyae Sone Aye**

#### Software Requirements Specification (SRS)
- Created the system architecture diagram for Version 1 (V1)
- Modified and added functional and non-functional requirements in Version 2 (V2)
- Created UML diagrams for V2:
  - Use Case Diagram  
  - System Architecture Diagram  
  - Software Architecture Diagram  

#### Website (Frontend)
- Developed **Dashboard** page to display:
  - Real-time **temperature**, **humidity**, and **smoke condition stage**
- Created **Profile** page to show:
  - Resident details (Name, Age, Room Number, Contact Number)
  - Fire alarm status
- Implemented dedicated CSS files:
  - Ensured consistent visuals
  - Focused on **readability and accessibility for elderly users**

#### Backend Integration
- Developed `app.py` to:
  - Fetch real-time sensor data from Raspberry Pi
  - Serve data to frontend via Flask
  - Auto-refresh every **3 seconds** for live updates
- Reconfiguration of new database at Firebase 
  - Create new database for storing user's informations
- Re-developed JSON-based communication to faciliate the data exchange 
  - Between Frontend pages
  - Between Backend  and Raspberry Pi board for seamless integration
- Full integration of website
  - Managed the overall system integration, ensuring the website functions reliably with the Raspberry Pi sensors and supports real-time monitoring.

#### Sensor Data Handling (Python Scripts)
- `temp_humidity_sensor.py`:  
  Continuously reads temperature and humidity from DHT sensor  
- `ultrasonic_sensor.py`:  
  Detects resident presence via ultrasonic sensing when fire is active  

---
### **Yao Zhenghan**

#### Software Requirements Specification (SRS)
- Edited Functional and Non-Functional Requirements (Version 1)
- Ensured alignment with client needs and sensor capabilities

#### Sprint Planning
- Updated Sprint Planning Template to Version 2
- Integrated planning tasks for the second phase of development

#### LCD Display Integration
- Programmed context-aware message displays:
  - **Idle State**: “Smart Fire Alert”, “System Ready!”
  - **Fire Detected State**: “FIRE DETECTED!”, water level %, release confirmation
  - **Override Mode**: Passcode prompts, success/failure messages
- Linked LCD responses to live sensor input

#### Keypad Module
- Integrated user override function via keypad
- Real-time display of entered keys for confirmation

#### Potentiometer Control
- Enabled dynamic control over water flow using DC motor
- LCD reflects volume adjustments for transparency

#### Servo Motor Functionality
- Simulated sprinkler rotation upon fire detection
- Operates independently of water flow regulation

#### DC Motor Management
- Controlled the sprinkler water flow
- Responsive to potentiometer adjustments

#### Buzzer Integration
- Activated alarm upon temperature-triggered fire detection
- Loud audio output for emergency awareness

#### Moisture Sensor Logic
- Detected presence of water to confirm sprinkler activation
- Displayed confirmation or error messages on LCD

#### Temperature Sensor (DHT)
- Triggered fire alert when temperature > 40°C
- Provided real-time temperature data for fire detection logic

---
---

**Emergency Contact**: For system emergencies, contact the configured email or Telegram alerts will be automatically sent.
