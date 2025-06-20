#!/usr/bin/env python3
"""
Netflix Multi-Agents System - FastMCP Version
"""

import json
import pandas as pd
import numpy as np
from collections import Counter
import re
from datetime import datetime
from typing import Dict, List, Any, Optional
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI()

# Netflix Dataset Analysis Tools - FastMCP Compatible

def search_movies_shows(query: str, content_type: str = "both") -> str:
    """Search for movies and TV shows by title, cast, director, or genre"""
    try:
        # Simulated Netflix data search
        results = []
        
        query_lower = query.lower()
        
        if "action" in query_lower:
            results = [
                "The Old Guard (2020) - Action, Adventure - Charlize Theron",
                "Extraction (2020) - Action, Thriller - Chris Hemsworth", 
                "Red Notice (2021) - Action, Comedy - Dwayne Johnson, Ryan Reynolds",
                "The Gray Man (2022) - Action, Thriller - Ryan Gosling, Chris Evans"
            ]
        elif "comedy" in query_lower:
            results = [
                "The Kissing Booth (2018) - Comedy, Romance - Joey King",
                "To All the Boys I've Loved Before (2018) - Comedy, Romance - Lana Condor",
                "Murder Mystery (2019) - Comedy, Crime - Adam Sandler, Jennifer Aniston",
                "Red Notice (2021) - Action, Comedy - Dwayne Johnson"
            ]
        elif "documentary" in query_lower:
            results = [
                "My Octopus Teacher (2020) - Documentary - Nature",
                "The Social Dilemma (2020) - Documentary - Technology",
                "Dick Johnson Is Dead (2020) - Documentary - Personal Story",
                "Tiger King (2020) - Documentary Series - True Crime"
            ]
        elif "korean" in query_lower:
            results = [
                "Squid Game (2021) - Thriller, Drama - Lee Jung-jae",
                "Kingdom (2019) - Horror, Historical - Ju Ji-hoon",
                "Crash Landing on You (2019) - Romance, Drama - Hyun Bin",
                "Hellbound (2021) - Horror, Supernatural - Yoo Ah-in"
            ]
        elif "thriller" in query_lower:
            results = [
                "Squid Game (2021) - Thriller, Drama - Korean Series",
                "Ozark (2017-2022) - Crime, Thriller - Jason Bateman",
                "The Watcher (2022) - Psychological Thriller - Bobby Cannavale",
                "Dahmer (2022) - True Crime Thriller - Evan Peters"
            ]
        else:
            # General search results
            results = [
                f"Search results for '{query}': Stranger Things (Sci-Fi), The Crown (Drama), Bridgerton (Romance), Money Heist (Crime)"
            ]
        
        # Filter by content type
        if content_type == "movie":
            results = [r for r in results if "Season" not in r and "Series" not in r]
        elif content_type == "tv" or content_type == "show":
            results = [r for r in results if "Season" in r or "Series" in r or "Show" in r]
        
        return json.dumps({
            "status": "success",
            "query": query,
            "content_type": content_type,
            "total_results": len(results),
            "results": results[:10]  # Limit to top 10
        }, indent=2)
        
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})

