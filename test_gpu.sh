#!/bin/bash 

# Desc:
# 	Ensure the gpu is configured correctly

# Please ensure the following are pip installed:
#	- numpy
#	- scipy
#	- pycuda

# Ensure you are in (.venv2), via virtualenv 
#	if not type $ activate

# Ensure neon is installed via $ make

echo 'Are you running this script on myrtle? It doesnt work on other machines' 
read ans

if [ -z $LD_LIBRARY_PATH ]; then 
	echo "Add the following to the .bashrc"
	echo "export LD_LIBRARY_PATH=\"/usr/local/cuda/lib64:/usr/local/cuda/lib:/usr/local/lib:\"\$LD_LIBRARY_PATH"
fi


python -c "\
import service.olivia as oli; \
from os.path import expanduser as home;
attrs = oli.converter.get_attribute_vector(home('~/SaturnServer/test_resources/test_tile.jpg'));\
print attrs; \
print 'done'; \
"

