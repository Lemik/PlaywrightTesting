import os
import json
import subprocess
from datetime import datetime
from pathlib import Path

class ReportsHelper:
    """Enhanced helper class for managing test reports with multiple formats"""
    
    def __init__(self):
        """Initialize the ReportsHelper"""
        self.reports_dir = "reports"
        self.logs_dir = os.path.join(self.reports_dir, "logs")
        self.screenshots_dir = os.path.join(self.reports_dir, "screenshots")
        self.allure_results_dir = os.path.join(self.reports_dir, "allure-results")
        self.allure_report_dir = os.path.join(self.reports_dir, "allure-report")
        self.json_reports_dir = os.path.join(self.reports_dir, "json")
        self._setup_directories()

    def _setup_directories(self):
        """Set up the reports directory structure"""
        # Create main reports directory
        if not os.path.exists(self.reports_dir):
            os.makedirs(self.reports_dir)

        # Create subdirectories
        directories = [
            self.logs_dir, 
            self.screenshots_dir, 
            self.allure_results_dir,
            self.allure_report_dir,
            self.json_reports_dir
        ]
        
        for directory in directories:
            if not os.path.exists(directory):
                os.makedirs(directory)

    def get_test_run_dir(self, test_name: str):
        """Get a directory for the current test run.
        
        Args:
            test_name (str): Name of the test
            
        Returns:
            str: Path to the test run directory
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        test_run_dir = os.path.join(self.reports_dir, f"{test_name}_{timestamp}")
        
        if not os.path.exists(test_run_dir):
            os.makedirs(test_run_dir)
            
        return test_run_dir

    def generate_allure_report(self):
        """Generate Allure HTML report from results"""
        try:
            cmd = [
                "allure", "generate", 
                self.allure_results_dir, 
                "-o", self.allure_report_dir, 
                "--clean"
            ]
            subprocess.run(cmd, check=True, capture_output=True, text=True)
            print(f"✅ Allure report generated: {self.allure_report_dir}/index.html")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to generate Allure report: {e}")
            return False
        except FileNotFoundError:
            print("❌ Allure command not found. Install it first:")
            print("   brew install allure (macOS)")
            print("   or download from: https://github.com/allure-framework/allure2/releases")
            return False

    def open_allure_report(self):
        """Open Allure report in browser"""
        try:
            cmd = ["allure", "open", self.allure_report_dir]
            subprocess.Popen(cmd)
            print(f"🌐 Opening Allure report in browser...")
        except Exception as e:
            print(f"❌ Failed to open Allure report: {e}")

    def get_report_summary(self):
        """Get a summary of available reports"""
        reports = {
            "html": f"{self.reports_dir}/report.html",
            "allure": f"{self.allure_report_dir}/index.html",
            "json": f"{self.reports_dir}/report.json",
            "log": f"{self.reports_dir}/report.log"
        }
        
        summary = "📊 Available Reports:\n"
        for report_type, path in reports.items():
            if os.path.exists(path):
                size = os.path.getsize(path) / 1024  # KB
                summary += f"   • {report_type.upper()}: {path} ({size:.1f} KB)\n"
            else:
                summary += f"   • {report_type.upper()}: {path} (not generated)\n"
        
        return summary

    def cleanup_old_reports(self, days=7):
        """Clean up reports older than specified days"""
        import time
        current_time = time.time()
        cutoff_time = current_time - (days * 24 * 60 * 60)
        
        cleaned = 0
        for root, dirs, files in os.walk(self.reports_dir):
            for file in files:
                file_path = os.path.join(root, file)
                if os.path.getmtime(file_path) < cutoff_time:
                    try:
                        os.remove(file_path)
                        cleaned += 1
                    except Exception as e:
                        print(f"Failed to remove {file_path}: {e}")
        
        print(f"🧹 Cleaned up {cleaned} old report files")
        return cleaned 