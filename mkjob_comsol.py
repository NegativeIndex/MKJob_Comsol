#!/usr/bin/env python
"""
Create a job file for Comsol simulations
"""

import os,glob,sys,shutil,subprocess
import re,random
import logging,argparse

def analyze_mph_files(idx):
    """Analyze the \*.mph files and \*_Done.mph files in the current
    folder. Generate a to-do list for the next simulation. The
    function returns a string based on idx.
    
      * idx=0: return the summary of the folder
   
      * idx>0: return a mph name chosen from the head of the to-do
        list. The mph name is a string without mph extension. The
        returned name is a random pick from the first idx unfinished
        names.

      * idx<0: return a mph name chosen form the tail of the to-do list.

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
    if idx==0:
        return "{} simulaitons; {} finished; {} werid".format(nt,nd,nb);
    elif m==0:  # todofiles is empety
        return ""
    elif idx>0:  # random pick from the head
        n=min(idx,m)
        return random.choice(todofiles[0:n])
    else:   # random pick from the tail
        n=min(-idx,m)
        return random.choice(todofiles[m+idx:m])

#####
def generate_job_file():
    """ Generate the job file

    """
    rfolder='/Users/wdai11/python-study/MKJob_Comsol'
    shutil.copy2(os.path.join(rfolder,'dwt-comsol-job-file.job'),
                 './dwt-comsol.job')
    print('copy dwt-comsol.job')
    with open('dwt-comsol.job', 'r') as f:
        jobfile=f.readlines()



    return ""

######
def main(argv):
    """usage: mkjob_comsol.py [-h] [-a] [-i IDX] 

    The system arguments will be simply passed to the main
    function. The main function can generate a job file or analyze the
    folder with the mph files based on the argument.

    optional arguments:

      -h, --help         show this help message and exit

      -a, --analyze      Analyze the folder instead generate the job file

      -i IDX, --idx IDX  Kill all the jobs with a status

    """
    logging.basicConfig(level=logging.DEBUG,
                        format='%(levelname)s: %(message)s')

    # parse args
    ss="Generate a job file and analyze mph files"
    parser = argparse.ArgumentParser(description=ss)
    parser.add_argument('-a', '--analyze', 
                        action='store_true',default=False,
                        help="Analyze the folder instead generate the job file")

    parser.add_argument('-i', '--idx', action="store", 
                        type=int,default=0,
                        help="Kill all the jobs with a status")
    argv.pop(0)
    # logging.debug(argv)
    args = parser.parse_args(argv)
    # logging.debug(args)
    
    if args.analyze:
        # analyze the folder, return the next simulation name
        ss=analyze_mph_files(args.idx)
    else:
        # generate job file
        ss=generate_job_file()
    return ss




# def main(argv):
#     shutil.copy2('/Users/wdai11/bin/dwt-comsol-job-file.job','./dwt-comsol.job')
#     print('copy dwt-comsol.job')
#     with open('dwt-comsol.job', 'r') as f:
#         jobfile=f.readlines()


#     for idx, line in enumerate(jobfile):
#         if re.search('COMSOLCOMSOL',line):
#             break
#     jobfile.pop(idx)
 
    # for mph in mphfiles:
    #     mph2=re.sub(".mph$","_Done.mph",mph)
    #     mph_status=mph2+'.status'
    #     mph_recovery=mph2+'.recovery'
    #     logfile=re.sub(".mph$","_Log_${num}.txt",mph)
    #     if   (mph2 in mphfiles or re.search("_Done.mph",mph)):
    #         print("{} is finished".format(mph))
    #     else:
    #         print("Process {}".format(mph))
    #     # if code
    #     ss="if [ -f {} ]; then\n".format(mph2)
    #     jobfile.insert(idx,ss)
    #     idx+=1
    #     # done file exist
    #     ss='  echo "{} exist" '.format(mph2)
    #     ss+=" >>${recordname}\n"
    #     jobfile.insert(idx,ss)
    #     idx+=1
    #     # else
    #     ss='else\n'
    #     jobfile.insert(idx,ss)
    #     idx+=1
    #     # file don't exist, begin to run
    #     ss='  echo "{} to run" '.format(mph2)
    #     ss+=" >>${recordname}\n"
    #     jobfile.insert(idx,ss)
    #     idx+=1
        # ss="  comsol -nn 1 -np 28 batch "
        # ss+=" -inputfile {} ".format(mph)
        # ss+=" -outputfile {} ".format(mph2)
        # ss+=" -batchlog {} ".format(logfile)
        # ss+=" >>${recordname}\n"
        # jobfile.insert(idx,ss)
        # idx+=1
        # ss='  rm -v {}\n'.format(mph_status)
        # jobfile.insert(idx,ss)
        # idx+=1
        # ss='  rm -v {}\n'.format(mph_recovery)
        # jobfile.insert(idx,ss)
        # idx+=1
        # # if end
        # ss='fi\n\n'
        # jobfile.insert(idx,ss)
        # idx+=1
        # ss='echo "===============================" >> ${recordname}\n'
        # jobfile.insert(idx,ss)
        # idx+=1
        # ss='date >> ${recordname}\n\n'
        # jobfile.insert(idx,ss)
        # idx+=1


    #     res=subprocess.check_output(["unique-number"]).decode("utf-8").rstrip()
  
    # for idx, line in enumerate(jobfile):
    #     line=re.sub("CURRENTDIRECTORY", os.getcwd(), line)
    #     line=re.sub("MYJOBNAME", "dwt-comsol-"+res, line)
    #     jobfile[idx]=line


    # with open('dwt-comsol.job', 'w') as f:
    #     for line in jobfile:
    #         f.write("{}".format(line))



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
