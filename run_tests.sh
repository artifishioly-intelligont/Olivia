#!/bin/bash


# Description:
#	Runs all the python unit tests (given they start with 'test__', naming convention underneath)
# 
# Test Naming Convention:
# 	A test for a .py file must start with 'test__' followed by the name of the .py file.
#	It must also be in the same directory as the python file under test.
#	e.g. 
#		a test for 'Perceptron.py' would be named 'test__Perceptron.py'
# Usage:
# 	Will search current directory and sub directories for tests.
#	
# 	$./run_tests.sh
#
# Exit Codes:
#	 0 - Every test passed (or no tests found)
#	-1 - At least one test failed (check ./failed_tests.log to find which ones)
#
clear
echo '=============================================================='
echo '	                  run_tests.sh'
echo '=============================================================='
echo '--------------------------------------------------------------'
echo '          Copying test_resources to local area'
echo '--------------------------------------------------------------'
for file in ./test_resources/; do
    cp $file ~/SaturnServer/test_resources/
done
echo 'All copied'
echo;
echo '--------------------------------------------------------------'
echo '                 Searching for tests'
echo '--------------------------------------------------------------'
echo "Searching for tests in ${PWD}"
echo ''

tests=$(find . -name test__*.py)

if [[ -z $tests ]]; then
	echo 'No tests found, exiting.'
	exit 0
fi 

echo 'Tests found:'
for test in $tests; do 
	echo -e "\033[34m${test}"
done
echo -e "\033[39m"; echo;


echo '--------------------------------------------------------------'
echo '                 Setting up log'
echo '--------------------------------------------------------------'
rm passed_tests.log && true
 touch passed_tests.log
echo "Created ./passed_tests.log"

rm failed_tests.log && true
 touch failed_tests.log
echo "Created ./failed_tests.log"
echo; echo;

for test in $tests; do
	echo '--------------------------------------------------------------'
	echo -e "     test: \033[34m${test}\033[39m"
	echo '--------------------------------------------------------------'
	python $test

	# If the test failed
	if [ $? -ne 0 ]; then
		echo $test >> failed_tests.log
	else
		echo $test >> passed_tests.log
	fi	
done

echo -e "\033[39m"
echo '--------------------------------------------------------------'
echo '                 Results'
echo '--------------------------------------------------------------'
echo " Passed Tests:"
for test in $(cat ./passed_tests.log); do
    echo -e "\033[32m${test}"
done
echo -e "\033[39m"
echo " Failed Tests:"
for test in $(cat ./failed_tests.log); do
    echo -e "\033[31m${test}"
done
echo -e "\033[39m"
# If any tests failed then this script will exit with a fail exit code
#	a pass code is exit code 0
#	a fail code is any non-zero number 
if [ -s ./failed_tests.log ];then
	echo;
	echo -e '\033[31m=============================================================='
	echo -e "	    		    FAILED"
	echo -e '==============================================================\033[39m'
	echo 'At least one failed test, entire test failed'
	exit -1
else
	
	echo -e '\033[32m=============================================================='
	echo -e "	    		    PASSED"
	echo -e '==============================================================\033[39m'
	echo 'All tests passed'
fi

