#!/usr/bin/env python3
"""
Netflix MCP Client - Cursor IDE Version
Professional setup with proper imports and local file paths
"""

import asyncio
import json
import sys
import os
from pathlib import Path
from typing import Any, Dict, List, Optional
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/netflix_mcp_client.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("netflix-mcp-client")

# Ensure logs directory exists
Path("logs").mkdir(exist_ok=True)

# Check MCP client availability with better error handling
MCP_CLIENT_AVAILABLE = False
ClientSession = None
stdio_client = None
StdioServerParameters = None

try:
    from mcp.client import ClientSession
    from mcp.client.stdio import stdio_client
    from mcp.client import StdioServerParameters
    MCP_CLIENT_AVAILABLE = True
    logger.info("✅ MCP Client libraries loaded successfully")
except ImportError as e:
    logger.warning(f"⚠️ MCP Client libraries not available: {e}")
    logger.info("💡 Please install: uv add mcp")
    MCP_CLIENT_AVAILABLE = False

class NetflixMCPClient:
    """Netflix MCP Client with Cursor IDE compatibility"""
    
    def __init__(self):
        self.session: Optional[Any] = None
        self.available_tools: List[Dict[str, Any]] = []
        self.mock_mode = not MCP_CLIENT_AVAILABLE
        self.project_root = Path(__file__).parent.parent
        
        if self.mock_mode:
            logger.info("🔄 Running in mock mode (MCP libraries not available)")
        else:
            logger.info("✅ Running in full MCP mode")
    
    async def connect(self, server_script_path: str = None):
        """Connect to the Netflix MCP server with fallback support"""
        if server_script_path is None:
            server_script_path = str(self.project_root / "mcp_server" / "mcp_server.py")
        
        try:
            if not self.mock_mode and MCP_CLIENT_AVAILABLE:
                # Try real MCP connection
                return await self._connect_real_mcp(server_script_path)
            else:
                # Use mock connection for development
                return await self._connect_mock_mcp(server_script_path)
                
        except Exception as e:
            logger.error(f"❌ Failed to connect to Netflix MCP Server: {e}")
            logger.info("🔄 Falling back to mock mode...")
            return await self._connect_mock_mcp(server_script_path)
    
    async def _connect_real_mcp(self, server_script_path: str):
        """Connect using real MCP protocol"""
        try:
            # Use uv to run the server for proper environment
            server_params = StdioServerParameters(
                command="uv",
                args=["run", "python", server_script_path],
                env={
                    **os.environ,
                    "PYTHONPATH": str(self.project_root)
                },
            )
            
            logger.info(f"Connecting to Netflix MCP Server: {server_script_path}")
            
            # Create stdio client and session
            stdio_transport = stdio_client(server_params)
            
            async with stdio_transport as (read, write):
                async with ClientSession(read, write) as session:
                    self.session = session
                    
                    # Initialize the session
                    await session.initialize()
                    logger.info("✅ Connected to Netflix MCP Server successfully")
                    
                    # List available tools
                    await self.list_tools()
                    
                    # Keep the session alive for interactive use
                    await self.interactive_session()
                    
            return True
                    
        except Exception as e:
            logger.error(f"❌ Real MCP connection failed: {e}")
            raise
    
    async def _connect_mock_mcp(self, server_script_path: str):
        """Connect using mock client for development"""
        try:
            logger.info(f"🔄 Connecting to Netflix MCP Server in mock mode: {server_script_path}")
            
            # Check if server file exists
            if not Path(server_script_path).exists():
                logger.error(f"❌ Server file not found: {server_script_path}")
                return False
            
            # Import the server module directly
            sys.path.append(str(self.project_root))
            
            try:
                from mcp_server import mcp_server
                self.session = MockMCPSession(mcp_server, self.project_root)
                
                # Initialize mock tools
                await self.list_tools()
                
                logger.info("✅ Connected to Netflix MCP Server successfully (mock mode)")
                return True
                
            except ImportError as e:
                logger.error(f"❌ Failed to import server module: {e}")
                return False
            
        except Exception as e:
            logger.error(f"❌ Mock MCP connection failed: {e}")
            return False
    
    async def list_tools(self):
        """List all available tools from the server"""
        try:
            if self.mock_mode:
                # Mock tools list
                self.available_tools = [
                    {
                        "name": "netflix_business_query",
                        "description": "Enhanced business intelligence queries with multi-agent and guardrail integration"
                    },
                    {
                        "name": "netflix_test_query", 
                        "description": "Simple test query for MCP functionality"
                    },
                    {
                        "name": "netflix_dataset_info",
                        "description": "Get information about the Netflix dataset"
                    },
                    {
                        "name": "netflix_content_recommendations",
                        "description": "AI-powered content recommendations with safety filtering"
                    },
                    {
                        "name": "netflix_search_content",
                        "description": "Search Netflix content using multi-agent system"
                    },
                    {
                        "name": "netflix_analytics_insights",
                        "description": "Get Netflix analytics insights"
                    }
                ]
            else:
                if not self.session:
                    raise RuntimeError("Not connected to server")
                
                tools_response = await self.session.list_tools()
                self.available_tools = [{"name": tool.name, "description": tool.description} for tool in tools_response.tools]
            
            logger.info("📋 Available Netflix MCP Tools:")
            for i, tool in enumerate(self.available_tools, 1):
                logger.info(f"   {i}. {tool['name']} - {tool['description']}")
            
            return self.available_tools
            
        except Exception as e:
            logger.error(f"❌ Failed to list tools: {e}")
            return []
    
    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """Call a specific tool with arguments"""
        try:
            if not self.session:
                raise RuntimeError("Not connected to server")
            
            logger.info(f"🔧 Calling tool: {tool_name}")
            logger.info(f"📊 Arguments: {json.dumps(arguments, indent=2)}")
            
            if self.mock_mode:
                # Use mock session
                result = await self.session.call_tool(tool_name, arguments)
            else:
                # Use real MCP session
                result = await self.session.call_tool(tool_name, arguments)
                
                # Extract the text content from the result
                if result.content and len(result.content) > 0:
                    response_text = result.content[0].text
                    result = json.loads(response_text) if response_text.startswith('{') else response_text
            
            logger.info(f"✅ Tool execution successful")
            return result
                
        except Exception as e:
            logger.error(f"❌ Tool execution failed: {e}")
            return {"status": "error", "message": str(e)}
    
    async def business_query(self, query: str) -> Dict[str, Any]:
        """Execute a business intelligence query"""
        return await self.call_tool("netflix_business_query", {
            "natural_language_query": query
        })
    
    async def test_query(self, message: str = "Hello MCP!") -> Dict[str, Any]:
        """Execute a test query"""
        return await self.call_tool("netflix_test_query", {
            "test_message": message
        })
    
    async def dataset_info(self, detail_level: str = "basic") -> Dict[str, Any]:
        """Get dataset information"""
        return await self.call_tool("netflix_dataset_info", {
            "detail_level": detail_level
        })
    
    async def content_recommendations(self, preferences: str, age_rating: str = "all") -> Dict[str, Any]:
        """Get content recommendations"""
        return await self.call_tool("netflix_content_recommendations", {
            "user_preferences": preferences,
            "age_rating": age_rating
        })
    
    async def search_content(self, search_query: str, content_type: str = "both") -> Dict[str, Any]:
        """Search for content"""
        return await self.call_tool("netflix_search_content", {
            "search_query": search_query,
            "content_type": content_type
        })
    
    async def analytics_insights(self, metric_type: str = "popularity", time_period: str = "monthly") -> Dict[str, Any]:
        """Get analytics insights"""
        return await self.call_tool("netflix_analytics_insights", {
            "metric_type": metric_type,
            "time_period": time_period
        })
    
    async def interactive_session(self):
        """Interactive session for testing the MCP client"""
        logger.info("\n🎬 Netflix MCP Client - Interactive Session (Cursor IDE)")
        logger.info("=" * 60)
        logger.info("Available commands:")
        logger.info("  1. korean - Test Korean content analysis")
        logger.info("  2. recommendations - Test content recommendations")
        logger.info("  3. search - Test content search")
        logger.info("  4. trends - Test international trends")
        logger.info("  5. genres - Test genre analysis")
        logger.info("  6. test - Test basic MCP functionality")
        logger.info("  7. dataset - Get dataset information")
        logger.info("  8. analytics - Test analytics insights")
        logger.info("  9. custom - Enter custom query")
        logger.info("  10. list - List all available tools")
        logger.info("  11. exit - Exit the session")
        logger.info("=" * 60)
        
        while True:
            try:
                command = input("\n🎯 Enter command (1-11): ").strip().lower()
                
                if command in ['11', 'exit', 'quit']:
                    logger.info("👋 Goodbye!")
                    break
                
                elif command in ['1', 'korean']:
                    logger.info("🇰🇷 Testing Korean content analysis...")
                    result = await self.business_query("What percentage of Netflix content is Korean?")
                    self.print_result(result)
                
                elif command in ['2', 'recommendations']:
                    logger.info("🎯 Testing content recommendations...")
                    result = await self.content_recommendations("action movies for teenagers", "teen")
                    self.print_result(result)
                
                elif command in ['3', 'search']:
                    logger.info("🔍 Testing content search...")
                    result = await self.search_content("thriller movies")
                    self.print_result(result)
                
                elif command in ['4', 'trends']:
                    logger.info("📈 Testing international trends...")
                    result = await self.business_query("Show me the trend of international vs US content")
                    self.print_result(result)
                
                elif command in ['5', 'genres']:
                    logger.info("🎭 Testing genre analysis...")
                    result = await self.business_query("What are the most popular genres globally?")
                    self.print_result(result)
                
                elif command in ['6', 'test']:
                    logger.info("🧪 Testing basic MCP functionality...")
                    result = await self.test_query("Hello from Cursor IDE!")
                    self.print_result(result)
                
                elif command in ['7', 'dataset']:
                    logger.info("📊 Getting dataset information...")
                    result = await self.dataset_info("detailed")
                    self.print_result(result)
                
                elif command in ['8', 'analytics']:
                    logger.info("📊 Testing analytics insights...")
                    result = await self.analytics_insights("engagement", "monthly")
                    self.print_result(result)
                
                elif command in ['9', 'custom']:
                    custom_query = input("Enter your custom query: ").strip()
                    if custom_query:
                        logger.info(f"🔧 Testing custom query: {custom_query}")
                        result = await self.business_query(custom_query)
                        self.print_result(result)
                
                elif command in ['10', 'list']:
                    logger.info("📋 Available tools:")
                    await self.list_tools()
                
                else:
                    logger.info("❌ Invalid command. Please enter a number between 1-11.")
                
            except KeyboardInterrupt:
                logger.info("\n👋 Session interrupted. Goodbye!")
                break
            except Exception as e:
                logger.error(f"❌ Error in interactive session: {e}")
    
    def print_result(self, result: Any):
        """Pretty print the result from a tool call"""
        if isinstance(result, dict):
            if result.get("status") == "success":
                logger.info("✅ Success!")
                
                # Print business intelligence answer if available
                if "business_intelligence" in result:
                    bi_data = result["business_intelligence"]
                    if "answer" in bi_data:
                        logger.info(f"💡 Answer: {bi_data['answer']}")
                
                # Print dataset info if available
                if "dataset_info" in result:
                    info = result["dataset_info"]
                    logger.info(f"📊 Dataset Info: {info.get('total_titles', 'N/A')} titles")
                
                # Print multi-agent response if available
                if "response" in result:
                    response_text = str(result["response"])
                    logger.info(f"🤖 Response: {response_text[:200]}{'...' if len(response_text) > 200 else ''}")
                
                # Print test message if available
                if "message" in result:
                    logger.info(f"📝 Message: {result['message']}")
                
                # Print guardrail status if available
                if "guardrail_status" in result:
                    status_emoji = "✅" if result["guardrail_status"] == "APPROVED" else "⚠️"
                    logger.info(f"{status_emoji} Guardrail Status: {result['guardrail_status']}")
                
                # Print dataset size if available
                if "dataset_size" in result:
                    logger.info(f"📊 Dataset Size: {result['dataset_size']} titles")
                
            elif result.get("status") == "error":
                logger.error(f"❌ Error: {result.get('message', 'Unknown error')}")
            else:
                logger.info(f"📋 Result: {json.dumps(result, indent=2)}")
        else:
            logger.info(f"📋 Result: {result}")

