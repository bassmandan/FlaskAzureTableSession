import json
import unittest
from uuid import uuid4

from flask_session_azure.storage_account import StorageAccount
from tests.storage_mock import StorageMock


class StorageTests(unittest.TestCase):
    connection_String = "DefaultEndpointsProtocol=https;AccountName=someAccount;AccountKey=someKey;EndpointSuffix=core.windows.net"
    encryption_key = "abcdefghijkmnopq"

    def _test_encryption_decryption(self, test_string, key):
        encrypted_data, tag, nonce = StorageAccount.encrypt(test_string, key)
        result = StorageAccount.decrypt(encrypted_data, tag, nonce, key)
        self.assertEqual(test_string, result)

    def test_encryption_cylce_string_key(self):
        key = "abcdefghijkmnopq"
        data = "Hi, I'm commander Shepard, and this is my favorite shop on the citadel"
        self._test_encryption_decryption(data, key)

    def test_encryption_cylce_byte_key(self):
        key = b"abcdefghijkmnopq"
        data = "Hi, I'm commander Shepard, and this is my favorite shop on the citadel"
        self._test_encryption_decryption(data, key)

    def test_encryption_cylce_json_paload(self):
        key = b"abcdefghijkmnopq"
        data = {"text": "Hi, I'm commander Shepard, and this is my favorite shop on the citadel", "score": 90.8}
        self._test_encryption_decryption(json.dumps(data), key)

    def test_storage_roundrip(self):
        id = str(uuid4())
        uut = StorageAccount(self.connection_String, "table_name", "partition_key", False)
        uut.table_service = StorageMock()
        self.assertIsNone(uut.read(id, self.encryption_key))
        data = {
            "id" : "id1"
        }
        uut.write(id, data, self.encryption_key)
        self.assertEqual(uut.read(id, self.encryption_key), data)
        data["id"] = "id2"
        uut.write(id, data, self.encryption_key)
        self.assertEqual(uut.read(id, self.encryption_key)["id"], "id2")

        uut.delete(id)
        self.assertIsNone(uut.read(id, self.encryption_key))
        uut.delete(id)



if __name__ == '__main__':
    unittest.main()
