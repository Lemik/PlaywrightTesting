import logging
import os
from datetime import datetime
import re

class TestLogger:
    """Helper class for test logging"""
    
    def __init__(self, test_name: str):
        """Initialize the TestLogger.
        
        Args:
            test_name (str): Name of the test for log file naming
        """
        self.test_name = self._sanitize_filename(test_name)
        self.log_dir = "reports/logs"
        self._setup_logger()

    def _sanitize_filename(self, filename: str) -> str:
        """Sanitize filename to be safe for all operating systems.
        
        Args:
            filename (str): Original filename
            
        Returns:
            str: Sanitized filename
        """
        # Remove invalid characters
        filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
        # Remove square brackets and their contents
        filename = re.sub(r'\[.*?\]', '', filename)
        # Replace multiple underscores with a single one
        filename = re.sub(r'_+', '_', filename)
        # Remove leading/trailing underscores
        filename = filename.strip('_')
        return filename

    def _setup_logger(self):
        """Set up the logger with proper formatting and file handling"""
        # Ensure log directory exists
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

        # Create logger
        self.logger = logging.getLogger(self.test_name)
        self.logger.setLevel(logging.DEBUG)

        # Create handlers
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = os.path.join(self.log_dir, f"{self.test_name}_{timestamp}.log")
        file_handler = logging.FileHandler(log_file)
        console_handler = logging.StreamHandler()

        # Create formatters and add it to handlers
        log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(log_format)
        console_handler.setFormatter(log_format)

        # Add handlers to the logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def info(self, message: str):
        """Log info message"""
        self.logger.info(message)

    def error(self, message: str):
        """Log error message"""
        self.logger.error(message)

    def debug(self, message: str):
        """Log debug message"""
        self.logger.debug(message)

    def warning(self, message: str):
        """Log warning message"""
        self.logger.warning(message) 