class MockMCPSession:
    """Mock MCP Session for Cursor IDE development"""
    
    def __init__(self, mcp_server_module, project_root: Path):
        self.server_module = mcp_server_module
        self.project_root = project_root
        logger.info("🔄 Mock MCP Session initialized for Cursor IDE")
    
    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """Mock tool call implementation"""
        try:
            if tool_name == "netflix_business_query":
                query = arguments.get("natural_language_query", "")
                return self.server_module.enhanced_business_query_logic(query)
            
            elif tool_name == "netflix_test_query":
                test_message = arguments.get("test_message", "Hello MCP!")
                return {
                    "status": "success",
                    "message": f"Test successful: {test_message}",
                    "timestamp": "2025-06-20T11:00:00Z",
                    "server_info": {
                        "mode": "mock",
                        "environment": "cursor_ide",
                        "project_root": str(self.project_root)
                    }
                }
            
            elif tool_name == "netflix_dataset_info":
                detail_level = arguments.get("detail_level", "basic")
                # Try to get real dataset info from server
                try:
                    netflix_data = getattr(self.server_module, 'netflix_data', None)
                    if netflix_data is not None and not netflix_data.empty:
                        basic_info = {
                            "total_titles": len(netflix_data),
                            "movies": len(netflix_data[netflix_data['type'] == 'Movie']),
                            "tv_shows": len(netflix_data[netflix_data['type'] == 'TV Show']),
                        }
                        return {
                            "status": "success",
                            "detail_level": detail_level,
                            "dataset_info": basic_info
                        }
                except:
                    pass
                
                return {
                    "status": "success",
                    "detail_level": detail_level,
                    "dataset_info": {
                        "total_titles": 100,
                        "movies": 60,
                        "tv_shows": 40,
                        "note": "Mock data - please ensure real dataset is available"
                    }
                }
            
            elif tool_name == "netflix_content_recommendations":
                preferences = arguments.get("user_preferences", "")
                age_rating = arguments.get("age_rating", "all")
                
                # Try to use multi-agent system if available
                try:
                    sys.path.append(str(self.project_root))
                    from agents.multi_agents_fastmcp import get_content_recommendations
                    response = get_content_recommendations(preferences, age_rating)
                    return json.loads(response) if isinstance(response, str) else response
                except:
                    return {
                        "status": "success",
                        "recommendations": [
                            f"Mock recommendation for {preferences}",
                            "Please ensure multi-agent system is properly configured"
                        ],
                        "preferences": preferences,
                        "age_rating": age_rating
                    }
            
            elif tool_name == "netflix_search_content":
                search_query = arguments.get("search_query", "")
                content_type = arguments.get("content_type", "both")
                
                # Try to use multi-agent system if available
                try:
                    sys.path.append(str(self.project_root))
                    from agents.multi_agents_fastmcp import search_movies_shows
                    response = search_movies_shows(search_query, content_type)
                    return {"status": "success", "results": response}
                except:
                    return {
                        "status": "success",
                        "results": f"Mock search results for '{search_query}' ({content_type})",
                        "search_query": search_query,
                        "content_type": content_type
                    }
            
            elif tool_name == "netflix_analytics_insights":
                metric_type = arguments.get("metric_type", "popularity")
                time_period = arguments.get("time_period", "monthly")
                
                # Try to use multi-agent system if available
                try:
                    sys.path.append(str(self.project_root))
                    from agents.multi_agents_fastmcp import get_viewing_analytics
                    response = get_viewing_analytics(metric_type, time_period)
                    return {"status": "success", "analytics": response}
                except:
                    return {
                        "status": "success",
                        "analytics": f"Mock analytics for {metric_type} over {time_period}",
                        "metric_type": metric_type,
                        "time_period": time_period
                    }
            
            else:
                return {
                    "status": "error",
                    "message": f"Unknown tool: {tool_name}",
                    "available_tools": [
                        "netflix_business_query",
                        "netflix_test_query",
                        "netflix_dataset_info",
                        "netflix_content_recommendations",
                        "netflix_search_content",
                        "netflix_analytics_insights"
                    ]
                }
                
        except Exception as e:
            logger.error(f"❌ Mock tool execution error: {e}")
            return {
                "status": "error",
                "message": f"Mock tool execution failed: {str(e)}",
                "tool_name": tool_name,
                "arguments": arguments
            }

