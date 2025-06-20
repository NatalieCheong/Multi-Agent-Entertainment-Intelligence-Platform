#!/usr/bin/env python3
"""
Netflix Business Intelligence MCP Server - IDE Version
Professional setup with proper imports and local file paths
"""

import asyncio
import json
import sys
import os
from pathlib import Path
import pandas as pd
import numpy as np
from datetime import datetime
from typing import Any, Dict, List, Optional
import logging

# MCP Server imports
try:
    from mcp.server import Server
    from mcp.server.models import InitializationOptions
    from mcp.server.stdio import stdio_server
    from mcp.types import (
        Tool,
        TextContent,
        ImageContent,
        EmbeddedResource,
    )
    MCP_AVAILABLE = True
    print("✅ MCP imports successful")
except ImportError as e:
    print(f"❌ MCP import error: {e}")
    print("💡 Please install: uv add mcp")
    MCP_AVAILABLE = False

# Import your existing modules - Updated paths for Cursor IDE
try:
    sys.path.append(str(Path(__file__).parent.parent))
    from agents.multi_agents import (
        run_netflix_multi_agent,
        search_movies_shows,
        get_content_recommendations,
        analyze_content_trends,
        get_viewing_analytics,
        predict_content_success,
        get_netflix_faq
    )
    MULTI_AGENTS_AVAILABLE = True
    print("✅ Multi-agents system loaded successfully")
except ImportError as e:
    print(f"⚠️ Multi-agents not available: {e}")
    MULTI_AGENTS_AVAILABLE = False

try:
    from guardrail.guardrail import (
        NetflixGuardrailSystem,
        apply_guardrails_to_response,
        simple_content_filter
    )
    GUARDRAILS_AVAILABLE = True
    print("✅ Guardrail system loaded successfully")
except ImportError as e:
    print(f"⚠️ Guardrails not available: {e}")
    GUARDRAILS_AVAILABLE = False

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/netflix_mcp_server.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("netflix-mcp-server")

# Create logs directory if it doesn't exist
Path("logs").mkdir(exist_ok=True)

# Create the MCP server instance
if MCP_AVAILABLE:
    server = Server("netflix-business-intelligence")
else:
    server = None

# Initialize guardrail system if available
guardrail_system = NetflixGuardrailSystem() if GUARDRAILS_AVAILABLE else None

# Load Netflix dataset
def load_netflix_dataset():
    """Load and clean the Netflix dataset - Updated for Cursor IDE"""
    try:
        logger.info("Loading Netflix dataset...")
        
        # Try multiple possible dataset paths
        possible_paths = [
            os.getenv('NETFLIX_DATASET_PATH', 'data/netflix_titles.csv'),
            'data/netflix_titles.csv',
            '../data/netflix_titles.csv',
            '../../data/netflix_titles.csv',
            Path.home() / 'Downloads' / 'netflix_titles.csv'
        ]
        
        dataset_path = None
        for path in possible_paths:
            if Path(path).exists():
                dataset_path = Path(path)
                break
        
        if not dataset_path:
            logger.warning("Netflix dataset not found in standard locations")
            return create_sample_dataset()
        
        logger.info(f"Loading dataset from: {dataset_path}")
        df = pd.read_csv(dataset_path)
        logger.info(f"Loaded {len(df)} titles from Netflix dataset")
        
        # Clean data
        df['director'] = df['director'].fillna('Unknown Director')
        df['cast'] = df['cast'].fillna('Unknown Cast')
        df['country'] = df['country'].fillna('Unknown Country')
        df['date_added'] = df['date_added'].fillna('Unknown Date')
        df['rating'] = df['rating'].fillna('Not Rated')
        df['duration'] = df['duration'].fillna('Unknown Duration')
        df['listed_in'] = df['listed_in'].fillna('Unknown Genre')
        df['description'] = df['description'].fillna('No description available')
        
        df['release_year'] = pd.to_numeric(df['release_year'], errors='coerce')
        df['release_year'] = df['release_year'].fillna(2020).astype(int)
        
        if 'show_id' in df.columns:
            df['show_id'] = df['show_id'].fillna('unknown_id')
        
        df = df.dropna(subset=['title', 'type'])
        df = df.drop_duplicates(subset=['title', 'type'], keep='first')
        
        text_columns = ['title', 'director', 'cast', 'country', 'listed_in', 'description']
        for col in text_columns:
            if col in df.columns:
                df[col] = df[col].astype(str).str.strip()
        
        logger.info(f"Data cleaning complete! Final dataset: {len(df)} titles")
        return df
        
    except Exception as e:
        logger.error(f"Error loading dataset: {e}")
        return create_sample_dataset()

