#!/usr/bin/env python3
"""
Netflix Business Intelligence MCP Server - Complete Version with TMDB Integration
Professional setup with proper imports and multi-data source support
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

# Import your existing modules - Updated paths for IDE
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

def load_netflix_dataset():
    """
    Load dataset with support for Netflix CSV, TMDB API, or sample data
    Enhanced with multiple data source options
    """
    try:
        logger.info("🔍 Loading Netflix dataset with multi-source support...")
        
        # Priority 1: Try to load local Netflix CSV files
        netflix_csv_paths = [
            os.getenv('NETFLIX_DATASET_PATH', 'data/netflix_titles.csv'),
            'data/netflix_titles.csv',
            '../data/netflix_titles.csv',
            '../../data/netflix_titles.csv',
            Path.home() / 'Downloads' / 'netflix_titles.csv'
        ]
        
        for path in netflix_csv_paths:
            if Path(path).exists():
                logger.info(f"📁 Loading Netflix CSV from: {path}")
                try:
                    df = pd.read_csv(path)
                    
                    # Validate the CSV structure
                    required_columns = ['title', 'type']
                    if all(col in df.columns for col in required_columns):
                        df = clean_netflix_dataset(df)
                        logger.info(f"✅ Successfully loaded {len(df)} titles from Netflix CSV")
                        return df
                    else:
                        logger.warning(f"⚠️ CSV file missing required columns: {path}")
                        continue
                        
                except Exception as e:
                    logger.warning(f"⚠️ Error reading CSV file {path}: {e}")
                    continue
        
        # Priority 2: Try TMDB API if available
        if os.getenv('TMDB_API_KEY'):
            logger.info("🎬 Netflix CSV not found, attempting TMDB API integration...")
            try:
                # Import TMDB integration
                sys.path.append(str(Path(__file__).parent.parent))
                from data_sources.tmdb_integration import TMDBDataSource
                
                tmdb = TMDBDataSource()
                logger.info("🔗 TMDB API connection established")
                
                # Get a reasonable amount of data for development/testing
                df = tmdb.get_combined_data(movie_pages=25, tv_pages=15)  # ~1000-1500 titles
                
                if not df.empty:
                    logger.info(f"✅ Successfully loaded {len(df)} titles from TMDB API")
                    return df
                else:
                    logger.warning("⚠️ TMDB API returned empty dataset")
                    
            except ImportError:
                logger.warning("⚠️ TMDB integration module not found")
            except Exception as e:
                logger.warning(f"⚠️ TMDB API error: {e}")
        else:
            logger.info("📋 TMDB_API_KEY not configured, skipping TMDB integration")
        
        # Priority 3: Fall back to sample dataset
        logger.warning("⚠️ No external data source available, creating sample dataset")
        return create_sample_dataset()
        
    except Exception as e:
        logger.error(f"❌ Critical error in dataset loading: {e}")
        return create_sample_dataset()

def clean_netflix_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and standardize Netflix dataset"""
    logger.info("🧹 Cleaning Netflix dataset...")
    
    try:
        # Fill missing values
        df['director'] = df['director'].fillna('Unknown Director')
        df['cast'] = df['cast'].fillna('Unknown Cast')
        df['country'] = df['country'].fillna('Unknown Country')
        df['date_added'] = df['date_added'].fillna('Unknown Date')
        df['rating'] = df['rating'].fillna('Not Rated')
        df['duration'] = df['duration'].fillna('Unknown Duration')
        df['listed_in'] = df['listed_in'].fillna('Unknown Genre')
        df['description'] = df['description'].fillna('No description available')
        
        # Clean release year
        df['release_year'] = pd.to_numeric(df['release_year'], errors='coerce')
        df['release_year'] = df['release_year'].fillna(2020).astype(int)
        
        # Handle show_id
        if 'show_id' in df.columns:
            df['show_id'] = df['show_id'].fillna('unknown_id')
        
        # Remove rows with missing critical data
        df = df.dropna(subset=['title', 'type'])
        
        # Remove duplicates
        df = df.drop_duplicates(subset=['title', 'type'], keep='first')
        
        # Clean text columns
        text_columns = ['title', 'director', 'cast', 'country', 'listed_in', 'description']
        for col in text_columns:
            if col in df.columns:
                df[col] = df[col].astype(str).str.strip()
        
        logger.info(f"✅ Dataset cleaned successfully: {len(df)} titles")
        return df
        
    except Exception as e:
        logger.error(f"❌ Error cleaning dataset: {e}")
        return df

