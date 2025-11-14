# Usage Guide - Finance AI Bot

## Quick Start

### 1. Installation

```bash
# Clone repository
git clone https://github.com/jaloliddin1006/finance-ai-bot.git
cd finance-ai-bot

# Run setup script
chmod +x setup.sh
./setup.sh
```

Or manually:

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your credentials

# Initialize database
aerich init -t config.database.TORTOISE_ORM
aerich init-db
```

### 2. Configuration

Edit `.env` file with your credentials:

```env
# Telegram Bot Token (get from @BotFather)
BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz

# Database
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=your_secure_password
DB_NAME=finance_bot

# Gemini API Key (get from https://ai.google.dev/)
GEMINI_API_KEY=AIzaSyABC123DEF456GHI789JKL

# Debug mode
DEBUG=True
```

### 3. Run the Bot

```bash
# Activate virtual environment
source venv/bin/activate

# Run bot
python main.py
```

### 4. Using Docker

```bash
# Build and run with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f bot

# Stop
docker-compose down
```

## Bot Commands

### /start
Start the bot and register in database.

**Example:**
```
User: /start
Bot: 👋 Salom, John!
     Men Finance AI Bot'man...
```

### /help
Get help and usage instructions.

**Example:**
```
User: /help
Bot: 📚 Finance AI Bot - Yordam
     🎤 Ovozli habar yuborish...
```

### /login
Check your login status and user information.

**Example:**
```
User: /login
Bot: ✅ Siz tizimga kirdingiz!
     👤 Foydalanuvchi: John
     🆔 Telegram ID: 123456789
```

## Voice Messages

Send a voice message describing a financial transaction:

**Example (Uzbek):**
```
Voice: "Men bugun 50000 so'm oziq-ovqatga sarfladim"

Bot Response:
📝 Transkripsiya:
Men bugun 50000 so'm oziq-ovqatga sarfladim

💰 Moliyaviy ma'lumotlar (JSON):
{
  "type": "expense",
  "amount": 50000,
  "category": "food",
  "description": "oziq-ovqat xarajati",
  "date": "2024-01-15"
}

📊 Tafsilotlar:
• Turi: expense
• Miqdor: 50000
• Kategoriya: food
• Tavsif: oziq-ovqat xarajati
• Sana: 2024-01-15
```

**Example (English):**
```
Voice: "I spent 100 dollars on groceries today"

Bot Response:
📝 Transkripsiya:
I spent 100 dollars on groceries today

💰 Moliyaviy ma'lumotlar (JSON):
{
  "type": "expense",
  "amount": 100,
  "category": "groceries",
  "description": "grocery shopping",
  "date": "2024-01-15"
}
```

## Text Messages

You can also send text messages instead of voice:

**Examples:**

```
User: Men 200000 so'm ish haqqi oldim
Bot: [Returns JSON with income data]

User: 15000 so'm transport
Bot: [Returns JSON with expense data]

User: I received my salary of 1000 USD
Bot: [Returns JSON with income data]
```

## JSON Format

All financial data is returned in this format:

```json
{
  "type": "income/expense",
  "amount": numeric_value,
  "category": "category_name",
  "description": "description_text",
  "date": "YYYY-MM-DD"
}
```

### Fields:

- **type**: Either "income" or "expense"
- **amount**: Numeric value of the transaction
- **category**: Category of the transaction (food, transport, salary, etc.)
- **description**: Brief description of the transaction
- **date**: Date of the transaction or "today"

## Database Management

### View Database

```bash
# Connect to PostgreSQL
psql -U postgres -d finance_bot

# View users
SELECT * FROM users;
```

### Migrations

```bash
# Create a new migration
aerich migrate --name add_new_field

# Apply migrations
aerich upgrade

# Rollback last migration
aerich downgrade
```

## Troubleshooting

### Bot Not Starting

**Check environment variables:**
```bash
# Verify .env file exists
cat .env

# Test configuration
python3 -c "from config import settings; print(settings.bot_token)"
```

**Check database connection:**
```bash
# Test PostgreSQL connection
psql -U postgres -d finance_bot -c "SELECT 1"
```

### Voice Messages Not Working

The current implementation uses a placeholder for audio transcription. For full voice transcription:

1. Use Google Speech-to-Text API
2. Or use Whisper API
3. Or integrate with Gemini Pro Vision

### Database Errors

```bash
# Reset migrations
rm -rf migrations/
aerich init -t config.database.TORTOISE_ORM
aerich init-db

# Or recreate database
dropdb finance_bot
createdb finance_bot
python main.py
```

### Import Errors

```bash
# Reinstall dependencies
pip install --force-reinstall -r requirements.txt

# Or create fresh virtual environment
deactivate
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Development

### Adding New Commands

1. Create handler in `app/handlers/`:

```python
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()

@router.message(Command("mycommand"))
async def cmd_mycommand(message: Message):
    await message.answer("Hello!")
```

2. Register in `app/handlers/__init__.py`:

```python
from . import mycommand

def setup_routers():
    main_router = Router()
    main_router.include_router(mycommand.router)
    return main_router
```

### Adding Database Models

1. Create model in `app/models/`:

```python
from tortoise import fields
from tortoise.models import Model

class Transaction(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.User")
    amount = fields.DecimalField(max_digits=10, decimal_places=2)
    type = fields.CharField(max_length=50)
```

2. Create migration:

```bash
aerich migrate --name add_transaction_model
aerich upgrade
```

## Best Practices

1. **Environment Variables**: Never commit `.env` file
2. **Error Handling**: Always wrap handlers in try-except
3. **Logging**: Use logger for debugging
4. **Database**: Always use ORM methods, avoid raw SQL
5. **Security**: Validate user input before processing

## Resources

- [aiogram Documentation](https://docs.aiogram.dev/)
- [Tortoise ORM Docs](https://tortoise.github.io/)
- [Google Gemini API](https://ai.google.dev/)
- [PostgreSQL Docs](https://www.postgresql.org/docs/)

## Support

For issues or questions:
1. Check this guide
2. Review logs: `tail -f bot.log`
3. Open GitHub issue
4. Contact maintainer
