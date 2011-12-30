#!/usr/bin/env python
"""test crypto algos"""

# std python
from sys import *
import unittest

# 3rd party
from Crypto.Cipher import DES
from Crypto.Cipher import AES

# make local python available
#import sys
#sys.path = [ "../../main/python"] + sys.path

# dropy local
#from dropy.sredis import SRedis



import os, random, struct
from Crypto.Cipher import AES

from cStringIO import StringIO

def encrypt_block(key, data, padchar=' '):
    """ Encrypts data using AES (CBC mode) with the given key.
        key:
            The encryption key - a string that must be
            either 16, 24 or 32 bytes long. Longer keys
            are more secure.
    """
    # http://eli.thegreenplace.net/2010/06/25/aes-encryption-of-files-in-python-with-pycrypto/
    import random
    #
    assert len(key) in [16, 24, 32]
    assert len(data) > 0
    iv = ''.join(chr(random.randint(0, 0xFF)) for i in range(16))
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    output = StringIO()
    output.write(struct.pack('<Q', len(data)))
    output.write(iv)
    if len(data) % 16 != 0:
        data += padchar * (16 - len(data) % 16)
    output.write(encryptor.encrypt(data))
    return output.getvalue()


def decrypt_block(key, crypted_data):
    """ Decrypts a file using AES (CBC mode) with the given key.
    """
    assert len(key) in [16, 24, 32]
    assert len(crypted_data) > 0
    infile = StringIO(crypted_data)
    origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
    iv = infile.read(16)
    decryptor = AES.new(key, AES.MODE_CBC, iv)
    data = decryptor.decrypt(infile.read())
    return data[:origsize]


class CryptoTestCase(unittest.TestCase):

    def setUp(self):
        pass
    def tearDown(self):
        pass

    # 32:__________12345678_1_2345678_2_2345678_3_2
    AES_SECRET = r"This is a keY! th/\t-noone will "

    def testAesData(self):
        """check AES en- and decryption of a data block"""
        data = r"klsjdfhalksjdfhalksj lksajdfhlkasjdf hlaksjdfhaksjdfjhlaksd flaskdjf halskdjfh alksdjfh jjdflaksjhdfiuui"
        r1 = encrypt_block(self.AES_SECRET, data)
        r2 = decrypt_block(self.AES_SECRET, r1)
        self.assertEquals(r2, data)


if __name__ == "__main__":
    unittest.main()