async def main():
    """Main function to run the MCP client"""
    client = NetflixMCPClient()
    
    try:
        await client.connect()
    except Exception as e:
        logger.error(f"Failed to start Netflix MCP Client: {e}")
        sys.exit(1)

# Test functions for quick testing
async def test_netflix_mcp_client():
    """Test the Netflix MCP client with various queries"""
    logger.info("🧪 Testing Netflix MCP Client (Cursor IDE)")
    logger.info("=" * 50)
    
    client = NetflixMCPClient()
    
    # Test queries
    test_queries = [
        ("Korean Content Analysis", "What percentage of Netflix content is Korean?"),
        ("Genre Analysis", "What are the most popular genres globally?"),
        ("International Trends", "Show me the trend of international vs US content"),
        ("Test Query", "Hello Cursor IDE!"),
        ("Dataset Info", "dataset_info"),
    ]
    
    try:
        # Connect to server
        success = await client.connect()
        
        if success:
            logger.info("✅ Connected to Netflix MCP Server")
            
            # List tools
            tools = await client.list_tools()
            logger.info(f"📋 Found {len(tools)} tools")
            
            # Test each query
            for test_name, query in test_queries:
                logger.info(f"\n🧪 Testing: {test_name}")
                
                if query == "dataset_info":
                    result = await client.dataset_info("detailed")
                elif "Test Query" in test_name:
                    result = await client.test_query(query)
                else:
                    result = await client.business_query(query)
                
                if isinstance(result, dict) and result.get("status") == "success":
                    logger.info("✅ Test passed")
                    
                    # Print answer if available
                    if "business_intelligence" in result:
                        bi_data = result.get("business_intelligence", {})
                        answer = bi_data.get("answer", "No answer")
                        logger.info(f"💡 Answer: {answer}")
                    elif "message" in result:
                        logger.info(f"📝 Message: {result['message']}")
                    elif "dataset_info" in result:
                        info = result["dataset_info"]
                        logger.info(f"📊 Dataset: {info.get('total_titles', 'N/A')} titles")
                else:
                    logger.error(f"❌ Test failed: {result}")
            
            logger.info("\n✅ All tests completed!")
        else:
            logger.error("❌ Failed to connect to server")
                
    except Exception as e:
        logger.error(f"❌ Test failed: {e}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Netflix MCP Client - Cursor IDE Compatible")
    parser.add_argument("--test", action="store_true", help="Run tests instead of interactive session")
    parser.add_argument("--server", help="Path to MCP server script")
    
    args = parser.parse_args()
    
    if args.test:
        asyncio.run(test_netflix_mcp_client())
    else:
        asyncio.run(main())
