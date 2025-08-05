# Smart Fire Alert System



---


# Team members & contributions



---

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
