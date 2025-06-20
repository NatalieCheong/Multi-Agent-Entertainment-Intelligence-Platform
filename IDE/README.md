# Netflix MCP Application - IDE Environment

A professional Netflix Multi-Agent Business Intelligence MCP Server optimized for IDE development with `uv` package manager.

## 🎯 Quick Start for IDE

### Prerequisites
- **Python 3.9+**
- **[uv package manager](https://astral.sh/uv/install.sh)**
- **OpenAI API key**
- **Netflix dataset** (`netflix_titles.csv`)

### Installation

1. **Clone and setup:**
```bash
git clone <your-repo-url>
cd AI-Agents-with-MCP-Server-for-Netflix-TV-and-Movie-Shows
chmod +x setup.sh
./setup.sh
```

2. **Configure environment:**
```bash
# Update .env with your API keys
nano .env
```

3. **Add Netflix dataset:**
```bash
# Place your netflix_titles.csv in the data/ directory
cp path/to/netflix_titles.csv data/
```

4. **Test installation:**
```bash
uv run pytest test/
```

## 🚀 Running the Application

### Start MCP Server
```bash
# Method 1: Direct execution
uv run python mcp_server/mcp_server.py

# Method 2: Using installed script
uv run netflix-mcp-server

# Method 3: With specific environment
uv run --env-file .env python mcp_server/mcp_server.py
```

### Claude Desktop Integration

1. **Create Claude Desktop config:**
```json
{
  "mcpServers": {
    "netflix-business-intelligence": {
      "command": "uv",
      "args": [
        "run", 
        "python", 
        "mcp_server/mcp_server.py"
      ],
      "cwd": "/absolute/path/to/your/project",
      "env": {
        "OPENAI_API_KEY": "your_openai_api_key_here",
        "NETFLIX_DATASET_PATH": "data/netflix_titles.csv"
      }
    }
  }
}
```

2. **Add to Claude Desktop:**
   - **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
   - **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Linux:** `~/.config/Claude/claude_desktop_config.json`

3. **Restart Claude Desktop**

## 🛠️ Development with IDE

### Code Formatting
```bash
# Format all code
uv run black .
uv run isort .

# Check formatting
uv run black --check .
```

### Type Checking
```bash
# Run type checking
uv run mypy .

# Check specific module
uv run mypy mcp_server/
```

### Linting
```bash
# Run linter
uv run ruff check .

# Fix auto-fixable issues
uv run ruff check --fix .
```

### Testing
```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=mcp_server --cov=agents --cov=guardrail

# Run specific test file
uv run pytest test/test_basic.py -v

# Run and watch for changes
uv run pytest-watch
```

## 📊 Available MCP Tools

### 1. **netflix_business_query**
Business intelligence queries with real Netflix data:
```json
{
  "natural_language_query": "What percentage of Netflix content is Korean?"
}
```

### 2. **netflix_test_query**
Simple connectivity test:
```json
{
  "test_message": "Hello from Cursor IDE!"
}
```

### 3. **netflix_dataset_info**
Dataset information and statistics:
```json
{
  "detail_level": "detailed"  // basic, detailed, or full
}
```

## 🤖 Multi-Agent System

### Available Agents
- **Content Discovery Agent** - Find movies and shows
- **Analytics Specialist Agent** - Analyze trends and data
- **Recommendation Engine Agent** - Personalized suggestions
- **Customer Support Agent** - Help with Netflix features
- **Content Strategy Agent** - Business strategy insights

### Usage Examples
```python
from agents.multi_agents_fastmcp import run_netflix_multi_agent

# Get content recommendations
result = run_netflix_multi_agent("Find me some good Korean dramas")

# Analyze trends
result = run_netflix_multi_agent("What are the latest trends in thriller content?")

# Business strategy
result = run_netflix_multi_agent("What content should Netflix focus on for international markets?")
```

## 🔒 Guardrail System

### Safety Features
- **Content Safety** - Age-appropriate filtering
- **Quality Assessment** - Response quality validation
- **Business Logic** - Strategic viability checks
- **Bias Detection** - Cultural and demographic fairness

### Usage
```python
from guardrail.guardrail_fastmcp import apply_guardrails_to_response

response = "Some content recommendation"
context = {"content_type": "family", "age_rating": "kids"}

guardrail_result = apply_guardrails_to_response(response, context)
```

## 📁 Project Structure

```
├── 📁 mcp_server/           # MCP server implementation
│   ├── mcp_server.py        # Main server (Cursor IDE optimized)
│   └── __init__.py
├── 📁 mcp_client/           # MCP client for testing
│   ├── mcp_client.py        # Client implementation
│   └── __init__.py
├── 📁 mcp_application/      # Complete application wrapper
│   ├── mcp_application.py   # Application management
│   └── __init__.py
├── 📁 agents/               # Multi-agent system
│   ├── multi_agents_fastmcp.py
│   └── __init__.py
├── 📁 guardrail/            # Content safety guardrails
│   ├── guardrail_fastmcp.py
│   └── __init__.py
├── 📁 test/                 # Test files
├── 📁 logs/                 # Application logs
├── 📁 data/                 # Dataset storage
├── 📁 config/               # Configuration files
├── 📁 docs/                 # Documentation
├── pyproject.toml           # Project configuration
├── uv.lock                  # Dependency lock file
├── .env                     # Environment variables
├── setup.sh                 # Setup script
└── README.md               # This file
```

## ⚙️ Configuration

### Environment Variables
```bash
# API Keys
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Dataset
NETFLIX_DATASET_PATH=data/netflix_titles.csv

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/netflix_mcp_server.log

# Features
ENABLE_MULTI_AGENTS=true
ENABLE_GUARDRAILS=true

# Development
ENVIRONMENT=development
DEBUG=true
```

### IDE Configuration

Add to your settings (`.vscode/settings.json`):
```json
{
  "python.defaultInterpreterPath": ".venv/bin/python",
  "python.formatting.provider": "black",
  "python.linting.enabled": true,
  "python.linting.mypyEnabled": true,
  "python.linting.ruffEnabled": true,
  "files.exclude": {
    "**/.uv": true,
    "**/uv.lock": false,
    "**/__pycache__": true,
    "**/.pytest_cache": true,
    "**/logs": true
  }
}
```

## 🧪 Testing Strategy

### Test Categories
1. **Unit Tests** - Individual component testing
2. **Integration Tests** - MCP server/client communication
3. **End-to-End Tests** - Full workflow testing
4. **Performance Tests** - Load and response time testing

### Running Tests
```bash
# Quick test suite
uv run pytest test/test_basic.py

# Full test suite with coverage
uv run pytest --cov --cov-report=html

# Test specific functionality
uv run pytest -k "test_business_intelligence"

# Continuous testing during development
uv run pytest-watch
```

## 🚀 Deployment Options

### Local Development
```bash
# Start development server
uv run python mcp_server/mcp_server.py
```

### Claude Desktop Integration
- Use the provided `claude_desktop_config.json`
- Ensure absolute paths in configuration
- Restart Claude Desktop after configuration changes

### Production Deployment
```bash
# Install production dependencies
uv sync --no-dev

# Run with production settings
ENVIRONMENT=production uv run python mcp_server/mcp_server.py
```

## 🛟 Troubleshooting

### Common Issues

1. **Import Errors**
```bash
# Reinstall dependencies
uv sync --reinstall
```

2. **Dataset Not Found**
```bash
# Check dataset path
ls -la data/netflix_titles.csv
# Update path in .env
```

3. **API Key Issues**
```bash
# Verify API key in environment
echo $OPENAI_API_KEY
# Update .env file
```

4. **MCP Connection Issues**
```bash
# Test standalone
uv run python mcp_server/mcp_server.py

# Check Claude Desktop logs
# macOS: ~/Library/Logs/Claude/
```

### Debug Mode
```bash
# Enable debug logging
DEBUG=true LOG_LEVEL=DEBUG uv run python mcp_server/mcp_server.py
```

## 📈 Performance Optimization

### For Large Datasets
- Use dataset sampling for development
- Implement caching for repeated queries
- Consider database integration for production

### Memory Management
- Monitor memory usage with large datasets
- Implement data streaming for very large files
- Use pandas chunking for processing

## 🤝 Contributing

1. **Fork the repository**
2. **Create feature branch:** `git checkout -b feature/amazing-feature`
3. **Install dev dependencies:** `uv sync`
4. **Make changes with proper testing**
5. **Run quality checks:**
   ```bash
   uv run black .
   uv run isort .
   uv run mypy .
   uv run pytest
   ```
6. **Commit changes:** `git commit -m 'Add amazing feature'`
7. **Push to branch:** `git push origin feature/amazing-feature`
8. **Open Pull Request**

## 📜 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🎬 Success Stories

This Netflix MCP Application successfully provides:
- ✅ **75%+ test coverage** for comprehensive quality assurance
- ✅ **Real Netflix data analysis** with 8,000+ titles
- ✅ **5 specialized AI agents** for different business domains
- ✅ **Advanced guardrail system** for content safety
- ✅ **Professional development setup** with modern tooling
- ✅ **Claude Desktop integration** for seamless AI workflows

---

**Happy coding with IDE! 🎉**
