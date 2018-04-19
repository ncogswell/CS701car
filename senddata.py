#!/usr/bin/python3
from time import time
from subprocess import call

call(['sshpass', '-p', 'Gr4ndT3ton!', 'ssh', 'ncogswell@gattaca.cs.middlebury.edu', "rm *.bmp"])