def get_content_recommendations(preferences: str, age_rating: str = "all") -> str:
    """Get personalized content recommendations based on user preferences"""
    try:
        preferences_lower = preferences.lower()
        
        recommendations = {
            "action": [
                {"title": "Extraction 2 (2023)", "description": "Chris Hemsworth action thriller sequel", "rating": "R"},
                {"title": "The Gray Man (2022)", "description": "Ryan Gosling CIA operative thriller", "rating": "PG-13"},
                {"title": "6 Underground (2019)", "description": "Michael Bay explosive action", "rating": "R"},
                {"title": "The Old Guard (2020)", "description": "Immortal warriors action", "rating": "R"}
            ],
            "romance": [
                {"title": "Purple Hearts (2022)", "description": "Military romance drama", "rating": "PG-13"},
                {"title": "The Half of It (2020)", "description": "Coming-of-age romance", "rating": "PG-13"},
                {"title": "Always Be My Maybe (2019)", "description": "Romantic comedy", "rating": "R"},
                {"title": "To All the Boys (2018)", "description": "Teen romantic comedy", "rating": "PG-13"}
            ],
            "thriller": [
                {"title": "The Watcher (2022)", "description": "Psychological thriller series", "rating": "TV-MA"},
                {"title": "Dahmer (2022)", "description": "True crime thriller series", "rating": "TV-MA"}, 
                {"title": "Ozark (2017-2022)", "description": "Crime thriller series", "rating": "TV-MA"},
                {"title": "Squid Game (2021)", "description": "Korean survival thriller", "rating": "TV-MA"}
            ],
            "family": [
                {"title": "Enola Holmes (2020)", "description": "Family adventure mystery", "rating": "PG-13"},
                {"title": "The Princess Switch (2018)", "description": "Family romantic comedy", "rating": "TV-PG"},
                {"title": "A Christmas Prince (2017)", "description": "Family holiday romance", "rating": "TV-PG"},
                {"title": "The Willoughbys (2020)", "description": "Animated family film", "rating": "PG"}
            ],
            "comedy": [
                {"title": "Murder Mystery (2019)", "description": "Adam Sandler comedy", "rating": "PG-13"},
                {"title": "The Kissing Booth (2018)", "description": "Teen romantic comedy", "rating": "TV-14"},
                {"title": "Emily in Paris (2020)", "description": "Comedy romance series", "rating": "TV-MA"},
                {"title": "Space Force (2020)", "description": "Steve Carell comedy series", "rating": "TV-MA"}
            ],
            "korean": [
                {"title": "Squid Game (2021)", "description": "Survival thriller series", "rating": "TV-MA"},
                {"title": "Crash Landing on You (2019)", "description": "Romantic drama series", "rating": "TV-14"},
                {"title": "Kingdom (2019)", "description": "Historical zombie series", "rating": "TV-MA"},
                {"title": "Hellbound (2021)", "description": "Supernatural horror series", "rating": "TV-MA"}
            ],
            "international": [
                {"title": "Money Heist (Spain)", "description": "Crime thriller series", "rating": "TV-MA"},
                {"title": "Dark (Germany)", "description": "Sci-fi mystery series", "rating": "TV-MA"},
                {"title": "Lupin (France)", "description": "Mystery thriller series", "rating": "TV-MA"},
                {"title": "Sacred Games (India)", "description": "Crime thriller series", "rating": "TV-MA"}
            ]
        }
        
        # Find matching category
        selected_recs = []
        for category in recommendations.keys():
            if category in preferences_lower:
                selected_recs.extend(recommendations[category])
        
        # If no specific match, provide popular content
        if not selected_recs:
            selected_recs = recommendations["action"]  # Default to action
        
        # Filter by age rating if specified
        if age_rating != "all":
            if age_rating.lower() in ["family", "kids", "pg"]:
                selected_recs = [r for r in selected_recs if r["rating"] in ["G", "PG", "PG-13", "TV-G", "TV-PG", "TV-14"]]
            elif age_rating.lower() in ["teen"]:
                selected_recs = [r for r in selected_recs if r["rating"] in ["PG-13", "TV-14", "TV-MA"]]
        
        # Limit to top 5 recommendations
        selected_recs = selected_recs[:5]
        
        return json.dumps({
            "status": "success",
            "user_preferences": preferences,
            "age_rating": age_rating,
            "total_recommendations": len(selected_recs),
            "recommendations": selected_recs
        }, indent=2)
        
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})

