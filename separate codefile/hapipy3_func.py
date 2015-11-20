# -*- coding: utf-8 -*-

'''
This module provides function definitions to HITRAN data.
'''

# define float range
def frange(x,y,step):
  while x<y:
    yield x
    x+=step


# interface for checking of variable's existance   
def empty(Instance):
    return True if Instance else False

# general interface for getattr
def getAttribute(Object,Attribute):
    return getattr(Object,Attribute)

# general interface for setattr
def setAttribute(Object,Attribute,Value):
    setattr(Object,Attribute,Value)
    return


# ---------- CONNECTION MANAGEMENT-------------

# interface for establishing HTTP connection
# can return object/structure/handle
def setupConnection(Host=GLOBAL_HOST):
    Connection = httplib.HTTPConnection(Host)
    if not empty(Connection):
       return Connection
    else:
       raise Exception('can''t setup connection')

# interface for HTTP-get method
# Connection must be established before use
def httpGet(URL,Connection=GLOBAL_CONNECTION):
    Method = 'get'
    ServerResponse = Connection.request(Method,URL)
    return ServerResponse

# parse local data language to remote frontend
# !!!!!!!!!
def parseToFrontend(Query,Host=GLOBAL_HOST):
    # convert Query object to server frontend's 
    # query language
    pass 
 
def prepareURL(Query,Connection=GLOBAL_CONNECTION):
    # make full URL from server name and it's parameters
    # considering server's frontend query language
    Host = getAttribute(Connection,'host')
    HostQuery = parseToFrontend(Query)
    URL = Host+HostQuery
    return URL

# stream raw data from the server
# the data is assumed to be very large that
# ordinary get is unefficient
def streamRawDataRemote(Query,Connection=GLOBAL_CONNECTION):
    pass

# collect raw data in whatever format server gives it
def getRawDataRemote(Query,Connection=GLOBAL_CONNECTION):
    URL = prepareURL(Query,Connection)    
    ServerResponse=httpGet(URL,Connection)
    return ServerResponse

## parse raw data 
#def parseRawData(RawData)
#    pass

# ---------- CONNECTION MANAGEMEND END --------


# ---------- NODE MANAGEMENT ------------------

# An interface for a node manager will follow soon.
# This is an implementation in Python
# Different implementations are language-specific.

# dafault node with simple DB engine
# Prototype for a global nodelist for a given host

# each node has it's unique ID, host name and 
#   node name within it's host
def createNode(NodeID,NodeList=GLOBAL_NODELIST):
    # create a node, throw if exists
    node = NodeList.get(NodeID)
    if node: raise Exception('node %s already exists' % NodeName)
    NodeList[NodeID] = {}
    pass

def getNodeIDs(NodeList=GLOBAL_NODELIST):
    # return list of all available nodes
    return NodeList.keys()

def getNodeProperty(NodeID,PropName,NodeList=GLOBAL_NODELIST):
    # get a property for certain node
    # if not found throw exception
    node = NodeList.get(NodeName)
    if node:
       prop = node.get(PropName)
       if prop:
          return prop
       else:
          raise Exception('node %s doesn''t have property %s' % (ModeName,Propname) )       
    else:
       raise Exception('no such node %s' % Nodename)

def setNodeProperty(NodeID,PropName,PropValue,NodeList=GLOBAL_NODELIST):
    # set a property for certain node
    # throw exception if node not found
    # if the property doesn't exist it will appear
    node = NodeList.get(NodeID)
    if not node: raise Exception('no such node %s ' % NodeName)
    NodeList[PropName] = PropValue
    return

def resolveNodeID(NodeName,NodeNames=GLOBAL_NODENAMES):
    for NodeID in NodeNames.keys():
        if NodeNames[NodeID]==NodeName: return NodeID

def checkAccess(DBName,TableName,NodeName,UserName,Requisites,NodeList=GLOBAL_NODELIST,NodeNames=GLOBAL_NODENAMES):
    # simple node-level authentication (bridge to AUTH system)
    NodeID = resolveNodeID(NodeName,NodeNames)
    Node = NodeList[NodeID]
    if Requisites.key in Node['keys_allowed']:
       return True
    else:
       return False

# ---------- NODE MANAGEMENT END --------------


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
def addUser():
    pass

def deleteUser():
    pass

def authenticate(UserName,Requisites,Privileges=GLOBAL_PRIVILEGES):
    # Authentication
    key_list = [Privileges[User]['ACCESS_KEY'] for User in Privileges.keys]
    return True if Requisites.AccessKey in key_list else False

def checkPrivileges(Path,UserName=GLOBAL_USER,Requisites=GLOBAL_REQUISITES,
                    Privileges=GLOBAL_PRIVILEGES,NodeList=GLOBAL_NODELIST,Nodenames=GLOBAL_NODENAMES):
    # Privileges are checked before executing every query (needs optimization)
    # Path example: SOME_DB::SOME_TABLE::SOME_NODE
    if not authenticate(UserName,Requisites,Privileges): return False
    (DBName,TableName,NodeName)=Path.split('::')
    # loop on all nodes , use NODE_MANAGER's functions instead of 
    #   working with GLOBAL_NODELIST directly
    if not checkAccess(DBName,TableName,NodeName,UserName,Requisites,NodeList,NodeNames):
       return False
    return True

# ---------- NODE AUTH SYSTEM END -------------


# ---------- DATABASE FRONTEND ----------------
def transport2object(TransportData):
    pass

def object2transport(ObjectData):
    pass

def getFullTableAndHeaderName(TableName):
    #print('TableName=',TableName)
    fullpath_data = VARIABLES['BACKEND_DATABASE_NAME'] + '/' + TableName + '.data'
    if not os.path.isfile(fullpath_data):
        fullpath_data = VARIABLES['BACKEND_DATABASE_NAME'] + '/' + TableName + '.par'
        if not os.path.isfile(fullpath_data):
            raise Exception('Lonely header \"%s\"' % fullpath_data)
    fullpath_header = VARIABLES['BACKEND_DATABASE_NAME'] + '/' + TableName + '.header'
    return fullpath_data,fullpath_header

def getParameterFormat(ParameterName,TableName):
    return LOCAL_TABLE_CACHE[TableName]['header']['format']


def getTableHeader(TableName):
    return LOCAL_TABLE_CACHE[TableName]['header']

# RowObject = list of tuples like (name,value,format)
def addRowObject(RowObject,TableName):
    # add RowObject to TableObject in CACHE
    # check consistency first
    if [p[0] for p in RowObject] != LOCAL_TABLE_CACHE[TableName]['header']['order']:
       raise Exception('The row is not consistent with the table')
    for par_name,par_value,par_format in RowObject:
        LOCAL_TABLE_CACHE[TableName]['data'][par_name] += par_value
    pass

def getRowObject(RowID,TableName):
    # return RowObject from TableObject in CACHE
    RowObject = []
    for par_name in LOCAL_TABLE_CACHE[TableName]['header']['order']:
        par_value = LOCAL_TABLE_CACHE[TableName]['data'][par_name][RowID]
        par_format = LOCAL_TABLE_CACHE[TableName]['header']['format'][par_name]
        RowObject.append((par_name,par_value,par_format))
    return RowObject

# INCREASE ROW COUNT
def addRowObject(RowObject,TableName):
    #print 'addRowObject: '
    #print 'RowObject: '+str(RowObject)
    #print 'TableName:'+TableName
    for par_name,par_value,par_format in RowObject:
        #print 'par_name,par_value,par_format: '+str((par_name,par_value,par_format))
        #print '>>> '+ str(LOCAL_TABLE_CACHE[TableName]['data'][par_name])
        LOCAL_TABLE_CACHE[TableName]['data'][par_name] += [par_value]

def setRowObject(RowID,RowObject,TableName):
    number_of_rows = LOCAL_TABLE_CACHE[TableName]['header']['number_of_rows']
    if RowID >= 0 and RowID < number_of_rows:
       for par_name,par_value,par_format in RowObject:
           LOCAL_TABLE_CACHE[TableName]['data'][par_name][RowID] = par_value
    else:
       # !!! XXX ATTENTION: THIS IS A TEMPORARY INSERTION XXX !!!
       LOCAL_TABLE_CACHE[TableName]['header']['number_of_rows'] += 1
       addRowObject(RowObject,TableName)

def getDefaultRowObject(TableName):
    # get a default RowObject from a table
    RowObject = []
    for par_name in LOCAL_TABLE_CACHE[TableName]['header']['order']:
        par_value = LOCAL_TABLE_CACHE[TableName]['header']['default'][par_name]
        par_format = LOCAL_TABLE_CACHE[TableName]['header']['format'][par_name]
        RowObject.append((par_name,par_value,par_format))
    return RowObject

def subsetOfRowObject(ParameterNames,RowObject):
    # return a subset of RowObject according to 
    #RowObjectNew = []
    #for par_name,par_value,par_format in RowObject:
    #     if par_name in ParameterNames:
    #        RowObjectNew.append((par_name,par_value,par_format))
    #return RowObjectNew
    dct = {}
    for par_name,par_value,par_format in RowObject:
        dct[par_name] = (par_name,par_value,par_format)
    RowObjectNew = []
    for par_name in ParameterNames:
        RowObjectNew.append(dct[par_name])
    return RowObjectNew


# Fortran string formatting
#  based on a pythonic format string
def formatString(par_format,par_value,lang='FORTRAN'):
    # Fortran format rules:
    #  %M.NP
    #        M - total field length (optional)
    #             (minus sign included in M)
    #        . - decimal ceparator (optional)
    #        N - number of digits after . (optional)
    #        P - [dfs] int/float/string
    # PYTHON RULE: if N is abcent, default value is 6
    regex = FORMAT_PYTHON_REGEX
    (lng,trail,lngpnt,ty) = re.search(regex,par_format).groups()
    result = par_format % par_value
    if ty.lower() in set(['f','e']):
       lng = int(lng) if lng else 0
       lngpnt = int(lngpnt) if lngpnt else 0
       result = par_format % par_value
       res = result.strip()
       if lng==lngpnt+1:
          if res[0:1]=='0':
             result =  '%%%ds' % lng % res[1:]
       if par_value<0:
          if res[1:2]=='0':
             result = '%%%ds' % lng % (res[0:1]+res[2:])
    return result

def formatGetLength(fmt,lang='FORTRAN'):
    regex = FORMAT_PYTHON_REGEX
   
def putRowObjectToString(RowObject):
    # serialize RowObject to string
    # TODO: support different languages (C,Fortran)
    output_string = ''
    for par_name,par_value,par_format in RowObject:
        # Python formatting
        #output_string += par_format % par_value
        # Fortran formatting
        #print 'par_name,par_value,par_format: '+str((par_name,par_value,par_format))
        output_string += formatString(par_format,par_value)
    return output_string

def putTableHeaderToString(TableName):
    output_string = ''
    regex = FORMAT_PYTHON_REGEX
    for par_name in LOCAL_TABLE_CACHE[TableName]['header']['order']:
        par_format = LOCAL_TABLE_CACHE[TableName]['header']['format'][par_name]
        (lng,trail,lngpnt,ty) = re.search(regex,par_format).groups()
        fmt = '%%%ss' % lng
        try:
            par_name_short = PARAMETER_NICKNAMES[par_name]
        except:
            par_name_short = par_name
        #output_string += fmt % par_name
        output_string += (fmt % par_name_short)[:int(lng)]
    return output_string

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def getRowObjectFromString(input_string,TableName):
    # restore RowObject from string, get formats and names in TableName
    #print 'getRowObjectFromString:'
    pos = 0
    RowObject = []
    #print 'Header: '+str(LOCAL_TABLE_CACHE[TableName]['header'])
    for par_name in LOCAL_TABLE_CACHE[TableName]['header']['order']:
        #print 'ITERATION\npos: '+str(pos) #
        #print 'par_name: '+par_name #
        par_format = LOCAL_TABLE_CACHE[TableName]['header']['format'][par_name]
        #print 'par_format: '+par_format #
        regex = '^\%([0-9]+)\.?[0-9]*([dfs])$' #
        regex = FORMAT_PYTHON_REGEX
        #print 'par_name: '+par_name #
        (lng,trail,lngpnt,ty) = re.search(regex,par_format).groups()
        lng = int(lng)
        #print 'lng,ty:'+str((lng,ty)) #
        par_value = input_string[pos:(pos+lng)]
        #print 'par_value: '+par_value #
        if ty=='d': # integer value
           par_value = int(par_value)
        elif ty.lower() in set(['e','f']): # float value
           par_value = float(par_value)
        elif ty=='s': # string value
           #par_value = par_value.strip() # strip spaces and tabs
           pass # don't strip string value
        else:
           raise Exception('Format \"%s\" is unknown' % par_format)
        RowObject.append((par_name,par_value,par_format))
        pos += lng
    return RowObject
    #LOCAL_TABLE_CACHE[TableName]['data'][par_name] += par_value # or append()?
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# Conversion between OBJECT_FORMAT and STORAGE_FORMAT
# This will substitute putTableToStorage and getTableFromStorage
def cache2storage(TableName):
    #print 'cache2storage:'
    try:
       os.mkdir(VARIABLES['BACKEND_DATABASE_NAME'])
    except:
       pass
    fullpath_data,fullpath_header = getFullTableAndHeaderName(TableName)
    #print 'fullpath_data:'+fullpath_data
    #print 'fullpath_header'+fullpath_header
    # check if file exists and throw an exception
    #if isfile(fullpath_data): raise Exception('Table \"%s\" already exists',NewTableName)
    #if isfile(fullpath_header): raise Exception('SCHEMA IS BROKEN')
    OutfileData = open(fullpath_data,'w')
    OutfileHeader = open(fullpath_header,'w')
    # write table data
    line_count = 1
    line_number = LOCAL_TABLE_CACHE[TableName]['header']['number_of_rows']
    for RowID in range(0,LOCAL_TABLE_CACHE[TableName]['header']['number_of_rows']):
        #print '%d line from %d' % (line_count,line_number)
        line_count += 1
        RowObject = getRowObject(RowID,TableName)
        #print 'RowObject:'+str(RowObject)
        raw_string = putRowObjectToString(RowObject)
        #print 'RowObject_string:'+raw_string
        OutfileData.write(raw_string+'\n')
    # write table header
    TableHeader = getTableHeader(TableName)
    OutfileHeader.write(json.dumps(TableHeader,indent=2))
    
def storage2cache(TableName):
    #print 'storage2cache:'
    #print('TableName',TableName)
    fullpath_data,fullpath_header = getFullTableAndHeaderName(TableName)
    InfileData = open(fullpath_data,'r')
    InfileHeader = open(fullpath_header,'r')
    #try:
    header_text = InfileHeader.read()
    try:
        Header = json.loads(header_text)
    except:
        print('HEADER:')
        print(header_text)
        raise Exception('Invalid header')
    #print 'Header:'+str(Header)
    LOCAL_TABLE_CACHE[TableName] = {}
    LOCAL_TABLE_CACHE[TableName]['header'] = Header
    LOCAL_TABLE_CACHE[TableName]['data'] = {}
    # initialize empty data to avoid problems
    for par_name in LOCAL_TABLE_CACHE[TableName]['header']['order']:
        LOCAL_TABLE_CACHE[TableName]['data'][par_name] = []
    line_count = 0
    #line_number = LOCAL_TABLE_CACHE[TableName]['header']['number_of_rows']
    for line in InfileData:
        #print '%d line from %d' % (line_count,line_number)
        #print 'line: '+line #
        try:
            RowObject = getRowObjectFromString(line,TableName)
            line_count += 1
        except:
            continue
        #print 'RowObject: '+str(RowObject)
        addRowObject(RowObject,TableName)
    #except:
    #    raise Exception('TABLE FETCHING ERROR')
    LOCAL_TABLE_CACHE[TableName]['header']['number_of_rows'] = line_count
    InfileData.close()
    InfileHeader.close()
    print '                     Lines parsed: %d' % line_count
    pass

# / FORMAT CONVERSION LAYER

def getTableNamesFromStorage(StorageName):
    file_names = listdir(StorageName)
    table_names = []
    for file_name in file_names:
        # search all files with "header" extensions
        #matchObject = re.search('(\w+)\.header$',file_name)
        matchObject = re.search('(.+)\.header$',file_name)
        if matchObject:
           #print('matchObject.group(1)=',matchObject.group(1))
           table_names.append(matchObject.group(1))
    return table_names

# FIX POSSIBLE BUG: SIMILAR NAMES OF .PAR AND .DATA FILES
# BUG FIXED BY INTRODUCING A PRIORITY:
#   *.data files have more priority than *.par files
#   See getFullTableAndHeaderName function for explanation
def scanForNewParfiles(StorageName):
    file_names = listdir(StorageName)
    headers = {} # without extensions!
    parfiles_without_header = []
    for file_name in file_names:
        # create dictionary of unique headers
        try:
            #fname,fext = re.search('(\w+)\.(\w+)',file_name).groups()
            fname,fext = re.search('(.+)\.(\w+)',file_name).groups()
        except:
            continue
        if fext == 'header': headers[fname] = True
    for file_name in file_names:
        # check if extension is 'par' and the header is absent
        try:
            #fname,fext = re.search('(\w+)\.(\w+)',file_name).groups()
            fname,fext = re.search('(.+)\.(\w+)',file_name).groups()
        except:
            continue
        if fext == 'par' and fname not in headers:
            parfiles_without_header.append(fname)
    return parfiles_without_header

def createHeader(TableName):
    fname = TableName+'.header'
    fp = open(VARIABLES['BACKEND_DATABASE_NAME']+'/'+fname,'w')
    if os.path.isfile(TableName):
        raise Exception('File \"%s\" already exists!' % fname)
    fp.write(json.dumps(HITRAN_DEFAULT_HEADER,indent=2))
    fp.close()

def loadCache():
    #print 'loadCache:'
    print('Using '+VARIABLES['BACKEND_DATABASE_NAME']+'\n')
    LOCAL_TABLE_CACHE = {} # ?????
    table_names = getTableNamesFromStorage(VARIABLES['BACKEND_DATABASE_NAME'])
    #print('table_names=',table_names)
    parfiles_without_header = scanForNewParfiles(VARIABLES['BACKEND_DATABASE_NAME'])
    # create headers for new parfiles
    for tab_name in parfiles_without_header:
        # get name without 'par' extension
        createHeader(tab_name)
        table_names.append(tab_name)
    for TableName in table_names:
        print TableName
        storage2cache(TableName)

def saveCache():
    #print 'saveCache:'
    try:
        # delete query buffer
        del LOCAL_TABLE_CACHE[QUERY_BUFFER]
    except:
        pass
    for TableName in LOCAL_TABLE_CACHE:
        print TableName
        cache2storage(TableName)

# DB backend level, start transaction
def databaseBegin(db=None):
    if db:
       VARIABLES['BACKEND_DATABASE_NAME'] = db
    else:
       VARIABLES['BACKEND_DATABASE_NAME'] = BACKEND_DATABASE_NAME_DEFAULT
    #print 'databaseBegin:'
    #print(os.path.isdir("/home/el"))
    #print(os.path.exists("/home/el/myfile.txt"))
    if not os.path.exists(VARIABLES['BACKEND_DATABASE_NAME']):
       os.mkdir(VARIABLES['BACKEND_DATABASE_NAME'])
    loadCache()

# DB backend level, end transaction
def databaseCommit():
    #print 'databaseCommit:'
    saveCache()

# Operations used in Condition verification
# Basic scheme: operationXXX(args),
# where args - list/array of arguments (>=1)

def operationAND(args):
    # any number if arguments
    for arg in args:
        if not arg:
           return False
    return True

def operationOR(args):
    # any number of arguments
    for arg in args:
        if arg:
           return True
    return False

def operationNOT(arg):
    # one argument
    return not arg

def operationRANGE(x,x_min,x_max):
    return x_min <= x <= x_max
    
def operationSUBSET(arg1,arg2):
    # True if arg1 is subset of arg2
    # arg1 is an element
    # arg2 is a set
    return arg1 in arg2

def operationLESS(args):
    # any number of args
    for i in range(1,len(args)):
        if args[i-1] >= args[i]:
           return False
    return True

def operationMORE(args):
    # any number of args
    for i in range(1,len(args)):
        if args[i-1] <= args[i]:
           return False
    return True

def operationLESSOREQUAL(args):
    # any number of args
    for i in range(1,len(args)):
        if args[i-1] > args[i]:
           return False
    return True

def operationMOREOREQUAL(args):
    # any number of args
    for i in range(1,len(args)):
        if args[i-1] < args[i]:
           return False
    return True

def operationEQUAL(args):
    # any number of args
    for i in range(1,len(args)):
        if args[i] != args[i-1]:
           return False
    return True

def operationNOTEQUAL(arg1,arg2):
    return arg1 != arg2
    
def operationSUM(args):
    # any numbers of arguments
    if type(args[0]) in set([int,float]):
       result = 0
    elif type(args[0]) in set([str,unicode]):
       result = ''
    else:
       raise Exception('SUM error: unknown arg type')
    for arg in args:
        result += arg
    return result

def operationDIFF(arg1,arg2):
    return arg1-arg2

def operationMUL(args):
    # any numbers of arguments
    if type(args[0]) in set([int,float]):
       result = 1
    else:
       raise Exception('MUL error: unknown arg type')
    for arg in args:
        result *= arg
    return result

def operationDIV(arg1,arg2):
    return arg1/arg2

def operationSTR(arg):
    # transform arg to str
    if type(arg)!=str:
       raise Exception('Type mismatch: STR')
    return arg

def operationSET(arg):
    # transform arg to list
    if type(arg) not in set([list,tuple,set]):
        raise Exception('Type mismatch: SET')
    return list(arg)

def operationMATCH(arg1,arg2):
    # Match regex (arg1) and string (arg2)
    #return bool(re.match(arg1,arg2)) # works wrong
    return bool(re.search(arg1,arg2))

def operationSEARCH(arg1,arg2):
    # Search regex (arg1) in string (arg2)
    # Output list of entries
    group = re.search(arg1,arg2).groups()
    result = []
    for item in group:
        result.append(('STR',item))
    return result

def operationFINDALL(arg1,arg2):
    # Search all groups of a regex
    # Output a list of groups of entries
    # XXX: If a group has more than 1 entry,
    #    there could be potential problems
    list_of_groups = re.findall(arg1,arg2)
    result = []
    for item in list_of_groups:
        result.append(('STR',item))
    return result

def operationLIST(args):
    # args is a list: do nothing (almost)
    return list(args)

# /operations

#def parse(Conditions):
#    pass

