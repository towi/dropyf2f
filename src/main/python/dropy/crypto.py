#!/usr/bin/env python
#
# Code adapted from: http://eli.thegreenplace.net/2010/06/25/aes-encryption-of-files-in-python-with-pycrypto/
#

# std python
import os, random, struct
from cStringIO import StringIO
import hashlib
import base64

# 3d party
from Crypto.Cipher import AES


## def encrypt_file(key, in_filename, out_filename=None, chunksize=64*1024):
## ( This is an adaptation from using filenames in order that StringIO can be used to encrypt a string. )
## Note: If in_file / out_file is provided, open with +b!

def encrypt_file(key, in_file, out_file=None, chunksize=64*1024):
    """ Encrypts a file using AES (CBC mode) with the
        given key.

        key:
            The encryption key - a string that must be
            either 16, 24 or 32 bytes long. Longer keys
            are more secure.

        in_file:
            Input file

        out_file:
            If None, a StringIO will be returned.

        chunksize:
            Sets the size of the chunk which the function
            uses to read and encrypt the file. Larger chunk
            sizes can be faster for some files and machines.
            chunksize must be divisible by 16.
    """
    if not out_file:
        out_file = StringIO()

    iv = ''.join(chr(random.randint(0, 0xFF)) for i in range(16))
    encryptor = AES.new(key, AES.MODE_CBC, iv)

    in_file.seek(0,2)
    filesize=in_file.tell()
    in_file.seek(0)

    # filesize = os.path.getsize(in_file)

    infile=in_file

    outfile=out_file
    outfile.seek(0)

    outfile.write(struct.pack('<Q', filesize))
    outfile.write(iv)

    while True:

        chunk = infile.read(chunksize)
        if len(chunk) == 0:
            break
        elif len(chunk) % 16 != 0:
            chunk += ' ' * (16 - len(chunk) % 16)

        outfile.write(encryptor.encrypt(chunk))

    outfile.seek(0)
    return outfile

## def decrypt_file(key, in_filename, out_filename=None, chunksize=24*1024):
## ( This is an adaptation from using filenames in order that StringIO can be used to encrypt a string. )
## Note: If in_file / out_file is provided, open with +b!

def decrypt_file(key, in_file, out_file=None, chunksize=24*1024):
    """ Decrypts a file using AES (CBC mode) with the
        given key. Parameters are similar to encrypt_file.
    """
    if not out_file:
        out_file = StringIO()

    infile=in_file
    infile.seek(0)

    outfile=out_file
    outfile.seek(0)

    origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
    iv = infile.read(16)
    decryptor = AES.new(key, AES.MODE_CBC, iv)

    while True:
        chunk = infile.read(chunksize)
        if len(chunk) == 0:
            break
        outfile.write(decryptor.decrypt(chunk))

    outfile.truncate(origsize)

    outfile.seek(0)
    return outfile

# Method suggested by Eli by turn mnemonic password into 32 byte key.
def getHashKey(aKey):
    return hashlib.sha256(aKey).digest()

# My ( J. Norment's ) Additions

def getInFile(aFileName=None):

    if not aFileName:
        return StringIO()
    else:
        return open(aFileName,'rb')

def getOutFile(aFileName=None):

    if not aFileName:
        return StringIO()
    else:
        return open(aFileName,'wb')

def getB64encoded(aString):
    return base64.b64encode(aString)

def getB64decoded(aString):
    return base64.b64decode(aString)

