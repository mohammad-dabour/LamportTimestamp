import grpc
import banking_pb2
import banking_pb2_grpc

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
        # iterate the processID of the branches

        
        # TODO: students are expected to store the processID of the branches
        #pass
      
    # TODO: students are expected to process requests from both Client and Branch
    #def crate_branch_stub(self, id):
            
    #    ch = grpc.insecure_channel("localhost:4080"+str(id))
    #    stub = banking_pb2_grpc.BankingStub(ch)
    #    
    #    return stub
 
    def withdraw(self, money):
        

    
        if self.balance >= money:
           
            self.balance = self.balance - money
            #self.update("withdraw", money)
            return self.check_id(self.id, "withdraw", fail=False)
            
            
        else:
            #ToDO return fail.
            return self.check_id(self.id, "withdraw", fail=True)
        
       
        
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
    
            if new_balance != self.balance:
                self.balance = new_balance
                return  self.check_id(self.id, "update", fail=False)
            
            else:
                return  self.check_id(self.id, "update", fail=True)


    
    def deposit(self, money):
        
        if money > 0:
            self.balance = self.balance + money
            #self.propagate("deposit", money)
            return  self.check_id(self.id, "deposit", fail=False)
            
        else:
            return  self.check_id(self.id, "deposit", fail=True)

            
    def query(self):
        #{'id': 1, 'recv': [{'interface': 'query', 'result': 'success', 'money': 500}]}
        r = self.check_id(self.id, "query", fail=False)
  
        
        return  self.check_id(self.id, "query", fail=False)

        #print("result", result)
    
    def MsgDelivery(self,request, context):
        

        
        result = dict()
        self.id = request.id
        interface = request.interface
        money = request.money
        #withdraw, query, deposit
        if interface == "withdraw":
            result = dict(self.withdraw(money))
            
            for id in self.branches:
                ch = grpc.insecure_channel("localhost:4080"+str(id))
                stub = banking_pb2_grpc.BankingStub(ch)
        
                #self.stubList.append(stub)
                req = banking_pb2.BankingRequest(id=id, interface = "update", money = result['money'])
                response = stub.MsgDelivery(req)
                if response.money != result['money']:
                    self.check_id(id, "withdraw", True)
            
        elif interface == "deposit":
            
                result = dict(self.deposit(money))
                
                for id in self.branches:
                    if id == self.id:
                        continue
                    ch = grpc.insecure_channel("localhost:4080"+str(id))
                    stub = banking_pb2_grpc.BankingStub(ch)
        
                     #self.stubList.append(stub)
                    req = banking_pb2.BankingRequest(id=id, interface = "update", money = result['money'])
                    response = stub.MsgDelivery(req)
                    if response.money != result['money']:
                        self.check_id(id, "deposit", True)
        
        elif interface == "update":
            result = dict(self.update(money))
            #print("Done: new balance is: ", self.balance, " interface was deposit ")
        else:
            result = dict(self.query())
         
        return banking_pb2.BankingReply(id=self.id, interface = result['interface'], result = result['result'],  money= result['money'])
