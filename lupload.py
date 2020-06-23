#! /usr/bin/python3
#
# @(!--#) @(#) lupload.py, version 006, 23-june-2020
#
# copy a Lua script to a Raritan intelligent PDU
#

############################################################################

import sys
import os
import argparse

import raritan.rpc
import raritan.rpc.luaservice

############################################################################

DEFAULT_USERNAME          = 'admin'
DEFAULT_UPASS             = 'UPASS'
DEFAULT_TIMEOUT           = 10

DEFINE_AUTOSTART          = 'autoStart:=yes'
DEFINE_AUTORESTART        = 'autoRestart:=yes'

############################################################################

def errortext(errornumber):
    if errornumber == 0:
        msg = 'NO_ERROR'
    elif errornumber == 1:
        msg = 'ERR_INVALID_NAME'
    elif errornumber == 2:
        msg = 'ERR_NO_SUCH_SCRIPT'
    elif errornumber == 3:
        msg = 'ERR_MAX_SCRIPT_NUMBERS_EXCEEDED'
    elif errornumber == 4:
        msg = 'ERR_MAX_SCRIPT_SIZE_EXCEEDED'
    elif errornumber == 5:
        msg = 'ERR_MAX_ALL_SCRIPT_SIZE_EXCEEDED'
    elif errornumber == 6:
        msg = 'ERR_NOT_TERMINATED'
    elif errornumber == 7:
        msg = 'ERR_NOT_RUNNING'
    elif errornumber == 8:
        msg = 'ERR_INVALID_ADDR'
    elif errornumber == 10:
        msg = 'ERR_TOO_MANY_ARGUMENTS'
    elif errornumber == 11:
        msg = 'ERR_ARGUMENT_NOT_VALID'
    else:
        msg = 'UNKNOWN_ERROR_CODE_{}'.format(errornumber)
    
    return msg

############################################################################

def validscriptname(scriptname):
    validflag = False
    
    if scriptname == '':
        return False
        
    if not (scriptname[0].isalpha()):
        return False
        
    for c in scriptname[1:]:
        if (c != '-') and (c != '_') and (not (c.isalnum())):
            return False
    
    return True

############################################################################

def basename(filename, suffixlist):
    for suffix in suffixlist:
        if filename.lower().endswith('.' + suffix):
            return filename[:-(len(suffix)+1)]
    
    return filename
            
############################################################################

def extractstartrestart(filename):
    global progname
    
    try:
        fh = open(filename, 'r', encoding='utf-8')
    except FileNotFoundError:
        print('{}: cannot open file "{}" for reading'.format(progname, filename), file=sys.stderr)
        sys.exit(1)
    
    start = False
    restart = False
    
    for line in fh:
        line = line.rstrip()
        
        if len(line) == 0:
            continue
        
        if line[0:2] != '--':
            break
            
        words = line.split()
        
        if len(words) == 2:
            if words[1] == DEFINE_AUTOSTART:
                start = True
            elif words[1] == DEFINE_AUTORESTART:
                restart = True
                
    fh.close()
    
    return start, restart

############################################################################

def main():
    global progname
    
    parser = argparse.ArgumentParser()

    parser.add_argument('--user',     help='username to login as', default=DEFAULT_USERNAME)
    parser.add_argument('--upass',    help='environment variable with user password', default=DEFAULT_UPASS)
    parser.add_argument('--timeout',  help='communication timeout', default=DEFAULT_TIMEOUT, type=int)
    parser.add_argument('pduname',    help='name or IP address of PDU to copy the script to', nargs=1)
    parser.add_argument('script',     help='script to upload', nargs=1)
        
    args = parser.parse_args()
    
    user = args.user

    try:
        password = os.environ[args.upass]
    except KeyError:
        print('{}: password environment variable "{}" is not defined'.format(progname, args.upass), file=sys.stderr)
        sys.exit(1)
        
    script = args.script[0]
    
    pduname = args.pduname[0]
    
    timeout = args.timeout
    
    if (not script.endswith('.lua')) and (not script.endswith('.LUA')):
        print('{}: script name "{}" does not have a .lua or .LUA suffix'.format(progname, script), file=sys.stderr)
        sys.exit(1)
    
    if len(script) < 5:    
        print('{}: script name "{}" is too short'.format(progname, script), file=sys.stderr)
        sys.exit(1)
    
    basescript = script[:-4]
    
    if not validscriptname(basescript):
        print('{}: script name "{}" contains invalid characters'.format(progname, script), file=sys.stderr)
        sys.exit(1)
    
    agent = raritan.rpc.Agent('https', pduname, user, password, disable_certificate_verification=True, timeout=timeout)

    luaservice_proxy = raritan.rpc.luaservice.Manager('/luaservice', agent)    

    snames = luaservice_proxy.getScriptNames()    

    try:
        scriptfh = open(script, 'r', encoding='utf=8')
    except FileNotFoundError:
        print('{}: cannot open script file "{}" for reading'.format(progname, script), file=sys.stderr)
        sys.exit(1)
        
    scriptcontent = scriptfh.read()
        
    scriptfh.close()
    
    autoStart, autoRestart = extractstartrestart(script)
    
    ### print(autoStart, autoRestart)
        
    scriptoptions = raritan.rpc.luaservice.ScriptOptions(
                  defaultArgs = {},
                  autoStart = autoStart,
                  autoRestart = autoRestart
              )
    
    rc = luaservice_proxy.setScript(basescript, scriptcontent, scriptoptions)
    
    if rc == 0:
        print('Upload of Lua script "{}" to PDU {} successful'.format(basescript, pduname))
    else:
        print('{}: upload failed with error code {} - {}'.format(progname, rc, errortext(rc)), file=sys.stderr)
        sys.exit(1)

    return 0

############################################################################

progname = os.path.basename(sys.argv[0])

sys.exit(main())
     
# end of file
