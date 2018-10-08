#!/usr/bin/env python
import os, sys, subprocess
import argparse
import commands
import time
import random

#____________________________________________________________________________________________________________
### processing the external os commands
def processCmd(cmd, quite = 0):
    status, output = commands.getstatusoutput(cmd)
    if (status !=0 and not quite):
        print 'Error in processing command:\n   ['+cmd+']'
        print 'Output:\n   ['+output+'] \n'
    return output


#__________________________________________________________
def getuid2(user):
    
    seed = '%i%i%i%i%i%i%i%i%i'%(random.randint(1,9),
                                 random.randint(0,9),
                                 random.randint(0,9),
                                 random.randint(0,9),
                                 random.randint(0,9),
                                 random.randint(0,9),
                                 random.randint(0,9),
                                 random.randint(0,9),
                                 random.randint(0,9))
    return seed
    

#_____________________________________________________________________________________________________________
def main():
    parser = argparse.ArgumentParser()

    parser.add_argument ('--mg5card', help='mg5 config file',  default='card.mg5')
    parser.add_argument ('--cutfile', help='cuts.f file for additional cuts',  default='cuts.f')
    parser.add_argument ('--model', help='model tarball',  default='model.tgz')
    parser.add_argument ('--outdir', help='output directory e.g. /eos/experiment/fcc/hh/generation/process', default='.')
    parser.add_argument ('--procname', help='process name', default='')
    parser.add_argument ('--njobs', help='number of jobs ', type=int, default=2)
    parser.add_argument ('--nev', help='number of events per job', type=int, default=10000)
    parser.add_argument ('--queue', help='master lsf queue', default='8nh')
    parser.add_argument ('--memory', help='min virtual memory', default='4000')
    parser.add_argument ('--disk', help='min disk space',       default='2000')
    parser.add_argument ('--pol', help='split polarisations (works only with VBS)', action='store_true')    

    args = parser.parse_args()

    outdir = os.path.abspath(args.outdir)
    mg5card = os.path.abspath(args.mg5card)
    cuts = os.path.abspath(args.cutfile)
    model = os.path.abspath(args.model)

    doPolarisations = "false"
    if args.pol:
       doPolarisations = "true"

    jobsdir = './BatchOutput/' + args.procname

    if not os.path.exists(jobsdir):
       os.makedirs(jobsdir)
       os.makedirs(jobsdir+'/std/')
       os.makedirs(jobsdir+'/cfg/')

    print '[Submitting jobs]'
    jobCount=0
    
    for job in xrange(args.njobs):

       seed = getuid2(2)

       print 'Submitting job '+str(job)+' out of '+str(args.njobs)
       basename =  args.procname+ '_'+seed

       cwd = os.getcwd()
       script = cwd + '/bin/submitMG.sh '
       
       cmd = 'bsub -o '+jobsdir+'/std/'+basename +'.out -e '+jobsdir+'/std/'+basename +'.err -q '+args.queue
       cmd += ' -R "rusage[mem={}:pool={}]"'.format(args.memory,args.disk)
       cmd +=' -J '+basename+' "'+script+mg5card+' '+args.procname+' '+outdir+' '+seed+' '+str(args.nev)+' '+cuts+' '+model+' '+doPolarisations+'"'
       
       print cmd
       
       # submitting jobs
       output = processCmd(cmd)
       while ('error' in output):
           time.sleep(1.0);
           output = processCmd(cmd)
           if ('error' not in output):
               print 'Submitted after retry - job '+str(jobCount+1)
       
       jobCount += 1
#_______________________________________________________________________________________
if __name__ == "__main__":
    main()

