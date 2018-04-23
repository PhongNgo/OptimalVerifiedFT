#!/usr/bin/python2.5 -u
#
# Copyright (c) 2016, Cormac Flanagan (University of California, Santa Cruz)
#                     and Stephen Freund (Williams College) 
#
# All rights reserved.  
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
# 
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#
#    * Redistributions in binary form must reproduce the above
#      copyright notice, this list of conditions and the following
#      disclaimer in the documentation and/or other materials provided
#      with the distribution.
#
#    * Neither the names of the University of California, Santa Cruz
#      and Williams College nor the names of its contributors may be
#      used to endorse or promote products derived from this software
#      without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

import math
import os
import os.path
import sys
import string
import datetime
import re
from xml.etree.ElementTree import ElementTree
import numpy as np
import scipy as sp
import scipy.stats
import math
from math import *
import datetime 

###################################################################################        
#
#  ROWS
#


#
# Represents a benchmark program
#
class Row:
      def __init__(self, name, abbrev, dir, command, extra='',beforeLine=''):
      	  self.name = name
	  self.abbrev = abbrev
	  self.dir = dir
	  self.values = {}
	  self.extra = extra
	  self.beforeLine=beforeLine
          self.command=command

###################################################################################        
#
#  COLUMNS
#

#
# Represents on column of data in a table.
#
class Column:
      def __init__(self, name, valFn, summary='', format='|c', titleFormat='|c|', sideways=False):
      	  self.name = name
	  self.valFn = valFn
	  self.summaryFn= lambda rows, outDir: summary
	  self.format = format
	  self.titleFormat=titleFormat
	  self.sideways = sideways

      def value(self, row, outDir):
          try: 
            return self.valFn(row, outDir)
          except Exception, inst:
            print '# !!! ' + str(inst)
            return '--'
 
      def summarize(self, rows, outDir):
	  return self.summaryFn(rows,outDir)


      def rep(self,row,value):
       	  return commify(value)


#
# Same as Column, but always has ( ) around the data.
#
class ColumnP:
      def __init__(self, name, valFn, summary='', format='|c', titleFormat='|c|', sideways=False):
      	  self.name = name
	  self.valFn = valFn
	  self.summaryFn= lambda rows, outDir: summary
	  self.format = format
	  self.titleFormat=titleFormat
	  self.sideways = sideways

      def value(self, row, outDir):
          try: 
            return self.valFn(row, outDir)
          except Exception, inst:
            print '# !!! ' + str(inst)
            return '--'
 
      def summarize(self, rows, outDir):
	  return self.summaryFn(rows,outDir)


      def rep(self,row,value):
       	  return "(" + str(commify(value)) + ")"



#
# A Column that reports numbers.
#
class NumericColumn(Column):
      def __init__(self, name, valFn, summary='',format='|c', titleFormat='|c|',exclude=[],scale=1, sideways=False):
      	  self.name = name
	  self.valFn = valFn
	  self.format = format
	  self.titleFormat=titleFormat
	  self.exclude = exclude
	  self.scale = scale
	  self.sideways = sideways
	  self.summaryFn= lambda rows, outDir: summary

      def value(self, row, outDir):
          try: 
              if (self.scale == 0):
                  return nicifySmall(int(self.valFn(row, outDir)))
              else:
                  return nicifySmall(self.valFn(row, outDir))
          except Exception, inst:
            print '# !!! ' + str(inst)
            return '--'


 



#
# A Column that reports the arithmetic average of rows.
#
class AverageColumn(Column):
      def __init__(self, name, valFn, format='|c', titleFormat='|c|',exclude=[],scale=1, sideways=False):
      	  self.name = name
	  self.valFn = valFn
	  self.format = format
	  self.titleFormat=titleFormat
	  self.exclude = exclude
	  self.scale = scale
	  self.sideways = sideways

      def value(self, row, outDir):
          try: 
              if (self.scale == 0):
                  return nicifySmall(int(self.valFn(row, outDir)))
              else:
                  return nicifySmall(self.valFn(row, outDir))
          except Exception, inst:
            print '# !!! ' + str(inst)
            return '--'
 
      def summarize(self, rows, outDir):
          count = 0
	  sum = 0
          for r in [r for r in rows if not (r in self.exclude)]:
              try:
  	        sum = sum + self.valFn(r, outDir)
                count = count + 1
              except Exception, inst:
                print '# !!! ' + str(inst)
          if count == 0:
	      return '--'
          else:
              if (self.scale == 0): 
                  return nicifySmall(int(round(float(sum)/float(count))))
              else:
                  return nicifySmall(round(float(sum)/float(count), self.scale))