def BACKUP__evaluateExpression__BACKUP(root,VarDictionary):
    # input = local tree root
    # XXX: this could be very slow due to passing
    #      every time VarDictionary as a parameter
    # Two special cases: 1) root=varname
    #                    2) root=list/tuple
    # These cases must be processed in a separate way
    if type(root) in set([list,tuple]):
       # root is not a leaf
       head = root[0].upper()
       # string constants are treated specially
       if head in set(['STR','STRING']): # one arg
          return operationSTR(root[1])
       elif head in set(['SET','LIST']):
          return operationSET(root[1])
       tail = root[1:]
       args = []
       # evaluate arguments recursively
       for element in tail: # resolve tree by recursion
           args.append(evaluateExpression(element,VarDictionary))
       # call functions with evaluated arguments
       if head in set(['&','&&','AND']): # many args 
          return operationAND(args)
       elif head in set(['|','||','OR']): # many args
          return operationOR(args)
       elif head in set(['!','NOT']): # one args
          return operationNOT(args[0])
       elif head in set(['RANGE','BETWEEN']): # three args
          return operationRANGE(args[0],args[1],args[2])
       elif head in set(['IN','SUBSET']): # two args
          return operationSUBSET(args[0],args[1])
       elif head in set(['<','LESS','LT']): # many args
          return operationLESS(args)
       elif head in set(['>','MORE','MT']): # many args
          return operationMORE(args)
       elif head in set(['<=','LESSOREQUAL','LTE']): # many args
          return operationLESSOREQUAL(args)
       elif head in set(['>=','MOREOREQUAL','MTE']): # many args
          return operationMOREOREQUAL(args)
       elif head in set(['=','==','EQ','EQUAL','EQUALS']): # many args
          return operationEQUAL(args)
       elif head in set(['!=','<>','~=','NE','NOTEQUAL']): # two args
          return operationNOTEQUAL(args[0],args[1])
       elif head in set(['+','SUM']): # many args
          return operationSUM(args)
       elif head in set(['-','DIFF']): # two args
          return operationDIFF(args[0],args[1])
       elif head in set(['*','MUL']): # many args
          return operationMUL(args)
       elif head in set(['/','DIV']): # two args
          return operationDIV(args[0],args[1])
       elif head in set(['MATCH','LIKE']): # two args
          return operationMATCH(args[0],args[1])
       elif head in set(['SEARCH']): # two args
          return operationSEARCH(args[0],args[1])
       elif head in set(['FINDALL']): # two args
          return operationFINDALL(args[0],args[1])
       else:
          raise Exception('Unknown operator: %s' % root[0])
    elif type(root)==str:
       # root is a par_name
       return VarDictionary[root]
    else: 
       # root is a non-string constant
       return root


# GROUPING ---------------------------------------------- 
def clearGroupIndex():
    #GROUP_INDEX = {}
    # XXX ??? is there a better solution ???
    for key in GROUP_INDEX.keys():
        del GROUP_INDEX[key]

def getValueFromGroupIndex(GroupIndexKey,FunctionName):
    # If no such index_key, create it and return a value
    if FunctionName not in GROUP_FUNCTION_NAMES:
       raise Exception('No such function \"%s\"' % FunctionName)
    # In the case if NewRowObjectDefault is requested
    if not GroupIndexKey:
       return GROUP_FUNCTION_NAMES[FunctionName]
    if FunctionName not in GROUP_INDEX[GroupIndexKey]['FUNCTIONS']:
       GROUP_INDEX[GroupIndexKey]['FUNCTIONS'][FunctionName] = {}
       GROUP_INDEX[GroupIndexKey]['FUNCTIONS'][FunctionName]['FLAG'] = True
       GROUP_INDEX[GroupIndexKey]['FUNCTIONS'][FunctionName]['VALUE'] = \
         GROUP_FUNCTION_NAMES[FunctionName]
    return GROUP_INDEX[GroupIndexKey]['FUNCTIONS'][FunctionName]['VALUE']

def setValueToGroupIndex(GroupIndexKey,FunctionName,Value):
    GROUP_INDEX[GroupIndexKey]['FUNCTIONS'][FunctionName]['VALUE'] = Value

def initializeGroup(GroupIndexKey):
    if GroupIndexKey not in GROUP_INDEX:
        print 'GROUP_DESC[COUNT]='+str(GROUP_DESC['COUNT'])
        GROUP_INDEX[GroupIndexKey] = {}
        GROUP_INDEX[GroupIndexKey]['FUNCTIONS'] = {}
        GROUP_INDEX[GroupIndexKey]['ROWID'] = len(GROUP_INDEX) - 1
    for FunctionName in GROUP_FUNCTION_NAMES:
        # initialize function flags (UpdateFlag)
        if FunctionName in GROUP_INDEX[GroupIndexKey]['FUNCTIONS']:
           GROUP_INDEX[GroupIndexKey]['FUNCTIONS'][FunctionName]['FLAG'] = True
    print 'initializeGroup: GROUP_INDEX='+str(GROUP_INDEX)

def groupCOUNT(GroupIndexKey):
    FunctionName = 'COUNT'
    Value = getValueFromGroupIndex(GroupIndexKey,FunctionName)
    if GroupIndexKey:
       if GROUP_INDEX[GroupIndexKey]['FUNCTIONS'][FunctionName]['FLAG']:
          GROUP_INDEX[GroupIndexKey]['FUNCTIONS'][FunctionName]['FLAG'] = False
          Value = Value + 1
          setValueToGroupIndex(GroupIndexKey,FunctionName,Value)
    return Value

def groupSUM():
    pass

def grouoMUL():
    pass

def groupAVG(): # TODO REMAKE
    pass

def groupMIN():
    pass

def groupMAX():
    pass

def groupSSQ(): # TODO REMAKE
    pass


# new evaluateExpression function,
#  accounting for groups
def evaluateExpression(root,VarDictionary,GroupIndexKey=None):
    # input = local tree root
    # XXX: this could be very slow due to passing
    #      every time VarDictionary as a parameter
    # Two special cases: 1) root=varname
    #                    2) root=list/tuple
    # These cases must be processed in a separate way
    if type(root) in set([list,tuple]):
       # root is not a leaf
       head = root[0].upper()
       # string constants are treated specially
       if head in set(['STR','STRING']): # one arg
          return operationSTR(root[1])
       elif head in set(['SET']):
          return operationSET(root[1])
       tail = root[1:]
       args = []
       # evaluate arguments recursively
       for element in tail: # resolve tree by recursion
           args.append(evaluateExpression(element,VarDictionary,GroupIndexKey))
       # call functions with evaluated arguments
       if head in set(['LIST']): # list arg
          return operationLIST(args)
       elif head in set(['&','&&','AND']): # many args 
          return operationAND(args)
       elif head in set(['|','||','OR']): # many args
          return operationOR(args)
       elif head in set(['!','NOT']): # one args
          return operationNOT(args[0])
       elif head in set(['RANGE','BETWEEN']): # three args
          return operationRANGE(args[0],args[1],args[2])
       elif head in set(['IN','SUBSET']): # two args
          return operationSUBSET(args[0],args[1])
       elif head in set(['<','LESS','LT']): # many args
          return operationLESS(args)
       elif head in set(['>','MORE','MT']): # many args
          return operationMORE(args)
       elif head in set(['<=','LESSOREQUAL','LTE']): # many args
          return operationLESSOREQUAL(args)
       elif head in set(['>=','MOREOREQUAL','MTE']): # many args
          return operationMOREOREQUAL(args)
       elif head in set(['=','==','EQ','EQUAL','EQUALS']): # many args
          return operationEQUAL(args)
       elif head in set(['!=','<>','~=','NE','NOTEQUAL']): # two args
          return operationNOTEQUAL(args[0],args[1])
       elif head in set(['+','SUM']): # many args
          return operationSUM(args)
       elif head in set(['-','DIFF']): # two args
          return operationDIFF(args[0],args[1])
       elif head in set(['*','MUL']): # many args
          return operationMUL(args)
       elif head in set(['/','DIV']): # two args
          return operationDIV(args[0],args[1])
       elif head in set(['MATCH','LIKE']): # two args
          return operationMATCH(args[0],args[1])
       elif head in set(['SEARCH']): # two args
          return operationSEARCH(args[0],args[1])
       elif head in set(['FINDALL']): # two args
          return operationFINDALL(args[0],args[1])
       # --- GROUPING OPERATOINS ---
       elif head in set(['COUNT']):
          return groupCOUNT(GroupIndexKey)
       else:
          raise Exception('Unknown operator: %s' % root[0])
    elif type(root)==str:
       # root is a par_name
       return VarDictionary[root]
    else: 
       # root is a non-string constant
       return root

def getVarDictionary(RowObject):
    # get VarDict from RowObject
    # VarDict: par_name => par_value
    VarDictionary = {}
    for par_name,par_value,par_format in RowObject:
        VarDictionary[par_name] = par_value
    return VarDictionary

def checkRowObject(RowObject,Conditions,VarDictionary):
    #VarDictionary = getVarDictionary(RowObject)   
    if Conditions:
       Flag = evaluateExpression(Conditions,VarDictionary)
    else:
       Flag=True
    return Flag

# ----------------------------------------------------
# /CONDITIONS
# ----------------------------------------------------


# ----------------------------------------------------
# PARAMETER NAMES (includeing creation of new ones)
# ----------------------------------------------------

# Bind an expression to a new parameter
#   in a form: ('BIND','new_par',('some_exp',...))
def operationBIND(parname,Expression,VarDictionary): # DISCARD?
    pass

# This section is for more detail processing of 
#   parlists. 

# Table creation must include not only subsets of 
#   existing parameters, but also new parameters
#   derived from functions on a special prefix language
# For this reason subsetOfRowObject(..) must be substituted
#   by newRowObject(ParameterNames,RowObject)

# For parsing use the function evaluateExpression

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# Get names from expression.
#  Must merge this one with evaluateExrpression.
# This is VERY LIMITED version of what will be 
#  when i'll make a language parser.
# For more ideas and info see LANGUAGE_REFERENCE

# more advansed version of expression evaluator
def evaluateExpressionPAR(ParameterNames,VarDictionary=None): # XXX DISCARD
    # RETURN: 1) Upper-level Expression names
    #         2) Upper-level Expression values
    # Is it reasonable to pass a Context to every parse function?
    # For now the function does the following:
    #   1) iterates through all UPPER-LEVEL list elements
    #   2) if element is a parname: return parname
    #      if element is an BIND expression: return bind name
    #              (see operationBIND)
    #   3) if element is an anonymous expression: return #N(=1,2,3...)
    # N.B. Binds can be only on the 0-th level of Expression    
    pass

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# GET FORMATS FROM SUB-EXPRESSION
# Could be very unstable error prone because the
#  format is COLUMN-FIXED!!!
# Should think about it some more.

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# Important function of the STORAGE LEVEL (column-fixed tables)
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

def getContextFormat(RowObject):
    # Get context format from the whole RowObject
    ContextFormat = {}
    for par_name,par_value,par_format in RowObject:
        ContextFormat[par_name] = par_format
    return ContextFormat

def getDefaultFormat(Type):
    if Type is int:
       return '%10d'
    elif Type is float:
       return '%25.15E'
    elif Type is str:
       return '%20s'
    elif Type is bool:
       return '%2d'
    else:
       raise Exception('Unknown type')
     
def getDefaultValue(Type):
    if Type is int:
       return 0
    elif Type is float:
       return 0.0
    elif Type is str:
       return ''
    elif Type is bool:
       return False
    else:
       raise Exception('Unknown type')

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# VarDictionary = Context (this name is more suitable)
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# GroupINdexKey is a key to special structure/dictionary GROUP_INDEX.
# GROUP_INDEX contains information needed to calculate streamed group functions
#  such as COUNT, AVG, MIN, MAX etc...

# TODO: remove RowObject from parameters
def newRowObject(ParameterNames,RowObject,VarDictionary,ContextFormat,GroupIndexKey=None):
    # Return a subset of RowObject according to 
    # ParameterNames include either parnames
    #  or expressions containing parnames literals
    # ContextFormat contains format for ParNames
    anoncount = 0
    RowObjectNew = []
    for expr in ParameterNames:
        if type(expr) in set([list,tuple]): # bind
           head = expr[0]
           if head in set(['let','bind','LET','BIND']):
              par_name = expr[1]
              par_expr = expr[2]
           else:
              par_name = "#%d" % anoncount
              anoncount += 1
              par_expr = expr
           par_value = evaluateExpression(par_expr,VarDictionary,GroupIndexKey)
           try:
              par_format = expr[3]
           except:
              par_format = getDefaultFormat(type(par_value))
        else: # parname
           par_name = expr
           par_value = VarDictionary[par_name]
           par_format = ContextFormat[par_name]
        RowObjectNew.append((par_name,par_value,par_format))
    return RowObjectNew

# ----------------------------------------------------
# /PARAMETER NAMES
# ----------------------------------------------------


# ----------------------------------------------------
# OPERATIONS ON TABLES
# ----------------------------------------------------



def getTableList():
    return LOCAL_TABLE_CACHE.keys()

def describeTable(TableName):
    """
    INPUT PARAMETERS: 
        TableName: name of the table to describe
    OUTPUT PARAMETERS: 
        none
    ---
    DESCRIPTION:
        Print information about table, including 
        parameter names, formats and wavenumber range.
    ---
    EXAMPLE OF USAGE:
        describeTable('sampletab')
    ---
    """
    print('-----------------------------------------')
    print TableName+' summary:'
    try:
       print('-----------------------------------------')
       print 'Comment: \n'+LOCAL_TABLE_CACHE[TableName]['header']['comment']
    except:
       pass
    print 'Number of rows: '+str(LOCAL_TABLE_CACHE[TableName]['header']['number_of_rows'])
    print 'Table type: '+str(LOCAL_TABLE_CACHE[TableName]['header']['table_type'])
    print('-----------------------------------------')
    print('            PAR_NAME           PAR_FORMAT')
    print('')
    for par_name in LOCAL_TABLE_CACHE[TableName]['header']['order']:
        par_format = LOCAL_TABLE_CACHE[TableName]['header']['format'][par_name]
        print '%20s %20s' % (par_name,par_format)
    print('-----------------------------------------')

# Write a table to File or STDOUT
def outputTable(TableName,Conditions=None,File=None,Header=True):
    # Display or record table with condition checking
    if File:
       Header = False
       OutputFile = open(File,'w')
    if Header:
       headstr = putTableHeaderToString(TableName)
       if File:
          OutputFile.write(headstr)
       else:
          print headstr
    for RowID in range(0,LOCAL_TABLE_CACHE[TableName]['header']['number_of_rows']):
        RowObject = getRowObject(RowID,TableName)
        VarDictionary = getVarDictionary(RowObject)
        VarDictionary['LineNumber'] = RowID
        if not checkRowObject(RowObject,Conditions,VarDictionary):
           continue
        raw_string = putRowObjectToString(RowObject)
        if File:
           OutputFile.write(raw_string+'\n')
        else:
           print raw_string

# Create table "prototype-based" way
def createTable(TableName,RowObjectDefault):
    # create a Table based on a RowObjectDefault
    LOCAL_TABLE_CACHE[TableName] = {}
    header_order = []
    header_format = {}
    header_default = {}
    data = {}
    for par_name,par_value,par_format in RowObjectDefault:
        header_order.append(par_name)
        header_format[par_name] = par_format
        header_default[par_name] = par_value
        data[par_name] = []
    #header_order = tuple(header_order) # XXX ?
    LOCAL_TABLE_CACHE[TableName]['header']={}
    LOCAL_TABLE_CACHE[TableName]['header']['order'] = header_order 
    LOCAL_TABLE_CACHE[TableName]['header']['format'] = header_format
    LOCAL_TABLE_CACHE[TableName]['header']['default'] = header_default
    LOCAL_TABLE_CACHE[TableName]['header']['number_of_rows'] = 0
    LOCAL_TABLE_CACHE[TableName]['header']['size_in_bytes'] = 0
    LOCAL_TABLE_CACHE[TableName]['header']['table_name'] = TableName
    LOCAL_TABLE_CACHE[TableName]['header']['table_type'] = 'column-fixed'
    LOCAL_TABLE_CACHE[TableName]['data'] = data
    

# simple "drop table" capability
def dropTable(TableName):
    """
    INPUT PARAMETERS: 
        TableName:  name of the table to delete
    OUTPUT PARAMETERS: 
        none
    ---
    DESCRIPTION:
        Deletes a table from local database.
    ---
    EXAMPLE OF USAGE:
        dropTable('some_dummy_table')
    ---
    """
    # delete Table from both Cache and Storage
    try:
       LOCAL_TABLE_CACHE[TableName] = {}
    except:
       pass
    # delete from storage
    pass # TODO

# Returns a column corresponding to parameter name
def getColumn(TableName,ParameterName):
    """
    INPUT PARAMETERS: 
        TableName:      source table name     (required)
        ParameterName:  name of column to get (required)
    OUTPUT PARAMETERS: 
        ColumnData:     list of values from specified column 
    ---
    DESCRIPTION:
        Returns a column with a name ParameterName from
        table TableName. Column is returned as a list of values.
    ---
    EXAMPLE OF USAGE:
        p1 = getColumn('sampletab','p1')
    ---
    """
    return LOCAL_TABLE_CACHE[TableName]['data'][ParameterName]

# Returns a list of columns corresponding to parameter names
def getColumns(TableName,ParameterNames):
    """
    INPUT PARAMETERS: 
        TableName:       source table name           (required)
        ParameterNames:  list of column names to get (required)
    OUTPUT PARAMETERS: 
        ListColumnData:   tuple of lists of values from specified column 
    ---
    DESCRIPTION:
        Returns columns with a names in ParameterNames from
        table TableName. Columns are returned as a tuple of lists.
    ---
    EXAMPLE OF USAGE:
        p1,p2,p3 = getColumns('sampletab',('p1','p2','p3'))
    ---
    """
    Columns = []
    for par_name in ParameterNames:
        Columns.append(LOCAL_TABLE_CACHE[TableName]['data'][par_name])
    return Columns

def addColumn(TableName,ParameterName,Before=None,Expression=None,Type=None,Default=None,Format=None):
    if ParameterName in LOCAL_TABLE_CACHE[TableName]['header']['format']:
       raise Exception('Column \"%s\" already exists' % ParameterName)
    if not Type: Type = float
    if not Default: Default = getDefaultValue(Type)
    if not Format: Format = getDefaultFormat(Type)
    number_of_rows = LOCAL_TABLE_CACHE[TableName]['header']['number_of_rows']
    # Mess with data
    if not Expression:
       LOCAL_TABLE_CACHE[TableName]['data'][ParameterName]=[Default for i in range(0,number_of_rows)]
    else:
       data = []
       for RowID in range(0,number_of_rows):
           RowObject = getRowObject(RowID,TableName)
           VarDictionary = getVarDictionary(RowObject)
           VarDictionary['LineNumber'] = RowID
           par_value = evaluateExpression(Expression,VarDictionary)
           data.append(par_value)
           LOCAL_TABLE_CACHE[TableName]['data'][ParameterName] = data
    # Mess with header
    header_order = LOCAL_TABLE_CACHE[TableName]['header']['order']
    if not Before: 
       header_order.append(ParameterName)
    else:
       #i = 0
       #for par_name in header_order:
       #    if par_name == Before: break
       #    i += 1
       i = header_order.index(Before)
       header_order = header_order[:i] + [ParameterName,] + header_order[i:]
    LOCAL_TABLE_CACHE[TableName]['header']['order'] = header_order
    LOCAL_TABLE_CACHE[TableName]['header']['format'][ParameterName] = Format
    LOCAL_TABLE_CACHE[TableName]['header']['default'][ParameterName] = Default
   

def deleteColumn(TableName,ParameterName):
    if ParameterName not in LOCAL_TABLE_CACHE[TableName]['header']['format']:
       raise Exception('No such column \"%s\"' % ParameterName)
    # Mess with data
    i = LOCAL_TABLE_CACHE[TableName]['header']['order'].index(ParameterName)
    del LOCAL_TABLE_CACHE[TableName]['header']['order'][i]
    del LOCAL_TABLE_CACHE[TableName]['header']['format'][ParameterName]
    del LOCAL_TABLE_CACHE[TableName]['header']['default'][ParameterName]
    if not LOCAL_TABLE_CACHE[TableName]['header']['order']:
       LOCAL_TABLE_CACHE[TableName]['header']['number_of_rows'] = 0
    # Mess with header
    del LOCAL_TABLE_CACHE[TableName]['data'][ParameterName]

def deleteColumns(TableName,ParameterNames):
    if type(ParameterNames) not in set([list,tuple,set]):
       ParameterNames = [ParameterNames]
    for ParameterName in ParameterNames:
        deleteColumn(TableName,ParameterName)

def renameColumn(TableName,OldParameterName,NewParameterName):
    pass

def insertRow():
    pass

def deleteRows(TableName,ParameterNames,Conditions):
    pass

# select from table to another table
#def selectInto(DestinationTableName,TableName,ParameterNames,Conditions):
#    # TableName must refer to an existing table in cache!!
#    # Conditions = Restrictables in specific format
#    # Sample conditions: cond = {'par1':{'range',[b_lo,b_hi]},'par2':b}
#    # return structure similar to TableObject and put it to QUERY_BUFFER
#    # if ParameterNames is '*' then all parameters are used
#    #table_columns = LOCAL_TABLE_CACHE[TableName]['data'].keys()
#    #table_length = len(TableObject['header']['number_of_rows'])
#    #if ParameterNames=='*':
#    #   ParameterNames = table_columns
#    # check if Conditions contain elements which are not in the TableObject
#    #condition_variables = getConditionVariables(Conditions)
#    #strange_pars = set(condition_variables)-set(table_variables)
#    #if strange_pars: 
#    #   raise Exception('The following parameters are not in the table \"%s\"' % (TableName,list(strange_pars)))
#    # do full scan each time
#    if DestinationTableName == TableName:
#       raise Exception('Selecting into source table is forbidden')
#    table_length = LOCAL_TABLE_CACHE[TableName]['header']['number_of_rows']
#    row_count = 0
#    for RowID in range(0,table_length):
#        RowObject = getRowObject(RowID,TableName)
#        RowObjectNew = subsetOfRowObject(ParameterNames,RowObject)
#        VarDictionary = getVarDictionary(RowObject)
#        if checkRowObject(RowObject,Conditions,VarDictionary):
#           addRowObject(RowObjectNew,DestinationTableName)
#           row_count += 1
#    LOCAL_TABLE_CACHE[DestinationTableName]['header']['number_of_rows'] += row_count

