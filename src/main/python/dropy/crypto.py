#!/usr/bin/env python
#
# Code adapted from: http://eli.thegreenplace.net/2010/06/25/aes-encryption-of-files-in-python-with-pycrypto/
#
# towi added:
# - crypt with arbitrary 'password' instead of a specific length 'key' (eg. 32byte)
# - data is compressed before encryption, because only then it is really crypted.
"""encryption and decryption utils.

Notes:
 * 'key' is an algorithm-specific "secret" used for en- end decryption. it is sometimes
   bount to some constraints, ie. specific lengths, alphabets or formats. with AES it
   is for example that the length mus be 16, 24 or 32.
 * 'passsword' is aribitrary and use to generate the 'key' whatever the algorithm is.
 * remember that encrypting something with redunancy inside leaves a vulnarability open.
   therefore you (or we) should compress data first before encryption. the better the compression
   (stripping the "redundancy", leaving the "information") the less vulnarable.
   - currently we only use "zlib level 1" compression, which is not good at all. But it is
     quite fast and at least gets rid of simple repeats which are the most obvious door
     for vulnaribility attacks.
   - in the final version i want to use googles 'snappy' algorithm because it offers the best
     tradeoff between speed and compession efficiency. it is not available as a std
     current Ubuntu LTS package (10.04), thus we wait a bit.
     - http://pypi.python.org/pypi/python-snappy
     - when you got http://code.google.com/p/snappy installed:
     - sudo easy_install python-snappy
"""

# std python
import os, random, struct
from cStringIO import StringIO
import hashlib
import base64
import zlib

# 3d party
from Crypto.Cipher import AES


## def encrypt_file(key, in_filename, out_filename=None, chunksize=64*1024):
## ( This is an adaptation from using filenames in order that StringIO can be used to encrypt a string. )
## Note: If in_file / out_file is provided, open with +b!

def encrypt_file_pw(password, in_file, out_file=None, chunksize=64*1024):
    """ Encrypts a file using AES (CBC mode) with the
        given arbitrary password.

        password:
            will be hashed to a 32byte long crypt key.

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
    key = getHashKey(password)
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

def decrypt_file_pw(password, in_file, out_file=None, chunksize=24*1024):
    """ Decrypts a file using AES (CBC mode) with the
        given password. Parameters are similar to encrypt_file_pw.
    """
    if not out_file:
        out_file = StringIO()

    infile=in_file
    infile.seek(0)

    outfile=out_file
    outfile.seek(0)

    origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
    iv = infile.read(16)
    key = getHashKey(password)
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
def getHashKey(password):
    key = hashlib.sha256(password).digest()
    assert len(key) == 32
    return key

######################################################################
#
# My ( J. Norment's ) Additions
#

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

################
#
# towis additions
#

def encrypt_block_pw(password, rawdata, padchar=' ', compress='zlib', compress_options=[1]):
    """ Encrypts data using AES (CBC mode) with the given arbitrary password.
        key:
            The encryption key - a string that must be
            either 16, 24 or 32 bytes long. Longer keys
            are more secure.
        compress_options:
            passed as '*compress_options' to the compression algorithm you choose.
            for compression='zlib' 'compress_options[0]' will become the compression level.
    """
    # http://eli.thegreenplace.net/2010/06/25/aes-encryption-of-files-in-python-with-pycrypto/
    ##############
    # prepare
    key = getHashKey(password) # make 32byte key for AES
    assert len(rawdata) > 0       #@TODO, we have to deal with this later
    iv = ''.join(chr(random.randint(0, 0xFF)) for i in range(16))
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    output = StringIO()
    ##############
    # compress -- enrcrypting uncompressed data is not safe
    if compress == None:
        data = rawdata
    elif compress == 'zlib':
        # level=1 is very fast, and good enough to get rid of long repeats
        data = zlib.compress(rawdata, *compress_options)
    else:
        raise ValueError("unknown compression '%s'" % compression)
    ##############
    # aux stuff
    # - write original compressed length unencrypted
    #   . could be done after IV to have it encrypted, too. but this is simpler.
    output.write(struct.pack('<Q', len(data)))
    # - write iv unencrypted
    output.write(iv)
    # - pad data
    if len(data) % 16 != 0:
        data += padchar * (16 - len(data) % 16)
    ################
    # encrypt data
    output.write(encryptor.encrypt(data))
    # result
    return output.getvalue()


def decrypt_block_pw(password, crypted_data, compress='zlib', compress_options=[]):
    """ Decrypts a file using AES (CBC mode) with the given arbitrary password.
    compress_options:
        passed to the decompression ficntion you chose via '*compress_options'.
        even though it is decompression we do here we call the parameter the same
        as in encrypt_block_pw() for symmetry. sorry.
    """
    ##################
    # prepare
    key = getHashKey(password) # make 32byte key for AES
    assert len(crypted_data) > 0
    infile = StringIO(crypted_data)
    ##################
    # aux stuff
    # - get original compressed size
    origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
    iv = infile.read(16)
    ##################
    # decrypt
    decryptor = AES.new(key, AES.MODE_CBC, iv)
    data = decryptor.decrypt(infile.read())
    ##################
    # decompress
    if compress == None:
        rawdata = data[:origsize]
    elif compress == 'zlib':
        # level=1 is very fast, and good enough to get rid of long repeats
        rawdata = zlib.decompress(data[:origsize], *compress_options)
    else:
        raise ValueError("unknown decompression '%s'" % compression)
    # result
    return rawdata


######################################################################
