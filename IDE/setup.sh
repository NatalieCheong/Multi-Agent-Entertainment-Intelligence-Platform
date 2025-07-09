#!/bin/bash
# Netflix MCP Application - Complete Setup Script with Multi-Source Support
# This script sets up the development environment using uv package manager

set -e  # Exit on any error

echo "🎬 Netflix Multi-Agent MCP Platform - Complete Setup"
echo "===================================================================================="
echo "🚀 Building the Future of AI-Powered Entertainment Analytics"
echo "===================================================================================="

# Color codes for better output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠️${NC} $1"
}

print_error() {
    echo -e "${RED}❌${NC} $1"
}

print_info() {
    echo -e "${BLUE}ℹ️${NC} $1"
}

# Check if uv is installed
echo -e "\n${BLUE}🔧 Checking Prerequisites${NC}"
echo "===================================================================================="

if ! command -v uv &> /dev/null; then
    print_error "uv package manager not found!"
    echo "📦 Please install uv first:"
    echo "   curl -LsSf https://astral.sh/uv/install.sh | sh"
    echo "   # or"
    echo "   pip install uv"
    echo "   # or"
    echo "   brew install uv"
    exit 1
fi

print_status "uv package manager found"

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2 | cut -d'.' -f1,2)
REQUIRED_VERSION="3.9"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" = "$REQUIRED_VERSION" ]; then
    print_status "Python $PYTHON_VERSION detected (>= 3.9 required)"
else
    print_error "Python 3.9+ required, found $PYTHON_VERSION"
    exit 1
fi

# Initialize the project
echo -e "\n${BLUE}📝 Project Initialization${NC}"
echo "===================================================================================="

if [ ! -f "pyproject.toml" ]; then
    print_info "Initializing new Python project with uv..."
    uv init --name netflix-mcp-application
    print_status "Project initialized"
else
    print_status "pyproject.toml already exists"
fi

# Install dependencies
echo -e "\n${BLUE}📦 Installing Dependencies${NC}"
echo "===================================================================================="

print_info "Installing core dependencies with uv..."
uv sync

print_info "Installing development dependencies..."
uv add --dev pytest pytest-asyncio pytest-cov black isort mypy ruff pytest-watch

print_info "Installing optional dependencies..."
# Add optional dependencies that might be useful
uv add --optional web fastapi uvicorn httpx
uv add --optional ml scikit-learn nltk

print_status "All dependencies installed successfully"

# Create necessary directories
echo -e "\n${BLUE}📁 Creating Project Structure${NC}"
echo "===================================================================================="

directories=("logs" "data" "config" "docs" "benchmarks" "demo" "deployment" "data_sources")

for dir in "${directories[@]}"; do
    if [ ! -d "$dir" ]; then
        mkdir -p "$dir"
        print_status "Created directory: $dir"
    else
        print_info "Directory already exists: $dir"
    fi
done

# Create .env file if it doesn't exist
echo -e "\n${BLUE}🔑 Environment Configuration${NC}"
echo "===================================================================================="

if [ ! -f ".env" ]; then
    print_info "Creating .env file template..."
    cat > .env << 'EOF'
# Netflix MCP Application Environment Variables
# ==============================================

# API Keys (Required for full functionality)
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
TMDB_API_KEY=your_tmdb_api_key_here

# Data Source Configuration
NETFLIX_DATASET_PATH=data/netflix_titles.csv
PREFERRED_DATA_SOURCE=auto  # auto, netflix_csv, tmdb_api, sample_data

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
ENABLE_ANALYTICS=true
MAX_CONCURRENT_AGENTS=5
RESPONSE_TIMEOUT=30

# Performance Configuration
CACHE_SIZE=1000
BATCH_PROCESSING=true
ASYNC_OPERATIONS=true
MEMORY_LIMIT=8GB

# Development Configuration
ENVIRONMENT=development
DEBUG=true

# Security Configuration (for production)
SECRET_KEY=netflix-mcp-secret-key-change-in-production
API_RATE_LIMIT=100
CORS_ORIGINS=*

# Database Configuration (optional)
DATABASE_URL=
REDIS_URL=

# Monitoring Configuration (optional)
PROMETHEUS_ENABLED=false
GRAFANA_ENABLED=false
ELASTICSEARCH_ENABLED=false
EOF
    print_warning "Please update the .env file with your actual API keys"
    print_info "Required: OPENAI_API_KEY"
    print_info "Optional: ANTHROPIC_API_KEY, TMDB_API_KEY"
else
    print_status ".env file already exists"
fi

# Check data sources
echo -e "\n${BLUE}📊 Checking Data Sources${NC}"
echo "===================================================================================="