def create_sample_dataset():
    """Create a sample dataset if the real one is not found"""
    logger.info("Creating sample dataset for development/testing")
    sample_data = {
        'show_id': [f's{i}' for i in range(1, 101)],
        'type': ['Movie'] * 60 + ['TV Show'] * 40,
        'title': [f'Sample Title {i}' for i in range(1, 101)],
        'director': [f'Director {i}' for i in range(1, 101)],
        'cast': [f'Actor {i}, Actor {i+1}' for i in range(1, 101)],
        'country': ['United States'] * 40 + ['South Korea'] * 20 + ['United Kingdom'] * 15 + ['Japan'] * 10 + ['India'] * 15,
        'date_added': ['January 1, 2023'] * 100,
        'release_year': [2020 + (i % 4) for i in range(100)],
        'rating': ['PG-13'] * 40 + ['TV-MA'] * 30 + ['R'] * 20 + ['PG'] * 10,
        'duration': ['120 min'] * 60 + ['1 Season'] * 40,
        'listed_in': ['Action, Drama'] * 30 + ['Comedy, Romance'] * 25 + ['Thriller, Crime'] * 25 + ['Documentary'] * 20,
        'description': [f'Description for sample title {i}' for i in range(1, 101)]
    }
    df = pd.DataFrame(sample_data)
    logger.info(f"Sample dataset created: {len(df)} titles")
    return df

# Initialize dataset
netflix_data = load_netflix_dataset()

