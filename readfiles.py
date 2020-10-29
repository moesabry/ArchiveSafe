#!/usr/bin/env python

from __future__ import with_statement

import os
import sys
import errno
import random
import secrets
import subprocess
import string
from random import *
from OpenSSL import crypto
#from OpenSSL.crypto import
from passlib.hash import argon2



from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import (
    Cipher,
    algorithms,
    modes)

import datetime
import time



def main():
    RunExp()

    

def RunExp():
    
    MyDir = '/home/moes/Documents/Test/2/'
    repfilename = 'D2_ReadRunReport_' + str(datetime.datetime.now()) + '.txt'
    repfile = open(repfilename,"w+")
    for filename in os.listdir(MyDir):
        repstr = filename + ","
        starttime = time.time()
        f = open(MyDir + filename,"r")
        opentime = time.time()
        txt = f.read()
        f.close
        endtime = time.time()
        repstr = repstr + str(len(txt)) + ',' + str(opentime - starttime) + ',' + str(endtime - opentime) + ',' + str(endtime - starttime) + '\n'
        repfile.write(repstr)

    repfile.close





if __name__ == '__main__':
    main()  
