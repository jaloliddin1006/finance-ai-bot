# Architecture Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         Telegram User                            │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ Voice/Text Messages
                         │ Commands (/start, /help, /login)
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Telegram Bot API                            │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                       Finance AI Bot                             │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                     Bot (aiogram)                         │  │
│  │  • Message Dispatcher                                     │  │
│  │  • Update Handler                                         │  │
│  │  • Router System                                          │  │
│  └──────────────┬───────────────────────────┬────────────────┘  │
│                 │                           │                    │
│                 ▼                           ▼                    │
│  ┌──────────────────────────┐  ┌───────────────────────────┐   │
│  │       Handlers           │  │       Middleware          │   │
│  │  • Start Handler         │  │  • Logging                │   │
│  │  • Help Handler          │  │  • Error Handling         │   │
│  │  • Login Handler         │  │  • Rate Limiting          │   │
│  │  • Voice Handler         │  └───────────────────────────┘   │
│  │  • Text Handler          │                                   │
│  └──────────┬───────────────┘                                   │
│             │                                                    │
│             ▼                                                    │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                     Services Layer                        │  │
│  │  ┌──────────────────────────────────────────────────┐    │  │
│  │  │           Gemini Service                         │    │  │
│  │  │  • Audio Transcription                          │    │  │
│  │  │  • Text Processing                              │    │  │
│  │  │  • Financial Data Extraction                    │    │  │
│  │  │  • JSON Formatting                              │    │  │
│  │  └──────────────────────────────────────────────────┘    │  │
│  └──────────┬───────────────────────────────────────────────┘  │
│             │                                                    │
│             ▼                                                    │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                     Models Layer                          │  │
│  │  • User Model (Tortoise ORM)                             │  │
│  │  • Database Schema                                        │  │
│  └──────────┬───────────────────────────────────────────────┘  │
└─────────────┼────────────────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     PostgreSQL Database                          │
│  Tables:                                                         │
│  • users (id, telegram_id, username, first_name, last_name...)  │
│  • aerich migrations                                            │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                     Google Gemini API                            │
│  • Text Analysis                                                 │
│  • Content Generation                                            │
│  • Data Extraction                                               │
└─────────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. Main Application (`main.py`)

**Responsibilities:**
- Initialize bot and dispatcher
- Configure logging
- Setup database connection
- Register routers
- Start polling

**Flow:**
```python
main() → init_db() → setup_routers() → start_polling() → close_db()
```

### 2. Configuration Layer (`config/`)

#### `settings.py`
- Loads environment variables
- Validates configuration
- Provides application settings

#### `database.py`
- Tortoise ORM configuration
- Database initialization
- Connection management

### 3. Handlers Layer (`app/handlers/`)

#### `start.py` - Start Command
```
User sends /start
  → Get user info from Telegram
  → Create or update user in database
  → Send welcome message
```

#### `help.py` - Help Command
```
User sends /help
  → Send usage instructions
  → Display available commands
```

#### `login.py` - Login Command
```
User sends /login
  → Check user in database
  → Display user information
  → Show login status
```

#### `voice.py` - Voice/Text Handler
```
Voice Message:
  → Download audio file
  → Process with Gemini API
  → Transcribe to text
  → Extract financial data
  → Format as JSON
  → Send response to user

Text Message:
  → Extract text
  → Process with Gemini API
  → Extract financial data
  → Format as JSON
  → Send response to user
```

### 4. Services Layer (`app/services/`)

#### `gemini_service.py`

**Methods:**
- `transcribe_audio()`: Convert audio to text
- `extract_financial_data()`: Parse text for financial info
- `process_voice_message()`: Complete voice processing pipeline

**Data Flow:**
```
Audio/Text Input
  ↓
Gemini API Processing
  ↓
Text Analysis
  ↓
JSON Extraction
  ↓
Formatted Response
```

### 5. Models Layer (`app/models/`)

#### `user.py` - User Model

**Fields:**
- `id`: Primary key
- `telegram_id`: Unique Telegram user ID
- `username`: Telegram username
- `first_name`: User's first name
- `last_name`: User's last name
- `is_active`: Active status
- `created_at`: Registration timestamp
- `updated_at`: Last update timestamp

**Relations:**
- Can be extended with transactions, budgets, etc.

### 6. Utilities (`app/utils/`)

#### `logger.py`
- Consistent logging setup
- Formatted output
- Level configuration

## Data Flow

### User Registration Flow
```
1. User → /start
2. Bot → Extract user data (telegram_id, username, name)
3. Bot → Check database for existing user
4. Bot → Create or update user record
5. Bot → Send welcome message
```

### Voice Message Flow
```
1. User → Voice message
2. Bot → Download audio file
3. Bot → Send to Gemini API
4. Gemini → Transcribe audio
5. Gemini → Extract financial data
6. Bot → Format response (text + JSON)
7. Bot → Send to user
```

### Text Message Flow
```
1. User → Text message
2. Bot → Extract text
3. Bot → Send to Gemini API
4. Gemini → Analyze text
5. Gemini → Extract financial data
6. Bot → Format as JSON
7. Bot → Send to user
```

## Database Schema

