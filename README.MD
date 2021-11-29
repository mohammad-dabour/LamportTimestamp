### This script wont run over python2.7

### To install the requirements run the following command:


$ pip3.9 install -r requirements.txt 

### [Optional]:
$ python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. banking.proto 

### To run the server and provide it with inputs run:

$ python3.9 run.py  -i input.json -t server

### To run the customer/client and provide it with input:

$ python run.py  -i input.json -t customer

### output.json file on linux/mac
$ ls  output.json

#### To stop the server:

$ python run.py  -s stop

### Important note: IF you want to test 2 different inputs files, you need first to stop the server properly after the 1st input file and then read the outputs and then start it again with new input file and then read the output. so output file will be overwritten.
 $ python run.py  -s stop
 $ python3.9 run.py  -i input.json -t server
