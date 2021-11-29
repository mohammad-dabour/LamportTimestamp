import grpc
import banking_pb2
import banking_pb2_grpc
import time


class Branch(banking_pb2_grpc.BankingServicer):

    def __init__(self, id, balance, branches):
        # unique ID of the Branch
        self.id = id
        # replica of the Branch's balance
        self.balance = balance
        # the list of process IDs of the branches
        self.branches = branches
        # the list of Client stubs to communicate with the branches
        self.stubList = list() ## what is supposed to be included here?...
        # a list of received messages used for debugging purpose
        self.recvMsg = list()
        self.writeset = 0
        self.writesetOps = list()

        # iterate the processID of the branches

        
   

 
    def withdraw(self, money):
        
        print("at: withdraw current balance ", self.balance)
    
        if self.balance >= money:
           
            self.balance = self.balance - money
            #self.update("withdraw", money)
            
            return self.check_id(self.id, "withdraw", False)
            
            
        else:
            #ToDO return fail.
            return self.check_id(self.id, "withdraw", True)
        
       
        
    def check_id(self,id, action, fail=False):
        result = dict()
        if fail:
            result = {
                "id": self.id,
                "interface": action,
                "result": "fail",
                "money": self.balance

            }
        else:
            result = {
                "id": self.id,
                "interface": action,
                "result": "success",
                "money": self.balance

            }
        return result
    

    
    
    def update(self, new_balance):
            print("Update was called")
            if new_balance != self.balance:
                if new_balance > self.balance: # it means deposit
                    self.writeset = 1
                    self.writesetOps.append("deposit")
                if new_balance < self.balance: # it means withdraw
                    self.writeset = 2
                    self.writesetOps.append("withdraw")
                
                self.balance = new_balance
                return  self.check_id(self.id, "update", False)
            
            else:
                return  self.check_id(self.id, "update", True)


    
    def deposit(self, money):
        #print("before: deposit current balance ", self.balance)
        if money > 0:

            self.balance = self.balance + money
            #self.propagate("deposit", money)
            return  self.check_id(self.id, "deposit", False)
            
        else:
            return  self.check_id(self.id, "deposit", True)

            
    def query(self):

        #{'id': 1, 'recv': [{'interface': 'query', 'result': 'success', 'money': 500}]}
        r = self.check_id(self.id, "query", False)
  
        
        return  self.check_id(self.id, "query", False)

        #print("result", result)


    def MsgDelivery(self,request, context):
        
        
        if request.reset == True:
            print("To reset at interface?..  ", request.interface)
            self.writeset = 0
            self.writesetOps = list()
        #else:
            #print("No it is not ", request.reset)
        result = dict()
        self.id = request.id
        interface = request.interface
        money = request.money

        #withdraw, query, deposit
        if interface == "get_writeset":
            return banking_pb2.BankingReply(id=self.id, writeset = self.writeset)


        if interface == "withdraw":
            if request.writeset  == self.writeset:
                self.writesetOps.append("withdraw")
                #print("at withdraw request.writeset  = ",request.writeset , "self.writeset = ",self.writeset)
                result = dict(self.withdraw(money))
                self.writeset = 2
            else:
                while  request.writeset  != self.writeset:
                    #print("request.writeset  = ",request.writeset , "self.writeset = ",self.writeset)
                    time.sleep(1)
            
            
            for id in self.branches:
                ch = grpc.insecure_channel("localhost:4080"+str(id))
                stub = banking_pb2_grpc.BankingStub(ch)
        
                #self.stubList.append(stub)
                req = banking_pb2.BankingRequest(id=id, interface = "update",
                 money = result['money'],
                  writeset = self.writeset,
                  reset = request.reset)
                response = stub.MsgDelivery(req)
                if response.money != result['money']:
                    self.check_id(id, "withdraw", True)
            #print("after: withdraw current balance ", self.balance)
        elif interface == "deposit":
                
                '''
                make sure that caller'r writeset and current server writeset has same value 
                because this means they're both working over the latest  version of balance
                '''
                if request.writeset  == self.writeset:
                    #print(" at deposit request.writeset  = ",request.writeset , "self.writeset = ",self.writeset)
                    result = dict(self.deposit(money))
                    self.writesetOps.append("deposit")
                    
                    self.writeset = 1
                else:
                    #print("request.writeset  = ",request.writeset , "self.writeset = ",self.writeset)
                    while  request.writeset != self.writeset:
                        print("am here!!!!... and request.writeset = ",request.writeset , " self.writeset = ",self.writeset )
                        time.sleep(1)
                
                for id in self.branches:
                    
                    if id == self.id:
                        continue
                    ch = grpc.insecure_channel("localhost:4080"+str(id))
                    stub = banking_pb2_grpc.BankingStub(ch)
                    #print("after done?..", id, self.id)
                    req = banking_pb2.BankingRequest(id=id,
                     interface = "update",
                      money = result['money'],
                       writeset = self.writeset,
                       reset =  request.reset)
                       
                    response = stub.MsgDelivery(req)
                    #print("then here")
                    if response.money != result['money']:
                        self.check_id(id, "deposit", True)
                #print("after: deposit current balance ", self.balance)
        elif interface == "update":
            #print("I came here..")
            result = dict(self.update(money))
            #print("Done: new balance is: ", self.balance, " interface was deposit ")
        else:
            if request.writeset  == self.writeset:
                result = dict(self.query())
            else:
                while  request.writeset  != self.writeset:
                    time.sleep(1)
            
         
        return banking_pb2.BankingReply(id=self.id,
         interface = result['interface'],
          result = result['result'],
            money= result['money'],
             writeset = self.writeset)
