# 🎬 Multi-Agent Entertainment Intelligence Platform

**A Professional Multi-Agent Business Intelligence MCP Server with AI Orchestration and Content Safety Guardrails**

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![MCP Protocol](https://img.shields.io/badge/MCP-Protocol-green.svg)](https://github.com/modelcontextprotocol)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![uv](https://img.shields.io/badge/uv-package%20manager-orange.svg)](https://github.com/astral-sh/uv)

## 🌟 Overview

This project represents the next generation of AI-powered entertainment intelligence platforms, featuring a sophisticated **Multi-Agent Architecture** integrated with the **Model Context Protocol (MCP)** for seamless AI service orchestration. Built for comprehensive entertainment industry analysis, it demonstrates advanced concepts in distributed AI systems and protocol standardization.

### 🎯 Key Innovation Areas

- **Agent Architecture & Orchestration**: Multi-agent system with specialized entertainment domain experts
- **MCP Ecosystem Building**: Standards-compliant protocol implementation for AI service integration
- **Content Safety Guardrails**: Advanced AI safety and quality assurance systems
- **Entertainment Intelligence**: Real-world industry data analysis with multiple data sources

## 🚀 Features

### 🤖 Multi-Agent System
- **5 Specialized AI Agents** for different entertainment business domains
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

### 📊 Entertainment Intelligence
- **Multi-Source Data Analysis** (Netflix, TMDB, and custom datasets)
- **International Content Trends** and market insights
- **Genre Performance Analytics** and recommendation systems
- **Competitive Intelligence** and market positioning analysis

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│          Entertainment Intelligence Platform                │
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
│  Netflix Dataset  │  TMDB Integration  │  Custom Sources   │
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
   git clone https://github.com/NatalieCheong/Multi-Agent-Entertainment-Intelligence-Platform.git
   cd Multi-Agent-Entertainment-Intelligence-Platform
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
uv run entertainment-intelligence-server

# Method 3: With specific environment
uv run --env-file .env python mcp_server/mcp_server.py
```

#### Claude Desktop Integration

1. **Configure Claude Desktop** (`claude_desktop_config.json`):
   ```json
   {
     "mcpServers": {
       "entertainment-intelligence": {
         "command": "uv",
         "args": ["run", "python", "mcp_server/mcp_server.py"],
         "cwd": "/absolute/path/to/Multi-Agent-Entertainment-Intelligence-Platform",
         "env": {
           "OPENAI_API_KEY": "your_openai_api_key_here",
           "NETFLIX_DATASET_PATH": "data/netflix_titles.csv",
           "TMDB_API_KEY": "your_tmdb_api_key_here"
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

### Entertainment Intelligence Queries
```
What percentage of Netflix content is Korean?
Show me the trend of international vs US content
What are the most popular genres globally?
Analyze thriller content performance in Asian markets
Compare Netflix and TMDB data for accuracy
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

# Run comprehensive demo
uv run python demo/demo_script.py --full

# Run performance benchmarks
uv run python benchmarks/performance_test.py --full
```

## 📊 Available MCP Tools

| Tool Name | Description | Use Case |
|-----------|-------------|----------|
| `entertainment_business_query` | Advanced BI queries with multi-agent analysis | Market research, trend analysis |
| `entertainment_test_query` | Simple connectivity and functionality test | Development and debugging |
| `entertainment_dataset_info` | Comprehensive dataset statistics | Data validation and exploration |
| `entertainment_content_recommendations` | AI-powered content suggestions | Personalization and user engagement |
| `entertainment_search_content` | Multi-agent content discovery | Content search and filtering |
| `entertainment_analytics_insights` | Advanced analytics and metrics | Performance monitoring and insights |
| `entertainment_data_source_switch` | Switch between data sources | TMDB/Netflix/Sample data management |

## 🤖 AI Agents Specifications

### 1. Content Discovery Agent
- **Purpose**: Movie and TV show search and discovery across multiple sources
- **Capabilities**: Genre filtering, cast/director search, cross-platform content metadata analysis
- **Use Cases**: Content recommendation, catalog exploration, user query resolution

### 2. Analytics Specialist Agent
- **Purpose**: Data analysis and business intelligence across entertainment platforms
- **Capabilities**: Trend analysis, performance metrics, competitive benchmarking
- **Use Cases**: Market research, strategy planning, ROI analysis

### 3. Recommendation Engine Agent
- **Purpose**: Personalized content suggestions using multiple data sources
- **Capabilities**: User preference modeling, collaborative filtering, content matching
- **Use Cases**: User engagement, personalization, retention optimization

### 4. Customer Support Agent
- **Purpose**: User assistance and platform guidance for entertainment services
- **Capabilities**: FAQ handling, troubleshooting, feature explanation
- **Use Cases**: Customer service, user onboarding, issue resolution

### 5. Content Strategy Agent
- **Purpose**: Business strategy and content planning for entertainment industry
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
Multi-Agent-Entertainment-Intelligence-Platform/
├── 📁 mcp_server/           # Entertainment MCP Server implementation
│   ├── mcp_server.py        # Main server with enhanced BI logic
│   └── __init__.py
├── 📁 mcp_client/           # MCP client for testing and development
│   ├── mcp_client.py        # Client implementation with mock support
│   └── __init__.py
├── 📁 mcp_application/      # Complete application wrapper
│   ├── mcp_application.py   # Application management and orchestration
│   └── __init__.py
├── 📁 agents/               # Entertainment AI Agents system
│   ├── multi_agents.py      # Agent definitions and orchestration logic
│   └── __init__.py
├── 📁 guardrail/            # Content Safety for Entertainment
│   ├── guardrail.py         # Guardrail system with AI judges
│   └── __init__.py
├── 📁 data_sources/         # Netflix, TMDB, and other data sources
│   ├── tmdb_integration.py  # TMDB API integration
│   └── __init__.py
├── 📁 demo/                 # Demonstration scripts and examples
│   ├── demo_script.py       # Comprehensive platform demonstration
│   └── __init__.py
├── 📁 benchmarks/           # Performance testing and optimization
│   ├── performance_test.py  # Performance benchmarking suite
│   └── __init__.py
├── 📁 deployment/           # Docker and deployment configurations
│   ├── docker-compose.yml   # Production deployment setup
│   ├── Dockerfile          # Container configuration
│   └── kubernetes/         # K8s deployment manifests
├── 📁 test/                 # Comprehensive test suite
│   ├── test_basic.py        # Basic functionality tests
│   ├── test_agents.py       # Multi-agent system tests
│   ├── test_guardrails.py   # Safety system tests
│   └── __init__.py
├── 📁 logs/                 # Application logs and monitoring
├── 📁 data/                 # Dataset storage (Netflix CSV/TMDB)
├── 📁 config/               # Configuration files and settings
├── 📁 docs/                 # Documentation and guides
├── 📁 scripts/              # Utility and helper scripts
│   ├── health_check.py      # System health verification
│   └── performance_monitor.py # Performance monitoring
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
PREFERRED_DATA_SOURCE=auto  # auto, netflix_csv, tmdb_api, sample_data

# Logging Configuration
LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR
LOG_FILE=logs/entertainment_intelligence_server.log

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

DATA_SOURCE_CONFIGURATION = {
    "tmdb_rate_limit": 40,  # requests per 10 seconds
    "netflix_cache_ttl": 3600,  # 1 hour
    "sample_data_size": 200  # number of sample records
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
```bash
# Build and run with Docker Compose
docker-compose up -d

# Scale for production
docker-compose --profile production up -d

# With monitoring stack
docker-compose --profile production --profile monitoring up -d
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
tail -f logs/entertainment_intelligence_server.log
```

**2. Dataset Loading Problems**
```bash
# Verify dataset exists
ls -la data/netflix_titles.csv

# Check TMDB API key
echo $TMDB_API_KEY

# Test with sample data
PREFERRED_DATA_SOURCE=sample_data uv run python mcp_server/mcp_server.py

# Switch data sources
uv run python -c "from mcp_server.mcp_server import load_netflix_dataset; print(len(load_netflix_dataset()))"
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

# Run performance benchmarks
uv run python benchmarks/performance_test.py --full

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
    "memory_limit": "8GB",
    "tmdb_concurrent_requests": 5,
    "data_processing_chunk_size": 1000
}
```

### Monitoring and Metrics
```bash
# Performance monitoring
uv run python scripts/performance_monitor.py

# System health check
uv run python scripts/health_check.py

# Generate performance report
uv run python benchmarks/performance_test.py --full

# Comprehensive demo with metrics
uv run python demo/demo_script.py --full
```

## 🤝 Contributing

We welcome contributions to the Multi-Agent Entertainment Intelligence Platform! This project represents cutting-edge work in Multi-Agent systems and MCP protocol implementation.

### Development Process

1. **Fork the Repository**
   ```bash
   git fork https://github.com/NatalieCheong/Multi-Agent-Entertainment-Intelligence-Platform.git
   ```

2. **Create Feature Branch**
   ```bash
   git checkout -b feature/amazing-entertainment-enhancement
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
   
   # Run comprehensive demo
   uv run python demo/demo_script.py --full
   ```

6. **Submit Pull Request**
   ```bash
   git commit -m 'Add amazing entertainment intelligence enhancement'
   git push origin feature/amazing-entertainment-enhancement
   ```

### Contribution Guidelines

- **Multi-Agent Focus**: Contributions should align with the multi-agent architecture vision
- **MCP Compliance**: Ensure all changes maintain MCP protocol compatibility
- **Safety First**: All new features must include appropriate guardrails
- **Documentation**: Update docs for any new functionality
- **Testing**: Maintain >90% test coverage for critical components

### Areas for Contribution

- **New Agent Types**: Specialized agents for different entertainment domains
- **Data Source Integrations**: Support for additional APIs and datasets
- **MCP Extensions**: Enhanced protocol features and capabilities
- **Guardrail Enhancements**: Advanced safety and quality measures
- **Performance Optimization**: Scalability and efficiency improvements
- **Industry-Specific Features**: Gaming, music, books, podcasts analytics

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2024 Multi-Agent Entertainment Intelligence Platform Contributors

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

This project represents innovative work in the intersection of Multi-Agent AI systems and entertainment intelligence. Special recognition to:

- **Anthropic** for the Claude AI platform and MCP protocol development
- **OpenAI** for GPT-4 and advanced language model capabilities
- **The Open Source Community** for foundational tools and libraries
- **Netflix** for inspiring the entertainment industry use case
- **TMDB** for providing comprehensive entertainment data APIs
- **Entertainment Industry** for real-world use case validation

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
- [Spotify Web API](https://developer.spotify.com/documentation/web-api) - Music streaming analytics

## 📞 Support & Community

### Getting Help
- **GitHub Issues**: Report bugs and request features
- **Discussions**: Join community conversations and Q&A
- **Documentation**: Comprehensive guides and API reference
- **Examples**: Real-world usage patterns and best practices

### Community Resources
- **Technical Blog**: Deep dives into multi-agent architecture for entertainment
- **Video Tutorials**: Step-by-step implementation guides
- **Conference Talks**: Presentations on MCP and multi-agent systems in entertainment
- **Research Papers**: Academic contributions and findings

### Professional Services
For enterprise deployment, custom agent development, or strategic consulting:
- **Architecture Consulting**: Multi-agent system design and implementation
- **Protocol Integration**: Custom MCP server development for entertainment platforms
- **Safety Compliance**: Guardrail system implementation and audit
- **Performance Optimization**: Scale and efficiency improvements for large datasets
- **Industry Integration**: Custom data source integrations and specialized agents

---

**🎬 Ready to revolutionize entertainment intelligence with Multi-Agent AI?**

**🚀 Get started today and build the future of intelligent entertainment platforms!**

---

*This project demonstrates cutting-edge concepts in Multi-Agent systems, MCP protocol implementation, and AI safety applied to the entertainment industry. It serves as both a functional entertainment intelligence platform and a reference architecture for enterprise AI applications in media and entertainment.*











