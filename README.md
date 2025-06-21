# Netflix Multi-Agent Business Intelligence MCP Server

A comprehensive Netflix Multi-Agent Business Intelligence MCP Server with AI Agents and Content Safety Guardrails for analyzing Netflix TV and Movie Shows data.

🎬 Project Overview

This project leverages the Model Context Protocol (MCP) to create an intelligent Netflix content analysis system using real Netflix dataset from Kaggle. The system employs multi-agent AI architecture with content safety guardrails to provide comprehensive business intelligence insights about Netflix's content strategy, trends, and global distribution.

🚀 Key Features

📊 Business Intelligence Capabilities

- Content Analysis: Deep dive into Netflix's 8,000+ titles catalog
- Global Content Distribution: Understanding content availability across different countries
- Trend Analysis: Movie vs TV show patterns over 20-30 years
- Release Strategy Insights: Optimal timing for TV show launches
- Talent Analysis: Actor/director performance across different content types
- Market Intelligence: Netflix's strategic focus on TV shows vs movies

🤖 Multi-Agent System

- Content Discovery Agent: Find movies and shows based on preferences
- Analytics Specialist Agent: Analyze trends, data, and market insights
- Recommendation Engine Agent: Personalized content suggestions
- Customer Support Agent: Help with Netflix features and policies
- Content Strategy Agent: Business strategy and investment insights

🔒 Content Safety Guardrails

- Age-Appropriate Filtering: Family-safe content recommendations
- Quality Assessment: Response accuracy and completeness validation
- Business Logic Validation: Strategic viability and market alignment
- Bias Detection: Cultural, demographic, and regional fairness
- Cultural Sensitivity: Global audience appropriateness

🛠️ Technical Architecture

- MCP Protocol Support: Full Model Context Protocol implementation
- Claude Desktop Integration: Seamless AI workflow integration
- Professional Development Setup: Modern Python tooling with uv package manager
- Cross-Platform Compatibility: IDE environment and Google Colab support

# 📈 Analytics & Insights
🌍 Global Content Analysis

- Content Distribution: Analysis of Netflix content across 190+ countries
- Regional Preferences: Local vs international content consumption patterns
- Cultural Impact: Korean content growth (370% viewership increase)
- Market Penetration: International content now represents 60%+ of viewing hours

📺 Content Evolution Trends

- Historical Analysis: 20-30 year movie release patterns
- Format Shift: TV shows vs movies strategic focus analysis
- Release Timing: Optimal launch windows for different content types
- Genre Performance: Drama, Comedy, Thriller, and International content trends

🎭 Talent & Production Insights

- Director Analysis: Most prolific directors and their content performance
- Actor Performance: Cross-content type talent analysis
- Production Trends: Netflix Originals vs licensed content strategy
- Investment Patterns: $15+ billion annual content investment analysis

🏗️ Project Structure
├── 📁 IDE/                          # Professional IDE Environment
│   ├── mcp_server/                  # MCP server implementation
│   ├── mcp_client/                  # MCP client for testing
│   ├── mcp_application/             # Complete application wrapper
│   ├── agents/                      # Multi-agent system
│   ├── guardrail/                   # Content safety guardrails
│   ├── test/                        # Test files
│   ├── pyproject.toml               # Project configuration
│   ├── setup.sh                     # Setup script
│   └── README.md                    # IDE environment guide
│
├── 📁 google_colab_environment/     # Google Colab Compatible
│   ├── notebook/                    # Jupyter notebook
│   ├── mcp_server/                  # Colab-optimized server
│   ├── agents/                      # Multi-agent system
│   ├── guardrail/                   # Safety guardrails
│   └── requirements.txt             # Dependencies
│
├── 📁 data/                         # Dataset storage
│   └── netflix_titles.csv           # Netflix dataset
│
└── 📁 docs/                         # Documentation

🔧 Quick Start
Prerequisites

Python 3.9+
uv package manager (for IDE environment)
OpenAI API key
Netflix dataset from Kaggle

IDE Environment Setup

1. Clone and setup:   
   git clone <your-repo-url>
   cd AI-Agents-with-MCP-Server-for-Netflix-TV-and-Movie-Shows/IDE
   chmod +x setup.sh
   ./setup.sh

2. Configure environment:
   # Update .env with your API keys
   nano .env

3. Add Netflix dataset:
   # Download from Kaggle and place in data directory
   cp path/to/netflix_titles.csv data/
   
4. Start the MCP server:

   uv run python mcp_server/mcp_server.py

Google Colab Setup

1. Upload files to Colab:

Upload all files from google_colab_environment/ to /content/
Mount Google Drive for dataset storage

2. Install dependencies:
   !pip install mcp openai pandas numpy nest-asyncio

Claude Desktop Integration: 

Add to Claude Desktop configuration:

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

3. Restart Claude Desktop

🎯 Available MCP Tools
1. netflix_business_query
Business intelligence queries with real Netflix data:

{
  "natural_language_query": "What percentage of Netflix content is Korean?"
}

2. netflix_content_recommendations
AI-powered content recommendations:

{
  "user_preferences": "action movies for teenagers",
  "age_rating": "teen"
}

3. netflix_analytics_insights
Analytics and trend insights:

{
  "metric_type": "engagement",
  "time_period": "monthly"
}

📊 Sample Business Intelligence Queries
  Content Distribution Analysis
- What type of content is available in different countries?
- How has the number of movies released per year changed over the last 20-30 years?
- Comparison of TV shows vs. movies on Netflix
- What is the best time to launch a TV show?
- Analysis of actors/directors of different types of shows/movies
- Does Netflix have more focus on TV Shows than movies in recent years?
- Understanding what content is available in different countries

  Advanced Analytics
- What percentage of Netflix content is Korean?
- What are the most popular genres globally?
- Show me the trend of international vs US content
- Which countries produce the most Netflix content?
- What's the distribution of content by release year?
- Which directors have the most titles on Netflix?

🧪 Testing
Run Comprehensive Tests

# IDE Environment
uv run pytest

# Test specific components
uv run python -c "from agents.multi_agents import test_netflix_multi_agents; test_netflix_multi_agents()"
uv run python -c "from guardrail.guardrail import test_guardrail_system; test_guardrail_system()"

Google Colab Testing

# In Colab notebook
from multi_agents_fastmcp import test_netflix_multi_agents
from guardrail_fastmcp import test_guardrail_system

test_netflix_multi_agents()
test_guardrail_system()

📈 Performance Metrics

✅ 75%+ test coverage for comprehensive quality assurance
✅ Real Netflix data analysis with 8,000+ titles
✅ 5 specialized AI agents for different business domains
✅ Advanced guardrail system for content safety
✅ Professional development setup with modern tooling
✅ Claude Desktop integration for seamless AI workflows

🔒 Safety & Compliance
Content Safety Features

Age-Appropriate Filtering: Automatic filtering for family content
Cultural Sensitivity: Global audience consideration
Bias Detection: Demographic and regional fairness
Quality Assurance: Response accuracy validation

Business Compliance

Strategic Alignment: Netflix business model compatibility
Market Viability: Commercial feasibility assessment
Competitive Analysis: Market positioning validation

Dataset Resources: https://www.kaggle.com/datasets/anandshaw2001/netflix-movies-and-tv-shows


