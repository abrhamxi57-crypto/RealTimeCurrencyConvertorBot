

# 💱 Currency Converter Telegram Bot

A Telegram bot built with Python that allows users to convert currencies in real time using exchange rate APIs. The bot is designed to provide fast, accurate, and user-friendly currency conversion directly inside Telegram.

---

# 📌 Project Description

This project is a Telegram-based currency converter that helps users quickly convert money from one currency to another without using a calculator or visiting a website.

The bot fetches live exchange rates from online APIs and returns converted values instantly. It also includes backup systems and local caching to ensure the service remains functional even if the primary API becomes unavailable.

---

# 🎯 Objectives

- Build a functional Telegram bot using Python
- Fetch and process live exchange rate data
- Practice API integration and JSON handling
- Implement backup and offline support systems
- Improve Python programming and problem-solving skills

---

# 👥 Target Users

This project is useful for:

- Travelers
- Online shoppers
- Forex learners
- E-commerce sellers
- Telegram users who need quick currency conversions

---

# 💡 Why This Project?

Currency values change frequently, and users often need fast conversions while chatting or browsing online.

Telegram bots provide a convenient and accessible way to automate tasks. This project combines:

- Python programming
- Telegram Bot API
- Real-time APIs
- Error handling
- Offline caching

into one practical application.

---

# ⚙️ Key Features

## 1. Quick Currency Conversion

Users can convert any amount between currencies using a simple command.

### Example

```bash
/convert 100 USD to EUR
```

### Example Output

```bash
100 USD = 92.45 EUR
```

The bot displays:

- Converted amount
- Exchange rate used
- Currency codes

---

## 2. Real-Time Exchange Rates

The bot fetches updated currency rates from online APIs.

Supported features:

- Live exchange rates
- Multiple global currencies
- Accurate conversion values

---

## 3. Multi-Currency Rate Summary

Users can request multiple exchange rates at once.

### Example

```bash
/rates USD
```

### Example Output

```bash
USD → EUR = 0.92
USD → GBP = 0.79
USD → JPY = 155.40
USD → CAD = 1.37
```

This feature is useful for travelers and business users comparing multiple currencies.

---

## 4. Error Handling

The bot handles invalid inputs and incorrect commands gracefully.

### Example

```bash
/convert abc USD EUR
```

### Response

```bash
Invalid amount. Please enter a numeric value.
```

### Example

```bash
/convert 100 US EUR
```

### Response

```bash
Invalid currency code. Use 3-letter currency codes like USD or EUR.
```

---

## 5. Offline Cache Support

The bot stores recent exchange rates locally in:

```bash
rates.json
```

If internet access or APIs fail, cached exchange rates are used temporarily.

---

# 🛠️ Technologies Used

| Technology       | Purpose                     |
| ---------------- | --------------------------- |
| Python           | Main programming language   |
| Telegram Bot API | Telegram integration        |
| JSON             | Data storage and processing |
| Requests Library | API communication           |
| Git & GitHub     | Version control             |
| ExchangeRate API | Live currency data          |

---

# 🌐 APIs Used

## Primary API

ExchangeRate API is used as the main source for currency exchange data.

### API Endpoint

```bash
https://v6.exchangerate-api.com/v6/{EXCHANGE_API_KEY}
```

The bot:

1. Sends a request to the API
2. Receives JSON exchange data
3. Extracts currency rates
4. Calculates converted amounts

---

## Backup API

If the main API fails, the bot switches to:

- Open FXEthio API

This improves reliability and reduces downtime.

---

## Final Emergency Fallback

If:

- Primary API fails
- Backup API fails
- Cache is unavailable

the bot will scrape publicly available forex values from the National Bank of Ethiopia (NBE) webpage.

Only public buy/sell exchange rates are extracted.

This method is used only as a last resort.

---

# 🧱 System Architecture

## Workflow

1. User sends command in Telegram
2. Telegram Bot API receives message
3. Python bot processes request
4. API / Cache fetches exchange rates
5. Bot calculates result
6. Result is returned to the user

## 📂 Project Directory Structure

```text
RealTimeCurrencyConvertorBot/
├── .env.example              # Environment variables template
├── .env                      # Local environment configuration (API keys & bot token)
├── .gitignore                # Git ignore rules for virtualenv, secrets, cache
├── requirements.txt          # Python project dependencies
├── README.md                 # Project documentation
├── main.py                   # Bot entry point and polling service
├── config.py                 # Central configuration and environment loader
├── data/                     # Local storage directory
│   ├── history.json          # User conversion history
│   ├── feedback.json         # User feedback log
│   ├── favorites.json        # Favorite currency pairs per user
│   └── rates_cache.json      # Offline rates cache with TTL
├── services/                 # Core business and integration services
│   ├── __init__.py
│   ├── storage_service.py    # Thread-safe JSON data storage service
│   └── currency_service.py   # Live API integration, failover & caching
└── handlers/                 # Modular Telegram bot handlers
    ├── __init__.py
    ├── commands.py           # /start, /help, /convert, /rates
    ├── callbacks.py          # Inline buttons (rates & favorites interaction)
    ├── messages.py           # Menu buttons and conversational message flow
    ├── favorites.py          # Favorite currency pair management
    └── keyboards.py          # Reply and inline keyboard builders
```

## 🚀 Setup and Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/abrhamxi/SE_python_project2025.git
   cd RealTimeCurrencyConvertorBot
   ```

2. **Create and activate a virtual environment:**
   ```bash
   virtualenv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env and insert your TELEGRAM_TOKEN and EXCHANGE_API_KEY
   ```

5. **Run the bot:**
   ```bash
   python main.py
   ```

# 🗓️ Development Plan

| Week   | Task                      |
| ------ | ------------------------- |
| Week 1 | Project idea and README   |
| Week 2 | Telegram bot setup        |
| Week 3 | API integration           |
| Week 4 | Currency conversion logic |
| Week 5 | Error handling and cache  |
| Week 6 | Testing and documentation |

---

# 🔒 Security & Reliability

The bot includes:

- Input validation
- Exception handling
- Backup APIs
- Offline cache support

These features help improve system reliability and user experience.

---

# ⚠️ Limitations

- Requires internet connection for live rates
- Depends on third-party APIs
- Free APIs may have request limits

---

# 🚀 Future Improvements

Possible future upgrades:

- Graphical dashboard
- Voice command support
- Historical currency charts
- AI-powered currency prediction
- Web deployment
- User authentication system

---

# 📸 Screenshots

<img width="399" height="379" alt="image" src="https://github.com/user-attachments/assets/7c7fc05d-1f32-4862-ac17-0c38ede108ec" />


Example:

- Bot command usage
- Conversion result
- Error messages

---

# 📚 Learning Outcomes

Through this project, I learned:

- Python programming
- API integration
- Telegram bot development
- JSON data processing
- Error handling
- GitHub project management

---

# 👨‍💻 Author

Name: Abrham Zimbelachew
Project: Currency Converter Telegram Bot
Year: 2026

---

# ✅ Conclusion

The Currency Converter Telegram Bot is a practical Python project that demonstrates real-world API integration, Telegram automation, and software reliability techniques.

The system provides users with fast and convenient currency conversion while maintaining stability through backup APIs and offline cache support.
```
