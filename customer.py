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
    def __init__(self, id, events, reset = False):
        # unique ID of the Customer
        self.id = id
        # events from the input
        self.events = events
        # a list of received messages used for debugging purpose
        self.recvMsg = list()
        # pointer for the stub
        self.stub = None
        self.result = {}
        self.writeset = 0
        self.prev = 0
        self.reset = reset
        self.ops = list()
        self.prev_dest = None
        

        


    # TODO: students are expected to create the Customer stub
    def createStub(self):
       
        ch = grpc.insecure_channel('localhost:4080'+str(self.events['dest']))
        self.stub = banking_pb2_grpc.BankingStub(ch)
        #print(ch._connectivity_state.connectivity)
        
        
        #response = stub.SquareRoot(number)
        #print(response)

    # TODO: students are expected to send out the events to the Bank
    
    async def executeEvents(self):
    #def executeEvents(self):
        
        #response = None
        self.createStub()
        
        if self.prev_dest == None:
            req = banking_pb2.BankingRequest(id=self.events['dest'], interface = "get_writeset", reset = False)
        else:
            req = banking_pb2.BankingRequest(id=self.prev_dest, interface = "get_writeset", reset = False)

       
        response1 =  self.stub.MsgDelivery(req)
        self.prev_dest = self.events['dest']

        if self.reset:
            response1.writeset=0


        if self.events['interface'] == "query" :
            #await asyncio.sleep(3)
           
            
            req = banking_pb2.BankingRequest(
                id=self.events['dest'],
                interface = self.events['interface'],
                writeset = response1.writeset,
                reset = self.reset)

            response =  self.stub.MsgDelivery(req)
           
            return {"id": int(self.id), "balance": response.money,
             "writeset": response.writeset,
              "interface": self.events['interface'] }
        
        self.prev+=1
        
        req = banking_pb2.BankingRequest(id=self.events['dest'], 
        interface = self.events['interface'],
         money = self.events['money'],
          writeset = response1.writeset,
          reset = self.reset)

        response =  self.stub.MsgDelivery(req)
        #return None
        return {"id": int(self.id), "balance": response.money, "writeset": response.writeset ,"interface": self.events['interface']}


def check_read_write(events):

    c = 0
    for e in events:
        evt = ['deposit', 'withdraw']
        if e['interface'] in evt:
            c+=1
        elif c==1:
            return True
    
        
    return False



        


async def fetch_customer(inputfile):
  
    processes =  json.load(open(inputfile,'r'))
    #branches = list()
    tasks = {}
    result = {}
    #global results
    

    r = []
    reset = False
    check = False
    for p in processes:
       
  
        writeset = 0
        
        
        if p['type'] == 'customer' or p['type'] == 'client':
            tasks[str(p['id'])] = []
            result[str(p['id'])] = []
            #result['recv'] = []

            
           


            #tasks[str(p['id'])]['result']['recv']  = result['recv']
            check  = check_read_write(p['events'])
            q = []
            
            for e in p['events']:


                c = Customer(p['id'], e, reset)
                task =  asyncio.create_task(c.executeEvents())
                tasks[str(p['id'])].append(task)
                tasks[str(p['id'])].append(check)
                reset = False


                #result = c.executeEvents()
                ##writeset = result['writeset']

                #if e['interface'] == "query" and not check:
                #    r.append({"id": result['id'], "balance": result['balance']})
                #elif e['interface'] == "query" and  check:
                #     q.append(result['balance'])
            #if check:
            #    r.append({"id": p['id'], 'balance': q}) 
            chek = False
                


            reset = True
              
       
    r = []
    result=[]
    check = None
    for id in tasks.keys():
        q = []
        if True in tasks[id]:
            check = True
        elif False in tasks[id]:
            check = False

        for e in tasks[id]:
            if not isinstance(e,bool):
                result = await e
                print(result)

                if result['interface'] == "query" and not check:
                    print("am heree..", result, "check  = ", check)
                    
                    r.append({"id": result['id'], "balance": result['balance']})
       
                elif result['interface'] == "query" and  check:
                    q.append(result['balance'])
        if check:

            r.append({"id": result['id'], 'balance': q})
        

    
    
        
        print(r)
     
       
    with open(outputfile, 'a') as outfile:
        json.dump(results, outfile)

    #f = 
    print("This result will also be stored into output.json file:\n\n", r, "\n\n")

    with open(outputfile, 'w') as outfile:
        json.dump(r, outfile)

          

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
    #fetch_customer(inputfile)
    asyncio.run(fetch_customer(inputfile))
   
