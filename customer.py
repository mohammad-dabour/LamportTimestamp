import grpc
import banking_pb2
import banking_pb2_grpc
import time
import json
import branch
from concurrent import futures
import multiprocessing
import datetime
import time
import asyncio 
import sys, getopt
from grpc import aio  
from multiprocessing import Process
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

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

        


    # TODO: students are expected to create the Customer stub
    def createStub(self):
       
        ch = grpc.insecure_channel('localhost:4080'+str(self.id))
        self.stub = banking_pb2_grpc.BankingStub(ch)
        #print(ch._connectivity_state.connectivity)
        
        
        #response = stub.SquareRoot(number)
        #print(response)

    # TODO: students are expected to send out the events to the Bank
  

    async def executeEvents(self):
        
       
        #self.createStub()
        async with grpc.aio.insecure_channel('localhost:4080'+str(self.id)) as ch:
            self.stub = banking_pb2_grpc.BankingStub(ch)
            #response = await stub.SayHello(helloworld_pb2.HelloRequest(name='you'))
            #print(e)
            #print(e['interface'])
            #req = banking_pb2.BankingRequest(id=self.id, interface = e['interface'], money = e['money'])
            if self.events['interface'] == "query" :
                await asyncio.sleep(3)
                req = banking_pb2.BankingRequest(id=self.id, interface = self.events['interface'],
                                             clock=1,c_id =0,
                                             remote_clock=0,
                                             e_id = 0)
            
                await self.stub.MsgDelivery(req)
                pass
                #await self.updates(e)
        
            else:
            
                print(f"start {self.events['interface']}  at  {time.strftime('%X')}")
            
            
                req = banking_pb2.BankingRequest(id=self.id, interface = self.events['interface'],
                                             clock=1,c_id =0,
                                             remote_clock=0,
                                             e_id = self.events['id'])
            
                await self.stub.MsgDelivery(req)
                
                
                print(f"END {self.events['interface']}  at  {time.strftime('%X')}")

        return 1
        #return {"interface": response.interface, 'result': response.result}


    
    def get_results(self, id):
        
        ch = grpc.insecure_channel('localhost:4080'+str(id))
        self.stub = banking_pb2_grpc.BankingStub(ch)
        
        req = banking_pb2.BResult(id=int(self.id),type=self.events['interface'])
        self.stub.MsgResult(req)
    
async def fetch_customer(inputfile):
  
    processes =  json.load(open(inputfile,'r'))
    #branches = list()
    tasks = {}
    tsk = []
    result = {}
    global results
    

   
    for p in processes:
       

        if p['type'] == 'customer' or p['type'] == 'client':
            tasks[str(p['id'])] = []
            result[str(p['id'])] = []
            result['recv'] = []

            for e in p['events']:
                c = Customer(p['id'], e)
                task =  asyncio.create_task(c.executeEvents())
                tasks[str(p['id'])].append(task)
                tsk.append(task)
    
    await asyncio.gather(*tsk)
    
    '''
    r = []
    resutl=[]
    for id in tasks.keys():
       
        for e in tasks[id]:
            r.append(await e)
    
    

        results.append(r[0])
        r =[]
    '''
    for p in processes:
   
        if p['type'] == 'customer' or p['type'] == 'client':
            
            for e in p['events']:
                if e['interface'] != "query":
                    print(p['id'], e)
                    c = Customer(p['id'], e)
                    c.get_results(int(p['id']))
                elif len(p['events'])>1:
                    continue
                else:
                    print(p['id'], e)
                    c = Customer(p['id'], e)
                    c.get_results(int(p['id']))

    

    

        

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
   
