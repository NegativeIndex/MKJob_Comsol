Welcome to MKJob_Comsol's documentation!
****************************************


MKJob_Comsol module
===================

Create a job file for Comsol simulations

MKJob_Comsol.mkjob_comsol.analyze_mph_files(pick)

   Analyze the *.mph files and *_Done.mph files in the current folder.
   Generate a to-do list for the next simulation. The function returns
   a string based on pick.

      * pick=0: return the summary of the folder

      * pick>0: return a mph name chosen from the head of the to-do
        list. The mph name is a string without mph extension. The
        returned name is a random pick from the first pick unfinished
        names.

      * pick<0: return a mph name chosen form the tail of the to-do
        list.

MKJob_Comsol.mkjob_comsol.generate_job_file(args)

   Generate the job file. We have to supply several parameters to the
   job file: cpu, memory, queue and pick (analyze_mph_files
   parameter).

MKJob_Comsol.mkjob_comsol.main(argv)

   usage: mkjob_comsol.py [-h] [-a] [-i IDX]

   The system arguments will be simply passed to the main function.
   The main function can generate a job file or analyze the folder
   with the mph files based on the argument.

   optional arguments:

      -h, --help

      show this help message and exit

      -a, --analyze

      Analyze the folder instead generate the job file

      -p PICK, --pick PICK

      How to pick the next simulaiton

      -q QUEUE, --queue QUEUE

      Define a queue: (all.q|UI|INFORMATICS)

      -c CORE, --core CORE

      Number of cores

      -m MEMORY, --memory MEMORY

      Minimum of memory of the node


Indices and tables
******************

* Index

* Module Index

* Search Page
