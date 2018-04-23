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

#
# This file defines the benchmarks used in the experiments.  Each
# defines a Row, which is comprised of a name, an abbreviation (must
# be unique), a directory, the command to start the program, and any
# extra flags to pass to RoadRunner.
#
# Most benchmarks contain the "-fancy" flag, which uses a "fancy"
# instrumentation mechanism to lower RoadRunner overhead for all tools
# by reducing the number of lookups in the Array -> Shadow Array map.
# (See the RoadRunner paper [PASTE 09] for details of that map.)  Two
# Dacapo programs (eclipse and tomcat) are not run with this
# optimization because it causes an internal JVM error that we have
# not been able to diagnose.
#

from tablelib import *

bench = ".."


# JGF 2
cr_crypt = Row('crypt', 'cryptc', bench + '/crypt', 'TEST_BENCH') 
cr_lufact = Row('lufact', 'lufactc', bench + '/lufact', 'TEST_BENCH') 
cr_series = Row('series', 'seriesc', bench + '/series', 'TEST_BENCH') 
cr_sor = Row('sor', 'sorc', bench + '/sor', 'TEST_BENCH') 
cr_sparse = Row('sparse', 'sparsematmultc', bench + '/sparsematmult', 'TEST_BENCH')

# JGF 3
br_moldyn = Row('moldyn', 'moldynb', bench + '/moldyn', 'TEST_BENCH') 
br_montecarlo = Row('montecarlo', 'montecarlob', bench + '/montecarlo', 'TEST_BENCH') 
br_raytracer = Row('raytracer', 'raytracerb', bench + '/raytracer', 'TEST_BENCH') 

javagrade_rows = [
 cr_crypt,
 cr_lufact,
 br_moldyn,
 br_montecarlo,
 br_raytracer,
 cr_series,
 cr_sor,
 cr_sparse
]

r_avrora = Row('avrora', 'avrora', bench + '/avrora', 'TEST_BENCH') 
r_batik = Row('batik', 'batik', bench + '/batik', 'TEST_BENCH') 
r_eclipse = Row('eclipse', 'eclipse', bench + '/eclipse', 'TEST_BENCH') 
r_fop = Row('fop', 'fop', bench + '/fop', 'TEST_BENCH') 
r_h2 = Row('h2', 'h2', bench + '/h2', 'TEST_BENCH')
r_jython = Row('jython', 'jython', bench + '/jython', 'TEST_BENCH') 
r_luindex = Row('luindex', 'luindex', bench + '/luindex', 'TEST_BENCH') 
r_lusearch = Row('lusearch', 'lusearch', bench + '/lusearch', 'TEST_BENCH') 
r_pmd = Row('pmd', 'pmd', bench + '/pmd', 'TEST_BENCH') 
r_sunflow = Row('sunflow', 'sunflow', bench + '/sunflow', 'TEST_BENCH') 

# Note: tomcat is patched to avoid StackOverflow exceptions.
#
# See: http://sourceforge.net/p/dacapobench/bugs/68/
#
# Tomcat *always* gets stuck in an infinite recusion and overflows the
# stack, violating the RR assumption that the program performs no
# jvm-level illegal operations.  Our options are to bulletproof every
# entry point into RR, since where exactly the StackOverflow exception
# is generated is JVM-dependent, not instrument the offending methods,
# or repair the code to avoid the infinite recursion.  We chose the
# last option with a patch from:
#
# http://mail-archives.apache.org/mod_mbox/tomcat-dev/200912.mbox/%3C20091216170201.ECA112388962@eris.apache.org%3E
#
# The patch is applied during the PREP phase of the TEST_BENCH script in the
# tomcat directory
#
r_tomcat = Row('tomcat', 'tomcat', bench + '/tomcat', 'TEST_BENCH') 

r_xalan = Row('xalan', 'xalan', bench + '/xalan', 'TEST_BENCH') 

dacapo_rows = [
r_avrora,
r_batik,
#r_eclipse, # doesn't work
r_fop,
r_h2,
r_jython,
r_luindex,
r_lusearch,
r_pmd,
r_sunflow, 
r_tomcat, 
r_xalan
]


# special rows for small data set
rows_small=[
    Row('crypt-a', 'crypta', bench + '/crypta', 'TEST_BENCH'),
    Row('lufact-a', 'lufacta', bench + '/lufacta', 'TEST_BENCH')
]