#
# A Column that reports the arithmetic average of rows, always using ( ).
#
class AverageColumnP(Column):
      def __init__(self, name, valFn, format='|c', titleFormat='|c|',exclude=[],scale=2, sideways=False):
      	  self.name = name
	  self.valFn = valFn
	  self.format = format
	  self.titleFormat=titleFormat
	  self.exclude = exclude
	  self.scale = scale
	  self.sideways = sideways

      def value(self, row, outDir):
          try: 
              if (self.scale == 0): 
                  return int(self.valFn(row, outDir))
              else:
                  return self.valFn(row, outDir)
          except Exception, inst:
            print '# !!! ' + str(inst)
            return '--'
 
      def summarize(self, rows, outDir):
          count = 0
	  sum = 0
          for r in [r for r in rows if not (r in self.exclude)]:
              try:
  	        sum = sum + self.valFn(r, outDir)
                count = count + 1
              except Exception, inst:
                print '# !!! ' + str(inst)
          if count == 0:
	      return '--'
          else:
              if (self.scale == 0): 
                  return '(' + str(int(round(float(sum)/float(count)))) + ')'
              else:
                  return  '(' + str(round(float(sum)/float(count), self.scale)) + ')'

      def rep(self,row,value):
       	  return '(' + commify(value) + ')'

#
# A Column that reports the geometric mean of rows.
#
class GeometricMeanColumn(Column):
      def __init__(self, name, valFn, format='|c', titleFormat='|c|',exclude=[],scale=3, sideways=False):
      	  self.name = name
	  self.valFn = valFn
	  self.format = format
	  self.titleFormat=titleFormat
	  self.exclude = exclude
	  self.scale = scale
	  self.sideways = sideways

      def value(self, row, outDir):
          try: 
            return self.valFn(row, outDir)
          except Exception, inst:
            print '# !!! ' + str(inst)
            return '--'
 
      def summarize(self, rows, outDir):
          count = 0
	  sum = 1
          for r in [r for r in rows if not (r in self.exclude)]:
              try:
  	        sum = sum * self.valFn(r, outDir)
                count = count + 1
              except Exception, inst:
                print '# !!! ' + str(inst)
          if count == 0:
	      return '--'
          else:
                if (pow(float(sum), (1/float(count))) >= 1):
                      return nicifySmall(round_sig(pow(float(sum), (1/float(count))), self.scale))
                else:
                      return nicifySmall(round_sig(pow(float(sum), (1/float(count))), self.scale))

      def rep(self,row,value):
       	  return nicifySmall(value)

#
# A Column that reports the geometric mean of rows, always using ( )
#
class GeometricMeanColumnP(Column):
      def __init__(self, name, valFn, format='|c', titleFormat='|c|',exclude=[],scale=1, sideways=False):
      	  self.name = name
	  self.valFn = valFn
	  self.format = format
	  self.titleFormat=titleFormat
	  self.exclude = exclude
	  self.scale = scale
	  self.sideways = sideways

      def value(self, row, outDir):
          try: 
            return self.valFn(row, outDir)
          except Exception, inst:
            print '# !!! ' + str(inst)
            return '--'
 
      def summarize(self, rows, outDir):
          count = 0
	  sum = 1
          for r in [r for r in rows if not (r in self.exclude)]:
              try:
  	        sum = sum * self.valFn(r, outDir)
                count = count + 1
              except Exception, inst:
                print '# !!! ' + str(inst)
          if count == 0:
	      return '--'
          else:
	      return '(' + str(round(pow(float(sum), (1/float(count))), self.scale)) + ')'

      def rep(self,row,value):
       	  return '(' + commify(value) + ')'