# select from table to another table
def selectInto(DestinationTableName,TableName,ParameterNames,Conditions):
    # TableName must refer to an existing table in cache!!
    # Conditions = Restrictables in specific format
    # Sample conditions: cond = {'par1':{'range',[b_lo,b_hi]},'par2':b}
    # return structure similar to TableObject and put it to QUERY_BUFFER
    # if ParameterNames is '*' then all parameters are used
    #table_columns = LOCAL_TABLE_CACHE[TableName]['data'].keys()
    #table_length = len(TableObject['header']['number_of_rows'])
    #if ParameterNames=='*':
    #   ParameterNames = table_columns
    # check if Conditions contain elements which are not in the TableObject
    #condition_variables = getConditionVariables(Conditions)
    #strange_pars = set(condition_variables)-set(table_variables)
    #if strange_pars: 
    #   raise Exception('The following parameters are not in the table \"%s\"' % (TableName,list(strange_pars)))
    # do full scan each time
    if DestinationTableName == TableName:
       raise Exception('Selecting into source table is forbidden')
    table_length = LOCAL_TABLE_CACHE[TableName]['header']['number_of_rows']
    row_count = 0
    for RowID in range(0,table_length):
        RowObject = getRowObject(RowID,TableName)
        VarDictionary = getVarDictionary(RowObject)
        VarDictionary['LineNumber'] = RowID
        ContextFormat = getContextFormat(RowObject)
        RowObjectNew = newRowObject(ParameterNames,RowObject,VarDictionary,ContextFormat)
        if checkRowObject(RowObject,Conditions,VarDictionary):
           addRowObject(RowObjectNew,DestinationTableName)
           row_count += 1
    LOCAL_TABLE_CACHE[DestinationTableName]['header']['number_of_rows'] += row_count

def length(TableName):
    tab_len = LOCAL_TABLE_CACHE[TableName]['header']['number_of_rows']
    #print(str(tab_len)+' rows in '+TableName)
    return tab_len

# select from table to QUERY_BUFFER
#def select(TableName,DestinationTableName=QUERY_BUFFER,ParameterNames=None,Conditions=None,Output=True,File=None):
#    if not ParameterNames: ParameterNames=LOCAL_TABLE_CACHE[TableName]['header']['order']
#    LOCAL_TABLE_CACHE[DestinationTableName] = {} # clear QUERY_BUFFER for the new result
#    RowObjectDefault = getDefaultRowObject(TableName)
#    RowObjectDefaultNew = subsetOfRowObject(ParameterNames,RowObjectDefault)
#    dropTable(DestinationTableName) # redundant
#    createTable(DestinationTableName,RowObjectDefaultNew)
#    selectInto(DestinationTableName,TableName,ParameterNames,Conditions)
#    if Output and DestinationTableName==QUERY_BUFFER:
#		outputTable(DestinationTableName,File=File)

# Select parameters from a table with certain conditions.
# Parameters can be the names or expressions.
# Conditions contain a list of expressions in a special language.
# Set Output to False to suppress output
# Set File=FileName to redirect output to a file.
def select(TableName,DestinationTableName=QUERY_BUFFER,ParameterNames=None,Conditions=None,Output=True,File=None):
    """
    INPUT PARAMETERS: 
        TableName:            name of source table              (required)
        DestinationTableName: name of resulting table           (optional)
        ParameterNames:       list of parameters or expressions (optional)
        Conditions:           list of logincal expressions      (optional)
        Output:   enable (True) or suppress (False) text output (optional)
        File:     enable (True) or suppress (False) file output (optional)
    OUTPUT PARAMETERS: 
        none
    ---
    DESCRIPTION:
        Select or filter the data in some table 
        either to standard output or to file (if specified)
    ---
    EXAMPLE OF USAGE:
        select('sampletab',DestinationTableName='outtab',ParameterNames=(p1,p2),
                Conditions=(('and',('>=','p1',1),('<',('*','p1','p2'),20))))
        Conditions means (p1>=1 and p1*p2<20)
    ---
    """
    # TODO: Variables defined in ParameterNames ('LET') MUST BE VISIBLE IN Conditions !!
    # check if table exists
    if TableName not in LOCAL_TABLE_CACHE.keys():
        raise Exception('%s: no such table. Check tableList() for more info.' % TableName)
    if not ParameterNames: ParameterNames=LOCAL_TABLE_CACHE[TableName]['header']['order']
    LOCAL_TABLE_CACHE[DestinationTableName] = {} # clear QUERY_BUFFER for the new result
    RowObjectDefault = getDefaultRowObject(TableName)
    VarDictionary = getVarDictionary(RowObjectDefault)
    ContextFormat = getContextFormat(RowObjectDefault)
    RowObjectDefaultNew = newRowObject(ParameterNames,RowObjectDefault,VarDictionary,ContextFormat)
    dropTable(DestinationTableName) # redundant
    createTable(DestinationTableName,RowObjectDefaultNew)
    selectInto(DestinationTableName,TableName,ParameterNames,Conditions)
    if Output and DestinationTableName==QUERY_BUFFER:
       outputTable(DestinationTableName,File=File)

# SORTING ===========================================================

def arrangeTable(TableName,DestinationTableName=None,RowIDList=None):
    #print 'AT/'
    #print 'AT: RowIDList = '+str(RowIDList)
    # make a subset of table rows according to RowIDList
    if not DestinationTableName:
       DestinationTablename = TableName
    if DestinationTableName != TableName:
       dropTable(DestinationTableName)
       LOCAL_TABLE_CACHE[DestinationTableName]['header']=LOCAL_TABLE_CACHE[TableName]['header']
       LOCAL_TABLE_CACHE[DestinationTableName]['data']={}
    LOCAL_TABLE_CACHE[DestinationTableName]['header']['number_of_rows'] = len(RowIDList)
    #print 'AT: RowIDList = '+str(RowIDList)
    for par_name in LOCAL_TABLE_CACHE[DestinationTableName]['header']['order']:
        par_data = LOCAL_TABLE_CACHE[TableName]['data'][par_name]
        LOCAL_TABLE_CACHE[DestinationTableName]['data'][par_name] = [par_data[i] for i in RowIDList]
    
def compareLESS(RowObject1,RowObject2,ParameterNames):
    #print 'CL/'
    # arg1 and arg2 are RowObjects
    # Compare them according to ParameterNames
    # Simple validity check:
    #if len(arg1) != len(arg2):
    #   raise Exception('Arguments have different lengths')
    #RowObject1Subset = subsetOfRowObject(ParameterNames,RowObject1)
    #RowObject2Subset = subsetOfRowObject(ParameterNames,RowObject2)
    #return RowObject1Subset < RowObject2Subset
    row1 = []
    row2 = []
    #n = len(RowObject1)
    #for i in range(0,n):
    #    par_name1 = RowObject1[i][0]
    #    if par_name1 in ParameterNames:
    #       par_value1 = RowObject1[i][1]
    #       par_value2 = RowObject2[i][1]
    #       row1 += [par_value1]
    #       row2 += [par_value2]
    VarDictionary1 = getVarDictionary(RowObject1)
    VarDictionary2 = getVarDictionary(RowObject2)
    for par_name in ParameterNames:
        par_value1 = VarDictionary1[par_name]
        par_value2 = VarDictionary2[par_name]
        row1 += [par_value1]
        row2 += [par_value2]
    Flag = row1 < row2
    #print 'CL: row1 = '+str(row1)
    #print 'CL: row2 = '+str(row2)
    #print 'CL: Flag = '+str(Flag)
    return Flag

def quickSort(index,TableName,ParameterNames,Accending=True):
    #print ''
    #print 'QS/'
    #print 'QS: index = '+str(index)
    #print index
    # ParameterNames: names of parameters which are
    #  taking part in the sorting
    if index == []:
       return []
    else:
       #pivot = lst[0]
       #lesser = quickSort([x for x in lst[1:] if x < pivot])
       #greater = quickSort([x for x in lst[1:] if x >= pivot])
       PivotID = index[0]
       Pivot = getRowObject(PivotID,TableName)
       lesser_index = []
       greater_index = [];
       for RowID in index[1:]:
           RowObject = getRowObject(RowID,TableName)           
           if compareLESS(RowObject,Pivot,ParameterNames): 
              lesser_index += [RowID]
           else:
              greater_index += [RowID]
       #print 'QS: lesser_index = '+str(lesser_index)
       #print 'QS: greater_index = '+str(greater_index)
       lesser = quickSort(lesser_index,TableName,ParameterNames,Accending)
       greater = quickSort(greater_index,TableName,ParameterNames,Accending)
       #return lesser + [pivot_index] + greater
       if Accending:
          return lesser + [PivotID] + greater
       else:
          return greater + [PivotID] + lesser

# Sorting must work well on the table itself!
def sort(TableName,DestinationTableName=None,ParameterNames=None,Accending=True,Output=False,File=None):
    """
    INPUT PARAMETERS: 
        TableName:                name of source table          (required)
        DestinationTableName:     name of resulting table       (optional)
        ParameterNames:       list of parameters or expressions to sort by    (optional)
        Accending:       sort in ascending (True) or descending (False) order (optional)
        Output:   enable (True) or suppress (False) text output (optional)
        File:     enable (True) or suppress (False) file output (optional)
    OUTPUT PARAMETERS: 
        none
    ---
    DESCRIPTION:
        Sort a table by a list of it's parameters or expressions.
        The sorted table is saved in DestinationTableName (if specified).
    ---
    EXAMPLE OF USAGE:
        sort('sampletab',ParameterNames=(p1,('+',p1,p2)))
    ---
    """
    number_of_rows = LOCAL_TABLE_CACHE[TableName]['header']['number_of_rows']
    index = range(0,number_of_rows)
    #print 'num = '+str(number_of_rows)
    if not DestinationTableName:
       DestinationTableName = TableName
    # if names are not provided use all parameters in sorting
    if not ParameterNames:
       ParameterNames = LOCAL_TABLE_CACHE[TableName]['header']['order']
    elif type(ParameterNames) not in set([list,tuple]):
       ParameterNames = [ParameterNames] # fix of stupid bug where ('p1',) != ('p1')
    #print 'SRT: ParameterNames = '+str(ParameterNames)
    #print 'parnames: '+str(ParameterNames)
    index_sorted = quickSort(index,TableName,ParameterNames,Accending)
    arrangeTable(TableName,DestinationTableName,index_sorted)
    if Output:
       outputTable(DestinationTableName,File=File)

# /SORTING ==========================================================
    

# GROUPING ==========================================================

# GROUP_INDEX global auxillary structure is a Dictionary,
#   which has the following properties:
#      1) Each key is a composite variable:
#          [array of values of ParameterNames variable
#           STREAM_UPDATE_FLAG]
#      2) Each value is an index in LOCAL_TABLE_CACHE[TableName]['data'][...],
#          corresponding to this key
#   STREAM_UPDATE_FLAG = TRUE if value in GROUP_INDEX needs updating
#                      = FALSE otherwise
#   If no grouping variables are specified (GroupParameterNames==None)
#    than the following key is used: "__GLOBAL__"




#def select(TableName,DestinationTableName=QUERY_BUFFER,ParameterNames=None,Conditions=None,Output=True,File=None):
#   # TODO: Variables defined in ParameterNames ('LET') MUST BE VISIBLE IN Conditions !!
#   if not ParameterNames: ParameterNames=LOCAL_TABLE_CACHE[TableName]['header']['order']
#   LOCAL_TABLE_CACHE[DestinationTableName] = {} # clear QUERY_BUFFER for the new result
#   RowObjectDefault = getDefaultRowObject(TableName)
#   VarDictionary = getVarDictionary(RowObjectDefault)
#   ContextFormat = getContextFormat(RowObjectDefault)
#   RowObjectDefaultNew = newRowObject(ParameterNames,RowObjectDefault,VarDictionary,ContextFormat)
#   dropTable(DestinationTableName) # redundant
#   createTable(DestinationTableName,RowObjectDefaultNew)
#   selectInto(DestinationTableName,TableName,ParameterNames,Conditions)
#   if Output and DestinationTableName==QUERY_BUFFER:
#      outputTable(DestinationTableName,File=File)


#def selectInto(DestinationTableName,TableName,ParameterNames,Conditions):
#   # do full scan each time
#   if DestinationTableName == TableName:
#      raise Exception('Selecting into source table is forbidden')
#   table_length = LOCAL_TABLE_CACHE[TableName]['header']['number_of_rows']
#   row_count = 0
#   for RowID in range(0,table_length):
#       RowObject = getRowObject(RowID,TableName)
#       VarDictionary = getVarDictionary(RowObject)
#       VarDictionary['_ID_'] = RowID
#       ContextFormat = getContextFormat(RowObject)
#       RowObjectNew = newRowObject(ParameterNames,RowObject,VarDictionary,ContextFormat)
#       if checkRowObject(RowObject,Conditions,VarDictionary):
#          addRowObject(RowObjectNew,DestinationTableName)
#          row_count += 1
#   LOCAL_TABLE_CACHE[DestinationTableName]['header']['number_of_rows'] += row_count


#def newRowObject(ParameterNames,RowObject,VarDictionary,ContextFormat):
#   anoncount = 0
#   RowObjectNew = []
#   for expr in ParameterNames:
#       if type(expr) in {list,tuple}: # bind
#          head = expr[0]
#          if head in {'BIND','LET'}:
#             par_name = expr[1]
#             par_expr = expr[2]
#          else:
#             par_name = "#%d" % anoncount
#             anoncount += 1
#             par_expr = expr
#          par_value = evaluateExpression(par_expr,VarDictionary)
#          try:
#             par_format = expr[3]
#          except:
#             par_format = getDefaultFormat(type(par_value))
#       else: # parname
#          par_name = expr
#          par_value = VarDictionary[par_name]
#          par_format = ContextFormat[par_name]
#       RowObjectNew.append((par_name,par_value,par_format))
#   return RowObjectNew

def group(TableName,DestinationTableName=QUERY_BUFFER,ParameterNames=None,GroupParameterNames=None,Output=True):
    """
    INPUT PARAMETERS: 
        TableName:                name of source table          (required)
        DestinationTableName:     name of resulting table       (optional)
        ParameterNames:       list of parameters or expressions to take       (optional)
        GroupParameterNames:  list of parameters or expressions to group by   (optional)
        Accending:       sort in ascending (True) or descending (False) order (optional)
        Output:   enable (True) or suppress (False) text output (optional)
    OUTPUT PARAMETERS: 
        none
    ---
    DESCRIPTION:
        none
    ---
    EXAMPLE OF USAGE:
        group('sampletab',ParameterNames=('p1',('sum','p2')),GroupParameterNames=('p1'))
        ... makes grouping by p1,p2. For each group it calculates sum of p2 values.
    ---
    """
    # Implements such functions as:
    # count,sum,avg,min,max,ssq etc...
    # 1) ParameterNames can contain group functions
    # 2) GroupParameterNames can't contain group functions
    # 3) If ParameterNames contains parameters defined by LET directive,
    #    it IS visible in the sub-context of GroupParameterNames
    # 4) Parameters defined in GroupParameterNames are NOT visible in ParameterNames
    # 5) ParameterNames variable represents the structure of the resulting table/collection
    # 6) GroupParameterNames can contain either par_names or expressions with par_names
    # Clear old GROUP_INDEX value
    clearGroupIndex()
    # Consistency check
    if TableName == DestinationTableName:
       raise Exception('TableName and DestinationTableName must be different')
    #if not ParameterNames: ParameterNames=LOCAL_TABLE_CACHE[TableName]['header']['order']
    # Prepare the new DestinationTable
    RowObjectDefault = getDefaultRowObject(TableName)
    VarDictionary = getVarDictionary(RowObjectDefault)
    ContextFormat = getContextFormat(RowObjectDefault)
    RowObjectDefaultNew = newRowObject(ParameterNames,RowObjectDefault,VarDictionary,ContextFormat)
    dropTable(DestinationTableName) # redundant
    createTable(DestinationTableName,RowObjectDefaultNew)
    # Loop through rows of source Table
    # On each iteration group functions update GROUP_INDEX (see description above)
    number_of_rows = LOCAL_TABLE_CACHE[TableName]['header']['number_of_rows']   
    # STAGE 1: CREATE GROUPS
    print 'LOOP:'
    for RowID in range(0,number_of_rows):
        print '--------------------------------'
        print 'RowID='+str(RowID)
        RowObject = getRowObject(RowID,TableName) # RowObject from source table
        VarDictionary = getVarDictionary(RowObject)
        print 'VarDictionary='+str(VarDictionary)
        # This is a trick which makes evaluateExpression function
        #   not consider first expression as an operation
        GroupParameterNames_ = ['LIST'] + list(GroupParameterNames)
        GroupIndexKey = evaluateExpression(GroupParameterNames_,VarDictionary)
        # List is an unhashable type in Python!
        GroupIndexKey = tuple(GroupIndexKey)       
        initializeGroup(GroupIndexKey)
        print 'GROUP_INDEX='+str(GROUP_INDEX)
        ContextFormat = getContextFormat(RowObject)
        RowObjectNew = newRowObject(ParameterNames,RowObject,VarDictionary,ContextFormat,GroupIndexKey)
        RowIDGroup = GROUP_INDEX[GroupIndexKey]['ROWID']
        setRowObject(RowIDGroup,RowObjectNew,DestinationTableName)
    # Output result if required
    if Output and DestinationTableName==QUERY_BUFFER:
       outputTable(DestinationTableName,File=File)

# /GROUPING =========================================================

REGEX_INTEGER_FIXCOL = lambda n: '\d{%d}' % n
REGEX_STRING_FIXCOL = lambda n: '[^\s]{%d}' % n
REGEX_FLOAT_F_FIXCOL = lambda n: '[\+\-\.\d]{%d}' % n
REGEX_FLOAT_E_FIXCOL = lambda n: '[\+\-\.\deEfF]{%d}' % n

# EXTRACTING ========================================================
# Extract sub-columns from string column
def extractColumns(TableName,SourceParameterName,ParameterFormats,ParameterNames=None,FixCol=False):
    """
    INPUT PARAMETERS: 
        TableName:             name of source table              (required)
        SourceParameterName:   name of source column to process  (required)
        ParameterFormats:      c formats of unpacked parameters  (required)
        ParameterNames:        list of resulting parameter names (optional)
        FixCol:      column-fixed (True) format of source column (optional)
    OUTPUT PARAMETERS: 
        none
    ---
    DESCRIPTION:
        Note, that this function is aimed to do some extra job on
        interpreting string parameters which is normally supposed
        to be done by the user.
    ---
    EXAMPLE OF USAGE:
        extractColumns('sampletab',SourceParameterName='p5',
                        ParameterFormats=('%d','%d','%d'),
                        ParameterNames=('p5_1','p5_2','p5_3'))
        This example extracts three integer parameters from
        a source column 'p5' and puts results in ('p5_1','p5_2','p5_3').
    ---
    """
    # ParameterNames = just the names without expressions
    # ParFormats contains python formats for par extraction
    # Example: ParameterNames=('v1','v2','v3')
    #          ParameterFormats=('%1s','%1s','%1s')
    # By default the format of parameters is column-fixed
    if type(LOCAL_TABLE_CACHE[TableName]['header']['default'][SourceParameterName]) not in set([str,unicode]):
       raise Exception('Source parameter must be a string')
    i=-1
    # bug when (a,) != (a)
    if ParameterNames and type(ParameterNames) not in set([list,tuple]):
       ParameterNames = [ParameterNames]
    if ParameterFormats and type(ParameterFormats) not in set([list,tuple]):
       ParameterFormats = [ParameterFormats]
    # if ParameterNames is empty, fill it with #1-2-3-...
    if not ParameterNames:
       ParameterNames = []
       # using naming convension #i, i=0,1,2,3...
       for par_format in ParameterFormats:
           while True:
                 i+=1
                 par_name = '#%d' % i
                 fmt = LOCAL_TABLE_CACHE[TableName]['header']['format'].get(par_name,None)
                 if not fmt: break
           ParameterNames.append(par_name)
    # check if ParameterNames are valid
    Intersection = set(ParameterNames).intersection(LOCAL_TABLE_CACHE[TableName]['header']['order'])
    if Intersection:
       raise Exception('Parameters %s already exist' % str(list(Intersection)))
    # loop over ParameterNames to prepare LOCAL_TABLE_CACHE
    i=0
    for par_name in ParameterNames:  
        par_format = ParameterFormats[i]     
        LOCAL_TABLE_CACHE[TableName]['header']['format'][par_name]=par_format
        LOCAL_TABLE_CACHE[TableName]['data'][par_name]=[] 
        i+=1
    # append new parameters in order list
    LOCAL_TABLE_CACHE[TableName]['header']['order'] += ParameterNames
    # cope with default values
    i=0
    format_regex = []
    format_types = []
    #print 'ParameterNames='+str(ParameterNames)
    for par_format in ParameterFormats:
        par_name = ParameterNames[i]
        regex = FORMAT_PYTHON_REGEX
        #print 'par_name: '+par_name
        #print 'par_format: '+par_format
        (lng,trail,lngpnt,ty) = re.search(regex,par_format).groups()
        ty = ty.lower()
	if ty == 'd':
           par_type = int
           if FixCol:
              format_regex_part = REGEX_INTEGER_FIXCOL(lng)
           else:
              format_regex_part = REGEX_INTEGER
        elif ty == 's':
           par_type = str
           if FixCol:
              format_regex_part = REGEX_STRING_FIXCOL(lng)
           else:
              format_regex_part = REGEX_STRING
        elif ty == 'f':
           par_type = float
           if FixCol:
              format_regex_part = REGEX_FLOAT_F_FIXCOL(lng)
           else:
              format_regex_part = REGEX_FLOAT_F
        elif ty == 'e':
           par_type = float
           if FixCol:
              format_regex_part = REGEX_FLOAT_E_FIXCOL(lng)
           else:
              format_regex_part = REGEX_FLOAT_E
        else:
           raise Exception('Unknown data type')
        format_regex.append('('+format_regex_part+')')
        format_types.append(par_type)
        def_val = getDefaultValue(par_type)
        LOCAL_TABLE_CACHE[TableName]['header']['default'][par_name]=def_val
        i+=1
    format_regex = '\s*'.join(format_regex)
    #print 'format_regex='+str(format_regex)
    #return format_regex
    # loop through values of SourceParameter
    for SourceParameterString in LOCAL_TABLE_CACHE[TableName]['data'][SourceParameterName]:
        try:
           ExtractedValues = list(re.search(format_regex,SourceParameterString).groups())
        except:
           raise Exception('Error with line \"%s\"' % SourceParameterString)
        i=0
        # loop through all parameters which are supposed to be extracted
        for par_name in ParameterNames:
            #print 'ExtractedValues[i]='+ExtractedValues[i]
            #print 'par_name='+par_name
            par_value = format_types[i](ExtractedValues[i])
            LOCAL_TABLE_CACHE[TableName]['data'][par_name].append(par_value)
            i+=1
    # explicitly check that number of rows are equal
    number_of_rows = LOCAL_TABLE_CACHE[TableName]['header']['number_of_rows']
    number_of_rows2 = len(LOCAL_TABLE_CACHE[TableName]['data'][SourceParameterName])
    number_of_rows3 = len(LOCAL_TABLE_CACHE[TableName]['data'][ParameterNames[0]])
    if not (number_of_rows == number_of_rows2 == number_of_rows3):
       raise Exception('Error while extracting parameters: check your regexp')

