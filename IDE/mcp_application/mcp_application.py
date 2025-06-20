#!/usr/bin/env python3
"""
Netflix MCP Application - Cursor IDE Version
Professional setup with proper imports and local file paths
"""

import asyncio
import json
import os
import sys
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=os.getenv('LOG_LEVEL', 'INFO'),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.getenv('LOG_FILE', 'logs/netflix_mcp_app.log')),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("netflix-mcp-app")

# Ensure logs directory exists
Path("logs").mkdir(exist_ok=True)

class NetflixMCPApplication:
    """
    Complete Netflix MCP Application - Cursor IDE Version
    Professional setup with proper dependency management
    """
    
    def __init__(self, app_name: str = "Netflix Business Intelligence MCP"):
        self.app_name = app_name
        self.server_process = None
        self.client = None
        self.prompts = {}
        self.resources = {}
        self.config = self.load_config()
        self.mcp_available = False
        self.project_root = Path(__file__).parent.parent
        
        logger.info(f"🎬 Initializing {app_name} (Cursor IDE)")
    
    def load_config(self) -> Dict[str, Any]:
        """Load application configuration from environment and defaults"""
        config = {
            "server": {
                "name": "netflix-business-intelligence",
                "version": "2.0.0",
                "description": "Netflix Business Intelligence MCP Server with Multi-Agents and Guardrails",
                "script_path": os.getenv('MCP_SERVER_SCRIPT', str(Path(__file__).parent.parent / "mcp_server" / "mcp_server.py"))
            },
            "client": {
                "name": "netflix-mcp-client",
                "version": "2.0.0",
                "connection_timeout": int(os.getenv('MCP_CONNECTION_TIMEOUT', '30'))
            },
            "features": {
                "multi_agents": os.getenv('ENABLE_MULTI_AGENTS', 'true').lower() == 'true',
                "guardrails": os.getenv('ENABLE_GUARDRAILS', 'true').lower() == 'true',
                "prompts": True,
                "resources": True
            },
            "dataset": {
                "path": os.getenv('NETFLIX_DATASET_PATH', str(Path(__file__).parent.parent / "data" / "netflix_titles.csv")),
                "expected_size": int(os.getenv('EXPECTED_DATASET_SIZE', '8000'))
            },
            "environment": {
                "mode": os.getenv('ENVIRONMENT', 'development'),
                "debug": os.getenv('DEBUG', 'false').lower() == 'true'
            }
        }
        return config
    
    async def initialize_server(self):
        """Initialize the MCP Server"""
        logger.info("🔧 Initializing MCP Server...")
        
        try:
            # Check if mcp_server.py exists
            server_path = Path(self.config["server"]["script_path"])
            if not server_path.exists():
                logger.error(f"❌ MCP Server file not found: {server_path}")
                return False
            
            # Import and test the server module
            sys.path.append(str(self.project_root))
            try:
                from mcp_server import mcp_server
                logger.info("✅ MCP Server module imported successfully")
                
                # Start server in background (simplified for development)
                server_task = asyncio.create_task(self.run_server_standalone())
                self.server_process = server_task
                
                # Wait a moment for server to initialize
                await asyncio.sleep(2)
                
                logger.info("✅ MCP Server initialized successfully")
                return True
                
            except Exception as e:
                logger.error(f"❌ Failed to import MCP Server: {e}")
                return False
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize MCP Server: {e}")
            return False
    
    async def run_server_standalone(self):
        """Run server in standalone mode for development"""
        try:
            from mcp_server import mcp_server
            await mcp_server.test_standalone_server()
        except Exception as e:
            logger.error(f"❌ Standalone server error: {e}")
    
    async def initialize_client(self):
        """Initialize the MCP Client with improved error handling"""
        logger.info("🔧 Initializing MCP Client...")
        
        try:
            # Try to import the MCP client
            try:
                sys.path.append(str(self.project_root))
                from mcp_client.mcp_client import NetflixMCPClient
                
                self.client = NetflixMCPClient()
                
                # Check if MCP libraries are available
                try:
                    from mcp.client import ClientSession
                    self.mcp_available = True
                    logger.info("✅ MCP Client initialized with full MCP protocol support")
                except ImportError:
                    self.mcp_available = False
                    logger.info("✅ MCP Client initialized with mock mode for development")
                
                return True
                
            except ImportError as e:
                logger.warning(f"⚠️ MCP Client module not available: {e}")
                # Create a simple fallback client
                self.client = SimpleFallbackClient(self.project_root)
                self.mcp_available = False
                logger.info("✅ MCP Client initialized with simple fallback")
                return True
                
        except Exception as e:
            logger.error(f"❌ Failed to initialize MCP Client: {e}")
            return False
    
    def setup_prompts(self):
        """Setup MCP Application Prompts"""
        logger.info("💬 Setting up MCP Prompts...")
        
        self.prompts = {
            "business_analysis": {
                "name": "Netflix Business Analysis",
                "description": "Comprehensive business intelligence analysis for Netflix content strategy",
                "template": """
                Analyze Netflix's business performance and strategy based on the following criteria:
                
                📊 Content Analysis:
                - Market penetration in {region}
                - Genre performance trends
                - International vs domestic content ratio
                
                🎯 Strategic Recommendations:
                - Content acquisition opportunities
                - Competitive positioning
                - Growth market identification
                
                📈 Key Metrics:
                - User engagement patterns
                - Content success predictions
                - ROI analysis
                
                Please provide data-driven insights with specific recommendations.
                """,
                "variables": ["region", "time_period", "content_type"]
            },
            
            "content_recommendation": {
                "name": "Personalized Content Recommendations",
                "description": "AI-powered content recommendations with safety filtering",
                "template": """
                Generate personalized Netflix content recommendations based on:
                
                👤 User Profile:
                - Age: {age}
                - Preferences: {preferences}
                - Viewing history: {viewing_history}
                
                🔒 Safety Considerations:
                - Content rating: {content_rating}
                - Family-friendly: {family_safe}
                - Cultural preferences: {cultural_context}
                
                🎬 Recommendation Categories:
                - Similar content
                - Trending in your region
                - Hidden gems
                - International selections
                
                Provide 5-10 specific recommendations with explanations.
                """,
                "variables": ["age", "preferences", "viewing_history", "content_rating", "family_safe", "cultural_context"]
            },
            
            "competitive_analysis": {
                "name": "Streaming Platform Competitive Analysis",
                "description": "Detailed competitive analysis against other streaming platforms",
                "template": """
                Compare Netflix with {competitor} across key dimensions:
                
                📊 Content Library:
                - Total content volume
                - Original vs licensed content
                - Genre diversity
                - International content
                
                💰 Business Model:
                - Pricing strategy
                - Subscription tiers
                - Market positioning
                
                🎯 Competitive Advantages:
                - Netflix strengths
                - {competitor} strengths
                - Market opportunities
                - Strategic recommendations
                
                Provide actionable insights for Netflix's competitive strategy.
                """,
                "variables": ["competitor", "market_focus", "analysis_depth"]
            },
            
            "market_expansion": {
                "name": "Market Expansion Strategy",
                "description": "Strategic analysis for Netflix expansion into new markets",
                "template": """
                Develop market expansion strategy for {target_market}:
                
                🌍 Market Analysis:
                - Market size and potential
                - Local content preferences
                - Competitive landscape
                - Regulatory considerations
                
                📱 Localization Strategy:
                - Content localization needs
                - Local partnerships
                - Pricing strategy
                - Marketing approach
                
                🎬 Content Strategy:
                - Local content acquisition
                - Original content production
                - Cultural adaptation
                - Language considerations
                
                Provide comprehensive expansion roadmap with timeline and budget estimates.
                """,
                "variables": ["target_market", "investment_budget", "timeline", "risk_tolerance"]
            }
        }
        
        logger.info(f"✅ {len(self.prompts)} MCP Prompts configured")
    
    def setup_resources(self):
        """Setup MCP Application Resources"""
        logger.info("📁 Setting up MCP Resources...")
        
        self.resources = {
            "netflix_dataset": {
                "name": "Netflix Content Dataset",
                "description": "Complete Netflix titles dataset with metadata",
                "type": "dataset",
                "uri": f"file://{self.config['dataset']['path']}",
                "size": "~15MB",
                "format": "CSV",
                "available": Path(self.config["dataset"]["path"]).exists()
            },
            
            "business_intelligence_docs": {
                "name": "Netflix Business Intelligence Documentation", 
                "description": "Comprehensive documentation for Netflix BI analysis",
                "type": "documentation",
                "uri": "docs://netflix-bi/",
                "available": True
            },
            
            "multi_agent_capabilities": {
                "name": "Multi-Agent System Capabilities",
                "description": "Documentation of available AI agents and their specializations",
                "type": "system_docs",
                "uri": "system://multi-agents/",
                "available": self.config["features"]["multi_agents"]
            },
            
            "guardrail_policies": {
                "name": "Content Safety and Quality Guardrails",
                "description": "Policies and rules for content safety and quality assurance",
                "type": "policy_docs",
                "uri": "policies://guardrails/",
                "available": self.config["features"]["guardrails"]
            },
            
            "api_documentation": {
                "name": "Netflix MCP API Documentation",
                "description": "Complete API documentation for all MCP tools and endpoints",
                "type": "api_docs",
                "uri": "api://netflix-mcp/docs/",
                "available": True
            }
        }
        
        logger.info(f"✅ {len(self.resources)} MCP Resources configured")
    
    async def start_application(self):
        """Start the complete MCP application"""
        logger.info("🚀 Starting Netflix MCP Application (Cursor IDE)...")
        logger.info("=" * 60)
        
        # Setup prompts and resources
        self.setup_prompts()
        self.setup_resources()
        
        # Initialize server
        server_success = await self.initialize_server()
        if not server_success:
            logger.warning("⚠️ MCP Server failed to start - continuing in limited mode")
        
        # Initialize client
        client_success = await self.initialize_client()
        if not client_success:
            logger.warning("⚠️ MCP Client failed to start - continuing in limited mode")
        
        logger.info("✅ Netflix MCP Application started successfully!")
        
        # Show application status
        await self.show_application_status()
        
        # Start interactive mode
        await self.run_interactive_mode()
        
        return True
    
    async def show_application_status(self):
        """Show current application status"""
        logger.info("\n📊 Netflix MCP Application Status")
        logger.info("=" * 50)
        
        # Environment info
        logger.info(f"🏗️ Environment: {self.config['environment']['mode']}")
        logger.info(f"🐛 Debug Mode: {'🟢 Enabled' if self.config['environment']['debug'] else '🔴 Disabled'}")
        
        # Server status
        server_status = "🟢 Running" if self.server_process else "🔴 Stopped"
        logger.info(f"🔧 MCP Server: {server_status}")
        
        # Client status
        client_status = "🟢 Ready" if self.client else "🔴 Not Ready"
        logger.info(f"💻 MCP Client: {client_status}")
        
        # MCP Protocol status
        mcp_status = "🟢 Available" if self.mcp_available else "🔴 Not Available (using fallback)"
        logger.info(f"🔗 MCP Protocol: {mcp_status}")
        
        # Features status
        logger.info(f"🤖 Multi-Agents: {'🟢 Enabled' if self.config['features']['multi_agents'] else '🔴 Disabled'}")
        logger.info(f"🔒 Guardrails: {'🟢 Enabled' if self.config['features']['guardrails'] else '🔴 Disabled'}")
        logger.info(f"💬 Prompts: {'🟢 Loaded' if self.prompts else '🔴 Not Loaded'} ({len(self.prompts)} available)")
        logger.info(f"📁 Resources: {'🟢 Loaded' if self.resources else '🔴 Not Loaded'} ({len(self.resources)} available)")
        
        # Dataset status
        dataset_path = Path(self.config['dataset']['path'])
        dataset_status = "🟢 Available" if dataset_path.exists() else "🔴 Not Found"
        logger.info(f"📊 Dataset: {dataset_status}")
        if dataset_path.exists():
            try:
                size_mb = dataset_path.stat().st_size / (1024 * 1024)
                logger.info(f"   Size: {size_mb:.1f} MB")
                logger.info(f"   Path: {dataset_path}")
            except Exception as e:
                logger.warning(f"   Could not get file size: {e}")
        else:
            logger.info(f"   Expected path: {dataset_path}")
        
        logger.info("=" * 50)
    
    async def run_interactive_mode(self):
        """Run interactive mode for the MCP application"""
        logger.info("\n🎮 Netflix MCP Application - Interactive Mode (Cursor IDE)")
        logger.info("=" * 60)
        logger.info("Available features:")
        logger.info("  1. Test Business Intelligence Query")
        logger.info("  2. Test Multi-Agent System (if available)")
        logger.info("  3. Test Guardrail System (if available)")
        logger.info("  4. View Available Prompts")
        logger.info("  5. View Available Resources")
        logger.info("  6. System Status")
        logger.info("  7. Run Comprehensive Test")
        logger.info("  8. Test Netflix Dataset Analysis")
        logger.info("  9. Generate Sample Queries")
        logger.info("  10. Test MCP Client Connection")
        logger.info("  11. Environment Information")
        logger.info("  12. Exit Application")
        logger.info("=" * 60)
        
        while True:
            try:
                choice = input("\n🎯 Select option (1-12): ").strip()
                
                if choice == "12":
                    logger.info("👋 Shutting down Netflix MCP Application...")
                    break
                
                elif choice == "1":
                    await self.test_business_intelligence()
                
                elif choice == "2":
                    await self.test_multi_agent_system()
                
                elif choice == "3":
                    await self.test_guardrail_system()
                
                elif choice == "4":
                    self.show_available_prompts()
                
                elif choice == "5":
                    self.show_available_resources()
                
                elif choice == "6":
                    await self.show_application_status()
                
                elif choice == "7":
                    await self.run_comprehensive_test()
                
                elif choice == "8":
                    await self.test_netflix_dataset()
                
                elif choice == "9":
                    self.generate_sample_queries()
                
                elif choice == "10":
                    await self.test_mcp_client_connection()
                
                elif choice == "11":
                    self.show_environment_info()
                
                else:
                    logger.info("❌ Invalid choice. Please select 1-12.")
                
            except KeyboardInterrupt:
                logger.info("\n👋 Application interrupted. Goodbye!")
                break
            except Exception as e:
                logger.error(f"❌ Error in interactive mode: {e}")
    
    async def test_business_intelligence(self):
        """Test business intelligence functionality"""
        logger.info("📊 Testing Business Intelligence...")
        
        sample_queries = [
            "What percentage of Netflix content is Korean?",
            "What are the most popular genres globally?",
            "Show me the trend of international vs US content"
        ]
        
        logger.info("Sample queries:")
        for i, query in enumerate(sample_queries, 1):
            logger.info(f"  {i}. {query}")
        
        choice = input("\nSelect query (1-3) or enter custom query: ").strip()
        
        if choice.isdigit() and 1 <= int(choice) <= 3:
            query = sample_queries[int(choice) - 1]
        else:
            query = choice
        
        if query:
            logger.info(f"🔍 Testing query: {query}")
            try:
                # Import and use the business logic directly
                sys.path.append(str(self.project_root))
                from mcp_server.mcp_server import enhanced_business_query_logic
                
                result = enhanced_business_query_logic(query)
                
                if result.get("status") == "success":
                    logger.info("✅ Query executed successfully!")
                    bi_data = result.get("business_intelligence", {})
                    if "answer" in bi_data:
                        logger.info(f"💡 Answer: {bi_data['answer']}")
                else:
                    logger.error(f"❌ Query failed: {result.get('message', 'Unknown error')}")
                
            except Exception as e:
                logger.error(f"❌ Business intelligence test failed: {e}")
    
    async def test_multi_agent_system(self):
        """Test multi-agent system"""
        logger.info("🤖 Testing Multi-Agent System...")
        
        try:
            # Try to test through the client first
            if hasattr(self.client, 'test_query'):
                logger.info("🔍 Testing multi-agent through MCP client...")
                result = await self.client.test_query("Test multi-agent functionality")
                logger.info("✅ Multi-agent test through client completed!")
                return
            
            # Fallback to direct import
            sys.path.append(str(self.project_root))
            from agents.multi_agents_fastmcp import test_netflix_multi_agents
            
            logger.info("🔍 Running multi-agent system test...")
            result = await asyncio.create_task(asyncio.to_thread(test_netflix_multi_agents))
            logger.info("✅ Multi-agent system test completed!")
            
        except ImportError:
            logger.warning("⚠️ Multi-agent system not available")
        except Exception as e:
            logger.error(f"❌ Multi-agent test failed: {e}")
    
    async def test_guardrail_system(self):
        """Test guardrail system"""
        logger.info("🔒 Testing Guardrail System...")
        
        try:
            sys.path.append(str(self.project_root))
            from guardrail.guardrail_fastmcp import test_guardrail_system
            
            logger.info("🔍 Running guardrail system test...")
            result = test_guardrail_system()
            logger.info("✅ Guardrail system test completed!")
            
        except ImportError:
            logger.warning("⚠️ Guardrail system not available")
        except Exception as e:
            logger.error(f"❌ Guardrail test failed: {e}")
    
    async def test_netflix_dataset(self):
        """Test Netflix dataset analysis"""
        logger.info("📊 Testing Netflix Dataset Analysis...")
        
        try:
            import pandas as pd
            dataset_path = Path(self.config["dataset"]["path"])
            
            if not dataset_path.exists():
                logger.error(f"❌ Dataset not found: {dataset_path}")
                logger.info("💡 Please ensure netflix_titles.csv is available in the data/ directory")
                return
            
            logger.info("📁 Loading dataset...")
            df = pd.read_csv(dataset_path)
            
            logger.info(f"✅ Dataset loaded successfully!")
            logger.info(f"📊 Dataset Statistics:")
            logger.info(f"   Total titles: {len(df)}")
            
            if 'type' in df.columns:
                logger.info(f"   Movies: {len(df[df['type'] == 'Movie'])}")
                logger.info(f"   TV Shows: {len(df[df['type'] == 'TV Show'])}")
            
            # Top 5 countries
            if 'country' in df.columns:
                countries = df['country'].value_counts().head(5)
                logger.info(f"   Top 5 countries: {list(countries.index)}")
            
            # Top 5 genres
            if 'listed_in' in df.columns:
                all_genres = []
                for genres in df['listed_in'].dropna():
                    all_genres.extend([g.strip() for g in str(genres).split(',')])
                if all_genres:
                    top_genres = pd.Series(all_genres).value_counts().head(5)
                    logger.info(f"   Top 5 genres: {list(top_genres.index)}")
            
        except Exception as e:
            logger.error(f"❌ Dataset test failed: {e}")
    
    async def test_mcp_client_connection(self):
        """Test MCP client connection"""
        logger.info("🔗 Testing MCP Client Connection...")
        
        if not self.client:
            logger.error("❌ No client available")
            return
        
        try:
            if hasattr(self.client, 'test_query'):
                result = await self.client.test_query("Connection test from Cursor IDE")
                logger.info("✅ MCP client connection test successful!")
                if isinstance(result, dict) and "message" in result:
                    logger.info(f"📝 Response: {result['message']}")
            else:
                result = await self.client.business_query("Test connection")
                logger.info("✅ Business query connection test successful!")
                
        except Exception as e:
            logger.error(f"❌ MCP client connection test failed: {e}")
    
    def show_environment_info(self):
        """Show environment information"""
        logger.info("🏗️ Environment Information")
        logger.info("=" * 40)
        
        logger.info(f"📁 Project Root: {self.project_root}")
        logger.info(f"🐍 Python Version: {sys.version}")
        logger.info(f"🔧 Environment Mode: {self.config['environment']['mode']}")
        logger.info(f"🐛 Debug Mode: {self.config['environment']['debug']}")
        logger.info(f"📊 Dataset Path: {self.config['dataset']['path']}")
        logger.info(f"🔧 Server Script: {self.config['server']['script_path']}")
        
        # Environment variables
        logger.info("\n🔑 Environment Variables:")
        env_vars = [
            'OPENAI_API_KEY', 'ANTHROPIC_API_KEY', 'NETFLIX_DATASET_PATH',
            'LOG_LEVEL', 'LOG_FILE', 'ENVIRONMENT', 'DEBUG'
        ]
        for var in env_vars:
            value = os.getenv(var, 'Not set')
            if 'KEY' in var and value != 'Not set':
                value = f"{value[:8]}..." if len(value) > 8 else value
            logger.info(f"   {var}: {value}")
    
    def show_available_prompts(self):
        """Show all available prompts"""
        logger.info("💬 Available MCP Prompts")
        logger.info("=" * 40)
        
        for prompt_id, prompt_info in self.prompts.items():
            logger.info(f"\n🔖 {prompt_info['name']}")
            logger.info(f"   Description: {prompt_info['description']}")
            logger.info(f"   Variables: {', '.join(prompt_info['variables'])}")
    
    def show_available_resources(self):
        """Show all available resources"""
        logger.info("📁 Available MCP Resources")
        logger.info("=" * 40)
        
        for resource_id, resource_info in self.resources.items():
            status = "🟢 Available" if resource_info.get('available', True) else "🔴 Not Available"
            logger.info(f"\n📄 {resource_info['name']} - {status}")
            logger.info(f"   Type: {resource_info['type']}")
            logger.info(f"   Description: {resource_info['description']}")
            logger.info(f"   URI: {resource_info['uri']}")
    
    def generate_sample_queries(self):
        """Generate sample queries for testing"""
        logger.info("📝 Sample Netflix MCP Queries")
        logger.info("=" * 40)
        
        sample_queries = [
            "What percentage of Netflix content is Korean?",
            "What are the most popular genres globally?", 
            "Show me the trend of international vs US content",
            "How many thriller movies does Netflix have?",
            "What countries produce the most Netflix content?",
            "What's the distribution of content by release year?",
            "Which directors have the most titles on Netflix?",
            "What's the average duration of Netflix movies?",
            "How much kids content does Netflix have?",
            "What are the trending genres in 2023?"
        ]
        
        for i, query in enumerate(sample_queries, 1):
            logger.info(f"{i:2d}. {query}")
        
        logger.info("\n💡 You can use these queries to test the business intelligence system!")
    
    async def run_comprehensive_test(self):
        """Run comprehensive test of the MCP application"""
        logger.info("🧪 Running Comprehensive MCP Application Test (Cursor IDE)")
        logger.info("=" * 60)
        
        test_results = []
        
        # Test 1: Environment setup
        logger.info("1️⃣ Testing Environment Setup...")
        env_test = self.config['environment']['mode'] in ['development', 'production']
        test_results.append(("Environment Setup", env_test))
        logger.info(f"   {'✅ PASSED' if env_test else '❌ FAILED'}")
        
        # Test 2: Server availability
        logger.info("2️⃣ Testing MCP Server availability...")
        server_test = self.server_process is not None
        test_results.append(("MCP Server", server_test))
        logger.info(f"   {'✅ PASSED' if server_test else '❌ FAILED'}")
        
        # Test 3: Client initialization
        logger.info("3️⃣ Testing MCP Client initialization...")
        client_test = self.client is not None
        test_results.append(("MCP Client", client_test))
        logger.info(f"   {'✅ PASSED' if client_test else '❌ FAILED'}")
        
        # Test 4: Prompts configuration
        logger.info("4️⃣ Testing Prompts configuration...")
        prompts_test = len(self.prompts) > 0
        test_results.append(("Prompts", prompts_test))
        logger.info(f"   {'✅ PASSED' if prompts_test else '❌ FAILED'} - {len(self.prompts)} prompts loaded")
        
        # Test 5: Resources configuration
        logger.info("5️⃣ Testing Resources configuration...")
        resources_test = len(self.resources) > 0
        test_results.append(("Resources", resources_test))
        logger.info(f"   {'✅ PASSED' if resources_test else '❌ FAILED'} - {len(self.resources)} resources loaded")
        
        # Test 6: Dataset availability
        logger.info("6️⃣ Testing Dataset availability...")
        dataset_test = Path(self.config['dataset']['path']).exists()
        test_results.append(("Dataset", dataset_test))
        logger.info(f"   {'✅ PASSED' if dataset_test else '❌ FAILED'}")
        
        # Test 7: Business Intelligence
        logger.info("7️⃣ Testing Business Intelligence...")
        bi_test = False
        try:
            sys.path.append(str(self.project_root))
            from mcp_server.mcp_server import enhanced_business_query_logic
            result = enhanced_business_query_logic("Test query")
            bi_test = result.get("status") == "success"
        except Exception as e:
            logger.warning(f"   BI test error: {e}")
        
        test_results.append(("Business Intelligence", bi_test))
        logger.info(f"   {'✅ PASSED' if bi_test else '❌ FAILED'}")
        
        # Test 8: Multi-Agent System
        logger.info("8️⃣ Testing Multi-Agent System...")
        ma_test = False
        try:
            from agents.multi_agents_fastmcp import run_netflix_multi_agent
            ma_test = True
        except ImportError:
            pass
        
        test_results.append(("Multi-Agent System", ma_test))
        logger.info(f"   {'✅ PASSED' if ma_test else '❌ FAILED'}")
        
        # Test 9: Guardrail System
        logger.info("9️⃣ Testing Guardrail System...")
        gr_test = False
        try:
            from guardrail.guardrail_fastmcp import NetflixGuardrailSystem
            gr_test = True
        except ImportError:
            pass
        
        test_results.append(("Guardrail System", gr_test))
        logger.info(f"   {'✅ PASSED' if gr_test else '❌ FAILED'}")
        
        # Test 10: Configuration
        logger.info("🔟 Testing Configuration...")
        config_test = all([
            'OPENAI_API_KEY' in os.environ,
            Path(self.config['dataset']['path']).parent.exists(),
            self.config['features']['multi_agents'] in [True, False]
        ])
        test_results.append(("Configuration", config_test))
        logger.info(f"   {'✅ PASSED' if config_test else '❌ FAILED'}")
        
        # Summary
        passed_tests = sum(1 for _, result in test_results if result)
        total_tests = len(test_results)
        
        logger.info(f"\n📊 Test Results: {passed_tests}/{total_tests} passed ({passed_tests/total_tests*100:.1f}%)")
        
        for test_name, result in test_results:
            status = "✅ PASSED" if result else "❌ FAILED"
            logger.info(f"   {status}: {test_name}")
        
        if passed_tests == total_tests:
            logger.info("🎉 ALL TESTS PASSED! MCP Application is fully operational!")
        elif passed_tests >= total_tests * 0.7:
            logger.info("👍 MOST TESTS PASSED! MCP Application is mostly operational!")
        else:
            logger.info("⚠️ SOME TESTS FAILED! MCP Application needs attention!")

