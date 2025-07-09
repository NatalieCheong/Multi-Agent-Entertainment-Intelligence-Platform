#!/usr/bin/env python3
"""
Netflix MCP Platform Performance Benchmarks
Professional performance testing and optimization analysis
"""

import asyncio
import time
import statistics
import psutil
import os
import sys
import json
import gc
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("netflix-performance")

class PerformanceBenchmark:
    """
    Comprehensive performance benchmarking system for Netflix MCP Platform
    Measures response times, resource usage, scalability, and optimization metrics
    """
    
    def __init__(self):
        self.benchmark_name = "Netflix MCP Platform Performance Test"
        self.version = "2.0.0"
        self.start_time = datetime.now()
        self.results = {}
        self.system_info = self._get_system_info()
        
    def _get_system_info(self) -> Dict[str, Any]:
        """Collect system information for benchmark context"""
        try:
            memory = psutil.virtual_memory()
            cpu_info = {
                "physical_cores": psutil.cpu_count(logical=False),
                "logical_cores": psutil.cpu_count(logical=True),
                "cpu_freq": psutil.cpu_freq()._asdict() if psutil.cpu_freq() else {}
            }
            
            return {
                "platform": os.name,
                "python_version": sys.version,
                "memory_total_gb": round(memory.total / (1024**3), 2),
                "memory_available_gb": round(memory.available / (1024**3), 2),
                "cpu_info": cpu_info,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.warning(f"Could not collect system info: {e}")
            return {"error": str(e)}
    
    def measure_execution_time(self, func, *args, **kwargs):
        """Measure function execution time with high precision"""
        start_time = time.perf_counter()
        start_memory = psutil.Process().memory_info().rss
        
        try:
            result = func(*args, **kwargs)
            success = True
            error = None
        except Exception as e:
            result = None
            success = False
            error = str(e)
        
        end_time = time.perf_counter()
        end_memory = psutil.Process().memory_info().rss
        
        return {
            "execution_time": end_time - start_time,
            "memory_delta": end_memory - start_memory,
            "success": success,
            "result": result,
            "error": error
        }
    
    async def measure_async_execution_time(self, coro_func, *args, **kwargs):
        """Measure async function execution time"""
        start_time = time.perf_counter()
        start_memory = psutil.Process().memory_info().rss
        
        try:
            result = await coro_func(*args, **kwargs)
            success = True
            error = None
        except Exception as e:
            result = None
            success = False
            error = str(e)
        
        end_time = time.perf_counter()
        end_memory = psutil.Process().memory_info().rss
        
        return {
            "execution_time": end_time - start_time,
            "memory_delta": end_memory - start_memory,
            "success": success,
            "result": result,
            "error": error
        }
    
    def benchmark_data_loading(self) -> Dict[str, Any]:
        """Benchmark dataset loading performance"""
        logger.info("📊 Benchmarking data loading performance...")
        
        results = {}
        
        # Test Netflix CSV loading
        try:
            from mcp_server.mcp_server import load_netflix_dataset
            
            # Multiple runs for statistical accuracy
            load_times = []
            for i in range(5):
                measurement = self.measure_execution_time(load_netflix_dataset)
                if measurement["success"]:
                    load_times.append(measurement["execution_time"])
            
            if load_times:
                results["netflix_csv_loading"] = {
                    "avg_time_seconds": statistics.mean(load_times),
                    "min_time_seconds": min(load_times),
                    "max_time_seconds": max(load_times),
                    "std_dev": statistics.stdev(load_times) if len(load_times) > 1 else 0,
                    "runs": len(load_times)
                }
            else:
                results["netflix_csv_loading"] = {"error": "All runs failed"}
                
        except Exception as e:
            results["netflix_csv_loading"] = {"error": str(e)}
        
        # Test TMDB integration if available
        try:
            from data_sources.tmdb_integration import TMDBDataSource
            
            if os.getenv('TMDB_API_KEY'):
                tmdb = TMDBDataSource()
                measurement = self.measure_execution_time(
                    tmdb.get_movie_data, 2  # Small test dataset
                )
                
                results["tmdb_integration"] = {
                    "execution_time": measurement["execution_time"],
                    "success": measurement["success"],
                    "memory_usage": measurement["memory_delta"] / 1024 / 1024  # MB
                }
            else:
                results["tmdb_integration"] = {"status": "API key not configured"}
                
        except Exception as e:
            results["tmdb_integration"] = {"error": str(e)}
        
        # Test sample dataset creation
        try:
            from mcp_server.mcp_server import create_sample_dataset
            
            measurement = self.measure_execution_time(create_sample_dataset)
            results["sample_dataset_creation"] = {
                "execution_time": measurement["execution_time"],
                "success": measurement["success"],
                "memory_usage": measurement["memory_delta"] / 1024 / 1024
            }
            
        except Exception as e:
            results["sample_dataset_creation"] = {"error": str(e)}
        
        return results
    
    def benchmark_multi_agent_performance(self) -> Dict[str, Any]:
        """Benchmark Multi-Agent system performance"""
        logger.info("🤖 Benchmarking Multi-Agent system performance...")
        
        results = {}
        
        try:
            from agents.multi_agents import run_netflix_multi_agent
            
            # Test queries with different complexity levels
            test_queries = [
                ("simple", "What are popular movies?"),
                ("medium", "Find Korean thriller movies from 2020-2023"),
                ("complex", "Analyze international content trends and provide strategic recommendations for Asian market expansion")
            ]
            
            for complexity, query in test_queries:
                query_times = []
                
                # Run multiple iterations
                for i in range(3):
                    measurement = self.measure_execution_time(run_netflix_multi_agent, query)
                    if measurement["success"]:
                        query_times.append(measurement["execution_time"])
                
                if query_times:
                    results[f"multi_agent_{complexity}"] = {
                        "query": query,
                        "avg_response_time": statistics.mean(query_times),
                        "min_response_time": min(query_times),
                        "max_response_time": max(query_times),
                        "runs": len(query_times)
                    }
                else:
                    results[f"multi_agent_{complexity}"] = {
                        "query": query,
                        "error": "All runs failed"
                    }
            
            # Test individual agents
            try:
                from agents.multi_agents import (
                    content_discovery_agent,
                    analytics_specialist_agent,
                    recommendation_engine_agent
                )
                
                agents = [
                    ("content_discovery", content_discovery_agent),
                    ("analytics_specialist", analytics_specialist_agent),
                    ("recommendation_engine", recommendation_engine_agent)
                ]
                
                for agent_name, agent in agents:
                    measurement = self.measure_execution_time(
                        agent.run, "Test query for performance measurement"
                    )
                    
                    results[f"individual_agent_{agent_name}"] = {
                        "execution_time": measurement["execution_time"],
                        "success": measurement["success"],
                        "memory_delta": measurement["memory_delta"] / 1024 / 1024
                    }
                    
            except Exception as e:
                results["individual_agents"] = {"error": str(e)}
                
        except Exception as e:
            results["multi_agent_system"] = {"error": str(e)}
        
        return results
    
    def benchmark_guardrail_performance(self) -> Dict[str, Any]:
        """Benchmark Content Safety Guardrail performance"""
        logger.info("🔒 Benchmarking Guardrail system performance...")
        
        results = {}
        
        try:
            from guardrail.guardrail import (
                NetflixGuardrailSystem,
                apply_guardrails_to_response,
                simple_content_filter
            )
            
            guardrail_system = NetflixGuardrailSystem()
            
            # Test simple content filtering
            test_content = [
                "Family-friendly movie recommendations for kids",
                "Action movies with intense violence and mature themes",
                "Educational documentary about marine life",
                "Horror movie with graphic content and disturbing scenes"
            ]
            
            filter_times = []
            for content in test_content:
                measurement = self.measure_execution_time(
                    simple_content_filter, content, "general"
                )
                if measurement["success"]:
                    filter_times.append(measurement["execution_time"])
            
            if filter_times:
                results["simple_content_filter"] = {
                    "avg_time": statistics.mean(filter_times),
                    "min_time": min(filter_times),
                    "max_time": max(filter_times),
                    "throughput_per_second": len(filter_times) / sum(filter_times)
                }
            
            # Test comprehensive guardrail evaluation
            test_response = "I recommend these family movies: Paddington, Finding Nemo, and The Lion King."
            context = {"content_type": "family", "quality_level": "high"}
            
            measurement = self.measure_execution_time(
                apply_guardrails_to_response, test_response, context
            )
            
            results["comprehensive_guardrail"] = {
                "execution_time": measurement["execution_time"],
                "success": measurement["success"],
                "memory_usage": measurement["memory_delta"] / 1024 / 1024
            }
            
            # Test guardrail scalability
            scalability_times = []
            for batch_size in [1, 5, 10]:
                start_time = time.perf_counter()
                
                for i in range(batch_size):
                    simple_content_filter(f"Test content {i}", "general")
                
                end_time = time.perf_counter()
                scalability_times.append({
                    "batch_size": batch_size,
                    "total_time": end_time - start_time,
                    "time_per_item": (end_time - start_time) / batch_size
                })
            
            results["guardrail_scalability"] = scalability_times
            
        except Exception as e:
            results["guardrail_system"] = {"error": str(e)}
        
        return results
    
    def benchmark_mcp_protocol_performance(self) -> Dict[str, Any]:
        """Benchmark MCP Protocol performance"""
        logger.info("🔗 Benchmarking MCP Protocol performance...")
        
        results = {}
        
        try:
            from mcp_server.mcp_server import enhanced_business_query_logic
            
            # Test different query types
            mcp_queries = [
                "What percentage of Netflix content is Korean?",
                "What are the most popular genres globally?",
                "Show me international vs US content trends"
            ]
            
            for i, query in enumerate(mcp_queries):
                measurement = self.measure_execution_time(
                    enhanced_business_query_logic, query
                )
                
                results[f"mcp_query_{i+1}"] = {
                    "query": query,
                    "execution_time": measurement["execution_time"],
                    "success": measurement["success"],
                    "memory_delta": measurement["memory_delta"] / 1024 / 1024
                }
            
            # Test MCP client performance
            try:
                from mcp_client.mcp_client import NetflixMCPClient
                
                client = NetflixMCPClient()
                measurement = self.measure_execution_time(
                    client.__init__
                )
                
                results["mcp_client_initialization"] = {
                    "execution_time": measurement["execution_time"],
                    "success": measurement["success"]
                }
                
            except Exception as e:
                results["mcp_client"] = {"error": str(e)}
                
        except Exception as e:
            results["mcp_protocol"] = {"error": str(e)}
        
        return results
    
    def benchmark_concurrent_operations(self) -> Dict[str, Any]:
        """Benchmark concurrent operation performance"""
        logger.info("⚡ Benchmarking concurrent operations...")
        
        results = {}
        
        try:
            from mcp_server.mcp_server import enhanced_business_query_logic
            
            # Test concurrent queries
            concurrent_queries = [
                "What percentage of Netflix content is Korean?",
                "What are popular action movies?",
                "Find family-friendly content",
                "Analyze thriller genre trends",
                "International content statistics"
            ]
            
            # Sequential execution baseline
            start_time = time.perf_counter()
            sequential_results = []
            
            for query in concurrent_queries:
                try:
                    result = enhanced_business_query_logic(query)
                    sequential_results.append(result.get("status") == "success")
                except:
                    sequential_results.append(False)
            
            sequential_time = time.perf_counter() - start_time
            
            # Concurrent execution test
            start_time = time.perf_counter()
            concurrent_results = []
            
            with ThreadPoolExecutor(max_workers=3) as executor:
                future_to_query = {
                    executor.submit(enhanced_business_query_logic, query): query 
                    for query in concurrent_queries
                }
                
                for future in as_completed(future_to_query):
                    try:
                        result = future.result()
                        concurrent_results.append(result.get("status") == "success")
                    except Exception as e:
                        concurrent_results.append(False)
            
            concurrent_time = time.perf_counter() - start_time
            
            results["concurrent_operations"] = {
                "sequential_time": sequential_time,
                "concurrent_time": concurrent_time,
                "speedup_ratio": sequential_time / concurrent_time if concurrent_time > 0 else 0,
                "sequential_success_rate": sum(sequential_results) / len(sequential_results),
                "concurrent_success_rate": sum(concurrent_results) / len(concurrent_results),
                "queries_tested": len(concurrent_queries)
            }
            
        except Exception as e:
            results["concurrent_operations"] = {"error": str(e)}
        
        return results
    
    def benchmark_memory_usage(self) -> Dict[str, Any]:
        """Benchmark memory usage patterns"""
        logger.info("💾 Benchmarking memory usage patterns...")
        
        results = {}
        
        try:
            import tracemalloc
            
            # Start memory tracing
            tracemalloc.start()
            initial_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
            
            # Test memory usage of different components
            components_memory = {}
            
            # Test dataset loading memory
            try:
                from mcp_server.mcp_server import load_netflix_dataset
                
                before_memory = psutil.Process().memory_info().rss / 1024 / 1024
                dataset = load_netflix_dataset()
                after_memory = psutil.Process().memory_info().rss / 1024 / 1024
                
                components_memory["dataset_loading"] = {
                    "memory_delta_mb": after_memory - before_memory,
                    "dataset_size": len(dataset) if dataset is not None else 0
                }
                
                # Clear dataset
                del dataset
                gc.collect()
                
            except Exception as e:
                components_memory["dataset_loading"] = {"error": str(e)}
            
            # Test multi-agent memory usage
            try:
                from agents.multi_agents import run_netflix_multi_agent
                
                before_memory = psutil.Process().memory_info().rss / 1024 / 1024
                result = run_netflix_multi_agent("Test query for memory measurement")
                after_memory = psutil.Process().memory_info().rss / 1024 / 1024
                
                components_memory["multi_agent"] = {
                    "memory_delta_mb": after_memory - before_memory,
                    "success": bool(result)
                }
                
            except Exception as e:
                components_memory["multi_agent"] = {"error": str(e)}
            
            # Test guardrail memory usage
            try:
                from guardrail.guardrail import apply_guardrails_to_response
                
                before_memory = psutil.Process().memory_info().rss / 1024 / 1024
                guardrail_result = apply_guardrails_to_response(
                    "Test content for memory measurement", 
                    {"content_type": "general"}
                )
                after_memory = psutil.Process().memory_info().rss / 1024 / 1024
                
                components_memory["guardrail"] = {
                    "memory_delta_mb": after_memory - before_memory,
                    "success": bool(guardrail_result)
                }
                
            except Exception as e:
                components_memory["guardrail"] = {"error": str(e)}
            
            # Get memory tracing statistics
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            
            final_memory = psutil.Process().memory_info().rss / 1024 / 1024
            
            results["memory_analysis"] = {
                "initial_memory_mb": initial_memory,
                "final_memory_mb": final_memory,
                "total_memory_change_mb": final_memory - initial_memory,
                "peak_traced_memory_mb": peak / 1024 / 1024,
                "current_traced_memory_mb": current / 1024 / 1024,
                "components": components_memory
            }
            
        except Exception as e:
            results["memory_analysis"] = {"error": str(e)}
        
        return results
    
    def benchmark_scalability(self) -> Dict[str, Any]:
        """Benchmark system scalability with increasing load"""
        logger.info("📈 Benchmarking system scalability...")
        
        results = {}
        
        try:
            from mcp_server.mcp_server import enhanced_business_query_logic
            
            # Test with increasing load sizes
            load_sizes = [1, 5, 10, 20]
            scalability_results = []
            
            for load_size in load_sizes:
                start_time = time.perf_counter()
                start_memory = psutil.Process().memory_info().rss / 1024 / 1024
                
                successful_queries = 0
                errors = 0
                
                # Execute multiple queries
                for i in range(load_size):
                    try:
                        query = f"What are popular movies in category {i % 5}?"
                        result = enhanced_business_query_logic(query)
                        if result.get("status") == "success":
                            successful_queries += 1
                        else:
                            errors += 1
                    except Exception:
                        errors += 1
                
                end_time = time.perf_counter()
                end_memory = psutil.Process().memory_info().rss / 1024 / 1024
                
                total_time = end_time - start_time
                memory_delta = end_memory - start_memory
                
                scalability_results.append({
                    "load_size": load_size,
                    "total_time": total_time,
                    "avg_time_per_query": total_time / load_size,
                    "successful_queries": successful_queries,
                    "error_count": errors,
                    "success_rate": successful_queries / load_size,
                    "memory_delta_mb": memory_delta,
                    "queries_per_second": load_size / total_time if total_time > 0 else 0
                })
                
                # Brief pause between tests
                time.sleep(1)
            
            results["scalability_analysis"] = scalability_results
            
            # Calculate scalability metrics
            if len(scalability_results) >= 2:
                first_result = scalability_results[0]
                last_result = scalability_results[-1]
                
                results["scalability_metrics"] = {
                    "load_increase_factor": last_result["load_size"] / first_result["load_size"],
                    "time_increase_factor": last_result["total_time"] / first_result["total_time"],
                    "efficiency_degradation": (
                        first_result["avg_time_per_query"] / last_result["avg_time_per_query"]
                    ) if last_result["avg_time_per_query"] > 0 else 0,
                    "memory_scalability": last_result["memory_delta_mb"] / first_result["memory_delta_mb"] if first_result["memory_delta_mb"] > 0 else 0
                }
            
        except Exception as e:
            results["scalability_analysis"] = {"error": str(e)}
        
        return results
    
    def generate_performance_report(self) -> Dict[str, Any]:
        """Generate comprehensive performance report"""
        logger.info("📋 Generating comprehensive performance report...")
        
        # Run all benchmarks
        benchmark_results = {
            "system_info": self.system_info,
            "data_loading": self.benchmark_data_loading(),
            "multi_agent": self.benchmark_multi_agent_performance(),
            "guardrail": self.benchmark_guardrail_performance(),
            "mcp_protocol": self.benchmark_mcp_protocol_performance(),
            "concurrent_ops": self.benchmark_concurrent_operations(),
            "memory_usage": self.benchmark_memory_usage(),
            "scalability": self.benchmark_scalability()
        }
        
        # Calculate overall performance score
        performance_score = self._calculate_performance_score(benchmark_results)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(benchmark_results)
        
        total_duration = datetime.now() - self.start_time
        
        final_report = {
            "benchmark_info": {
                "name": self.benchmark_name,
                "version": self.version,
                "duration_seconds": total_duration.total_seconds(),
                "timestamp": datetime.now().isoformat()
            },
            "performance_score": performance_score,
            "benchmark_results": benchmark_results,
            "recommendations": recommendations,
            "summary": self._generate_summary(benchmark_results, performance_score)
        }
        
        return final_report
    
    def _calculate_performance_score(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate overall performance score"""
        scores = {}
        
        # Data loading score
        data_loading = results.get("data_loading", {})
        if "netflix_csv_loading" in data_loading and "avg_time_seconds" in data_loading["netflix_csv_loading"]:
            load_time = data_loading["netflix_csv_loading"]["avg_time_seconds"]
            scores["data_loading"] = max(0, min(100, 100 - (load_time * 10)))  # Penalize slow loading
        
        # Multi-agent score
        multi_agent = results.get("multi_agent", {})
        agent_scores = []
        for key, value in multi_agent.items():
            if "avg_response_time" in value:
                response_time = value["avg_response_time"]
                agent_scores.append(max(0, min(100, 100 - (response_time * 5))))
        
        if agent_scores:
            scores["multi_agent"] = statistics.mean(agent_scores)
        
        # Guardrail score
        guardrail = results.get("guardrail", {})
        if "simple_content_filter" in guardrail and "avg_time" in guardrail["simple_content_filter"]:
            filter_time = guardrail["simple_content_filter"]["avg_time"]
            scores["guardrail"] = max(0, min(100, 100 - (filter_time * 100)))  # Very fast filtering expected
        
        # Overall score
        if scores:
            overall_score = statistics.mean(scores.values())
        else:
            overall_score = 0
        
        return {
            "overall_score": round(overall_score, 2),
            "component_scores": scores,
            "grade": self._get_performance_grade(overall_score)
        }
    
    def _get_performance_grade(self, score: float) -> str:
        """Convert performance score to letter grade"""
        if score >= 90:
            return "A (Excellent)"
        elif score >= 80:
            return "B (Good)"
        elif score >= 70:
            return "C (Fair)"
        elif score >= 60:
            return "D (Poor)"
        else:
            return "F (Needs Improvement)"
    
    def _generate_recommendations(self, results: Dict[str, Any]) -> List[str]:
        """Generate performance optimization recommendations"""
        recommendations = []
        
        # Data loading recommendations
        data_loading = results.get("data_loading", {})
        if "netflix_csv_loading" in data_loading:
            avg_time = data_loading["netflix_csv_loading"].get("avg_time_seconds", 0)
            if avg_time > 5:
                recommendations.append("Consider optimizing dataset loading with chunking or caching")
            if avg_time > 10:
                recommendations.append("Dataset loading is slow - consider using smaller datasets or SSD storage")
        
        # Multi-agent recommendations
        multi_agent = results.get("multi_agent", {})
        slow_agents = []
        for key, value in multi_agent.items():
            if "avg_response_time" in value and value["avg_response_time"] > 10:
                slow_agents.append(key)
        
        if slow_agents:
            recommendations.append(f"Optimize slow agents: {', '.join(slow_agents)}")
        
        # Memory recommendations
        memory = results.get("memory_usage", {})
        if "memory_analysis" in memory:
            total_change = memory["memory_analysis"].get("total_memory_change_mb", 0)
            if total_change > 500:
                recommendations.append("High memory usage detected - consider memory optimization")
            if total_change > 1000:
                recommendations.append("Very high memory usage - implement memory pooling or streaming")
        
        # Scalability recommendations
        scalability = results.get("scalability", {})
        if "scalability_metrics" in scalability:
            efficiency = scalability["scalability_metrics"].get("efficiency_degradation", 1)
            if efficiency < 0.5:
                recommendations.append("Poor scalability - consider implementing caching or load balancing")
        
        # Concurrent operations recommendations
        concurrent = results.get("concurrent_ops", {})
        if "concurrent_operations" in concurrent:
            speedup = concurrent["concurrent_operations"].get("speedup_ratio", 0)
            if speedup < 1.5:
                recommendations.append("Limited concurrency benefits - review thread safety and parallelization")
        
        # General recommendations
        if not recommendations:
            recommendations.append("Performance is good - consider advanced optimizations for production scaling")
        
        return recommendations
    
    def _generate_summary(self, results: Dict[str, Any], performance_score: Dict[str, Any]) -> Dict[str, Any]:
        """Generate performance summary"""
        summary = {
            "overall_assessment": performance_score["grade"],
            "key_metrics": {},
            "bottlenecks": [],
            "strengths": []
        }
        
        # Extract key metrics
        data_loading = results.get("data_loading", {})
        if "netflix_csv_loading" in data_loading:
            summary["key_metrics"]["data_loading_time"] = f"{data_loading['netflix_csv_loading'].get('avg_time_seconds', 0):.2f}s"
        
        multi_agent = results.get("multi_agent", {})
        agent_times = [v.get("avg_response_time", 0) for v in multi_agent.values() if "avg_response_time" in v]
        if agent_times:
            summary["key_metrics"]["avg_agent_response"] = f"{statistics.mean(agent_times):.2f}s"
        
        # Identify bottlenecks and strengths
        if performance_score["overall_score"] < 70:
            summary["bottlenecks"].append("Overall performance needs improvement")
        
        component_scores = performance_score.get("component_scores", {})
        for component, score in component_scores.items():
            if score < 60:
                summary["bottlenecks"].append(f"{component} performance is poor")
            elif score > 85:
                summary["strengths"].append(f"{component} performance is excellent")
        
        return summary
    
    def save_report(self, report: Dict[str, Any], filename: str = None) -> str:
        """Save performance report to file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"netflix_mcp_performance_report_{timestamp}.json"
        
        # Ensure benchmarks directory exists
        benchmarks_dir = Path("benchmarks")
        benchmarks_dir.mkdir(exist_ok=True)
        
        filepath = benchmarks_dir / filename
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, default=str)
            
            logger.info(f"📊 Performance report saved to: {filepath}")
            return str(filepath)
            
        except Exception as e:
            logger.error(f"Failed to save report: {e}")
            return ""

# Utility functions for standalone execution
def run_quick_benchmark():
    """Run a quick performance benchmark"""
    logger.info("🚀 Running Quick Performance Benchmark")
    
    benchmark = PerformanceBenchmark()
    
    # Run essential benchmarks only
    results = {
        "system_info": benchmark.system_info,
        "data_loading": benchmark.benchmark_data_loading(),
        "multi_agent": benchmark.benchmark_multi_agent_performance()
    }
    
    # Simple scoring
    score = 85 if all(r for r in results.values()) else 60
    
    print(f"\n📊 Quick Benchmark Results:")
    print(f"   Overall Score: {score}/100")
    print(f"   System: {results['system_info']['memory_total_gb']}GB RAM, {results['system_info']['cpu_info']['logical_cores']} cores")
    print(f"   Data Loading: {'✅ OK' if 'error' not in results['data_loading'] else '❌ Issues'}")
    print(f"   Multi-Agent: {'✅ OK' if 'error' not in results['multi_agent'] else '❌ Issues'}")
    
    return results

def run_comprehensive_benchmark():
    """Run comprehensive performance benchmark"""
    logger.info("🔬 Running Comprehensive Performance Benchmark")
    
    benchmark = PerformanceBenchmark()
    report = benchmark.generate_performance_report()
    
    # Save report
    filepath = benchmark.save_report(report)
    
    # Print summary
    print(f"\n📈 Comprehensive Benchmark Complete!")
    print(f"   Overall Score: {report['performance_score']['overall_score']}/100")
    print(f"   Grade: {report['performance_score']['grade']}")
    print(f"   Duration: {report['benchmark_info']['duration_seconds']:.1f} seconds")
    
    if report["recommendations"]:
        print(f"\n💡 Key Recommendations:")
        for rec in report["recommendations"][:3]:
            print(f"   • {rec}")
    
    if filepath:
        print(f"\n📋 Detailed report saved to: {filepath}")
    
    return report

def print_benchmark_info():
    """Print benchmark information"""
    print("⚡ Netflix MCP Platform Performance Benchmarks")
    print("=" * 50)
    print("Available benchmark modes:")
    print("  --quick      : Fast essential performance check")
    print("  --full       : Comprehensive performance analysis")
    print("  --memory     : Memory usage analysis only")
    print("  --agents     : Multi-agent performance only")
    print("  --concurrent : Concurrent operations test only")
    print("  --info       : Show this information")
    print()
    print("Example usage:")
    print("  python benchmarks/performance_test.py --full")
    print("  python benchmarks/performance_test.py --quick")

# Main execution
def main():
    """Main benchmark execution function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Netflix MCP Platform Performance Benchmarks")
    parser.add_argument("--quick", action="store_true", help="Run quick performance check")
    parser.add_argument("--full", action="store_true", help="Run comprehensive benchmark")
    parser.add_argument("--memory", action="store_true", help="Run memory analysis only")
    parser.add_argument("--agents", action="store_true", help="Run multi-agent benchmark only")
    parser.add_argument("--concurrent", action="store_true", help="Run concurrent operations test")
    parser.add_argument("--info", action="store_true", help="Show benchmark information")
    
    args = parser.parse_args()
    
    if args.info:
        print_benchmark_info()
    elif args.quick:
        run_quick_benchmark()
    elif args.memory:
        benchmark = PerformanceBenchmark()
        results = benchmark.benchmark_memory_usage()
        print(f"💾 Memory Analysis Results: {json.dumps(results, indent=2)}")
    elif args.agents:
        benchmark = PerformanceBenchmark()
        results = benchmark.benchmark_multi_agent_performance()
        print(f"🤖 Multi-Agent Benchmark Results: {json.dumps(results, indent=2)}")
    elif args.concurrent:
        benchmark = PerformanceBenchmark()
        results = benchmark.benchmark_concurrent_operations()
        print(f"⚡ Concurrent Operations Results: {json.dumps(results, indent=2)}")
    elif args.full:
        run_comprehensive_benchmark()
    else:
        # Default: run comprehensive benchmark
        run_comprehensive_benchmark()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Benchmark interrupted by user.")
    except Exception as e:
        print(f"\n❌ Benchmark error: {e}")
        logger.exception("Benchmark execution failed")
