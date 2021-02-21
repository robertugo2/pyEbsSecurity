# pyEbsSecurity
Python functions to interact with EBS Security API.
## Install
```commandline
mkdir pyEbsSecurity
cd pyEbsSecurity
git close https://github.com/robertugo2/pyEbsSecurity.git
pip install -r requirements
```
## Usage
Browse to src file in command line. Then open python3 interpreter:
```commandline
cd src
python3
```
Then you can import and use EbsSecurityLib class as follows:
```python
from EbsSecurityLib import EbsSecurityLib

# Init
ebs = EbsSecurityLib('ac-ebs.juwentus.pl/ava', '<your email>', '<your password/pin>')
# Get state of partition, True - armed, False - disarmed
# Note: 'get_arm' doesn't call api, it uses internal cache. 
#        To update a cache, please call 'update_partitions' function.
armStatus = ebs.get_arm(1)
# Arm partition number 1
# Note: set_arm automatically updates internal cache.
ebs.set_arm(1, True)
armStatus = ebs.get_arm(1) # armStatus will be True
# Disarm partition number 1
ebs.set_arm(1, False)
armStatus = ebs.get_arm(1) # armStatus will be False

# ... After some time ...

# Update internal cache
ebs.update_partitions()
# Get status of partiton 2
armStatus = ebs.get_arm(2)
```

## Description of classes
For full help for following classes, please open corresponding source code.
### src/EbsSecurityLib
It is high level handler of EBS Security API - wraps API into some user-friendly functionality-limited functions.
### src/EbsSecurity
Actual API class, that wraps API calls without further processing.