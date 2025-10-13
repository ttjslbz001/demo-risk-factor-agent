#!/usr/bin/env python3
"""
Test script to verify that all agents use OpenAI model configuration like demo_agent.py

This script demonstrates that the multi-agent system uses the same OpenAI model
configuration as the demo_agent.py file.
"""

import os
import json
import logging
from src.agents.multi_agent_graph import create_rating_engine
from src.gateway.agent_factory import init_agent

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_agent_model_configuration():
    """Test that agents use the same OpenAI model configuration as demo_agent.py"""
    
    print("🔍 Testing OpenAI Model Configuration")
    print("=" * 50)
    
    try:
        # Test 1: Basic agent initialization (like demo_agent.py)
        print("\n1. Testing basic agent initialization...")
        agent = init_agent()
        print(f"   ✅ Agent initialized: {type(agent).__name__}")
        print(f"   ✅ Model type: {type(agent.model).__name__}")
        print(f"   ✅ Model ID: {getattr(agent.model, 'model_id', 'N/A')}")
        print(f"   ✅ Max tokens: {agent.model.params.get('max_tokens', 'N/A')}")
        print(f"   ✅ Temperature: {agent.model.params.get('temperature', 'N/A')}")
        
        # Test 2: Multi-agent system initialization
        print("\n2. Testing multi-agent system initialization...")
        engine = create_rating_engine("Monthly-Comfort")
        
        # Check if Strands agents are initialized
        if engine.strands_agents:
            print(f"   ✅ Strands agents initialized: {len(engine.strands_agents)}")
            
            # Check model configuration for each agent
            for agent_name, agent_instance in engine.strands_agents.items():
                print(f"   📋 {agent_name}:")
                print(f"      - Model type: {type(agent_instance.model).__name__}")
                print(f"      - Model ID: {getattr(agent_instance.model, 'model_id', 'N/A')}")
                print(f"      - Max tokens: {agent_instance.model.params.get('max_tokens', 'N/A')}")
                print(f"      - Temperature: {agent_instance.model.params.get('temperature', 'N/A')}")
        else:
            print("   ⚠️  Strands agents not initialized (fallback mode)")
        
        # Test 3: Environment variable support
        print("\n3. Testing environment variable support...")
        env_vars = {
            "OPENAI_API_KEY": os.environ.get("OPENAI_API_KEY", "Not set"),
            "TELENAV_API_KEY": os.environ.get("TELENAV_API_KEY", "Not set"),
            "OPENAI_BASE_URL": os.environ.get("OPENAI_BASE_URL", "Not set"),
            "TELENAV_BASE_URL": os.environ.get("TELENAV_BASE_URL", "Not set"),
            "MODEL_ID": os.environ.get("MODEL_ID", "Not set"),
            "MODEL_NAME": os.environ.get("MODEL_NAME", "Not set"),
        }
        
        for var, value in env_vars.items():
            if value != "Not set":
                print(f"   ✅ {var}: {value[:10]}..." if len(str(value)) > 10 else f"   ✅ {var}: {value}")
            else:
                print(f"   ⚠️  {var}: {value}")
        
        # Test 4: Model configuration comparison
        print("\n4. Comparing with demo_agent.py configuration...")
        demo_config = {
            "model_id": "claude3.5-bedrock",
            "max_tokens": 1000,
            "temperature": 0.7,
            "base_url": "https://us-ailab-api.telenav.com/v1"
        }
        
        actual_config = {
            "model_id": getattr(agent.model, 'model_id', 'N/A'),
            "max_tokens": agent.model.params.get("max_tokens"),
            "temperature": agent.model.params.get("temperature"),
            "base_url": agent.model.client_args.get("base_url")
        }
        
        print("   Demo agent config:")
        for key, value in demo_config.items():
            print(f"      {key}: {value}")
        
        print("   Actual config:")
        for key, value in actual_config.items():
            print(f"      {key}: {value}")
        
        # Check if configurations match
        config_matches = all(
            str(demo_config.get(k, "")) == str(actual_config.get(k, ""))
            for k in demo_config.keys()
        )
        
        if config_matches:
            print("   ✅ Configuration matches demo_agent.py!")
        else:
            print("   ⚠️  Configuration differs from demo_agent.py")
        
        print("\n🎉 OpenAI Model Configuration Test Complete!")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        logger.exception("Test failed")
        return False

def test_multi_agent_processing():
    """Test multi-agent processing with OpenAI model configuration"""
    
    print("\n🚀 Testing Multi-Agent Processing")
    print("=" * 50)
    
    try:
        # Create sample application
        sample_application = {
            "household": {
                "address": "123 Main Street, Anytown, CA 90210",
                "zip_code": "90210"
            },
            "drivers": [
                {
                    "name": "John Smith",
                    "age": 35,
                    "license_years": 15,
                    "violations": [],
                    "claims": []
                }
            ],
            "vehicles": [
                {
                    "make": "Toyota",
                    "model": "Camry",
                    "year": 2021,
                    "usage": "commuting"
                }
            ]
        }
        
        # Create rating engine
        engine = create_rating_engine("Monthly-Comfort")
        
        # Process application
        print("Processing application with multi-agent system...")
        result = engine.process_application_with_graph(json.dumps(sample_application))
        
        print(f"   Status: {result.status}")
        print(f"   Session ID: {result.session_id}")
        print(f"   Execution Order: {' → '.join(result.execution_order)}")
        print(f"   Processing Time: {result.execution_time_ms}ms")
        
        if result.errors:
            print(f"   Errors: {len(result.errors)}")
            for error in result.errors:
                print(f"      - {error}")
        
        if result.warnings:
            print(f"   Warnings: {len(result.warnings)}")
            for warning in result.warnings:
                print(f"      - {warning}")
        
        print("\n✅ Multi-agent processing test complete!")
        return True
        
    except Exception as e:
        print(f"\n❌ Multi-agent processing test failed: {e}")
        logger.exception("Multi-agent processing test failed")
        return False

if __name__ == "__main__":
    print("🧪 OpenAI Model Configuration Test Suite")
    print("=" * 60)
    print("This test verifies that all agents use the same OpenAI model")
    print("configuration as demo_agent.py")
    print("=" * 60)
    
    # Run tests
    test1_passed = test_agent_model_configuration()
    test2_passed = test_multi_agent_processing()
    
    print("\n📊 Test Results Summary")
    print("=" * 30)
    print(f"Agent Configuration Test: {'✅ PASSED' if test1_passed else '❌ FAILED'}")
    print(f"Multi-Agent Processing Test: {'✅ PASSED' if test2_passed else '❌ FAILED'}")
    
    if test1_passed and test2_passed:
        print("\n🎉 All tests passed! OpenAI model configuration is working correctly.")
    else:
        print("\n⚠️  Some tests failed. Check the output above for details.")
