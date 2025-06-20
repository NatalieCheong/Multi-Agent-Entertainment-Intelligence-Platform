#!/bin/bash
# Netflix MCP Application - Cursor IDE Setup Script
# This script sets up the development environment using uv package manager

set -e  # Exit on any error

echo "🎬 Netflix MCP Application - Cursor IDE Setup"
echo "=" * 60

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "❌ uv package manager not found!"
    echo "📦 Please install uv first:"
    echo "   curl -LsSf https://astral.sh/uv/install.sh | sh"
    echo "   # or"
    echo "   pip install uv"
    exit 1
fi

echo "✅ uv package manager found"

# Initialize the project if pyproject.toml doesn't exist
if [ ! -f "pyproject.toml" ]; then
    echo "📝 Initializing new Python project with uv..."
    uv init --name netflix-mcp-application
else
    echo "✅ pyproject.toml already exists"
fi

# Install dependencies
echo "📦 Installing dependencies with uv..."
uv sync

# Install development dependencies
echo "🛠️ Installing development dependencies..."
uv add --dev pytest pytest-asyncio pytest-cov black isort mypy ruff

# Create necessary directories
echo "📁 Creating project directories..."
mkdir -p logs
mkdir -p data
mkdir -p config
mkdir -p docs

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "🔑 Creating .env file template..."
    cat > .env << EOF
# Netflix MCP Application Environment Variables
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
NETFLIX_DATASET_PATH=data/netflix_titles.csv

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=logs/netflix_mcp_server.log

# MCP Server Configuration
MCP_SERVER_HOST=localhost
MCP_SERVER_PORT=8000
MCP_SERVER_MODE=development

# Multi-Agent Configuration
ENABLE_MULTI_AGENTS=true
ENABLE_GUARDRAILS=true

# Development Configuration
ENVIRONMENT=development
DEBUG=true
EOF
    echo "⚠️ Please update the .env file with your actual API keys"
else
    echo "✅ .env file already exists"
fi

# Create .gitignore if it doesn't exist
if [ ! -f ".gitignore" ]; then
    echo "📝 Creating .gitignore..."
    cat > .gitignore << EOF
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~

# Logs
logs/
*.log

# Data files
data/
*.csv
*.json
*.parquet

# API Keys and secrets
.env
.env.local
.env.production
.env.staging
config/secrets.json

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# uv
.uv/
uv.lock

# Pytest
.pytest_cache/
.coverage
htmlcov/

# MyPy
.mypy_cache/
.dmypy.json
dmypy.json

# Ruff
.ruff_cache/

# Claude Desktop
claude_desktop_config.json.backup
EOF
else
    echo "✅ .gitignore already exists"
fi

# Create README.md if it doesn't exist
if [ ! -f "README.md" ]; then
    echo "📚 Creating README.md..."
    cat > README.md << EOF
# Netflix MCP Application

A comprehensive Netflix Multi-Agent Business Intelligence MCP Server with AI Agents and Content Safety Guardrails.

## Features

- 🎬 **Business Intelligence**: Real Netflix dataset analysis with advanced queries
- 🤖 **Multi-Agent System**: 5 specialized AI agents for different Netflix domains
- 🔒 **Content Safety**: Advanced guardrail system for content filtering
- 📊 **Claude Desktop Integration**: Full MCP protocol support
- 🛠️ **Professional Setup**: Modern Python development with uv package manager

## Quick Start

### Prerequisites

