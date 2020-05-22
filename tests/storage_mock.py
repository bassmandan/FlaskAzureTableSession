from azure.common import AzureMissingResourceHttpError


class StorageMock(object):
    def __init__(self):
        self.data = dict()

    def get_entity(self, table_name, partition_key, key):
        full_key = f"{table_name}/{partition_key}/{key}"
        try:
            return self.data[full_key]
        except KeyError:
            raise AzureMissingResourceHttpError("Not found", 404)

    def insert_or_merge_entity(self, table_name: str, entity: dict):
        partition_key = entity["PartitionKey"]
        key = entity["RowKey"]
        full_key = f"{table_name}/{partition_key}/{key}"
        self.data[full_key] = entity

    def delete_entity(self, table_name, partition_key, key):
        full_key = f"{table_name}/{partition_key}/{key}"
        try:
            del self.data[full_key]
        except KeyError:
            raise AzureMissingResourceHttpError("Not found", 404)
