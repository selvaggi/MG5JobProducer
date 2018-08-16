import os, sys, subprocess

kws = ['090', '095', '098', '100', '102', '105', '110']

pols=['TT','LL','TL']

queue = '2nw'
njobs='200'
nevents='5000'

process='mg_pp_vbs_wwss_kw'

for k in kws:
    cmd='python bin/submitMGjobs.py --mg5card examples/pp_vbs_wwss_kw_{}.mg5  --model models/sm_kw.tar --outdir /eos/experiment/fcc/hh/generation/lhe/ --procname {}_{} --njobs {} --nev {} --queue {} --pol'.format(k,process, k,njobs,nevents,queue)
    print cmd
    #os.system(cmd)

'''
# fix wrong names
for k in kws:
    for p in pols:
        cmd='mv /eos/experiment/fcc/hh/generation/lhe/pp_vbs_wwss_kw_{}_{}  /eos/experiment/fcc/hh/generation/lhe/mg_pp_vbs_wwss_kw_{}_{} '.format(k,p,k,p)
        print cmd
'''


'''
paramFile = 'param.py'
br_ww_2l2v = 0.0466

# extract cross sections from lhe files and logs and write in param file form
os.system('rm param.py')
for k in kws:

    print ' '
    print '     pp_vbs_wwss_kw_{}'.format(k)
    print ' '
    
    # pick up one stdout file that contains at least 5k events

    batchjobs_dir = 'BatchOutput/pp_vbs_wwss_kw_{}/std/'.format(k)

    cmd = "find {} -type f -name '*.out'".format(batchjobs_dir)
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    lst = proc.communicate()[0]
    list_of_files = lst.splitlines()

    ngood_files = 0
    
    crosssection = 0.

    ftt = 0.
    ftl = 0.
    fll = 0.
    
    for log in list_of_files:

        bad_file = False
        nev = -1
        xsec = -1.
        frac_tt = -1.
        frac_tl = -1.
        frac_ll = -1.

        with open(log) as f:

            for line in f:
                if 'Nb of events' in line:
                    list_of_words = line.split(":",1)
                    nev=int(list_of_words[1])

                if 'Cross-section' in line:
                    list_of_words = line.split()
                    if any("Cross-section" in s for s in list_of_words):
                       xsec = float(list_of_words[2])
                       #print '   cross-section: ', xsec

                if 'nTT fraction' in line:
                   list_of_words = line.split("=",1)
                   frac_tt = float(list_of_words[1])

                if 'nTL fraction' in line:
                   list_of_words = line.split("=",1)
                   frac_tl = float(list_of_words[1])

                if 'nLL fraction' in line:
                   list_of_words = line.split("=",1)
                   frac_ll = float(list_of_words[1])

            if nev < int(nevents):
                bad_file = True
            if xsec < 0:
                bad_file = True
            if frac_tt < 0:
                bad_file = True
            if frac_tl < 0:
                bad_file = True
            if frac_ll < 0:
                bad_file = True

        if not bad_file:
            ngood_files += 1
            crosssection += xsec
            fll += frac_ll
            ftt += frac_tt
            ftl += frac_tl

    # print values of extracted parameters

    lep_xsec = float(crosssection)/ngood_files * br_ww_2l2v

    print 'number of good files:', ngood_files
    print 'total cross-section       : {:.3f} pb'.format(float(crosssection)/ngood_files)
    print 'branching ratio           : {:.3f}'.format(float(br_ww_2l2v))

    print 'cross-section into leps   : {:.3f} pb'.format(lep_xsec)
    print 'TT cross-section          : {:.3f} pb'.format(float(ftt)/ngood_files * lep_xsec)
    print 'TL cross-section          : {:.3f} pb'.format(float(ftl)/ngood_files * lep_xsec)
    print 'LL cross-section          : {:.3f} pb'.format(float(fll)/ngood_files * lep_xsec)

    print 'TT fraction               : {:.3f}'.format(float(ftt)/ngood_files)
    print 'TL fraction               : {:.3f}'.format(float(ftl)/ngood_files)
    print 'LL fraction               : {:.3f}'.format(float(fll)/ngood_files)


    with open(paramFile, 'a') as jf:
        jf.write("'{}_{}_TT':['','inclusive','','{:.3f}','1.0','1.0'],\n".format(process,k,float(ftt)/ngood_files * lep_xsec))
        jf.write("'{}_{}_TL':['','inclusive','','{:.3f}','1.0','1.0'],\n".format(process,k,float(ftl)/ngood_files * lep_xsec))
        jf.write("'{}_{}_LL':['','inclusive','','{:.3f}','1.0','1.0'],\n".format(process,k,float(fll)/ngood_files * lep_xsec))
'''
