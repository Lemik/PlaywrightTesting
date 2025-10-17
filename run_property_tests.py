#!/usr/bin/env python3
"""
Test runner script for property functionality tests.
This script provides an easy way to run property-related tests with proper configuration.
"""

import os
import sys
import subprocess
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables at the top level
load_dotenv(override=True)

def run_property_tests():
    """Run property functionality tests with proper configuration."""
    
    # Ensure we're in the correct directory
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # Check if required environment variables are set
    url = os.getenv('URL')
    landlord_email = os.getenv('LANDLORD_USER_EMAIL')
    landlord_password = os.getenv('LANDLORD_USER_PASSWORD')
    
    print(f"🔍 Environment check:")
    print(f"   URL: {'✅ Set' if url else '❌ Not set'}")
    print(f"   LANDLORD_USER_EMAIL: {'✅ Set' if landlord_email else '❌ Not set'}")
    print(f"   LANDLORD_USER_PASSWORD: {'✅ Set' if landlord_password else '❌ Not set'}")
    
    if not url:
        print("❌ Error: URL environment variable not set. Please check your .env file.")
        sys.exit(1)
    
    if not landlord_email or not landlord_password:
        print("❌ Error: LANDLORD_USER_EMAIL and LANDLORD_USER_PASSWORD environment variables not set.")
        print("Please check your .env file.")
        sys.exit(1)
    
    print("🚀 Starting Property Functionality Tests")
    print(f"📍 Testing URL: {url}")
    print("=" * 50)
    
    # Run the property tests
    test_files = [
        "tests/test_property_functionality.py",
        "tests/test_landlord_property.py"
    ]
    
    for test_file in test_files:
        if Path(test_file).exists():
            print(f"\n📋 Running tests from: {test_file}")
            print("-" * 30)
            
            try:
                # Run pytest with specific test file
                result = subprocess.run([
                    "python", "-m", "pytest", 
                    test_file,
                    "-v",  # Verbose output
                    "--tb=short",  # Short traceback format
                    "--capture=no"  # Show print statements
                ], capture_output=False, text=True)
                
                if result.returncode == 0:
                    print(f"✅ Tests in {test_file} completed successfully")
                else:
                    print(f"❌ Tests in {test_file} failed")
                    
            except Exception as e:
                print(f"❌ Error running tests in {test_file}: {e}")
        else:
            print(f"⚠️  Test file not found: {test_file}")
    
    print("\n" + "=" * 50)
    print("🏁 Property functionality tests completed!")

def run_specific_test(test_name):
    """Run a specific test by name."""
    
    # Ensure we're in the correct directory
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    print(f"🎯 Running specific test: {test_name}")
    print("=" * 50)
    
    try:
        result = subprocess.run([
            "python", "-m", "pytest", 
            f"tests/test_property_functionality.py::{test_name}",
            "-v",
            "--tb=short",
            "--capture=no"
        ], capture_output=False, text=True)
        
        if result.returncode == 0:
            print(f"✅ Test '{test_name}' completed successfully")
        else:
            print(f"❌ Test '{test_name}' failed")
            
    except Exception as e:
        print(f"❌ Error running test '{test_name}': {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Run specific test
        test_name = sys.argv[1]
        run_specific_test(test_name)
    else:
        # Run all property tests
        run_property_tests() 