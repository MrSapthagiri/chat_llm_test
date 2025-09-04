import os
import logging
import logging.config
import yaml
from pathlib import Path

def setup_logger(config_path=None):
    """
    Set up logging configuration from a YAML file.
    If config_path is not provided, use default configuration.
    
    Args:
        config_path (str, optional): Path to logging configuration file
        
    Returns:
        logging.Logger: Configured logger
    """
    if config_path and os.path.exists(config_path):
        # Load configuration from file
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    else:
        # Create logs directory if it doesn't exist
        Path('logs').mkdir(exist_ok=True)
        
        # Use default configuration
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler('logs/app.log', mode='a')
            ]
        )
    
    return logging.getLogger(__name__)


def get_logger(name):
    """
    Get a logger with the specified name.
    
    Args:
        name (str): Logger name
        
    Returns:
        logging.Logger: Logger instance
    """
    return logging.getLogger(name)