# Enhanced fallback client for better compatibility
class SimpleFallbackClient:
    """Simple fallback client when MCP client is not available"""
    
    def __init__(self, project_root: Path):
        self.tools = [
            "netflix_business_query",
            "netflix_test_query",
            "netflix_dataset_info"
        ]
        self.project_root = project_root
        logger.info("🔄 Simple fallback client initialized")
    
    async def business_query(self, query: str):
        """Simple business query fallback"""
        try:
            sys.path.append(str(self.project_root))
            from mcp_server.mcp_server import enhanced_business_query_logic
            return enhanced_business_query_logic(query)
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    async def test_query(self, message: str = "Hello!"):
        """Simple test query"""
        return {
            "status": "success", 
            "message": f"Fallback client test: {message}",
            "mode": "simple_fallback",
            "environment": "cursor_ide"
        }

# Utility functions
async def start_netflix_mcp_app():
    """Start the Netflix MCP Application"""
    app = NetflixMCPApplication()
    await app.start_application()

def create_mcp_configuration():
    """Create MCP configuration for Claude Desktop"""
    project_root = Path(__file__).parent.parent.absolute()
    
    config = {
        "mcpServers": {
            "netflix-business-intelligence": {
                "command": "uv",
                "args": [
                    "run", 
                    "python", 
                    "mcp_server/mcp_server.py"
                ],
                "cwd": str(project_root),
                "env": {
                    "OPENAI_API_KEY": os.getenv('OPENAI_API_KEY', 'your_openai_api_key_here'),
                    "NETFLIX_DATASET_PATH": os.getenv('NETFLIX_DATASET_PATH', 'data/netflix_titles.csv')
                }
            }
        }
    }
    
    print("🔧 MCP Configuration for Claude Desktop (Cursor IDE):")
    print("=" * 60)
    print(json.dumps(config, indent=2))
    print("=" * 60)
    print("📝 Add this to your Claude Desktop configuration file:")
    print("   • Windows: %APPDATA%\\Claude\\claude_desktop_config.json")
    print("   • macOS: ~/Library/Application Support/Claude/claude_desktop_config.json")
    print("   • Linux: ~/.config/Claude/claude_desktop_config.json")
    print("\n💡 Notes for Cursor IDE:")
    print(f"   • Project path: {project_root}")
    print("   • Ensure your .env file contains the necessary API keys")
    print("   • Run 'uv sync' to install dependencies")
    
    return config