# Split string columns into sub-columns with given names
def splitColumn(TableName,SourceParameterName,ParameterNames,Splitter):
    pass

# /EXTRACTING =======================================================

# ---------------------------------------------------------------
# ---------------------------------------------------------------
# /LOCAL DATABASE MANAGEMENT SYSTEM
# ---------------------------------------------------------------
# ---------------------------------------------------------------


# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# GLOBAL API FUNCTIONS
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

def queryHITRAN(TableName,iso_id_list,numin,numax):
    #import httplib
    #conn = httplib.HTTPConnection('hitranazure.cloudapp.com')
    #conn.Request('')
    #r = conn.getresponse()
    #print r.status, r.reason
    #data1 = data1.read
    TableHeader = HITRAN_DEFAULT_HEADER
    TableHeader['table_name'] = TableName
    DataFileName = VARIABLES['BACKEND_DATABASE_NAME'] + '/' + TableName + '.data'
    HeaderFileName = VARIABLES['BACKEND_DATABASE_NAME'] + '/' + TableName + '.header'
    #if TableName in LOCAL_TABLE_CACHE.keys():
    #   raise Exception('Table \"%s\" exists' % TableName)
    #if os.path.isfile(DataFileName):
    #   raise Exception('File \"%s\" exists' % DataFileName)
    #if os.path.isfile(HeaderFileName):
    #   raise Exception('!!File \"%s\" exists' % HeaderFileName)
    # create URL
    iso_id_list_str = [str(iso_id) for iso_id in iso_id_list]
    iso_id_list_str = ','.join(iso_id_list_str)
    #url = 'http://hitran.cloudapp.net' + '/lbl/5?' + \
    #url = 'http://hitranazure.cloudapp.net' + '/lbl/5?' + \
    #'iso_ids_list=' + iso_id_list_str + '&' + \
    #'numin=' + str(numin) + '&' + \
    #'numax=' + str(numax) + '&' + \
    #'access=api' + '&' + \
    #'key=' + GLOBAL_HITRAN_APIKEY
    url = GLOBAL_HOST + '/lbl/api?' + \
    'iso_ids_list=' + iso_id_list_str + '&' + \
    'numin=' + str(numin) + '&' + \
    'numax=' + str(numax)
    #print('url=',url)  # DEBUG
    # More efficient way: download by chunks
    try:
        req = urllib2.urlopen(url)
    except HTTPError:
        raise Exception('Failed to retrieve data for given parameters.')
    except URLError:
        raise Exception('Cannot connect to %s. Try again or edit GLOBAL_HOST variable.' % GLOBAL_HOST)
    #CHUNK = 16 * 1024 # default value
    CHUNK = 64 * 1024
    print 'BEGIN DOWNLOAD: '+TableName
    with open(DataFileName,'w') as fp:
       while True:
          chunk = req.read(CHUNK)
          if not chunk: break
          fp.write(chunk)
          print '  %d bytes written to %s' % (CHUNK,DataFileName)
    with open(HeaderFileName,'w') as fp:
       fp.write(json.dumps(TableHeader,indent=2))
       print 'Header written to %s' % HeaderFileName
    print 'END DOWNLOAD'
    # Set comment
    # Get this table to LOCAL_TABLE_CACHE
    storage2cache(TableName)
    print 'PROCESSED'


# Node initialization
def nodeInit(): 
    # very unoptimal, since it loads all tables in memory!!
    #loadCache()
    databaseBegin() # DB backend level, start transaction
    NODE_READY = True

# returns a table instance created from Query object
def globalSelectInto(NewTablePath,SourceTablePath,ParameterNames,Conditions):
    # creates table from parsed data
    # and store it in the database DB
    
    dbname,tablename,nodename = NewTablePath.split('::')
    dbname1,tablename1,nodename1 = SourceTablePath.split('::')

    if not NODE_READY: raise Exception('Node \"%s\" is not ready. Call nodeInit()' % NODE_NAME)

    # should get rid of selectLocal as planning to use network interface
    # ......    selectLocal OR selectRemote

    pass

# ---------------------------------------------------------------

###?def cacheTableLookup(Query,Cache=GlobalCache):
###?    # try to find table in Cache by it's Query
###?    # if fails, return empty instance 
###?    # reasons of failure:
###?    #   - Query is not registered in cache
###?    #   - Query is registered, but Table is too old
###?    return []

###?def cacheTableUpdate()
###?    pass

###?def cacheTable(Query,Cache=GlobalCache,Connection=GlobalConnection):
###?    # returns a table from the Cache by table's Query
###?    # if cashed table is not found fetch it remotely
###?    OldTable = cacheTableLookup(Query,Cache)
###?    if not empty(OldTable)
###?       return OldTable
###?    else:
###?       RawData = getRawDataRemote(Query,Connection)
###?       ParsedData = parseRawData(RawData)
###?       NewTable = createTable(ParsedData)
###?       updateCache(Cache,NewTable)
###?    return NewTable

# query_string - query written in the 
# formal language of local database frontend
def makeQuery(query_string,Connection=GLOBAL_CONNECTION):
    # makes a query to remote server
    # using connection instance
    pass

# ---------- DATABASE FRONTEND END -------------

# ---------- DATABASE BACKEND 1 ----------------

# This is a simple database backend for Python
# which uses standard 



# ---------- DATABASE BACKEND 1 END ------------


# simple implementation of getting a line list from a remote server
def getLinelist(local_name,query,api_key):
    return makeQuery(local_name)

# -------------------------------------------------------------------
# -------------------------------------------------------------------
# / GLOBABL API FUNCTIONS
# -------------------------------------------------------------------
# -------------------------------------------------------------------


# ---------------- FILTER ---------------------------------------------
def filter(TableName,Conditions):
    select(TableName=TableName,Conditions=Conditions,Output=False)


# iso.py
def print_iso():
    print('The dictionary \"ISO\" contains information on isotopologues in HITRAN\n')
    print('   M    I          id                  iso_name   abundance      mass        mol_name')
    for i in ISO:
        ab = ISO[i][ISO_INDEX['abundance']]
        ma = ISO[i][ISO_INDEX['mass']]
        ab = ab if ab else -1
        ma = ma if ma else -1
        print('%4i %4i     : %5i %25s %10f %10f %15s' % (i[0],i[1],ISO[i][ISO_INDEX['id']],ISO[i][ISO_INDEX['iso_name']],ab,ma,ISO[i][ISO_INDEX['mol_name']]))

def print_iso_id():
    print('The dictionary \"ISO_ID\" contains information on \"global\" IDs of isotopologues in HITRAN\n')
    print('   id            M    I                    iso_name       abundance       mass        mol_name')
    for i in ISO_ID:
        ab = ISO_ID[i][ISO_ID_INDEX['abundance']]
        ma = ISO_ID[i][ISO_ID_INDEX['mass']]
        ab = ab if ab else -1
        ma = ma if ma else -1
        print('%5i     :   %4i %4i   %25s %15.10f %10f %15s' % (i,ISO_ID[i][ISO_ID_INDEX['M']],ISO_ID[i][ISO_ID_INDEX['I']],ISO_ID[i][ISO_ID_INDEX['iso_name']],ab,ma,ISO_ID[i][ISO_ID_INDEX['mol_name']]))

def print_profiles():
    print('Profiles available:')
    print('  HT      : PROFILE_HT')
    print('  Voigt   : PROFILE_VOIGT')
    print('  Lorentz : PROFILE_LORENTZ')
    print('  Doppler : PROFILE_DOPPLER')

slit_functions = 'slit_functions'
def print_slit_functions():
    print('  RECTANGULAR : SLIT_RECTANGULAR')
    print('  TRIANGULAR  : SLIT_TRIANGULAR')
    print('  GAUSSIAN    : SLIT_GAUSSIAN')
    print('  DIFFRACTION : SLIT_DIFFRACTION')
    print('  MICHELSON   : SLIT_MICHELSON')
    print('  DISPERSION/LORENTZ : SLIT_DISPERSION')

def getHelp__BAK(arg=None):
    if not arg:
        print('getHelp( ... )')
        print('---------------------')
        print('db_begin')
        print('db_commit')
        print('tableList')
        print('describe')
        print('select')
        print('sort')
        print('group')
        print('extractColumn')
        print('getColumn')
        print('getColumns')
        print('dropTable')
        print('absorptionCoefficient_HT')
        print('absorptionCoefficient_Voigt')
        print('absorptionCoefficient_Lorentz')
        print('absorptionCoefficient_Doppler')
        print('transmittanceSpectrum')
        print('absorptionSpectrum')
        print('radianceSpectrum')
        print('partitionSum')
        print('profiles')
        print('slit_functions')
        print('convolveSpectrum')
        print('ISO_ID')
        print('read_hotw')
        print('getStickXY')
        print('abundance')
        print('molecularMass')
        print('moleculeName')
        print('isotopologueName')      
        return
    if arg == ISO:
        print_iso()
    elif arg == ISO_ID:
        print_iso_id()
    elif arg == profiles:
        print_profiles()
    elif arg == slit_functions:
        print_slit_functions()
    else:
       help(arg)


# Get atmospheric (natural) abundance
# for a specified isotopologue
# M - molecule number
# I - isotopologue number
def abundance(M,I):
    """
    INPUT PARAMETERS: 
        M: HITRAN molecule number
        I: HITRAN isotopologue number
    OUTPUT PARAMETERS: 
        Abbundance: natural abundance
    ---
    DESCRIPTION:
        Return natural (Earth) abundance of HITRAN isotolopogue.
    ---
    EXAMPLE OF USAGE:
        ab = abundance(1,1) # H2O
    ---
    """
    return ISO[(M,I)][ISO_INDEX['abundance']]

# Get molecular mass
# for a specified isotopologue
# M - molecule number
# I - isotopologue number
def molecularMass(M,I):
    """
    INPUT PARAMETERS: 
        M: HITRAN molecule number
        I: HITRAN isotopologue number
    OUTPUT PARAMETERS: 
        MolMass: molecular mass
    ---
    DESCRIPTION:
        Return molecular mass of HITRAN isotolopogue.
    ---
    EXAMPLE OF USAGE:
        mass = molecularMass(1,1) # H2O
    ---
    """
    return ISO[(M,I)][ISO_INDEX['mass']]

# Get molecule name
# for a specified isotopologue
# M - molecule number
# I - isotopologue number
def moleculeName(M):
    """
    INPUT PARAMETERS: 
        M: HITRAN molecule number
    OUTPUT PARAMETERS: 
        MolName: molecular name
    ---
    DESCRIPTION:
        Return name of HITRAN molecule.
    ---
    EXAMPLE OF USAGE:
        molname = moleculeName(1) # H2O
    ---
    """
    return ISO[(M,1)][ISO_INDEX['mol_name']]

# Get isotopologue name
# for a specified isotopologue
# M - molecule number
# I - isotopologue number
def isotopologueName(M,I):
    """
    INPUT PARAMETERS: 
        M: HITRAN molecule number
        I: HITRAN isotopologue number
    OUTPUT PARAMETERS: 
        IsoMass: isotopologue mass
    ---
    DESCRIPTION:
        Return name of HITRAN isotolopogue.
    ---
    EXAMPLE OF USAGE:
        isoname = isotopologueName(1,1) # H2O
    ---
    """
    return ISO[(M,I)][ISO_INDEX['iso_name']]

# ----------------------- table list ----------------------------------
def tableList():
    """
    INPUT PARAMETERS: 
        none
    OUTPUT PARAMETERS: 
        TableList: a list of available tables
    ---
    DESCRIPTION:
        Return a list of tables present in database.
    ---
    EXAMPLE OF USAGE:
        lst = tableList()
    ---
    """

    return getTableList()

# ----------------------- describe ----------------------------------
def describe(TableName):
    """
    INPUT PARAMETERS: 
        TableName: name of the table to describe
    OUTPUT PARAMETERS: 
        none
    ---
    DESCRIPTION:
        Print information about table, including 
        parameter names, formats and wavenumber range.
    ---
    EXAMPLE OF USAGE:
        describe('sampletab')
    ---
    """
    describeTable(TableName)

# ---------------------- /ISO.PY ---------------------------------------

def db_begin(db=None):
    """
    INPUT PARAMETERS: 
        db: database name (optional)
    OUTPUT PARAMETERS: 
        none
    ---
    DESCRIPTION:
        Open a database connection. A database is stored 
        in a folder given in db input parameter.
        Default=data
    ---
    EXAMPLE OF USAGE:
        db_begin('bar')
    ---
    """
    databaseBegin(db)

def db_commit():
    """
    INPUT PARAMETERS: 
        none
    OUTPUT PARAMETERS: 
        none
    ---
    DESCRIPTION:
        Commit all changes made to opened database.
        All tables will be saved in corresponding files.
    ---
    EXAMPLE OF USAGE:
        db_commit()
    ---
    """
    databaseCommit()

# ------------------ QUERY HITRAN ---------------------------------------

def comment(TableName,Comment):
    LOCAL_TABLE_CACHE[TableName]['header']['comment'] = Comment

def fetch_by_ids(TableName,iso_id_list,numin,numax):
    """
    INPUT PARAMETERS: 
        TableName:   local table name to fetch in (required)
        iso_id_list: list of isotopologue id's    (required)
        numin:       lower wavenumber bound       (required)
        numax:       upper wavenumber bound       (required)
    OUTPUT PARAMETERS: 
        none
    ---
    DESCRIPTION:
        Download line-by-line data from HITRANonline server
        and save it to local table. The input parameter iso_id_list
        contains list of "global" isotopologue Ids (see help on ISO_ID).
        Note: this function is required if user wants to download
        multiple species into single table.
    ---
    EXAMPLE OF USAGE:
        fetch_by_ids('water',[1,2,3,4],4000,4100)
    ---
    """
    if type(iso_id_list) not in set([list,tuple]):
       iso_id_list = [iso_id_list]
    queryHITRAN(TableName,iso_id_list,numin,numax)
    iso_names = [ISO_ID[i][ISO_ID_INDEX['iso_name']] for i in iso_id_list]
    Comment = 'Contains lines for '+','.join(iso_names)
    Comment += ('\n in %.3f-%.3f wavenumber range' % (numin,numax))
    comment(TableName,Comment)

#def queryHITRAN(TableName,iso_id_list,numin,numax):
def fetch(TableName,M,I,numin,numax):
    """
    INPUT PARAMETERS: 
        TableName:   local table name to fetch in (required)
        M:           HITRAN molecule number       (required)
        I:           HITRAN isotopologue number   (required)
        numin:       lower wavenumber bound       (required)
        numax:       upper wavenumber bound       (required)
    OUTPUT PARAMETERS: 
        none
    ---
    DESCRIPTION:
        Download line-by-line data from HITRANonline server
        and save it to local table. The input parameters M and I
        are the HITRAN molecule and isotopologue numbers.
        This function results in a table containing single 
        isotopologue specie. To have multiple species in a 
        single table use fetch_by_ids instead.
    ---
    EXAMPLE OF USAGE:
        fetch('HOH',1,1,4000,4100)
    ---
    """
    queryHITRAN(TableName,[ISO[(M,I)][ISO_INDEX['id']]],numin,numax)
    iso_name = ISO[(M,I)][ISO_INDEX['iso_name']]
    Comment = 'Contains lines for '+iso_name
    Comment += ('\n in %.3f-%.3f wavenumber range' % (numin,numax))
    comment(TableName,Comment)

# ------------------ partition sum --------------------------------------

# ------------------- LAGRANGE INTERPOLATION ----------------------

#def AtoB(aa,bb,A,B,npt)
def AtoB(aa,A,B,npt):
#***************************
#...LaGrange 3- and 4-point interpolation
#...arrays A and B are the npt data points,  given aa, a value of the 
#...A variable, the routine will find the corresponding bb value
#
#...input:  aa
#...output: bb 
    for I in range(2,npt+1):
        if A[I-1] >= aa:
            if I < 3 or I == npt:
                J = I
                if I < 3: J = 3
                if I == npt: J = npt
                J = J-1   # zero index correction
                A0D1=A[J-2]-A[J-1]
                if A0D1 == 0.0: A0D1=0.0001
                A0D2=A[J-2]-A[J]
                if A0D2 == 0.0: A0D2=0.0000
                A1D1=A[J-1]-A[J-2]
                if A1D1 == 0.0: A1D1=0.0001
                A1D2=A[J-1]-A[J]
                if A1D2 == 0.0: A1D2=0.0001
                A2D1=A[J]-A[J-2]
                if A2D1 == 0.0: A2D1=0.0001
                A2D2=A[J]-A[J-1]
                if A2D2 == 0.0: A2D2=0.0001

                A0=(aa-A[J-1])*(aa-A[J])/(A0D1*A0D2)
                A1=(aa-A[J-2])*(aa-A[J])/(A1D1*A1D2)
                A2=(aa-A[J-2])*(aa-A[J-1])/(A2D1*A2D2)

                bb = A0*B[J-2] + A1*B[J-1] + A2*B[J]

            else:
                J = I
                J = J-1   # zero index correction
                A0D1=A[J-2]-A[J-1]
                if A0D1 == 0.0: A0D1=0.0001
                A0D2=A[J-2]-A[J]
                if A0D2 == 0.0: A0D2=0.0001
                A0D3 = (A[J-2]-A[J+1])
                if A0D3 == 0.0: A0D3=0.0001
                A1D1=A[J-1]-A[J-2]
                if A1D1 == 0.0: A1D1=0.0001
                A1D2=A[J-1]-A[J]
                if A1D2 == 0.0: A1D2=0.0001
                A1D3 = A[J-1]-A[J+1]
                if A1D3 == 0.0: A1D3=0.0001

                A2D1=A[J]-A[J-2]
                if A2D1 == 0.0: A2D1=0.0001
                A2D2=A[J]-A[J-1]
                if A2D2 == 0.0: A2D2=0.0001
                A2D3 = A[J]-A[J+1]
                if A2D3 == 0.0: A2D3=0.0001

                A3D1 = A[J+1]-A[J-2]
                if A3D1 == 0.0: A3D1=0.0001
                A3D2 = A[J+1]-A[J-1]
                if A3D2 == 0.0: A3D2=0.0001
                A3D3 = A[J+1]-A[J]
                if A3D3 == 0.0: A3D3=0.0001

                A0=(aa-A[J-1])*(aa-A[J])*(aa-A[J+1])
                A0=A0/(A0D1*A0D2*A0D3)
                A1=(aa-A[J-2])*(aa-A[J])*(aa-A[J+1])
                A1=A1/(A1D1*A1D2*A1D3)
                A2=(aa-A[J-2])*(aa-A[J-1])*(aa-A[J+1])
                A2=A2/(A2D1*A2D2*A2D3)
                A3=(aa-A[J-2])*(aa-A[J-1])*(aa-A[J])
                A3=A3/(A3D1*A3D2*A3D3)

                bb = A0*B[J-2] + A1*B[J-1] + A2*B[J] + A3*B[J+1]

            break

    return bb


#  --------------- TIPS IMPLEMENTATION ----------------------

def BD_TIPS_2011_PYTHON(M,I,T):

    # out of temperature range
    if T<70. or T>3000.:
        #Qt = -1.
        #gi = 0.
        #return gi,Qt
        raise Exception('TIPS: T must be between 70K and 3000K.')
    
    try:
        # get statistical weight for specified isotopologue
        gi = TIPS_GSI_HASH[(M,I)]
        # interpolate partition sum for specified isotopologue
        Qt = AtoB(T,Tdat,TIPS_ISO_HASH[(M,I)],TIPS_NPT)
    except KeyError:
        raise Exception('TIPS: no data for M,I = %d,%d.' % (M,I))
    
    return gi,Qt

# Total internal partition sum
# M - molecule number
# I - isotopologue number
# T - temperature (K)
# returns (StatWeight,PartitionSum)
def partitionSum(M,I,T,step=None):
    """
    INPUT PARAMETERS: 
        M: HITRAN molecule number              (required)
        I: HITRAN isotopologue number          (required)
        T: temperature conditions              (required)
        step:  step to calculate temperatures  (optional)
    OUTPUT PARAMETERS:
        TT: list of temperatures (present only if T is a list)
        PartSum: partition sums calculated on a list of temperatures
    ---
    DESCRIPTION:
        Calculate range of partition sums at different temperatures.
        This function uses a python implementation of TIPS-2011 code:

        Reference:
            A. L. Laraia, R. R. Gamache, J. Lamouroux, I. E. Gordon, L. S. Rothman.
            Total internal partition sums to support planetary remote sensing.
            Icarus, Volume 215, Issue 1, September 2011, Pages 391–400
            http://dx.doi.org/10.1016/j.icarus.2011.06.004

        Output depends on a structure of input parameter T so that:
            1) If T is a scalar/list and step IS NOT provided,
                then calculate partition sums over each value of T.
            2) If T is a list and step parameter IS provided,
                then calculate partition sums between T[0] and T[1]
                with a given step.
    ---
    EXAMPLE OF USAGE:
        PartSum = partitionSum(1,1,[296,1000])
        TT,PartSum = partitionSum(1,1,[296,1000],step=0.1)
    ---
    """
	# partitionSum
    if not step:
       if type(T) not in set([list,tuple]):
          return BD_TIPS_2011_PYTHON(M,I,T)[1]
       else:
          return [BD_TIPS_2011_PYTHON(M,I,temp)[1] for temp in T]
    else:
       #n = (T[1]-T[0])/step
       #TT = linspace(T[0],T[1],n)
       TT = arange(T[0],T[1],step)
       return TT,array([BD_TIPS_2011_PYTHON(M,I,temp)[1] for temp in TT])

# ------------------ partition sum --------------------------------------


# ------------------ LINESHAPES -----------------------------------------