# Check Netflix CSV
if [ -f "data/netflix_titles.csv" ]; then
    file_size=$(du -h "data/netflix_titles.csv" | cut -f1)
    print_status "Netflix dataset found (Size: $file_size)"
    
    # Quick validation of CSV structure
    if head -1 "data/netflix_titles.csv" | grep -q "show_id,type,title"; then
        print_status "Netflix CSV structure validated"
    else
        print_warning "Netflix CSV structure may be incorrect"
    fi
else
    print_warning "Netflix dataset not found (data/netflix_titles.csv)"
    print_info "Download from: https://www.kaggle.com/datasets/shivamb/netflix-shows"
fi

# Check TMDB API key
if [ -f ".env" ] && grep -q "TMDB_API_KEY=your_tmdb_api_key_here" .env; then
    print_warning "TMDB API key not configured"
    print_info "Get API key from: https://www.themoviedb.org/settings/api"
elif [ -f ".env" ] && grep -q "TMDB_API_KEY=" .env && ! grep -q "TMDB_API_KEY=your_tmdb_api_key_here" .env; then
    print_status "TMDB API key configured"
else
    print_info "TMDB API key status unknown"
fi

# Data source recommendation
if [ -f "data/netflix_titles.csv" ]; then
    print_status "Recommended: Use Netflix CSV for comprehensive analysis"
elif grep -q "TMDB_API_KEY=" .env && ! grep -q "TMDB_API_KEY=your_tmdb_api_key_here" .env; then
    print_status "Recommended: Use TMDB API for real-time data"
else
    print_warning "No external data source configured - will use sample data"
    print_info "Add Netflix CSV to data/ or set TMDB_API_KEY in .env for better functionality"
fi

# Create .gitignore if it doesn't exist
echo -e "\n${BLUE}📝 Git Configuration${NC}"
echo "===================================================================================="

if [ ! -f ".gitignore" ]; then
    print_info "Creating comprehensive .gitignore..."
    cat > .gitignore << 'EOF'
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

# IDEs and Editors
.vscode/
.idea/
*.swp
*.swo
*~
.cursor/
.sublime-*

# Logs and monitoring
logs/
*.log
monitoring/
grafana/data/
prometheus/data/

# Data files (protect sensitive data)
data/netflix_titles.csv
data/*.csv
data/*.json
data/*.parquet
data/*.xlsx
models/
custom_models/

# API Keys and secrets
.env
.env.local
.env.production
.env.staging
.env.development
config/secrets.json
config/keys/
*.key
*.pem

# OS generated files
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db
desktop.ini

# Package managers
.uv/
uv.lock
node_modules/
package-lock.json
yarn.lock

# Testing and coverage
.pytest_cache/
.coverage
htmlcov/
.tox/
.nox/
coverage.xml
*.cover
*.py,cover
.hypothesis/

# Type checking
.mypy_cache/
.dmypy.json
dmypy.json
.pytype/

# Linting
.ruff_cache/
.pylint.d/

# Jupyter Notebooks
.ipynb_checkpoints
*.ipynb

# Docker
.dockerignore
docker-compose.override.yml
.docker/

# Temporary files
tmp/
temp/
*.tmp
*.temp
.cache/

# Build artifacts
dist/
build/
*.egg-info/

# Claude Desktop (backup configs)
claude_desktop_config.json.backup

# Benchmarks and performance data
benchmarks/results/
benchmarks/*.json
performance_reports/

# Demo outputs
demo/outputs/
demo/recordings/

# Deployment artifacts
deployment/*.pid
deployment/logs/
k8s/secrets/
helm/charts/*/charts/
terraform/.terraform/
terraform/terraform.tfstate*

# AI model artifacts
*.pkl
*.joblib
*.model
*.onnx
EOF
    print_status ".gitignore created"
else
    print_status ".gitignore already exists"
fi

# Create comprehensive README.md if it doesn't exist
echo -e "\n${BLUE}📚 Documentation Setup${NC}"
echo "===================================================================================="

if [ ! -f "README.md" ]; then
    print_info "Creating comprehensive README.md..."
    cat > README.md << 'EOF'
# 🎬 Netflix Multi-Agent MCP Platform