def create_sample_dataset():
    """Create a comprehensive sample dataset for development/testing"""
    logger.info("🎭 Creating enhanced sample dataset for development...")
    
    try:
        # Enhanced sample data with more realistic content
        sample_data = {
            'show_id': [f's{i}' for i in range(1, 201)],  # 200 titles
            'type': ['Movie'] * 120 + ['TV Show'] * 80,
            'title': [
                # Popular movies
                'The Irishman', 'Bird Box', 'Extraction', 'The Old Guard', 'Enola Holmes',
                'Red Notice', 'Don\'t Look Up', 'The Adam Project', 'The Gray Man', 'Purple Hearts',
                'Glass Onion', 'All Quiet on the Western Front', 'The Sea Beast', 'Pinocchio', 'Blonde',
                
                # International movies
                'Squid Game: The Movie', 'Money Heist: Korea', 'The Call', 'Space Sweepers', 'Carter',
                'RRR', 'Gangubai Kathiawadi', 'Haseen Dillruba', 'Shershaah', 'Sardar Udham',
                
                # TV Shows
                'Stranger Things', 'The Crown', 'Ozark', 'Bridgerton', 'The Witcher',
                'Wednesday', 'Monster: The Jeffrey Dahmer Story', 'The Watcher', 'Inventing Anna', 'Maid',
                'Squid Game', 'All of Us Are Dead', 'Kingdom', 'My Name', 'Hellbound',
                'Money Heist', 'Elite', 'La Casa de Papel', 'Control Z', 'Who Killed Sara?',
                
                # Family content
                'The Kissing Booth', 'To All the Boys I\'ve Loved Before', 'The Princess Switch', 'A Christmas Prince',
                'The Knight Before Christmas', 'Holiday in the Wild', 'The Perfect Date', 'Sierra Burgess Is a Loser'
            ] + [f'Sample Title {i}' for i in range(48, 201)],  # Fill remaining with generic titles
            
            'director': [
                'Martin Scorsese', 'Susanne Bier', 'Sam Hargrave', 'Gina Prince-Bythewood', 'Harry Bradbeer',
                'Rawson Marshall Thurber', 'Adam McKay', 'Shawn Levy', 'Russo Brothers', 'Julius Avery'
            ] * 20,  # Repeat for all entries
            
            'cast': [
                'Robert De Niro, Al Pacino, Joe Pesci',
                'Sandra Bullock, Trevante Rhodes',
                'Chris Hemsworth, Rudhraksh Jaiswal',
                'Charlize Theron, KiKi Layne',
                'Millie Bobby Brown, Henry Cavill'
            ] * 40,  # Repeat for all entries
            
            'country': (
                ['United States'] * 80 +
                ['South Korea'] * 30 +
                ['United Kingdom'] * 20 +
                ['Spain'] * 15 +
                ['India'] * 15 +
                ['Japan'] * 10 +
                ['Germany'] * 8 +
                ['France'] * 7 +
                ['Brazil'] * 5 +
                ['Canada'] * 5 +
                ['Australia'] * 3 +
                ['Mexico'] * 2
            ),
            
            'date_added': [
                'January 1, 2023', 'February 15, 2023', 'March 10, 2023', 'April 5, 2023',
                'May 20, 2023', 'June 12, 2023', 'July 8, 2023', 'August 25, 2023',
                'September 14, 2023', 'October 31, 2023', 'November 18, 2023', 'December 22, 2023'
            ] * 17,  # Cycle through dates
            
            'release_year': (
                [2023] * 40 + [2022] * 50 + [2021] * 45 + [2020] * 35 +
                [2019] * 20 + [2018] * 10
            ),
            
            'rating': (
                ['TV-MA'] * 60 + ['PG-13'] * 50 + ['R'] * 30 +
                ['TV-14'] * 25 + ['PG'] * 20 + ['TV-PG'] * 15
            ),
            
            'duration': (
                [f'{90 + (i % 60)} min' for i in range(120)] +  # Movies: 90-150 min
                [f'{1 + (i % 5)} Season{"s" if (1 + i % 5) > 1 else ""}' for i in range(80)]  # TV: 1-5 seasons
            ),
            
            'listed_in': [
                'Action & Adventure, Crime, Drama',
                'Horror, Thriller',
                'Action & Adventure, International Movies',
                'Action & Adventure, Sci-Fi & Fantasy',
                'Children & Family, Comedies',
                'Comedies, Romance',
                'Comedies, Dramas',
                'Action & Adventure, Thrillers',
                'Crime, Dramas, International Movies',
                'Documentaries, International Movies',
                'Horror, International Movies, Thrillers',
                'International TV Shows, Korean TV Shows, TV Dramas',
                'International TV Shows, Spanish-Language TV Shows',
                'Kids & Family, TV Comedies',
                'Crime, International TV Shows, TV Dramas',
                'Anime, International TV Shows'
            ] * 13,  # Cycle through genres
            
            'description': [
                f'An engaging {["drama", "comedy", "thriller", "action", "romance"][i % 5]} that captivates audiences with its compelling storyline and outstanding performances. '
                f'This {"movie" if i < 120 else "series"} explores themes of {"family, love, and redemption" if i % 2 == 0 else "adventure, mystery, and discovery"}.'
                for i in range(200)
            ]
        }
        
        df = pd.DataFrame(sample_data)
        
        # Add some variety to the data
        df.loc[df['country'] == 'South Korea', 'listed_in'] = 'International Movies, Korean Movies, Dramas'
        df.loc[df['country'] == 'Spain', 'listed_in'] = 'International Movies, Spanish-Language Movies, Thrillers'
        df.loc[df['country'] == 'India', 'listed_in'] = 'International Movies, Bollywood Movies, Dramas'
        df.loc[df['type'] == 'TV Show', 'listed_in'] = df.loc[df['type'] == 'TV Show', 'listed_in'].str.replace('Movies', 'TV Shows')
        
        logger.info(f"✅ Enhanced sample dataset created: {len(df)} titles")
        logger.info(f"📊 Breakdown: {len(df[df['type'] == 'Movie'])} movies, {len(df[df['type'] == 'TV Show'])} TV shows")
        logger.info(f"🌍 Countries: {df['country'].value_counts().head().to_dict()}")
        
        return df
        
    except Exception as e:
        logger.error(f"❌ Error creating sample dataset: {e}")
        # Minimal fallback dataset
        return pd.DataFrame({
            'show_id': ['s1', 's2', 's3'],
            'type': ['Movie', 'TV Show', 'Movie'],
            'title': ['Sample Movie 1', 'Sample TV Show 1', 'Sample Movie 2'],
            'director': ['Unknown Director'] * 3,
            'cast': ['Unknown Cast'] * 3,
            'country': ['United States'] * 3,
            'date_added': ['January 1, 2023'] * 3,
            'release_year': [2023, 2023, 2023],
            'rating': ['PG-13'] * 3,
            'duration': ['120 min', '1 Season', '110 min'],
            'listed_in': ['Drama'] * 3,
            'description': ['Sample description'] * 3
        })

