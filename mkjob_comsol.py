#!/usr/bin/env python
"""
Create a job file for Comsol simulations.
"""

import os,glob,sys,shutil,subprocess
import re,random
import logging,argparse

def analyze_mph_files(pick):
    """Analyze the \*.mph files and \*_Done.mph files in the current
    folder. Generate a to-do list for the next simulation. The
    function returns a string based on pick.
    
      * pick=0: return the summary of the folder.
   
      * pick>0: return a mph name chosen from the head of the to-do
        list. The mph name is a string without mph extension. The
        returned name is a random pick from the first pick unfinished
        names. pick=1 means to choose the first one.

      * pick<0: return a mph name chosen form the tail of the to-do list.

    """
    mphfiles=glob.glob("*mph")
    logfiles=glob.glob("*Log.txt")
    mphfiles.sort()
    todofiles=[]
    nt=0 # total simulaitons
    nd=0 # finished simulations
    nb=0 # bad simulations

    for mph in mphfiles:
        if not re.search("mph$",mph):
            continue

        if  re.search("_Done.mph",mph):
            # end with Done
            mph2=re.sub("_Done","",mph)
            if mph2 in mphfiles:
                pass
            else:
                nb+=1
        else: 
            # not end with Done
            nt+=1
            mph2=re.sub("\.mph","_Done.mph",mph)
            # logging.debug(mph2)
            log=re.sub("\.mph","_Log.txt",mph)
            if mph2 in mphfiles and log  in logfiles:
                nd+=1
            else:
                mph3=re.sub("\.mph$","",mph)
                todofiles.append(mph3)
    
    # retrun a string
    m=len(todofiles)
    if pick is None: pick=0
    if pick==0:
        return "{} simulaitons; {} to do; {} finished; {} weird".format(
            nt,nt-nd,nd,nb);
    elif m==0:  # todofiles is empety
        return ""
    elif pick>0:  # random pick from the head
        n=min(pick,m)
        return random.choice(todofiles[0:n])
    else:   # random pick from the tail
        n=min(-pick,m)
        return random.choice(todofiles[m+pick:m])

#####
def generate_job_file(args):

    """Generate the job file. We have to supply several parameters to the
    job file: cpu, memory, queue and pick (analyze_mph_files parameter).

    """
    rfolder=os.path.dirname(os.path.realpath(__file__))
    jobname='./dwt-comsol.job'
    shutil.copy2(os.path.join(rfolder,'dwt-comsol-job-file.job'),
                 jobname)
    print('copy dwt-comsol.job')
    
    # read the job file
    with open(jobname, 'r') as f:
        jobfile=f.readlines()

    # change job file
    for idx, line in enumerate(jobfile):
        if args.queue is not None:
            if re.match('#\$ -q\s+([.\w]+)',line):
                jobfile[idx]='#$ -q {}\n'.format(args.queue)

        if args.core is not None:
            if re.match('#\$ -pe\s+(\d+)cpn\s+(\d+)',line):
                jobfile[idx]='#$ -pe {}cpn {}\n'.format(args.core,args.core)
            if re.match('ncore=(\d+)',line):
                jobfile[idx]='ncore={}\n'.format(round(args.core/2))
                
        if args.memory is not None:
            if re.match('#\$ -l\s+mt=(\d+)G',line):
                jobfile[idx]='#$ -l mt={}G\n'.format(args.memory)

        if args.pick is not None:
            if re.match('pick=([-\d]+)',line):
                jobfile[idx]='pick={}\n'.format(args.pick)
            

    # read the info
    nones = lambda n: [None for _ in range(n)]
    queue,core,memory,pick=nones(4)

    for idx, line in enumerate(jobfile):
        mobj=re.match('#\$ -q\s+([.\w]+)',line)
        if mobj:
            queue=mobj.group(1)    
        mobj=re.match('#\$ -pe\s+(\d+)cpn\s+(\d+)',line)
        if mobj:
            core=mobj.group(2)
        mobj=re.match('#\$ -l\s+mt=(\d+)G',line)
        if mobj:
            memory=mobj.group(1)    
        mobj=re.match('pick=([-\d]+)',line)
        if mobj:
            pick=mobj.group(1)    

    # write the job file
    with open(jobname, 'w') as f:
        for line in jobfile:
            f.write("{}".format(line))

       
    ss='queue={}, core={}, memory={}G, pick={}'.format(queue,core,memory,pick)    
    return ss


######
def main(argv):
    """usage: mkjob_comsol.py [-h] [-a] [-i IDX] 

    The system arguments will be simply passed to the main
    function. The main function can generate a job file or analyze the
    folder with the mph files based on the argument.

    optional arguments:

      -h, --help         show this help message and exit

      -a, --analyze      Analyze the folder instead generate the job file

      -p PICK, --pick PICK   How to pick the next simulaiton

      -q QUEUE, --queue QUEUE  Define a queue: (all.q|UI|INFORMATICS)

      -c CORE, --core CORE  Number of cores

      -m MEMORY, --memory MEMORY   Minimum of memory of the node


    """
    logging.basicConfig(level=logging.DEBUG,
                        format='%(levelname)s: %(message)s')

    # parse args
    ss="Generate a job file and analyze mph files"
    parser = argparse.ArgumentParser(description=ss)
    parser.add_argument('-a', '--analyze', 
                        action='store_true',default=False,
                        help="Analyze the folder instead generate the job file")

    parser.add_argument('-p', '--pick', action="store", 
                        type=int,default=None,
                        help="How to pick the next simulaiton")

    parser.add_argument('-q', '--queue',
                        default=None,
                        help="Define a queue: (all.q|UI|INFORMATICS)")
    parser.add_argument('-c', '--core', type=int,
                        default=None,
                        help="Number of cores")
    parser.add_argument('-m', '--memory', type=int,
                        default=None,
                        help="Minimum of memory of the node")

    argv.pop(0)
    # logging.debug(argv)
    args = parser.parse_args(argv)
    # logging.debug(args)
    
    if args.analyze:
        # analyze the folder, return the next simulation name
        ss=analyze_mph_files(args.pick)
    else:
        # generate job file
        ss1=generate_job_file(args)
        ss2=analyze_mph_files(0)
        ss=ss1+'\n'+ss2
    return ss
 


#########################
# main function
if __name__=='__main__':
    # clear screen
    # os.system('cls' if os.name == 'nt' else 'clear')
    args=sys.argv
    # args.pop()
    ss=main(args)
    # sys.exit(ss)
    print(ss)
