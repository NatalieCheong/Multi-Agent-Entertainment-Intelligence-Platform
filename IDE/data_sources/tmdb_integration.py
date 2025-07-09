#!/usr/bin/env python3
"""
TMDB Data Source Integration
Professional TMDB API integration for Netflix MCP Platform
"""

import requests
import pandas as pd
from typing import Dict, List, Any, Optional
import os
import logging
import time
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=os.getenv('LOG_LEVEL', 'INFO'),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("tmdb-integration")

class TMDBDataSource:
    """
    Professional TMDB API integration for entertainment content data
    Converts TMDB data to Netflix CSV-compatible format
    """
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('TMDB_API_KEY')
        self.base_url = "https://api.themoviedb.org/3"
        self.session = requests.Session()
        
        if not self.api_key:
            raise ValueError("TMDB API key not found. Please set TMDB_API_KEY environment variable.")
        
        # Configure session headers
        self.session.headers.update({
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json;charset=utf-8'
        })
        
        # Genre mapping cache
        self.genre_map = {}
        self._load_genre_mapping()
        
        logger.info("✅ TMDB Data Source initialized successfully")
    
    def _load_genre_mapping(self):
        """Load genre ID to name mapping from TMDB"""
        try:
            # Movie genres
            movie_response = self.session.get(f"{self.base_url}/genre/movie/list")
            if movie_response.status_code == 200:
                movie_genres = movie_response.json().get('genres', [])
                for genre in movie_genres:
                    self.genre_map[genre['id']] = genre['name']
            
            # TV genres
            tv_response = self.session.get(f"{self.base_url}/genre/tv/list")
            if tv_response.status_code == 200:
                tv_genres = tv_response.json().get('genres', [])
                for genre in tv_genres:
                    self.genre_map[genre['id']] = genre['name']
                    
            logger.info(f"✅ Loaded {len(self.genre_map)} genre mappings")
            
        except Exception as e:
            logger.error(f"❌ Failed to load genre mapping: {e}")
            # Fallback genre mapping
            self.genre_map = {
                28: "Action", 35: "Comedy", 18: "Drama", 27: "Horror",
                10749: "Romance", 878: "Science Fiction", 53: "Thriller",
                9648: "Mystery", 14: "Fantasy", 80: "Crime"
            }
    
    def get_movie_data(self, page_limit: int = 100, min_vote_count: int = 100) -> pd.DataFrame:
        """
        Fetch movie data from TMDB and convert to Netflix format
        
        Args:
            page_limit: Maximum number of pages to fetch
            min_vote_count: Minimum vote count for quality filtering
            
        Returns:
            DataFrame in Netflix CSV format
        """
        logger.info(f"🎬 Fetching movie data from TMDB (up to {page_limit} pages)")
        
        movies_data = []
        
        for page in range(1, min(page_limit + 1, 501)):  # TMDB limit is 500 pages
            try:
                url = f"{self.base_url}/discover/movie"
                params = {
                    'page': page,
                    'sort_by': 'popularity.desc',
                    'vote_count.gte': min_vote_count,
                    'include_adult': 'false'
                }
                
                response = self.session.get(url, params=params)
                
                if response.status_code == 200:
                    data = response.json()
                    movies = data.get('results', [])
                    
                    if not movies:  # No more results
                        break
                    
                    for movie in movies:
                        # Get additional details
                        movie_details = self._get_movie_details(movie['id'])
                        
                        # Convert to Netflix format
                        netflix_format = self._convert_movie_to_netflix_format(movie, movie_details)
                        movies_data.append(netflix_format)
                    
                    logger.info(f"📄 Processed page {page}, total movies: {len(movies_data)}")
                    
                    # Rate limiting
                    time.sleep(0.1)
                    
                elif response.status_code == 429:  # Rate limited
                    logger.warning("⏱️ Rate limited, waiting 10 seconds...")
                    time.sleep(10)
                    continue
                else:
                    logger.error(f"❌ API error on page {page}: {response.status_code}")
                    break
                    
            except Exception as e:
                logger.error(f"❌ Error processing page {page}: {e}")
                continue
        
        df = pd.DataFrame(movies_data)
        logger.info(f"✅ Successfully fetched {len(df)} movies from TMDB")
        return df
    
    def get_tv_data(self, page_limit: int = 50, min_vote_count: int = 50) -> pd.DataFrame:
        """
        Fetch TV show data from TMDB and convert to Netflix format
        
        Args:
            page_limit: Maximum number of pages to fetch
            min_vote_count: Minimum vote count for quality filtering
            
        Returns:
            DataFrame in Netflix CSV format
        """
        logger.info(f"📺 Fetching TV show data from TMDB (up to {page_limit} pages)")
        
        tv_data = []
        
        for page in range(1, min(page_limit + 1, 501)):
            try:
                url = f"{self.base_url}/discover/tv"
                params = {
                    'page': page,
                    'sort_by': 'popularity.desc',
                    'vote_count.gte': min_vote_count,
                    'include_null_first_air_dates': 'false'
                }
                
                response = self.session.get(url, params=params)
                
                if response.status_code == 200:
                    data = response.json()
                    shows = data.get('results', [])
                    
                    if not shows:
                        break
                    
                    for show in shows:
                        # Get additional details
                        show_details = self._get_tv_details(show['id'])
                        
                        # Convert to Netflix format
                        netflix_format = self._convert_tv_to_netflix_format(show, show_details)
                        tv_data.append(netflix_format)
                    
                    logger.info(f"📄 Processed TV page {page}, total shows: {len(tv_data)}")
                    time.sleep(0.1)
                    
                elif response.status_code == 429:
                    logger.warning("⏱️ Rate limited, waiting 10 seconds...")
                    time.sleep(10)
                    continue
                else:
                    logger.error(f"❌ TV API error on page {page}: {response.status_code}")
                    break
                    
            except Exception as e:
                logger.error(f"❌ Error processing TV page {page}: {e}")
                continue
        
        df = pd.DataFrame(tv_data)
        logger.info(f"✅ Successfully fetched {len(df)} TV shows from TMDB")
        return df
    
    def get_combined_data(self, movie_pages: int = 50, tv_pages: int = 25) -> pd.DataFrame:
        """
        Get combined movie and TV show data
        
        Args:
            movie_pages: Number of movie pages to fetch
            tv_pages: Number of TV pages to fetch
            
        Returns:
            Combined DataFrame in Netflix format
        """
        logger.info("🎭 Fetching combined movie and TV data from TMDB")
        
        try:
            # Get movies and TV shows
            movies_df = self.get_movie_data(page_limit=movie_pages)
            tv_df = self.get_tv_data(page_limit=tv_pages)
            
            # Combine datasets
            combined_df = pd.concat([movies_df, tv_df], ignore_index=True)
            
            # Clean and validate data
            combined_df = self._clean_dataset(combined_df)
            
            logger.info(f"✅ Combined dataset: {len(movies_df)} movies + {len(tv_df)} TV shows = {len(combined_df)} total")
            return combined_df
            
        except Exception as e:
            logger.error(f"❌ Error creating combined dataset: {e}")
            return pd.DataFrame()
    
    def _get_movie_details(self, movie_id: int) -> Dict[str, Any]:
        """Get detailed movie information"""
        try:
            url = f"{self.base_url}/movie/{movie_id}"
            params = {'append_to_response': 'credits,production_countries'}
            
            response = self.session.get(url, params=params)
            
            if response.status_code == 200:
                return response.json()
            else:
                return {}
                
        except Exception as e:
            logger.warning(f"Failed to get movie details for {movie_id}: {e}")
            return {}
    
    def _get_tv_details(self, tv_id: int) -> Dict[str, Any]:
        """Get detailed TV show information"""
        try:
            url = f"{self.base_url}/tv/{tv_id}"
            params = {'append_to_response': 'credits,production_countries'}
            
            response = self.session.get(url, params=params)
            
            if response.status_code == 200:
                return response.json()
            else:
                return {}
                
        except Exception as e:
            logger.warning(f"Failed to get TV details for {tv_id}: {e}")
            return {}
    
    def _convert_movie_to_netflix_format(self, movie: Dict[str, Any], details: Dict[str, Any]) -> Dict[str, Any]:
        """Convert TMDB movie data to Netflix CSV format"""
        
        # Extract cast and crew
        credits = details.get('credits', {})
        cast_list = [member['name'] for member in credits.get('cast', [])[:5]]  # Top 5 cast
        crew_list = credits.get('crew', [])
        directors = [member['name'] for member in crew_list if member.get('job') == 'Director']
        
        # Extract countries
        countries = details.get('production_countries', [])
        country_names = [country['name'] for country in countries]
        
        # Map genres
        genre_names = [self.genre_map.get(genre_id, 'Unknown') for genre_id in movie.get('genre_ids', [])]
        
        # Determine rating based on adult flag and content
        rating = self._determine_rating(movie.get('adult', False), movie.get('overview', ''))
        
        return {
            'show_id': f"tm_movie_{movie['id']}",
            'type': 'Movie',
            'title': movie.get('title', 'Unknown Title'),
            'director': ', '.join(directors) if directors else 'Unknown Director',
            'cast': ', '.join(cast_list) if cast_list else 'Unknown Cast',
            'country': ', '.join(country_names) if country_names else 'United States',
            'date_added': datetime.now().strftime('%B %d, %Y'),
            'release_year': int(movie.get('release_date', '2023')[:4]) if movie.get('release_date') else 2023,
            'rating': rating,
            'duration': f"{details.get('runtime', 120)} min",
            'listed_in': ', '.join(genre_names) if genre_names else 'Drama',
            'description': movie.get('overview', 'No description available')[:500]  # Limit description length
        }
    
    def _convert_tv_to_netflix_format(self, show: Dict[str, Any], details: Dict[str, Any]) -> Dict[str, Any]:
        """Convert TMDB TV show data to Netflix CSV format"""
        
        # Extract cast and crew
        credits = details.get('credits', {})
        cast_list = [member['name'] for member in credits.get('cast', [])[:5]]
        crew_list = credits.get('crew', [])
        creators = [member['name'] for member in crew_list if member.get('job') in ['Creator', 'Executive Producer']]
        
        # Extract countries
        countries = details.get('production_countries', [])
        country_names = [country['name'] for country in countries]
        
        # Map genres
        genre_names = [self.genre_map.get(genre_id, 'Unknown') for genre_id in show.get('genre_ids', [])]
        
        # Determine seasons info
        number_of_seasons = details.get('number_of_seasons', 1)
        duration = f"{number_of_seasons} Season{'s' if number_of_seasons != 1 else ''}"
        
        # Determine rating
        rating = self._determine_rating(False, show.get('overview', ''))
        
        return {
            'show_id': f"tm_tv_{show['id']}",
            'type': 'TV Show',
            'title': show.get('name', 'Unknown Title'),
            'director': ', '.join(creators) if creators else 'Unknown Creator',
            'cast': ', '.join(cast_list) if cast_list else 'Unknown Cast',
            'country': ', '.join(country_names) if country_names else 'United States',
            'date_added': datetime.now().strftime('%B %d, %Y'),
            'release_year': int(show.get('first_air_date', '2023')[:4]) if show.get('first_air_date') else 2023,
            'rating': rating,
            'duration': duration,
            'listed_in': ', '.join(genre_names) if genre_names else 'Drama',
            'description': show.get('overview', 'No description available')[:500]
        }
    
    def _determine_rating(self, is_adult: bool, overview: str) -> str:
        """Determine content rating based on available information"""
        if is_adult:
            return 'R'
        
        # Simple content analysis for rating
        overview_lower = overview.lower()
        
        if any(word in overview_lower for word in ['violence', 'murder', 'kill', 'death', 'blood']):
            return 'R'
        elif any(word in overview_lower for word in ['teen', 'high school', 'young adult']):
            return 'PG-13'
        elif any(word in overview_lower for word in ['family', 'children', 'kid']):
            return 'PG'
        else:
            return 'PG-13'  # Default rating
    
    def _clean_dataset(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and validate the dataset"""
        logger.info("🧹 Cleaning and validating dataset...")
        
        # Remove duplicates
        initial_size = len(df)
        df = df.drop_duplicates(subset=['title', 'type'], keep='first')
        logger.info(f"🗑️ Removed {initial_size - len(df)} duplicates")
        
        # Clean text fields
        text_columns = ['title', 'director', 'cast', 'country', 'listed_in', 'description']
        for col in text_columns:
            if col in df.columns:
                df[col] = df[col].astype(str).str.strip()
                df[col] = df[col].replace('nan', 'Unknown')
        
        # Validate release years
        current_year = datetime.now().year
        df['release_year'] = pd.to_numeric(df['release_year'], errors='coerce')
        df.loc[df['release_year'] > current_year, 'release_year'] = current_year
        df.loc[df['release_year'] < 1900, 'release_year'] = 2000
        df['release_year'] = df['release_year'].fillna(2023).astype(int)
        
        # Ensure required fields are not empty
        df['title'] = df['title'].replace('Unknown Title', f'Title {df.index}')
        df['description'] = df['description'].fillna('No description available')
        
        logger.info(f"✅ Dataset cleaned: {len(df)} titles ready")
        return df
    
    def save_to_csv(self, df: pd.DataFrame, filename: str = 'tmdb_netflix_format.csv') -> str:
        """Save dataset to CSV file"""
        try:
            # Ensure data directory exists
            data_dir = Path('data')
            data_dir.mkdir(exist_ok=True)
            
            filepath = data_dir / filename
            df.to_csv(filepath, index=False, encoding='utf-8')
            
            logger.info(f"💾 Dataset saved to: {filepath}")
            logger.info(f"📊 File size: {filepath.stat().st_size / 1024 / 1024:.2f} MB")
            
            return str(filepath)
            
        except Exception as e:
            logger.error(f"❌ Failed to save dataset: {e}")
            return ""

# Utility functions
def create_tmdb_dataset(movie_pages: int = 50, tv_pages: int = 25, save_file: bool = True) -> pd.DataFrame:
    """
    Create a complete TMDB dataset in Netflix format
    
    Args:
        movie_pages: Number of movie pages to fetch
        tv_pages: Number of TV pages to fetch
        save_file: Whether to save the dataset to CSV
        
    Returns:
        Combined dataset DataFrame
    """
    try:
        tmdb = TMDBDataSource()
        df = tmdb.get_combined_data(movie_pages=movie_pages, tv_pages=tv_pages)
        
        if save_file and not df.empty:
            filename = f"tmdb_dataset_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            tmdb.save_to_csv(df, filename)
        
        return df
        
    except Exception as e:
        logger.error(f"❌ Failed to create TMDB dataset: {e}")
        return pd.DataFrame()

def test_tmdb_integration():
    """Test TMDB integration functionality"""
    logger.info("🧪 Testing TMDB Integration")
    logger.info("=" * 40)
    
    try:
        # Test API key
        tmdb = TMDBDataSource()
        logger.info("✅ TMDB API key validated")
        
        # Test small dataset
        df = tmdb.get_combined_data(movie_pages=2, tv_pages=1)
        
        if not df.empty:
            logger.info(f"✅ Successfully created dataset with {len(df)} titles")
            logger.info(f"📊 Dataset columns: {list(df.columns)}")
            logger.info(f"🎬 Movies: {len(df[df['type'] == 'Movie'])}")
            logger.info(f"📺 TV Shows: {len(df[df['type'] == 'TV Show'])}")
            
            # Show sample
            logger.info("\n📋 Sample titles:")
            for i, row in df.head(3).iterrows():
                logger.info(f"   {row['type']}: {row['title']} ({row['release_year']})")
                
            return True
        else:
            logger.error("❌ Failed to create dataset")
            return False
            
    except Exception as e:
        logger.error(f"❌ TMDB integration test failed: {e}")
        return False

if __name__ == "__main__":
    # Test the integration
    success = test_tmdb_integration()
    
    if success:
        print("\n🎉 TMDB Integration is working correctly!")
        print("💡 You can now use TMDB as a data source for your Netflix MCP Platform")
        print("\nTo create a full dataset, run:")
        print("python data_sources/tmdb_integration.py --create-dataset")
    else:
        print("\n❌ TMDB Integration test failed")
        print("💡 Please check your TMDB_API_KEY in the .env file")
