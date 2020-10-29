# ArchiveSafe
Python application using FUSE to demonstrate client puzzles usage in archives. This application was developed as an evaluation experiment for a research paper https://arxiv.org/abs/2009.00086.

The code is written in pyrhon 3. It is wrapping a FUSE driver from https://github.com/skorokithakis/python-fuse-sample.

Command to run: python3 MyFuse_D1.py mountpoint root &

Prerequisites:
 - python3-pip
 - argon2
 - fusepy
 - argon2-cffi
 - passlib
 - pyOpenSSL

createfiles.py: Creates test files for the experiment and record processing times to a report file.
readfiles.py: Reads the files created by createfiles.py and record processing times to a report file.