**A Professional Multi-Agent Business Intelligence MCP Server with AI Orchestration and Content Safety Guardrails**

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![MCP Protocol](https://img.shields.io/badge/MCP-Protocol-green.svg)](https://github.com/modelcontextprotocol)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![uv](https://img.shields.io/badge/uv-package%20manager-orange.svg)](https://github.com/astral-sh/uv)

## 🌟 Overview

This project represents the next generation of AI-powered content analysis platforms, featuring a sophisticated **Multi-Agent Architecture** integrated with the **Model Context Protocol (MCP)** for seamless AI service orchestration.

### 🎯 Key Innovation Areas

- **Agent Architecture & Orchestration**: Multi-agent system with specialized Netflix domain experts
- **MCP Ecosystem Building**: Standards-compliant protocol implementation for AI service integration
- **Content Safety Guardrails**: Advanced AI safety and quality assurance systems
- **Business Intelligence**: Real-world entertainment industry data analysis capabilities

## 🚀 Quick Start

### Prerequisites

- **Python 3.9+**
- **[uv package manager](https://github.com/astral-sh/uv)**
- **OpenAI API key**

### Installation

1. **Clone and setup:**
```bash
git clone <your-repo-url>
cd netflix-mcp-platform
chmod +x setup.sh
./setup.sh
```

2. **Configure environment:**
```bash
# Update .env with your API keys
nano .env
```

3. **Add data source (choose one):**
```bash
# Option A: Netflix CSV (recommended)
# Download and place netflix_titles.csv in data/ directory

# Option B: TMDB API
# Set TMDB_API_KEY in .env file

# Option C: Sample data (automatic fallback)
```

### Running the Platform

```bash
# Start MCP server
uv run python mcp_server/mcp_server.py

# Or run comprehensive demo
uv run python demo/demo_script.py --full

# Or run performance benchmarks
uv run python benchmarks/performance_test.py --full
```

## 📊 Available Data Sources

| Source | Description | Setup Required |
|--------|-------------|----------------|
| **Netflix CSV** | Complete Netflix dataset | Download CSV to `data/` |
| **TMDB API** | Real-time movie/TV data | Configure `TMDB_API_KEY` |
| **Sample Data** | Generated test dataset | No setup (automatic) |

## 🤖 Multi-Agent System

- **Content Discovery Agent** - Find movies and shows
- **Analytics Specialist Agent** - Analyze trends and data  
- **Recommendation Engine Agent** - Personalized suggestions
- **Customer Support Agent** - Help with Netflix features
- **Content Strategy Agent** - Business strategy insights

## 🔗 MCP Protocol Integration

Full Claude Desktop integration with standardized AI service communication.

## 🔒 Content Safety Guardrails

Advanced AI safety system with content filtering, quality assessment, and bias detection.

## 📈 Performance & Monitoring

Built-in benchmarking, performance monitoring, and scalability testing.

## 🏗️ Project Structure

```
├── mcp_server/          # MCP server implementation
├── agents/              # Multi-agent system
├── guardrail/           # Content safety guardrails
├── data_sources/        # TMDB integration
├── demo/                # Demonstration scripts
├── benchmarks/          # Performance testing
├── deployment/          # Docker and deployment configs
└── docs/                # Documentation
```

## 🧪 Testing

```bash
# Run all tests
uv run pytest

# Run performance benchmarks
uv run python benchmarks/performance_test.py

# Run demo
uv run python demo/demo_script.py
```

## 🚀 Deployment

Docker Compose configuration available for production deployment.

## 📜 License

MIT License - see [LICENSE](LICENSE) file for details.

---

**Ready to revolutionize entertainment analytics with Multi-Agent AI?**
EOF
    print_status "README.md created"
else
    print_status "README.md already exists"
fi

# Create basic test files
echo -e "\n${BLUE}🧪 Setting Up Tests${NC}"
echo "===================================================================================="

mkdir -p test

if [ ! -f "test/test_basic.py" ]; then
    cat > test/test_basic.py << 'EOF'
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
        from agents import multi_agents
        from guardrail import guardrail
        assert True
    except ImportError as e:
        pytest.fail(f"Import failed: {e}")

def test_sample_business_logic():
    """Test basic business logic functionality"""
    from mcp_server.mcp_server import enhanced_business_query_logic
    
    result = enhanced_business_query_logic("What percentage of Netflix content is Korean?")
    assert result["status"] == "success"
    assert "business_intelligence" in result

def test_data_source_loading():
    """Test data source loading functionality"""
    from mcp_server.mcp_server import load_netflix_dataset
    
    dataset = load_netflix_dataset()
    assert dataset is not None
    assert len(dataset) > 0
    assert "title" in dataset.columns
    assert "type" in dataset.columns

if __name__ == "__main__":
    pytest.main([__file__])
EOF
    print_status "Basic test file created"
fi

# Create additional helpful scripts
echo -e "\n${BLUE}🛠️ Creating Helper Scripts${NC}"
echo "===================================================================================="

# Create health check script
if [ ! -f "scripts/health_check.py" ]; then
    mkdir -p scripts
    cat > scripts/health_check.py << 'EOF'
#!/usr/bin/env python3
"""Health check script for Netflix MCP Platform"""

import sys
import os
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

def check_environment():
    """Check environment setup"""
    print("🔍 Environment Health Check")
    print("=" * 40)
    
    # Check Python version
    print(f"Python Version: {sys.version}")
    
    # Check data sources
    netflix_csv = Path("data/netflix_titles.csv")
    print(f"Netflix CSV: {'✅ Found' if netflix_csv.exists() else '❌ Not Found'}")
    
    tmdb_key = os.getenv('TMDB_API_KEY')
    print(f"TMDB API Key: {'✅ Configured' if tmdb_key and tmdb_key != 'your_tmdb_api_key_here' else '❌ Not Configured'}")
    
    openai_key = os.getenv('OPENAI_API_KEY')
    print(f"OpenAI API Key: {'✅ Configured' if openai_key and openai_key != 'your_openai_api_key_here' else '❌ Not Configured'}")
    
    # Check modules
    try:
        from mcp_server.mcp_server import load_netflix_dataset
        dataset = load_netflix_dataset()
        print(f"Dataset Loading: ✅ Working ({len(dataset)} titles)")
    except Exception as e:
        print(f"Dataset Loading: ❌ Error ({e})")
    
    print("\n🎉 Health check complete!")

if __name__ == "__main__":
    check_environment()
EOF
    chmod +x scripts/health_check.py
    print_status "Health check script created"
fi

# Run a quick validation test
echo -e "\n${BLUE}🧪 Running Initial Validation${NC}"
echo "===================================================================================="

print_info "Testing Python environment..."
if uv run python -c "print('✅ Python environment working')"; then
    print_status "Python environment verified"
else
    print_error "Python environment test failed"
    exit 1
fi

print_info "Testing basic imports..."
if uv run python -c "import pandas as pd, numpy as np; print('✅ Core libraries working')"; then
    print_status "Core libraries verified"
else
    print_warning "Some core libraries may need attention"
fi

print_info "Testing project structure..."
if uv run python -c "from pathlib import Path; assert Path('mcp_server').exists(); print('✅ Project structure OK')"; then
    print_status "Project structure verified"
else
    print_error "Project structure validation failed"
fi

# Final summary and instructions
echo -e "\n${GREEN}🎉 Setup Complete!${NC}"
echo "===================================================================================="
echo -e "📋 ${BLUE}Next Steps:${NC}"
echo ""
echo "1. 🔑 Configure API Keys:"
echo "   nano .env"
echo "   # Add your OPENAI_API_KEY (required)"
echo "   # Add your TMDB_API_KEY (optional)"
echo ""
echo "2. 📊 Add Data Source (choose one):"
echo "   # Option A: Download Netflix dataset"
echo "   # Place netflix_titles.csv in data/ directory"
echo "   # Option B: Configure TMDB_API_KEY in .env"
echo "   # Option C: Use sample data (automatic)"
echo ""
echo "3. 🧪 Test Installation:"
echo "   uv run python scripts/health_check.py"
echo "   uv run python -m pytest test/"
echo ""
echo "4. 🚀 Start the Platform:"
echo "   uv run python mcp_server/mcp_server.py"
echo ""
echo "5. 🎭 Run Demo:"
echo "   uv run python demo/demo_script.py --full"
echo ""
echo "6. ⚡ Run Benchmarks:"
echo "   uv run python benchmarks/performance_test.py --full"
echo ""
echo "7. 🔗 Configure Claude Desktop:"
echo "   # See claude_desktop_config.json for integration"
echo ""
echo -e "🎬 ${GREEN}Your Netflix Multi-Agent MCP Platform is ready!${NC}"
echo -e "📚 ${BLUE}Check README.md for detailed usage instructions${NC}"
echo -e "🔧 ${BLUE}Run health check: uv run python scripts/health_check.py${NC}"
echo "===================================================================================="

# Show data source status
echo -e "\n${BLUE}📊 Current Data Source Status:${NC}"
if [ -f "data/netflix_titles.csv" ]; then
    echo -e "${GREEN}✅ Netflix CSV Available${NC} - Ready for comprehensive analysis"
elif grep -q "TMDB_API_KEY=" .env && ! grep -q "TMDB_API_KEY=your_tmdb_api_key_here" .env; then
    echo -e "${GREEN}✅ TMDB API Configured${NC} - Ready for real-time data"
else
    echo -e "${YELLOW}⚠️ Using Sample Data${NC} - Configure external source for production"
fi

echo -e "\n${GREEN}🚀 Happy coding with the Netflix Multi-Agent MCP Platform!${NC}"