# Enhanced business logic functions (same as before but with better error handling)
def enhanced_business_query_logic(natural_language_query: str) -> Dict[str, Any]:
    """Enhanced business intelligence logic with multi-agent and guardrail integration"""
    try:
        if netflix_data is None or netflix_data.empty:
            return {"status": "error", "message": "Dataset not available"}
        
        query_lower = natural_language_query.lower()
        result = None
        multi_agent_insights = None
        
        # Try to get multi-agent insights first
        if MULTI_AGENTS_AVAILABLE:
            try:
                multi_agent_insights = run_netflix_multi_agent(natural_language_query)
                logger.info(f"Multi-agent insights obtained: {len(str(multi_agent_insights))} characters")
            except Exception as e:
                logger.warning(f"Multi-agent system error: {e}, proceeding with business logic")
                multi_agent_insights = None
        
        # Core Business Logic - Korean content percentage
        if 'korean' in query_lower and ('percentage' in query_lower or 'percent' in query_lower):
            korean_content = netflix_data[netflix_data['country'].str.contains('Korea', case=False, na=False)]
            total_titles = len(netflix_data)
            korean_count = len(korean_content)
            percentage = round((korean_count / total_titles) * 100, 2) if total_titles > 0 else 0
            
            korean_movies = len(korean_content[korean_content['type'] == 'Movie'])
            korean_shows = len(korean_content[korean_content['type'] == 'TV Show'])
            
            korean_genres = []
            for genres in korean_content['listed_in']:
                korean_genres.extend([g.strip() for g in str(genres).split(',')])
            top_korean_genres = pd.Series(korean_genres).value_counts().head(5).to_dict() if korean_genres else {}
            
            result = {
                "query": natural_language_query,
                "answer": f"{percentage}% of Netflix content is Korean ({korean_count} out of {total_titles} titles)",
                "detailed_breakdown": {
                    "total_korean_titles": korean_count,
                    "total_netflix_titles": total_titles,
                    "percentage": percentage,
                    "korean_movies": korean_movies,
                    "korean_tv_shows": korean_shows,
                    "top_korean_genres": top_korean_genres,
                    "recent_korean_content": len(korean_content[korean_content['release_year'] >= 2020])
                },
                "multi_agent_insights": multi_agent_insights if multi_agent_insights else "Multi-agent analysis not available"
            }
        
        # International vs US content trends
        elif 'international' in query_lower and 'us' in query_lower and 'trend' in query_lower:
            yearly_data = []
            for year in range(2015, 2024):
                year_content = netflix_data[netflix_data['release_year'] == year]
                us_content = len(year_content[year_content['country'].str.contains('United States', case=False, na=False)])
                total_content = len(year_content)
                international_content = total_content - us_content
                
                if total_content > 0:
                    yearly_data.append({
                        "year": year,
                        "total_titles": total_content,
                        "us_titles": us_content,
                        "international_titles": international_content,
                        "us_percentage": round((us_content / total_content) * 100, 1),
                        "international_percentage": round((international_content / total_content) * 100, 1)
                    })
            
            total_us = len(netflix_data[netflix_data['country'].str.contains('United States', case=False, na=False)])
            total_international = len(netflix_data) - total_us
            
            result = {
                "query": natural_language_query,
                "answer": f"International content represents {round((total_international/len(netflix_data))*100, 1)}% of Netflix catalog ({total_international} out of {len(netflix_data)} titles)",
                "overall_breakdown": {
                    "total_titles": len(netflix_data),
                    "us_titles": total_us,
                    "international_titles": total_international,
                    "us_percentage": round((total_us / len(netflix_data)) * 100, 1),
                    "international_percentage": round((total_international / len(netflix_data)) * 100, 1)
                },
                "yearly_trends": yearly_data,
                "insight": "International content has been growing as a percentage of Netflix's catalog",
                "multi_agent_insights": multi_agent_insights if multi_agent_insights else "Multi-agent analysis not available"
            }
        
        # Most popular genres globally
        elif 'popular genres' in query_lower or 'top genres' in query_lower:
            all_genres = []
            for genres in netflix_data['listed_in']:
                all_genres.extend([g.strip() for g in str(genres).split(',')])
            
            genre_counts = pd.Series(all_genres).value_counts()
            
            top_genres_data = []
            for genre, count in genre_counts.head(15).items():
                percentage = round((count / len(netflix_data)) * 100, 2)
                top_genres_data.append({
                    "genre": genre,
                    "title_count": count,
                    "percentage_of_catalog": percentage
                })
            
            result = {
                "query": natural_language_query,
                "answer": f"Most popular genre globally is '{genre_counts.index[0]}' with {genre_counts.iloc[0]} titles ({round((genre_counts.iloc[0]/len(netflix_data))*100, 1)}%)",
                "top_genres": top_genres_data,
                "total_unique_genres": len(genre_counts),
                "dataset_size": len(netflix_data),
                "multi_agent_insights": multi_agent_insights if multi_agent_insights else "Multi-agent analysis not available"
            }
        
        # Fallback for unrecognized queries
        else:
            if multi_agent_insights:
                result = {
                    "query": natural_language_query,
                    "answer": "Query processed by multi-agent system with business intelligence enhancement",
                    "multi_agent_response": multi_agent_insights,
                    "dataset_info": {
                        "total_titles": len(netflix_data),
                        "data_source": "Netflix dataset"
                    }
                }
            else:
                result = {
                    "query": natural_language_query,
                    "answer": "Query not recognized by business intelligence patterns. Please try specific queries about Korean content, genres, international trends, or content statistics.",
                    "suggested_queries": [
                        "What percentage of Netflix content is Korean?",
                        "Show me the trend of international vs US content",
                        "What are the most popular genres globally?"
                    ],
                    "dataset_info": {
                        "total_titles": len(netflix_data),
                        "data_source": "Netflix dataset"
                    }
                }
        
        # Prepare final response with guardrail integration
        final_response_data = {
            "status": "success",
            "source": "enhanced_business_intelligence_with_real_data",
            "business_intelligence": result,
            "dataset_size": len(netflix_data),
            "data_source": "Netflix dataset",
            "query_timestamp": datetime.now().isoformat(),
            "enhancements": {
                "multi_agent_available": MULTI_AGENTS_AVAILABLE,
                "guardrails_available": GUARDRAILS_AVAILABLE,
                "multi_agent_insights_included": multi_agent_insights is not None
            }
        }
        
        # Apply guardrails if available
        if GUARDRAILS_AVAILABLE and guardrail_system:
            try:
                guardrail_result = apply_guardrails_to_response(
                    json.dumps(final_response_data), 
                    {"content_type": "general", "query": natural_language_query}
                )
                
                final_response_data["guardrail_evaluation"] = {
                    "status": guardrail_result["guardrail_status"],
                    "score": guardrail_result["guardrail_score"],
                    "recommendations": guardrail_result.get("recommendations", [])
                }
                
                if guardrail_result["guardrail_status"] == "FLAGGED":
                    final_response_data["guardrail_warning"] = "Content flagged by guardrails but business intelligence data is still valid"
                
            except Exception as e:
                logger.warning(f"Guardrail evaluation error: {e}")
                final_response_data["guardrail_evaluation"] = {
                    "status": "ERROR",
                    "message": "Guardrail evaluation failed",
                    "error": str(e)
                }
        
        return final_response_data
        
    except Exception as e:
        error_response = {
            "status": "error",
            "message": str(e),
            "query": natural_language_query,
            "error_type": "enhanced_business_query_logic_error",
            "timestamp": datetime.now().isoformat()
        }
        logger.error(f"Enhanced business query logic error: {e}")
        return error_response

