import os
import json
import csv
from datetime import datetime
from pathlib import Path

class ScrapyPipeline:
    """
    Pipeline for processing and storing data from Scrapy spiders.
    Supports storing data in JSON, CSV, and other formats.
    """
    
    def __init__(self, output_dir="data/scrapy_output", file_format="json"):
        """
        Initialize the Scrapy pipeline with output directory and file format.
        
        Args:
            output_dir (str): Directory to store output files
            file_format (str): Format to store data (json, csv)
        """
        self.output_dir = output_dir
        self.file_format = file_format.lower()
        self.ensure_output_dir()
        self.items = []
        
    def ensure_output_dir(self):
        """
        Create output directory if it doesn't exist
        """
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)
        
    def process_item(self, item, spider):
        """
        Process a scraped item and add it to the collection.
        
        Args:
            item (dict): Scraped item data
            spider: The spider that scraped the item
            
        Returns:
            dict: The processed item
        """
        # Add timestamp to item
        item['timestamp'] = datetime.now().isoformat()
        
        # Add to collection
        self.items.append(item)
        
        return item
    
    def close_spider(self, spider):
        """
        Called when spider finishes, saves all collected items.
        
        Args:
            spider: The spider that just finished
        """
        if not self.items:
            return
            
        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{spider.name}_{timestamp}"
        
        # Print debug info
        print(f"Saving {len(self.items)} items in {self.file_format} format to {filename}")
        
        if self.file_format == "json":
            self._save_as_json(filename)
        elif self.file_format == "csv":
            self._save_as_csv(filename)
        else:
            raise ValueError(f"Unsupported file format: {self.file_format}")
            
        # Clear items after saving
        self.items = []
    
    def _save_as_json(self, filename):
        """
        Save items as JSON file
        
        Args:
            filename (str): Base filename without extension
        """
        filepath = os.path.join(self.output_dir, f"{filename}.json")
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.items, f, ensure_ascii=False, indent=2)
            
    def _save_as_csv(self, filename):
        """
        Save items as CSV file
        
        Args:
            filename (str): Base filename without extension
        """
        if not self.items:
            return
            
        filepath = os.path.join(self.output_dir, f"{filename}.csv")
        
        # Get all possible field names from all items
        fieldnames = set()
        for item in self.items:
            fieldnames.update(item.keys())
        
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=sorted(fieldnames))
            writer.writeheader()
            writer.writerows(self.items)