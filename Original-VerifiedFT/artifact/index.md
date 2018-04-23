## VerifiedFT: A Verified, High-Performance Precise Dynamic Race Detector
James Wilcox (University of Washington)
<br>
Cormac Flanagan (University of California, Santa Cruz)
<br>
Stephen Freund (Williams College)


## Overview

This artifact accompanies our paper "VerifiedFT: A Verified, High-Performance Precise Dynamic Race Detector" presented at PPoPP '18.  It contains the infrastructure to use our race detection tools and to run the CIVL program verifier.   

The instructions below assume that the contents of this artifact have been placed in the directory `~/workspace/`.

This instruction file can be found in `~/workspace/RoadRunner/artifact/index.html`. 

Below you will find Quick Start instructions for running FastTrack and VerifiedFT on some small prorgams and verifying the algorithm with CIVL.
We then provide more detailed discussion of how to:

1. reproduce our benchmark experiments.  
2. validate the CIVL verification proof.

#### Machine Specs

We used a machine with a 16 core AMD Opteron processor and 64GB of memory to generate the results in the paper.  A similarly-sized machine or VM should be able to run all experiments.

* **Default:** A machine with 42GB of memory and 8 CPUs is adequate to repeat all experiments.  We have configured RoadRunner to use 40GB by default.

* **Minimal:** With 16GB, most tests should still run, but a number of the largest benchmarks may have either degraded performance or fail.  At least four cores should be used.

#### Software

This artifact relies on various software packages, most notably Java (1.7 or 1.8) and CIVL (which is distributed as part of the Boogie system). 

You should clone and build CIVL in `~/workspace/boogie`.  The following will clone the specific version of CIVL we used from github:

~~~diff
> cd ~/workspace/
> git clone https://github.com/boogie-org/boogie.git
> cd boogie
> git checkout 17a8832d9bfccac07b81debe09f50b832c964f5c
~~~

Follow the Boogie installation instructions for your particular system.  We built, 

The RoadRunner directory should be readily portable to any reasonable computer, though our benchmark scripts will require Python, pdflatex, gtimeout, and possibly other additional packages to be installed.


## Quick-Start

	
1. Set up environment variables and checking tools. Verify that the `PROGRAM_ARGS` variable reflects the number of cores on the machine.

	~~~diff
	> cd ~/workspace/RoadRunner
	> source msetup
	...lots of output...
	> ant
	...lots of output...
	> printenv PROGRAM_ARGS
	8
	~~~
* Use VerifiedFT to check a simple program. (This and all other examples are in `~/workspace/RoadRunner/artifact/examples`).
	- Compile the `BlockedArrayAccess` source file.  This program uses four threads to write into a large array.  It divides the array into 4 disjoint blocks to avoid races

		```diff
		> cd ~/workspace/RoadRunner/artifact/examples/BlockedArrayAccess
		> cat BlockedArrayAccess.java
		...
		public class BlockedArrayAccess {
         ...
		}
		...
		> javac -source 1.7 -target 1.7 BlockedArrayAccess.java
		```
	  We specify the javac 1.7 source and target because the RoadRunner framework 
	  does not fully support checking Java 1.8 class files yet.  You may get a warning
	  about the "bootstrap class path", which can be ignored.


	- Run the program in RoadRunner (with no analysis).

		```diff	
		> base_rrrun -quiet -noxml BlockedArrayAccess
		...
		[main: ----- ----- ----- -----       Meep Meep.      ----- ----- ----- -----]
		[main: ]
		[main: ]
		[main: ----- ----- ----- -----      Thpthpthpth.     ----- ----- ----- -----]
		[RR: Total Time: 50]
		```
		The Total Time is the time to run that target in milliseconds.
		The `Meep Meep` and `Thpthpthpth` lines delineate the start/end of the target's execution.
		The command line flags have the following meaning:
		- `-quiet` turns off most RoadRunner logging messages.
		- `-noxml` turns off printing an XML diagnostic summary at the end of the run.
		
		You may run without those flags to see more details, although most of the output will not be relevant at the moment.
	      
      
	- Run VerifiedFT (version 2) on the program.

		```diff	
		> vft_v2_rrrun -quiet -noxml BlockedArrayAccess
		...
		[RR: Total Time: 1263]
		```
		This program is free of races, so no errors are reported.
		
	- Count the fraction of accesses on which the three optimized fastpaths are taken.

		```diff	
		> ft_count -quiet -noxml BlockedArrayAccess
		...
		Write Same Epoch:       0.166667
		Read Same Epoch:        0.166668
		Read Shared Same Epoch: 0.333332
		------------------------------------
		All Fast Paths:         0.666667
		...
		```
		The number of field accesses is negligible, so these ratios reflect the array accesses.  See the source code for a full accounting of which path each access will take. 		
	- VerifiedFT and FastTrack variants can be run with commands similar to the above:

	
		```diff	
		> # VerifiedFT version 1
		> vft_v1_rrrun -quiet -noxml BlockedArrayAccess
		...
		[RR: Total Time: 2862]
		
		> # VerifiedFT version 1.5
		> vft_v1.5_rrrun -quiet -noxml BlockedArrayAccess
		...
		[RR: Total Time: 2366]
		
		> # Original Mutex-Based FastTrack
		> ft_old_rrrun -quiet -noxml BlockedArrayAccess
		...
		[RR: Total Time: 1584]

		> # Original CAS-Based FastTrack
		> ft_cas_old_rrrun -quiet -noxml BlockedArrayAccess
		...
		[RR: Total Time: 1227]

		```

