# LLM Test Project with Scrapy Data Storage

This project provides functionality for running Scrapy spiders and storing the scraped data in various formats (JSON, CSV).

## Installation

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Scrapy Data Storage

The project includes a pipeline for storing data scraped by Scrapy spiders. The data can be stored in JSON or CSV format.

### Running Scrapy Spiders

Use the `run_scrapy.py` script to run Scrapy spiders and store the scraped data:

```bash
python scripts/run_scrapy.py --spider=example_quotes --output=data/scrapy_output --format=json
```

Options:
- `--spider`: Name of the spider to run (default: all available spiders)
- `--output`: Directory to store output files (default: data/scrapy_output)
- `--format`: Format to store data (json, csv) (default: json)

### Creating Custom Spiders

Create custom spiders in the `spiders` directory. Here's an example spider that scrapes quotes from quotes.toscrape.com:

```python
import scrapy

class ExampleSpider(scrapy.Spider):
    name = 'example_quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']
    
    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('small.author::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall(),
                'url': response.url
            }
        
        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
```

### Using the ScrapyPipeline

The `ScrapyPipeline` class in `pipelines/scrapy_pipeline.py` handles storing the scraped data. It supports JSON and CSV formats.

```python
from pipelines.scrapy_pipeline import ScrapyPipeline

# Initialize the pipeline
pipeline = ScrapyPipeline(output_dir="data/scrapy_output", file_format="json")

# Process an item
item = {"title": "Example", "content": "This is an example item"}
pipeline.process_item(item, spider)

# Save all items when the spider finishes
pipeline.close_spider(spider)
```

### Using the ScrapyRunner

The `ScrapyRunner` class in `utiles/scrapy_runner.py` provides a convenient way to run Scrapy spiders:

```python
from utiles.scrapy_runner import ScrapyRunner

# Initialize the runner
runner = ScrapyRunner(output_dir="data/scrapy_output", file_format="json")

# Run a specific spider
runner.run_spider("example_quotes")

# Run all available spiders
runner.run_all_spiders()
```