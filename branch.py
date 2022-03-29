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
        self.money = 0
        
        self.recvMsg = list()
        
        # clock is going to be initilze here
        self.clock = clock

        self.e_id = -1
        self.sub_event = {}
        self.prop_req=False
        self.r_c =0
        self.withdraw_failed=False
      

        

    def event_request(self, event):
   

        self.clock = max(self.clock, self.r_c) + 1
        
        self.msg["data"].append({"id": self.e_id, "name": event+"_request", "clock": self.clock})
        
        self.sub_event[str(self.e_id)].append({"clock": self.clock, "name": event+"_request"})
     
        if event == "withdraw":
            if self.balance >= self.money:
                self.event_execute(event)
            else:

                self.withdraw_failed= True
               
                return banking_pb2.BankingReply(id=self.id, interface = "failed", clock = self.clock) 
        else:
            self.event_execute(event)

        

 
    def event_execute(self, event):
        
        
        if event == "withdraw":
                self.balance = self.balance  - self.money
       
        self.clock = self.clock+1
        self.msg["data"].append({"id": self.e_id, "name": event+"_execute", "clock": self.clock})
        self.sub_event[str(self.e_id)].append({"clock": self.clock, "name": event+"_execute"})
    

    
    def event_response(self,event):
        
        
        self.clock = self.clock+1

        self.sub_event[str(self.e_id)].append({"clock": self.clock, "name": event+"_response"})
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
            
        elif  request.type == "deposit":
            self.event_response("deposit")

        if not os.path.exists("output1.json"):

            with open("output1.json", 'w') as outfile:
                    json.dump([self.msg], outfile)
        else:
            
            jfile = json.load(open("output1.json",'r'))
            
            flag = True
            for msg in range(0,len(jfile)):
                if jfile[msg]['pid'] == self.msg['pid']:
                    #print("jfile[",msg,"] = ",jfile[msg],"\n")
                    #print("self.msg= ",self.msg,"\n")
                    jfile[msg] = self.msg
                    #print("after  ",jfile,"\n")
                    flag = False
         
            
            if flag:
                jfile.append(self.msg)


            with open("output1.json", 'w') as outfile:
                json.dump(jfile, outfile)

        if not os.path.exists("output2.json") and request.type != "query":
    

                with open("output2.json", 'w') as outfile:

                    event = {"eventid": str(self.e_id), "data": self.sub_event[str(self.e_id)]}
                    json.dump([event], outfile)

        elif request.type != "query":  
          
            jfile = json.load(open("output2.json",'r'))


            event = {"eventid": str(self.e_id), "data": self.sub_event[str(self.e_id)]}
            flag = True
           
            jfile.append(event)
   
            with open("output2.json", 'w') as outfile:
                    json.dump(jfile, outfile)


            
        return banking_pb2.BResult(id=self.id)

    def MsgDelivery(self,request, context):
        

       
        self.e_id = request.e_id
        interface = request.interface
        c_id = request.c_id
        self.money = request.money
        self.id = request.id
        
         
        remote_clock  = request.remote_clock
        self.r_c = remote_clock
  

        if request.interface != "query":
            if str(self.e_id) not in self.sub_event and interface != "deposit_propogate" and interface != "withdraw_propogate":
                
                self.sub_event[str(self.e_id)] = []

        if interface == "withdraw":
            
            
            saveit_withdraw = self.e_id
            
            self.event_request("withdraw")
     
            for id in self.branches:
                if id == self.id:
                      
                    continue
                if self.withdraw_failed:
                    return banking_pb2.BankingReply(id=self.id, interface = "failed", clock = self.clock) 

                    break
                
                self.prop_req+=1
                ch = grpc.insecure_channel("localhost:4080"+str(id))
                stub = banking_pb2_grpc.BankingStub(ch)
                req = banking_pb2.BankingRequest(id=id, 
                                                 interface = "withdraw_propogate",
                                                 c_id = saveit_withdraw,
                                                 remote_clock = self.clock,
                                                money = self.money)
                
                response = stub.MsgDelivery(req)
                self.e_id = saveit_withdraw
                self.clock=max(self.clock, response.clock)
                self.sub_event[str(saveit_withdraw)].append({"clock": response.clock-1, "name": "withdraw_propogate_request"})
                self.sub_event[str(saveit_withdraw)].append({"clock": response.clock, "name": "withdraw_propogate_execute"})
                self.e_id = saveit_withdraw
                self.event_propogate_response(self.e_id, "withdraw")
                self.sub_event[str(saveit_withdraw)].append({"clock": self.clock, "name": "withdraw_propogate_response"})

        elif interface == "deposit":
            
                self.balance = self.balance  + self.money 
                self.event_request("deposit")
               
                saveit_deposit = self.e_id
                
                
                for id in self.branches:
                    
                    if id == self.id:
                      
                        continue

                    ch = grpc.insecure_channel("localhost:4080"+str(id))
                    stub = banking_pb2_grpc.BankingStub(ch)
        
       
                    req = banking_pb2.BankingRequest(id=id, interface = "deposit_propogate",
                                                     c_id = saveit_deposit,
                                                     remote_clock = self.clock,
                                                    money = self.money)
                    response = stub.MsgDelivery(req)
                    self.e_id = saveit_deposit
                    self.clock=max(self.clock, response.clock)
                    print("AAwell i got saveit_deposit: "+str(self.e_id)," ", saveit_deposit, self.sub_event.keys())

                    self.sub_event[str(saveit_deposit)].append({"clock": response.clock-1, "name": "deposit_propogate_request"})
                    self.sub_event[str(saveit_deposit)].append({"clock": response.clock, "name": "deposit_propogate_execute"})
                   
                    print("is it zero deposit = ", self.e_id)
                    
                    self.event_propogate_response(self.e_id, "deposit")
                    self.sub_event[str(saveit_deposit)].append({"clock": self.clock, "name": "deposit_propogate_response"})
                    
        elif interface == "withdraw_propogate":
            
            self.balance = self.balance  - self.money 

            result = self.event_propogate_request(remote_clock,c_id,"withdraw")
            
            return banking_pb2.BankingReply(id=self.id, interface = "withdraw_propogate", clock = result['clock'])
         
            
        elif interface == "deposit_propogate":
            self.balance = self.balance  + self.money
            result = self.event_propogate_request(remote_clock,c_id,"deposit")
            
            return banking_pb2.BankingReply(id=self.id, interface = "deposit_propogate", clock = result['clock'])
        
        return banking_pb2.BankingReply(id=self.id, interface = "done", clock = self.clock)