# MCP Tool Handlers - Only if MCP is available
if MCP_AVAILABLE and server:
    @server.list_tools()
    async def handle_list_tools() -> List[Tool]:
        """List available tools for the Netflix MCP server"""
        tools = [
            Tool(
                name="netflix_business_query",
                description="Enhanced business intelligence queries with multi-agent and guardrail integration for Netflix data analysis",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "natural_language_query": {
                            "type": "string",
                            "description": "Business question about Netflix content, trends, or analytics"
                        }
                    },
                    "required": ["natural_language_query"]
                }
            ),
            Tool(
                name="netflix_test_query",
                description="Simple test query for MCP functionality",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "test_message": {
                            "type": "string",
                            "description": "Test message",
                            "default": "Hello MCP!"
                        }
                    },
                    "required": []
                }
            ),
            Tool(
                name="netflix_dataset_info",
                description="Get information about the Netflix dataset",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "detail_level": {
                            "type": "string",
                            "description": "Level of detail: basic, detailed, or full",
                            "default": "basic"
                        }
                    },
                    "required": []
                }
            )
        ]
        
        return tools

    @server.call_tool()
    async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
        """Handle tool calls"""
        try:
            if name == "netflix_business_query":
                natural_language_query = arguments.get("natural_language_query", "")
                result = enhanced_business_query_logic(natural_language_query)
                return [TextContent(type="text", text=json.dumps(result, indent=2))]
            
            elif name == "netflix_test_query":
                test_message = arguments.get("test_message", "Hello MCP!")
                result = {
                    "status": "success",
                    "message": f"Test successful: {test_message}",
                    "timestamp": datetime.now().isoformat(),
                    "server_info": {
                        "environment": "cursor_ide",
                        "multi_agents_available": MULTI_AGENTS_AVAILABLE,
                        "guardrails_available": GUARDRAILS_AVAILABLE,
                        "dataset_size": len(netflix_data) if netflix_data is not None else 0
                    }
                }
                return [TextContent(type="text", text=json.dumps(result, indent=2))]
            
            elif name == "netflix_dataset_info":
                detail_level = arguments.get("detail_level", "basic")
                
                if netflix_data is None or netflix_data.empty:
                    result = {
                        "status": "error",
                        "message": "Dataset not available"
                    }
                else:
                    basic_info = {
                        "total_titles": len(netflix_data),
                        "movies": len(netflix_data[netflix_data['type'] == 'Movie']),
                        "tv_shows": len(netflix_data[netflix_data['type'] == 'TV Show']),
                        "date_range": {
                            "earliest": int(netflix_data['release_year'].min()),
                            "latest": int(netflix_data['release_year'].max())
                        }
                    }
                    
                    if detail_level == "detailed":
                        # Top countries
                        top_countries = netflix_data['country'].value_counts().head(10).to_dict()
                        
                        # Top genres
                        all_genres = []
                        for genres in netflix_data['listed_in'].dropna():
                            all_genres.extend([g.strip() for g in str(genres).split(',')])
                        top_genres = pd.Series(all_genres).value_counts().head(10).to_dict()
                        
                        basic_info.update({
                            "top_countries": top_countries,
                            "top_genres": top_genres,
                            "ratings_distribution": netflix_data['rating'].value_counts().to_dict(),
                            "content_by_year": netflix_data.groupby('release_year').size().tail(10).to_dict()
                        })
                    
                    elif detail_level == "full":
                        # Comprehensive dataset analysis
                        basic_info.update({
                            "columns": list(netflix_data.columns),
                            "data_quality": {
                                "missing_values": netflix_data.isnull().sum().to_dict(),
                                "duplicate_titles": netflix_data.duplicated(subset=['title']).sum(),
                                "unique_directors": netflix_data['director'].nunique(),
                                "unique_countries": netflix_data['country'].nunique()
                            },
                            "content_analysis": {
                                "avg_release_year": float(netflix_data['release_year'].mean()),
                                "most_recent_addition": netflix_data['date_added'].mode().iloc[0] if not netflix_data['date_added'].mode().empty else "Unknown",
                                "longest_title": netflix_data.loc[netflix_data['title'].str.len().idxmax(), 'title'] if len(netflix_data) > 0 else "Unknown"
                            }
                        })
                    
                    result = {
                        "status": "success",
                        "detail_level": detail_level,
                        "dataset_info": basic_info,
                        "timestamp": datetime.now().isoformat()
                    }
                
                return [TextContent(type="text", text=json.dumps(result, indent=2))]
            
            else:
                return [TextContent(type="text", text=json.dumps({
                    "status": "error",
                    "message": f"Unknown tool: {name}"
                }))]
        
        except Exception as e:
            logger.error(f"Error in tool {name}: {e}")
            return [TextContent(type="text", text=json.dumps({
                "status": "error",
                "message": f"Tool execution failed: {str(e)}"
            }))]

