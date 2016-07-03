curl -XDELETE 'http://localhost:9200/stackoverflowtags/'

curl -X PUT localhost:9200/stackoverflowtags

curl -X PUT localhost:9200/stackoverflowtags/tag/_mapping -d '{
  "tag" : {
        "properties" : {
            "name" : { "type" : "string" },
            "suggest" : { "type" : "completion",
                          "analyzer" : "simple",
                          "search_analyzer" : "simple"
            }
        }
    }
}'

curl -X PUT 'localhost:9200/stackoverflowtags/tag/1?refresh=true' -d '{
    "name" : "java",
    "suggest" : {
        "input": "java",
        "output": "java",
        "weight" : 34
    }
}'

curl -X POST 'localhost:9200/stackoverflowtags/_suggest?pretty' -d '{
    "tag-suggest" : {
        "text" : "j",
        "completion" : {
            "field" : "suggest"
        }
    }
}'