# ------------------ complex probability function -----------------------


# "naive" implementation for benchmarks
def cpf3(X,Y):

    # X,Y,WR,WI - numpy arrays
    if type(X) != ndarray: 
        if type(X) not in set([list,tuple]): 
            X = array([X])
        else:
            X = array(X)
    if type(Y) != ndarray: 
        if type(Y) not in set([list,tuple]): 
            Y = array([Y])
        else:
            Y = array(Y)

    zm1 = zone/__ComplexType__(X + zi*Y) # maybe redundant
    zm2 = zm1**2
    zsum = zone
    zterm=zone

    for tt_i in tt:
        zterm *= zm2*tt_i
        zsum += zterm
    
    zsum *= zi*zm1*pipwoeronehalf
    
    return zsum.real, zsum.imag


# Complex probability function implementation (Humlicek)
def cpf(X,Y):

    # X,Y,WR,WI - numpy arrays
    if type(X) != ndarray: 
        if type(X) not in set([list,tuple]): 
            X = array([X])
        else:
            X = array(X)
    if type(Y) != ndarray: 
        if type(Y) not in set([list,tuple]): 
            Y = array([Y])
        else:
            Y = array(Y)
    
    # REGION3
    index_REGION3 = where(sqrt(X**2 + Y**2) > __FloatType__(8.0e0))
    X_REGION3 = X[index_REGION3]
    Y_REGION3 = Y[index_REGION3]
    zm1 = zone/__ComplexType__(X_REGION3 + zi*Y_REGION3)
    zm2 = zm1**2
    zsum_REGION3 = zone
    zterm=zone
    for tt_i in tt:
        zterm *= zm2*tt_i
        zsum_REGION3 += zterm
    zsum_REGION3 *= zi*zm1*pipwoeronehalf
    
    index_REGION12 = setdiff1d(array(arange(len(X))),array(index_REGION3))
    X_REGION12 = X[index_REGION12]
    Y_REGION12 = Y[index_REGION12]
    
    WR = __FloatType__(0.0e0)
    WI = __FloatType__(0.0e0)
    
    # REGION12
    Y1_REGION12 = Y_REGION12 + __FloatType__(1.5e0)
    Y2_REGION12 = Y1_REGION12**2

    # REGION2    
    subindex_REGION2 = where((Y_REGION12 <= 0.85e0) & 
                             (abs(X_REGION12) >= (18.1e0*Y_REGION12 + 1.65e0)))
    
    index_REGION2 = index_REGION12[subindex_REGION2]
    
    X_REGION2 = X[index_REGION2]
    Y_REGION2 = Y[index_REGION2]
    Y1_REGION2 = Y1_REGION12[subindex_REGION2]
    Y2_REGION2 = Y2_REGION12[subindex_REGION2]
    Y3_REGION2 = Y_REGION2 + __FloatType__(3.0e0)
    
    WR_REGION2 = WR
    WI_REGION2 = WI

    WR_REGION2 = zeros(len(X_REGION2))
    ii = abs(X_REGION2) < __FloatType__(12.0e0)
    WR_REGION2[ii] = exp(-X_REGION2[ii]**2)
    WR_REGION2[~ii] = WR
    
    for I in range(6):
        R_REGION2 = X_REGION2 - T[I]
        R2_REGION2 = R_REGION2**2
        D_REGION2 = __FloatType__(1.0e0) / (R2_REGION2 + Y2_REGION2)
        D1_REGION2 = Y1_REGION2 * D_REGION2
        D2_REGION2 = R_REGION2 * D_REGION2
        WR_REGION2 = WR_REGION2 + Y_REGION2 * (U[I]*(R_REGION2*D2_REGION2 - 1.5e0*D1_REGION2) + 
                                               S[I]*Y3_REGION2*D2_REGION2)/(R2_REGION2 + 2.25e0)
        R_REGION2 = X_REGION2 + T[I]
        R2_REGION2 = R_REGION2**2                
        D_REGION2 = __FloatType__(1.0e0) / (R2_REGION2 + Y2_REGION2)
        D3_REGION2 = Y1_REGION2 * D_REGION2
        D4_REGION2 = R_REGION2 * D_REGION2
        WR_REGION2 = WR_REGION2 + Y_REGION2 * (U[I]*(R_REGION2*D4_REGION2 - 1.5e0*D3_REGION2) - 
                                               S[I]*Y3_REGION2*D4_REGION2)/(R2_REGION2 + 2.25e0)
        WI_REGION2 = WI_REGION2 + U[I]*(D2_REGION2 + D4_REGION2) + S[I]*(D1_REGION2 - D3_REGION2)

    # REGION3
    index_REGION1 = setdiff1d(array(index_REGION12),array(index_REGION2))
    X_REGION1 = X[index_REGION1]
    Y_REGION1 = X[index_REGION1]
    
    subindex_REGION1 = setdiff1d(array(arange(len(index_REGION12))),array(subindex_REGION2))
    Y1_REGION1 = Y1_REGION12[subindex_REGION1]
    Y2_REGION1 = Y2_REGION12[subindex_REGION1]
    
    WR_REGION1 = WR
    WI_REGION1 = WI  
    
    for I in range(6):
        R_REGION1 = X_REGION1 - T[I]
        D_REGION1 = __FloatType__(1.0e0) / (R_REGION1**2 + Y2_REGION1)
        D1_REGION1 = Y1_REGION1 * D_REGION1
        D2_REGION1 = R_REGION1 * D_REGION1
        R_REGION1 = X_REGION1 + T[I]
        D_REGION1 = __FloatType__(1.0e0) / (R_REGION1**2 + Y2_REGION1)
        D3_REGION1 = Y1_REGION1 * D_REGION1
        D4_REGION1 = R_REGION1 * D_REGION1
        
        WR_REGION1 = WR_REGION1 + U[I]*(D1_REGION1 + D3_REGION1) - S[I]*(D2_REGION1 - D4_REGION1)
        WI_REGION1 = WI_REGION1 + U[I]*(D2_REGION1 + D4_REGION1) + S[I]*(D1_REGION1 - D3_REGION1)

    # total result
    WR_TOTAL = zeros(len(X))
    WI_TOTAL = zeros(len(X))
    # REGION3
    WR_TOTAL[index_REGION3] = zsum_REGION3.real
    WI_TOTAL[index_REGION3] = zsum_REGION3.imag
    # REGION2
    WR_TOTAL[index_REGION2] = WR_REGION2
    WI_TOTAL[index_REGION2] = WI_REGION2
    # REGION1
    WR_TOTAL[index_REGION1] = WR_REGION1
    WI_TOTAL[index_REGION1] = WI_REGION1
    
    return WR_TOTAL,WI_TOTAL


# ------------------ Hartmann-Tran Profile (HTP) ------------------------
def pcqsdhc_BACKUP(sg0,GamD,Gam0,Gam2,Shift0,Shift2,anuVC,eta,sg):
    #-------------------------------------------------
    #      "pCqSDHC": partially-Correlated quadratic-Speed-Dependent Hard-Collision
    #      Subroutine to Compute the complex normalized spectral shape of an 
    #      isolated line by the pCqSDHC model
    #
    #      Reference:
    #      H. Tran, N.H. Ngo, J.-M. Hartmann.
    #      Efficient computation of some speed-dependent isolated line profiles.
    #      JQSRT, Volume 129, November 2013, Pages 199–203
    #      http://dx.doi.org/10.1016/j.jqsrt.2013.06.015
    #
    #      Input/Output Parameters of Routine (Arguments or Common)
    #      ---------------------------------
    #      T          : Temperature in Kelvin (Input).
    #      amM1       : Molar mass of the absorber in g/mol(Input).
    #      sg0        : Unperturbed line position in cm-1 (Input).
    #      GamD       : Doppler HWHM in cm-1 (Input)
    #      Gam0       : Speed-averaged line-width in cm-1 (Input).       
    #      Gam2       : Speed dependence of the line-width in cm-1 (Input).
    #      anuVC      : Velocity-changing frequency in cm-1 (Input).
    #      eta        : Correlation parameter, No unit (Input).
    #      Shift0     : Speed-averaged line-shift in cm-1 (Input).
    #      Shift2     : Speed dependence of the line-shift in cm-1 (Input)       
    #      sg         : Current WaveNumber of the Computation in cm-1 (Input).
    #
    #      Output Quantities (through Common Statements)
    #      -----------------
    #      LS_pCqSDHC_R: Real part of the normalized spectral shape (cm)
    #      LS_pCqSDHC_I: Imaginary part of the normalized spectral shape (cm)
    #
    #      Called Routines: 'CPF'      (Complex Probability Function)
    #      ---------------  'CPF3'      (Complex Probability Function for the region 3)
    #
    #      Called By: Main Program
    #      ---------
    #
    #     Double Precision Version
    #
    #-------------------------------------------------
    
    # sg is the only vector argument which is passed to fusnction
    
    if type(sg) not in set([array,ndarray,list,tuple]):
        sg = array([sg])
    
    number_of_points = len(sg)
    Aterm_GLOBAL = zeros(number_of_points,dtype=__ComplexType__)
    Bterm_GLOBAL = zeros(number_of_points,dtype=__ComplexType__)

    cte=sqrt(log(2.0e0))/GamD
    rpi=sqrt(pi)
    iz = __ComplexType__(0.0e0 + 1.0e0j)

    c0 = __ComplexType__(Gam0 - 1.0e0j*Shift0)
    c2=__ComplexType__(Gam2 - 1.0e0j*Shift2)
    c0t = __ComplexType__((1.0e0 - eta) * (c0 - 1.5e0 * c2) + anuVC)
    c2t = __ComplexType__((1.0e0 - eta) * c2)
    Y = __ComplexType__(1.0e0 / ((2.0e0*cte*c2t))**2)

    # X - vector, Y - scalar
    X = (iz * (sg - sg0) + c0t) / c2t

    # PART1
    if abs(c2t) == 0.0e0:
        Z1 = (iz*(sg - sg0) + c0t) * cte
        xZ1 = -Z1.imag
        yZ1 = Z1.real
        WR1,WI1 = cpf(xZ1,yZ1)
        Aterm_GLOBAL = rpi*cte*__ComplexType__(WR1 + 1.0e0j*WI1)
        index_Z1 = abs(Z1) <= 4.0e3
        index_NOT_Z1 = ~index_Z1
        if any(index_Z1):
            Bterm_GLOBAL = rpi*cte*((1.0e0 - Z1**2)*__ComplexType__(WR1 + 1.0e0j*WI1) + Z1/rpi)
        if any(index_NOT_Z1):
            Bterm_GLOBAL = cte*(rpi*__ComplexType__(WR1 + 1.0e0j*WI1) + 0.5e0/Z1 - 0.75e0/(Z1**3))
    else:
        # PART2, PART3 AND PART4   (PART4 IS A MAIN PART)
        index_PART2 = abs(X) < 3.0e-8 * abs(Y)
        index_PART3 = (abs(Y) < 1.0e-15 * abs(X)) & ~index_PART2
        index_PART4 = ~ (index_PART2 | index_PART3)
        
        # PART4
        if any(index_PART4):
            X_TMP = X[index_PART4]
            Z1 = sqrt(X_TMP + Y) - sqrt(Y)
            Z2 = Z1 + __FloatType__(2.0e0) * sqrt(Y)
            xZ1 = -Z1.imag
            yZ1 =  Z1.real
            xZ2 = -Z2.imag
            yZ2 =  Z2.real
            SZ1 = sqrt(xZ1**2 + yZ1**2)
            SZ2 = sqrt(xZ2**2 + yZ2**2)
            DSZ = abs(SZ1 - SZ2)
            SZmx = maximum(SZ1,SZ2)
            SZmn = minimum(SZ1,SZ2)
            length_PART4 = len(index_PART4)
            WR1_PART4 = zeros(length_PART4)
            WI1_PART4 = zeros(length_PART4)
            WR2_PART4 = zeros(length_PART4)
            WI2_PART4 = zeros(length_PART4)
            index_CPF3 = (DSZ <= 1.0e0) & (SZmx > 8.0e0) & (SZmn <= 8.0e0)
            index_CPF = ~index_CPF3 # can be removed
            if any(index_CPF3):
                WR1,WI1 = cpf3(xZ1[index_CPF3],yZ1[index_CPF3])
                WR2,WI2 = cpf3(xZ2[index_CPF3],yZ2[index_CPF3])
                WR1_PART4[index_CPF3] = WR1
                WI1_PART4[index_CPF3] = WI1
                WR2_PART4[index_CPF3] = WR2
                WI2_PART4[index_CPF3] = WI2
            if any(index_CPF):
                WR1,WI1 = cpf(xZ1[index_CPF],yZ1[index_CPF])
                WR2,WI2 = cpf(xZ2[index_CPF],yZ2[index_CPF])
                WR1_PART4[index_CPF] = WR1
                WI1_PART4[index_CPF] = WI1
                WR2_PART4[index_CPF] = WR2
                WI2_PART4[index_CPF] = WI2
            
            Aterm = rpi*cte*(__ComplexType__(WR1_PART4 + 1.0e0j*WI1_PART4) - __ComplexType__(WR2_PART4+1.0e0j*WI2_PART4))
            Bterm = (-1.0e0 +
                      rpi/(2.0e0*sqrt(Y))*(1.0e0 - Z1**2)*__ComplexType__(WR1_PART4 + 1.0e0j*WI1_PART4)-
                      rpi/(2.0e0*sqrt(Y))*(1.0e0 - Z2**2)*__ComplexType__(WR2_PART4 + 1.0e0j*WI2_PART4)) / c2t
            Aterm_GLOBAL[index_PART4] = Aterm
            Bterm_GLOBAL[index_PART4] = Bterm

        # PART2
        if any(index_PART2):
            X_TMP = X[index_PART2]
            Z1 = (iz*(sg[index_PART2] - sg0) + c0t) * cte
            Z2 = sqrt(X_TMP + Y) + sqrt(Y)
            xZ1 = -Z1.imag
            yZ1 = Z1.real
            xZ2 = -Z2.imag
            yZ2 = Z2.real
            WR1_PART2,WI1_PART2 = cpf(xZ1,yZ1)
            WR2_PART2,WI2_PART2 = cpf(xZ2,yZ2) 
            Aterm = rpi*cte*(__ComplexType__(WR1_PART2 + 1.0e0j*WI1_PART2) - __ComplexType__(WR2_PART2 + 1.0e0j*WI2_PART2))
            Bterm = (-1.0e0 +
                      rpi/(2.0e0*sqrt(Y))*(1.0e0 - Z1**2)*__ComplexType__(WR1_PART2 + 1.0e0j*WI1_PART2)-
                      rpi/(2.0e0*sqrt(Y))*(1.0e0 - Z2**2)*__ComplexType__(WR2_PART2 + 1.0e0j*WI2_PART2)) / c2t
            Aterm_GLOBAL[index_PART2] = Aterm
            Bterm_GLOBAL[index_PART2] = Bterm
            
        # PART3
        if any(index_PART3):
            X_TMP = X[index_PART3]
            xZ1 = -sqrt(X_TMP + Y).imag
            yZ1 = sqrt(X_TMP + Y).real
            WR1_PART3,WI1_PART3 =  cpf(xZ1,yZ1) 
            index_ABS = abs(sqrt(X_TMP)) <= 4.0e3
            index_NOT_ABS = ~index_ABS
            Aterm = zeros(len(index_PART3),dtype=__ComplexType__)
            Bterm = zeros(len(index_PART3),dtype=__ComplexType__)
            if any(index_ABS):
                xXb = -sqrt(X).imag
                yXb = sqrt(X).real
                WRb,WIb = cpf(xXb,yXb)
                Aterm[index_ABS] = (2.0e0*rpi/c2t)*(1.0e0/rpi - sqrt(X_TMP[index_ABS])*__ComplexType__(WRb + 1.0e0j*WIb))
                Bterm[index_ABS] = (1.0e0/c2t)*(-1.0e0+
                                  2.0e0*rpi*(1.0e0 - X_TMP[index_ABS]-2.0e0*Y)*(1.0e0/rpi-sqrt(X_TMP[index_ABS])*__ComplexType__(WRb + 1.0e0j*WIb))+
                                  2.0e0*rpi*sqrt(X_TMP[index_ABS] + Y)*__ComplexType__(WR1_PART3 + 1.0e0j*WI1_PART3))
            if any(index_NOT_ABS):
                Aterm[index_NOT_ABS] = (1.0e0/c2t)*(1.0e0/X_TMP[index_NOT_ABS] - 1.5e0/(X_TMP[index_NOT_ABS]**2))
                Bterm[index_NOT_ABS] = (1.0e0/c2t)*(-1.0e0 + (1.0e0 - X_TMP[index_NOT_ABS] - 2.0e0*Y)*
                                        (1.0e0/X_TMP[index_NOT_ABS] - 1.5e0/(X_TMP[index_NOT_ABS]**2))+
                                         2.0e0*rpi*sqrt(X_TMP[index_NOT_ABS] + Y)*__ComplexType__(WR1 + 1.0e0j*WI1))
            Aterm_GLOBAL[index_PART3] = Aterm
            Bterm_GLOBAL[index_PART3] = Bterm
            
    # common part
    LS_pCqSDHC = (1.0e0/pi) * (Aterm_GLOBAL / (1.0e0 - (anuVC-eta*(c0-1.5e0*c2))*Aterm_GLOBAL + eta*c2*Bterm_GLOBAL))
    return LS_pCqSDHC.real,LS_pCqSDHC.imag



