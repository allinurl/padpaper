#!/bin/sh
# Install script for PadPaper

echo Checking for dependencies...
echo
PYTHON=`which python`
if [ $PYTHON ]; then
	echo "Python found at: $PYTHON    OK"
else
	echo "Python not found!"
	exit 1
fi
echo
python -c "from Tkinter import *"
Tk=$?
if [ $Tk -eq 0 ]; then
	echo "Tkinter module found.                  OK"
    #(sip found at: $Tk)"
else
	echo "Tkinter module not found!"
	exit 1
fi

echo
echo Changing to root to install files

su -c "mkdir -p /usr/share/PadPaper-EDITOR-1.02/ && cp *.py *.gif README COPYING AUTHORS /usr/share/PadPaper-EDITOR-1.02/ && chmod a+x /usr/share/PadPaper-EDITOR-1.02/PadPaper.py && ln -sf /usr/share/PadPaper-EDITOR-1.02/PadPaper.py /usr/bin/PadPaper"

echo
echo PadPaper Editor v1.02 the OpenSource Text editor system
echo 2003 Pro Soft Gerardo Orellana
echo This program is free software you can redistribute it and
echo as published by the Free Software Foundation version 1
echo of the License, or at your option any later version
echo
echo Contact Information:
echo Gerardo Orellana
echo Pro Soft
echo EMail: hello@goaccess.io 
echo
echo Created in Python 2.3 with Tkinter module
echo 2003
echo 
echo To run PadPaper Editor 1.02 type PadPaper
echo

