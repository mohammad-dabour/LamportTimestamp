import branch
from concurrent import futures
import json
import grpc
import banking_pb2
import banking_pb2_grpc
import multiprocessing
import time
import os
import sys, getopt
import subprocess
from os.path import exists

inputfile = ''
outputfile = 'output.txt'
class Server:
    
    def __init__(self,inputfile='input.json'):
        self.process = json.load(open(inputfile,'r'))
        self.pids = list()
    
    
    def get_branches(self):
        
        branches = list()
        for p in self.process:
            if p['type'] == 'branch' or p['type'] == 'bank':
                branches.append(p['id'])
     
        return branches
   
    def get_balance(self, id):

        for p in self.process:
            if (p['type'] == 'branch' or p['type'] == 'bank') and p['id'] == id:
                 return p['balance']

                
    def get_ids(self):
     
        ids = list()
        for p in self.process:
            if p['type'] == 'branch' or p['type'] == 'bank':
                ids.append(p['id'])
        return ids

    def add_pid(self, pid):
        
        if not exists('pids.run'):
            with open('pids.run','w') as f:
                f.write(str(pid)+" ")
              
        elif os.path.getsize("pids.run")==0:
            with open('pids.run','a') as f: 
                 f.write(str(pid)+" ")
        else:
            with open('pids.run','r') as f:
                if len(f.read().split(',')) >=len(self.get_branches()):
                    print("We have only ",self.get_branches()," opening, we can not open further branches.")
                    import sys
                    sys.exit(2)
            with open('pids.run','a') as f: 
                 f.write(str(pid)+" ")
    
    def stop(self):
        if exists('pids.run'):
            try:
                p = subprocess.run("kill -9 `cat pids.run`", shell=True, check=True)
                os.remove("pids.run")
            except subprocess.CalledProcessError as grepexc:                                                                                                   
                print("Failed to delete", grepexc.returncode)
                

        if not exists('pids.run'):
            return True
        else:
            return False
    def check_processes(self):
        if exists('pids.run') and os.path.getsize("pids.run") > 0:
            return True
            
    def serve(self, bind_address, balance, branches):
        
        process = multiprocessing.current_process()
        
        self.add_pid(process.pid)
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        banking_pb2_grpc.add_BankingServicer_to_server(branch.Branch(id, balance, branches), server)
        server.add_insecure_port(bind_address)
        server.start()
        #_wait_forever(server)
        server.wait_for_termination()
    

    def run(self):
    
    
        ids = self.get_ids()
        branches = self.get_branches()
        workers = list()
        for id in ids:
            balance = self.get_balance(id)
        
            bind_address = '[::]:4080'+str(id)
            print("Starting server. Listning on port port  4080"+str(id))
        
            worker = multiprocessing.Process(target=self.serve,
                                             args=(bind_address,balance, branches))
            worker.start()
            workers.append(worker)
    
        for worker in workers:
            worker.join()
        
    

        


def readargs(argv):
    global inputfile
    global outputfile
  
    try:
        
        opts, args = getopt.getopt(argv,"hi:so:",["ifile=","ofile="])
        if len(opts) < 1:
    
            print ('\nhelp: \n\tserver.py -i <inputfile>  | -s stop \n')
            sys.exit(2)    
    except getopt.GetoptError:
        
        print ('server.py -i <inputfile> | -s stop')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('help: \t\nserver.py -i <inputfile> ')
            sys.exit()
        elif opt == '-s':
            
            server = Server()
            if server.check_processes():
                f = server.stop()
                if not f:
                    print("Failed to shutdown gracefully")
                else:
                    print("All servers stopeed successfuly")
                    sys.exit(0)
            else:
                print("No service is running")
                sys.exit(0)
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
             outputfile = arg
                
if __name__ == "__main__":
    readargs(sys.argv[1:])
    server = Server(inputfile)
    server.run()