# ------------------ Hartmann-Tran Profile (HTP) ------------------------
def pcqsdhc(sg0,GamD,Gam0,Gam2,Shift0,Shift2,anuVC,eta,sg):
    #-------------------------------------------------
    #      "pCqSDHC": partially-Correlated quadratic-Speed-Dependent Hard-Collision
    #      Subroutine to Compute the complex normalized spectral shape of an 
    #      isolated line by the pCqSDHC model
    #
    #      Reference:
    #      H. Tran, N.H. Ngo, J.-M. Hartmann.
    #      Efficient computation of some speed-dependent isolated line profiles.
    #      JQSRT, Volume 129, November 2013, Pages 199–203
    #      http://dx.doi.org/10.1016/j.jqsrt.2013.06.015
    #
    #      Input/Output Parameters of Routine (Arguments or Common)
    #      ---------------------------------
    #      T          : Temperature in Kelvin (Input).
    #      amM1       : Molar mass of the absorber in g/mol(Input).
    #      sg0        : Unperturbed line position in cm-1 (Input).
    #      GamD       : Doppler HWHM in cm-1 (Input)
    #      Gam0       : Speed-averaged line-width in cm-1 (Input).       
    #      Gam2       : Speed dependence of the line-width in cm-1 (Input).
    #      anuVC      : Velocity-changing frequency in cm-1 (Input).
    #      eta        : Correlation parameter, No unit (Input).
    #      Shift0     : Speed-averaged line-shift in cm-1 (Input).
    #      Shift2     : Speed dependence of the line-shift in cm-1 (Input)       
    #      sg         : Current WaveNumber of the Computation in cm-1 (Input).
    #
    #      Output Quantities (through Common Statements)
    #      -----------------
    #      LS_pCqSDHC_R: Real part of the normalized spectral shape (cm)
    #      LS_pCqSDHC_I: Imaginary part of the normalized spectral shape (cm)
    #
    #      Called Routines: 'CPF'      (Complex Probability Function)
    #      ---------------  'CPF3'      (Complex Probability Function for the region 3)
    #
    #      Called By: Main Program
    #      ---------
    #
    #     Double Precision Version
    #
    #-------------------------------------------------
    
    # sg is the only vector argument which is passed to fusnction
    
    if type(sg) not in set([array,ndarray,list,tuple]):
        sg = array([sg])
    
    number_of_points = len(sg)
    Aterm_GLOBAL = zeros(number_of_points,dtype=__ComplexType__)
    Bterm_GLOBAL = zeros(number_of_points,dtype=__ComplexType__)

    cte=sqrt(log(2.0e0))/GamD
    rpi=sqrt(pi)
    iz = __ComplexType__(0.0e0 + 1.0e0j)

    c0 = __ComplexType__(Gam0 + 1.0e0j*Shift0)
    c2 = __ComplexType__(Gam2 + 1.0e0j*Shift2)
    c0t = __ComplexType__((1.0e0 - eta) * (c0 - 1.5e0 * c2) + anuVC)
    c2t = __ComplexType__((1.0e0 - eta) * c2)

    # PART1
    if abs(c2t) == 0.0e0:
        Z1 = (iz*(sg0 - sg) + c0t) * cte
        xZ1 = -Z1.imag
        yZ1 = Z1.real
        WR1,WI1 = cpf(xZ1,yZ1)
        Aterm_GLOBAL = rpi*cte*__ComplexType__(WR1 + 1.0e0j*WI1)
        index_Z1 = abs(Z1) <= 4.0e3
        index_NOT_Z1 = ~index_Z1
        if any(index_Z1):
            Bterm_GLOBAL = rpi*cte*((1.0e0 - Z1**2)*__ComplexType__(WR1 + 1.0e0j*WI1) + Z1/rpi)
        if any(index_NOT_Z1):
            Bterm_GLOBAL = cte*(rpi*__ComplexType__(WR1 + 1.0e0j*WI1) + 0.5e0/Z1 - 0.75e0/(Z1**3))
    else:
        # PART2, PART3 AND PART4   (PART4 IS A MAIN PART)

        # X - vector, Y - scalar
        X = (iz * (sg0 - sg) + c0t) / c2t
        Y = __ComplexType__(1.0e0 / ((2.0e0*cte*c2t))**2)
        csqrtY = (Gam2 - iz*Shift2) / (2.0e0*cte*(1.0e0-eta) * (Gam2**2 + Shift2**2))

        index_PART2 = abs(X) <= 3.0e-8 * abs(Y)
        index_PART3 = (abs(Y) <= 1.0e-15 * abs(X)) & ~index_PART2
        index_PART4 = ~ (index_PART2 | index_PART3)
        
        # PART4
        if any(index_PART4):
            X_TMP = X[index_PART4]
            Z1 = sqrt(X_TMP + Y) - csqrtY
            Z2 = Z1 + __FloatType__(2.0e0) * csqrtY
            xZ1 = -Z1.imag
            yZ1 =  Z1.real
            xZ2 = -Z2.imag
            yZ2 =  Z2.real
            SZ1 = sqrt(xZ1**2 + yZ1**2)
            SZ2 = sqrt(xZ2**2 + yZ2**2)
            DSZ = abs(SZ1 - SZ2)
            SZmx = maximum(SZ1,SZ2)
            SZmn = minimum(SZ1,SZ2)
            length_PART4 = len(index_PART4)
            WR1_PART4 = zeros(length_PART4)
            WI1_PART4 = zeros(length_PART4)
            WR2_PART4 = zeros(length_PART4)
            WI2_PART4 = zeros(length_PART4)
            index_CPF3 = (DSZ <= 1.0e0) & (SZmx > 8.0e0) & (SZmn <= 8.0e0)
            index_CPF = ~index_CPF3 # can be removed
            if any(index_CPF3):
                WR1,WI1 = cpf3(xZ1[index_CPF3],yZ1[index_CPF3])
                WR2,WI2 = cpf3(xZ2[index_CPF3],yZ2[index_CPF3])
                WR1_PART4[index_CPF3] = WR1
                WI1_PART4[index_CPF3] = WI1
                WR2_PART4[index_CPF3] = WR2
                WI2_PART4[index_CPF3] = WI2
            if any(index_CPF):
                WR1,WI1 = cpf(xZ1[index_CPF],yZ1[index_CPF])
                WR2,WI2 = cpf(xZ2[index_CPF],yZ2[index_CPF])
                WR1_PART4[index_CPF] = WR1
                WI1_PART4[index_CPF] = WI1
                WR2_PART4[index_CPF] = WR2
                WI2_PART4[index_CPF] = WI2
            
            Aterm = rpi*cte*(__ComplexType__(WR1_PART4 + 1.0e0j*WI1_PART4) - __ComplexType__(WR2_PART4+1.0e0j*WI2_PART4))
            Bterm = (-1.0e0 +
                      rpi/(2.0e0*csqrtY)*(1.0e0 - Z1**2)*__ComplexType__(WR1_PART4 + 1.0e0j*WI1_PART4)-
                      rpi/(2.0e0*csqrtY)*(1.0e0 - Z2**2)*__ComplexType__(WR2_PART4 + 1.0e0j*WI2_PART4)) / c2t
            Aterm_GLOBAL[index_PART4] = Aterm
            Bterm_GLOBAL[index_PART4] = Bterm

        # PART2
        if any(index_PART2):
            X_TMP = X[index_PART2]
            Z1 = (iz*(sg0 - sg[index_PART2]) + c0t) * cte
            Z2 = sqrt(X_TMP + Y) + csqrtY
            xZ1 = -Z1.imag
            yZ1 = Z1.real
            xZ2 = -Z2.imag
            yZ2 = Z2.real
            WR1_PART2,WI1_PART2 = cpf(xZ1,yZ1)
            WR2_PART2,WI2_PART2 = cpf(xZ2,yZ2) 
            Aterm = rpi*cte*(__ComplexType__(WR1_PART2 + 1.0e0j*WI1_PART2) - __ComplexType__(WR2_PART2 + 1.0e0j*WI2_PART2))
            Bterm = (-1.0e0 +
                      rpi/(2.0e0*csqrtY)*(1.0e0 - Z1**2)*__ComplexType__(WR1_PART2 + 1.0e0j*WI1_PART2)-
                      rpi/(2.0e0*csqrtY)*(1.0e0 - Z2**2)*__ComplexType__(WR2_PART2 + 1.0e0j*WI2_PART2)) / c2t
            Aterm_GLOBAL[index_PART2] = Aterm
            Bterm_GLOBAL[index_PART2] = Bterm
            
        # PART3
        if any(index_PART3):
            X_TMP = X[index_PART3]
            xZ1 = -sqrt(X_TMP + Y).imag
            yZ1 = sqrt(X_TMP + Y).real
            WR1_PART3,WI1_PART3 =  cpf(xZ1,yZ1) 
            index_ABS = abs(sqrt(X_TMP)) <= 4.0e3
            index_NOT_ABS = ~index_ABS
            Aterm = zeros(len(index_PART3),dtype=__ComplexType__)
            Bterm = zeros(len(index_PART3),dtype=__ComplexType__)
            if any(index_ABS):
                xXb = -sqrt(X).imag
                yXb = sqrt(X).real
                WRb,WIb = cpf(xXb,yXb)
                Aterm[index_ABS] = (2.0e0*rpi/c2t)*(1.0e0/rpi - sqrt(X_TMP[index_ABS])*__ComplexType__(WRb + 1.0e0j*WIb))
                Bterm[index_ABS] = (1.0e0/c2t)*(-1.0e0+
                                  2.0e0*rpi*(1.0e0 - X_TMP[index_ABS]-2.0e0*Y)*(1.0e0/rpi-sqrt(X_TMP[index_ABS])*__ComplexType__(WRb + 1.0e0j*WIb))+
                                  2.0e0*rpi*sqrt(X_TMP[index_ABS] + Y)*__ComplexType__(WR1_PART3 + 1.0e0j*WI1_PART3))
            if any(index_NOT_ABS):
                Aterm[index_NOT_ABS] = (1.0e0/c2t)*(1.0e0/X_TMP[index_NOT_ABS] - 1.5e0/(X_TMP[index_NOT_ABS]**2))
                Bterm[index_NOT_ABS] = (1.0e0/c2t)*(-1.0e0 + (1.0e0 - X_TMP[index_NOT_ABS] - 2.0e0*Y)*
                                        (1.0e0/X_TMP[index_NOT_ABS] - 1.5e0/(X_TMP[index_NOT_ABS]**2))+
                                         2.0e0*rpi*sqrt(X_TMP[index_NOT_ABS] + Y)*__ComplexType__(WR1 + 1.0e0j*WI1))
            Aterm_GLOBAL[index_PART3] = Aterm
            Bterm_GLOBAL[index_PART3] = Bterm
            
    # common part
    LS_pCqSDHC = (1.0e0/pi) * (Aterm_GLOBAL / (1.0e0 - (anuVC-eta*(c0-1.5e0*c2))*Aterm_GLOBAL + eta*c2*Bterm_GLOBAL))
    return LS_pCqSDHC.real,LS_pCqSDHC.imag



# ------------------  CROSS-SECTIONS, XSECT.PY --------------------------------

# set interfaces for TIPS(M,I,T)
PYTIPS = lambda M,I,T: BD_TIPS_2011_PYTHON(M,I,T)[1]

# set interfaces for profiles
#PYHTP = pcqsdhc
#PROFILE_HTP = PYHTP
#PROFILE_VOIGT = lambda sg0,GamD,Gam0,sg: PROFILE_HTP(sg0,GamD,Gam0,cZero,cZero,cZero,cZero,cZero,sg)
#PROFILE_LORENTZ = lambda sg0,Gam0,sg: Gam0/(pi*(Gam0**2+(sg-sg0)**2))
#PROFILE_DOPPLER = lambda sg0,GamD,sg: cSqrtLn2divSqrtPi*exp(-cLn2*((sg-sg0)/GamD)**2)/GamD


def PROFILE_HT(sg0,GamD,Gam0,Gam2,Shift0,Shift2,anuVC,eta,sg):
    """
    #-------------------------------------------------
    #      "pCqSDHC": partially-Correlated quadratic-Speed-Dependent Hard-Collision
    #      Subroutine to Compute the complex normalized spectral shape of an 
    #      isolated line by the pCqSDHC model
    #
    #      References:
    #
    #      1) N.H. Ngo, D. Lisak, H. Tran, J.-M. Hartmann.
    #         An isolated line-shape model to go beyond the Voigt profile in 
    #         spectroscopic databases and radiative transfer codes.
    #         JQSRT, Volume 129, November 2013, Pages 89–100
    #         http://dx.doi.org/10.1016/j.jqsrt.2013.05.034
    #
    #      2) H. Tran, N.H. Ngo, J.-M. Hartmann.
    #         Efficient computation of some speed-dependent isolated line profiles.
    #         JQSRT, Volume 129, November 2013, Pages 199–203
    #         http://dx.doi.org/10.1016/j.jqsrt.2013.06.015
    #
    #      3) H. Tran, N.H. Ngo, J.-M. Hartmann.
    #         Erratum to “Efficient computation of some speed-dependent isolated line profiles”.
    #         JQSRT, Volume 134, February 2014, Pages 104
    #         http://dx.doi.org/10.1016/j.jqsrt.2013.10.015
    #
    #      Input/Output Parameters of Routine (Arguments or Common)
    #      ---------------------------------
    #      T       : Temperature in Kelvin (Input).
    #      amM1    : Molar mass of the absorber in g/mol(Input).
    #      sg0     : Unperturbed line position in cm-1 (Input).
    #      GamD    : Doppler HWHM in cm-1 (Input)
    #      Gam0    : Speed-averaged line-width in cm-1 (Input).       
    #      Gam2    : Speed dependence of the line-width in cm-1 (Input).
    #      anuVC   : Velocity-changing frequency in cm-1 (Input).
    #      eta     : Correlation parameter, No unit (Input).
    #      Shift0  : Speed-averaged line-shift in cm-1 (Input).
    #      Shift2  : Speed dependence of the line-shift in cm-1 (Input)       
    #      sg      : Current WaveNumber of the Computation in cm-1 (Input).
    #
    #      The function has two outputs:
    #      -----------------
    #      (1): Real part of the normalized spectral shape (cm)
    #      (2): Imaginary part of the normalized spectral shape (cm)
    #
    #      Called Routines: 'CPF'       (Complex Probability Function)
    #      ---------------  'CPF3'      (Complex Probability Function for the region 3)
    #
    #      Based on a double precision Fortran version
    #
    #-------------------------------------------------
    """
    return pcqsdhc(sg0,GamD,Gam0,Gam2,Shift0,Shift2,anuVC,eta,sg)



def PROFILE_VOIGT(sg0,GamD,Gam0,sg):
    """
    # Voigt profile based on HTP.
    # Input parameters:
    #   sg0: Unperturbed line position in cm-1 (Input).
    #   GamD: Doppler HWHM in cm-1 (Input)
    #   Gam0: Speed-averaged line-width in cm-1 (Input).       
    #   sg: Current WaveNumber of the Computation in cm-1 (Input).
    """
    return PROFILE_HTP(sg0,GamD,Gam0,cZero,cZero,cZero,cZero,cZero,sg)

def PROFILE_LORENTZ(sg0,Gam0,sg):
    """
    # Lorentz profile.
    # Input parameters:
    #   sg0: Unperturbed line position in cm-1 (Input).
    #   Gam0: Speed-averaged line-width in cm-1 (Input).       
    #   sg: Current WaveNumber of the Computation in cm-1 (Input).
    """
    return Gam0/(pi*(Gam0**2+(sg-sg0)**2))

def PROFILE_DOPPLER(sg0,GamD,sg):
    """
    # Doppler profile.
    # Input parameters:
    #   sg0: Unperturbed line position in cm-1 (Input).
    #   GamD: Doppler HWHM in cm-1 (Input)
    #   sg: Current WaveNumber of the Computation in cm-1 (Input).
    """
    return cSqrtLn2divSqrtPi*exp(-cLn2*((sg-sg0)/GamD)**2)/GamD

# Volume concentration of all gas molecules at the pressure p and temperature T
def volumeConcentration(p,T):
    return (p/9.869233e-7)/(cBolts*T) # CGS

# ------------------------------- PARAMETER DEPENDENCIES --------------------------------

# temperature dependence for intencities (HITRAN)
def EnvironmentDependency_Intensity(LineIntensityRef,T,Tref,SigmaT,SigmaTref,
                                    LowerStateEnergy,LineCenter):
    const = __FloatType__(1.4388028496642257)
    ch = exp(-const*LowerStateEnergy/T)*(1-exp(-const*LineCenter/T))
    zn = exp(-const*LowerStateEnergy/Tref)*(1-exp(-const*LineCenter/Tref))
    LineIntensity = LineIntensityRef*SigmaTref/SigmaT*ch/zn
    return LineIntensity

# environmental dependence for GammaD (HTP, Voigt)    # Tref/T ????
def EnvironmentDependency_GammaD(GammaD_ref,T,Tref):
    # Doppler parameters do not depend on pressure!
    return GammaD_ref*sqrt(T/Tref)

# environmental dependence for Gamma0 (HTP, Voigt)
def EnvironmentDependency_Gamma0(Gamma0_ref,T,Tref,p,pref,TempRatioPower):
    return Gamma0_ref*p/pref*(Tref/T)**TempRatioPower

# environmental dependence for Gamma2 (HTP)
def EnvironmentDependency_Gamma2(Gamma2_ref,T,Tref,p,pref,TempRatioPower):
    return Gamma2_ref*p/pref*(Tref/T)**TempRatioPower

# environmental dependence for Delta0 (HTP)
def EnvironmentDependency_Delta0(Delta0_ref,p,pref):
    return Delta0_ref*p/pref

# environmental dependence for Delta2 (HTP)
def EnvironmentDependency_Delta2(Delta2_ref,p,pref):
    return Delta2_ref*p/pref

# environmental dependence for anuVC (HTP)
def EnvironmentDependency_anuVC(anuVC_ref,T,Tref,p,pref):
    return anuVC_ref*Tref/T*p/pref

# ------------------------------- /PARAMETER DEPENDENCIES --------------------------------

# ------------------------------- BINGINGS --------------------------------


# check and argument for being a tuple or list
# this is connected with a "bug" that in Python
# (val) is not a tuple, but (val,) is a tuple
def listOfTuples(a):
    if type(a) not in set([list,tuple]):
        a = [a]
    return a


# determine default parameters from those which are passed to absorptionCoefficient_...
def getDefaultValuesForXsect(Components,SourceTables,Environment,OmegaRange,
                             OmegaStep,OmegaWing,IntensityThreshold,Format):
    if SourceTables[0] == None:
        SourceTables = ['__BUFFER__',]
    if Environment == None:
        Environment = {'T':296., 'p':1.}
    if Components == [None]:
        CompDict = {}
        for TableName in SourceTables:
            # check table existance
            if TableName not in LOCAL_TABLE_CACHE.keys():
                raise Exception('%s: no such table. Check tableList() for more info.' % TableName)
            mol_ids = LOCAL_TABLE_CACHE[TableName]['data']['molec_id']
            iso_ids = LOCAL_TABLE_CACHE[TableName]['data']['local_iso_id']
            if len(mol_ids) != len(iso_ids):
                raise Exception('Lengths if mol_ids and iso_ids differ!')
            MI_zip = zip(mol_ids,iso_ids)
            MI_zip = set(MI_zip)
            for mol_id,iso_id in MI_zip:
                CompDict[(mol_id,iso_id)] = None
        Components = CompDict.keys()
    if OmegaRange == None:
        omega_min = float('inf')
        omega_max = float('-inf')
        for TableName in SourceTables:
            nu = LOCAL_TABLE_CACHE[TableName]['data']['nu']
            numin = min(nu)
            numax = max(nu)
            if omega_min > numin:
                omega_min = numin
            if omega_max < numax:
                omega_max = numax
        OmegaRange = (omega_min,omega_max)
    OmegaDelta = OmegaRange[1]-OmegaRange[0]
    if OmegaStep == None:
        #OmegaStep = OmegaDelta/100.
        OmegaStep = 0.01 # cm-1
    if OmegaWing == None:
        #OmegaWing = OmegaDelta/10.
        OmegaWing = 0.0 # cm-1
    if not Format:
        Infinitesimal = 1e-14 # put this to header in next version!
        min_number_of_digits = 4 # minimal number of digits after dec. pnt.
        last_digit_pos = 0
        while modf(OmegaStep * 10**last_digit_pos)[0] > Infinitesimal:
            last_digit_pos += 1
        actual_number_of_digits = max(min_number_of_digits,last_digit_pos)
        Format = '%%.%df %%e' % actual_number_of_digits
    return Components,SourceTables,Environment,OmegaRange,\
           OmegaStep,OmegaWing,IntensityThreshold,Format


# save numpy arrays to file
# arrays must have same dimensions
def save_to_file(fname,fformat,*arg):
    f = open(fname,'w')
    for i in range(len(arg[0])):
        argline = []
        for j in range(len(arg)):
            argline.append(arg[j][i])
        f.write((fformat+'\n') % tuple(argline))
    f.close()


# calculate apsorption for HT profile
def absorptionCoefficient_HT(Components=None,SourceTables=None,partitionFunction=PYTIPS,
                             Environment=None,OmegaRange=None,OmegaStep=None,OmegaWing=None,
                             IntensityThreshold=DefaultIntensityThreshold,
                             OmegaWingHW=DefaultOmegaWingHW,
                             ParameterBindings=DefaultParameterBindings,
                             EnvironmentDependencyBindings=DefaultEnvironmentDependencyBindings,
                             GammaL='gamma_air', HITRAN_units=True, LineShift=True,
                             File=None, Format=None, OmegaGrid=None):
    """
    INPUT PARAMETERS: 
        Components:  list of tuples [(M,I,D)], where
                        M - HITRAN molecule number,
                        I - HITRAN isotopologue number,
                        D - abundance (optional)
        SourceTables:  list of tables from which to calculate cross-section   (optional)
        partitionFunction:  pointer to partition function (default is PYTIPS) (optional)
        Environment:  dictionary containing thermodynamic parameters.
                        'p' - pressure in atmospheres,
                        'T' - temperature in Kelvin
                        Default={'p':1.,'T':296.}
        OmegaRange:  wavenumber range to consider.
        OmegaStep:   wavenumber step to consider. 
        OmegaWing:   absolute wing for calculating a lineshape (in cm-1) 
        IntensityThreshold:  threshold for intensities
        OmegaWingHW:  relative wing for calculating a lineshape (in halfwidths)
        GammaL:  specifies broadening parameter ('gamma_air' or 'gamma_self')
        HITRAN_units:  use cm2/molecule (True) or cm-1 (False) for absorption coefficient
        File:   write output to file (if specified)
        Format:  c-format of file output (accounts significant digits in OmegaStep)
    OUTPUT PARAMETERS: 
        Omegas: wavenumber grid with respect to parameters OmegaRange and OmegaStep
        Xsect: absorption coefficient calculated on the grid. 
               Units are switched by HITRAN_units 
    ---
    DESCRIPTION:
        Calculate absorption coefficient using HT (Hartmann-Tran) profile.
        Absorption coefficient is calculated at arbitrary temperature and pressure.
        User can vary a wide range of parameters to control a process of calculation
        (such as OmegaRange, OmegaStep, OmegaWing, OmegaWingHW, IntensityThreshold).
        The choice of these parameters depends on properties of a particular linelist.
        Default values are a sort of guess which gives a decent precicion (on average) 
        for a reasonable amount of cpu time. To increase calculation accuracy,
        user should use a trial and error method.
    ---
    EXAMPLE OF USAGE:
        nu,coef = absorptionCoefficient_HT(((2,1),),'co2',OmegaStep=0.01,
                                           HITRAN_units=False,GammaL='gamma_self')
    ---
    """

    # warn user about too large omega step
    if OmegaStep>0.1: warn('Too small omega step: possible accuracy decline')

    # "bug" with 1-element list
    Components = listOfTuples(Components)
    SourceTables = listOfTuples(SourceTables)
    
    # determine final input values
    Components,SourceTables,Environment,OmegaRange,OmegaStep,OmegaWing,\
    IntensityThreshold,Format = \
       getDefaultValuesForXsect(Components,SourceTables,Environment,OmegaRange,
                                OmegaStep,OmegaWing,IntensityThreshold,Format)
    
    # get uniform linespace for cross-section
    #number_of_points = (OmegaRange[1]-OmegaRange[0])/OmegaStep + 1
    #Omegas = linspace(OmegaRange[0],OmegaRange[1],number_of_points)
    if OmegaGrid is not None:
        Omegas = npsort(OmegaGrid)
    else:
        Omegas = arange(OmegaRange[0],OmegaRange[1],OmegaStep)
    number_of_points = len(Omegas)
    Xsect = zeros(number_of_points)
       
    # reference temperature and pressure
    Tref = __FloatType__(296.) # K
    pref = __FloatType__(1.) # atm
    
    # actual temperature and pressure
    T = Environment['T'] # K
    p = Environment['p'] # atm
       
    # create dictionary from Components
    ABUNDANCES = {}
    NATURAL_ABUNDANCES = {}
    for Component in Components:
        M = Component[0]
        I = Component[1]
        if len(Component) >= 3:
            ni = Component[2]
        else:
            try:
                ni = ISO[(M,I)][ISO_INDEX['abundance']]
            except KeyError:
                raise Exception('cannot find component M,I = %d,%d.' % (M,I))
        ABUNDANCES[(M,I)] = ni
        NATURAL_ABUNDANCES[(M,I)] = ISO[(M,I)][ISO_INDEX['abundance']]
        
    # precalculation of volume concentration
    if HITRAN_units:
        factor = __FloatType__(1.0)
    else:
        factor = volumeConcentration(p,T) 
        
    # SourceTables contain multiple tables
    for TableName in SourceTables:

        # get line centers
        nline = LOCAL_TABLE_CACHE[TableName]['header']['number_of_rows']
        
        # loop through line centers (single stream)
        for RowID in range(nline):
            
            # get basic line parameters (lower level)
            LineCenterDB = LOCAL_TABLE_CACHE[TableName]['data']['nu'][RowID]
            LineIntensityDB = LOCAL_TABLE_CACHE[TableName]['data']['sw'][RowID]
            LowerStateEnergyDB = LOCAL_TABLE_CACHE[TableName]['data']['elower'][RowID]
            MoleculeNumberDB = LOCAL_TABLE_CACHE[TableName]['data']['molec_id'][RowID]
            IsoNumberDB = LOCAL_TABLE_CACHE[TableName]['data']['local_iso_id'][RowID]
            #Gamma0DB = LOCAL_TABLE_CACHE[TableName]['data']['gamma_air'][RowID]
            #Gamma0DB = LOCAL_TABLE_CACHE[TableName]['data']['gamma_self'][RowID]
            Gamma0DB = LOCAL_TABLE_CACHE[TableName]['data'][GammaL][RowID]
            TempRatioPowerDB = LOCAL_TABLE_CACHE[TableName]['data']['n_air'][RowID]
            #TempRatioPowerDB = 1.0 # for planar molecules
            try:
                Gamma2DB = LOCAL_TABLE_CACHE[TableName]['data']['gamma2'][RowID]
            except:
                Gamma2DB = 0
            if LineShift:
                Shift0DB = LOCAL_TABLE_CACHE[TableName]['data']['delta_air'][RowID]
            else:
                Shift0DB = 0
            try:
                if LineShift:
                    Shift2DB = LOCAL_TABLE_CACHE[TableName]['data']['shift2'][RowID]
                else:
                    Shift2DB = 0
            except:
                Shift2DB = 0
            try:
                anuVCDB = LOCAL_TABLE_CACHE[TableName]['data']['anuVC'][RowID]
            except:
                anuVCDB = 0
            try:
                eta = LOCAL_TABLE_CACHE[TableName]['data']['eta'][RowID]
            except:
                eta = 0
            
            # filter by molecule and isotopologue
            if (MoleculeNumberDB,IsoNumberDB) not in ABUNDANCES: continue
            
            # partition functions for T and Tref
            # TODO: optimize
            SigmaT = partitionFunction(MoleculeNumberDB,IsoNumberDB,T)
            SigmaTref = partitionFunction(MoleculeNumberDB,IsoNumberDB,Tref)
            
            # get all environment dependences from voigt parameters
            
            #   intensity
            LineIntensity = EnvironmentDependency_Intensity(LineIntensityDB,T,Tref,SigmaT,SigmaTref,
                                                            LowerStateEnergyDB,LineCenterDB)
            
            #   FILTER by LineIntensity: compare it with IntencityThreshold
            # TODO: apply wing narrowing instead of filtering, this would be more appropriate
            if LineIntensity < IntensityThreshold: continue
            
            #   doppler broadening coefficient (GammaD)
            # V1 >>>
            #GammaDDB = cSqrtLn2*LineCenterDB/cc*sqrt(2*cBolts*T/molecularMass(MoleculeNumberDB,IsoNumberDB))
            #GammaD = EnvironmentDependency_GammaD(GammaDDB,T,Tref)
            # V2 >>>
            cMassMol = 1.66053873e-27 # hapi
            #cMassMol = 1.6605402e-27 # converter
            m = molecularMass(MoleculeNumberDB,IsoNumberDB) * cMassMol * 1000
            GammaD = sqrt(2*cBolts*T*log(2)/m/cc**2)*LineCenterDB

            #   lorentz broadening coefficient
            Gamma0 = EnvironmentDependency_Gamma0(Gamma0DB,T,Tref,p,pref,TempRatioPowerDB)
            
            #   quadratic speed dependence of lorentz broadening coefficient
            Gamma2 = Gamma2DB*p/pref*(Tref/T)**TempRatioPowerDB
            
            #   shift coefficient
            Shift0 = Shift0DB*p/pref
            
            #   quadratic speed dependence of shift coefficient
            Shift2 = Shift2DB*p/pref
            
            #   Dicke narrowing coefficient
            anuVC = anuVCDB*p/pref*Tref/T

            #   get final wing of the line according to Gamma0, OmegaWingHW and OmegaWing
            # XXX min or max?
            OmegaWingF = max(OmegaWing,OmegaWingHW*Gamma0,OmegaWingHW*GammaD)
                       
            #PROFILE_VOIGT(sg0,GamD,Gam0,sg)
            #      sg0           : Unperturbed line position in cm-1 (Input).
            #      GamD          : Doppler HWHM in cm-1 (Input)
            #      Gam0          : Speed-averaged line-width in cm-1 (Input).
            #      sg            : Current WaveNumber of the Computation in cm-1 (Input).
            
            # XXX time?
            BoundIndexLower = bisect(Omegas,LineCenterDB-OmegaWingF)
            BoundIndexUpper = bisect(Omegas,LineCenterDB+OmegaWingF)
            #lineshape_vals = PROFILE_HT(LineCenterDB,GammaD,Gamma0,Omegas[BoundIndexLower:BoundIndexUpper])[0]
            lineshape_vals = PROFILE_HT(LineCenterDB,GammaD,Gamma0,Gamma2,Shift0,Shift2,anuVC,eta,
                                        Omegas[BoundIndexLower:BoundIndexUpper])[0]
            Xsect[BoundIndexLower:BoundIndexUpper] += factor / NATURAL_ABUNDANCES[(MoleculeNumberDB,IsoNumberDB)] * \
                                                      ABUNDANCES[(MoleculeNumberDB,IsoNumberDB)] * \
                                                      LineIntensity * lineshape_vals
    
    if File: save_to_file(File,Format,Omegas,Xsect)
    return Omegas,Xsect

