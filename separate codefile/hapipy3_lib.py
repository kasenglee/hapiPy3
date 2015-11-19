# -*- coding: utf-8 -*-

'''
This module provides a lib to HITRAN data.
'''

import httplib
import urllib2
import json
import os, os.path
import re
from os import listdir
from numpy import zeros,array,zeros,where,setdiff1d,ndarray,arange
from numpy import complex128,complex64,int64,int32,float64,float32
from numpy import sqrt,abs,exp,pi,log,sin,cos
from numpy import convolve
#from numpy import linspace
from numpy import any,minimum,maximum
from numpy import modf
from numpy import sort as npsort
from bisect import bisect
#from collections import OrderedDict
from warnings import warn
from urllib2 import HTTPError,URLError
import pydoc

HAPI_VERSION = '1.0'

# version header
print('HAPI VERSION: %s' % HAPI_VERSION)