# Contributing to Finance AI Bot

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository
2. Clone your fork
3. Create a feature branch
4. Make your changes
5. Test your changes
6. Submit a pull request

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/finance-ai-bot.git
cd finance-ai-bot

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env
# Edit .env with your credentials

# Initialize database
aerich init -t config.database.TORTOISE_ORM
aerich init-db

# Run tests
python test_setup.py
```

## Code Style

- Follow PEP 8 style guide
- Use type hints where possible
- Add docstrings to functions and classes
- Keep functions small and focused
- Use meaningful variable names

### Example:

```python
async def process_transaction(user_id: int, amount: float, type: str) -> dict:
    """
    Process a financial transaction
    
    Args:
        user_id: User's telegram ID
        amount: Transaction amount
        type: Transaction type (income/expense)
        
    Returns:
        Dictionary with transaction details
    """
    # Implementation here
    pass
```

## Project Structure

```
finance-ai-bot/
├── app/
│   ├── handlers/      # Message and command handlers
│   ├── models/        # Database models
│   ├── services/      # Business logic
│   └── utils/         # Utility functions
├── config/            # Configuration files
├── migrations/        # Database migrations
├── main.py           # Entry point
└── tests/            # Test files
```

## Adding Features

### New Command

1. Create handler file in `app/handlers/`:

```python
# app/handlers/stats.py
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()

@router.message(Command("stats"))
async def cmd_stats(message: Message):
    """Show user statistics"""
    await message.answer("Your statistics...")
```

2. Register in `app/handlers/__init__.py`:

```python
from . import stats

def setup_routers():
    main_router = Router()
    main_router.include_router(stats.router)
    return main_router
```

### New Database Model

1. Create model in `app/models/`:

```python
# app/models/transaction.py
from tortoise import fields
from tortoise.models import Model

class Transaction(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="transactions")
    amount = fields.DecimalField(max_digits=10, decimal_places=2)
    type = fields.CharField(max_length=20)
    created_at = fields.DatetimeField(auto_now_add=True)
    
    class Meta:
        table = "transactions"
```

2. Export in `app/models/__init__.py`:

```python
from .transaction import Transaction

__all__ = ["User", "Transaction"]
```

3. Create migration:

```bash
aerich migrate --name add_transaction_model
aerich upgrade
```

### New Service

1. Create service in `app/services/`:

```python
# app/services/analytics_service.py
from typing import List, Dict
from app.models import Transaction

class AnalyticsService:
    """Service for financial analytics"""
    
    async def get_monthly_summary(self, user_id: int) -> Dict:
        """Get monthly summary for user"""
        # Implementation
        pass
```

2. Export in `app/services/__init__.py`:

```python
from .analytics_service import AnalyticsService

analytics_service = AnalyticsService()
```

## Testing

### Running Tests

```bash
# Run all tests
python test_setup.py

# Test specific functionality
python -c "from app.models import User; print('OK')"
```

### Writing Tests

Create test files in `tests/` directory:

```python
# tests/test_models.py
import pytest
from app.models import User

async def test_user_creation():
    """Test user model creation"""
    user = await User.create(
        telegram_id=123456,
        username="testuser"
    )
    assert user.telegram_id == 123456
```

## Documentation

- Update README.md if you add major features
- Update USAGE.md with usage examples
- Add docstrings to new functions
- Comment complex logic

## Commit Messages

Use clear, descriptive commit messages:

```
Add transaction history feature

- Create Transaction model
- Add /history command
- Display last 10 transactions
```

Format:
- Use present tense ("Add feature" not "Added feature")
- Keep first line under 50 characters
- Add detailed description if needed

## Pull Request Process

1. **Update your branch:**
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Run tests:**
   ```bash
   python test_setup.py
   ```

3. **Create pull request:**
   - Clear title describing the change
   - Description of what was changed and why
   - Reference any related issues

4. **Code review:**
   - Address review comments
   - Keep discussion focused and respectful

## Areas for Contribution

### Priority Features

- [ ] Full voice transcription integration
- [ ] Transaction history storage
- [ ] Budget tracking
- [ ] Financial reports
- [ ] Multi-language support
- [ ] Category management
- [ ] Export functionality

### Improvements

- [ ] Better error handling
- [ ] More comprehensive tests
- [ ] Performance optimization
- [ ] UI/UX improvements
- [ ] Documentation improvements

### Bug Fixes

Check [Issues](https://github.com/jaloliddin1006/finance-ai-bot/issues) for reported bugs.

## Code Review Checklist

Before submitting PR, ensure:

- [ ] Code follows project style
- [ ] All tests pass
- [ ] New features have tests
- [ ] Documentation is updated
- [ ] No sensitive data in code
- [ ] Commit messages are clear
- [ ] No unnecessary files included

## Getting Help

- Open an issue for questions
- Join discussions
- Check existing issues and PRs
- Read documentation

## License

By contributing, you agree that your contributions will be licensed under the project's license.

## Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Project documentation

Thank you for contributing! 🎉
