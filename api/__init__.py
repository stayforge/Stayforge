class MongoRepository:
    def __init__(self, database, collection, client, model_class=None):
        self.database = database
        self.collection = collection
        self.client = client
        self.model_class = model_class