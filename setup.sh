#!/bin/bash

# Finance AI Bot Setup Script

echo "🤖 Finance AI Bot Setup"
echo "======================="

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python version: $python_version"

# Create virtual environment
echo ""
echo "📦 Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo ""
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Copy environment file
if [ ! -f .env ]; then
    echo ""
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your credentials"
else
    echo ""
    echo "✓ .env file already exists"
fi

# Initialize database migrations
echo ""
echo "🔄 Initializing database migrations..."
aerich init -t config.database.TORTOISE_ORM
aerich init-db

echo ""
echo "✅ Setup completed!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your credentials"
echo "2. Ensure PostgreSQL is running"
echo "3. Run: source venv/bin/activate"
echo "4. Run: python main.py"
