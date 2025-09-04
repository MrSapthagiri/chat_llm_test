#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script to run Scrapy spiders and store the scraped data.

Usage:
    python run_scrapy.py --spider=<spider_name> --output=<output_dir> --format=<format>

Options:
    --spider    Name of the spider to run (default: all available spiders)
    --output    Directory to store output files (default: data/scrapy_output)
    --format    Format to store data (json, csv) (default: json)
"""

import os
import sys
import argparse
import logging
from pathlib import Path

# Add the project root directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from utiles.scrapy_runner import ScrapyRunner
from utiles.logger import setup_logger


def parse_arguments():
    """
    Parse command line arguments.
    
    Returns:
        argparse.Namespace: Parsed arguments
    """
    parser = argparse.ArgumentParser(description="Run Scrapy spiders and store the scraped data.")
    
    parser.add_argument(
        "--spider",
        type=str,
        default=None,
        help="Name of the spider to run (default: all available spiders)"
    )
    
    parser.add_argument(
        "--output",
        type=str,
        default="data/scrapy_output",
        help="Directory to store output files (default: data/scrapy_output)"
    )
    
    parser.add_argument(
        "--format",
        type=str,
        choices=["json", "csv"],
        default="json",
        help="Format to store data (json, csv) (default: json)"
    )
    
    return parser.parse_args()


def main():
    """
    Main function to run Scrapy spiders.
    """
    # Parse command line arguments
    args = parse_arguments()
    
    # Setup logger
    setup_logger()
    logger = logging.getLogger(__name__)
    
    # Create output directory if it doesn't exist
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    logger.info(f"Starting Scrapy runner with output directory: {output_dir}")
    logger.info(f"Output format: {args.format}")
    
    # Initialize the Scrapy runner
    runner = ScrapyRunner(output_dir=str(output_dir), file_format=args.format)
    
    # Run the specified spider or all available spiders
    if args.spider:
        logger.info(f"Running spider: {args.spider}")
        print(f"Running spider {args.spider} with output format {args.format} to directory {output_dir}")
        success = runner.run_spider(args.spider)
        if success:
            logger.info(f"Spider {args.spider} completed successfully")
        else:
            logger.error(f"Spider {args.spider} failed")
    else:
        logger.info("Running all available spiders")
        results = runner.run_all_spiders()
        
        # Log results
        for spider_name, success in results.items():
            if success:
                logger.info(f"Spider {spider_name} completed successfully")
            else:
                logger.error(f"Spider {spider_name} failed")
    
    logger.info("Scrapy runner finished")


if __name__ == "__main__":
    main()