#!/bin/bash

# Virtual environment activation script
# Usage: source activate_env.sh

echo "🚀 Activating virtual environment..."

# Change to project directory
cd "$(dirname "$0")"

# Activate virtual environment
source .venv/bin/activate

echo "✅ Virtual environment activated!"
echo "Python: $(which python)"
echo ""
echo "📝 Next steps:"
echo "   1. Make sure .env is configured:"
echo "      OPENAI_API_KEY=your-key"
echo "      OPENAI_BASE_URL=your-url"
echo ""
echo "   2. Start the assistant:"
echo "      python main.py"
echo ""
echo "   3. Or use uv run:"
echo "      uv run python main.py"
echo ""

