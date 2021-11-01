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
        
       
        self.createStub()
        
            #print(e)
            #print(e['interface'])
            #req = banking_pb2.BankingRequest(id=self.id, interface = e['interface'], money = e['money'])
        if self.events['interface'] == "query" :
       
            await asyncio.sleep(3)
            req = banking_pb2.BankingRequest(id=self.id, interface = self.events['interface'], money = self.events['money'])
            response =  self.stub.MsgDelivery(req)   
            return {"interface": response.interface, 'result': response.result, 'money' : response.money}
        
                #await self.updates(e)
        
        req = banking_pb2.BankingRequest(id=self.id, interface = self.events['interface'], money = self.events['money'])
        response =  self.stub.MsgDelivery(req)
        return {"interface": response.interface, 'result': response.result}

async def fetch_customer(inputfile):
  
    processes =  json.load(open(inputfile,'r'))
    #branches = list()
    tasks = {}
    result = {}
    global results
    

   
    for p in processes:
       

        if p['type'] == 'customer' or p['type'] == 'client':
            tasks[str(p['id'])] = []
            result[str(p['id'])] = []
            result['recv'] = []
            #tasks[str(p['id'])]['result']['recv']  = result['recv']

            for e in p['events']:
                c = Customer(p['id'], e)
                task =  asyncio.create_task(c.executeEvents())
                tasks[str(p['id'])].append(task)
    r = []
    resutl=[]
    for id in tasks.keys():
       
        for e in tasks[id]:
            r.append(await e)
    
    
        print({'id': id, 'recv': r})
        results.append(r[0])
        r =[]
    with open(outputfile, 'a') as outfile:
        json.dump(results, outfile)

        
    #result[id].append(await e)
           

    

    

        

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
   
