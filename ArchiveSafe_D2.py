#!/usr/bin/env python

from __future__ import with_statement

import os
import sys
import errno
import random
import secrets
import subprocess
import datetime
import time
import string
from random import *

from fuse import FUSE, FuseOSError, Operations
from passlib.hash import argon2

files_dict = {}
files_change = {}


class Passthrough(Operations):
    
    
    def __init__(self, root):
        self.root = root

    # Helpers
    # =======

    def _full_path(self, partial):
        if partial.startswith("/"):
            partial = partial[1:]
        path = os.path.join(self.root, partial)
        return path

    # Filesystem methods
    # ==================

    def access(self, path, mode):
        full_path = self._full_path(path)
        if not os.access(full_path, mode):
            raise FuseOSError(errno.EACCES)

    def chmod(self, path, mode):
        full_path = self._full_path(path)
        return os.chmod(full_path, mode)

    def chown(self, path, uid, gid):
        full_path = self._full_path(path)
        return os.chown(full_path, uid, gid)

    def getattr(self, path, fh=None):
        full_path = self._full_path(path)
        st = os.lstat(full_path)
        return dict((key, getattr(st, key)) for key in ('st_atime', 'st_ctime',
                     'st_gid', 'st_mode', 'st_mtime', 'st_nlink', 'st_size', 'st_uid'))

    def readdir(self, path, fh): #return all files except the key and tmp files
        full_path = self._full_path(path)
        dirents = ['.', '..']
        if os.path.isdir(full_path):
            dirents.extend(os.listdir(full_path))
        for r in dirents:
            if r[-5:] !='.puzz':
                yield r

    def readlink(self, path):
        pathname = os.readlink(self._full_path(path))
        if pathname.startswith("/"):
            # Path name is absolute, sanitize it.
            return os.path.relpath(pathname, self.root)
        else:
            return pathname

    def mknod(self, path, mode, dev):
        return os.mknod(self._full_path(path), mode, dev)

    def rmdir(self, path):
        full_path = self._full_path(path)
        return os.rmdir(full_path)

    def mkdir(self, path, mode):
        return os.mkdir(self._full_path(path), mode)

    def statfs(self, path):
        full_path = self._full_path(path)
        stv = os.statvfs(full_path)
        return dict((key, getattr(stv, key)) for key in ('f_bavail', 'f_bfree',
            'f_blocks', 'f_bsize', 'f_favail', 'f_ffree', 'f_files', 'f_flag',
            'f_frsize', 'f_namemax'))

    def unlink(self, path):
        return os.unlink(self._full_path(path))

    def symlink(self, name, target):
        return os.symlink(target, self._full_path(name))

    def rename(self, old, new):
        return os.rename(self._full_path(old), self._full_path(new))

    def link(self, target, name):
        return os.link(self._full_path(name), self._full_path(target))

    def utimens(self, path, times=None):
        return os.utime(self._full_path(path), times)

    # File methods
    # ============

    def open(self, path, flags):
        repf = open("/home/moes/Documents/Reports/D2_MainRep.txt","a") #Data collection report
        full_path = self._full_path(path)
        repstr = 'Open,' + full_path + ','
        startopentime = time.time()
        myext = full_path[-5:]
        if myext != '.puzz': #Skip already decrypted copies
            startkeyreadtime = time.time()
            key_file = open(full_path + '.key.puzz','r') #Opening puzzle file (Puzzle, hash parameters, encryption vector)
            keyread = key_file.readline()
            key_file.close()
            MyKeyPuzz = keyread[:30]
            MyHashParms = keyread[-77:]
            myvic = keyread[31:63]
            endkeyreadtime = time.time()
            startkeyguesstime = time.time()
            for i in range(256): #Puzzle Solve
                MyGuess = format(i,'x')
                MyGuess = MyGuess.zfill(2)
                MyGuess = MyGuess + MyKeyPuzz
                if argon2.verify(MyGuess, MyHashParms):
                    break
            endkeyguesstime = time.time()
            startdecrypttime = time.time()
            mytmpext = secrets.token_hex(4) #Random suffix to allow handling multiple copies of the same file simultaneously
            mycmd = 'openssl enc -aes-128-cbc -d -K ' + MyGuess + ' -in ' + full_path + ' -out ' + full_path + mytmpext + '.tmp.puzz' + ' -iv ' + myvic
            os.system(mycmd)
            enddecrypttime = time.time()
            startsysopentime = time.time()
            full_path = full_path + mytmpext + '.tmp.puzz'
            fh = os.open(full_path, flags) #Setting the file handler fh to point to the decrypted file to allow reading
            endsysopentime = time.time()
            files_dict[fh] = mytmpext
            endopentime = time.time()
            repstr = repstr + str(endkeyreadtime - startkeyreadtime) + ',' + str(endkeyguesstime - startkeyguesstime) + ',' + str(enddecrypttime - startdecrypttime) + ',' + str(endsysopentime - startsysopentime) + ',' + str(endopentime - startopentime) + '\n'
            repf.write(repstr)
            return fh

    def create(self, path, mode, fi=None):
        repf = open("/home/moes/Documents/Reports/D2_MainRep.txt","a") #Data collection report
        full_path = self._full_path(path)
        repstr = 'Create,' + full_path + ','
        startcreatetime = time.time()
        myext = full_path[-5:]
        if myext != '.puzz':
            full_path = self._full_path(path)
            org_full_path = full_path
            startkeygentime = time.time()
            MyKey = secrets.token_hex(16)
            MyKeyPuzz = MyKey[2:]
            myhash = argon2.hash(MyKey)
            myhex = 'a' + 'b' + 'c' + 'd' + 'e' + 'f' + string.digits
            myvic = "".join(choice(myhex) for x in range(32))
            key_file = open(full_path + '.key.puzz','w') #Creating puzzle file (Puzzle, hash parameters, encryption vector)
            key_file.write(MyKeyPuzz + ',' + myvic + ',' + myhash)
            key_file.close()
            endkeygentime = time.time()
            mytmpext = secrets.token_hex(4)
            full_path = full_path + mytmpext + '.tmp.puzz'
            startsysopentime = time.time()
            fh = os.open(full_path, os.O_WRONLY | os.O_CREAT, mode) #Setting the file handler fh to point to the decrypted file to allow writing
            endsysopentime = time.time()
            startencrypttime = time.time()
            mycmd = 'openssl enc -aes-128-cbc -K ' + MyKey + ' -in ' + full_path + ' -out ' + org_full_path + ' -iv ' + myvic
            os.system(mycmd)
            endencrypttime = time.time()
            files_dict[fh] = mytmpext
            endcreatetime = time.time()
            repstr = repstr + str(endkeygentime - startkeygentime) + ',,' + str(endencrypttime - startencrypttime) + ',' + str(endsysopentime - startsysopentime) + ',' + str(endcreatetime - startcreatetime) + '\n'
            repf.write(repstr)
            return fh

    def release(self, path, fh):
        repf = open("/home/moes/Documents/Reports/D2_MainRep.txt","a") #Data collection report
        full_path = self._full_path(path)
        repstr = 'Release,' + full_path + ','
        startreleasetime = time.time()
        myext = full_path[-5:]
        if myext != '.puzz':
            startkeygentime = time.time()
            MyKey = secrets.token_hex(16)
            MyKeyPuzz = MyKey[2:]
            myhash = argon2.hash(MyKey)
            myhex = 'a' + 'b' + 'c' + 'd' + 'e' + 'f' + string.digits
            myvic = "".join(choice(myhex) for x in range(32))
            key_file = open(full_path + '.key.puzz','w') #Creating puzzle file (Puzzle, hash parameters, encryption vector)
            key_file.write(MyKeyPuzz + ',' + myvic + ',' + myhash)
            key_file.close()
            endkeygentime = time.time()
            startencrypttime = time.time()
            mytmpext = files_dict[fh] #Random suffix to allow handling multiple copies of the same file simultaneously
            mycmd = 'openssl enc -aes-128-cbc -K ' + MyKey + ' -in ' + full_path + mytmpext + '.tmp.puzz -out ' + full_path + ' -iv ' + myvic
            os.system(mycmd)
            endencrypttime = time.time()
            endreleasetime = time.time()
            repstr = repstr + str(endkeygentime - startkeygentime) + ',,' + str(endencrypttime - startencrypttime) + ',,' + str(endreleasetime - startreleasetime) + '\n'
            repf.write(repstr)
            return os.close(fh)	

    def read(self, path, length, offset, fh):
        os.lseek(fh, offset, os.SEEK_SET)
        return os.read(fh, length)

    def write(self, path, buf, offset, fh):
        os.lseek(fh, offset, os.SEEK_SET)
        return os.write(fh, buf)

    def truncate(self, path, length, fh=None): #write the encrypted data but do not delete .tmp
        full_path = self._full_path(path)
        myext = full_path[-5:]
        if myext != '.puzz':
            full_path = self._full_path(path)
            full_path = full_path + '.tmp.puzz' #Writing to the decrypted copy of the file
            with open(full_path, 'r+') as f:
                f.truncate(length)

    def flush(self, path, fh): 
        return os.fsync(fh)


    def fsync(self, path, fdatasync, fh): #Write the encrypted data but do not delete .tmp
        full_path = self._full_path(path)
        full_path = full_path + '.tmp.puzz' #Writing to the decrypted copy of the file
        return self.flush(full_path, fh)


def main(mountpoint, root):
    
    FUSE(Passthrough(root), mountpoint, nothreads=True, foreground=True)


if __name__ == '__main__':
    main(sys.argv[2], sys.argv[1])  