#
# A Column that reports the sum of rows.
#
class SumColumn(Column):
      def __init__(self, name, valFn, format='|c', titleFormat='|c|',exclude=[], sideways=False):
      	  self.name = name
	  self.valFn = valFn
	  self.format = format
	  self.titleFormat=titleFormat
	  self.exclude = exclude
	  self.sideways = sideways

      def value(self, row, outDir):
          try: 
            return self.valFn(row, outDir)
          except Exception, inst:
            print '!!! ' + str(inst)
            return '--'
 
      def summarize(self, rows, outDir):
	  sum = 0
          for r in [r for r in rows if not (r in self.exclude)]:
              try:
  	        sum = sum + self.valFn(r, outDir)
              except Exception, inst:
                print '!!! ' + str(inst)
	  return commify(sum)


###################################################################################        
#
#  EXPERIMENTS
#

class Experiment:
      def __init__(self, abbrev, commandString, checkTimeOut=True,excludes=[]):
	  self.abbrev = abbrev
	  self.commandString = commandString
	  self.checkTimeOut=checkTimeOut
	  self.excludes = excludes
          self.cached = dict()
 
      def logFileName(self, row):
          return self.abbrev + "-" + row.abbrev + ".out"

      def stdoutFileName(self, row):
          return self.abbrev + "-" + row.abbrev + ".log"

      def moveOldLogs(self, logDir, row):
      	  logPrefix = logDir + '/' + self.logFileName(row)
	  if os.path.exists(logPrefix):
	  	  i = 0
	 	  while os.path.exists('%s.%d' % (logPrefix, i)):
	  	  	i = i + 1

		  if i == 51:
		        os.remove('%s.%d' % (logPrefix, 50))
                        i = 50

  	          while i > 0:
  	  	  	os.rename( '%s.%d' % (logPrefix, i-1), '%s.%d' % (logPrefix, i))
                        i = i - 1
          	  os.rename(logPrefix, '%s.%d' % (logPrefix, 0))

      def replace(self, s, row, logDir, extra=""):
      	  s = s.replace('%rowextra', row.extra)
      	  s = s.replace('%name', row.name)
      	  s = s.replace('%command', row.command)
	  s = s.replace('%row', row.abbrev)
	  s = s.replace('%dir', row.dir)
	  s = s.replace('%path', logDir)
	  s = s.replace('%log', self.logFileName(row))
	  s = s.replace('%extra', extra)
	  return s

      def run(self, row, logDir, extra=""):
          self.moveOldLogs(logDir, row)
          cmd = self.replace(self.commandString, row, logDir, extra)
          cmd = cmd + ' > ' + logDir + '/' + self.stdoutFileName(row) + ' 2>&1 '
