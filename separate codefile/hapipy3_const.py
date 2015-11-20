# -*- coding: utf-8 -*-

'''
This module provides constants definitions to HITRAN data.
'''
 
# define precision
__ComplexType__ = complex128
__IntegerType__ = int64
__FloatType__ = float64

# define zero
cZero = __FloatType__(0.)

# physical constants
cBolts = 1.380648813E-16 # erg/K, CGS
cc = 2.99792458e10 # cm/s, CGS
hh = 6.626196e-27 # erg*s, CGS

# computational constants
cSqrtLn2divSqrtPi = 0.469718639319144059835
cLn2 = 0.6931471805599
cSqrtLn2 = 0.8325546111577
cSqrt2Ln2 = 1.1774100225


# declare global variables
GLOBAL_DEBUG = False
GLOBAL_CURRENT_DIR ='.'

GLOBAL_HITRAN_APIKEY = 'e20e4bd3-e12c-4931-99e0-4c06e88536bd'

GLOBAL_USER = 'user'
GLOBAL_REQUISITES = []

GLOBAL_CONNECTION = []
GLOBAL_DATABASE = 'hitran'

LOCAL_HOST = 'localhost'

# DEBUG switch
if GLOBAL_DEBUG:
   GLOBAL_HOST = LOCAL_HOST+':8000' # localhost
else:
   GLOBAL_HOST = 'http://hitran.org'

# this is a backup url in the case GLOBAL_HOST does not work
GLOBAL_HOST_BACKUP = 'http://hitranazure.cloudapp.net/'


# UNPARSED QUERY OBJECT
# uses formal language (SQL, noSQL, custom...)
GlobalQueryString = ''

# PARSED QUERY OBJECT
# = prototype for a Query instance
# there should be a getAttrbute/setSettribute functions defined
# For Django: Query=QuerySet (as  an example)
Query = {}

# prototype for cache storage
# there must be function for record/retrieve
# caching is performed by the value of Query
# cache parameters: (query+table_name)
# if there is already table with such query, copy it
# if there is already tble with such query AND table_name,
# return it as is => IT MAY DEPEND ON CERTAIN QUERY TYPE!!
TABLES = {} # hash/dictionary


# ---------- NODE MANAGEMENT ------------------

# An interface for a node manager will follow soon.
# This is an implementation in Python
# Different implementations are language-specific.

# dafault node with simple DB engine
# Prototype for a global nodelist for a given host

# each node has it's unique ID, host name and 
#   node name within it's host

NODE_NAME = 'local'

GLOBAL_NODENAMES = {
   0 : 'hitran-main',
   1 : 'local'
}

GLOBAL_NODELIST = {
   0 : {  # main HITRAN node
       'host' : GLOBAL_HOST,
       'ACCESS_KEY' : '9b6a7975-2a84-43d8-920e-f4dea9db6805' # guest
   },
   1 : {  # local node prototype
       'host' : LOCAL_HOST,
       'ACCESS_KEY' : '6cfd7040-24a6-4197-81f9-6e25e50005b2', # admin
   }
}


# ---------- NODE AUTH SYSTEM -----------------

# AUTH SYSTEM is tightly connected to Node manager.

# Prototype for authentication  system.
# AUTH is responsible for giving an access privileges to all users.
# Each users has a key ACCESS_KEY which is stored in
#  a special database HOST:ACCESS_KEYS on a host.
# Every node has a separate privileges list connected with
#  each key. Auth system 

# The current auth system is based on secret keys of access
# Default key is 'admin', it's created seamlessly for a local admin.

# Prototype for key storage

# RECONSIDER THIS LATER !!!

GLOBAL_PRIVILEGES = {
   'admin' : {
       'ACCESS_KEY' : '6cfd7040-24a6-4197-81f9-6e25e50005b2',
       'LEVEL' : 'ADMIN'
   },
   'guest' : {
       'ACCESS_KEY' : '9b6a7975-2a84-43d8-920e-f4dea9db6805',
       'LEVEL' : 'USER'
   }
}


# ---------- DATABASE FRONTEND ----------------
#FORMAT_PYTHON_REGEX = '^\%([0-9]*)\.?([0-9]*)([dfs])$'
FORMAT_PYTHON_REGEX = '^\%(\d*)(\.(\d*))?([edfsEDFS])$'

