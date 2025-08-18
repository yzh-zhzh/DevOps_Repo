### **Yao Zhenghan**

---

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
