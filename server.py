import branch
from concurrent import futures
import json
import grpc
import banking_pb2
import banking_pb2_grpc
import multiprocessing
import datetime
import time

def get_branches():
    processes =  json.load(open('input.json','r'))
    branches = list()
    for p in processes:
        if p['type'] == 'branch':
            branches.append(p['id'])
     
    return branches

def get_balance(id):
    processes =  json.load(open('input.json','r'))
    for p in processes:
        if p['type'] == 'branch' and p['id'] == id:
            return p['balance']

def get_ids():
    processes =  json.load(open('input.json','r'))
    ids = list()
    for p in processes:
        if p['type'] == 'branch':
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
        

        #options = (('grpc.so_reuseport', 1),)
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        banking_pb2_grpc.add_BankingServicer_to_server(branch.Branch(id, balance, branches), server)
        server.add_insecure_port(bind_address)
        server.start()
        _wait_forever(server)
        #server.wait_for_termination()

def main():
    
    ids = get_ids()
    branches = get_branches()
    workers = list()
    for id in ids:
        balance = get_balance(id)
        
        bind_address = '[::]:4080'+str(id)
        print("create server with id = ", str(id), " and port = 4080",str(id))
        worker = multiprocessing.Process(target=serve,
                                             args=(bind_address,balance, branches))
        worker.start()
        workers.append(worker)
    
    for worker in workers:
        worker.join()

main()
