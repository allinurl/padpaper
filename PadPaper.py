#!/usr/bin/python

# PadPaper Editor v1.02 - the OpenSource Text editor system
# Copyright (C) 2003 Pro Soft Gerardo Orellana

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; version 1
# of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA  02111-1307, USA.

# Contact information:
# Gerardo Orellana
# Pro Soft
# EMail: hello@goaccess.io 


Version = '1.02'

from Tkinter import *
from tkFileDialog   import *               
from tkMessageBox   import *
from tkSimpleDialog import *
from tkColorChooser import askcolor

import tkMessageBox
import tkSimpleDialog
import tkFileDialog
import Tkinter
import os
import sys
import commands

from string import split, atoi

START     = '1.0'                         
SEL_FIRST = SEL + '.first'                 
SEL_LAST  = SEL + '.last'      

import sys, os, string

FontScale = 0			   # use bigger font on linux	         
if sys.platform[:3] != 'win':      # and other non-windows boxes   
    FontScale = 3
    
title = 'PadPaper Editor v1.02 - the OpenSource Text editor system'
textmsg = ('''Copyright (C) 2003 Pro Soft, Gerardo Orellana
  This program is free software; you can redistribute it and/or
  modify it under the terms of the GNU General Public License
  as published by the Free Software Foundation; version 1
  of the License, or (at your option) any later version.
  This program is distributed in the hope that it will be useful,   
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.
  You should have received a copy of the GNU General Public License
  along with this program; if not, write to the Free Software
  Foundation, Inc., 59 Temple Place - Suite 330,
  Boston, MA  02111-1307, USA.
  
  Contact Information:
  Programmer and Core Developer: Gerardo Orellana
  EMail: hello@goaccess.io''')

  
  
  
  
