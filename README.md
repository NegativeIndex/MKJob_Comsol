# MKJob_Comsol
Generate a job file for Comsol simulations on Argon cluster


## v1.0 (10/31/2019)

   * **dwt-comsol-job-file.job** is the template job file

   * **mkjob-comsol.py** is the command to generate the job file.


## v2.0 (11/01/2019)

   Since we have the lincence restriction, I cannot use the
   embarrassingly parallel strategy. I have to run a series of
   simulations in serial.

   There are two ways to run Comsol simulation on Argon cluster. One
   method is to run Matlab code. This method worked but I got the
   licence problem recently. I don't want to spend time to solve the
   problem. So I take the second method. I generates a series of mph
   files with all the parameters defined; then moved the mph files to
   the cluster and ran these files. It seems Comsol can handle the
   licence better than Matlab with Comsol.
