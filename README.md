# Finance AI Bot 🤖💰

Telegram bot using aiogram with Gemini AI integration for voice transcription and financial data extraction.

## Features ✨

- 📝 Voice message transcription using Gemini API
- 💰 Automatic financial data extraction from text/voice
- 🗄️ PostgreSQL database with Tortoise ORM
- 🔄 Database migrations with Aerich
- 🎯 Commands: /start, /help, /login
- 📊 JSON format output for financial data

## Technology Stack 🛠️

- **Bot Framework**: aiogram 3.4.1
- **Database**: PostgreSQL with Tortoise ORM
- **Migrations**: Aerich
- **AI**: Google Gemini API
- **Language**: Python 3.10+

## Project Structure 📁

```
finance-ai-bot/
├── app/
│   ├── handlers/           # Bot command and message handlers
│   │   ├── start.py       # /start command
│   │   ├── help.py        # /help command
│   │   ├── login.py       # /login command
│   │   └── voice.py       # Voice and text message handler
│   ├── models/            # Database models
│   │   └── user.py        # User model
│   ├── services/          # Business logic services
│   │   └── gemini_service.py  # Gemini API integration
│   └── __init__.py
├── config/
│   ├── settings.py        # Application settings
│   ├── database.py        # Database configuration
│   └── __init__.py
├── migrations/            # Database migrations (auto-generated)
├── main.py               # Application entry point
├── requirements.txt      # Python dependencies
├── pyproject.toml       # Aerich configuration
├── .env.example         # Environment variables template
└── README.md            # This file
```

## Installation 🚀

### Prerequisites

- Python 3.10 or higher
- PostgreSQL database
- Telegram Bot Token (from @BotFather)
- Google Gemini API Key

### Setup Steps

1. **Clone the repository**
```bash
git clone https://github.com/jaloliddin1006/finance-ai-bot.git
cd finance-ai-bot
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env file with your credentials
```

Required environment variables:
- `BOT_TOKEN`: Your Telegram Bot token
- `DB_HOST`: PostgreSQL host (default: localhost)
- `DB_PORT`: PostgreSQL port (default: 5432)
- `DB_USER`: PostgreSQL username
- `DB_PASSWORD`: PostgreSQL password
- `DB_NAME`: Database name
- `GEMINI_API_KEY`: Your Google Gemini API key
- `DEBUG`: Enable debug mode (True/False)

5. **Initialize database migrations**
```bash
aerich init -t config.database.TORTOISE_ORM
aerich init-db
```

6. **Run the bot**
```bash
python main.py
```

## Database Migrations 🔄

### Create a new migration
```bash
aerich migrate --name migration_name
```

### Apply migrations
```bash
aerich upgrade
```

### Rollback migration
```bash
aerich downgrade
```

## Usage 📱

### Commands

- `/start` - Start the bot and register user in database
- `/help` - Show help message and usage instructions
- `/login` - Check login status and user information

### Voice Messages

1. Send a voice message to the bot
2. The bot will:
   - Transcribe the audio to text
   - Extract financial data (type, amount, category, description, date)
   - Return both the transcription and JSON formatted data

### Text Messages

Send a text message describing a financial transaction, for example:
- "Men bugun 50000 so'm oziq-ovqatga sarfladim"
- "I received 100 dollars salary today"

The bot will extract and return financial data in JSON format.

## JSON Output Format 📄

```json
{
  "type": "income/expense",
  "amount": 0,
  "category": "category_name",
  "description": "transaction_description",
  "date": "transaction_date"
}
```

## Development 👨‍💻

### Code Structure

- **Handlers**: Process user commands and messages
- **Models**: Define database schema
- **Services**: Business logic and external API integrations
- **Config**: Application configuration and settings

### Adding New Features

1. Create new handler in `app/handlers/`
2. Add router to `app/handlers/__init__.py`
3. Update database models if needed
4. Create migration if database schema changed

## Security 🔒

- Never commit `.env` file
- Keep API keys and tokens secret
- Use environment variables for sensitive data
- Regularly update dependencies

## Troubleshooting 🔧

### Database connection error
- Check PostgreSQL is running
- Verify database credentials in `.env`
- Ensure database exists

### Bot not responding
- Verify `BOT_TOKEN` is correct
- Check internet connection
- Review logs for errors

### Gemini API errors
- Verify `GEMINI_API_KEY` is valid
- Check API quota and limits
- Review Gemini API documentation

## Contributing 🤝

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License 📝

This project is licensed under the MIT License.

## Support 💬

For issues, questions, or contributions, please open an issue on GitHub.

## Roadmap 🗺️

- [ ] Full audio transcription support
- [ ] Multiple language support
- [ ] Transaction history
- [ ] Budget tracking
- [ ] Financial reports
- [ ] Export to Excel/CSV
- [ ] User preferences
- [ ] Category management

## Acknowledgments 🙏

- [aiogram](https://github.com/aiogram/aiogram) - Modern Telegram Bot framework
- [Tortoise ORM](https://github.com/tortoise/tortoise-orm) - Easy async ORM
- [Google Gemini](https://ai.google.dev/) - AI-powered text processing
- [Aerich](https://github.com/tortoise/aerich) - Database migrations