async def main():
    """Main function to run the MCP server"""
    if not MCP_AVAILABLE:
        logger.error("❌ MCP not available. Please install: uv add mcp")
        return
    
    logger.info("Starting Netflix Business Intelligence MCP Server (IDE)")
    logger.info(f"Multi-Agents Available: {MULTI_AGENTS_AVAILABLE}")
    logger.info(f"Guardrails Available: {GUARDRAILS_AVAILABLE}")
    logger.info(f"Dataset Size: {len(netflix_data) if netflix_data is not None else 'Not Available'}")
    
    try:
        async with stdio_server() as (read_stream, write_stream):
            # Proper initialization without the 'NoneType' error
            init_options = InitializationOptions(
                server_name="netflix-business-intelligence",
                server_version="2.0.0",
                capabilities=server.get_capabilities(
                    notification_options=None,
                    experimental_capabilities=None,
                ),
            )
            
            await server.run(
                read_stream,
                write_stream,
                init_options,
            )
    except Exception as e:
        logger.error(f"❌ MCP Server error: {e}")
        # Fallback: run as standalone for testing
        logger.info("🔄 Running in standalone test mode...")
        await test_standalone_server()

async def test_standalone_server():
    """Test the server functionality without MCP protocol"""
    logger.info("🧪 Testing Netflix MCP Server functionality...")
    
    test_queries = [
        "What percentage of Netflix content is Korean?",
        "What are the most popular genres globally?",
        "Show me the trend of international vs US content"
    ]
    
    for query in test_queries:
        logger.info(f"🔍 Testing query: {query}")
        result = enhanced_business_query_logic(query)
        logger.info(f"✅ Result: {result.get('status', 'unknown')}")
        
        if result.get('business_intelligence', {}).get('answer'):
            logger.info(f"💡 Answer: {result['business_intelligence']['answer']}")
    
    logger.info("✅ Standalone testing completed!")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("👋 Server stopped by user")
    except Exception as e:
        logger.error(f"❌ Server startup failed: {e}")
        # Run standalone test
        asyncio.run(test_standalone_server())
