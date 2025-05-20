import os
from datetime import datetime

class ReportsHelper:
    """Helper class for managing test reports directory structure"""
    
    def __init__(self):
        """Initialize the ReportsHelper"""
        self.reports_dir = "reports"
        self.logs_dir = os.path.join(self.reports_dir, "logs")
        self.screenshots_dir = os.path.join(self.reports_dir, "screenshots")
        self._setup_directories()

    def _setup_directories(self):
        """Set up the reports directory structure"""
        # Create main reports directory
        if not os.path.exists(self.reports_dir):
            os.makedirs(self.reports_dir)

        # Create subdirectories
        for directory in [self.logs_dir, self.screenshots_dir]:
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