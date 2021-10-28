import subprocess
import sys, getopt
import os
import time
inputfile=''
outputfile=''

def run(argv):
    global inputfile
    global outputfile
    cmd = ""
    try:
        
        opts, args = getopt.getopt(argv,"hi:sot:",["ifile=","ofile=","stop="])
        
        if len(opts) < 1:
    
            print ('\nhelp: \n\trun.py -i <inputfile> -o <outputfile> | -s stop \n')
            sys.exit(2)    
    except getopt.GetoptError:
        
        print ('run.py -i <inputfile> -o <outputfile>| -s stop')
        sys.exit(2)
        
    for opt, arg in opts:
        if opt == '-h':
            print ('run.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt == '-s':
            p = subprocess.run("/usr/bin/python3.9  server.py -s stop", shell=True, check=True)
            try:
                os.remove("nohup.out")
                os.remove("pids.run")
            except:
                pass
            sys.exit(0)
        elif opt in ("-i", "--ifile"):
            inputfile = arg
            cmd ="-i "+inputfile
        elif opt in ("-o", "--ofile"):
            outputfile = arg
            cmd ="-o "+outputfile
    try:
        p = subprocess.run("/usr/bin/python3.9  server.py -s stop >/dev/null", shell=True, check=True)
        try:
            os.remove("pids.run")
            os.remove("nohup.out")
        except:
            pass
    except subprocess.CalledProcessError as grepexc:    
        pass
 
    p = subprocess.run("nohup /usr/bin/python3.9  server.py "+cmd+" 2>/dev/null&", shell=True, check=True)
    print("starting services...\n")
    time.sleep(2)
    try:
        with open('./nohup.out') as f:
            for l in f.readlines():
                print(l)
    except IOError as e:
        print(" service did not start.", e)
    
if __name__ == "__main__":
    run(sys.argv[1:])
