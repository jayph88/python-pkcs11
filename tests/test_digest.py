"""
PKCS#11 Digests
"""

import hashlib

from pkcs11 import Mechanism, KeyType, Attribute

from . import TestCase, Not


class DigestTests(TestCase):

    def test_digest(self):
        data = 'THIS IS SOME DATA TO DIGEST'
        digest = self.session.digest(data, mechanism=Mechanism.SHA256)

        self.assertEqual(digest,
                         hashlib.sha256(data.encode('utf-8')).digest())

    def test_digest_generator(self):
        data = (
            b'This is ',
            b'some data ',
            b'to digest.',
        )

        digest = self.session.digest(data, mechanism=Mechanism.SHA256)

        m = hashlib.sha256()
        for d in data:
            m.update(d)

        self.assertEqual(digest, m.digest())

    @Not.nfast
    def test_digest_key(self):
        key = self.session.generate_key(KeyType.AES, 128,
                                        store=False, template={
                                            Attribute.SENSITIVE: False,
                                            Attribute.EXTRACTABLE: True,
                                        })

        digest = self.session.digest(key, mechanism=Mechanism.SHA256)

        self.assertEqual(digest,
                         hashlib.sha256(key[Attribute.VALUE]).digest())

    @Not.nfast
    def test_digest_key_data(self):
        key = self.session.generate_key(KeyType.AES, 128,
                                        store=False, template={
                                            Attribute.SENSITIVE: False,
                                            Attribute.EXTRACTABLE: True,
                                        })

        data = (
            b'Some data',
            key,
        )

        digest = self.session.digest(data, mechanism=Mechanism.SHA256)

        m = hashlib.sha256()
        m.update(data[0])
        m.update(data[1][Attribute.VALUE])

        self.assertEqual(digest, m.digest())
