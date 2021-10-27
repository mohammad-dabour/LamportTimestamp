import branch
from concurrent import futures
import json
import grpc
import banking_pb2
import banking_pb2_grpc
import multiprocessing
import datetime
import time
import os
import sys, getopt
inputfile = ''
outputfile = 'output.txt'

def get_branches():
    processes =  json.load(open(inputfile,'r'))
    branches = list()
    for p in processes:
        if p['type'] == 'branch' or p['type'] == 'bank':
            branches.append(p['id'])
     
    return branches

def get_balance(id):
    processes =  json.load(open(inputfile,'r'))
    for p in processes:
        if (p['type'] == 'branch' or p['type'] == 'bank') and p['id'] == id:
            return p['balance']

def get_ids():
    processes =  json.load(open(inputfile,'r'))
    ids = list()
    for p in processes:
        if p['type'] == 'branch' or p['type'] == 'bank':
            ids.append(p['id'])
    return ids

_ONE_DAY = datetime.timedelta(days=1)
_PROCESS_COUNT = multiprocessing.cpu_count()
_THREAD_CONCURRENCY = _PROCESS_COUNT

def _wait_forever(server):
    try:
        while True:
            time.sleep(_ONE_DAY.total_seconds())
    except KeyboardInterrupt:
        server.stop(None)


        
def serve(bind_address, balance, branches):
        
        process = multiprocessing.current_process()
        print("PIDs:", process.pid)
        #options = (('grpc.so_reuseport', 1),)
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        banking_pb2_grpc.add_BankingServicer_to_server(branch.Branch(id, balance, branches), server)
        server.add_insecure_port(bind_address)
        server.start()
        #_wait_forever(server)
        server.wait_for_termination()



def main():
    
    
    ids = get_ids()
    branches = get_branches()
    workers = list()
    for id in ids:
        balance = get_balance(id)
        
        bind_address = '[::]:4080'+str(id)
        print("Starting server. Listning on port port  4080"+str(id))
        
        worker = multiprocessing.Process(target=serve,
                                             args=(bind_address,balance, branches))
        worker.start()
        workers.append(worker)
    
    for worker in workers:
        worker.join()
    

        
inputfile =''
outputfile=''

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
    main()
