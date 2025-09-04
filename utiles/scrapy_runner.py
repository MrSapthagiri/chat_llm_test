import os
import sys
import logging
from pathlib import Path
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.spiderloader import SpiderLoader

# Use absolute import instead of relative import
from pipelines.scrapy_pipeline import ScrapyPipeline

class ScrapyRunner:
    """
    Runner class for executing Scrapy spiders and storing the scraped data.
    """
    
    def __init__(self, output_dir="data/scrapy_output", file_format="json"):
        """
        Initialize the Scrapy runner.
        
        Args:
            output_dir (str): Directory to store output files
            file_format (str): Format to store data (json, csv)
        """
        self.output_dir = output_dir
        self.file_format = file_format
        self.logger = logging.getLogger(__name__)
        
    def setup_crawler_process(self):
        """
        Set up the Scrapy crawler process with custom settings.
        
        Returns:
            CrawlerProcess: Configured crawler process
        """
        # Add the project root to sys.path to help with imports
        project_root = str(Path(__file__).parent.parent)
        if project_root not in sys.path:
            sys.path.insert(0, project_root)
            
        settings = get_project_settings()
        
        # Configure settings for the crawler
        settings.update({
            'ITEM_PIPELINES': {
                'pipelines.scrapy_pipeline.ScrapyPipeline': 300,
            },
            'LOG_LEVEL': 'INFO',
            'COOKIES_ENABLED': False,
            'DOWNLOAD_DELAY': 1,  # 1 second delay between requests
            'CONCURRENT_REQUESTS': 8,
            'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'SPIDER_MODULES': ['spiders'],
            'NEWSPIDER_MODULE': 'spiders',
        })
        
        return CrawlerProcess(settings)
    
    def run_spider(self, spider_name, spider_args=None):
        """
        Run a specific spider by name with optional arguments.
        
        Args:
            spider_name (str): Name of the spider to run
            spider_args (dict): Arguments to pass to the spider
            
        Returns:
            bool: True if spider ran successfully, False otherwise
        """
        if spider_args is None:
            spider_args = {}
            
        try:
            # Set up the crawler process
            process = self.setup_crawler_process()
            
            # Add pipeline settings
            pipeline = ScrapyPipeline(output_dir=self.output_dir, file_format=self.file_format)
            print(f"Created pipeline with output_dir={self.output_dir}, file_format={self.file_format}")
            process.settings.update({
                'PIPELINE_INSTANCE': pipeline
            })
            
            # Run the spider
            self.logger.info(f"Starting spider: {spider_name}")
            process.crawl(spider_name, **spider_args)
            process.start()  # This blocks until the crawl is finished
            
            self.logger.info(f"Spider {spider_name} completed successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Error running spider {spider_name}: {str(e)}")
            return False
    
    def list_available_spiders(self):
        """
        List all available spiders in the project.
        
        Returns:
            list: List of available spider names
        """
        try:
            settings = get_project_settings()
            spider_loader = SpiderLoader.from_settings(settings)
            return spider_loader.list()
        except Exception as e:
            self.logger.error(f"Error listing spiders: {str(e)}")
            return []
    
    def run_all_spiders(self, spider_args=None):
        """
        Run all available spiders.
        
        Args:
            spider_args (dict): Arguments to pass to all spiders
            
        Returns:
            dict: Dictionary with spider names as keys and success status as values
        """
        if spider_args is None:
            spider_args = {}
            
        results = {}
        spiders = self.list_available_spiders()
        
        for spider_name in spiders:
            results[spider_name] = self.run_spider(spider_name, spider_args)
            
        return results