### Users Table
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    telegram_id BIGINT UNIQUE NOT NULL,
    username VARCHAR(255),
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_users_telegram_id ON users(telegram_id);
```

## Configuration

### Environment Variables
```
BOT_TOKEN          → Telegram Bot API token
GEMINI_API_KEY     → Google Gemini API key
DB_HOST            → PostgreSQL host
DB_PORT            → PostgreSQL port
DB_USER            → Database username
DB_PASSWORD        → Database password
DB_NAME            → Database name
DEBUG              → Debug mode flag
```

## API Integrations

### 1. Telegram Bot API
- **Protocol**: HTTPS REST
- **Method**: Long Polling
- **Rate Limit**: 30 messages/second
- **Used For**: 
  - Receiving messages
  - Sending responses
  - Downloading files

### 2. Google Gemini API
- **Protocol**: HTTPS REST
- **Model**: gemini-pro
- **Rate Limit**: Depends on API key
- **Used For**:
  - Text generation
  - Content analysis
  - Data extraction

### 3. PostgreSQL
- **Protocol**: PostgreSQL protocol
- **Connection**: asyncpg driver
- **Pool Size**: Configurable
- **Used For**:
  - User storage
  - Transaction history (future)
  - Session management

## Security Considerations

### 1. Environment Variables
- All sensitive data in .env
- Never committed to git
- Validated on startup

### 2. Database Security
- Password-protected access
- Connection encryption (SSL)
- Prepared statements (SQL injection prevention)

### 3. Input Validation
- User input sanitized
- File size limits
- Rate limiting

### 4. API Security
- API keys secured
- Request signing
- Error handling (no sensitive data leaks)

## Scalability

### Current Capacity
- Single instance: ~100-1000 users
- Database: 1M+ users
- Response time: <2 seconds

### Scaling Options

**Horizontal Scaling:**
```
Load Balancer
    ↓
Bot Instance 1 ┐
Bot Instance 2 ├→ PostgreSQL Master
Bot Instance 3 ┘     ↓
                PostgreSQL Replica
```

**Caching Layer:**
```
Bot → Redis Cache → PostgreSQL
```

**Message Queue:**
```
Bot → RabbitMQ → Worker Processes → Gemini API
```

## Performance Optimization

### Current Implementation
- Async I/O (asyncio)
- Connection pooling (Tortoise ORM)
- Efficient queries

### Future Improvements
- Redis caching for frequent queries
- Message queue for long tasks
- CDN for media files
- Database query optimization

## Error Handling

### Levels
1. **Handler Level**: Try-catch in handlers
2. **Service Level**: API error handling
3. **Database Level**: Connection retry logic
4. **Global Level**: Unhandled exception handler

### User Feedback
```
Try:
    Process request
Except Specific Error:
    Log error
    Send user-friendly message
Except General Error:
    Log full traceback
    Send generic error message
```

## Monitoring & Logging

### Log Levels
- **INFO**: Normal operations
- **WARNING**: Unusual but handled
- **ERROR**: Failed operations
- **DEBUG**: Detailed information

### Logged Events
- User commands
- API calls
- Database operations
- Errors and exceptions

### Log Format
```
timestamp - logger_name - level - message
```

## Testing Strategy

### Unit Tests
- Model operations
- Service methods
- Utility functions

### Integration Tests
- Handler workflows
- Database operations
- API integrations

### Manual Tests
- Commands testing
- Voice message processing
- Error scenarios

## Deployment Architecture

### Development
```
Local Machine → PostgreSQL (local) → Gemini API
```

### Production
```
VPS/Cloud → PostgreSQL (RDS/managed) → Gemini API
    ↓
  Backup Service
```

### Docker
```
docker-compose
    ↓
  ├─ PostgreSQL Container
  └─ Bot Container
```

## Future Enhancements

### Planned Features
1. Transaction history storage
2. Budget tracking
3. Financial reports
4. Category management
5. Multi-language support
6. Export to Excel/CSV
7. Notifications
8. Recurring transactions

### Architecture Changes
1. Add Transaction model
2. Implement caching layer
3. Add message queue
4. Create analytics service
5. Add notification service

## Code Organization

### Separation of Concerns
- **Handlers**: User interaction
- **Services**: Business logic
- **Models**: Data structure
- **Config**: Settings
- **Utils**: Helper functions

### Dependency Flow
```
main.py
  ↓
handlers → services → models
  ↓           ↓
config    config
```

### Best Practices
- Single Responsibility Principle
- Dependency Injection
- Async/Await pattern
- Type hints
- Comprehensive docstrings

## Technology Stack Summary

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Bot Framework | aiogram 3.4.1 | Telegram bot handling |
| Database | PostgreSQL | Data persistence |
| ORM | Tortoise ORM 0.20.0 | Database abstraction |
| Migrations | Aerich 0.7.2 | Schema versioning |
| AI/ML | Google Gemini API | Text processing |
| Configuration | pydantic-settings | Settings management |
| Environment | python-dotenv | Environment variables |
| Containerization | Docker | Deployment |
| Orchestration | Docker Compose | Multi-container apps |

## Conclusion

This architecture provides:
- ✅ Scalable foundation
- ✅ Clean separation of concerns
- ✅ Easy maintainability
- ✅ Security best practices
- ✅ Extensibility for future features
- ✅ Comprehensive error handling
- ✅ Professional code organization
