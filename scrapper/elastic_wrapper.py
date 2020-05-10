from elasticsearch import Elasticsearch


class ElasticWrapper:
    def __init__(self):
        self.es = Elasticsearch()
        self.index = 'blog-posts'

    def store_post(self, post, index='blog-posts'):
        try:
            # self.es.ping()

            if not self.es.indices.exists(index):
                print("[Elastic]: blog-posts index was not created. Creating now!")
                # need mappings ------
                # self.es.indices.create(index=index, body=self.mapping)
        except ConnectionError as error:
            print("[Elastic]: Failed to connect to the ElasticSearch storage.\nError: {}".format(error))


