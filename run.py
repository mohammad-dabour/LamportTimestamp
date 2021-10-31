import subprocess
import sys, getopt
import os
import time
inputfile=''
outputfile=''
python_path = sys.executable 

def execute(cmd, types):
    
    if types == "server":
        cmd = "  server.py "+cmd
     
  
    
    elif types == "customer":
        cmd = "  customer.py "+cmd
 
    
    try:
        
        if types == "server":
            p = subprocess.run("nohup "+python_path +cmd+" 2>/dev/null&", shell=True, check=True)
            print("starting services...\n")
            time.sleep(2)
        
            try:
                with open('./nohup.out') as f:
                    for l in f.readlines():
                        print(l)
            except IOError as e:
                print(" service did not start.", e)
        else:
            print("running your request..")
            p = subprocess.run(python_path +cmd, shell=True, check=True)
    
    except subprocess.CalledProcessError as grepexc:    
        print("Failed to start..")
        sys.exit(2)

def run(argv):
    global inputfile
    global outputfile
    cmd = ""
    types=""
    try:
        
        opts, args = getopt.getopt(argv,"hi:t:s",["ifile=", "type=","stop="])
        
        if len(opts) < 1:
    
            print ('\nhelp: \n\trun.py -i <inputfile>  -t server/customer | -s stop \n')
            sys.exit(2)    
    except getopt.GetoptError:
        
        print ('run.py -i <inputfile> -o <outputfile>| -s stop')
        sys.exit(2)
   
    for opt, arg in opts:
        
        if opt == '-h':
            print ('run.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt == '-s':
            p = subprocess.run(python_path +" server.py -s stop", shell=True, check=True)
            time.sleep(2)
            try:
                os.remove("nohup.out")
                os.remove("pids.run")
            except:
                pass
            sys.exit(0)
            
        elif opt in ("-i", "--ifile"):
           
            inputfile = arg
            cmd ="-i "+inputfile
        
        elif opt in ("-t", "--type"):
            types = arg
          
    execute(cmd, types)


    
if __name__ == "__main__":
    run(sys.argv[1:])