def analyze_content_trends(year_range: str, genre: str = "all") -> str:
    """Analyze Netflix content trends by year and genre"""
    try:
        trend_data = {
            "2020-2023": {
                "total_content": "15,000+ titles added",
                "top_genres": ["Drama", "Comedy", "Action", "Documentary", "International"],
                "growth_trend": "40% increase in original content",
                "popular_regions": ["South Korea", "Spain", "India", "Brazil"],
                "key_insights": [
                    "Korean content viewership increased 370%",
                    "International content now represents 60% of viewing",
                    "Documentary viewership grew 180%",
                    "Mobile viewing increased 65%"
                ]
            },
            "2018-2020": {
                "total_content": "12,000+ titles added", 
                "top_genres": ["Comedy", "Drama", "Action", "Horror", "Romance"],
                "growth_trend": "25% increase in international content",
                "popular_regions": ["UK", "Canada", "Australia", "Mexico"],
                "key_insights": [
                    "Binge-watching behavior increased 45%",
                    "Original series outperformed licensed content",
                    "Mobile streaming adoption accelerated",
                    "Documentary category emerged as major growth area"
                ]
            },
            "2015-2018": {
                "total_content": "8,000+ titles added",
                "top_genres": ["Drama", "Comedy", "Action", "Romance", "Thriller"],
                "growth_trend": "Netflix Originals strategy launched",
                "popular_regions": ["United States", "UK", "Canada"],
                "key_insights": [
                    "Original content strategy proved successful",
                    "Global expansion accelerated",
                    "Cord-cutting trend accelerated",
                    "Streaming became mainstream"
                ]
            }
        }
        
        # Determine period based on year_range
        period = "2020-2023"  # Default
        if "2018" in year_range or "2019" in year_range:
            period = "2018-2020"
        elif "2015" in year_range or "2016" in year_range or "2017" in year_range:
            period = "2015-2018"
        
        data = trend_data[period]
        
        # Generate genre-specific insights if requested
        genre_analysis = {}
        if genre != "all":
            genre_lower = genre.lower()
            if genre_lower in ["action", "drama", "comedy", "thriller", "documentary"]:
                genre_analysis = {
                    "genre_focus": genre,
                    "market_share": f"{genre} represents approximately 15-20% of {period} content",
                    "growth_rate": f"{genre} content grew 25-45% during {period}",
                    "audience_engagement": f"{genre} shows 85%+ completion rates",
                    "regional_performance": f"Top performing regions for {genre}: Global appeal"
                }
        
        return json.dumps({
            "status": "success",
            "analysis_period": year_range,
            "genre_filter": genre,
            "trend_analysis": {
                "period": period,
                "content_volume": data["total_content"],
                "top_genres": data["top_genres"],
                "growth_trend": data["growth_trend"],
                "popular_regions": data["popular_regions"],
                "key_insights": data["key_insights"]
            },
            "genre_specific_analysis": genre_analysis if genre_analysis else None,
            "strategic_recommendations": [
                f"Continue investing in {data['popular_regions'][0]} content",
                f"Expand {data['top_genres'][0]} genre offerings",
                "Focus on mobile-optimized content",
                "Strengthen international co-productions"
            ]
        }, indent=2)
        
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})

def get_viewing_analytics(metric_type: str, time_period: str = "monthly") -> str:
    """Get Netflix viewing analytics and statistics"""
    try:
        analytics = {
            "popularity": {
                "top_content": [
                    "Stranger Things (2.65B hours)",
                    "Wednesday (1.72B hours)", 
                    "Squid Game (1.65B hours)",
                    "Dahmer (856M hours)",
                    "The Crown (744M hours)"
                ],
                "trending_now": [
                    "Ginny & Georgia",
                    "You",
                    "The Night Agent",
                    "Glass Onion"
                ],
                "time_period": time_period
            },
            "engagement": {
                "average_viewing_time": "2.1 hours per session",
                "completion_rates": {
                    "series": "73%",
                    "movies": "89%",
                    "documentaries": "65%",
                    "reality_shows": "78%"
                },
                "binge_watching": "45% of users watch 3+ episodes in one session",
                "replay_rate": "23% of content is rewatched",
                "time_period": time_period
            },
            "demographics": {
                "age_distribution": {
                    "18-34": "45%",
                    "35-54": "35%", 
                    "13-17": "12%",
                    "55+": "8%"
                },
                "viewing_patterns": {
                    "mobile": "65%",
                    "tv": "30%", 
                    "desktop": "5%"
                },
                "peak_hours": "7PM - 11PM local time",
                "weekend_boost": "25% increase in viewing time"
            },
            "regional": {
                "growth_markets": {
                    "Asia-Pacific": "+23%",
                    "Latin America": "+18%",
                    "Europe": "+12%",
                    "North America": "+8%"
                },
                "content_preferences": {
                    "Asia": "K-dramas, Anime, Local content",
                    "Europe": "Crime thrillers, Documentaries",
                    "Latin America": "Telenovelas, Reality shows",
                    "North America": "Original series, Movies"
                },
                "subscriber_metrics": f"Growing {time_period} across all regions"
            }
        }
        
        selected_analytics = analytics.get(metric_type, {
            "message": f"Analytics for {metric_type}: Data shows strong performance across all {time_period} metrics",
            "available_metrics": list(analytics.keys())
        })
        
        return json.dumps({
            "status": "success",
            "metric_type": metric_type,
            "time_period": time_period,
            "analytics_data": selected_analytics,
            "last_updated": datetime.now().strftime("%Y-%m-%d"),
            "data_source": "Netflix Global Analytics"
        }, indent=2)
        
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})

