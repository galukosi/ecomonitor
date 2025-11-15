

# EcoMonitor

EcoMonitor is a web platform for monitoring IoT safety devices, starting with **GasGuard**.  
It provides user authentication, device registration by serial number, and real-time dashboards.  

## Features
- User registration & authentication.  
- Device linking via unique serial number.  
- Real-time GasGuard data monitoring.  
- Historical charts (PostgreSQL).  
- Device control from dashboard:
  - Switch to local/offline mode.  
  - Factory reset (EEPROM clear).  
  - Telegram alerts.  

## Tech stack
- **Backend:** Django + Django REST Framework  
- **Frontend:** HTML, CSS, JavaScript  
- **Database:** PostgreSQL  
- **API:** REST (data from ESP32)  

## 🔹 How to run
```bash
# Clone project
git clone https://github.com/trinity-corp/ecomonitor.git
cd ecomonitor

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start server
python manage.py runserver

```
Made by Andriy Tymchuk, 2025.
