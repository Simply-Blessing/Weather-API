# 🌦 Weather API

A simple Flask-based Weather API that fetches live weather data from the **OpenWeatherMap API**, caches results with **Redis**, and applies **rate limiting** to prevent abuse.

---

## 🧰 Features

- 🌍 Get current weather by city name
- ⚡ Caching with **Redis** (12-hour expiry)
- 🚦 Rate limiting using **Flask-Limiter**
- 😎 Weather condition emojis for easy reading
- 🔐 Secure API key loading via `.env`

---

## 🏗️ Tech Stack

- **Flask** — lightweight web framework
- **Redis** — in-memory cache for API responses
- **Flask-Limiter** — request rate limiting
- **Requests** — for external API calls
- **python-dotenv** — load environment variables
- **OpenWeatherMap API** — weather data source

---

## 📦 Installation

### 1️⃣ Clone the repository

```bash
git clone https://github.com/yourusername/weather-api.git
cd weather-api
```

2️⃣ Create and activate a Conda environment

```bash
conda create -n weatherapi python=3.11 -y
conda activate weatherapi
```

3️⃣ Install dependencies

```bash
pip install flask flask-limiter requests redis python-dotenv
```

4️⃣ Install Redis (if you are using Anaconda Powershell and windows)
check out this installation guide:
https://medium.com/@baertschi91/redis-installation-guide-for-windows-67ca177e2836

```bash
conda install -c binstar redis-server
conda install -c anaconda redis-py
```

5️⃣ Run Redis on a powershell prompt in your conda environment

```bash
redis-server
```

6️⃣ On another powershell prompt you connect Redis using this

```bash
redis-cli ping
```

---

## 🚀 Run the App

Sign in at [OpenWeatherMap](https://openweathermap.org/) to get your free API key.

```bash
# .env
API_KEY=your_openweathermap_api_key
```

Running it on the command line or powershell

```bash
python app.py
```

By default, the app runs at:

```bash
http://127.0.0.1:5000
```

---

## 🌤 Usage

Get current weather
```bash
http://127.0.0.1:5000/weather?city=<city_name>
```
```bash
http://127.0.0.1:5000/weather?city=london
```
Response:

```bash
{
  "city": "london",
  "temperature": "17°C",
  "emoji": "☁",
  "description": "scattered clouds"
}
```

---

## 🧠 How It Works

- The user sends a request like /weather?city=london.
- The app first checks Redis cache using the key weather:london.
- If data exists → it’s served instantly from cache.
- If not → it fetches from OpenWeatherMap, parses, stores it in Redis (12-hour TTL), and returns JSON.

---

## Project Inspiration

[Weather API Wrapper Service](https://roadmap.sh/projects/weather-api-wrapper-service)

[Weather APP from Bro code](https://youtu.be/Q4377DH5Jso)
