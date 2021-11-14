import grpc
import banking_pb2
import banking_pb2_grpc
import time
import json
import os.path
import asyncio 
import sys, getopt
from grpc import aio  


class Customer: #client
    def __init__(self, id, events):
        # unique ID of the Customer
        self.id = id
        # events from the input
        self.events = events
        # a list of received messages used for debugging purpose
        self.recvMsg = list()
        # pointer for the stub
        self.stub = None
        self.result = {}



    async def executeEvents(self):
        
       # the clinet reuqests will run async mode.

        async with grpc.aio.insecure_channel('localhost:4080'+str(self.id)) as ch:
            self.stub = banking_pb2_grpc.BankingStub(ch)
          
            if self.events['interface'] == "query" :
                await asyncio.sleep(3)
                req = banking_pb2.BankingRequest(id=self.id, interface = self.events['interface'],
                                             clock=1,c_id =0,
                                             remote_clock=0,
                                             e_id = 0,
                                             money = self.events['money'])
            
                await self.stub.MsgDelivery(req)
           

        
            else:
            
                print(f"start {self.events['interface']}  at  {time.strftime('%X')}")
                #await asyncio.sleep(1)
               
                req = banking_pb2.BankingRequest(id=self.id, interface = self.events['interface'],
                                             clock=1,
                                             c_id =self.events['id'],
                                             remote_clock=0,
                                             e_id = self.events['id'],
                                                money = self.events['money'])
                
            
                await self.stub.MsgDelivery(req)
                print(f"END {self.events['interface']}  at  {time.strftime('%X')}")


    
    def get_results(self, id):
        
        ch = grpc.insecure_channel('localhost:4080'+str(id))
        self.stub = banking_pb2_grpc.BankingStub(ch)
        
        req = banking_pb2.BResult(id=int(self.events['id']),type=self.events['interface'])
        self.stub.MsgResult(req)
    
async def fetch_customer(inputfile):
  
    processes =  json.load(open(inputfile,'r'))
 

    tsk = []
   
    for p in processes:
       

        if p['type'] == 'customer' or p['type'] == 'client':
  

            for e in p['events']:
                c = Customer(p['id'], e)
                task =  asyncio.create_task(c.executeEvents())
     
                tsk.append(task)
    
    await asyncio.gather(*tsk)
    

    for p in processes:
   
        if p['type'] == 'customer' or p['type'] == 'client':
            
            for e in p['events']:
                if e['interface'] != "query":
          
                    c = Customer(p['id'], e)
                    c.get_results(int(p['id']))
                elif len(p['events'])>1:
                    continue
                else:
     
                    c = Customer(p['id'], e)
                    c.get_results(int(p['id']))
        
def read_results():

        
        jfile1, jfile2 = [], []
        if os.path.exists("output1.json"):
                
            jfile1 = json.load(open("output1.json",'r'))
            
                

        if os.path.exists("output2.json"):
                
            jfile2 = json.load(open("output2.json",'r'))
        
        with open("output.json", 'w') as outfile:
             json.dump(jfile1+jfile2, outfile)

        print(jfile1+jfile2) 
        
inputfile =''
outputfile='output.json'
results = []
def readargs(argv):
    global inputfile
    global outputfile

    try:
        
        opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
        if len(opts) < 1:
            print(len(opts))
            print ('\nhelp: \n\tcustomer.py -i <inputfile> -o <outputfile>\n')
            sys.exit(2)    
    except getopt.GetoptError:
        
        print ('customer.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('customer.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
             outputfile = arg
if __name__ == "__main__":
    readargs(sys.argv[1:])
    asyncio.run(fetch_customer(inputfile))
    read_results()
   
