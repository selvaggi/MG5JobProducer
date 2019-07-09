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
    parser.add_argument ('--pol', help='split polarisations (works only with VBS)', action='store_true')    
    parser.add_argument ('--decay', help='specify if W or Z decay', action='store_true')    

    parser.add_argument ('--queue', help='run time in s',
                       dest='queue',
                       default='3600')

    parser.add_argument ('--cpu', help='number of CPUs (1 cpu = 2 gb RAM)', default='1')

    args = parser.parse_args()

    outdir = os.path.abspath(args.outdir)
    mg5card = os.path.abspath(args.mg5card)
    cuts = os.path.abspath(args.cutfile)
    model = os.path.abspath(args.model)

    queue         = args.queue
    cpu           = args.cpu

    script = 'bin/submitMG.sh'

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


    cmdfile="""# here goes your shell script
executable    = {}

# here you specify where to put .log, .out and .err files
output                = configs/std/condor.$(ClusterId).$(ProcId).out
error                 = configs/std/condor.$(ClusterId).$(ProcId).err
log                   = configs/std/condor.$(ClusterId).log

+AccountingGroup = "group_u_CMST3.all"
+MaxRunTime = {}
RequestCpus = {}
""".format(script,queue,cpu)

    
    for job in xrange(args.njobs):

       seed = getuid2(2)

       #print 'Submitting job '+str(job)+' out of '+str(args.njobs)
       basename =  args.procname+ '_'+seed

       cwd = os.getcwd()

       basename = os.path.basename(outdir) + '_'+str(job)
       outputFile = outdir+'/'+basename+'.root'
       seed=str(job)

       cmdfile += 'arguments="{} {} {} {} {} {} {} {}"\n'.format(mg5card, args.procname, outdir, seed, str(args.nev), cuts, model, doPolarisations)
       cmdfile += 'queue\n'
       

    with open('configs/condor.sub', "w") as f:
        f.write(cmdfile)

    # submitting jobs
    os.system('condor_submit configs/condor.sub')
       

#_______________________________________________________________________________________
if __name__ == "__main__":
    main()

