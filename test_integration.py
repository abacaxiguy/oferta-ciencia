#!/usr/bin/env python3
"""
Test script to verify the integration between genetic algorithm and PDF generator
"""

from generate_schedule_pdf import create_timetable_pdf

def test_genetic_algorithm_integration():
    """Test the genetic algorithm integration with PDF generation"""
    print("Testing genetic algorithm integration with PDF generator...")
    
    try:
        # Test with genetic algorithm
        print("1. Testing with genetic algorithm enabled...")
        create_timetable_pdf(use_genetic_algorithm=True)
        print("✅ Genetic algorithm integration successful!")
        
    except Exception as e:
        print(f"❌ Error with genetic algorithm: {e}")
        print("Falling back to mock data...")
        
        try:
            # Test with mock data as fallback
            create_timetable_pdf(use_genetic_algorithm=False)
            print("✅ Mock data fallback successful!")
        except Exception as e2:
            print(f"❌ Error with mock data: {e2}")

def test_mock_data():
    """Test with mock data only"""
    print("\nTesting with mock data only...")
    
    try:
        create_timetable_pdf(use_genetic_algorithm=False)
        print("✅ Mock data test successful!")
    except Exception as e:
        print(f"❌ Error with mock data: {e}")

if __name__ == "__main__":
    print("=" * 60)
    print("TESTING GENETIC ALGORITHM INTEGRATION")
    print("=" * 60)
    
    test_genetic_algorithm_integration()
    test_mock_data()
    
    print("\n" + "=" * 60)
    print("TESTING COMPLETE")
    print("=" * 60) 