def predict_content_success(content_type: str, genre: str, target_audience: str) -> str:
    """Predict potential success of content based on historical data and trends"""
    try:
        success_factors = {
            "movie": {
                "action": {
                    "success_probability": "85%",
                    "target_demo": "18-34 male",
                    "key_factors": ["Star power", "VFX quality", "International appeal"],
                    "roi_estimate": "150-300%",
                    "risk_level": "Medium"
                },
                "romance": {
                    "success_probability": "92%", 
                    "target_demo": "18-45 female",
                    "key_factors": ["Chemistry", "Storytelling", "Diverse casting"],
                    "roi_estimate": "200-400%",
                    "risk_level": "Low"
                },
                "comedy": {
                    "success_probability": "78%",
                    "target_demo": "All demographics",
                    "key_factors": ["Cultural relevance", "Star comedian", "Repeat viewing"],
                    "roi_estimate": "120-250%",
                    "risk_level": "Medium"
                },
                "horror": {
                    "success_probability": "83%",
                    "target_demo": "16-35",
                    "key_factors": ["Original concept", "Jump scares", "Word of mouth"],
                    "roi_estimate": "180-350%",
                    "risk_level": "Medium-High"
                }
            },
            "series": {
                "drama": {
                    "success_probability": "94%",
                    "target_demo": "25-54",
                    "key_factors": ["Character development", "Season arcs", "Emotional depth"],
                    "roi_estimate": "250-500%",
                    "risk_level": "Low"
                },
                "thriller": {
                    "success_probability": "88%",
                    "target_demo": "18-44",
                    "key_factors": ["Plot twists", "Suspense", "Binge-ability"],
                    "roi_estimate": "200-400%",
                    "risk_level": "Medium"
                },
                "comedy": {
                    "success_probability": "85%",
                    "target_demo": "Broad appeal",
                    "key_factors": ["Ensemble cast", "Cultural zeitgeist", "Meme potential"],
                    "roi_estimate": "180-350%",
                    "risk_level": "Medium"
                },
                "documentary": {
                    "success_probability": "72%",
                    "target_demo": "25+ educated",
                    "key_factors": ["Timely topic", "Expert access", "Visual storytelling"],
                    "roi_estimate": "100-200%",
                    "risk_level": "Low-Medium"
                }
            }
        }
        
        # Get prediction data
        content_data = success_factors.get(content_type, {})
        genre_data = content_data.get(genre.lower(), {
            "success_probability": "65%",
            "target_demo": target_audience,
            "key_factors": ["Market research needed"],
            "roi_estimate": "100-180%",
            "risk_level": "High"
        })
        
        # Generate additional insights
        market_insights = []
        if "international" in target_audience.lower():
            market_insights.append("International content performs 40% better globally")
        if "young" in target_audience.lower() or "teen" in target_audience.lower():
            market_insights.append("Young adult content has 60% higher social media engagement")
        if "family" in target_audience.lower():
            market_insights.append("Family content has 80% higher repeat viewing rates")
        
        return json.dumps({
            "status": "success",
            "prediction_analysis": {
                "content_type": content_type,
                "genre": genre,
                "target_audience": target_audience,
                "success_probability": genre_data.get("success_probability", "65%"),
                "target_demographic": genre_data.get("target_demo", target_audience),
                "key_success_factors": genre_data.get("key_factors", []),
                "estimated_roi": genre_data.get("roi_estimate", "100-180%"),
                "risk_assessment": genre_data.get("risk_level", "Medium"),
                "market_insights": market_insights
            },
            "recommendations": [
                "Conduct focus group testing with target demographic",
                "Analyze competitor performance in similar genre",
                "Consider regional adaptation for international markets",
                "Plan comprehensive marketing strategy aligned with target audience"
            ],
            "confidence_score": "High" if float(genre_data.get("success_probability", "65%").rstrip("%")) > 80 else "Medium"
        }, indent=2)
        
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})

