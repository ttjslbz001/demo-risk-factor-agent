"""
Test script for risk_subject_iter function
"""

from risk_subject_ite import risk_subject_iter, AZ_HARDCODE_RISK_SUBJECT_MAP

def main():
    print("🔍 Testing risk_subject_iter function")
    print("=" * 60)
    
    # Call the function
    result = risk_subject_iter(profile=None, risk_subject_mapping={})
    
    # Display results
    print(f"\n📊 Results Summary:")
    print(f"   Total risk factors: {len(AZ_HARDCODE_RISK_SUBJECT_MAP)}")
    print(f"   Driver/Household factors: {len(result['driver'])}")
    print(f"   Vehicle factors: {len(result['vehicle'])}")
    
    # Show driver/household factors
    print(f"\n👤 Driver/Household Risk Factors ({len(result['driver'])} total):")
    for i, factor in enumerate(result['driver'], 1):
        print(f"   {i}. {factor['risk_factor_name']} ({factor['subject_type']})")
    
    # Show vehicle factors (first 10 only)
    print(f"\n🚗 Vehicle Risk Factors ({len(result['vehicle'])} total, showing first 10):")
    for i, factor in enumerate(result['vehicle'][:10], 1):
        print(f"   {i}. {factor['risk_factor_name']} ({factor['subject_type']})")
    
    if len(result['vehicle']) > 10:
        print(f"   ... and {len(result['vehicle']) - 10} more vehicle factors")
    
    # Verify categorization
    print(f"\n✅ Verification:")
    all_categorized = len(result['driver']) + len(result['vehicle'])
    print(f"   All factors categorized: {all_categorized == len(AZ_HARDCODE_RISK_SUBJECT_MAP)}")
    
    # Show breakdown by original subject type
    driver_count = sum(1 for f in result['driver'] if f['subject_type'] == 'driver')
    household_count = sum(1 for f in result['driver'] if f['subject_type'] == 'household')
    vehicle_count = sum(1 for f in result['vehicle'] if f['subject_type'] == 'vehicle')
    
    print(f"\n📈 Breakdown:")
    print(f"   Driver type → result['driver']: {driver_count}")
    print(f"   Household type → result['driver']: {household_count}")
    print(f"   Vehicle type → result['vehicle']: {vehicle_count}")

if __name__ == "__main__":
    main()



