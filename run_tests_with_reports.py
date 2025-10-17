#!/usr/bin/env python3
"""
Enhanced test runner with multiple reporting options
"""

import argparse
import subprocess
import sys
from helpers.reports import ReportsHelper

def run_tests_with_reports(test_path=None, report_type="all", parallel=False):
    """
    Run tests with specified report type
    
    Args:
        test_path (str): Specific test file or directory to run
        report_type (str): Type of reports to generate (all, html, allure, json, console)
        parallel (bool): Run tests in parallel
    """
    reports_helper = ReportsHelper()
    
    # Build pytest command
    cmd = ["python", "-m", "pytest"]
    
    # Add test path if specified
    if test_path:
        cmd.append(test_path)
    
    # Add parallel execution if requested
    if parallel:
        cmd.extend(["-n", "auto"])
    
    # Configure reports based on type
    if report_type == "all":
        # Use default configuration from pytest.ini
        pass
    elif report_type == "html":
        cmd.extend(["--html=reports/report.html", "--self-contained-html"])
    elif report_type == "allure":
        cmd.extend(["--alluredir=reports/allure-results"])
    elif report_type == "json":
        cmd.extend(["--json-report", "--json-report-file=reports/report.json"])
    elif report_type == "console":
        cmd.extend(["-v", "--tb=short"])
    elif report_type == "minimal":
        cmd.extend(["-q", "--tb=no"])
    
    print(f"🚀 Running tests with {report_type} reports...")
    print(f"Command: {' '.join(cmd)}")
    
    try:
        # Run tests
        result = subprocess.run(cmd, check=False)
        
        # Generate additional reports if needed
        if report_type in ["all", "allure"] and result.returncode == 0:
            print("\n📊 Generating Allure report...")
            reports_helper.generate_allure_report()
        
        # Show report summary
        print("\n" + reports_helper.get_report_summary())
        
        return result.returncode
        
    except KeyboardInterrupt:
        print("\n⏹️  Test execution interrupted by user")
        return 1
    except Exception as e:
        print(f"\n❌ Error running tests: {e}")
        return 1

def main():
    parser = argparse.ArgumentParser(description="Run Playwright tests with enhanced reporting")
    parser.add_argument(
        "test_path", 
        nargs="?", 
        help="Specific test file or directory to run (e.g., tests/test_login.py)"
    )
    parser.add_argument(
        "--report", 
        choices=["all", "html", "allure", "json", "console", "minimal"],
        default="all",
        help="Type of reports to generate (default: all)"
    )
    parser.add_argument(
        "--parallel", 
        action="store_true",
        help="Run tests in parallel"
    )
    parser.add_argument(
        "--open-allure", 
        action="store_true",
        help="Open Allure report in browser after generation"
    )
    parser.add_argument(
        "--cleanup", 
        action="store_true",
        help="Clean up old reports before running tests"
    )
    
    args = parser.parse_args()
    
    reports_helper = ReportsHelper()
    
    # Cleanup old reports if requested
    if args.cleanup:
        print("🧹 Cleaning up old reports...")
        reports_helper.cleanup_old_reports()
    
    # Run tests
    exit_code = run_tests_with_reports(
        test_path=args.test_path,
        report_type=args.report,
        parallel=args.parallel
    )
    
    # Open Allure report if requested
    if args.open_allure and args.report in ["all", "allure"]:
        reports_helper.open_allure_report()
    
    sys.exit(exit_code)

if __name__ == "__main__":
    main() 