def get_netflix_faq(topic: str) -> str:
    """Get answers to frequently asked questions about Netflix"""
    try:
        faq_data = {
            "subscription": {
                "question": "Netflix subscription plans and pricing",
                "answer": "Netflix offers three main plans: Standard with ads ($6.99/month) - HD quality, 2 screens; Standard ($15.49/month) - HD quality, 2 screens, no ads; Premium ($22.99/month) - 4K UHD quality, 4 screens, no ads. All plans include unlimited movies and TV shows.",
                "additional_info": [
                    "Plans can be changed anytime",
                    "First month often discounted for new users",
                    "Student discounts not available",
                    "Annual payment options available in some regions"
                ]
            },
            "content": {
                "question": "Netflix content library and availability",
                "answer": "Netflix has 15,000+ titles globally, including original series, movies, documentaries, and international content. Content varies by region due to licensing agreements. Netflix Originals are available worldwide.",
                "additional_info": [
                    "New content added weekly",
                    "Original content available in 190+ countries",
                    "Content rotates based on licensing deals",
                    "Regional preferences influence local content"
                ]
            },
            "download": {
                "question": "Downloading content for offline viewing",
                "answer": "Download feature available on mobile app and Windows 10 app for offline viewing. Download limits vary by subscription tier: Basic (1 device), Standard (2 devices), Premium (4 devices).",
                "additional_info": [
                    "Downloads expire after 7 days offline",
                    "Some content has download restrictions",
                    "Downloads don't count against data usage when watching",
                    "Auto-download feature available for series"
                ]
            },
            "sharing": {
                "question": "Account sharing and household policies",
                "answer": "Netflix updated account sharing policies in 2023. Primary household can use account freely. Additional members outside household require extra member fees ($7.99/month in US).",
                "additional_info": [
                    "Household defined by IP address and device usage",
                    "Travel viewing allowed for account holders", 
                    "Profile management helps organize viewing",
                    "Kids profiles have parental controls"
                ]
            },
            "quality": {
                "question": "Streaming quality and technical requirements",
                "answer": "Streaming quality depends on plan and internet speed: Basic with ads (480p), Standard (1080p HD), Premium (4K UHD). Minimum 3 Mbps for SD, 5 Mbps for HD, 25 Mbps for 4K.",
                "additional_info": [
                    "Quality auto-adjusts based on connection",
                    "Data usage: SD (1GB/hour), HD (3GB/hour), 4K (7GB/hour)",
                    "Quality settings can be manually adjusted",
                    "HDR and Dolby Vision on compatible devices"
                ]
            },
            "originals": {
                "question": "Netflix Original content",
                "answer": "Netflix Originals are exclusive content produced or distributed solely by Netflix worldwide. Includes series, movies, documentaries, and specials from global creators.",
                "additional_info": [
                    "Award-winning original content",
                    "Available in 40+ languages",
                    "Investment exceeds $15 billion annually",
                    "Local originals in 30+ countries"
                ]
            },
            "cancel": {
                "question": "Canceling Netflix subscription",
                "answer": "Cancel anytime through Account settings. No cancellation fees. Access continues until end of current billing period. Can restart subscription anytime with same preferences.",
                "additional_info": [
                    "Viewing history and preferences saved for 10 months",
                    "Profiles and My List preserved during pause",
                    "Email notifications before account closure",
                    "Easy reactivation process"
                ]
            }
        }
        
        topic_lower = topic.lower()
        
        # Find matching FAQ
        selected_faq = None
        for key, faq in faq_data.items():
            if key in topic_lower or any(word in topic_lower for word in key.split()):
                selected_faq = faq
                break
        
        if not selected_faq:
            # Return general help if no specific match
            selected_faq = {
                "question": f"General Netflix help for: {topic}",
                "answer": "For detailed help with Netflix services, visit help.netflix.com or contact Netflix customer support directly through the app or website.",
                "additional_info": [
                    "24/7 customer support available",
                    "Live chat and phone support options",
                    "Comprehensive help center online",
                    "Community forums for user discussions"
                ]
            }
        
        return json.dumps({
            "status": "success",
            "topic": topic,
            "faq_response": selected_faq,
            "available_topics": list(faq_data.keys()),
            "help_resources": [
                "help.netflix.com",
                "Netflix mobile app help section",
                "Customer support chat",
                "Netflix community forums"
            ]
        }, indent=2)
        
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})

