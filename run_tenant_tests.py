#!/usr/bin/env python3
"""
Tenant Tests Runner

This script runs the tenant functionality tests specifically.
It provides a convenient way to test the /tenants page functionality.

Usage:
    python run_tenant_tests.py
    python run_tenant_tests.py --verbose
    python run_tenant_tests.py --headed
"""

import subprocess
import sys
import argparse
import os
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description='Run tenant functionality tests')
    parser.add_argument('--verbose', '-v', action='store_true', help='Run tests in verbose mode')
    parser.add_argument('--headed', action='store_true', help='Run tests in headed mode (show browser)')
    parser.add_argument('--slow-mo', type=int, default=100, help='Slow down Playwright operations (milliseconds)')
    parser.add_argument('--workers', type=int, default=1, help='Number of test workers')
    parser.add_argument('--retries', type=int, default=1, help='Number of retries for failed tests')
    
    args = parser.parse_args()
    
    # Build pytest command
    cmd = [
        'python', '-m', 'pytest',
        'tests/test_tenant_functionality.py',
        '--tb=short'
    ]
    
    if args.verbose:
        cmd.append('-v')
    
    if args.headed:
        cmd.extend(['--headed'])
    
    cmd.extend([
        '--slow-mo', str(args.slow_mo),
        '--workers', str(args.workers),
        '--retries', str(args.retries)
    ])
    
    print("Running tenant functionality tests...")
    print(f"Command: {' '.join(cmd)}")
    print("-" * 50)
    
    try:
        result = subprocess.run(cmd, check=True)
        print("-" * 50)
        print("✅ All tenant tests passed!")
        return 0
    except subprocess.CalledProcessError as e:
        print("-" * 50)
        print(f"❌ Some tenant tests failed with exit code: {e.returncode}")
        return e.returncode
    except KeyboardInterrupt:
        print("\n⚠️  Tests interrupted by user")
        return 1
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return 1

if __name__ == '__main__':
    sys.exit(main()) 