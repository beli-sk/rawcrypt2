#!/usr/bin/env python3
#
#  Copyright 2017 Michal Belica <https://beli.sk>
# 
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
# 
#      http://www.apache.org/licenses/LICENSE-2.0
# 
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
import os
import sys
import argparse
from getpass import getpass
from binascii import hexlify, unhexlify

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
backend = default_backend()


VERSION = '2.0.0'
PROG_NAME = "Rawcrypt"
DESCRIPTION = 'Rawcrypt 2 - simple data encryption tool'


def read_blocks(f, size=1024):
    while True:
        data = f.read(size)
        if not data:
            break
        yield data

def encrypt(infile, outfile, key):
    iv = os.urandom(12)
    encryptor = Cipher(
            algorithms.AES(key),
            modes.GCM(iv),
            backend=backend,
            ).encryptor()
    outfile.write(iv)
    for block in read_blocks(infile):
        outfile.write(encryptor.update(block))
    outfile.write(encryptor.finalize())
    outfile.write(encryptor.tag)

def decrypt(infile, outfile, key):
    iv = infile.read(12)
    if len(iv) != 12:
        raise Exception('IV of incorrect length was read from input.')
    decryptor = Cipher(
            algorithms.AES(key),
            modes.GCM(iv),
            backend=backend,
            ).decryptor()
    buff = b''
    for block in read_blocks(infile):
        block = buff + block
        buff = block[-16:]
        block = block[:-16]
        outfile.write(decryptor.update(block))
    decryptor.finalize_with_tag(buff)

def derive_key(password, salt=None):
    if salt is None:
        salt = os.urandom(16)
    kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=2**20,
            backend=backend,
            )
    return salt, kdf.derive(password.encode())

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
            description=DESCRIPTION + '\n\nData is read from stdin and written to stdout.',
            formatter_class=argparse.RawTextHelpFormatter,
            )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-e', '--encrypt', action='store_true', help='encrypt')
    group.add_argument('-d', '--decrypt', action='store_true', help='decrypt')
    parser.add_argument('-p', '--password', help='en/de-cryption password\n'
            '(will be asked for if not given)')
    parser.add_argument('-v', '--version', action='version',
            version='{} {}'.format(PROG_NAME, VERSION))
    args = parser.parse_args()
    if args.password:
        password = args.password
    else:
        password = getpass('Password: ')
    if args.encrypt:
        salt, key = derive_key(password)
        sys.stdout.buffer.write(salt)
        encrypt(sys.stdin.buffer, sys.stdout.buffer, key)
    elif args.decrypt:
        salt = sys.stdin.buffer.read(16)
        if len(salt) != 16:
            raise Exception('Salt of incorrect length read from input.')
        salt, key = derive_key(password, salt)
        decrypt(sys.stdin.buffer, sys.stdout.buffer, key)

