import sys
import math
from sets import Set
# Setup PyROOT environment

import yaml
import glob 
import os
import zipfile
import re
import gzip 


def GetHeaderAndBody(infile):
     
     buf_head = []
     buf_body = []
     
     with gzip.open(infile) as fp:
         for result in re.findall('<LesHouchesEvents version="3.0">(.*?)</init>', fp.read(), re.S):
             buf_head.append(result)
     with gzip.open(infile) as fp:
         for result in re.findall('</init>(.*?)</LesHouchesEvents>', fp.read(), re.S):
             #print result
	     buf_body.append(result)
     

     #buf_head.insert(0,'</init>\n')
     buf_head.insert(0,'<LesHouchesEvents version="3.0">\n')
     buf_head.append('</init>\n')
     #buf_body.append('</LesHouchesEvent>\n')
     
     return buf_head, buf_body


if len(sys.argv) < 4:
  print(" Usage: python mergeLHE.py [process] [FCC/HELHC] [NEV_CHUNK]")
  sys.exit(1)

# parameters
process = sys.argv[1]
coll = sys.argv[2]
nevents_per_file = sys.argv[3]

l=process
indir = '/afs/cern.ch/work/h/helsens/public/FCCDicts/yaml/{}/lhe'.format(coll)


outfile=indir+'/'+l+'/merge.yaml'
totsize=0
totevents=0
process=None
outfiles=[]
outfilesbad=[]
outdir=None
ndone=0
nbad=0


nevents_per_file = 10000
ntemp = 0
list_of_files = []
final_name = []

All_files = glob.glob("%s/%s/events_*.yaml"%(indir,l))
print "%s/%s/events_*.yaml"%(indir,l)


print '%s/%s/check'%(indir,l)

print 'merging process %s  %i files'%(l,len(All_files))

i = 0
for f in All_files:
    i += 1
    if not os.path.isfile(f): 
        print 'file does not exists... %s'%f
        continue
    
    print f

    with open(f, 'r') as stream:
        try:
            tmpf = yaml.load(stream)
            lhefile = tmpf['processing']['out']
            list_of_files.append(lhefile)
            ndone+=1
                    
            head, body = GetHeaderAndBody(lhefile)
            # first file of chunk, extract header
            if ntemp == 0:
                print 'first file in chunk'
                final_name = lhefile
                #print head
                with open('tmp.lhe', 'w') as sf:
                    for ll in head:
                        sf.write(ll)
                    #for ll in body:
                    #   sf.write(ll)

            if not os.path.isfile(lhefile):
                continue
           
	    ntemp += tmpf['processing']['nevents']
            print ntemp, lhefile

            # append body here only
            with open('tmp.lhe', 'a') as sf:
                for ll in body:
		    sf.write(ll)
            
            # close file
            if ntemp > nevents_per_file or i == len(All_files):
                print 'reach max: dump into file'
                with open('tmp.lhe', 'a') as sf:
                    sf.write('</LesHouchesEvents>\n')
                if os.path.isfile('tmp.lhe.gz'):
                   os.system('rm tmp.lhe.gz')
                os.system('gzip tmp.lhe')
                
                print 'cleaning files that have been merged ...'
                for rf in list_of_files:
                    print rf
                    os.system('rm {}'.format(rf))
                
                print 'copying merged file'
                cmd = 'python /afs/cern.ch/work/h/helsens/public/FCCutils/eoscopy.py tmp.lhe.gz {}'.format(final_name)
                os.system(cmd)
                #os.system('rm tmp.lhe.gz')
                
                #/afs/cern.ch/work/h/helsens/public/FCCutils/eoscopy.py
                ntemp = 0
                list_of_files = []
                final_name = ''
                

        except yaml.YAMLError as exc:
            print(exc)
        except IOError as exc:
            print "I/O error({0}): {1}".format(exc.errno, exc.strerror)
            print "outfile ",f
 