class TextEditor:

    ftypes = [('All files',     '*'),               
              ('Text files',   '.txt'),               
              ('Python files', '.py')]                

    colors = [{'fg':'black',      'bg':'white'},      
              {'fg':'yellow',     'bg':'black'},    
              {'fg':'white',      'bg':'blue'},       
              {'fg':'black',      'bg':'beige'},      
              {'fg':'yellow',     'bg':'purple'},
              {'fg':'black',      'bg':'brown'},
              {'fg':'lightgreen', 'bg':'darkgreen'},
              {'fg':'darkblue',   'bg':'orange'},
              {'fg':'orange',     'bg':'darkblue'}]

    fonts  = [('system',    5+FontScale, 'normal'),  
    	      ('courier',    6+FontScale, 'normal'), 
              ('courier',    8+FontScale, 'normal'),  
	      ('courier',    9+FontScale, 'normal'),
	      ('courier',   12+FontScale, 'normal'),
	      ('courier',   14+FontScale, 'normal'),
	      ('courier',   16+FontScale, 'normal'),
	      ('courier',   18+FontScale, 'normal'),
	      ('courier',   20+FontScale, 'normal'),
	      ('courier',    6+FontScale, 'bold'),
              ('courier',   10+FontScale, 'bold'),    
              ('courier',   10+FontScale, 'italic'),  
              ('times',     10+FontScale, 'normal'),
              ('helvetica', 10+FontScale, 'normal'),
              ('ariel',     10+FontScale, 'normal'),
              ('system',    10+FontScale, 'normal'),
              ('courier',   20+FontScale, 'normal')]

    def acerca(self):
	alert = Tk()
	alert.title("PadPaper Editor: "+title)
	Label(alert,text="PadPaper Editor: "+textmsg).pack()
	alert.mainloop()
	
    def isEmpty(self):
        return not self.getAllText()	


    def new(self):
        self.name = "PadPaper"
	doit = self.isEmpty() or askyesno(self.name, 'Do you want to close this file??')   
	if doit:
	  self.editor.delete(1.0,END)
	  self.filename=''
	  self.filemenu.entryconfig(2,state=DISABLED)
	  self.window.title('PadPaper Editor: New File')
	

    def open(self):
        
	if self.isEmpty() or askyesno('Save changes', 'Do you want to close this Document?' ):
            self.filename = askopenfilename()
	if self.filename:
            daFile = open(self.filename,'r')
            text = daFile.read()
            self.editor.delete(1.0,END)
            self.editor.insert(END,text)
	    self.filemenu.entryconfig(2,state=NORMAL)
	    self.window.title('PadPaper Editor v1.02: '+self.filename)

    def saveas(self):
        self.filename = asksaveasfilename()
	if self.filename:
            aFile = open(self.filename,'w')
            text = self.editor.get(1.0,END)
            aFile.write(text)
	    self.filemenu.entryconfig(2,state=NORMAL)
	    self.window.title('PadPaper Editor v1.02: '+self.filename)

    def save(self):
	if self.filename:
	    aFile = open(self.filename,'w')
	    text = self.editor.get(1.0,END)
	    aFile.write(text)
	else:
	    self.saveas()
	    
    def onDelete(self):                         
        if not self.editor.tag_ranges(SEL):
            tkMessageBox.showerror('ERROR','No text selected')
        else:
            self.editor.delete(SEL_FIRST, SEL_LAST)
	    	
    def onCopy(self):                           
        if not self.editor.tag_ranges(SEL):      
            tkMessageBox.showerror('ERROR','Nothing to Copy')
        else:
            text = self.editor.get(SEL_FIRST, SEL_LAST)

    def onCut(self):
        if not self.editor.tag_ranges(SEL):
           tkMessageBox.showerror('ERROR','Nothing to Cut')
        else:
            self.onCopy()                      
            self.onDelete()

    def onCut(self):
        if not self.editor.tag_ranges(SEL):
           tkMessageBox.showerror('ERROR','Nothing to Cut')
        else:
            self.onCopy()                     
            self.onDelete()

    def onPaste(self):
        try:
            text = self.editor.selection_get(selection='CLIPBOARD')
        except TclError:
            showerror('Paste', 'Nothing to paste')
            return
	self.editor.insert(INSERT, text)	  # add at current insert cursor
        self.editor.tag_remove(SEL, '1.0', END)
        self.editor.tag_add(SEL, INSERT+'-%dc' % len(text), INSERT)
        self.editor.see(INSERT)
	
    def process(self):
    	s = commands.getoutput('ps -x ' )
        
        self.editor.insert(INSERT, s)          
        self.editor.tag_remove(SEL, '1.0', END)
        self.editor.tag_add(SEL, INSERT+'-%dc' % len(s), INSERT)
        self.editor.see(INSERT)  
	self.window.title('PadPaper Editor v1.02: '+'Linux Process')
	
    def hd(self):
    	s = commands.getoutput('df -a ' )
        
        self.editor.insert(INSERT, s)          
        self.editor.tag_remove(SEL, '1.0', END)
        self.editor.tag_add(SEL, INSERT+'-%dc' % len(s), INSERT)
        self.editor.see(INSERT)  
	self.window.title('PadPaper Editor v1.02: '+'Linux HD INFO')	

    def onSelectAll(self):
        self.editor.tag_add(SEL, '1.0', END+'-1c')   
        self.editor.mark_set(INSERT, '1.0')          
        self.editor.see(INSERT)                     

    def gotoLine(self):
	line = tkSimpleDialog.askinteger('Goto Line', 'Enter line number')
        self.editor.update() 
        self.editor.focus()
        if line is not None:
            maxindex = self.editor.index(Tkinter.END+'-1c')
            maxline  = int(maxindex.split('.')[0])
            if (line > 0) and (line <= maxline):
                self.editor.mark_set(Tkinter.INSERT, '%d.0' % line)
		self.editor.tag_remove(Tkinter.SEL, '1.0',Tkinter.END)
		self.editor.tag_add(Tkinter.SEL, Tkinter.INSERT,'insert + 1l')
                self.editor.see(Tkinter.INSERT)
            else: tkMessageBox.showerror('Ir a', 'Bad line number')	
	    
    def onFind(self, lastkey=None):
        self.name = "PadPaper"
        key = lastkey or askstring(self.name, 'Enter search string')
        self.editor.update()
        self.editor.focus()
        self.lastfind = key
        if key:
            where = self.editor.search(key, INSERT, END)       
            if not where:
                showerror(self.name, 'String not found')
            else:
                pastkey = where + '+%dc' % len(key)           
                self.editor.tag_remove(SEL, '1.0', END)         
                self.editor.tag_add(SEL, where, pastkey)         
                self.editor.mark_set(INSERT, pastkey)           
                self.editor.see(where)                          

    def onRefind(self):
        self.onFind(self.lastfind)

    def onChange(self):
        self.name = "PadPaper"
        new = Toplevel(self.editor)
        Label(new, text='Find text:').grid(row=0, column=0)
        Label(new, text='Change to:').grid(row=1, column=0)
        self.change1 = Entry(new)
        self.change2 = Entry(new)
        self.change1.grid(row=0, column=1, sticky=EW)
        self.change2.grid(row=1, column=1, sticky=EW)
        Button(new, text='Find',
               command=self.onDoFind).grid(row=0, column=2, sticky=EW)
        Button(new, text='Apply',
	       command=self.onDoChange).grid(row=1, column=2,sticky=EW)
        new.columnconfigure(1, weight=1)    

    def onDoFind(self):
	self.onFind(self.change1.get()) 		   # Find in change box

    def onDoChange(self):
	if self.editor.tag_ranges(SEL): 		     # must find first
            self.editor.delete(SEL_FIRST, SEL_LAST)         
            self.editor.insert(INSERT, self.change2.get())  
            self.editor.see(INSERT)
            self.onFind(self.change1.get())               
            self.editor.update()   
	    

    def onFontList(self):
        self.fonts.append(self.fonts[0])          
        del self.fonts[0]                        
        self.editor.config(font=self.fonts[0])
	
    def onColorList(self):
        self.colors.append(self.colors[0])       
        del self.colors[0]                        
	self.editor.config(fg=self.colors[0]['fg'],bg=self.colors[0]['bg'])

    def onPickFg(self):
        self.pickColor('fg')                       
    def onPickBg(self):                            
        self.pickColor('bg')                       
    def pickColor(self, part):                    
        (triple, hexstr) = askcolor()
        if hexstr:
            apply(self.editor.config, (), {part: hexstr})	
			        
    def display_readme(self):
        self.read_me_text = open(self.maindir+'COPYING')
    
    	self.topin = Toplevel(height=30, width=50)
	self.topin.title(string="ReadMe GNU License PadPaper Editor v1.02")
        self.topin.resizable(height=0, width=0)

        self.topin.focus_set()

        
	self.readme_text = Text(self.topin, relief='ridge',width=74,height=30,background="white",foreground="black",borderwidth=4)
        self.readme_text.pack()
        for x in self.read_me_text:

            self.temp_string = x
            self.readme_text.insert(END, self.temp_string)

        self.readme_text.config(state=DISABLED) 

    def change_font(self):

        def set_font():

            if self.size_check.get() == 1:
                if self.font_check.get() == 1:
                    font = ('times', 10, 'normal')
                elif self.font_check.get() == 2:
                    font = ('system', 10, 'normal')
                elif self.font_check.get() == 3:
                    font = ('courier', 10, 'normal')
                else:
                   font = ('helvetica', 10, 'normal')

            elif self.size_check.get() == 2:
                if self.font_check.get() == 1:
                    font = ('times', 12, 'normal')
                elif self.font_check.get() == 2:
                    font = ('system', 12, 'normal')
                elif self.font_check.get() == 3:
                    font = ('courier', 12, 'normal')
                else:
                    font = ('helvetica', 12, 'normal')

            elif self.size_check.get() == 3:
                if self.font_check.get() == 1:
                    font = ('times', 14, 'normal')
                elif self.font_check.get() == 2:
                    font = ('system', 14, 'normal')
                elif self.font_check.get() == 3:
                    font = ('courier', 14, 'normal')
                else:
                    font = ('helvetica', 14, 'normal')

            else:
                if self.font_check.get() == 1:
                    font = ('times', 18, 'normal')
                elif self.font_check.get() == 2:
                    font = ('system', 18, 'normal')
                elif self.font_check.get() == 3:
                    font = ('courier', 18, 'normal')
                else:
                    font = ('helvetica', 18, 'normal')

            self.editor.config(font=font)
                    
            top.destroy()

        top = Toplevel(width=100, height=100)
        top.title("Font Change")
        top.resizable(height=0, width=0)
        top.focus_set()

        self.size_check = IntVar()
        self.size_check.set(2)

        self.font_check = IntVar()
        self.font_check.set(1)

        self.style_check = IntVar()
        self.style_check.set(1)

	size_1 = Radiobutton(top, text="10",variable=self.size_check, value=1)
	size_2 = Radiobutton(top, text="12",variable=self.size_check, value=2)
	size_3 = Radiobutton(top, text="14",variable=self.size_check, value=3)
	size_4 = Radiobutton(top, text="18",variable=self.size_check, value=4)

	font_1 = Radiobutton(top, text="Times",variable=self.font_check, value=1)
	font_2 = Radiobutton(top, text="System",variable=self.font_check, value=2)
	font_3 = Radiobutton(top, text="Courier",variable=self.font_check, value=3)
	font_4 = Radiobutton(top, text="Helvetica",variable=self.font_check, value=4)

        size_1.grid(row=0, column=0)
        size_2.grid(row=0, column=1)
        size_3.grid(row=0, column=2)
        size_4.grid(row=0, column=3)

        font_1.grid(row=1, column=0)
        font_2.grid(row=1, column=1)
        font_3.grid(row=1, column=2)
        font_4.grid(row=1, column=3)

	cancel = Button(top, width=6, text="Cancel",command=top.destroy, relief=RIDGE)
        cancel.grid(row=2, column=1)
        
	ok = Button(top, width=6, text="OK",command=set_font, relief=RIDGE)
        ok.grid(row=2, column=2)
    
    def getAllText(self):
        return self.editor.get('1.0', END+'-1c') 	

    def onInfo(self):
        text  = self.getAllText()                  
        bytes = len(text)                          
        lines = len(string.split(text, '\n'))     
        words = len(string.split(text))
        index = self.editor.index(INSERT)
        where = tuple(string.split(index, '.'))
        showinfo('FILE' + ' Information',
                 'Current cursor location:\n' +
                 '  line: \t%s\n  column: %s\n\n' % where +
                 'File text statistics:\n' +
		 '  bytes:\t%d\n  lines:\t%d\n	words:\t%d\n' %(bytes, lines, words))	
	
         
    def onQuit(self):
        self.name = "PadPaper"
	if askyesno(self.name, 'Do you really want to %s?' % 'quit PadPaper'):
            self.window.quit()
	    print'''Thanks for use PadPaper Editor v1.02
	    by Gerardo Orellana: Core Developer''' 
   		 
    ######################
    # File MENU commands #
    ######################	    

    def __init__(self, maindir):
        self.maindir = maindir
    
        self.window = Tk()
        self.menubar = Menu(bd=2)

                         
        self.filemenu = Menu(tearoff=0,relief=RIDGE)
       
	self.filemenu.add_command(label='New',underline=0,command=self.new)
       
	self.filemenu.add_command(label='Open...',underline=1,command=self.open)

       
	self.filemenu.add_command(label='Save',underline=2,command=self.save,state=DISABLED)

	self.filemenu.add_command(label='Save As...',underline=0,command=self.saveas)
        self.filemenu.add_separator()
       
	self.filemenu.add_command(label='Quit',underline=0,command=self.onQuit)

       
	self.menubar.add(CASCADE,label='File',underline=0,menu=self.filemenu)
        
        self.filemenu1=Menu(tearoff=0,relief=RIDGE)
       
	self.menubar.add(CASCADE,label='Edit',underline=0,menu=self.filemenu1)

       
	self.filemenu1.add_command(label='Find',underline=0,command=self.onFind)

	self.filemenu1.add_command(label='Find Next',underline=0,command=self.onRefind)
	self.filemenu1.add_command(label='Goto Line',underline=0,command=self.gotoLine)
       
	self.filemenu1.add_command(label='Replace',underline=0,command=self.onChange)

        self.filemenu1.add_separator()
       
	self.filemenu1.add_command(label='Copy',underline=1,command=self.onCopy)

       
	self.filemenu1.add_command(label='Paste',underline=0,command=self.onPaste)

       
	self.filemenu1.add_command(label='Cut',underline=2,command=self.onCut)

        self.filemenu1.add_separator()
       
	self.filemenu1.add_command(label='Delete',underline=0,command=self.onDelete)
    
	self.filemenu1.add_command(label='Select All',underline=3,command=self.onSelectAll)
        

        self.filemenu2=Menu(tearoff=0,relief=RIDGE)
       
	self.menubar.add(CASCADE,label='Settings',underline=0,menu=self.filemenu2)

       
	self.filemenu2.add_command(label='Fonts',underline=0,command=self.change_font)

        self.filemenu2.add_separator()
	self.filemenu2.add_command(label='Info.File',underline=0,command=self.onInfo)
	self.filemenu2.add_command(label='Linux Process',underline=0,command=self.process)	
	self.filemenu2.add_command(label='INFO Linux HD',underline=0,command=self.hd)
        
        self.filemenu3=Menu(tearoff=0,relief=RIDGE)
       
	self.menubar.add(CASCADE,label='Options',underline=0,menu=self.filemenu3)

	self.filemenu3.add_command(label='Random Font',underline=0,command=self.onFontList)
	self.filemenu3.add_command(label='Random Color Background',underline=0,command=self.onColorList)
        self.filemenu3.add_separator()
	self.filemenu3.add_command(label='List of Background Colors',underline=0,command=self.onPickBg)
	self.filemenu3.add_command(label='List of Fonts Colors',underline=0,command=self.onPickFg)
        
        self.filemenu4=Menu(tearoff=0,relief=RIDGE)
       
	self.menubar.add(CASCADE,label='Help',underline=0,menu=self.filemenu4)

	self.filemenu4.add_command(label='About PadPaper...',underline=0,command=self.acerca)
	self.filemenu4.add_command(label='Readme PadPaper Editor v1.02',underline=0,command=self.display_readme)
        
        self.window.config(menu=self.menubar)
        self.ys=Scrollbar(self.window,orient=VERTICAL,relief=RIDGE)
	self.editor = Text(self.window,relief='ridge',background="white",foreground="black",yscrollcommand=self.ys.set,width=140,height=44,borderwidth=4)

        
        self.toolbar = Frame(self.window,relief=RIDGE,bd=4)
        
        image =PhotoImage(file=self.maindir + 'filenew.gif') 
        image1=PhotoImage(file=self.maindir + 'fileopen.gif')
        image2=PhotoImage(file=self.maindir + 'filesave.gif')
        image3=PhotoImage(file=self.maindir + 'find.gif')

        image5=PhotoImage(file=self.maindir + 'editcopy.gif')
        image6=PhotoImage(file=self.maindir + 'editcut.gif')
        image7=PhotoImage(file=self.maindir + 'editpaste.gif')
        image8=PhotoImage(file=self.maindir + 'fileclose.gif')
        image9=PhotoImage(file=self.maindir + 'exit.gif')
        
             
	self.new = Button(self.toolbar,image=image,width=40,command=self.new, relief=FLAT)
        self.new.pack(side=LEFT, padx=2, pady=2)  

	self.new = Button(self.toolbar,image=image1,width=40,command=self.open, relief=FLAT)
        self.new.pack(side=LEFT, padx=2, pady=2)

	self.new = Button(self.toolbar,image=image2,width=40,command=self.saveas, relief=FLAT)
        self.new.pack(side=LEFT, padx=2, pady=2)
        
	self.new = Button(self.toolbar,image=image3,width=40,command=self.onFind, relief=FLAT)
        self.new.pack(side=LEFT, padx=2, pady=2)
        
	self.new = Button(self.toolbar,image=image5,width=40,command=self.onCopy, relief=FLAT)
        self.new.pack(side=LEFT, padx=2, pady=2)

	self.new = Button(self.toolbar,image=image6,width=40,command=self.onCut, relief=FLAT)
        self.new.pack(side=LEFT, padx=2, pady=2)	
        
	self.new = Button(self.toolbar,image=image7,width=40,command=self.onPaste, relief=FLAT)
        self.new.pack(side=LEFT, padx=2, pady=2)
        
	self.new = Button(self.toolbar,image=image8,width=40,command=self.onDelete, relief=FLAT)
        self.new.pack(side=LEFT, padx=2, pady=2)	
        
	self.new = Button(self.toolbar,image=image9,width=40,command=self.onQuit, relief=FLAT)
        self.new.pack(side=LEFT, padx=2, pady=2)
        

	self.status = Label(self.window, text="PadPaper Editor 1.02", bd=1, relief=FLAT, anchor=W)
        self.status.pack(side=BOTTOM, fill=X)
          
        self.toolbar.pack(side=TOP, fill=X)
        
        self.ys.config(command=self.editor.yview)
        self.editor.pack(side=LEFT)
        self.ys.pack(side=RIGHT,fill='y')
        self.window.title('PadPaper Editor: New File')
        self.filename=''
        
        
        self.window.mainloop()

if __name__ == '__main__':  # when run as a script
    print sys.platform[:3]
    if sys.platform[:3] != 'lin':      # win or lin   
        maindir = ''
    else:
        maindir='/usr/share/PadPaper-EDITOR-1.02/'
	theproggie = TextEditor(maindir)