#          cmd = cmd + ' > ' + logDir + '/' + self.stdoutFileName(row) + ' 2> ' + logDir + '/' + self.stdoutFileName(row) + '.err'
	  print '# Start Time: ' + str(datetime.datetime.now()) 
          print '# Command:' 
          print '        ' + cmd
          sys.stdout.flush()
          if row in self.excludes:
	       print '    -> SKIPPED '
	  else:
              sys.stdout.flush()
              os.system(cmd)
              sys.stdout.flush()

      def getRaw(self, file):
            if (not (file in self.cached)):
                  self.cached[file]=ElementTree(file=open(file,'r'))
            return self.cached[file]

      def extractXML(self, file, field):
      	  doc = self.getRaw(file)
    	  l = [ e.findtext('.') for e in doc.findall(field)]
	  return l

      def checktimedOut(self, file):
          if self.checkTimeOut:
	            doc = self.getRaw(file)
          	    if doc.findtext('./timeout').strip() == 'YES':
	     	       raise Exception('Timeout: ' + file)
                    if doc.findtext('./failed').strip() == "true":
	     	       raise Exception('Failed!: ' + file)

      def readFirstLine(self, row, logDir):
          fileName = logDir + '/' + self.logFileName(row)
	  return open(fileName).readline().strip()

      def readFirstLineAsFloat(self, row, logDir):
          fileName = logDir + '/' + self.logFileName(row)
	  return float(open(fileName).readline().strip())

      def getXMLEntryAsInt(self, row, logDir, field): 
          fileName = logDir + '/' + self.logFileName(row)
	  self.checktimedOut(fileName)
      	  l = self.extractXML(fileName, field)
    	  if len(l) != 1:
       	     print 'Warning: Not singleton %s %s' % (fileName, field)
    	  return int(l[0])


      def getXMLEntryAsBoolean(self, row, logDir, field): 
          fileName = logDir + '/' + self.logFileName(row)
	  self.checktimedOut(fileName)
      	  l = self.extractXML(fileName, field)
    	  if len(l) != 1:
       	     print 'Warning: Not singleton %s %s' % (fileName, field)
    	  return bool(l[0])

      def getXMLCounter(self, row, logDir, name): 
          fileName = logDir + '/' + self.logFileName(row)
	  self.checktimedOut(fileName)
          doc = self.getRaw(fileName)

	  ls = [e for e in doc.findall('./counters/counter')]
          l = [e for e in ls if e.findtext('./name').strip()[1:-1] == name.strip()]

	  if len(l) != 1:
	         print 'Warning: Not singleton %s %s' % (file, name)

    	  return int(l[0].findtext('./value').replace(',','').split()[0])


      def getXMLCounterAsFloat(self, row, logDir, name): 
          fileName = logDir + '/' + self.logFileName(row)
	  self.checktimedOut(fileName)
          doc = self.getRaw(fileName)

	  ls = [e for e in doc.findall('./counters/counter')]
          l = [e for e in ls if e.findtext('./name').strip()[1:-1] == name.strip()]

	  if len(l) != 1:
	         print 'Warning: Not singleton %s %s' % (file, name)

    	  return float(l[0].findtext('./value').replace(',','').split()[0])

      def getXMLCounterField(self, row, logDir, name, path='total'): 
          fileName = logDir + '/' + self.logFileName(row)
	  self.checktimedOut(fileName)
          doc = self.getRaw(fileName)

	  ls = [e for e in doc.findall('./counters/counter')]
          l = [e for e in ls if e.findtext('./name').strip()[1:-1] == name.strip()]

	  if len(l) != 1:
	         print 'Warning: Not singleton %s %s' % (file, name)

    	  return (l[0].findtext('./value/' + path).replace(',','').split()[0])


##############


class MultiExperiment(Experiment):
      def __init__(self, abbrev, commandString, iters, checkTimeout=True,excludes=[],startNum=0):
	  self.abbrev = abbrev
	  self.commandString = commandString
	  self.iters = iters
          self.startNum = startNum
	  self.checkTimeOut=checkTimeout
	  self.excludes = excludes
          self.cached = dict()


      def logFileName(self, row, iter):
          return self.abbrev + "-" + row.abbrev + '-' + str(iter) + ".out"

      def stdoutFileName(self, row, iter):
          return self.abbrev + "-" + row.abbrev + '-' + str(iter) + ".log"

      def moveOldLogs(self, logDir, row, iter):
      	  logPrefix = logDir + '/' + self.logFileName(row, iter)
	  if os.path.exists(logPrefix):
	  	  i = 0
	 	  while os.path.exists('%s.%d' % (logPrefix, i)):
	  	  	i = i + 1

		  if i == 51:
		        os.remove('%s.%d' % (logPrefix, 50))
                        i = 50

  	          while i > 0:
  	  	  	os.rename( '%s.%d' % (logPrefix, i-1), '%s.%d' % (logPrefix, i))
                        i = i - 1
          	  os.rename(logPrefix, '%s.%d' % (logPrefix, 0))


      def replace(self, s, row, logDir, iter, extra=""):
      	  s = s.replace('%rowextra', row.extra)
      	  s = s.replace('%name', row.name)
      	  s = s.replace('%command', row.command)
	  s = s.replace('%row', row.abbrev)
	  s = s.replace('%dir', row.dir)
	  s = s.replace('%path', logDir)
	  s = s.replace('%log', self.logFileName(row, iter))
	  s = s.replace('%extra', extra)
	  return s

      def iterRange(self):
          return range(self.startNum, self.startNum+self.iters)

      def run(self, row, logDir, extra=""):
          for iter in self.iterRange():
	            self.moveOldLogs(logDir, row, iter)
	            cmd = self.replace(self.commandString, row, logDir, iter, extra)
		    cmd = cmd + ' > ' + logDir + '/' + self.stdoutFileName(row,iter) + ' 2>&1 '
