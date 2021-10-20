import grpc
import banking_pb2
import banking_pb2_grpc
import time
import json

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

        


    # TODO: students are expected to create the Customer stub
    def createStub(self):
       
        ch = grpc.insecure_channel('localhost:4080'+str(self.id))
        self.stub = banking_pb2_grpc.BankingStub(ch)
        #print(ch._connectivity_state.connectivity)
        
        
        #response = stub.SquareRoot(number)
        #print(response)

    # TODO: students are expected to send out the events to the Bank
    def executeEvents(self):
        result = {}
        result['id'] = self.id
        result['recv'] = []
        
        for e in self.events:
            #print(e)
           
            req = banking_pb2.BankingRequest(id=self.id, interface = e['interface'], money = e['money'])
         
            response = self.stub.MsgDelivery(req)
            
            result['recv'].append( {"interface": response.interface, 'result': response.result, 'money' : response.money}  )
        print(result)
   
    





def fetch_customer():

    processes =  json.load(open('input.json','r'))

    for p in processes:
        if p['type'] == 'customer':
          
            c = Customer(p['id'], p['events'])
            c.createStub()
            c.executeEvents()
 
fetch_customer()