4. Checking other Examples.  You can repeat these steps on the other examples that illustrate a racy program, and how to handle programs larger than a single class.
 
	* `BlockedArrayAccessRacy`:  Same as previous, but with two workers and a missing join operation, leading to a race on array index a[5000000] through a[9999999], on line 37.  (RoadRunner is configured to report only the first race on each syntactic field declaration or array instruction, so we see only one message.  The `-maxWarn` flag controls this.)
	
		```diff
		> cd ~/workspace/RoadRunner/artifact/examples/BlockedArrayAccessRacy
		> cat BlockedArrayAccessRacy.java
	   ...
		> javac -source 1.7 -target 1.7 BlockedArrayAccessRacy.java
		> base_rrrun -quiet -noxml BlockedArrayAccessRacy
	 	> vft_v2_rrrun -quiet -noxml BlockedArrayAccessRacy
		...
		## 
		## =====================================================================
		## FastTrack Error
		## 
		##          Thread: 0    
		##           Blame: wr_array@BlockedArrayAccessRacy.java:37:51
		##           Count: 1    (max: 1)
		##      Alloc Site: null
		##    Shadow State: [W=(2:3) R=(0:0) V=[]]
		##  Current Thread: [tid=0    C=[(0:5) (1:3) (2:0) (3:0)]   E=(0:5)]
		##           Array: @02[5000000]
		##         Message: Write-Write Race
		##     Previous Op: Write by  null
		##     Currrent Op: Write by  main[tid = 0]
		##           Stack: tools.fasttrack.FastTrackTool.arrayError(FastTrackTool.java:768)
		##                  tools.fasttrack.FastTrackTool.error(FastTrackTool.java:750)
		##                  tools.fasttrack.FastTrackTool.write(FastTrackTool.java:512)
		##                  tools.fasttrack.FastTrackTool.access(FastTrackTool.java:305)
		##                  rr.tool.RREventGenerator.arrayWrite(RREventGenerator.java:584)
		##                  BlockedArrayAccessRacy.__$rr_main__$rr__Original_(BlockedArrayAccessRacy.java:37)
		##                  BlockedArrayAccessRacy.main(BlockedArrayAccessRacy.java:22)
		##                  ...
		##                  
		## =====================================================================
		## 
		...
		```
		The same error will be reported when the other variants are used.
	
	* `MultipleClasses`: This example is similar to `BlockedArrayAccess` but uses two classes. It shows how testing a program containing more than one class file is essentially the same.  We provide the script `tools.sh` to perform the same steps as above under this scenario.  It can be used as a model for writing and running other tests using multiple classes.
	
		```diff
		> cd ~/workspace/RoadRunner/artifact/examples/MultipleClasses
		> ./tools.sh
		###  build all java files
		...
		###  run normally --  sanity check
		...
		###  run in RoadRunner
		...
		###  run with VerifiedFT version 2
		...
		###  run with VerifiedFT version 1
		...
		###  run with VerifiedFT version 1.5
		...
		###  run with Original Mutex-based FastTrack
		...
		###  run with Original CAS-based FastTrack
		```
	
	* `JarFile`: Same as the previous, but for classes stored in a jar file rather than class files (which is how the benchmarks are packaged.)  The script `tools.sh` performs the same steps as above under this scenario.  It can be used as a model for writing and running other tests using jar files.
	
		```diff
		> cd ~/workspace/RoadRunner/artifact/examples/JarFile
		> ./tools.sh
		###  build all java files
		...
		###  create jar file will all class files
		...
		###  run normally --  sanity check
		...
		###  run in RoadRunner
		...
		###  run with VerifiedFT version 2
		...
		###  run with VerifiedFT version 1
		...
		###  run with VerifiedFT version 1.5
		...
		###  run with Original Mutex-based FastTrack
		...
		###  run with Original CAS-based FastTrack
		...
		```
	
