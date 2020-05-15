import json

from elasticsearch import Elasticsearch

from data_model.blogposts import PostEncoder, convert_to_dict, dict_to_obj


class ElasticWrapper:
    settings = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0
        },
        "mappings": {
            "contribution": {
                "properties": {
                    "id": {"type": "integer"},
                    "conversation": {
                        "type": "nested",
                        "properties": {
                            "genid": {"type": "integer"},
                            "ref": {"type": "integer"},
                            "time": {"type": "text"},
                            "nickname": {"type": "text"},
                            "text": {"type": "text"}
                        }
                    }
                }
            }
        }
    }

    def __init__(self):
        self.es = Elasticsearch()
        self.index = 'oanadi'

    def store_post(self, contribution, index='oanadi'):
        try:
            if self.es.ping():
                print('[Elastic]: Yay Connect')
            else:
                print('[Elastic]: It could not connect!')

            if not self.es.indices.exists(index):
                print("[Elastic]: blog-posts-please index was not created. Creating now!")
                self.es.indices.create(index=index, body=self.settings)

        except ConnectionError as error:
            print("[Elastic]: Failed to connect to the ElasticSearch storage.\nError: {}".format(error))


if __name__ == "__main__":
    print('test')