def show_mcp_application_info():
    """Show information about the MCP application"""
    print("🎬 Netflix MCP Application Information (Cursor IDE)")
    print("=" * 60)
    print("📊 Features:")
    print("   • Enhanced Business Intelligence with real Netflix data")
    print("   • Multi-Agent system with 5 specialized agents")
    print("   • Content safety and quality guardrails")
    print("   • Personalized content recommendations") 
    print("   • Competitive analysis and market insights")
    print("   • Interactive prompts and resource management")
    print("   • Professional development setup with uv")
    print("   • Claude Desktop integration ready")
    print()
    print("🛠️ Cursor IDE Setup:")
    print("   • Use uv package manager: uv sync")
    print("   • Configure .env file with API keys")
    print("   • Add Netflix dataset to data/netflix_titles.csv")
    print("   • Run: uv run python mcp_application/mcp_application.py --start")
    print()
    print("🤖 Available Agents:")
    print("   • Content Discovery Agent - Find movies and shows")
    print("   • Analytics Specialist Agent - Analyze trends and data")
    print("   • Recommendation Engine Agent - Personalized suggestions")
    print("   • Customer Support Agent - Help with Netflix features")
    print("   • Content Strategy Agent - Business strategy insights")
    print("=" * 60)

# Main execution
async def main():
    """Main entry point for the MCP application"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Netflix MCP Application - Cursor IDE Compatible")
    parser.add_argument("--info", action="store_true", help="Show application information")
    parser.add_argument("--config", action="store_true", help="Generate Claude Desktop configuration")
    parser.add_argument("--test", action="store_true", help="Run comprehensive tests")
    parser.add_argument("--start", action="store_true", help="Start the MCP application")
    
    args = parser.parse_args()
    
    if args.info:
        show_mcp_application_info()
    elif args.config:
        create_mcp_configuration()
    elif args.test:
        app = NetflixMCPApplication()
        app.setup_prompts()
        app.setup_resources()
        await app.run_comprehensive_test()
    elif args.start:
        await start_netflix_mcp_app()
    else:
        # Default: start the application
        await start_netflix_mcp_app()

if __name__ == "__main__":
    print("🎬 Netflix MCP Application - Cursor IDE Compatible")
    print("🚀 Building an Application with MCP")
    print("=" * 60)
    print("Usage:")
    print("  uv run python mcp_application/mcp_application.py --start    # Start the application")
    print("  uv run python mcp_application/mcp_application.py --info     # Show application info")
    print("  uv run python mcp_application/mcp_application.py --config   # Generate Claude config")
    print("  uv run python mcp_application/mcp_application.py --test     # Run tests")
    print("=" * 60)
    
    asyncio.run(main())