4. Run CIVL on our VerifiedFT CIVL implementation.  Our code is is located in `~/workspace/RoadRunner/artifact/civl/verified-ft.bpl`.  It should take about 20 seconds on a reasonable machine.  

	~~~diff
	> cd ~/workspace/RoadRunner/artifact/civl/
	> mono ~/workspace/boogie/Binaries/Boogie.exe -noinfer -useArrayTheory verified-ft.bpl 
	Boogie program verifier version 2.3.0.61016, Copyright (c) 2003-2014, Microsoft.
	
	Boogie program verifier finished with 322 verified, 0 errors
	~~~
	

## Benchmarks

* **Running a benchmark progam.** The benchmark programs from the [JavaGrande](https://www2.epcc.ed.ac.uk/computing/research_activities/java_grande/threads/contents.html) and [DaCapo](http://dacapobench.org/) suites are in `~/workspace/RoadRunner/benchmarks`.  	We provide variants of the commands above to run the benchmarks with each tool. 

	The following will run the program for 15 iterations of the benchmark workload after three iterations to warm up the VM.  Note: we do not use the `-noxml` flag here.

	```diff
	> cd ~/workspace/RoadRunner/benchmarks/lufacta
	> bench_base_rrrun       -quiet -warmup=3 -benchmark=15
	> bench_vft_v1_rrrun     -quiet -warmup=3 -benchmark=15
	> bench_vft_v1.5_rrrun   -quiet -warmup=3 -benchmark=15
	> bench_vft_v2_rrrun     -quiet -warmup=3 -benchmark=15
	> bench_ft_old_rrrun     -quiet -warmup=3 -benchmark=15
	> bench_ft_cas_old_rrrun -quiet -warmup=3 -benchmark=15
	```

   The output for each one of these will include XML timing data for each iteration, and also the average of the benchmark iterations.
   
   	```
	<counter><name> "RRBench: Warmup 1" </name>                          <value>         92 </value> </counter>
    <counter><name> "RRBench: Warmup 2" </name>                          <value>         41 </value> </counter>
    <counter><name> "RRBench: Warmup 3" </name>                          <value>         30 </value> </counter>
    <counter><name> "RRBench: Iter 1" </name>                            <value>         16 </value> </counter>
    <counter><name> "RRBench: Iter 2" </name>                            <value>         25 </value> </counter>
    ...
    <counter><name> "RRBench: Iter 15" </name>                           <value>         31 </value> </counter>
    <counter><name> "RRBench: Average" </name>                           <value>         27 </value> </counter>
   	```
    
    The `bench_ft_count` command will output the fast path ratios for FastTrack in the same format as before.  The ratios will be over all of the benchmark runs.  (The raw operation counts can be found in the XML output).
  
   	```diff
	> bench_ft_count -quiet -noxml -warmup=3 -benchmark=15
	...
	Write Same Epoch:       0.0104076
	Read Same Epoch:        0.0218640
	Read Shared Same Epoch: 0.319649
	------------------------------------
	All Fast Paths:         0.351921
	...
   	```
 
	 
	 
* **Benchmark File Structure.** Each benchmark is in its own subdirectory and contains the following files:
	 * `RRBench.java`: The driver we wrote for RoadRunner's benchmarking feature.
	 * `original.jar`: The complete code for the benchmark, including `RRBench.class`.  (Source code for the benchmarks can be found via the links to the original sources above.)
	 * Various other scripts and log files that glue together the various pieces of our infrastructure and provide any special configuration options for each program.  You should not need to use these directly.
	 
	We include two **small** benchmarks --- crypta and lufacta --- to illustrate the experiment workflow.
	Our full set of **large** benchmarks includes avrora, batik, crypt, fop, h2, jython, lufact, luindex, lusearch, moldyn, montecarlo, pmd, raytracer, series, sor, sparsematmult, sunflow, tomcat, xalan.


* **Running Full Tests.**  We provide a number of shell and Python scripts to automatically run the tools and gather the data presented in the paper.  Whenever running these scripts, the actual commands used to drive the underlying tools are printed to the terminal.
The full run of all benchmarks takes multiple days to complete, so we have provided a number of simpler options to use here.

	* Small Test of crypt and lufact with size A (small) workloads.  Those two programs are run for one trial, where each trial starts a VM, performs the workload 3 times as warmup, and then measures the average time of 10 runs.

		```diff
		> cd ~/workspace/RoadRunner/benchmarks/Experiments
		> # Run 1 trial of 10 iterations on crypta and lufacta 
		> ./SMALL_TESTS   # About 5-10 minutes
		```

		The data generated by `SMALL_TESTS` is stored in the `table-bench` sub-directory (with names that should be intuitively clear).  It is summarized in the following files in the directory `~/workspace/RoadRunner/benchmarks/Experiments/`:
		* Table 1: [small-tables-perf.pdf](../../RoadRunner/benchmarks/Experiments/small-tables-perf.pdf)
		* Fast Path Frequencies: [small-tables-stats.pdf](../../RoadRunner/benchmarks/Experiments/small-tables-stats.pdf)
			
		The supporting data in CSV format is also in that directory: `small-stats.csv`,`small-perf.csv`.

	* Large Tests of all benchmarks.  These will take longer to run.  Here we show three experiments like the above.  These show varying numbers of trials and iterations with each trial:
		
		```diff
		> # Run 1 trial of 1 iterations each, on all benchmarks
		> ./LARGE_TESTS 1 1  # 5-10 hours      
		
		> # Run 1 trial of 10 iterations each, on all benchmarks
		> ./LARGE_TESTS 10 1  # About 12-24 hours      
		
		> # Run 5 trials of 10 iterations each, on all benchmarks 
		> ./LARGE_TESTS 10 5  # About 2-4 days      
		```
		
		You can also run the tests for a single benchmark as follows:
		
		```diff
		> # Run 1 trial of 10 iterations each, 
		> # on given benchmark only (use dir name to identify benchmark)
		> ./ONE_LARGE_TEST lufact 10 1   # varies: typically 1-4 hours
		```

		The following does the same for all benchmarks, but with 10 trials of 10 iterations.  (This matches the experiments in the paper.)
			
		~~~diff
		> # Run 10 trials of 10 iterations each
		> # on all benchmarks 
		> ./LARGE_TESTS 10 10              # About 4-8 days
		~~~
	
		The data generated by `LARGE_TESTS` and the other scripts above follows the same format as the small 	tests, and all of the log files are also in the directory `~/workspace/RoadRunner/benchmarks/Experiments/`:  
	
		* Table 1: [tables-perf.pdf](../../RoadRunner/benchmarks/Experiments/tables-perf.pdf)
		* Fast Path Frequencies: [tables-stats.pdf](../../RoadRunner/benchmarks/Experiments/tables-stats.pdf)
	
		The supporting data in CSV format is also in that directory: `large-stats.csv`,`large-perf.csv`.  		You may see some discrepencies in the number of errors reported because the exact trace observed may impact the races reported.  

	
* **Benchmark Results.** These show the full results for our test machine:
	* **Test Machine: 2.4GHz 16-core AMD Opteron processor with 64GB running Ubuntu Linux**.
The data is in `~/workspace/RoadRunner/benchmarks/Experiments-16CoreAMD`.  We used ten trials of 10 iterations for the run-time tests.  Here are the top-level graphs and tables from that directory:
		* Table 1: [tables-perf.pdf](../../RoadRunner/benchmarks/Experiments-16CoreAMD/tables-perf.pdf)
		* Fast Path Frequencies: [tables-stats.pdf](../../RoadRunner/benchmarks/Experiments-16CoreAMD/tables-stats.pdf)

	The results are mostly consistent across platforms, although several benchmarks have pretty different performance profiles when run inside a VM on different hosts.  This can lead to some variability in relative the performance between our various tools.
	

## CIVL Algorithm Proof

The file `~/workspace/RoadRunner/artifact/civl/verified-ft.bpl` contains the VerifiedFT algorithm written in CIVL.  (It has been ported to the latest version of CIVL since we submitted the paper, and it is a bit longer than what the paper claims as a result of changes in how methods are specified.   The event handlers `Read`, `Write`, `Fork`, `Join`, `Acquire`, and `Release` are the core of the algorithm.  Each is declared as a refinement of an atomic specification, as in:

~~~
procedure {:yields} {:layer 20} {:refines "AtomicRelease"} Release({:linear "tid"} tid: Tid, l: Lock)
~~~
The `AtomicRelease` is the atomic specification of the `Release` code.  The atomic specifications embody the formal analysis rules from the paper, and the event handler implementations reflect the Version 2 code.

We illustrate that CIVL is indeed verifying the appropriate correctness properties for our algorithm by showing the errors that are reported when we introduce several small bugs into our algorithm.

* Example 1:  The top-level `Driver` function models threads performing arbitrary operations that adhere to the well-formed trace assumptions.  If we add `false` as a post-condition, CIVL will be unable to verify that the code meets the specification.  To do this, search for the line containing `"ARTIFACT EXAMPLE 1"` and uncomment it:

	~~~
	// ensures {:layer 30} false; // ARTIFACT EXAMPLE 1: uncomment this line
	~~~

	CIVL now reports an error:

	~~~diff
	> cd ~/workspace/RoadRunner/artifact/civl
	> mono ~/workspace/boogie/Binaries/Boogie.exe  -noinfer -typeEncoding:m -useArrayTheory  ./verified-ft.bpl 
	...
	verified-ft.bpl(1120,1): Error BP5003: A postcondition might not hold on this return path.
	...
	~~~

   Revert this change to the original.

* Example 2:  Comment out the line labelled `"ARTIFACT EXAMPLE 2"` inside the `Release` function to remove the increment to the current thread's clock:

	~~~
	call VC.Inc(tid, ShadowableTid(tid), tid);  // ARTIFACT EXAMPLE 2: comment out this line
	~~~
	
	CIVL now reports that `Release` does not conform to its spec:
	
	~~~diff
	> mono ~/workspace/boogie/Binaries/Boogie.exe  -noinfer -typeEncoding:m -useArrayTheory  ./verified-ft.bpl 
	...
	verified-ft.bpl(774,3): Error: Transition invariant in initial state violated
	...
    ~~~ 

   Revert this change to the original.

* Example 3:  Similarly, comment/uncomment the lines labelled `"ARTIFACT EXAMPLE 3"` inside the `Release` specification to (incorrectly) assert that the current thread's clock increment does not change:

	~~~
    assume VCArrayGet(shadow.VC[v2], tid) == EpochInc(VCArrayGet(shadow.VC.old[v2], tid));   // ARTIFACT EXAMPLE 3: comment out this line
    // assume shadow.VC[v2] == shadow.VC.old[v2];                                            // ARTIFACT EXAMPLE 3: uncomment this line
	~~~
	
	CIVL will again report that the spec. is not satisfied.
	
	
## Code Structure and Building

The RoadRunner source can be recompiled as follows:

```diff
> cd ~/workspace/RoadRunner
> source msetup
> ant clean
> ant 
```

The RoadRunner tool classes for the five FastTrack implementations are the following:

* VerifiedFT Version 1: [~/workspace/RoadRunner/src/tools/fasttrack/FastTrackToolV1.java](../src/tools/fasttrack/FastTrackToolV1.java)
* VerifiedFT Version 1.5: [~/workspace/RoadRunner/src/tools/fasttrack/FastTrackToolV15.java](../src/tools/fasttrack/FastTrackToolV15.java)
* VerifiedFT Version 2: [~/workspace/RoadRunner/src/tools/fasttrack/FastTrackTool.java](../src/tools/fasttrack/FastTrackTool.java)
* Original FasTrack Mutex: [~/workspace/RoadRunner/src/tools/old/fasttrack/FastTrackTool.java](../src/tools/old/fasttrack/FastTrackTool.java) 
* Original FasTrack CAS: [~/workspace/RoadRunner/src/tools/old/fasttrack_cas/FastTrackTool.java](../src/tools/old/fasttrack_cas/FastTrackTool.java) 

This artifact relies on various other software packages, most notably CIVL (which is distributed as part of the Boogie system).  The RoadRunner directory should be readily portable to any reasonable computer, though our benchmark scripts will require Python, latex, and several other additional packages to be installed.
   
## Known Issues

* None