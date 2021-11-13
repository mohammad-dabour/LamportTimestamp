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
      

        

    def event_request(self, event):
        self.clock = max(self.clock, self.r_c) + 1
        
        self.msg["data"].append({"id": self.e_id, "name": event+"_request", "clock": self.clock})
        self.sub_event["data"].append({"clock": self.clock, "name": event+"_request"})

        self.event_execute(event)

        

 
    def event_execute(self, event):

        self.clock = self.clock+1
        self.msg["data"].append({"id": self.e_id, "name": event+"_execute", "clock": self.clock})
        self.sub_event["data"].append({"clock": self.clock, "name": event+"_execute"})
    

    
    def event_response(self,event):
        self.clock = self.clock+1

        self.sub_event["data"].append({"clock": self.clock, "name": event+"_response"})
        self.msg["data"].append({"id": self.e_id, "name": event+"_response", "clock": self.clock})

        


    
    def event_propogate_request(self, remote_clock, c_id, event):

        self.clock = max(self.clock, remote_clock)+1
        self.msg["data"].append({"id": c_id, "name": event+"_propogate_request", "clock": self.clock})
        return self.event_propogate_execute(c_id, event)

    def event_propogate_execute(self, c_id, event):
            self.clock = self.clock+1
         
            self.msg["data"].append({"id": c_id, "name": event+"_propogate_execute", "clock": self.clock})
            return {"id": c_id, "name": event+"_propogate_execute", "clock": self.clock}
   
    def event_propogate_response(self, clock, event):
            self.clock +=1
            self.msg["data"].append({"id": self.e_id, "name": event+"_propogate_response", "clock": self.clock})
            
      





        
    
    def MsgResult(self, request, context):
        
        self.e_id = request.id
        if request.type == "withdraw":
            self.event_response("withdraw")
            
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
            
            self.event_response("deposit")

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
        #if interface != "query":
            
        self.e_id = request.e_id
         
        remote_clock  = request.remote_clock
        self.r_c = remote_clock
        if len(self.sub_event.keys()) == 0 and (interface == "withdraw" or interface=="deposit"):
            self.sub_event = {"eventid": self.e_id, "data": []}
        
    
       
        if interface == "withdraw":
            
            self.event_request("withdraw")
            saveit = self.e_id
            
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
                self.e_id = saveit
                self.event_propogate_response(self.e_id, "withdraw")
                self.sub_event["data"].append({"clock": self.clock, "name": "withdraw_propogate_response"})
      
        elif interface == "deposit":
            
                self.event_request("deposit")
                saveit = self.e_id
                
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
                    self.e_id = saveit
                    print("is it zero deposit = ", self.e_id)
                    
                    self.event_propogate_response(self.e_id, "deposit")
                    self.sub_event["data"].append({"clock": self.clock, "name": "deposit_propogate_response"})
              
        elif interface == "withdraw_propogate":

            result = self.event_propogate_request(remote_clock,c_id,"withdraw")

            return banking_pb2.BankingReply(id=self.id, interface = "withdraw_propogate", clock = result['clock'])
         
            
        elif interface == "deposit_propogate":
 
            result = self.event_propogate_request(remote_clock,c_id,"deposit")
            
            return banking_pb2.BankingReply(id=self.id, interface = "deposit_propogate", clock = result['clock'])
        
        return banking_pb2.BankingReply(id=self.id, interface = "done", clock = self.clock)