# calculate apsorption for Voigt profile
def absorptionCoefficient_Voigt(Components=None,SourceTables=None,partitionFunction=PYTIPS,
                                Environment=None,OmegaRange=None,OmegaStep=None,OmegaWing=None,
                                IntensityThreshold=DefaultIntensityThreshold,
                                OmegaWingHW=DefaultOmegaWingHW,
                                ParameterBindings=DefaultParameterBindings,
                                EnvironmentDependencyBindings=DefaultEnvironmentDependencyBindings,
                                GammaL='gamma_air', HITRAN_units=True, LineShift=True,
                                File=None, Format=None, OmegaGrid=None):   
    """
    INPUT PARAMETERS: 
        Components:  list of tuples [(M,I,D)], where
                        M - HITRAN molecule number,
                        I - HITRAN isotopologue number,
                        D - abundance (optional)
        SourceTables:  list of tables from which to calculate cross-section   (optional)
        partitionFunction:  pointer to partition function (default is PYTIPS) (optional)
        Environment:  dictionary containing thermodynamic parameters.
                        'p' - pressure in atmospheres,
                        'T' - temperature in Kelvin
                        Default={'p':1.,'T':296.}
        OmegaRange:  wavenumber range to consider.
        OmegaStep:   wavenumber step to consider. 
        OmegaWing:   absolute wing for calculating a lineshape (in cm-1) 
        IntensityThreshold:  threshold for intensities
        OmegaWingHW:  relative wing for calculating a lineshape (in halfwidths)
        GammaL:  specifies broadening parameter ('gamma_air' or 'gamma_self')
        HITRAN_units:  use cm2/molecule (True) or cm-1 (False) for absorption coefficient
        File:   write output to file (if specified)
        Format:  c-format of file output (accounts significant digits in OmegaStep)
    OUTPUT PARAMETERS: 
        Omegas: wavenumber grid with respect to parameters OmegaRange and OmegaStep
        Xsect: absorption coefficient calculated on the grid
    ---
    DESCRIPTION:
        Calculate absorption coefficient using Voigt profile.
        Absorption coefficient is calculated at arbitrary temperature and pressure.
        User can vary a wide range of parameters to control a process of calculation
        (such as OmegaRange, OmegaStep, OmegaWing, OmegaWingHW, IntensityThreshold).
        The choise of these parameters depends on properties of a particular linelist.
        Default values are a sort of guess which gives a decent precision (on average) 
        for a reasonable amount of cpu time. To increase calculation accuracy,
        user should use a trial and error method.
    ---
    EXAMPLE OF USAGE:
        nu,coef = absorptionCoefficient_Voigt(((2,1),),'co2',OmegaStep=0.01,
                                              HITRAN_units=False,GammaL='gamma_self')
    ---
    """

    # warn user about too large omega step
    if OmegaStep>0.1: warn('Too small omega step: possible accuracy decline')

    # "bug" with 1-element list
    Components = listOfTuples(Components)
    SourceTables = listOfTuples(SourceTables)
    
    # determine final input values
    Components,SourceTables,Environment,OmegaRange,OmegaStep,OmegaWing,\
    IntensityThreshold,Format = \
       getDefaultValuesForXsect(Components,SourceTables,Environment,OmegaRange,
                                OmegaStep,OmegaWing,IntensityThreshold,Format)
    
    # get uniform linespace for cross-section
    #number_of_points = (OmegaRange[1]-OmegaRange[0])/OmegaStep + 1
    #Omegas = linspace(OmegaRange[0],OmegaRange[1],number_of_points)
    if OmegaGrid is not None:
        Omegas = npsort(OmegaGrid)
    else:
        Omegas = arange(OmegaRange[0],OmegaRange[1],OmegaStep)
    number_of_points = len(Omegas)
    Xsect = zeros(number_of_points)
       
    # reference temperature and pressure
    Tref = __FloatType__(296.) # K
    pref = __FloatType__(1.) # atm
    
    # actual temperature and pressure
    T = Environment['T'] # K
    p = Environment['p'] # atm
       
    # create dictionary from Components
    ABUNDANCES = {}
    NATURAL_ABUNDANCES = {}
    for Component in Components:
        M = Component[0]
        I = Component[1]
        if len(Component) >= 3:
            ni = Component[2]
        else:
            try:
                ni = ISO[(M,I)][ISO_INDEX['abundance']]
            except KeyError:
                raise Exception('cannot find component M,I = %d,%d.' % (M,I))
        ABUNDANCES[(M,I)] = ni
        NATURAL_ABUNDANCES[(M,I)] = ISO[(M,I)][ISO_INDEX['abundance']]
        
    # precalculation of volume concentration
    if HITRAN_units:
        factor = __FloatType__(1.0)
    else:
        factor = volumeConcentration(p,T) 
        
    # SourceTables contain multiple tables
    for TableName in SourceTables:

        # get line centers
        nline = LOCAL_TABLE_CACHE[TableName]['header']['number_of_rows']
        
        # loop through line centers (single stream)
        for RowID in range(nline):
            
            # get basic line parameters (lower level)
            LineCenterDB = LOCAL_TABLE_CACHE[TableName]['data']['nu'][RowID]
            LineIntensityDB = LOCAL_TABLE_CACHE[TableName]['data']['sw'][RowID]
            LowerStateEnergyDB = LOCAL_TABLE_CACHE[TableName]['data']['elower'][RowID]
            MoleculeNumberDB = LOCAL_TABLE_CACHE[TableName]['data']['molec_id'][RowID]
            IsoNumberDB = LOCAL_TABLE_CACHE[TableName]['data']['local_iso_id'][RowID]
            #Gamma0DB = LOCAL_TABLE_CACHE[TableName]['data']['gamma_air'][RowID]
            #Gamma0DB = LOCAL_TABLE_CACHE[TableName]['data']['gamma_self'][RowID]
            Gamma0DB = LOCAL_TABLE_CACHE[TableName]['data'][GammaL][RowID]
            TempRatioPowerDB = LOCAL_TABLE_CACHE[TableName]['data']['n_air'][RowID]
            #TempRatioPowerDB = 1.0 # for planar molecules
            if LineShift:
                Shift0DB = LOCAL_TABLE_CACHE[TableName]['data']['delta_air'][RowID]
            else:
                Shift0DB = 0
            
            # filter by molecule and isotopologue
            if (MoleculeNumberDB,IsoNumberDB) not in ABUNDANCES: continue
            
            # partition functions for T and Tref
            # TODO: optimize
            SigmaT = partitionFunction(MoleculeNumberDB,IsoNumberDB,T)
            SigmaTref = partitionFunction(MoleculeNumberDB,IsoNumberDB,Tref)
            
            # get all environment dependences from voigt parameters
            
            #   intensity
            LineIntensity = EnvironmentDependency_Intensity(LineIntensityDB,T,Tref,SigmaT,SigmaTref,
                                                            LowerStateEnergyDB,LineCenterDB)
            
            #   FILTER by LineIntensity: compare it with IntencityThreshold
            # TODO: apply wing narrowing instead of filtering, this would be more appropriate
            if LineIntensity < IntensityThreshold: continue
            
            #   doppler broadening coefficient (GammaD)
            # V1 >>>
            #GammaDDB = cSqrtLn2*LineCenterDB/cc*sqrt(2*cBolts*T/molecularMass(MoleculeNumberDB,IsoNumberDB))
            #GammaD = EnvironmentDependency_GammaD(GammaDDB,T,Tref)
            # V2 >>>
            cMassMol = 1.66053873e-27 # hapi
            #cMassMol = 1.6605402e-27 # converter
            m = molecularMass(MoleculeNumberDB,IsoNumberDB) * cMassMol * 1000
            GammaD = sqrt(2*cBolts*T*log(2)/m/cc**2)*LineCenterDB
            
            #   lorentz broadening coefficient
            Gamma0 = EnvironmentDependency_Gamma0(Gamma0DB,T,Tref,p,pref,TempRatioPowerDB)
            
            #   get final wing of the line according to Gamma0, OmegaWingHW and OmegaWing
            # XXX min or max?
            OmegaWingF = max(OmegaWing,OmegaWingHW*Gamma0,OmegaWingHW*GammaD)

            #   shift coefficient
            Shift0 = Shift0DB*p/pref
            
            # XXX other parameter (such as Delta0, Delta2, anuVC etc.) will be included in HTP version
            
            #PROFILE_VOIGT(sg0,GamD,Gam0,sg)
            #      sg0           : Unperturbed line position in cm-1 (Input).
            #      GamD          : Doppler HWHM in cm-1 (Input)
            #      Gam0          : Speed-averaged line-width in cm-1 (Input).
            #      sg            : Current WaveNumber of the Computation in cm-1 (Input).
            
            # XXX time?
            BoundIndexLower = bisect(Omegas,LineCenterDB-OmegaWingF)
            BoundIndexUpper = bisect(Omegas,LineCenterDB+OmegaWingF)
            lineshape_vals = PROFILE_VOIGT(LineCenterDB+Shift0,GammaD,Gamma0,Omegas[BoundIndexLower:BoundIndexUpper])[0]
            Xsect[BoundIndexLower:BoundIndexUpper] += factor / NATURAL_ABUNDANCES[(MoleculeNumberDB,IsoNumberDB)] * \
                                                      ABUNDANCES[(MoleculeNumberDB,IsoNumberDB)] * \
                                                      LineIntensity * lineshape_vals
    
    if File: save_to_file(File,Format,Omegas,Xsect)
    return Omegas,Xsect


# calculate apsorption for Lorentz profile
def absorptionCoefficient_Lorentz(Components=None,SourceTables=None,partitionFunction=PYTIPS,
                                  Environment=None,OmegaRange=None,OmegaStep=None,OmegaWing=None,
                                  IntensityThreshold=DefaultIntensityThreshold,
                                  OmegaWingHW=DefaultOmegaWingHW,
                                  ParameterBindings=DefaultParameterBindings,
                                  EnvironmentDependencyBindings=DefaultEnvironmentDependencyBindings,
                                  GammaL='gamma_air', HITRAN_units=True, LineShift=True,
                                  File=None, Format=None, OmegaGrid=None):
    """
    INPUT PARAMETERS: 
        Components:  list of tuples [(M,I,D)], where
                        M - HITRAN molecule number,
                        I - HITRAN isotopologue number,
                        D - abundance (optional)
        SourceTables:  list of tables from which to calculate cross-section   (optional)
        partitionFunction:  pointer to partition function (default is PYTIPS) (optional)
        Environment:  dictionary containing thermodynamic parameters.
                        'p' - pressure in atmospheres,
                        'T' - temperature in Kelvin
                        Default={'p':1.,'T':296.}
        OmegaRange:  wavenumber range to consider.
        OmegaStep:   wavenumber step to consider. 
        OmegaWing:   absolute wing for calculating a lineshape (in cm-1) 
        IntensityThreshold:  threshold for intensities
        OmegaWingHW:  relative wing for calculating a lineshape (in halfwidths)
        GammaL:  specifies broadening parameter ('gamma_air' or 'gamma_self')
        HITRAN_units:  use cm2/molecule (True) or cm-1 (False) for absorption coefficient
        File:   write output to file (if specified)
        Format:  c-format of file output (accounts significant digits in OmegaStep)
    OUTPUT PARAMETERS: 
        Omegas: wavenumber grid with respect to parameters OmegaRange and OmegaStep
        Xsect: absorption coefficient calculated on the grid
    ---
    DESCRIPTION:
        Calculate absorption coefficient using Lorentz profile.
        Absorption coefficient is calculated at arbitrary temperature and pressure.
        User can vary a wide range of parameters to control a process of calculation
        (such as OmegaRange, OmegaStep, OmegaWing, OmegaWingHW, IntensityThreshold).
        The choise of these parameters depends on properties of a particular linelist.
        Default values are a sort of guess which gives a decent precision (on average) 
        for a reasonable amount of cpu time. To increase calculation accuracy,
        user should use a trial and error method.
    ---
    EXAMPLE OF USAGE:
        nu,coef = absorptionCoefficient_Lorentz(((2,1),),'co2',OmegaStep=0.01,
                                               HITRAN_units=False,GammaL='gamma_self')
    ---
    """

    # warn user about too large omega step
    if OmegaStep>0.1: warn('Too small omega step: possible accuracy decline')

    # "bug" with 1-element list
    Components = listOfTuples(Components)
    SourceTables = listOfTuples(SourceTables)
    
    # determine final input values
    Components,SourceTables,Environment,OmegaRange,OmegaStep,OmegaWing,\
    IntensityThreshold,Format = \
       getDefaultValuesForXsect(Components,SourceTables,Environment,OmegaRange,
                                OmegaStep,OmegaWing,IntensityThreshold,Format)
                
    # get uniform linespace for cross-section
    #number_of_points = (OmegaRange[1]-OmegaRange[0])/OmegaStep + 1
    #Omegas = linspace(OmegaRange[0],OmegaRange[1],number_of_points)
    if OmegaGrid is not None:
        Omegas = npsort(OmegaGrid)
    else:
        Omegas = arange(OmegaRange[0],OmegaRange[1],OmegaStep)
    number_of_points = len(Omegas)
    Xsect = zeros(number_of_points)
       
    # reference temperature and pressure
    Tref = __FloatType__(296.) # K
    pref = __FloatType__(1.) # atm
    
    # actual temperature and pressure
    T = Environment['T'] # K
    p = Environment['p'] # atm
       
    # create dictionary from Components
    ABUNDANCES = {}
    NATURAL_ABUNDANCES = {}
    for Component in Components:
        M = Component[0]
        I = Component[1]
        if len(Component) >= 3:
            ni = Component[2]
        else:
            try:
                ni = ISO[(M,I)][ISO_INDEX['abundance']]
            except KeyError:
                raise Exception('cannot find component M,I = %d,%d.' % (M,I))
        ABUNDANCES[(M,I)] = ni
        NATURAL_ABUNDANCES[(M,I)] = ISO[(M,I)][ISO_INDEX['abundance']]
        
    # precalculation of volume concentration
    if HITRAN_units:
        factor = __FloatType__(1.0)
    else:
        factor = volumeConcentration(p,T) 
        
    # SourceTables contain multiple tables
    for TableName in SourceTables:

        # get line centers
        nline = LOCAL_TABLE_CACHE[TableName]['header']['number_of_rows']
        
        # loop through line centers (single stream)
        for RowID in range(nline):
            
            # get basic line parameters (lower level)
            LineCenterDB = LOCAL_TABLE_CACHE[TableName]['data']['nu'][RowID]
            LineIntensityDB = LOCAL_TABLE_CACHE[TableName]['data']['sw'][RowID]
            LowerStateEnergyDB = LOCAL_TABLE_CACHE[TableName]['data']['elower'][RowID]
            MoleculeNumberDB = LOCAL_TABLE_CACHE[TableName]['data']['molec_id'][RowID]
            IsoNumberDB = LOCAL_TABLE_CACHE[TableName]['data']['local_iso_id'][RowID]
            #Gamma0DB = LOCAL_TABLE_CACHE[TableName]['data']['gamma_air'][RowID]
            #Gamma0DB = LOCAL_TABLE_CACHE[TableName]['data']['gamma_self'][RowID]
            Gamma0DB = LOCAL_TABLE_CACHE[TableName]['data'][GammaL][RowID]
            TempRatioPowerDB = LOCAL_TABLE_CACHE[TableName]['data']['n_air'][RowID]
            #TempRatioPowerDB = 1.0 # for planar molecules
            if LineShift:
                Shift0DB = LOCAL_TABLE_CACHE[TableName]['data']['delta_air'][RowID]
            else:
                Shift0DB = 0

                # filter by molecule and isotopologue
            if (MoleculeNumberDB,IsoNumberDB) not in ABUNDANCES: continue
            
            # partition functions for T and Tref
            # TODO: optimize
            SigmaT = partitionFunction(MoleculeNumberDB,IsoNumberDB,T)
            SigmaTref = partitionFunction(MoleculeNumberDB,IsoNumberDB,Tref)
            
            # get all environment dependences from voigt parameters
            
            #   intensity
            LineIntensity = EnvironmentDependency_Intensity(LineIntensityDB,T,Tref,SigmaT,SigmaTref,
                                                            LowerStateEnergyDB,LineCenterDB)
            
            #   FILTER by LineIntensity: compare it with IntencityThreshold
            # TODO: apply wing narrowing instead of filtering, this would be more appropriate
            if LineIntensity < IntensityThreshold: continue
                       
            #   lorentz broadening coefficient
            Gamma0 = EnvironmentDependency_Gamma0(Gamma0DB,T,Tref,p,pref,TempRatioPowerDB)
            
            #   get final wing of the line according to Gamma0, OmegaWingHW and OmegaWing
            # XXX min or max?
            OmegaWingF = max(OmegaWing,OmegaWingHW*Gamma0)

            #   shift coefficient
            Shift0 = Shift0DB*p/pref
                       
            # XXX other parameter (such as Delta0, Delta2, anuVC etc.) will be included in HTP version
            
            #PROFILE_VOIGT(sg0,GamD,Gam0,sg)
            #      sg0           : Unperturbed line position in cm-1 (Input).
            #      GamD          : Doppler HWHM in cm-1 (Input)
            #      Gam0          : Speed-averaged line-width in cm-1 (Input).
            #      sg            : Current WaveNumber of the Computation in cm-1 (Input).
            # XXX time?
            BoundIndexLower = bisect(Omegas,LineCenterDB-OmegaWingF)
            BoundIndexUpper = bisect(Omegas,LineCenterDB+OmegaWingF)
            lineshape_vals = PROFILE_LORENTZ(LineCenterDB+Shift0,Gamma0,Omegas[BoundIndexLower:BoundIndexUpper])
            Xsect[BoundIndexLower:BoundIndexUpper] += factor / NATURAL_ABUNDANCES[(MoleculeNumberDB,IsoNumberDB)] * \
                                                      ABUNDANCES[(MoleculeNumberDB,IsoNumberDB)] * \
                                                      LineIntensity * lineshape_vals
            
    if File: save_to_file(File,Format,Omegas,Xsect)
    return Omegas,Xsect