# ----------------------------------------------------
# ----------------------------------------------------
# CONDITIONS
# ----------------------------------------------------
# ----------------------------------------------------
# ----------------------------------------------------
# hierarchic query.condition language:
# Conditions: CONS = ('and', ('=','p1','p2'), ('<','p1',13))
# String literals are distinguished from variable names 
#  by using the operation ('STRING','some_string')
# ----------------------------------------------------

# necessary conditions for hitranonline:
SAMPLE_CONDITIONS = ('AND',('SET','internal_iso_id',[1,2,3,4,5,6]),('>=','nu',0),('<=','nu',100))

# sample hitranonline protocol
# http://hitran.cloudapp.net/lbl/5?output_format_id=1&iso_ids_list=5&numin=0&numax=100&access=api&key=e20e4bd3-e12c-4931-99e0-4c06e88536bd

CONDITION_OPERATIONS = set(['AND','OR','NOT','RANGE','IN','<','>','<=','>=','==','!=','LIKE','STR','+','-','*','/','MATCH','SEARCH','FINDALL'])


# GROUPING ---------------------------------------------- 

GROUP_INDEX = {}
# GROUP_INDEX has the following structure:
#  GROUP_INDEX[KEY] = VALUE
#    KEY = table line values
#    VALUE = {'FUNCTIONS':DICT,'FLAG':LOGICAL,'ROWID':INTEGER}
#      FUNCTIONS = {'FUNC_NAME':DICT}
#            FUNC_NAME = {'FLAG':LOGICAL,'NAME':STRING}

# name and default value
GROUP_FUNCTION_NAMES = { 'COUNT' :  0,
                         'SUM'   :  0,
                         'MUL'   :  1,
                         'AVG'   :  0,
                         'MIN'   : +1e100,
                         'MAX'   : -1e100,
                         'SSQ'   : 0,
                       }


# EXTRACTING ========================================================

REGEX_INTEGER = '[+-]?\d+'
REGEX_STRING = '[^\s]+'
REGEX_FLOAT_F = '[+-]?\d*\.?\d+'
REGEX_FLOAT_E = '[+-]?\d*\.?\d+[eEfF]?[+-]?\d+' 


QUERY_BUFFER = '__BUFFER__'

# NODE CODE 
NODE_READY = False


# iso.py
profiles = 'profiles'
tutorial='tutorial'
units='units'
index='index'
data='data'
spectra='spectra'
plotting='plotting'
python='python'

python_tutorial_text = \


# define static data
zone = __ComplexType__(1.0e0 + 0.0e0j)
zi = __ComplexType__(0.0e0 + 1.0e0j)
tt = __FloatType__([0.5e0,1.5e0,2.5e0,3.5e0,4.5e0,5.5e0,6.5e0,7.5e0,8.5e0,9.5e0,10.5e0,11.5e0,12.5e0,13.5e0,14.5e0])
pipwoeronehalf = __FloatType__(0.564189583547756e0)

T = __FloatType__([0.314240376e0,0.947788391e0,1.59768264e0,2.27950708e0,3.02063703e0,3.8897249e0])
U = __FloatType__([1.01172805e0,-0.75197147e0,1.2557727e-2,1.00220082e-2,-2.42068135e-4,5.00848061e-7])
S = __FloatType__([1.393237e0,0.231152406e0,-0.155351466e0,6.21836624e-3,9.19082986e-5,-6.27525958e-7])

PROFILE_HTP = PROFILE_HT # stub for backwards compatibility


# ------------------------------- /PARAMETER DEPENDENCIES --------------------------------

# default parameter bindings
DefaultParameterBindings = {}

# default temperature dependencies
DefaultEnvironmentDependencyBindings = {}

# ------------------------------- /BINGINGS --------------------------------

# default values for intensity threshold
DefaultIntensityThreshold = 0. # cm*molec

# default value for omega wing in halfwidths (from center)
DefaultOmegaWingHW = 50. # cm-1    HOTW default

absorptionCoefficient_Gauss = absorptionCoefficient_Doppler
