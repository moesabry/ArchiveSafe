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
    for i in range (1,2):
        CreateFiles(i)
 

def CreateFiles(d):

    repfilename = 'D2_WriteRunReport_' + str(datetime.datetime.now()) + '.txt'
    repfile = open(repfilename,"w+")
    MyDir = '/home/moes/Documents/Test/2/'
    for j in range (1,2):
        for i in range (1001,2001):
            currfile = MyDir + 'D2_1k_' + str(i) 
            allchar = string.ascii_letters + string.digits
            fillstr = "".join(choice(allchar) for x in range(1000))
            starttime = time.time()
            f = open(currfile,"w+")
            f.write(fillstr)
            f.close
            endtime = time.time()
            repstr = currfile + "," + str(endtime - starttime) + '\n'
            repfile.write(repstr)

        for i in range (1001,2001):
            currfile = MyDir + 'D2_100k_' + str(i) 
            allchar = string.ascii_letters + string.digits
            fillstr = "".join(choice(allchar) for x in range(100000))
            starttime = time.time()
            f = open(currfile,"w+")
            f.write(fillstr)
            f.close
            endtime = time.time()
            repstr = currfile + "," + str(endtime - starttime) + '\n'
            repfile.write(repstr)

        for i in range (1001,2001):
            currfile = MyDir + 'D0_1M_' + str(i)
            allchar = string.ascii_letters + string.digits
            fillstr = "".join(choice(allchar) for x in range(1000000))
            starttime = time.time()
            f = open(currfile,"w+")
            f.write(fillstr)
            f.close
            endtime = time.time()
            repstr = currfile + "," + str(endtime - starttime) + '\n'
            repfile.write(repstr)

        for i in range (1001,2001):
            currfile = MyDir + 'D2_10M_' + str(i)
            allchar = string.ascii_letters + string.digits
            fillstr = "".join(choice(allchar) for x in range(10000000))
            starttime = time.time()
            f = open(currfile,"w+")
            f.write(fillstr)
            f.close
            endtime = time.time()
            repstr = currfile + "," + str(endtime - starttime) + '\n'
            repfile.write(repstr)

        for i in range (1001,1201):
            currfile = MyDir + 'D2_100M_' + str(i)
            allchar = string.ascii_letters + string.digits
            fillstr = "".join(choice(allchar) for x in range(100000000))
            starttime = time.time()
            f = open(currfile,"w+")
            f.write(fillstr)
            f.close
            endtime = time.time()
            repstr = currfile + "," + str(endtime - starttime) + '\n'
            repfile.write(repstr)





if __name__ == '__main__':
    main()  
