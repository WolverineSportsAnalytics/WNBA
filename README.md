[![Build Status](https://travis-ci.org/WolverineSportsAnalytics/WNBA.svg?branch=master)](https://travis-ci.org/WolverineSportsAnalytics/WNBA)
[![Coverage Status](https://coveralls.io/repos/github/WolverineSportsAnalytics/WNBA/badge.svg)](https://coveralls.io/github/WolverineSportsAnalytics/WNBA)
# Contributors:
    - Jake Becker
    - Evan Ciancio
    - Phillip Mathew
    - Justin Liss
    - Sri Garlapati
    - Brendan Hart
    - Christopher Castro
    - Cooper James
    - Drew Macleod
    - Shuzheng Zheng

# Overview

This is a repository to hold scripts for WolverineSportsAnalytics WNBA daily fantasy sports lineup Optimization

# Installation Instructions

#### Clone the repository 
Make a directory - note - make sure there are no spaces in file path

`git clone https://github.com/WolverineSportsAnalytics/WNBA.git`

`cd WNBA`

#### Install Virtual Env 
Virtual Env acts as a virtual environment so that we can virtually install python packages and not overwrite the ones 
on our system 

`pip install virtualenv`

#### Create Virtual Env and Enter it 
Go to your directory where you cloned the repository 

`$ virtualenv --python=/usr/bin/python2.7 ENV/`

Check your python version to see if you are running python 2.7

`$ python --version`

`$ source env/bin/activate`

#### Install the requirements
    - Make sure in home directory - try these to see if it works 

`pip install -r requirements.txt`


#### Deactivate the Virtual ENV
`$ deactivate`

##### Extra: If You Want to Install A New Package
    - make sure in home directory
    
`$ source bin/activate`

`pip install package`

`pip freeze > requirements.txt`

`$ deactivate`