# calculate apsorption for Doppler profile
def absorptionCoefficient_Doppler(Components=None,SourceTables=None,partitionFunction=PYTIPS,
                                  Environment=None,OmegaRange=None,OmegaStep=None,OmegaWing=None,
                                  IntensityThreshold=DefaultIntensityThreshold,
                                  OmegaWingHW=DefaultOmegaWingHW,
                                  ParameterBindings=DefaultParameterBindings,
                                  EnvironmentDependencyBindings=DefaultEnvironmentDependencyBindings,
                                  GammaL='dummy', HITRAN_units=True, LineShift=True,
                                  File=None, Format=None, OmegaGrid=None):   
    """
    INPUT PARAMETERS: 
        Components:  list of tuples [(M,I,D)], where
                        M - HITRAN molecule number,
                        I - HITRAN isotopologue number,
                        D - abundance (optional)
        SourceTables:  list of tables from which to calculate cross-section   (optional)
        partitionFunction:  pointer to partition function (default is PYTIPS) (optional)
        Environment:  dictionary containing thermodynamic parameters.
                        'p' - pressure in atmospheres,
                        'T' - temperature in Kelvin
                        Default={'p':1.,'T':296.}
        OmegaRange:  wavenumber range to consider.
        OmegaStep:   wavenumber step to consider. 
        OmegaWing:   absolute wing for calculating a lineshape (in cm-1) 
        IntensityThreshold:  threshold for intensities
        OmegaWingHW:  relative wing for calculating a lineshape (in halfwidths)
        GammaL:  specifies broadening parameter ('gamma_air' or 'gamma_self')
        HITRAN_units:  use cm2/molecule (True) or cm-1 (False) for absorption coefficient
        File:   write output to file (if specified)
        Format:  c-format of file output (accounts significant digits in OmegaStep)
    OUTPUT PARAMETERS: 
        Omegas: wavenumber grid with respect to parameters OmegaRange and OmegaStep
        Xsect: absorption coefficient calculated on the grid
    ---
    DESCRIPTION:
        Calculate absorption coefficient using Doppler (Gauss) profile.
        Absorption coefficient is calculated at arbitrary temperature and pressure.
        User can vary a wide range of parameters to control a process of calculation
        (such as OmegaRange, OmegaStep, OmegaWing, OmegaWingHW, IntensityThreshold).
        The choise of these parameters depends on properties of a particular linelist.
        Default values are a sort of guess which give a decent precision (on average) 
        for a reasonable amount of cpu time. To increase calculation accuracy,
        user should use a trial and error method.
    ---
    EXAMPLE OF USAGE:
        nu,coef = absorptionCoefficient_Doppler(((2,1),),'co2',OmegaStep=0.01,
                                              HITRAN_units=False,GammaL='gamma_self')
    ---
    """

    # warn user about too large omega step
    if OmegaStep>0.005: warn('Too small omega step: possible accuracy decline')

    # "bug" with 1-element list
    Components = listOfTuples(Components)
    SourceTables = listOfTuples(SourceTables)
    
    # determine final input values
    Components,SourceTables,Environment,OmegaRange,OmegaStep,OmegaWing,\
    IntensityThreshold,Format = \
       getDefaultValuesForXsect(Components,SourceTables,Environment,OmegaRange,
                                OmegaStep,OmegaWing,IntensityThreshold,Format)
    # special for Doppler case: set OmegaStep to a smaller value
    if not OmegaStep: OmegaStep = 0.001
                
    # get uniform linespace for cross-section
    #number_of_points = (OmegaRange[1]-OmegaRange[0])/OmegaStep + 1
    #Omegas = linspace(OmegaRange[0],OmegaRange[1],number_of_points)
    if OmegaGrid is not None:
        Omegas = npsort(OmegaGrid)
    else:
        Omegas = arange(OmegaRange[0],OmegaRange[1],OmegaStep)
    number_of_points = len(Omegas)
    Xsect = zeros(number_of_points)
       
    # reference temperature and pressure
    Tref = __FloatType__(296.) # K
    pref = __FloatType__(1.) # atm
    
    # actual temperature and pressure
    T = Environment['T'] # K
    p = Environment['p'] # atm
       
    # create dictionary from Components
    ABUNDANCES = {}
    NATURAL_ABUNDANCES = {}
    for Component in Components:
        M = Component[0]
        I = Component[1]
        if len(Component) >= 3:
            ni = Component[2]
        else:
            try:
                ni = ISO[(M,I)][ISO_INDEX['abundance']]
            except KeyError:
                raise Exception('cannot find component M,I = %d,%d.' % (M,I))
        ABUNDANCES[(M,I)] = ni
        NATURAL_ABUNDANCES[(M,I)] = ISO[(M,I)][ISO_INDEX['abundance']]
        
    # precalculation of volume concentration
    if HITRAN_units:
        factor = __FloatType__(1.0)
    else:
        factor = volumeConcentration(p,T) 
        
    # SourceTables contain multiple tables
    for TableName in SourceTables:

        # get line centers
        nline = LOCAL_TABLE_CACHE[TableName]['header']['number_of_rows']
        
        # loop through line centers (single stream)
        for RowID in range(nline):
            
            # get basic line parameters (lower level)
            LineCenterDB = LOCAL_TABLE_CACHE[TableName]['data']['nu'][RowID]
            LineIntensityDB = LOCAL_TABLE_CACHE[TableName]['data']['sw'][RowID]
            LowerStateEnergyDB = LOCAL_TABLE_CACHE[TableName]['data']['elower'][RowID]
            MoleculeNumberDB = LOCAL_TABLE_CACHE[TableName]['data']['molec_id'][RowID]
            IsoNumberDB = LOCAL_TABLE_CACHE[TableName]['data']['local_iso_id'][RowID]
            if LineShift:
                Shift0DB = LOCAL_TABLE_CACHE[TableName]['data']['delta_air'][RowID]
            else:
                Shift0DB = 0
            
            # filter by molecule and isotopologue
            if (MoleculeNumberDB,IsoNumberDB) not in ABUNDANCES: continue
            
            # partition functions for T and Tref
            # TODO: optimize
            SigmaT = partitionFunction(MoleculeNumberDB,IsoNumberDB,T)
            SigmaTref = partitionFunction(MoleculeNumberDB,IsoNumberDB,Tref)
            
            # get all environment dependences from voigt parameters
            
            #   intensity
            LineIntensity = EnvironmentDependency_Intensity(LineIntensityDB,T,Tref,SigmaT,SigmaTref,
                                                            LowerStateEnergyDB,LineCenterDB)
            
            #   FILTER by LineIntensity: compare it with IntencityThreshold
            # TODO: apply wing narrowing instead of filtering, this would be more appropriate
            if LineIntensity < IntensityThreshold: continue
            
            #   doppler broadening coefficient (GammaD)
            #GammaDDB = cSqrtLn2*LineCenterDB/cc*sqrt(2*cBolts*T/molecularMass(MoleculeNumberDB,IsoNumberDB))
            #GammaD = EnvironmentDependency_GammaD(GammaDDB,T,Tref)
            #print(GammaD)

            cMassMol = 1.66053873e-27
            #cSqrt2Ln2 = 1.1774100225
            fSqrtMass = sqrt(molecularMass(MoleculeNumberDB,IsoNumberDB))
            #fSqrtMass = sqrt(32831.2508809)
            cc_ = 2.99792458e8
            cBolts_ = 1.3806503e-23
            #cBolts_ = 1.3806488E-23
            GammaD = (cSqrt2Ln2/cc_)*sqrt(cBolts_/cMassMol)*sqrt(T) * LineCenterDB/fSqrtMass
            
            #GammaD = 4.30140e-7*LineCenterDB*sqrt(T/molecularMass(MoleculeNumberDB,IsoNumberDB))

            #cc_ = 2.99792458e8 # 2.99792458e10 # 2.99792458e8
            #cBolts_ = 1.3806503e-23 #1.3806488E-16 # 1.380648813E-16 # 1.3806503e-23 # 1.3806488E-23
            #GammaD = sqrt(log(2))*LineCenterDB*sqrt(2*cBolts_*T/(cMassMol*molecularMass(MoleculeNumberDB,IsoNumberDB)*cc_**2))
            #print(GammaD)
            
            #   get final wing of the line according to GammaD, OmegaWingHW and OmegaWing
            # XXX min or max?
            OmegaWingF = max(OmegaWing,OmegaWingHW*GammaD)

            #   shift coefficient
            Shift0 = Shift0DB*p/pref

            # XXX other parameter (such as Delta0, Delta2, anuVC etc.) will be included in HTP version
            
            #PROFILE_VOIGT(sg0,GamD,Gam0,sg)
            #      sg0           : Unperturbed line position in cm-1 (Input).
            #      GamD          : Doppler HWHM in cm-1 (Input)
            #      Gam0          : Speed-averaged line-width in cm-1 (Input).
            #      sg            : Current WaveNumber of the Computation in cm-1 (Input).
                                              
            # XXX time?
            BoundIndexLower = bisect(Omegas,LineCenterDB-OmegaWingF)
            BoundIndexUpper = bisect(Omegas,LineCenterDB+OmegaWingF)
            lineshape_vals = PROFILE_DOPPLER(LineCenterDB+Shift0,GammaD,Omegas[BoundIndexLower:BoundIndexUpper])
            #lineshape_vals = PROFILE_VOIGT(LineCenterDB,GammaD,cZero,Omegas[BoundIndexLower:BoundIndexUpper])[0]
            #Xsect[BoundIndexLower:BoundIndexUpper] += lineshape_vals # DEBUG
            Xsect[BoundIndexLower:BoundIndexUpper] += factor / NATURAL_ABUNDANCES[(MoleculeNumberDB,IsoNumberDB)] * \
                                                      ABUNDANCES[(MoleculeNumberDB,IsoNumberDB)] * \
                                                      LineIntensity * lineshape_vals

    if File: save_to_file(File,Format,Omegas,Xsect)
    return Omegas,Xsect

# ---------------------------------------------------------------------------
# SHORTCUTS AND ALIASES FOR ABSORPTION COEFFICIENTS
# ---------------------------------------------------------------------------


def abscoef_HT(table=None,step=None,grid=None,env={'T':296.,'p':1.},file=None):
    return absorptionCoefficient_HT(SourceTables=table,OmegaStep=step,OmegaGrid=grid,Environment=env,File=file)

def abscoef_Voigt(table=None,step=None,grid=None,env={'T':296.,'p':1.},file=None):
    return absorptionCoefficient_Voigt(SourceTables=table,OmegaStep=step,OmegaGrid=grid,Environment=env,File=file)
    
def abscoef_Lorentz(table=None,step=None,grid=None,env={'T':296.,'p':1.},file=None):
    return absorptionCoefficient_Lorentz(SourceTables=table,OmegaStep=step,OmegaGrid=grid,Environment=env,File=file)

def abscoef_Doppler(table=None,step=None,grid=None,env={'T':296.,'p':1.},file=None):
    return absorptionCoefficient_Doppler(SourceTables=table,OmegaStep=step,OmegaGrid=grid,Environment=env,File=file)

abscoef_Gauss = abscoef_Doppler
    
def abscoef(table=None,step=None,grid=None,env={'T':296.,'p':1.},file=None): # default
    return absorptionCoefficient_Lorentz(SourceTables=table,OmegaStep=step,OmegaGrid=grid,Environment=env,File=file)
    
# ---------------------------------------------------------------------------
    
def transmittanceSpectrum(Omegas,AbsorptionCoefficient,Environment={'l':100.},
                          File=None, Format='%e %e'):
    """
    INPUT PARAMETERS: 
        Omegas:       wavenumber grid                           (required)
        AbsorptionCoefficient:  absorption coefficient on grid  (required)
        Environment:  dictionary containing path length in cm.
                      Default={'l':100.}
        File:         name of the output file                 (optional) 
        Format: c format used in file output, default '%e %e' (optional)
    OUTPUT PARAMETERS: 
        Omegas: wavenumber grid
        Xsect:  transmittance spectrum calculated on the grid
    ---
    DESCRIPTION:
        Calculate a transmittance spectrum (dimensionless) based
        on previously calculated absorption coefficient.
        Transmittance spectrum is calculated at an arbitrary
        optical path length 'l' (1 m by default)
    ---
    EXAMPLE OF USAGE:
        nu,trans = transmittanceSpectrum(nu,coef)
    ---
    """
    l = Environment['l']
    Xsect = exp(-AbsorptionCoefficient*l)
    if File: save_to_file(File,Format,Omegas,Xsect)
    return Omegas,Xsect

def absorptionSpectrum(Omegas,AbsorptionCoefficient,Environment={'l':100.},
                       File=None, Format='%e %e'):
    """
    INPUT PARAMETERS: 
        Omegas:       wavenumber grid                           (required)
        AbsorptionCoefficient:  absorption coefficient on grid  (required)
        Environment:  dictionary containing path length in cm.
                      Default={'l':100.}
        File:         name of the output file                 (optional) 
        Format: c format used in file output, default '%e %e' (optional)
    OUTPUT PARAMETERS: 
        Omegas: wavenumber grid
        Xsect:  transmittance spectrum calculated on the grid
    ---
    DESCRIPTION:
        Calculate an absorption spectrum (dimensionless) based
        on previously calculated absorption coefficient.
        Absorption spectrum is calculated at an arbitrary
        optical path length 'l' (1 m by default)
    ---
    EXAMPLE OF USAGE:
        nu,absorp = absorptionSpectrum(nu,coef)
    ---
    """
    l = Environment['l']
    Xsect = 1-exp(-AbsorptionCoefficient*l)
    if File: save_to_file(File,Format,Omegas,Xsect)
    return Omegas,Xsect

def radianceSpectrum(Omegas,AbsorptionCoefficient,Environment={'l':100.,'T':296.},
                     File=None, Format='%e %e'):
    """
    INPUT PARAMETERS: 
        Omegas:       wavenumber grid                          (required)
        AbsorptionCoefficient:  absorption coefficient on grid (required)
        Environment:  dictionary containing path length in cm.
                      and temperature in Kelvin.
                      Default={'l':100.,'T':296.}
        File:         name of the output file                 (optional) 
        Format: c format used in file output, default '%e %e' (optional)
    OUTPUT PARAMETERS: 
        Omegas: wavenumber grid
        Xsect:  radiance spectrum calculated on the grid
    ---
    DESCRIPTION:
        Calculate a radiance spectrum (in W/sr/cm^2/cm-1) based
        on previously calculated absorption coefficient.
        Radiance spectrum is calculated at an arbitrary
        optical path length 'l' (1 m by default) and 
        temperature 'T' (296 K by default). For obtaining a
        physically meaningful result 'T' must be the same 
        as a temperature which was used in absorption coefficient.
    ---
    EXAMPLE OF USAGE:
        nu,radi = radianceSpectrum(nu,coef)
    ---
    """
    l = Environment['l']
    T = Environment['T']
    Alw = 1-exp(-AbsorptionCoefficient*l)
    LBBTw = 2*hh*cc**2*Omegas**3 / (exp(hh*cc*Omegas/(cBolts*T)) - 1) * 1.0E-7
    Xsect = Alw*LBBTw # W/sr/cm**2/cm**-1
    if File: save_to_file(File,Format,Omegas,Xsect)
    return Omegas,Xsect


# GET X,Y FOR FINE PLOTTING OF A STICK SPECTRUM
def getStickXY(TableName):
    """
    Get X and Y for fine plotting of a stick spectrum.
    Usage: X,Y = getStickXY(TableName).
    """
    cent,intens = getColumns(TableName,('nu','sw'))
    n = len(cent)
    cent_ = zeros(n*3)
    intens_ = zeros(n*3)
    for i in range(n):
        intens_[3*i] = 0
        intens_[3*i+1] = intens[i]
        intens_[3*i+2] = 0
        cent_[(3*i):(3*i+3)] = cent[i]
    return cent_,intens_
# /GET X,Y FOR FINE PLOTTING OF A STICK SPECTRUM


# LOW-RES SPECTRA (CONVOLUTION WITH APPARATUS FUNCTION)

# /LOW-RES SPECTRA (CONVOLUTION WITH APPARATUS FUNCTION)

# /----------------------------------------------------------------------------


# ------------------  HITRAN-ON-THE-WEB COMPATIBILITY -------------------------

def read_hotw(filename):
    """
    Read cross-section file fetched from HITRAN-on-the-Web.
    The format of the file line must be as follows: 
      nu, coef
    Other lines are omitted.
    """
    import sys
    f = open(filename,'r')
    nu = []
    coef = []
    for line in f:
        pars = line.split()
        try:
            nu.append(float(pars[0]))
            coef.append(float(pars[1]))
        except:
            if False:
                print(sys.exc_info())
            else:
                pass    
    return array(nu),array(coef)

# alias for read_hotw for backwards compatibility
read_xsect = read_hotw
    
# /----------------------------------------------------------------------------

# ------------------  SPECTRAL CONVOLUTION -------------------------

# rectangular slit function
def SLIT_RECTANGULAR(x,g):
    """
    Instrumental (slit) function.
    B(x) = 1/γ , if |x| ≤ γ/2 & B(x) = 0, if |x| > γ/2,
    where γ is a slit width or the instrumental resolution.
    """
    index_inner = abs(x) <= g/2
    index_outer = ~index_inner
    y = zeros(len(x))
    y[index_inner] = 1/g
    y[index_outer] = 0
    return y

# triangular slit function
def SLIT_TRIANGULAR(x,g):
    """
    Instrumental (slit) function.
    B(x) = 1/γ*(1-|x|/γ), if |x| ≤ γ & B(x) = 0, if |x| > γ,
    where γ is the line width equal to the half base of the triangle.
    """
    index_inner = abs(x) <= g
    index_outer = ~index_inner
    y = zeros(len(x))
    y[index_inner] = 1/g * (1 - abs(x[index_inner])/g)
    y[index_outer] = 0
    return y

# gaussian slit function
def SLIT_GAUSSIAN(x,g):
    """
    Instrumental (slit) function.
    B(x) = sqrt(ln(2)/pi)/γ*exp(-ln(2)*(x/γ)**2),
    where γ/2 is a gaussian half-width at half-maximum.
    """
    g /= 2
    return sqrt(log(2))/(sqrt(pi)*g)*exp(-log(2)*(x/g)**2)

# dispersion slit function
def SLIT_DISPERSION(x,g):
    """
    Instrumental (slit) function.
    B(x) = γ/pi/(x**2+γ**2),
    where γ/2 is a lorentzian half-width at half-maximum.
    """
    g /= 2
    return g/pi/(x**2+g**2)

# cosinus slit function
def SLIT_COSINUS(x,g):
    return (cos(pi/g*x)+1)/(2*g)

# diffraction slit function
def SLIT_DIFFRACTION(x,g):
    """
    Instrumental (slit) function.
    """
    y = zeros(len(x))
    index_zero = x==0
    index_nonzero = ~index_zero
    dk_ = pi/g
    x_ = dk_*x[index_nonzero]
    w_ = sin(x_)
    r_ = w_**2/x_**2
    y[index_zero] = 1
    y[index_nonzero] = r_/g
    return y

# apparatus function of the ideal Michelson interferometer
def SLIT_MICHELSON(x,g):
    """
    Instrumental (slit) function.
    B(x) = 2/γ*sin(2pi*x/γ)/(2pi*x/γ) if x!=0 else 1,
    where 1/γ is the maximum optical path difference.
    """
    y = zeros(len(x))
    index_zero = x==0
    index_nonzero = ~index_zero
    dk_ = 2*pi/g
    x_ = dk_*x[index_nonzero]
    y[index_zero] = 1
    y[index_nonzero] = 2/g*sin(x_)/x_
    return y

# spectral convolution with an apparatus (slit) function
def convolveSpectrum(Omega,CrossSection,Resolution=0.1,AF_wing=10.,SlitFunction=SLIT_RECTANGULAR):
    """
    INPUT PARAMETERS: 
        Omega:         wavenumber grid                           (required)
        CrossSection:  high-res cross section calculated on grid (required)
        Resolution:    instrumental resolution γ                 (optional)
        AF_wing:       instrumental function wing                (optional)
        SlitFunction:  instrumental function for low-res spectra calculation (optional)
    OUTPUT PARAMETERS: 
        Omega: wavenumber grid
        CrossSection: low-res cross section calculated on grid
        i1: lower index in Omega input
        i2: higher index in Omega input
        slit: slit function calculated over grid [-AF_wing; AF_wing]
                with the step equal to instrumental resolution. 
    ---
    DESCRIPTION:
        Produce a simulation of experimental spectrum via the convolution 
        of a “dry” spectrum with an instrumental function.
        Instrumental function is provided as a parameter and
        is calculated in a grid with the width=AF_wing and step=Resolution.
    ---
    EXAMPLE OF USAGE:
        nu_,radi_,i,j,slit = convolveSpectrum(nu,radi,Resolution=2.0,AF_wing=10.0,
                                                SlitFunction=SLIT_MICHELSON)
    ---
    """
    step = Omega[1]-Omega[0]
    if step>=Resolution: raise Exception('step must be less than resolution')
    x = arange(-AF_wing,AF_wing+step,step)
    slit = SlitFunction(x,Resolution)
    # FIXING THE BUG: normalize slit function
    slit /= sum(slit)*step # simple normalization
    left_bnd = len(slit)/2
    right_bnd = len(Omega) - len(slit)/2
    #CrossSectionLowRes = convolve(CrossSection,slit,mode='valid')*step
    CrossSectionLowRes = convolve(CrossSection,slit,mode='same')*step
    #return Omega[left_bnd:right_bnd],CrossSectionLowRes,left_bnd,right_bnd,slit
    return Omega[left_bnd:right_bnd],CrossSectionLowRes[left_bnd:right_bnd],left_bnd,right_bnd,slit

# DEBUG
# spectral convolution with an apparatus (slit) function
def convolveSpectrumSame(Omega,CrossSection,Resolution=0.1,AF_wing=10.,SlitFunction=SLIT_RECTANGULAR):
    """
    Convolves cross section with a slit function with given parameters.
    """
    step = Omega[1]-Omega[0]
    x = arange(-AF_wing,AF_wing+step,step)
    slit = SlitFunction(x,Resolution)
    print('step=')
    print(step)
    print('x=')
    print(x)
    print('slitfunc=')
    print(SlitFunction)
    CrossSectionLowRes = convolve(CrossSection,slit,mode='same')*step
    return Omega,CrossSectionLowRes,None,None,slit

# DEBUG
def convolveSpectrumFull(Omega,CrossSection,Resolution=0.1,AF_wing=10.,SlitFunction=SLIT_RECTANGULAR):
    """
    Convolves cross section with a slit function with given parameters.
    """
    step = Omega[1]-Omega[0]
    x = arange(-AF_wing,AF_wing+step,step)
    slit = SlitFunction(x,Resolution)
    print('step=')
    print(step)
    print('x=')
    print(x)
    print('slitfunc=')
    print(SlitFunction)
    CrossSectionLowRes = convolve(CrossSection,slit,mode='full')*step
    return Omega,CrossSectionLowRes,None,None

# ------------------------------------------------------------------