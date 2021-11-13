import grpc
import banking_pb2
import banking_pb2_grpc
import asyncio 
import time
import os.path
import json
class Branch(banking_pb2_grpc.BankingServicer):

    def __init__(self, id, balance, branches, clock=1): 
        # unique ID of the Branch
        self.id = id
        # replica of the Branch's balance
        self.balance = balance
        # the list of process IDs of the branches
        self.branches = branches
        # the list of Client stubs to communicate with the branches
        self.stubList = list() ## what is supposed to be included here?...
        # a list of received messages used for debugging purpose
        self.msg = {"pid": self.id, "data": []}
        
        self.recvMsg = list()
        
        # clock is going to be initilze here
        self.clock = clock
        self.result = dict()
        self.e_id = self.id
        self.sub_event = {}
        self.result["pid"] = id
        self.result["data"] = []
        self.prop_req=False
        self.r_c =0
      

        

    def withdraw_request(self):
        
        self.clock = max(self.clock, self.r_c) + 1
        
        #if self.clock ==1:
        #    self.clock+=1
        self.msg["data"].append({"id": self.id, "name": "withdraw_request", "clock": self.clock})
        self.sub_event["data"].append({"clock": self.clock, "name": "withdraw_request"})
        self.withdraw_execute()
        

 
    def withdraw_execute(self):
        #if self.clock==2:
        #    self.clock = self.clock+1
        self.clock = self.clock+1
        self.msg["data"].append({"id": self.e_id, "name": "withdraw_execute", "clock": self.clock})
        self.sub_event["data"].append({"clock": self.clock, "name": "withdraw_execute"})
    
        
    
    def withdraw_response(self):
        self.clock = self.clock+1
        
        self.sub_event["data"].append({"clock": self.clock, "name": "withdraw_response"})
        self.msg["data"].append({"id": self.e_id, "name": "withdraw_response", "clock": self.clock})

        


    
    def withdraw_propogate_request(self, remote_clock, c_id):

        self.clock = max(self.clock, remote_clock)+1
     
        self.msg["data"].append({"id": c_id, "name": "withdraw_propogate_request", "clock": self.clock})
        return self.withdraw_propogate_execute(c_id)

    def withdraw_propogate_execute(self, c_id):
            self.clock = self.clock+1
         
            
            self.msg["data"].append({"id": c_id, "name": "withdraw_propogate_execute", "clock": self.clock})
            return {"id": c_id, "name": "withdraw_propogate_execute", "clock": self.clock}
   
    def withdraw_propogate_response(self, clock):
            self.clock +=1
            
            self.msg["data"].append({"id": self.e_id, "name": "withdraw_propogate_response", "clock": self.clock})
            
      


    def deposit_propogate_request(self, remote_clock ,c_id):
        self.clock = max(self.clock, remote_clock)+1

        self.msg["data"].append({"id": c_id, "name": "deposit_propogate_request", "clock": self.clock})
        return self.deposit_propogate_execute(c_id)
        

    def deposit_propogate_execute(self, c_id):
            self.clock = self.clock+1
            self.msg["data"].append({"id": c_id, "name": "deposit_propogate_execute", "clock": self.clock})
            return dict({"id": c_id, "name": "deposit_propogate_execute", "clock": self.clock})
    
    def deposit_propogate_response(self, clock):
        
            self.clock +=1

            self.msg["data"].append({"id": self.e_id, "name": "deposit_propogate_response", "clock": self.clock})



    def deposit_request(self):

        self.clock = max(self.clock, self.r_c)+1
        
        self.sub_event["data"].append({"clock": self.clock, "name": "deposit_request"})

        #internal operations does not need to sync time.
        self.msg["data"].append({"id": self.e_id, "name": "deposit_request", "clock": 2})

        self.deposit_execute()
    

    def deposit_execute(self):
        
        if self.clock ==2:
            self.clock+=1
        
        self.sub_event["data"].append({"clock": self.clock, "name": "deposit_execute"})

        self.msg["data"].append({"id": self.e_id, "name": "deposit_execute", "clock": 3})


        
    def deposit_response(self):
        
        self.clock = self.clock+1
        
        self.sub_event["data"].append({"clock": self.clock, "name": "deposit_response"})

        self.msg["data"].append({"id": self.e_id, "name": "deposit_response", "clock": self.clock})



        
    
    def MsgResult(self, request, context):
        
        
        if request.type == "withdraw":
            self.withdraw_response()
            
            if not os.path.exists("output1.json"):
                
                #processes =  json.load(open("output.json",'w'))
                with open("output1.json", 'w') as outfile:
                     json.dump([self.msg], outfile)
            else:
                
                jfile = json.load(open("output1.json",'r'))
                jfile.append(self.msg)
                with open("output1.json", 'w') as outfile:
                    json.dump(jfile, outfile)
                

            if not os.path.exists("output2.json"):
                #processes =  json.load(open("output.json",'w'))
                with open("output2.json", 'w') as outfile:
                     json.dump([self.sub_event], outfile) 
            else:
                
                jfile = json.load(open("output2.json",'r'))
                jfile.append(self.sub_event)
                with open("output2.json", 'w') as outfile:
                    json.dump(jfile, outfile)

        
        elif request.type == "deposit":
            
            self.deposit_response()
          
            #print(self.msg,"\n")
            #print(self.sub_event,"\n")
            if not os.path.exists("output1.json"):
                #processes =  json.load(open("output.json",'w'))
                
                with open("output1.json", 'w') as outfile:
                     json.dump([self.msg], outfile)
            else:
                a = []
                jfile = list(json.load(open("output1.json",'r')))
                
                jfile.append(self.msg)
                with open("output1.json", 'w') as outfile:
                    json.dump(jfile, outfile)
            
            if not os.path.exists("output2.json"):
                #processes =  json.load(open("output.json",'w'))
                with   open("output2.json", 'w') as outfile:
                     json.dump([self.sub_event], outfile) 
            else:
                
                jfile = json.load(open("output2.json",'r'))
                jfile.append(self.msg)
                with open("output2.json", 'w') as outfile:
                    json.dump(jfile, outfile)
        else:
            if not os.path.exists("output1.json"):
                
                #processes =  json.load(open("output.json",'w'))
                with open("output1.json", 'w') as outfile:
                     json.dump([self.msg], outfile)
            else:
                
                jfile = json.load(open("output1.json",'r'))
                jfile.append(self.msg)
                with open("output1.json", 'w') as outfile:
                    json.dump(jfile, outfile)
            
        return banking_pb2.BResult(id=self.id)

    def MsgDelivery(self,request, context):
        
        

        
        self.id = request.id
        interface = request.interface
        c_id = request.c_id
        self.e_id = request.e_id
        remote_clock  = request.remote_clock
        self.r_c = remote_clock
        if len(self.sub_event.keys()) == 0 and (interface == "withdraw" or interface=="deposit"):
            self.sub_event = {"eventid": self.e_id, "data": []}
        
        #if interface == "query":
        #    print(self.msg,"\n")
       
        if interface == "withdraw":
            
            self.withdraw_request()

            
            for id in self.branches:
                if id == self.id:
                      
                    continue
                    
                self.prop_req+=1
                ch = grpc.insecure_channel("localhost:4080"+str(id))
                stub = banking_pb2_grpc.BankingStub(ch)
                req = banking_pb2.BankingRequest(id=id, interface = "withdraw_propogate",
                                                 c_id = self.e_id,
                                                 remote_clock = self.clock)
                
                response = stub.MsgDelivery(req)

                self.clock=max(self.clock, response.clock)
                self.sub_event["data"].append({"clock": response.clock-1, "name": "withdraw_propogate_request"})
                self.sub_event["data"].append({"clock": response.clock, "name": "withdraw_propogate_execute"})

                self.withdraw_propogate_response(self.e_id)
                self.sub_event["data"].append({"clock": self.clock, "name": "withdraw_propogate_response"})
      
        elif interface == "deposit":
            
                self.deposit_request()

                
                for id in self.branches:
                    
                    if id == self.id:
                      
                        continue
              
                    ch = grpc.insecure_channel("localhost:4080"+str(id))
                    stub = banking_pb2_grpc.BankingStub(ch)
        
                
                    req = banking_pb2.BankingRequest(id=id, interface = "deposit_propogate",
                                                     c_id = self.e_id, remote_clock = self.clock)
                    response = stub.MsgDelivery(req)
                    
                    self.clock=max(self.clock, response.clock)
                    self.sub_event["data"].append({"clock": response.clock-1, "name": "deposit_propogate_request"})
                    self.sub_event["data"].append({"clock": response.clock, "name": "deposit_propogate_execute"})

                    self.deposit_propogate_response(self.e_id)
                    self.sub_event["data"].append({"clock": self.clock, "name": "deposit_propogate_response"})
              
        elif interface == "withdraw_propogate":
            ### check if clock >2 then go ahead else wait untile request is done.

            result = self.withdraw_propogate_request(remote_clock,c_id)

            return banking_pb2.BankingReply(id=self.id, interface = "withdraw_propogate", clock = result['clock'])
         
            
        elif interface == "deposit_propogate":
 
            result = self.deposit_propogate_request(remote_clock,c_id)
            
            return banking_pb2.BankingReply(id=self.id, interface = "deposit_propogate", clock = result['clock'])
        
        return banking_pb2.BankingReply(id=self.id, interface = "done", clock = self.clock)
