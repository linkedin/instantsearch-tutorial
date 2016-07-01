curl -XGET 'http://localhost:9200/stackoverflow/posts/_search' -d '{
    
    "query" : {
        "match": {
            "name": {
                "query": "d",
                "operator": "and"
            }
        }
    }
}'
