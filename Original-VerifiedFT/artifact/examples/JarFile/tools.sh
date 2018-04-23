#!/bin/bash

echo
echo "###  build all java files"
javac -source 1.7 -target 1.7 *.java

echo
echo "###  create jar file will all class files"
jar -cf program.jar *.class

echo
echo "###  run normally --  sanity check"
java -classpath program.jar BlockedArrayMain

echo
echo "###  run in RoadRunner"
base_rrrun -quiet -noxml -classpath=program.jar BlockedArrayMain

echo
echo "###  run with VerifiedFT version 2"
vft_v2_rrrun -quiet -noxml -classpath=program.jar BlockedArrayMain

echo
echo "###  run with VerifiedFT version 1"
vft_v1_rrrun -quiet -noxml -classpath=program.jar BlockedArrayMain

echo
echo "###  run with VerifiedFT version 1.5"
vft_v1.5_rrrun -quiet -noxml -classpath=program.jar BlockedArrayMain

echo
echo "###  run with Original Mutex-based FastTrack"
ft_old_rrrun -quiet -noxml -classpath=program.jar BlockedArrayMain

echo
echo "###  run with Original CAS-based FastTrack"
ft_cas_old_rrrun -quiet -noxml -classpath=program.jar BlockedArrayMain