# Netflix Specialized Agent Classes - FastMCP Compatible

class NetflixAgent:
    """Base Netflix agent class using OpenAI directly"""
    
    def __init__(self, name: str, instructions: str, tools: List[str] = None, model: str = "gpt-4o-mini"):
        self.name = name
        self.instructions = instructions
        self.model = model
        self.tools = tools or []
        self.client = OpenAI()
    
    def run(self, user_input: str) -> str:
        """Run the agent with user input"""
        try:
            # Create messages
            messages = [
                {"role": "system", "content": self.instructions},
                {"role": "user", "content": user_input}
            ]
            
            # Call OpenAI
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=1500
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Error running agent {self.name}: {str(e)}"

# Create Netflix Specialized Agents

content_discovery_agent = NetflixAgent(
    name="Content Discovery Agent",
    instructions=(
        "You are a Netflix Content Discovery Agent. Help users find movies and TV shows based on their preferences. "
        "Use the available search and recommendation functions to provide personalized content suggestions. "
        "Consider user's genre preferences, age ratings, and viewing history. "
        "Provide detailed information about recommended content including plot summaries, cast, and ratings. "
        "Offer alternative suggestions if initial search doesn't match preferences. "
        "Always explain why you're recommending specific content."
    ),
    tools=["search_movies_shows", "get_content_recommendations"]
)

analytics_specialist_agent = NetflixAgent(
    name="Analytics Specialist Agent", 
    instructions=(
        "You are a Netflix Analytics Specialist. Provide comprehensive Netflix analytics and insights. "
        "Use trend analysis and viewing analytics to provide data-driven insights. "
        "Analyze content performance, viewer behavior, and market trends. "
        "Present data in clear, actionable insights with specific numbers and percentages. "
        "Compare historical trends with current performance. "
        "Provide strategic recommendations based on data analysis. "
        "Focus on business intelligence and competitive positioning."
    ),
    tools=["analyze_content_trends", "get_viewing_analytics", "predict_content_success"]
)

recommendation_engine_agent = NetflixAgent(
    name="Recommendation Engine Agent",
    instructions=(
        "You are a Netflix Recommendation Engine. Create personalized viewing recommendations for users. "
        "Use user preferences, demographics, and viewing patterns to suggest content. "
        "Consider factors like genre preferences, content ratings, international content, and trending shows. "
        "Explain why specific content is recommended based on user profile. "
        "Provide backup recommendations if primary suggestions don't appeal. "
        "Update recommendations based on user feedback and maintain conversation context."
    ),
    tools=["get_content_recommendations", "predict_content_success", "search_movies_shows"]
)

customer_support_agent = NetflixAgent(
    name="Customer Support Agent",
    instructions=(
        "You are a Netflix Customer Support Agent. Handle customer inquiries about Netflix services professionally. "
        "Provide clear, helpful information about subscriptions, features, plans, and policies. "
        "Use the FAQ knowledge base to answer common questions accurately. "
        "Maintain a friendly, professional customer service tone. "
        "Offer step-by-step solutions for common problems. "
        "Direct users to appropriate resources for technical issues requiring escalation. "
        "Always prioritize customer satisfaction and clear communication."
    ),
    tools=["get_netflix_faq"]
)

