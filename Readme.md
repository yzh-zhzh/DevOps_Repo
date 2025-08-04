#  Smart Automate Fire Alert System 

## Team Members & Contributions

---

### **Phoo Pyae Sone Aye**

#### 📄 Software Requirements Specification (SRS)
- Created the system architecture diagram for Version 1 (V1)
- Modified and added functional and non-functional requirements in Version 2 (V2)
- Created UML diagrams for V2:
  - Use Case Diagram  
  - System Architecture Diagram  
  - Software Architecture Diagram  

#### 💻 Website (Frontend)
- Developed **Dashboard** page to display:
  - Real-time **temperature**, **humidity**, and **smoke condition stage**
- Created **Profile** page to show:
  - Resident details (Name, Age, Room Number, Contact Number)
  - Fire alarm status
- Implemented dedicated CSS files:
  - Ensured consistent visuals
  - Focused on **readability and accessibility for elderly users**

#### 🔧 Backend Integration
- Developed `app.py` to:
  - Fetch real-time sensor data from Raspberry Pi
  - Serve data to frontend via Flask
  - Auto-refresh every **3 seconds** for live updates

#### 📡 Sensor Data Handling (Python Scripts)
- `temp_humidity_sensor.py`:  
  Continuously reads temperature and humidity from DHT sensor  
- `ultrasonic_sensor.py`:  
  Detects resident presence via ultrasonic sensing when fire is active  

---