# Initialize dataset
netflix_data = load_netflix_dataset()

# Enhanced business logic functions with improved error handling
def enhanced_business_query_logic(natural_language_query: str) -> Dict[str, Any]:
    """
    Enhanced business intelligence logic with multi-agent and guardrail integration
    Now supports multiple data sources and improved error handling
    """
    try:
        if netflix_data is None or netflix_data.empty:
            return {
                "status": "error", 
                "message": "Dataset not available - please check data source configuration",
                "suggestions": [
                    "Ensure Netflix CSV is available in data/ directory",
                    "Configure TMDB_API_KEY for alternative data source",
                    "Check logs for detailed error information"
                ]
            }
        
        query_lower = natural_language_query.lower()
        result = None
        multi_agent_insights = None
        
        # Try to get multi-agent insights first
        if MULTI_AGENTS_AVAILABLE:
            try:
                multi_agent_insights = run_netflix_multi_agent(natural_language_query)
                logger.info(f"🤖 Multi-agent insights obtained: {len(str(multi_agent_insights))} characters")
            except Exception as e:
                logger.warning(f"⚠️ Multi-agent system error: {e}, proceeding with business logic")
                multi_agent_insights = None
        
        # Enhanced Business Logic Patterns
        
        # Korean content analysis
        if 'korean' in query_lower and ('percentage' in query_lower or 'percent' in query_lower):
            korean_content = netflix_data[netflix_data['country'].str.contains('Korea', case=False, na=False)]
            total_titles = len(netflix_data)
            korean_count = len(korean_content)
            percentage = round((korean_count / total_titles) * 100, 2) if total_titles > 0 else 0
            
            korean_movies = len(korean_content[korean_content['type'] == 'Movie'])
            korean_shows = len(korean_content[korean_content['type'] == 'TV Show'])
            
            # Analyze Korean genres
            korean_genres = []
            for genres in korean_content['listed_in']:
                korean_genres.extend([g.strip() for g in str(genres).split(',')])
            top_korean_genres = pd.Series(korean_genres).value_counts().head(5).to_dict() if korean_genres else {}
            
            # Recent Korean content
            recent_korean = len(korean_content[korean_content['release_year'] >= 2020])
            
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
                    "recent_korean_content": recent_korean,
                    "korean_content_growth": "Strong growth in Korean original content since 2020"
                },
                "data_source": "Netflix dataset" if 'netflix' in str(netflix_data.iloc[0]['show_id']).lower() else "TMDB API",
                "multi_agent_insights": multi_agent_insights if multi_agent_insights else "Multi-agent analysis not available"
            }
        
        # International vs US content trends
        elif 'international' in query_lower and 'us' in query_lower and 'trend' in query_lower:
            yearly_data = []
            
            for year in range(2018, 2024):
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
            overall_intl_percentage = round((total_international / len(netflix_data)) * 100, 1)
            
            # Analyze top international countries
            intl_content = netflix_data[~netflix_data['country'].str.contains('United States', case=False, na=False)]
            top_intl_countries = intl_content['country'].value_counts().head(10).to_dict()
            
            result = {
                "query": natural_language_query,
                "answer": f"International content represents {overall_intl_percentage}% of Netflix catalog ({total_international} out of {len(netflix_data)} titles)",
                "overall_breakdown": {
                    "total_titles": len(netflix_data),
                    "us_titles": total_us,
                    "international_titles": total_international,
                    "us_percentage": round((total_us / len(netflix_data)) * 100, 1),
                    "international_percentage": overall_intl_percentage
                },
                "yearly_trends": yearly_data,
                "top_international_countries": top_intl_countries,
                "insights": [
                    "International content has been steadily growing",
                    "Netflix has expanded significantly in non-English markets",
                    "Local content strategy drives global engagement"
                ],
                "multi_agent_insights": multi_agent_insights if multi_agent_insights else "Multi-agent analysis not available"
            }
        
        # Genre popularity analysis
        elif 'popular genres' in query_lower or 'top genres' in query_lower:
            all_genres = []
            for genres in netflix_data['listed_in']:
                all_genres.extend([g.strip() for g in str(genres).split(',')])
            
            genre_counts = pd.Series(all_genres).value_counts()
            
            # Detailed genre analysis
            top_genres_data = []
            for genre, count in genre_counts.head(15).items():
                percentage = round((count / len(netflix_data)) * 100, 2)
                
                # Get genre content by type
                genre_content = netflix_data[netflix_data['listed_in'].str.contains(genre, case=False, na=False)]
                movies_count = len(genre_content[genre_content['type'] == 'Movie'])
                shows_count = len(genre_content[genre_content['type'] == 'TV Show'])
                
                top_genres_data.append({
                    "genre": genre,
                    "total_titles": count,
                    "percentage_of_catalog": percentage,
                    "movies": movies_count,
                    "tv_shows": shows_count,
                    "avg_release_year": int(genre_content['release_year'].mean()) if not genre_content.empty else 2020
                })
            
            # Genre trends by year
            recent_genres = netflix_data[netflix_data['release_year'] >= 2020]
            recent_genre_list = []
            for genres in recent_genres['listed_in']:
                recent_genre_list.extend([g.strip() for g in str(genres).split(',')])
            recent_genre_counts = pd.Series(recent_genre_list).value_counts().head(5).to_dict()
            
            result = {
                "query": natural_language_query,
                "answer": f"Most popular genre globally is '{genre_counts.index[0]}' with {genre_counts.iloc[0]} titles ({round((genre_counts.iloc[0]/len(netflix_data))*100, 1)}%)",
                "top_genres_detailed": top_genres_data,
                "recent_trends": {
                    "top_genres_2020_plus": recent_genre_counts,
                    "trend_analysis": "Action, International content, and Documentaries show strong growth"
                },
                "genre_statistics": {
                    "total_unique_genres": len(genre_counts),
                    "dataset_size": len(netflix_data),
                    "avg_genres_per_title": round(len(all_genres) / len(netflix_data), 1)
                },
                "multi_agent_insights": multi_agent_insights if multi_agent_insights else "Multi-agent analysis not available"
            }
        
        # Content by country analysis
        elif 'country' in query_lower or 'countries' in query_lower:
            country_analysis = netflix_data['country'].value_counts().head(15)
            
            country_details = []
            for country, count in country_analysis.items():
                country_content = netflix_data[netflix_data['country'] == country]
                movies_count = len(country_content[country_content['type'] == 'Movie'])
                shows_count = len(country_content[country_content['type'] == 'TV Show'])
                avg_year = int(country_content['release_year'].mean()) if not country_content.empty else 2020
                
                country_details.append({
                    "country": country,
                    "total_titles": count,
                    "percentage": round((count / len(netflix_data)) * 100, 2),
                    "movies": movies_count,
                    "tv_shows": shows_count,
                    "average_release_year": avg_year
                })
            
            result = {
                "query": natural_language_query,
                "answer": f"Top content-producing country is {country_analysis.index[0]} with {country_analysis.iloc[0]} titles ({round((country_analysis.iloc[0]/len(netflix_data))*100, 1)}%)",
                "country_breakdown": country_details,
                "global_distribution": {
                    "total_countries": netflix_data['country'].nunique(),
                    "top_5_countries": country_analysis.head(5).to_dict()
                },
                "multi_agent_insights": multi_agent_insights if multi_agent_insights else "Multi-agent analysis not available"
            }
        
        # General fallback with multi-agent response
        else:
            if multi_agent_insights:
                result = {
                    "query": natural_language_query,
                    "answer": "Query processed by advanced multi-agent system with comprehensive business intelligence",
                    "multi_agent_response": multi_agent_insights,
                    "dataset_info": {
                        "total_titles": len(netflix_data),
                        "data_source": "Netflix dataset" if 'netflix' in str(netflix_data.iloc[0]['show_id']).lower() else "TMDB API",
                        "last_updated": datetime.now().strftime("%Y-%m-%d")
                    },
                    "capabilities": [
                        "Korean content analysis",
                        "International vs US content trends", 
                        "Genre popularity analysis",
                        "Country-wise content distribution",
                        "Custom multi-agent insights"
                    ]
                }
            else:
                result = {
                    "query": natural_language_query,
                    "answer": "Query not recognized by business intelligence patterns. Please try specific queries about Korean content, genres, international trends, or content statistics.",
                    "suggested_queries": [
                        "What percentage of Netflix content is Korean?",
                        "Show me the trend of international vs US content",
                        "What are the most popular genres globally?",
                        "Which countries produce the most Netflix content?"
                    ],
                    "dataset_info": {
                        "total_titles": len(netflix_data),
                        "data_source": "Netflix dataset" if len(netflix_data) > 100 else "Sample data",
                        "available_analysis": "Korean content, genres, countries, trends"
                    }
                }
        
        # Prepare final response with enhanced metadata
        final_response_data = {
            "status": "success",
            "source": "enhanced_business_intelligence_v2.0",
            "business_intelligence": result,
            "dataset_metadata": {
                "size": len(netflix_data),
                "data_source": "TMDB API" if 'tm_' in str(netflix_data.iloc[0]['show_id']) else "Netflix CSV" if len(netflix_data) > 100 else "Sample Data",
                "content_types": netflix_data['type'].value_counts().to_dict(),
                "year_range": f"{netflix_data['release_year'].min()}-{netflix_data['release_year'].max()}",
                "countries": netflix_data['country'].nunique(),
                "last_processed": datetime.now().isoformat()
            },
            "query_timestamp": datetime.now().isoformat(),
            "enhancements": {
                "multi_agent_available": MULTI_AGENTS_AVAILABLE,
                "guardrails_available": GUARDRAILS_AVAILABLE,
                "multi_agent_insights_included": multi_agent_insights is not None,
                "data_source_type": "external_api" if 'tm_' in str(netflix_data.iloc[0]['show_id']) else "local_csv" if len(netflix_data) > 100 else "sample_data"
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
                logger.warning(f"⚠️ Guardrail evaluation error: {e}")
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
            "timestamp": datetime.now().isoformat(),
            "suggestions": [
                "Check dataset availability and format",
                "Verify API keys if using external data sources",
                "Try simpler queries first",
                "Check logs for detailed error information"
            ]
        }
        logger.error(f"❌ Enhanced business query logic error: {e}")
        return error_response

# MCP Tool Handlers - Enhanced with multi-source support
if MCP_AVAILABLE and server:
    @server.list_tools()
    async def handle_list_tools() -> List[Tool]:
        """List available tools for the Netflix MCP server with enhanced descriptions"""
        tools = [
            Tool(
                name="netflix_business_query",
                description="Enhanced business intelligence queries with multi-agent and guardrail integration for Netflix data analysis. Supports Netflix CSV, TMDB API, and sample data sources.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "natural_language_query": {
                            "type": "string",
                            "description": "Business question about Netflix content, trends, or analytics (e.g., 'What percentage of content is Korean?', 'Show international vs US trends')"
                        }
                    },
                    "required": ["natural_language_query"]
                }
            ),
            Tool(
                name="netflix_test_query",
                description="Simple test query for MCP functionality and system health check",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "test_message": {
                            "type": "string",
                            "description": "Test message for connectivity verification",
                            "default": "Hello MCP!"
                        }
                    },
                    "required": []
                }
            ),
            Tool(
                name="netflix_dataset_info",
                description="Get comprehensive information about the active Netflix dataset including source, size, and quality metrics",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "detail_level": {
                            "type": "string",
                            "description": "Level of detail: basic (summary), detailed (statistics), or full (comprehensive analysis)",
                            "enum": ["basic", "detailed", "full"],
                            "default": "basic"
                        }
                    },
                    "required": []
                }
            ),
            Tool(
                name="netflix_data_source_switch",
                description="Switch between available data sources (Netflix CSV, TMDB API, or Sample Data) and reload dataset",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "data_source": {
                            "type": "string",
                            "description": "Preferred data source",
                            "enum": ["netflix_csv", "tmdb_api", "sample_data", "auto"],
                            "default": "auto"
                        },
                        "reload": {
                            "type": "boolean",
                            "description": "Force reload of dataset",
                            "default": false
                        }
                    },
                    "required": ["data_source"]
                }
            )
        ]
        
        return tools

    @server.call_tool()
    async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
        """Handle tool calls with enhanced functionality"""
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
                        "environment": "multi_source_mcp_server",
                        "version": "2.0.0",
                        "multi_agents_available": MULTI_AGENTS_AVAILABLE,
                        "guardrails_available": GUARDRAILS_AVAILABLE,
                        "dataset_size": len(netflix_data) if netflix_data is not None else 0,
                        "dataset_source": "TMDB API" if netflix_data is not None and 'tm_' in str(netflix_data.iloc[0]['show_id']) else "Netflix CSV" if netflix_data is not None and len(netflix_data) > 100 else "Sample Data",
                        "data_sources_available": {
                            "netflix_csv": "Available" if Path("data/netflix_titles.csv").exists() else "Not Found",
                            "tmdb_api": "Available" if os.getenv('TMDB_API_KEY') else "API Key Not Configured",
                            "sample_data": "Always Available"
                        }
                    }
                }
                return [TextContent(type="text", text=json.dumps(result, indent=2))]
            
            elif name == "netflix_dataset_info":
                detail_level = arguments.get("detail_level", "basic")
                
                if netflix_data is None or netflix_data.empty:
                    result = {
                        "status": "error",
                        "message": "Dataset not available - check data source configuration"
                    }
                else:
                    # Determine data source
                    if 'tm_' in str(netflix_data.iloc[0]['show_id']):
                        data_source = "TMDB API"
                        source_details = {
                            "api_configured": bool(os.getenv('TMDB_API_KEY')),
                            "real_time_data": True,
                            "update_frequency": "On-demand via API"
                        }
                    elif len(netflix_data) > 100:
                        data_source = "Netflix CSV"
                        csv_path = Path("data/netflix_titles.csv")
                        source_details = {
                            "file_path": str(csv_path),
                            "file_size_mb": round(csv_path.stat().st_size / 1024 / 1024, 2) if csv_path.exists() else 0,
                            "last_modified": datetime.fromtimestamp(csv_path.stat().st_mtime).isoformat() if csv_path.exists() else "Unknown"
                        }
                    else:
                        data_source = "Sample Data"
                        source_details = {
                            "purpose": "Development and testing",
                            "generated": True,
                            "realistic_data": True
                        }
                    
                    basic_info = {
                        "data_source": data_source,
                        "source_details": source_details,
                        "total_titles": len(netflix_data),
                        "movies": len(netflix_data[netflix_data['type'] == 'Movie']),
                        "tv_shows": len(netflix_data[netflix_data['type'] == 'TV Show']),
                        "date_range": {
                            "earliest": int(netflix_data['release_year'].min()),
                            "latest": int(netflix_data['release_year'].max())
                        },
                        "countries_represented": netflix_data['country'].nunique(),
                        "unique_genres": len([genre.strip() for genres in netflix_data['listed_in'].dropna() for genre in str(genres).split(',')]),
                        "data_quality": {
                            "completeness": f"{((len(netflix_data) - netflix_data.isnull().sum().sum()) / (len(netflix_data) * len(netflix_data.columns)) * 100):.1f}%",
                            "duplicate_titles": netflix_data.duplicated(subset=['title']).sum()
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
                        
                        # Content by year
                        yearly_content = netflix_data.groupby('release_year').size().tail(10).to_dict()
                        
                        basic_info.update({
                            "top_countries": top_countries,
                            "top_genres": top_genres,
                            "ratings_distribution": netflix_data['rating'].value_counts().to_dict(),
                            "content_by_recent_years": yearly_content,
                            "average_release_year": round(netflix_data['release_year'].mean(), 1)
                        })
                    
                    elif detail_level == "full":
                        # Comprehensive dataset analysis
                        basic_info.update({
                            "columns": list(netflix_data.columns),
                            "data_types": netflix_data.dtypes.astype(str).to_dict(),
                            "memory_usage_mb": round(netflix_data.memory_usage(deep=True).sum() / 1024 / 1024, 2),
                            "data_quality_detailed": {
                                "missing_values": netflix_data.isnull().sum().to_dict(),
                                "duplicate_titles": netflix_data.duplicated(subset=['title']).sum(),
                                "unique_directors": netflix_data['director'].nunique(),
                                "unique_countries": netflix_data['country'].nunique(),
                                "title_length_stats": {
                                    "avg_length": round(netflix_data['title'].str.len().mean(), 1),
                                    "longest_title": netflix_data.loc[netflix_data['title'].str.len().idxmax(), 'title'] if len(netflix_data) > 0 else "Unknown"
                                }
                            },
                            "content_analysis": {
                                "avg_release_year": float(netflix_data['release_year'].mean()),
                                "content_span_years": int(netflix_data['release_year'].max() - netflix_data['release_year'].min()),
                                "most_common_rating": netflix_data['rating'].mode().iloc[0] if not netflix_data['rating'].mode().empty else "Unknown",
                                "international_content_percentage": round((len(netflix_data[~netflix_data['country'].str.contains('United States', case=False, na=False)]) / len(netflix_data)) * 100, 1)
                            },
                            "performance_metrics": {
                                "load_time_estimate": "< 1 second" if len(netflix_data) < 1000 else "1-3 seconds" if len(netflix_data) < 10000 else "3-10 seconds",
                                "query_complexity_support": "High" if len(netflix_data) > 100 else "Basic",
                                "scalability_rating": "Production Ready" if data_source in ["Netflix CSV", "TMDB API"] else "Development Only"
                            }
                        })
                    
                    result = {
                        "status": "success",
                        "detail_level": detail_level,
                        "dataset_info": basic_info,
                        "timestamp": datetime.now().isoformat(),
                        "recommendations": [
                            "Dataset is ready for business intelligence queries",
                            f"Current source ({data_source}) provides good data quality",
                            "Multi-agent system can leverage this dataset effectively"
                        ] if data_source != "Sample Data" else [
                            "Consider adding Netflix CSV or configuring TMDB API for production use",
                            "Sample data is suitable for development and testing",
                            "Switch to external data source for comprehensive analysis"
                        ]
                    }
                
                return [TextContent(type="text", text=json.dumps(result, indent=2))]
            
            elif name == "netflix_data_source_switch":
                data_source = arguments.get("data_source", "auto")
                reload = arguments.get("reload", False)
                
                try:
                    global netflix_data
                    
                    if data_source == "auto" or reload:
                        # Reload with automatic source detection
                        netflix_data = load_netflix_dataset()
                        actual_source = "TMDB API" if 'tm_' in str(netflix_data.iloc[0]['show_id']) else "Netflix CSV" if len(netflix_data) > 100 else "Sample Data"
                    
                    elif data_source == "netflix_csv":
                        # Force Netflix CSV loading
                        csv_paths = ['data/netflix_titles.csv', '../data/netflix_titles.csv']
                        loaded = False
                        for path in csv_paths:
                            if Path(path).exists():
                                netflix_data = pd.read_csv(path)
                                netflix_data = clean_netflix_dataset(netflix_data)
                                actual_source = "Netflix CSV"
                                loaded = True
                                break
                        
                        if not loaded:
                            raise FileNotFoundError("Netflix CSV file not found")
                    
                    elif data_source == "tmdb_api":
                        # Force TMDB API loading
                        if not os.getenv('TMDB_API_KEY'):
                            raise ValueError("TMDB_API_KEY not configured")
                        
                        from data_sources.tmdb_integration import TMDBDataSource
                        tmdb = TMDBDataSource()
                        netflix_data = tmdb.get_combined_data(movie_pages=30, tv_pages=20)
                        actual_source = "TMDB API"
                    
                    elif data_source == "sample_data":
                        # Force sample data creation
                        netflix_data = create_sample_dataset()
                        actual_source = "Sample Data"
                    
                    result = {
                        "status": "success",
                        "message": f"Successfully switched to {actual_source}",
                        "data_source_switched_to": actual_source,
                        "dataset_info": {
                            "size": len(netflix_data),
                            "movies": len(netflix_data[netflix_data['type'] == 'Movie']),
                            "tv_shows": len(netflix_data[netflix_data['type'] == 'TV Show']),
                            "countries": netflix_data['country'].nunique(),
                            "year_range": f"{netflix_data['release_year'].min()}-{netflix_data['release_year'].max()}"
                        },
                        "timestamp": datetime.now().isoformat()
                    }
                    
                except Exception as e:
                    result = {
                        "status": "error",
                        "message": f"Failed to switch to {data_source}: {str(e)}",
                        "current_source": "TMDB API" if netflix_data is not None and 'tm_' in str(netflix_data.iloc[0]['show_id']) else "Netflix CSV" if netflix_data is not None and len(netflix_data) > 100 else "Sample Data",
                        "available_sources": {
                            "netflix_csv": Path("data/netflix_titles.csv").exists(),
                            "tmdb_api": bool(os.getenv('TMDB_API_KEY')),
                            "sample_data": True
                        }
                    }
                
                return [TextContent(type="text", text=json.dumps(result, indent=2))]
            
            else:
                return [TextContent(type="text", text=json.dumps({
                    "status": "error",
                    "message": f"Unknown tool: {name}",
                    "available_tools": [
                        "netflix_business_query",
                        "netflix_test_query", 
                        "netflix_dataset_info",
                        "netflix_data_source_switch"
                    ]
                }))]
        
        except Exception as e:
            logger.error(f"❌ Error in tool {name}: {e}")
            return [TextContent(type="text", text=json.dumps({
                "status": "error",
                "message": f"Tool execution failed: {str(e)}",
                "tool": name,
                "timestamp": datetime.now().isoformat()
            }))]

async def main():
    """Main function to run the enhanced MCP server"""
    if not MCP_AVAILABLE:
        logger.error("❌ MCP not available. Please install: uv add mcp")
        logger.info("🔄 Running in standalone test mode...")
        await test_standalone_server()
        return
    
    logger.info("🚀 Starting Netflix Business Intelligence MCP Server v2.0 (Multi-Source)")
    logger.info("=" * 70)
    logger.info(f"📊 Dataset: {len(netflix_data)} titles loaded")
    logger.info(f"🗂️ Data Source: {'TMDB API' if netflix_data is not None and 'tm_' in str(netflix_data.iloc[0]['show_id']) else 'Netflix CSV' if netflix_data is not None and len(netflix_data) > 100 else 'Sample Data'}")
    logger.info(f"🤖 Multi-Agents: {'✅ Available' if MULTI_AGENTS_AVAILABLE else '❌ Not Available'}")
    logger.info(f"🔒 Guardrails: {'✅ Available' if GUARDRAILS_AVAILABLE else '❌ Not Available'}")
    logger.info(f"🔗 Data Sources Available:")
    logger.info(f"   • Netflix CSV: {'✅' if Path('data/netflix_titles.csv').exists() else '❌'}")
    logger.info(f"   • TMDB API: {'✅' if os.getenv('TMDB_API_KEY') else '❌'}")
    logger.info(f"   • Sample Data: ✅ (Always Available)")
    
    try:
        async with stdio_server() as (read_stream, write_stream):
            # Enhanced initialization
            init_options = InitializationOptions(
                server_name="netflix-business-intelligence-v2",
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
        logger.info("🔄 Falling back to standalone test mode...")
        await test_standalone_server()

async def test_standalone_server():
    """Test the enhanced server functionality without MCP protocol"""
    logger.info("🧪 Testing Enhanced Netflix MCP Server functionality...")
    logger.info("=" * 60)
    
    # Test data source information
    data_source = "TMDB API" if netflix_data is not None and 'tm_' in str(netflix_data.iloc[0]['show_id']) else "Netflix CSV" if netflix_data is not None and len(netflix_data) > 100 else "Sample Data"
    logger.info(f"📊 Active Data Source: {data_source}")
    logger.info(f"📈 Dataset Size: {len(netflix_data) if netflix_data is not None else 0} titles")
    
    test_queries = [
        "What percentage of Netflix content is Korean?",
        "What are the most popular genres globally?",
        "Show me the trend of international vs US content",
        "Which countries produce the most content?"
    ]
    
    successful_queries = 0
    
    for i, query in enumerate(test_queries, 1):
        logger.info(f"\n🔍 Test Query {i}: {query}")
        try:
            result = enhanced_business_query_logic(query)
            
            if result.get('status') == 'success':
                successful_queries += 1
                logger.info(f"✅ SUCCESS - Query processed successfully")
                
                # Show answer
                bi_data = result.get('business_intelligence', {})
                answer = bi_data.get('answer', 'No answer provided')
                logger.info(f"💡 Answer: {answer}")
                
                # Show data source
                dataset_meta = result.get('dataset_metadata', {})
                source = dataset_meta.get('data_source', 'Unknown')
                logger.info(f"🗂️ Source: {source}")
                
            else:
                logger.error(f"❌ FAILED - {result.get('message', 'Unknown error')}")
                
        except Exception as e:
            logger.error(f"❌ ERROR - Query failed: {e}")
    
    # Summary
    success_rate = successful_queries / len(test_queries) * 100
    logger.info(f"\n📊 Test Summary:")
    logger.info(f"   Successful Queries: {successful_queries}/{len(test_queries)}")
    logger.info(f"   Success Rate: {success_rate:.1f}%")
    logger.info(f"   Data Source: {data_source}")
    logger.info(f"   Multi-Agent System: {'✅ Available' if MULTI_AGENTS_AVAILABLE else '❌ Not Available'}")
    logger.info(f"   Guardrail System: {'✅ Available' if GUARDRAILS_AVAILABLE else '❌ Not Available'}")
    
    if success_rate >= 75:
        logger.info("🎉 Enhanced Netflix MCP Server is working excellently!")
    else:
        logger.info("⚠️ Enhanced Netflix MCP Server needs attention!")
    
    logger.info("✅ Standalone testing completed!")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("👋 Server stopped by user")
    except Exception as e:
        logger.error(f"❌ Server startup failed: {e}")
        # Run standalone test as fallback
        asyncio.run(test_standalone_server())