content_strategy_agent = NetflixAgent(
    name="Content Strategy Agent",
    instructions=(
        "You are a Netflix Content Strategy Agent. Provide strategic insights for content planning and acquisition. "
        "Use market trend analysis and success prediction for content investment decisions. "
        "Analyze audience behavior and engagement metrics for strategic planning. "
        "Recommend content strategies based on data, trends, and competitive analysis. "
        "Consider global and regional market dynamics in recommendations. "
        "Provide competitive analysis and positioning recommendations. "
        "Focus on ROI, market opportunities, and strategic growth initiatives."
    ),
    tools=["analyze_content_trends", "predict_content_success", "get_viewing_analytics"]
)

# Netflix Triage Agent - Routes to appropriate specialist
class NetflixTriageAgent(NetflixAgent):
    """Netflix Triage Agent that routes queries to appropriate specialists"""
    
    def __init__(self):
        super().__init__(
            name="Netflix Triage Agent",
            instructions=(
                "You are the Netflix Triage Agent. Welcome users and route their requests to appropriate specialists. "
                "Analyze user requests and determine the best agent to handle their query: "
                "- Content discovery/search → Content Discovery Agent "
                "- Analytics/insights/trends → Analytics Specialist Agent "
                "- Personalized recommendations → Recommendation Engine Agent "
                "- Customer support/FAQ → Customer Support Agent "
                "- Business strategy/content planning → Content Strategy Agent "
                "Gather necessary context and provide a smooth handoff with relevant information. "
                "If the query is complex, you can handle it directly using available tools."
            )
        )
        
        # Available agents for routing
        self.agents = {
            "content_discovery": content_discovery_agent,
            "analytics": analytics_specialist_agent,
            "recommendations": recommendation_engine_agent,
            "support": customer_support_agent,
            "strategy": content_strategy_agent
        }
        
        # Available tools
        self.available_tools = {
            "search_movies_shows": search_movies_shows,
            "get_content_recommendations": get_content_recommendations,
            "analyze_content_trends": analyze_content_trends,
            "get_viewing_analytics": get_viewing_analytics,
            "predict_content_success": predict_content_success,
            "get_netflix_faq": get_netflix_faq
        }
    
    def route_query(self, user_input: str) -> str:
        """Route user query to appropriate agent or handle directly"""
        try:
            user_input_lower = user_input.lower()
            
            # Determine which agent to use
            if any(word in user_input_lower for word in ["find", "search", "looking for", "show me", "discover"]):
                agent = self.agents["content_discovery"]
                response = agent.run(user_input)
                
                # Try to use actual tools if needed
                if "action" in user_input_lower or "comedy" in user_input_lower or "thriller" in user_input_lower:
                    try:
                        search_result = search_movies_shows(user_input, "both")
                        rec_result = get_content_recommendations(user_input)
                        return f"{response}\n\n📊 Search Results:\n{search_result}\n\n🎯 Recommendations:\n{rec_result}"
                    except:
                        pass
                return response
                
            elif any(word in user_input_lower for word in ["recommend", "suggest", "what should i watch", "preferences"]):
                agent = self.agents["recommendations"]
                response = agent.run(user_input)
                
                # Add actual recommendations
                try:
                    rec_result = get_content_recommendations(user_input)
                    return f"{response}\n\n🎯 Personalized Recommendations:\n{rec_result}"
                except:
                    pass
                return response
                
            elif any(word in user_input_lower for word in ["trend", "analytic", "data", "performance", "insight", "statistics"]):
                agent = self.agents["analytics"]
                response = agent.run(user_input)
                
                # Add actual analytics
                try:
                    if "trend" in user_input_lower:
                        trend_result = analyze_content_trends("2020-2023", "all")
                        return f"{response}\n\n📈 Trend Analysis:\n{trend_result}"
                    elif "viewing" in user_input_lower or "engagement" in user_input_lower:
                        analytics_result = get_viewing_analytics("engagement", "monthly")
                        return f"{response}\n\n📊 Viewing Analytics:\n{analytics_result}"
                except:
                    pass
                return response
                
            elif any(word in user_input_lower for word in ["plan", "subscription", "price", "cancel", "help", "support", "faq"]):
                agent = self.agents["support"]
                response = agent.run(user_input)
                
                # Add actual FAQ
                try:
                    if "plan" in user_input_lower or "subscription" in user_input_lower:
                        faq_result = get_netflix_faq("subscription")
                        return f"{response}\n\n💡 Detailed Information:\n{faq_result}"
                    elif "download" in user_input_lower:
                        faq_result = get_netflix_faq("download")
                        return f"{response}\n\n💡 Download Information:\n{faq_result}"
                except:
                    pass
                return response
                
            elif any(word in user_input_lower for word in ["strategy", "business", "investment", "market", "acquisition", "compete"]):
                agent = self.agents["strategy"]
                response = agent.run(user_input)
                
                # Add actual strategy analysis
                try:
                    if "predict" in user_input_lower or "success" in user_input_lower:
                        predict_result = predict_content_success("series", "drama", "international")
                        return f"{response}\n\n🎯 Success Prediction:\n{predict_result}"
                except:
                    pass
                return response
                
            else:
                # Handle general queries with triage agent
                general_response = super().run(user_input)
                
                # Try to provide some helpful tools
                try:
                    rec_result = get_content_recommendations("popular content")
                    return f"{general_response}\n\n🎬 Popular Content Recommendations:\n{rec_result}"
                except:
                    pass
                return general_response
                
        except Exception as e:
            return f"Netflix Triage Agent encountered an error: {str(e)}. Please try rephrasing your query."

