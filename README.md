# gutenberg-authors
A Linked Data mashup of Project Gutenberg and DBpedia

#### Demo at: http://tools.nypl-labs.biz/gutenberg


```
47000_metadata.json - Source of the gutenberg data w/ eng. wikipedia ids
---
download_data   - Stores the RDF from dbpedia endpoint
analyze_data.py - Analyzes and enriches data creates allData(_example).json
es_index.py     - Dumps the data into elastic search
---
JSON Elastic Search Settings
es_authors_mapping.json
es_authors_setting.json
es_query_multi.json


ES command chain:
curl -XDELETE localhost:9200/gutenberg/ | python -m json.tool
curl -XPUT localhost:9200/gutenberg/ | python -m json.tool
curl -XPOST localhost:9200/gutenberg/_close | python -m json.tool
curl -XPUT localhost:9200/gutenberg/_settings -d @es_authors_setting.json | python -m json.tool
curl -XPOST localhost:9200/gutenberg/_open | python -m json.tool
curl -XPUT localhost:9200/gutenberg/_mapping/author -d @es_authors_mapping.json | python -m json.tool
python3.4 es_index.py
curl -XGET localhost:9200/gutenberg/author/_search/ -d @es_query_multi.json | python -m json.tool


```
