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

if __name__ == "__main__":
    pytest.main([__file__])

