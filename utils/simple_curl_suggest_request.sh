curl -X POST 'localhost:9200/stackoverflowtags/_suggest?pretty' -d '{
    "tag-suggest" : {
        "text" : "n",
            "completion" : {
                    "field" : "suggest"
                        }
                        }
}'''