# Create the main triage agent instance
netflix_triage_agent = NetflixTriageAgent()

# Main multi-agent runner function
def run_netflix_multi_agent(user_input: str) -> str:
    """Run Netflix multi-agent system with user input"""
    try:
        print(f"🎬 Netflix Multi-Agent System Processing: {user_input}")
        result = netflix_triage_agent.route_query(user_input)
        print("✅ Multi-agent processing complete")
        return result
    except Exception as e:
        error_msg = f"Error in Netflix multi-agent system: {str(e)}"
        print(f"❌ {error_msg}")
        return error_msg

def test_netflix_multi_agents():
    """Test the Netflix multi-agent system"""
    print("🎬 Testing Netflix Multi-Agent System (FastMCP Version)")
    print("=" * 60)
    
    test_queries = [
        "I'm looking for action movies with good ratings",
        "What are the latest trends in thriller content?", 
        "Recommend some Korean dramas for me",
        "What are Netflix subscription plans?",
        "What content should Netflix focus on for international markets?"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n🧪 Test {i}: {query}")
        print("-" * 40)
        try:
            result = run_netflix_multi_agent(query)
            print(f"✅ Result: {result[:200]}...")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n✅ Netflix Multi-Agent System Test Complete!")

# Individual tool test functions
def test_search_tool():
    """Test search tool"""
    print("🔍 Testing Search Tool:")
    result = search_movies_shows("action movies")
    print(result)

def test_recommendations_tool():
    """Test recommendations tool"""
    print("🎯 Testing Recommendations Tool:")
    result = get_content_recommendations("Korean dramas and comedies")
    print(result)

def test_analytics_tool():
    """Test analytics tool"""
    print("📊 Testing Analytics Tool:")
    result = analyze_content_trends("2020-2023", "thriller")
    print(result)

def test_faq_tool():
    """Test FAQ tool"""
    print("❓ Testing FAQ Tool:")
    result = get_netflix_faq("subscription")
    print(result)

# Main execution for Google Colab
if __name__ == "__main__":
    print("🎬 Netflix Multi-Agents System (FastMCP Compatible)")
    print("📊 6 Tools + 5 Specialized Agents + 1 Triage Agent")
    print("🚀 Ready for Google Colab execution!")
    print("=" * 60)
    print("🧪 Available test functions:")
    print("   • test_netflix_multi_agents() - Full system test")
    print("   • test_search_tool() - Test search functionality")
    print("   • test_recommendations_tool() - Test recommendations")
    print("   • test_analytics_tool() - Test analytics")
    print("   • test_faq_tool() - Test FAQ system")
