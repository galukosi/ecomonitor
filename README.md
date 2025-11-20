![Знімок екрана_20-11-2025_215157_ecomonitor-znv9 onrender com](https://github.com/user-attachments/assets/356f25b8-c4af-4724-87a8-9d5992b29017)

# EcoMonitor

EcoMonitor is a web platform for monitoring -Guard devices, such as GasGuard, TempGuard and HumidGuard.
It provides user authentication, device registration by serial number, real-time dashboards, device management.  

## Features
- User registration and authentication.
- Device linking via unique serial number.
- Real-time measurement monitoring.
- Historical data storage (PostgreSQL):
  - View all readings on the website.
  - Export all readings in JSON.
  - Export all readings in CSV.
  - Clear all readings.
- Send command to the device:
  - Enable/disable screen.
  - Reboot.
  - Factory reset.
- Configuration options:
  - Set minimum and maximum safe thresholds.
  - Link custom Telegram bot for getting alerts.

## Tech stack
- **Backend:** Django + Django REST Framework  
- **Frontend:** HTML, CSS, JavaScript  
- **Database:** PostgreSQL  
- **API:** REST (data from ESP32)

## Supported devices
- **[GasGuard](https://github.com/trinity-corp/gasguard)**
- **[TempGuard](https://github.com/trinity-corp/tempguard)**
- **[HumidGuard](https://github.com/trinity-corp/humidguard)**

## How to run
```bash
# Clone project
git clone https://github.com/trinity-corp/ecomonitor.git
cd ecomonitor

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Start server
python manage.py runserver

```

## Future ideas
- More -Guard devices.
- Detailed readings management, such as selecting specific values readings, or readings from specific dates.
- Translating the website to other languages.
- Advanced device management.

Made by Andriy Tymchuk, 2025.
