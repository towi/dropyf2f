#!/usr/bin/env python
"""test crypto algos"""

# std python
import sys
import unittest

# make local python available
#import sys
sys.path = [ "../../main/python"] + sys.path

# dropy local
from dropy.crypto import encrypt_block_pw, decrypt_block_pw

VERBOSE = True

class CryptoTestCase(unittest.TestCase):

    def setUp(self):
        pass
    def tearDown(self):
        pass

    PASSWORD = r"This is 1 Key!"

    def test10AesData(self):
        """check AES en- and decryption of a data block"""
        data = r"klsjdfhalksjdfhalksj lksajdfhlkasjdf hlaksjdfhaksjdfjhlaksd flaskdjf halskdjfh alksdjfh jjdflaksjhdfiuui"
        r1 = encrypt_block_pw(self.PASSWORD, data)
        r2 = decrypt_block_pw(self.PASSWORD, r1)
        self.assertEquals(r2, data)

    def test11AesNocompress(self):
        """check AES without compression"""
        data = r"klsjdfhalksjdfhalksj lksajdfhlkasjdf hlaksjdfhaksjdfjhlaksd flaskdjf halskdjfh alksdjfh jjdflaksjhdfiuui"
        r1 = encrypt_block_pw(self.PASSWORD, data, compress=None)
        r2 = decrypt_block_pw(self.PASSWORD, r1, compress=None)
        self.assertEquals(r2, data)

    def test20AesLongRepeatedData(self):
        """check AES encryption of long repeats"""
        def atest(data):
            r1 = encrypt_block_pw(self.PASSWORD, data, compress_options=[9])
            r2 = decrypt_block_pw(self.PASSWORD, r1)
            n1 = encrypt_block_pw(self.PASSWORD, data, compress=None)
            n2 = decrypt_block_pw(self.PASSWORD, n1, compress=None)
            if VERBOSE: print >>sys.stderr, "  len(in):", len(data), " len(crypt):", len(r1), " len(crypt-nocompress):", len(n1)
            self.assertEquals(r2, data)
            self.assertEquals(n2, data)
        if VERBOSE: print >>sys.stderr
        atest("a")
        atest("a"*10)
        atest("a"*100)
        atest("a"*1000)
        atest("a"*10000)
        atest("a"*100000)
        atest("ab"*1000)
        atest("abc"*1000)
        atest("lkfajshdklj"*1000)
        atest("abcdeabc"*1000)
        atest("jdfalksjdfhlaksjd fhlkasjdhflkasjdfhlaksdjfhalskd jhfalskdjfhlkasjdhflkasjhdflk jashldk"*100)
        atest("dfalksjdfhlaksjd fhlkasjdhflkasjdfhlaksdjfhalskd jhfalskdjfhlkasjdhflkasjhdflk jashldk"*100000)

    def test21AesCompressionLevel(self):
        """check AES encryption compression efficiency"""
        def atest(data, opts):
            if opts==None:
                r1 = encrypt_block_pw(self.PASSWORD, data)
            else:
                r1 = encrypt_block_pw(self.PASSWORD, data, compress_options=opts)
            r2 = decrypt_block_pw(self.PASSWORD, r1)
            if VERBOSE: print >>sys.stderr, "  len(in):", len(data), " len(crypt):", len(r1), " opts:", opts
            self.assertEquals(r2, data)
        if VERBOSE: print >>sys.stderr
        data = "dfalksjdfhlaksjd fhlkasjdhflkasjdfhlaksdjfhalskd jhfalskdjfhlkasjdhflkasjhdflk jashldk"*100000
        atest(data, None)
        atest(data, [])
        atest(data, [0])
        atest(data, [1])
        atest(data, [9])

if __name__ == "__main__":
    unittest.main()