#                    cmd = cmd + ' > ' + logDir + '/' + self.stdoutFileName(row,iter) + ' 2> ' + logDir + '/' + self.stdoutFileName(row,iter) + '.err'
                    print '!!! ' + str(datetime.datetime.now()) + ' ' + cmd
                    sys.stdout.flush()
		    if row in self.excludes:
		       print '    -> SKIPPED '
		    else:
		       os.system(cmd)
                    sys.stdout.flush()
                 
      def getXMLEntry(self, row, iter, logDir, field) :
          fileName = logDir + '/' + self.logFileName(row, iter)
          self.checktimedOut(fileName)
          l = self.extractXML(fileName, field)
          if len(l) != 1:
              print 'Warning: Not singleton %s %s' % (fileName, field)
          return l[0] 

      def getXMLEntriesAsRawList(self, row, logDir, field): 
          return [self.getXMLEntry(row, iter, logDir, field) for iter in self.iterRange()]


      def getFirstXMLEntry(self, row, iter, logDir, field) :
          fileName = logDir + '/' + self.logFileName(row, iter)
          self.checktimedOut(fileName)
          l = self.extractXML(fileName, field)
          return l[0] 

      def getFirstXMLEntriesAsRawList(self, row, logDir, field): 
          return [self.getFirstXMLEntry(row, iter, logDir, field) for iter in self.iterRange()]

      def getXMLEntryAsInt(self, row, logDir, field): 
          r = 0
          for iter in self.iterRange():
	          fileName = logDir + '/' + self.logFileName(row, iter)
		  self.checktimedOut(fileName)
      	  	  l = self.extractXML(fileName, field)
		  if len(l) != 1:
	                  print 'Warning: Not singleton %s %s' % (fileName, field)
         	  r = r + int(l[0])
          return r / self.iters

      def getXMLEntryAsFloat(self, row, logDir, field): 
          r = 0
          for iter in self.iterRange():
	          fileName = logDir + '/' + self.logFileName(row, iter)
		  self.checktimedOut(fileName)
      	  	  l = self.extractXML(fileName, field)
		  if len(l) != 1:
	                  print 'Warning: Not singleton %s %s' % (fileName, field)
         	  r = r + float(l[0])
          return r / self.iters

      def stdDevXMLEntryAsInt(self, row, logDir, field): 
          r = 0.0
          mean = self.getXMLEntryAsInt(row, logDir, field)
          for iter in self.iterRange():
	          fileName = logDir + '/' + self.logFileName(row, iter)
		  self.checktimedOut(fileName)
      	  	  l = self.extractXML(fileName, field)
		  if len(l) != 1:
	                  print 'Warning: Not singleton %s %s' % (fileName, field)
                  v = int(l[0]);
         	  r = r + (v - mean) * (v - mean)
                  print " --- %d %d %d" % (v, r, mean)
          return math.sqrt(r / self.iters)

      def ci(self, row, logDir, field, confidence = 0.95): 
          m = self.getXMLEntryAsInt(row, logDir, field)
