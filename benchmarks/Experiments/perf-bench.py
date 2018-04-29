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
import numpy as np
import numpy.random as npr
import sys

### CONSTANTS

# Will compute average of N x TRIALS runs.  Each trials starts in new JVM and warms up.

N = 10  # number of iters in each trial
TRIALS = 10 # number of trials
START = 0 # special start index...

if (len(sys.argv) > 4):
    N = int(sys.argv[4])
    TRIALS = int(sys.argv[5])
    
S = 2  # number of decimal places for table entries

###########################################

### PERFORMANCE TABLE

jvmArgs='-Xmx64g -Xms1g -noverify'
defaultRRArgs='%rowextra -quiet -maxWarn=1 -xml=%log -logs=%path %extra '

# Timing Command Line
standardCmd =  'cd %dir ; gtimeout -s 9 -k 5 2h                                env RR_MODE=FAST env JVM_ARGS="$JVM_ARGS ' + jvmArgs +'"  ./%command    -benchmark='+str(N) +'  -classpath=original.jar ' + defaultRRArgs + '  '

# The experiments to run to gather timing measurements.
baseExperiment =      MultiExperiment('BaseTime', standardCmd + " -tool=N -noinst", TRIALS, startNum=START)
ftExperimentV3 =        MultiExperiment('FastTrackV2', standardCmd + " -tool=FT2", TRIALS, startNum=START)
ftExperimentV1 =        MultiExperiment('FastTrackV1', standardCmd + " -tool=FT2-V1", TRIALS, startNum=START)
ftExperimentV2 =        MultiExperiment('FastTrackV1.5', standardCmd + " -tool=FT2-V1.5", TRIALS, startNum=START)
ftExperimentOld =        MultiExperiment('FastTrackOld', standardCmd + " -tool=tools.old.fasttrack.FastTrackTool", TRIALS, startNum=START)
ftExperimentOldCAS =        MultiExperiment('FastTrackCASOld', standardCmd + " -tool=tools.old.fasttrack_cas.FastTrackTool", TRIALS, startNum=START)
ftExperimentV4 =        MultiExperiment('FastTrackEnhancedV1', standardCmd + " -tool=FT2E-V1", TRIALS, startNum=START)
ftExperimentV4L =       MultiExperiment('FastTrackEnhancedV1L', standardCmd + " -tool=FT2EL-V1", TRIALS, startNum=START)
ftExperimentV5 =        MultiExperiment('FastTrackEnhanced', standardCmd + " -tool=FT2E", TRIALS, startNum=START)
ftExperimentV5L =       MultiExperiment('FastTrackEnhancedL', standardCmd + " -tool=FT2EL", TRIALS, startNum=START)
ftExperimentV6 =        MultiExperiment('FastTrackEnhancedV2', standardCmd + " -tool=FT2E-V2", TRIALS, startNum=START)
ftExperimentV7 =        MultiExperiment('FastTrackEnhancedV3', standardCmd + " -tool=FT2E-V3", TRIALS, startNum=START)
ftExperimentV8 =        MultiExperiment('FastTrackEnhancedV4', standardCmd + " -tool=FT2E-V4", TRIALS, startNum=START)


def getTime(e,row,outDir): 
    return e.getXMLCounter(row,outDir,'RRBench: Average')



def bootstrap_ratio(numers, denoms, num_samples, statistic, alpha):
    """Returns bootstrap estimate of 100.0*(1-alpha) CI for statistic for ratio of two sample sets."""
    nNumers = len(numers)
    nDenoms = len(denoms)
    nIdx = npr.randint(0, nNumers, (num_samples, nNumers))
    dIdx = npr.randint(0, nDenoms, (num_samples, nDenoms))
    nSamples = numers[nIdx]
    dSamples = denoms[dIdx]
    nStats = statistic(nSamples, 1)
    dStats = statistic(dSamples, 1)
    ratios = np.divide(nStats,dStats)
    stat = np.sort(ratios)
    low = stat[int((alpha/2.0)*num_samples)]
    high = stat[int((1-alpha/2.0)*num_samples)]
    return (low,high)

def bootstrap(data, num_samples, statistic, alpha):
    """Returns bootstrap estimate of 100.0*(1-alpha) CI for statistic."""
    n = len(data)
    idx = npr.randint(0, n, (num_samples, n))
    samples = data[idx]
    stat = np.sort(statistic(samples, 1))
    low = stat[int((alpha/2.0)*num_samples)]
    high = stat[int((1-alpha/2.0)*num_samples)]
    return (low,high)

def getTimings(experiment, row, outDir):
    times = []
    for i in range(1,N+1):
        times.extend(experiment.getXMLCounterAsRawList(row,outDir,'RRBench: Iter ' + str(i)))
    return times

# def confidenceIntervalForSlowdown(e, row, outDir):
#     rawBase = getTimings(e3, row, outDir)
#     rawE = getTimings
#     low,hi = bootstrap(bootstrap_ratio(np.array(rawE), np.array(rawBase)), 1000, scipy.stats.gmean, 0.05)

#     lowBase, hiBase = bootstrap(np.array(rawBase), 1000, np.mean, 0.021)
#     lowE, hiE = bootstrap(np.array(rawE), 1000, np.mean, 0.021)

#     return     str (round(np.mean(np.array(rawE)) / np.mean(np.array(rawBase)),1)) + ":" + str(round(low, 1)) + "-" + str(round(hi, 1)) + ":" + str(round(lowE/hiBase, 1)) + "-" + str(round(hiE/lowBase, 1))


