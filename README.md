# 🎬 Netflix Multi-Agent MCP Platform

**A Professional Multi-Agent Business Intelligence MCP Server with AI Orchestration and Content Safety Guardrails**

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![MCP Protocol](https://img.shields.io/badge/MCP-Protocol-green.svg)](https://github.com/modelcontextprotocol)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![uv](https://img.shields.io/badge/uv-package%20manager-orange.svg)](https://github.com/astral-sh/uv)

## 🌟 Overview

This project represents the next generation of AI-powered content analysis platforms, featuring a sophisticated **Multi-Agent Architecture** integrated with the **Model Context Protocol (MCP)** for seamless AI service orchestration. Built specifically for entertainment industry analysis, it demonstrates advanced concepts in distributed AI systems and protocol standardization.

### 🎯 Key Innovation Areas

- **Agent Architecture & Orchestration**: Multi-agent system with specialized Netflix domain experts
- **MCP Ecosystem Building**: Standards-compliant protocol implementation for AI service integration
- **Content Safety Guardrails**: Advanced AI safety and quality assurance systems
- **Business Intelligence**: Real-world entertainment industry data analysis capabilities

## 🚀 Features

### 🤖 Multi-Agent System
- **5 Specialized AI Agents** for different Netflix business domains
- **Intelligent Agent Orchestration** with dynamic workflow routing
- **Context-Aware Communication** between agents using MCP protocol
- **Scalable Agent Architecture** designed for enterprise deployment

### 🔗 MCP Protocol Integration
- **Standards-Compliant Implementation** of Model Context Protocol
- **Claude Desktop Integration** with full MCP support
- **Tool-based Architecture** with extensible capabilities
- **Real-time Communication** between AI models and external systems

### 🔒 Advanced Guardrails
- **Content Safety Filtering** with multi-dimensional analysis
- **Quality Assurance** for AI-generated responses
- **Business Logic Validation** for strategic recommendations
- **Bias Detection** and cultural sensitivity assessment

### 📊 Business Intelligence
- **Real Netflix Dataset Analysis** with 8,000+ titles
- **International Content Trends** and market insights
- **Genre Performance Analytics** and recommendation systems
- **Competitive Intelligence** and market positioning analysis

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                Netflix MCP Platform Architecture            │
├─────────────────────────────────────────────────────────────┤
│  Claude Desktop  │  External Clients  │  API Integrations   │
├─────────────────────────────────────────────────────────────┤
│                    MCP Protocol Layer                       │
├─────────────────────────────────────────────────────────────┤
│ Content Discovery │ Analytics │ Recommendations │ Support   │
│     Agent         │ Specialist│     Engine      │ Agent     │
├─────────────────────────────────────────────────────────────┤
│              Multi-Agent Orchestration Hub                  │
├─────────────────────────────────────────────────────────────┤
│    Safety Guardrails    │    Business Logic Validation     │
├─────────────────────────────────────────────────────────────┤
│  Netflix Dataset  │  TMDB Integration  │  Sample Data      │
└─────────────────────────────────────────────────────────────┘
```

## 🛠️ Technical Stack

### Core Technologies
- **Python 3.9+** with modern async/await patterns
- **MCP Protocol** for standardized AI service communication
- **OpenAI GPT-4** for advanced language model capabilities
- **uv Package Manager** for professional dependency management
- **Pandas & NumPy** for high-performance data analysis

### AI & Machine Learning
- **Multi-Agent Framework** with specialized domain agents
- **LangChain Integration** for complex workflow orchestration
- **Content Safety AI** for guardrail implementation
- **Business Intelligence AI** for strategic analysis

### Development & Deployment
- **Professional IDE Setup** optimized for Cursor/VS Code
- **Claude Desktop Integration** with MCP protocol
- **Comprehensive Testing** with pytest and coverage
- **Modern Python Tooling** (Black, isort, mypy, ruff)

## 📦 Quick Start

### Prerequisites

- **Python 3.9+** installed on your system
- **[uv package manager](https://github.com/astral-sh/uv)** for dependency management
- **OpenAI API key** for AI functionality
- **Git** for version control

### 🚀 Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/NatalieCheong/Multi-Agents-with-MCP-Server-Analyze-Netflix-TV-and-Movie-Shows.git
   cd Multi-Agents-with-MCP-Server-Analyze-Netflix-TV-and-Movie-Shows/IDE
   ```

2. **Run Setup Script**
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

3. **Configure Environment**
   ```bash
   # Update .env file with your API keys
   nano .env
   ```
   
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ANTHROPIC_API_KEY=your_anthropic_api_key_here
   NETFLIX_DATASET_PATH=data/netflix_titles.csv
   TMDB_API_KEY=your_tmdb_api_key_here  # Optional
   ```

4. **Add Data Source** (Choose one option)

   **Option A: Netflix Dataset (Recommended)**
   ```bash
   # Download netflix_titles.csv and place in data/ directory
   wget -O data/netflix_titles.csv "your_netflix_dataset_url"
   ```

   **Option B: TMDB API Integration**
   ```bash
   # Get API key from https://www.themoviedb.org/settings/api
   # Add TMDB_API_KEY to your .env file
   ```

   **Option C: Sample Data**
   ```bash
   # System will automatically create sample data if no other source is available
   ```

### 🎮 Running the Platform

#### Start MCP Server
```bash
# Method 1: Direct execution
uv run python mcp_server/mcp_server.py

# Method 2: Using installed script
uv run netflix-mcp-server

# Method 3: With specific environment
uv run --env-file .env python mcp_server/mcp_server.py
```

#### Claude Desktop Integration

1. **Configure Claude Desktop** (`claude_desktop_config.json`):
   ```json
   {
     "mcpServers": {
       "netflix-business-intelligence": {
         "command": "uv",
         "args": ["run", "python", "mcp_server/mcp_server.py"],
         "cwd": "/absolute/path/to/your/project",
         "env": {
           "OPENAI_API_KEY": "your_openai_api_key_here",
           "NETFLIX_DATASET_PATH": "data/netflix_titles.csv"
         }
       }
     }
   }
   ```

2. **Configuration File Locations**:
   - **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
   - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Linux**: `~/.config/Claude/claude_desktop_config.json`

3. **Restart Claude Desktop**

## 🎯 Usage Examples

### Business Intelligence Queries
```
What percentage of Netflix content is Korean?
Show me the trend of international vs US content
What are the most popular genres globally?
Analyze thriller content performance in Asian markets
```

### Multi-Agent Interactions
```
Find action movies suitable for teenagers
Recommend family-friendly international content
Analyze competitor strategy for streaming market
Predict success probability for Korean drama series
```

### Content Safety Validation
```
Evaluate content appropriateness for kids
Check cultural sensitivity for global audience
Assess business viability of investment strategy
Analyze potential bias in recommendation algorithm
```

## 🏢 Business Applications

### Entertainment Industry
- **Content Strategy Planning** with data-driven insights
- **Market Analysis** for international expansion
- **Audience Segmentation** and preference analysis
- **Competitive Intelligence** and positioning

### AI Platform Development
- **Multi-Agent System** architecture patterns
- **MCP Protocol** implementation and standards
- **AI Safety Guardrails** for content platforms
- **Distributed AI Services** orchestration

### Enterprise Solutions
- **Business Intelligence** with AI-powered analysis
- **Content Moderation** at scale
- **Strategic Decision Support** systems
- **Risk Assessment** and compliance validation

## 🧪 Testing & Development

### Run Tests
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

### Code Quality
```bash
# Format code
uv run black .
uv run isort .

# Type checking
uv run mypy .

# Linting
uv run ruff check .

# Fix auto-fixable issues
uv run ruff check --fix .
```

### Development Server
```bash
# Enable debug mode
DEBUG=true LOG_LEVEL=DEBUG uv run python mcp_server/mcp_server.py

# Test multi-agent system
uv run python agents/multi_agents.py

# Test guardrail system
uv run python guardrail/guardrail.py
```

## 📊 Available MCP Tools

| Tool Name | Description | Use Case |
|-----------|-------------|----------|
| `netflix_business_query` | Advanced BI queries with multi-agent analysis | Market research, trend analysis |
| `netflix_test_query` | Simple connectivity and functionality test | Development and debugging |
| `netflix_dataset_info` | Comprehensive dataset statistics | Data validation and exploration |
| `netflix_content_recommendations` | AI-powered content suggestions | Personalization and user engagement |
| `netflix_search_content` | Multi-agent content discovery | Content search and filtering |
| `netflix_analytics_insights` | Advanced analytics and metrics | Performance monitoring and insights |

## 🤖 AI Agents Specifications

### 1. Content Discovery Agent
- **Purpose**: Movie and TV show search and discovery
- **Capabilities**: Genre filtering, cast/director search, content metadata analysis
- **Use Cases**: Content recommendation, catalog exploration, user query resolution

### 2. Analytics Specialist Agent
- **Purpose**: Data analysis and business intelligence
- **Capabilities**: Trend analysis, performance metrics, competitive benchmarking
- **Use Cases**: Market research, strategy planning, ROI analysis

### 3. Recommendation Engine Agent
- **Purpose**: Personalized content suggestions
- **Capabilities**: User preference modeling, collaborative filtering, content matching
- **Use Cases**: User engagement, personalization, retention optimization

### 4. Customer Support Agent
- **Purpose**: User assistance and platform guidance
- **Capabilities**: FAQ handling, troubleshooting, feature explanation
- **Use Cases**: Customer service, user onboarding, issue resolution

### 5. Content Strategy Agent
- **Purpose**: Business strategy and content planning
- **Capabilities**: Market analysis, investment recommendations, strategic insights
- **Use Cases**: Content acquisition, market expansion, competitive positioning

## 🔒 Safety & Compliance

### Content Safety Features
- **Age Appropriateness Filtering** with automatic content rating
- **Cultural Sensitivity Analysis** for global content deployment
- **Bias Detection** across demographic and geographic dimensions
- **Quality Assurance** with automated response validation

### Business Compliance
- **Strategic Viability Assessment** for investment recommendations
- **Risk Analysis** for market expansion strategies
- **Regulatory Compliance** checking for international markets
- **Ethical AI Guidelines** implementation and monitoring

## 📁 Project Structure

```
├── 📁 mcp_server/           # MCP server implementation
│   ├── mcp_server.py        # Main server with enhanced BI logic
│   └── __init__.py
├── 📁 mcp_client/           # MCP client for testing and development
│   ├── mcp_client.py        # Client implementation with mock support
│   └── __init__.py
├── 📁 mcp_application/      # Complete application wrapper
│   ├── mcp_application.py   # Application management and orchestration
│   └── __init__.py
├── 📁 agents/               # Multi-agent system implementation
│   ├── multi_agents.py      # Agent definitions and orchestration logic
│   └── __init__.py
├── 📁 guardrail/            # Content safety and quality guardrails
│   ├── guardrail.py         # Guardrail system with AI judges
│   └── __init__.py
├── 📁 test/                 # Comprehensive test suite
│   ├── test_basic.py        # Basic functionality tests
│   └── __init__.py
├── 📁 logs/                 # Application logs and monitoring
├── 📁 data/                 # Dataset storage (Netflix CSV/TMDB)
├── 📁 config/               # Configuration files
├── 📁 docs/                 # Documentation and guides
├── pyproject.toml           # Modern Python project configuration
├── uv.lock                  # Dependency lock file for reproducibility
├── .env                     # Environment variables (API keys, config)
├── setup.sh                 # Professional setup script
├── README.md               # This comprehensive guide
└── claude_desktop_config.json # Claude Desktop integration config
```

## ⚙️ Configuration Options

### Environment Variables
```bash
# API Configuration
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
TMDB_API_KEY=your_tmdb_api_key_here

# Data Source Configuration
NETFLIX_DATASET_PATH=data/netflix_titles.csv
PREFERRED_DATA_SOURCE=netflix_csv  # netflix_csv, tmdb_api, sample_data

# Logging Configuration
LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR
LOG_FILE=logs/netflix_mcp_server.log

# Feature Flags
ENABLE_MULTI_AGENTS=true
ENABLE_GUARDRAILS=true
ENABLE_ANALYTICS=true

# Development Configuration
ENVIRONMENT=development  # development, staging, production
DEBUG=true
MCP_SERVER_PORT=8000
```

### Advanced Configuration
```python
# config/settings.py
GUARDRAIL_THRESHOLDS = {
    "content_safety": 0.8,
    "quality_assessment": 0.85,
    "bias_detection": 0.7,
    "business_viability": 0.75
}

AGENT_CONFIGURATION = {
    "max_concurrent_agents": 5,
    "response_timeout": 30,
    "retry_attempts": 3,
    "context_window": 4000
}
```

## 🚀 Deployment Options

### Development Deployment
```bash
# Local development server
uv run python mcp_server/mcp_server.py

# With hot reload
uvicorn mcp_server.mcp_server:app --reload --port 8000
```

### Production Deployment
```bash
# Install production dependencies only
uv sync --no-dev

# Run with production settings
ENVIRONMENT=production uv run python mcp_server/mcp_server.py

# With process manager
pm2 start ecosystem.config.js
```

### Docker Deployment
```dockerfile
FROM python:3.11-slim

# Install uv
RUN pip install uv

# Copy project files
COPY . /app
WORKDIR /app

# Install dependencies
RUN uv sync --no-dev

# Expose port
EXPOSE 8000

# Run server
CMD ["uv", "run", "python", "mcp_server/mcp_server.py"]
```

## 🛟 Troubleshooting

### Common Issues and Solutions

**1. MCP Connection Issues**
```bash
# Check if server is running
uv run python mcp_server/mcp_server.py

# Verify Claude Desktop configuration
cat ~/.config/Claude/claude_desktop_config.json

# Check logs for errors
tail -f logs/netflix_mcp_server.log
```

**2. Dataset Loading Problems**
```bash
# Verify dataset exists
ls -la data/netflix_titles.csv

# Check TMDB API key
echo $TMDB_API_KEY

# Test with sample data
PREFERRED_DATA_SOURCE=sample_data uv run python mcp_server/mcp_server.py
```

**3. Import Errors**
```bash
# Reinstall dependencies
uv sync --reinstall

# Check Python path
python -c "import sys; print(sys.path)"

# Verify installation
uv run python -c "print('Environment OK')"
```

**4. Performance Issues**
```bash
# Enable debug logging
DEBUG=true LOG_LEVEL=DEBUG uv run python mcp_server/mcp_server.py

# Check system resources
htop

# Monitor agent performance
uv run python -m agents.multi_agents --benchmark
```

## 📈 Performance Optimization

### System Requirements
- **Minimum**: 4GB RAM, 2 CPU cores, 10GB disk space
- **Recommended**: 8GB RAM, 4 CPU cores, 50GB disk space
- **Production**: 16GB RAM, 8 CPU cores, 100GB disk space

### Performance Tuning
```python
# config/performance.py
OPTIMIZATION_SETTINGS = {
    "agent_pool_size": 10,
    "cache_size": 1000,
    "batch_processing": True,
    "async_operations": True,
    "memory_limit": "8GB"
}
```

### Monitoring and Metrics
```bash
# Performance monitoring
uv run python scripts/performance_monitor.py

# System health check
uv run python scripts/health_check.py

# Generate performance report
uv run python scripts/performance_report.py
```

## 🤝 Contributing

We welcome contributions to the Netflix MCP Platform! This project represents cutting-edge work in Multi-Agent systems and MCP protocol implementation.

### Development Process

1. **Fork the Repository**
   ```bash
   git fork https://github.com/NatalieCheong/Multi-Agents-with-MCP-Server-Analyze-Netflix-TV-and-Movie-Shows.git
   ```

2. **Create Feature Branch**
   ```bash
   git checkout -b feature/amazing-multi-agent-enhancement
   ```

3. **Install Development Dependencies**
   ```bash
   uv sync
   uv add --dev pytest pytest-asyncio pytest-cov
   ```

4. **Make Your Changes**
   - Follow the existing code style and patterns
   - Add comprehensive tests for new functionality
   - Update documentation as needed
   - Ensure all agents work together harmoniously

5. **Run Quality Checks**
   ```bash
   # Format and lint
   uv run black .
   uv run isort .
   uv run mypy .
   uv run ruff check .
   
   # Run tests
   uv run pytest --cov
   
   # Test multi-agent integration
   uv run python agents/multi_agents.py --test
   ```

6. **Submit Pull Request**
   ```bash
   git commit -m 'Add amazing multi-agent enhancement'
   git push origin feature/amazing-multi-agent-enhancement
   ```

### Contribution Guidelines

- **Multi-Agent Focus**: Contributions should align with the multi-agent architecture vision
- **MCP Compliance**: Ensure all changes maintain MCP protocol compatibility
- **Safety First**: All new features must include appropriate guardrails
- **Documentation**: Update docs for any new functionality
- **Testing**: Maintain >90% test coverage for critical components

### Areas for Contribution

- **New Agent Types**: Specialized agents for different entertainment domains
- **MCP Extensions**: Enhanced protocol features and capabilities
- **Guardrail Enhancements**: Advanced safety and quality measures
- **Performance Optimization**: Scalability and efficiency improvements
- **Integration Connectors**: Support for additional data sources and platforms

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2024 Netflix MCP Platform Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## 🌟 Acknowledgments

This project represents innovative work in the intersection of Multi-Agent AI systems and protocol standardization. Special recognition to:

- **Anthropic** for the Claude AI platform and MCP protocol development
- **OpenAI** for GPT-4 and advanced language model capabilities
- **The Open Source Community** for foundational tools and libraries
- **Netflix** for inspiring the entertainment industry use case
- **TMDB** for providing alternative data sources and APIs

## 🔗 Related Projects

### Multi-Agent Systems
- [LangChain](https://github.com/langchain-ai/langchain) - Framework for developing applications with LLMs
- [AutoGPT](https://github.com/Significant-Gravitas/AutoGPT) - Autonomous AI agent platform
- [CrewAI](https://github.com/joaomdmoura/crewAI) - Multi-agent collaboration framework

### MCP Protocol
- [Model Context Protocol](https://github.com/modelcontextprotocol) - Official MCP specification
- [Claude Desktop](https://claude.ai/desktop) - AI desktop application with MCP support
- [MCP Servers](https://github.com/modelcontextprotocol/servers) - Reference MCP server implementations

### Entertainment Analytics
- [Kaggle Netflix Dataset](https://www.kaggle.com/datasets/shivamb/netflix-shows) - Netflix content analysis datasets
- [TMDB API](https://www.themoviedb.org/documentation/api) - The Movie Database API
- [OMDb API](https://www.omdbapi.com/) - Open Movie Database API

## 📞 Support & Community

### Getting Help
- **GitHub Issues**: Report bugs and request features
- **Discussions**: Join community conversations and Q&A
- **Documentation**: Comprehensive guides and API reference
- **Examples**: Real-world usage patterns and best practices

### Community Resources
- **Technical Blog**: Deep dives into multi-agent architecture
- **Video Tutorials**: Step-by-step implementation guides
- **Conference Talks**: Presentations on MCP and multi-agent systems
- **Research Papers**: Academic contributions and findings

### Professional Services
For enterprise deployment, custom agent development, or strategic consulting:
- **Architecture Consulting**: Multi-agent system design and implementation
- **Protocol Integration**: Custom MCP server development
- **Safety Compliance**: Guardrail system implementation and audit
- **Performance Optimization**: Scale and efficiency improvements

---

**🎬 Ready to revolutionize entertainment analytics with Multi-Agent AI?**

**🚀 Get started today and build the future of intelligent content platforms!**

---

*This project demonstrates cutting-edge concepts in Multi-Agent systems, MCP protocol implementation, and AI safety. It serves as both a functional entertainment analytics platform and a reference architecture for enterprise AI applications.*
