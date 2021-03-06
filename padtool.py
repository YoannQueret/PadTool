#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright (C) 2020
# Fabien Cuny, fabien.cuny7 at orange.fr
# http://www.github.com/fabcd14/PadTool

# This file is part of PadTool.
# PadTool is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
# PadTool is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with PadTool.  If not, see <http://www.gnu.org/licenses/>.

version = "v0.9.4"

# Import system libraries

import configparser
from selenium import webdriver
import selenium
import re
import subprocess
import platform
import time
import sys
import getopt
import os
import threading

from urllib.request import *

from misc import str_tools
from plugins import _pluginsManagement

def header():
    print ("PadTool " + version + " - MOT SLS and DLS generator for PAD encoder")
    print (" By Fabien Cuny (fabcd14) - DAB Radio Normandie")
    print (" ")
    print (" Reads json / xml / txt / html data from a specific file, and outputs DLS+ text")
    print (" from these informations and generates SLS with personnalized templates")
    print (" https://github.com/fabcd14")
    print (" ")
    print ("-------------------------------------------------------------------------------")
    print (" ")

def main(argv):
    header()

    inputFile = ''
    try:
        opts, args = getopt.getopt(argv,"c:",["config="])
    except getopt.GetoptError:
        print ('padtool.py -c <configfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('padtool.py -c <configfile>')
            sys.exit()
        elif opt in ("-c", "--config"):
            inputFile = arg
    
    if(inputFile == ""):
        print ('Using local config.ini file')
        inputFile = "config.ini"
    else:
        print ('Using config file : "' + inputFile + '"')

    try:
        with open(inputFile): pass
    except IOError:
        print ('The file "' +  inputFile + '" has not been found !')
        sys.exit(2)

    # Config file parsing
    cfg = configparser.ConfigParser()
    cfg.read(inputFile, encoding='utf-8')
    try:
        mode = cfg.get('general', 'mode')
        outFolder = cfg.get('general', 'outFolder')
        radioName = cfg.get('general', 'radioName')
        slogan = cfg.get('general', 'slogan')
    except configparser.NoOptionError as error:
        print("Mandatory parameter is missing : " + str(error))
        sys.exit(2)

    if (mode == 'standalone'):
        try:
            timer = cfg.get('general', 'timer')
            print ("Standalone Mode, timer period set to: " + timer + "s")
        except configparser.NoOptionError as error:
            print("Mandatory parameter is missing: " + str(error))
            sys.exit(2)
    elif (mode == 'server'):
        print ("Server mode, not implemented yet :(")
    elif (mode == 'dabctl'):
        print ("DAB-CTL mode, timer period overriden to: 15s")
        timer = 15
    else:
        print("Parameter 'mode' not recognized. Only the options 'standalone', 'server' or 'dabctl' are supported")
        sys.exit(2)

    # For Proxy
    if (cfg.get('proxy', 'enabled') == "1"):   
        proxy_handler = ProxyHandler({'http': cfg.get('proxy', 'http'), 'https': cfg.get('proxy', 'https')})
        opener = build_opener(proxy_handler)
        install_opener(opener)

    # Generate slides with logo first if enabled
    try:
        _pluginsManagement.initPlugins(inputFile, cfg, mode, timer)
    except configparser.NoOptionError as error:
        print("Mandatory parameter is missing : " + str(error))
        sys.exit(2)

if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        print('Ctrl+C received : PadTool exits...')
        try:
            sys.exit(0)
            driver = None
        except SystemExit:
            os._exit(0)
            driver = None
    except Exception as ex:
        try:
            print ("Error : " + str(ex))
            sys.exit(0)
        except SystemExit:
            os._exit(0)
