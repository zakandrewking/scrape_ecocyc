#!/bin/bash
if [[ $# -ne 1 ]]; then
    echo "Usage: ./run output_directory"
else
    scrapy crawl gene_list -o $1/results.json
fi