#          return bootstrap(m, 10000, np.mean, 0.05)
          return 0

      def readFirstLineAsInt(self, row, logDir):
          r = 0
          for iter in self.iterRange(): 
            fileName = logDir + '/' + self.logFileName(row, iter)
  	    n = int(open(fileName).readline().strip())
	    r = r + n
	  return r / self.iters

      def getXMLCounter(self, row, logDir, name): 
          r = 0
          for iter in self.iterRange(): 
            fileName = logDir + '/' + self.logFileName(row, iter)
  	    self.checktimedOut(fileName)
            doc = self.getRaw(fileName)

	    ls = [e for e in doc.findall('./counters/counter')]
            l = [e for e in ls if e.findtext('./name').strip()[1:-1] == name.strip()]

	    if len(l) != 1:
	            print 'Warning: Not singleton %s %s' % (file, name)
	    r = r + int(l[0].findtext('./value').replace(',','').split()[0])

    	  return r / self.iters


      def getXMLCounterAsFloat(self, row, logDir, name): 
          r = 0
          for iter in self.iterRange(): 
            fileName = logDir + '/' + self.logFileName(row, iter)
  	    self.checktimedOut(fileName)
            doc = self.getRaw(fileName)

	    ls = [e for e in doc.findall('./counters/counter')]
            l = [e for e in ls if e.findtext('./name').strip()[1:-1] == name.strip()]

	    if len(l) != 1:
	            print 'Warning: Not singleton %s %s' % (file, name)
	    r = r + float(l[0].findtext('./value').replace(',','').split()[0])

    	  return r / self.iters


      def getXMLCounterAsRawList(self, row, logDir, name): 
          r = []
          for iter in self.iterRange(): 
            fileName = logDir + '/' + self.logFileName(row, iter)
  	    self.checktimedOut(fileName)
            doc = self.getRaw(fileName)

	    ls = [e for e in doc.findall('./counters/counter')]
            l = [e for e in ls if e.findtext('./name').strip()[1:-1] == name.strip()]

	    if len(l) != 1:
	            print 'Warning: Not singleton %s %s' % (file, name)
	    r.append(float(l[0].findtext('./value').replace(',','').split()[0]))

    	  return r


      def readFirstLineAsFloat(self, row, logDir):
          r = 0
          for iter in self.iterRange(): 
            fileName = logDir + '/' + self.logFileName(row, iter)
  	    n = float(open(fileName).readline().strip())
	    r = r + n
	  return r / self.iters



      def getMaxXMLEntryAsInt(self, row, logDir, field): 
          r = 0
          for iter in self.iterRange():
	          fileName = logDir + '/' + self.logFileName(row, iter)
		  self.checktimedOut(fileName)
      	  	  l = self.extractXML(fileName, field)
		  if len(l) != 1:
	                  print 'Warning: Not singleton %s %s' % (fileName, field)
         	  if r < int(l[0]):
		     r = int(l[0])
          return r

      def getMaxXMLCounterAsInt(self, row, logDir, name): 
          r = 0
          for iter in self.iterRange():
	          fileName = logDir + '/' + self.logFileName(row, iter)
		  self.checktimedOut(fileName)
      	  	  doc = self.extractXML(fileName, field)

	  	  ls = [e for e in doc.findall('./counters/counter')]
          	  l = [e for e in ls if e.findtext('./name').strip()[1:-1] == name.strip()]

	  	  if len(l) != 1:
	             	    print 'Warning: Not singleton %s %s' % (file, field)

    	  	  x = int(l[0].findtext('./value').replace(',','').split()[0])
		  if r < x:
		     r = x
          return r


      def getMinXMLEntryAsInt(self, row, logDir, field): 
          r = 0
          for iter in self.iterRange():
	          fileName = logDir + '/' + self.logFileName(row, iter)
		  self.checktimedOut(fileName)
      	  	  l = self.extractXML(fileName, field)
		  if len(l) != 1:
	                  print 'Warning: Not singleton %s %s' % (fileName, field)
         	  if iter == 0 or r > int(l[0]):
		     r = int(l[0])
          return r

      def getMinXMLCounterAsInt(self, row, logDir, name): 
          r = 0
          for iter in self.iterRange():
	          fileName = logDir + '/' + self.logFileName(row, iter)
		  self.checktimedOut(fileName)
      	  	  doc = self.extractXML(fileName, field)

	  	  ls = [e for e in doc.findall('./counters/counter')]
          	  l = [e for e in ls if e.findtext('./name').strip()[1:-1] == name.strip()]

	  	  if len(l) != 1:
	             	    print 'Warning: Not singleton %s %s' % (file, field)

    	  	  x = int(l[0].findtext('./value').replace(',','').split()[0])
		  if iter == 0 or r > x:
		     r = x
          return r

      def getXMLCounterField(self, row, logDir, name, path='total'): 
          r = 0
          for iter in self.iterRange():
	          fileName = logDir + '/' + self.logFileName(row, iter)
		  self.checktimedOut(fileName)
      	  	  doc = self.getRaw(fileName)

	  	  ls = [e for e in doc.findall('./counters/counter')]
          	  l = [e for e in ls if e.findtext('./name').strip()[1:-1] == name.strip()]

	  	  if len(l) != 1:
	             	    print 'Warning: Not singleton %s %s' % (file, field)

    	  	  x = int(float(l[0].findtext('./value/' + path).replace(',','').split()[0]))
		  if iter == 0 or r > x:
		     r = x
          return r



def containsPrefix(p, l):
    for s in l:
    	if p.startswith(s):
	   return True
    return False