def confidenceIntervalForSlowdownRatios(e1, e2, row, outDir):
    raw1 = getTimings(e1, row, outDir)
    raw2 = getTimings(e2, row, outDir)
    print raw1
    print raw2
    low, hi = bootstrap_ratio(np.array(raw1),np.array(raw2), 1000, np.mean, 0.05)
    return str(round(low, 3)) + "-" + str(round(hi, 3))


def makeOverhead(e,name='',title='c|',rowf='r|'):
    if name=='':
       name = e.abbrev
    return GeometricMeanColumn(name, 
                  lambda row, outDir: 
		               max(0.01, round(float(e.getXMLCounter(row,outDir,'RRBench: Average')) / float(baseExperiment.getXMLCounter(row,outDir,'RRBench: Average')), S) - 1),rowf,title,[],sideways=True)


def makeOverheadRatio(n,d,name='',title='c|',rowf='r|'):
    if name=='':
       name = e.abbrev    
    return GeometricMeanColumnP(name, 
                  lambda row, outDir: 
		                max(0.01, round(max(0.01, round(float(n.getXMLCounter(row,outDir,'RRBench: Average'))
                                                 / float(baseExperiment.getXMLCounter(row,outDir,'RRBench: Average')) - 1.0, S))
                                              / max(0.01, round(float(d.getXMLCounter(row,outDir,'RRBench: Average')) 
                                                 / float(baseExperiment.getXMLCounter(row,outDir,'RRBench: Average')) - 1.0 ,S)), S)),rowf,title,[],scale=S)

 
def makeErrors(e,name='',title='c|',row='r|'):
    if name=='':
       name = e.abbrev
    return SumColumn(name,
                  lambda row, outDir: 
		        e.getXMLEntryAsInt(row, outDir, './errorTotal'), row, title)


# Columns for the table

cols = [
    Column("", (lambda row, outDir: row.name), 'Geo Mean', '|l|', '|c|'),
    Column("(sec)", lambda row, outDir: round(baseExperiment.getXMLCounter(row,outDir,'RRBench: Average') / 1000.0, S), '','r|','c|'),
##    makeOverhead(ftExperimentOld,'FTOld'),
##    makeOverhead(ftExperimentOldCAS,'FTOldCAS'),
##    makeOverhead(ftExperimentV1,'VFT-v1'),
##    makeOverhead(ftExperimentV2,'VFT-v1.5'),
    makeOverhead(ftExperimentV4,'VFT-E-v1'),
##    makeOverhead(ftExperimentV6,'VFT-E-v2'),
#    makeOverhead(ftExperimentV7,'VFT-E-v3'),
    makeOverhead(ftExperimentV8,'VFT-E-v4'),
 #   makeOverhead(ftExperimentV6,'VFT-E-V2'),
    makeOverhead(ftExperimentV3,'VFT-v2'),
##    makeOverhead(ftExperimentV5,'VFT-E'),
              
#    Column("(ci)", lambda row, outDir: confidenceIntervalForSlowdownRatios(ftExperimentV3,ftExperimentOldCAS,row, outDir), '','c|','c|')
]

headers = [
    [Header('',1,'|c|'),
     Header('',1),
     Header('Overhead',3,'c|'),
     ],
    [Header('Program',1,'|c|'),
     Header('Time',1,'c|'),
     Header('',1),Header('',1), 
     Header('',1), #Header('',1),
#     Header('',1),
     ]
]

exps=[
    baseExperiment,
##    ftExperimentOldCAS,
##    ftExperimentV1,
##    ftExperimentV2,
    ftExperimentV4,
##    ftExperimentV6,
 #   ftExperimentV7,
    ftExperimentV8,
    #ftExperimentV6,
    ftExperimentV3,
##    ftExperimentV5,
##    ftExperimentOld,
]

perfTable =      Table('Performance', 'large-perf', headers,  javagrade_rows + dacapo_rows, cols, exps,'bench')
smallperfTable = Table('Performance', 'small-perf', headers,  rows_small, cols, exps,'bench')


############## ERRORS ###############

cols = [
    Column("Program", (lambda row, outDir: row.name), 'Total', '|l||', '|c||'),
##    makeErrors(ftExperimentOld,'FTOld', 'c|','r|'),
##    makeErrors(ftExperimentOldCAS,'FTOldCAS', 'c|','r|'),
##    makeErrors(ftExperimentV1,'VFT-v1', 'c|','r|'),
##    makeErrors(ftExperimentV2,'VFT-v1.5', 'c|','r|'),
    makeErrors(ftExperimentV4,'VFT-E-v1', 'c|','r|'),
##    makeErrors(ftExperimentV6,'VFT-E-v2', 'c|','r|'),
 #   makeErrors(ftExperimentV7,'VFT-E-v3', 'c|','r|'),
    makeErrors(ftExperimentV8,'VFT-E-v4', 'c|','r|'),
 #   makeErrors(ftExperimentV6,'VFT-E-V2', 'c|','r|'),
    makeErrors(ftExperimentV3,'VFT-v2', 'c|','r|'),
##    makeErrors(ftExperimentV5,'VFT-E', 'c|','r|'),
]

headers = [
    [Header('',1,'|c||'),Header('Warnings',3,'|c|')]
]

errorTable = Table('Performance', 'large', headers, javagrade_rows + dacapo_rows, cols, [],'bench')
smallErrorTable = Table('Performance', 'small', headers, rows_small, cols, [],'bench')

################ 
tables = [ perfTable, smallperfTable, errorTable, smallErrorTable ]

genRows = sys.argv[1]
genExps = sys.argv[2]

# Comment out this line if you want to regenerate data...
#genExps = "none"

genTables  = extractFromList(sys.argv[3], tables)

file = 'tables-perf'
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
