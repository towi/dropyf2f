=====================================
 Other Software used in this Project
=====================================

Required to be installed
========================

PyCypto
--------
 * a quite standard C implementation for python of several cryptographic stuff
 * http://www.amk.ca/python/code/crypto
 * Ubuntu: sudo apt-get install python-crypto
 * more links:
   * http://www.codekoala.com/blog/2009/aes-encryption-python-using-pycrypto/

Example::

  >>> from Crypto.Cipher import DES
  >>> obj=DES.new('abcdefgh', DES.MODE_ECB)
  >>> plain="Guido van Rossum is a space alien."
  >>> len(plain)
  34
  >>> obj.encrypt(plain)
  Traceback (innermost last):
    File "<stdin>", line 1, in ?
  ValueError: Strings for DES must be a multiple of 8 in length
  >>> ciph=obj.encrypt(plain+'XXXXXX')
  >>> ciph
  '\021,\343Nq\214DY\337T\342pA\372\255\311s\210\363,\300j\330\250\312\347\342I\3215w\03561\303dgb/\006'
  >>> obj.decrypt(ciph)
  'Guido van Rossum is a space alien.XXXXXX'


redis
-----
 * an advanced key-value store; mainly for Unix/Posix but available for Windows as well
 * http://redis.io
 * Ubuntu: sudo apt-get install redis-server
 * more links:
   -  http://try.redis-db.com/

Example::

  $ redis-cli SET server:name fido
  $ redis-cli GET server:name
  fido


redis-py
--------
 * the simple python interface to redis
 * https://github.com/andymccurdy/redis-py
 * Ubuntu: sudo apt-get install python-redis


Included foreign packages
=========================


pyDes
-----
 * python only DES encryption
 * http://twhiteman.netfirms.com/des.html


pyAES
-----

 * python only AES encryption
 * http://brandon.sternefamily.net/files/pyAES.txt
 * http://brandon.sternefamily.net/posts/2007/06/aes-tutorial-python-implementation/