def extractFromList(part, whole):
	    if part == 'all':
	       return whole
	    elif part == 'none':
	       return []
	    else:
	       return [e for e in whole if containsPrefix(e.abbrev,part.split(':'))]

###################################################################################        
#
#  TABLES
#


#
# Represents a possibly-multi-column header in a table.
#
class Header:
      def __init__(self, name, width=1, format='c|', cline=True, sideways=False):
      	  self.name = name
	  self.width = width
	  self.format = format
	  self.cline = cline
	  self.sideways = sideways

class Table:
	def __init__(self, logName, abbrev, headers, rows, cols, experiments, logDir='logs'):
	      self.abbrev = abbrev
	      self.logDir = os.getcwd() + '/' + 'table' + '-' + logDir
	      self.rows = rows
	      self.cols = cols
	      self.headers = headers
	      self.experiments = experiments

	      print "# !!! creating %s..." % (self.logDir)
	      if os.path.exists(self.logDir):
	      	 print "# !!! WARNING: outdir exists"
	      else:
		os.mkdir(self.logDir)
	     	print ""
	      
        def gen(self, genRowsOnly, genExperimentsOnly):

	    genRows = extractFromList(genRowsOnly, self.rows)
	    genExps = extractFromList(genExperimentsOnly, self.experiments)
	    x = self.logDir

            for r in genRows:
                for e in genExps:
	    	    print '# !!! Generating %s(%s)...' % (e.abbrev,r.abbrev)
	    	    try:
			e.run(r, x)
		    except Exception, inst:
			print '# !!! Error running run command: ' + str(inst)

	def dump(self, primaryOut, summarize=False, sortKey = None): 
	    out = open(self.abbrev + '.tex','w')
	    csv = open(self.abbrev + '.csv','w')
    	    width = len(self.cols)
    	    primaryOut.write('\\noindent\n')
	    primaryOut.write('\\input{%s}\n' % (self.abbrev + '.tex'))

            # headers
    	    out.write('\\begin{tabular}{')
    	    for i in range(width):
    	    	out.write(self.cols[i].format)
    	    out.write('}\n')
    	    out.write('\\hline\n')

      	    for line in self.headers:
	        first = True
	    	for h in line:
		    if not first:
		      	 out.write('&')
              	    first = False
		    if h.sideways:
		       out.write('\\multicolumn{%d}{%s}{\\begin{sideways}%s\\end{sideways}}' % (h.width,h.format,h.name))
		    else:
		       out.write('\\multicolumn{%d}{%s}{%s}' % (h.width,h.format,h.name))
	        out.write('\\\\ \n')
	        i = 1
      	  	for h in line:
	      	    if h.width > 1 and h.cline:
	      	       out.write('\\cline{%d-%d}\n' % (i, i+(h.width-1)))
              	    i = i + h.width

            first = True
            for col in self.cols:
  	        if not first:
	            out.write('&')
              	first = False
		if col.sideways:
	    	  out.write('\\multicolumn{1}{%s}{\\begin{sideways}%s\\end{sideways}}' % (col.titleFormat,col.name))
		else:
	    	  out.write('\\multicolumn{1}{%s}{%s}' % (col.titleFormat,col.name))
                csv.write('%s,' % col.name)
	    out.write('\\\\ \n')
            csv.write('\n')

    	    out.write('\\hline\n')	     
    	    out.write('\\hline\n')

            # body
            if (sortKey != None):
                sortedRows = sorted(self.rows, key = lambda r : (sortKey(r,self.logDir)));
            else:
                sortedRows = self.rows

    	    for r in sortedRows:
	        out.write(r.beforeLine)
	        first = True
		for c in self.cols:
		    if not first:
		      	 out.write('&')
              	    first = False
	    	    try:
			v = c.value(r, self.logDir)
			print '# !!! %s(%s x %s) = %s' % (self.abbrev,r.abbrev,c.name, str(v))
                        s = str(c.rep(r,v))
		    	out.write(' %10s ' % s)
                        csv.write('%s,' % s.replace(",", "").replace('*','').replace('(','').replace(')',''))
            	    except Exception, inst:
			print '# !!! Error running value command: %s(%s x %s) = %s' % (self.abbrev,r.abbrev,c.name, str(inst))
		    	out.write(' %10s ' % ('--'))
                        csv.write(',')
        
		out.write('\\\\ \n')
                csv.write('\n')
                
            # summary
    	    out.write('\\hline\n')

	    if summarize:
	       first = True
    	       out.write('\\hline\n')
               for col in self.cols:
  	           if not first:
	              out.write('&')
              	   first = False
                   s = str(col.summarize(self.rows,self.logDir))
	    	   out.write(' %10s ' % s)
                   csv.write('%s,' % s.replace(",", "").replace('*','').replace('(','').replace(')',''))
	       out.write('\\\\ \n')
    	       out.write('\\hline\n')
               csv.write('\n')


            # footer
    	    out.write('\\end{tabular}\n')
	    out.close()
            csv.close()

            print("##########################")
            os.system('cat ' + self.abbrev + '.csv');
            print("##########################")

