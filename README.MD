### This project does not support python2.x

Its meant to implement The Lamport timestamp algorithm which is a simple logical clock algorithm used to determine the order of events here the event is a  banking transaction over dummy banking system. I used gRPC asyncio. The main purpose of this project was to impement Lamport timestamp algorithm..however a possible improvment for this dummy project can be  converting client side to API using flask which I might do later, note this is just a proof of concept of logical clock for event ordering, so I used the Async to show how it works.


### To install the requirements run the following command:


$ pip3.9 install -r requirements.txt 

### [Optional]:
$ python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. banking.proto 

### To run the server and provide it with inputs run:

$ python3.9 run.py  -i input.json -t server

### To run the customer/client and provide it with input:

$ python run.py  -i input.json -t customer

### To find the output file..
$ ls  output.json

#### To stop the server:

$ python run.py  -s stop

### output.json file on linux/mac
 $ ls output.json
