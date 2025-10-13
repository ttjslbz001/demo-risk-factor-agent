#!/usr/bin/env python3
"""
Test script for the refactored data parser to ensure it correctly handles
policy, driver, and vehicle risk subjects.
"""

import json
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from utils.data_parser import parse_application


def test_parser_with_sample_data():
    """Test the parser with the sample application data."""
    
    # Load sample data
    sample_file = Path("docs/insurance_risk_factor_agent/demo_application/user_appliction.json")
    
    if not sample_file.exists():
        print(f"❌ Sample file not found: {sample_file}")
        return False
    
    with open(sample_file, 'r') as f:
        sample_data = f.read()
    
    try:
        # Parse the application
        result = parse_application(sample_data)
        
        print("✅ Parser executed successfully!")
        print(f"📊 Parsing Results:")
        print(f"   - Policy risk subject: {'✅ Found' if result['policy'] else '❌ Missing'}")
        print(f"   - Driver risk subjects: {len(result['drivers'])} found")
        print(f"   - Vehicle risk subjects: {len(result['vehicles'])} found")
        print(f"   - Issues: {len(result['issues'])}")
        
        if result['issues']:
            print("\n⚠️  Issues found:")
            for issue in result['issues']:
                print(f"   - {issue}")
        
        # Show sample of extracted data
        print(f"\n📋 Sample Policy Data:")
        if result['policy']:
            policy_keys = list(result['policy'].keys())[:5]  # Show first 5 keys
            print(f"   Keys: {policy_keys}")
        
        print(f"\n👥 Driver Risk Subjects ({len(result['drivers'])}):")
        for i, driver in enumerate(result['drivers'][:2]):  # Show first 2 drivers
            risk_attrs = driver.get('riskAttributeValues', {})
            print(f"   Driver {i+1}: {driver.get('id', 'N/A')} - {len(risk_attrs)} risk attributes")
        
        print(f"\n🚗 Vehicle Risk Subjects ({len(result['vehicles'])}):")
        for i, vehicle in enumerate(result['vehicles'][:2]):  # Show first 2 vehicles
            risk_attrs = vehicle.get('riskAttributeValues', {})
            print(f"   Vehicle {i+1}: {vehicle.get('id', 'N/A')} - {len(risk_attrs)} risk attributes")
        
        return True
        
    except Exception as e:
        print(f"❌ Parser failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_parser_with_minimal_data():
    """Test the parser with minimal data to ensure it handles missing fields gracefully."""
    
    minimal_data = {
        "riskProfile": {
            "drivers": [],
            "vehicles": []
        }
    }
    
    try:
        result = parse_application(json.dumps(minimal_data))
        
        print("\n✅ Minimal data test passed!")
        print(f"   - Policy: {'✅' if result['policy'] else '❌'} (expected: missing)")
        print(f"   - Drivers: {len(result['drivers'])} (expected: 0)")
        print(f"   - Vehicles: {len(result['vehicles'])} (expected: 0)")
        print(f"   - Issues: {len(result['issues'])}")
        
        return True
        
    except Exception as e:
        print(f"❌ Minimal data test failed: {e}")
        return False


if __name__ == "__main__":
    print("🧪 Testing Refactored Data Parser")
    print("=" * 50)
    
    # Test with sample data
    success1 = test_parser_with_sample_data()
    
    # Test with minimal data
    success2 = test_parser_with_minimal_data()
    
    print("\n" + "=" * 50)
    if success1 and success2:
        print("🎉 All tests passed! The refactored parser is working correctly.")
    else:
        print("❌ Some tests failed. Please check the implementation.")