############


def stats(file):
          try: 
		  doc = ElementTree(file=open(file,'r'))
		  return ' <td> %s </td><td> %s </td><td> %s </td><td> %s  </td> ' % (	
		    	     "<font color=\"red\"><b>FAIL</b></font>" if [e.findtext('.') for e in doc.findall('./failed')][0].strip() == "true" else " OK ",
    	    		    [ e.findtext('.') for e in doc.findall('./errorTotal')][0].strip(),
		    	    [ e.findtext('.') for e in doc.findall('./warningsTotal')][0].strip(),
		    	    [ e.findtext('.') for e in doc.findall('./yikesTotal')][0].strip())
          except Exception, inst:
            	return str(inst)

def toHTML(logDirName):
     	  logDir = os.getcwd() + '/' + 'table' + '-' + logDirName
	  out = open(logDirName + '.html','w')
          out.write('<html><body>')

          prefs = []

          for root, dirs, files in os.walk(logDir):
	      for name in files:
	      	  if re.compile(".*-.*.out$").match(name):
		     prefs.append(name.split('-')[0])
	  prefs = set(prefs)

          out.write('<table border=1>')
	  out.write("<tr><td>Experiment</td><td>xml</td><td>log</td><td>status</td><td>errors</td><td>warnings</td><td>yikes</td><td>previous</td></tr>\n")
	  for p in prefs:

	      for root, dirs, files in os.walk(logDir):
	          for name in files:
                      if re.compile(p + "-.*.out$").match(name):
                          print name
                          out.write('<tr>')
                          out.write('<td><b>%s - %s</b></td>' % (p,name.split('-')[1]))
                          outFile = ("%s/%s" % (root, name))
                          out.write('<td><a href=\"%s\">%s</a></td>' % (outFile, outFile.split('/')[-1]))
                          out.write('<td><a href=\"%s/%s\">log</a></td>' % (root, name.replace('.out', '.log')))
                          out.write(' %s ' % stats(root + '/' + name))
                          i = 0
                          out.write('<td>')
                          
                          while '%s.%d' % (name,i) in files:
                              out.write(' :: <a href=\"%s/%s.%d\">%d</a>' % (root, name, i,i))
                              i = i + 1
                          out.write('</td>')
                          out.write('</tr>\n')

          out.write('</table>')
          out.write('<br>\n')
          out.write('</body></html>\n\n\n')
	  out.close()




####################
#
#  HELPERS
#

regex = re.compile(r'^(-?\d+)(\d{3})')

def commify(num, separator=','):
    """commify(num, separator) -> string

    Return a string representing the number num with separator inserted
    for every power of 1000.   Separator defaults to a comma.
    E.g., commify(1234567) -> '1,234,567'
    """
    num = str(num)  # just in case we were passed a numeric value
    more_to_do = 1
    while more_to_do:
        (num, more_to_do) = regex.subn(r'\1%s\2' % separator,num)
    return num



zeros=True

def nicifySmall(num):
    if (not zeros):
        return str(num)
    if (num > 0.0001):
        return str(num)
    else:
        if (num == 0):
            return "0"
        else:
            result = "0."
            d = num
            while (d < 0.1):
                result = result + "0"
                d = d * 10
            while (d < 10):
                d = d * 10
            return result + str(int(d))


def round_sig(x, sig=2):
    if x == 0:
        return 0
    else:
        return round(x, sig-int(floor(log10(x)))-1)
