#!/usr/bin/python
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

from tablelib import *
from allperf import *

### CONSTANTS

# Will compute average of TRIALS runs.  Each trials starts in new JVM and warms up.

TRIALS = 1 # number of trials

if (len(sys.argv) > 4):
    TRIALS = int(sys.argv[4])
    
S = 2  # number of decimal places for table entries

###########################################

### PERFORMANCE TABLE

jvmArgs='-Xmx64g -Xms1g -noverify'
defaultRRArgs='%rowextra -quiet -maxWarn=1 -xml=%log -logs=%path %extra '

# Timing Command Line
standardCmd =  'cd %dir ; gtimeout -s 9 -k 5 2h                                env RR_MODE=SLOW env JVM_ARGS="$JVM_ARGS ' + jvmArgs +'"  ./%command   -classpath=original.jar ' + defaultRRArgs + '  '

# The experiments to run to gather timing measurements.
ftExperimentV2 =        MultiExperiment('FastTrackV2Counts', standardCmd + " -tool=FT2", TRIALS)

def sameEpochPercent(e,name='',title='c|',rowf='r|'):
    if name=='':
       name = e.abbrev
    return AverageColumn(name, 
                  lambda row, outDir: 
		               round(float((e.getXMLCounter(row,outDir,'FT: Read Same Epoch')+e.getXMLCounter(row,outDir,'FT: Write Same Epoch'))) / 
                                     float(e.getXMLCounter(row,outDir,'FT: Total Access Ops')),S), rowf,title,[],scale=3,sideways=True)


def sameReadEpochPercent(e,name='',title='c|',rowf='r|'):
    if name=='':
       name = e.abbrev
    return AverageColumn(name, 
                  lambda row, outDir: 
		               round(float((e.getXMLCounter(row,outDir,'FT: Read Same Epoch'))) / 
                                     float(e.getXMLCounter(row,outDir,'FT: Total Access Ops')),S), rowf,title,[],scale=3,sideways=True)

def sameReadSharedEpochPercent(e,name='',title='c|',rowf='r|'):
    if name=='':
       name = e.abbrev
    return AverageColumn(name, 
                  lambda row, outDir: 
		               round(float((e.getXMLCounter(row,outDir,'FT: ReadShared Same Epoch'))) / 
                                     float(e.getXMLCounter(row,outDir,'FT: Total Access Ops')),S), rowf,title,[],scale=3,sideways=True)

def sameWriteEpochPercent(e,name='',title='c|',rowf='r|'):
    if name=='':
       name = e.abbrev
    return AverageColumn(name, 
                  lambda row, outDir: 
		               round(float(e.getXMLCounter(row,outDir,'FT: Write Same Epoch')) / 
                                     float(e.getXMLCounter(row,outDir,'FT: Total Access Ops')),S), rowf,title,[],scale=3,sideways=True)

def sameEpochWithRSPercent(e,name='',title='c|',rowf='r|'):
    if name=='':
       name = e.abbrev
    return AverageColumn(name, 
                  lambda row, outDir: 
		               round(float((e.getXMLCounter(row,outDir,'FT: Read Same Epoch')+e.getXMLCounter(row,outDir,'FT: ReadShared Same Epoch')+e.getXMLCounter(row,outDir,'FT: Write Same Epoch'))) / 
                                     float(e.getXMLCounter(row,outDir,'FT: Total Access Ops')),S),rowf,title,[],scale=3,sideways=True)


# Columns for the table

cols = [
    Column("", (lambda row, outDir: row.name), 'Mean', '|l|', '|c|'),
    sameReadEpochPercent(ftExperimentV2,'ReadSameEpoch'),
    sameWriteEpochPercent(ftExperimentV2,'WriteSameEpoch'),
    sameReadSharedEpochPercent(ftExperimentV2,'ReadSharedSameEpoch'),
    sameEpochWithRSPercent(ftExperimentV2,'Total'),
]

exps=[
    ftExperimentV2,
]

statsTable =      Table('Performance', 'large-stats',  [],  javagrade_rows + dacapo_rows, cols, exps,'stats')
smallstatsTable =      Table('Performance', 'small-stats',  [],  rows_small, cols, exps,'stats')

################ 
tables = [ statsTable, smallstatsTable ]

genRows = sys.argv[1]
genExps = sys.argv[2]

# Comment out this line if you want to regenerate data...
#genExps = "none"

genTables  = extractFromList(sys.argv[3], tables)

file = 'tables-stats'
out=open(file + '.tex','w')
out.write('\\documentclass[landscape]{article}\n\\usepackage{lscape}\n\\usepackage{rotating}\n\\begin{document}\n')
out.write('\\oddsidemargin -0.5in \n')
out.write('\\tiny\n')

for t in genTables:
  t.gen(genRows, genExps)
  t.dump(out,True) 
  out.write('\n\n\n \\pagebreak \n\n\n')

out.write('\\end{document}\n')
out.close()

os.system('pdflatex ' + file + '.tex')