- Python 3.9+
- [uv package manager](https://github.com/astral-sh/uv)
- OpenAI API key

### Installation

1. Clone the repository:
\`\`\`bash
git clone https://github.com/yourusername/AI-Agents-with-MCP-Server-for-Netflix-TV-and-Movie-Shows.git
cd AI-Agents-with-MCP-Server-for-Netflix-TV-and-Movie-Shows
\`\`\`

2. Run the setup script:
\`\`\`bash
chmod +x setup.sh
./setup.sh
\`\`\`

3. Update your API keys in \`.env\`:
\`\`\`bash
OPENAI_API_KEY=your_actual_openai_api_key_here
\`\`\`

4. Add Netflix dataset to \`data/netflix_titles.csv\`

### Usage

#### Running the MCP Server

\`\`\`bash
# Start the MCP server
uv run python mcp_server/mcp_server.py

# Or use the installed script
uv run netflix-mcp-server
\`\`\`

#### Claude Desktop Integration

1. Add the configuration to Claude Desktop:
\`\`\`json
{
  "mcpServers": {
    "netflix-business-intelligence": {
      "command": "uv",
      "args": ["run", "python", "mcp_server/mcp_server.py"],
      "cwd": "/path/to/your/project",
      "env": {
        "OPENAI_API_KEY": "your_openai_api_key_here"
      }
    }
  }
}
\`\`\`

2. Restart Claude Desktop

#### Testing

\`\`\`bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov

# Test specific modules
uv run python -m pytest test/
\`\`\`

#### Development

\`\`\`bash
# Format code
uv run black .
uv run isort .

# Type checking
uv run mypy .

# Linting
uv run ruff check .
\`\`\`

## Project Structure

\`\`\`
├── mcp_server/          # MCP server implementation
├── mcp_client/          # MCP client for testing
├── mcp_application/     # Complete application
├── agents/              # Multi-agent system
├── guardrail/           # Content safety guardrails
├── test/                # Test files
├── logs/                # Log files
├── data/                # Dataset storage
├── config/              # Configuration files
└── docs/                # Documentation
\`\`\`

## Available Tools

### Business Intelligence
- Korean content analysis
- Genre popularity trends
- International vs US content trends
- Dataset statistics and insights

### Multi-Agent System
- Content Discovery Agent
- Analytics Specialist Agent
- Recommendation Engine Agent
- Customer Support Agent
- Content Strategy Agent

### Safety Features
- Content safety filtering
- Quality assessment
- Business logic validation
- Bias detection

## Environment Variables

See \`.env\` file for all configuration options.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## License

MIT License - see LICENSE file for details.
EOF
else
    echo "✅ README.md already exists"
fi

# Create a simple test to verify everything works
echo "🧪 Creating basic test..."
mkdir -p test
cat > test/test_basic.py << EOF
"""Basic tests for Netflix MCP Application"""
import pytest
import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

def test_imports():
    """Test that main modules can be imported"""
    try:
        from mcp_server import mcp_server
        from agents import multi_agents_fastmcp
        from guardrail import guardrail_fastmcp
        assert True
    except ImportError as e:
        pytest.fail(f"Import failed: {e}")

def test_sample_business_logic():
    """Test basic business logic functionality"""
    from mcp_server.mcp_server import enhanced_business_query_logic
    
    result = enhanced_business_query_logic("What percentage of Netflix content is Korean?")
    assert result["status"] == "success"
    assert "business_intelligence" in result

if __name__ == "__main__":
    pytest.main([__file__])
EOF

# Run a quick test
echo "🧪 Running basic tests..."
if uv run python -c "print('✅ Python environment working')"; then
    echo "✅ Python environment verified"
else
    echo "❌ Python environment test failed"
    exit 1
fi

# Final instructions
echo ""
echo "🎉 Setup completed successfully!"
echo "=" * 60
echo "📋 Next steps:"
echo ""
echo "1. 🔑 Update your API keys in .env file:"
echo "   nano .env"
echo ""
echo "2. 📊 Add Netflix dataset to data/netflix_titles.csv"
echo ""
echo "3. 🧪 Test the installation:"
echo "   uv run python -m pytest test/"
echo ""
echo "4. 🚀 Start the MCP server:"
echo "   uv run python mcp_server/mcp_server.py"
echo ""
echo "5. 🔗 Configure Claude Desktop with the generated config"
echo ""
echo "🎬 Your Netflix MCP Application is ready for development!"
echo "📚 Check README.md for detailed usage instructions"
echo "=" * 60
