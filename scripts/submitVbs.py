import os, sys, subprocess,re 

#collect = True
collect = False

#kws = ['090', '095', '098', '100', '102', '105', '110']
#kws = ['050','070','080', '120', '130', '150']
#kws = ['050','070','080','090', '095', '098', '100', '102', '105', '110','120', '130', '150']
kws = ['050','070','080','090', '095']

#kws = ['110']

pols=['TT','LL','TL']

queue = '1nw'
njobs='20'
nevents='5000'

process='mg_pp_vbs_wwss_kw'
outdir='/eos/experiment/fcc/hh/generation/lhe/'

model='models/sm_kw.tar'


if not collect:
    for k in kws:
        cmd='python bin/submitMGjobs.py --mg5card examples/{}_{}.mg5  --model {} --outdir {} --procname {}_{} --njobs {} --nev {} --queue {} --pol'.format(process,k,model,outdir,process, k,njobs,nevents,queue)
        print cmd
        os.system(cmd)


else:

    paramFile = 'param.py'
    br_ww_2l2v = 0.0466

    # extract cross sections from lhe files and logs and write in param file form
    os.system('rm param.py')
    for k in kws:

        print ' '
        print '     {}_{}'.format(process,k)
        print ' '

        # pick up one stdout file that contains at least 5k events

        batchjobs_dir = 'BatchOutput/{}_{}/std/'.format(process,k)

        cmd = "find {} -type f -name '*.out'".format(batchjobs_dir)
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        lst = proc.communicate()[0]
        list_of_files = lst.splitlines()

        ngood_files = 0

        crosssection = 0.

        neventstot = 0

        ftt = 0.
        ftl = 0.
        fll = 0.

        i = 0
        for log in list_of_files:

            bad_file = False
            nev = -1
            xsec = -1.
            frac_tt = -1.
            frac_tl = -1.
            frac_ll = -1.

            '''
            if i > 1000:
                break
            '''
            i += 1

            #print '------ new log file ----'

            with open(log) as f:

                for line in f:
                    if 'Nb of events' in line:
                        #list_of_words = line.split(":",1)

                        digis = re.findall(r"[-+]?\d*\.\d+|\d+", line)  
                        if len(digis) > 0:
                            nev= int(digis[0])
                            #print 'nev', nev
                           
                    if 'Cross-section' in line:
                        digis = re.findall(r"[-+]?\d*\.\d+|\d+", line)  
                        #print digis
                        if len(digis) > 0:
                            xsec= float(digis[0])
                            #print '   cross-section: ', xsec

                    if 'nTT fraction' in line:
                        digis = re.findall(r"[-+]?\d*\.\d+|\d+", line)  
                        #print digis
                        if len(digis) > 0:
                           frac_tt= float(digis[0])
                           #print  'tt', frac_tt
                       
                    if 'nTL fraction' in line:
                        digis = re.findall(r"[-+]?\d*\.\d+|\d+", line)  
                        #print digis
                        if len(digis) > 0:
                          frac_tl= float(digis[0])
                          #print  'tl', frac_tl

                    if 'nLL fraction' in line:
                        digis = re.findall(r"[-+]?\d*\.\d+|\d+", line)  
                        #print digis
                        if len(digis) > 0:
                          frac_ll= float(digis[0])
                          #print  'll', frac_ll

                '''
                print log
                print nev, xsec, frac_tt, frac_tl, frac_ll
                print ngood_files
                '''
                #print nev, xsec, frac_tt, frac_tl, frac_ll
                
                if xsec < 0:
                    bad_file = True
                if frac_tt < 0:
                    bad_file = True
                if frac_tl < 0:
                    bad_file = True
                if frac_ll < 0:
                    bad_file = True


            #print nev, xsec, frac_tt, frac_tl, frac_ll, bad_file

            if not bad_file:
                
                neventstot += nev
                ngood_files += 1
                crosssection += nev*xsec
                fll += nev*frac_ll
                ftt += nev*frac_tt
                ftl += nev*frac_tl

            # print values of extracted parameters

            #
            #print 'print all extracted values'
            #print neventstot, ngood_files, crosssection, fll, ftt, ftl


        #print 'print all extracted values'
        #print neventstot, ngood_files, crosssection, fll, ftt, ftl

        
        crosssection = float(crosssection)/neventstot
        ftt = float(ftt)/neventstot
        ftl = float(ftl)/neventstot
        fll = float(fll)/neventstot
        
        lep_xsec = crosssection* br_ww_2l2v

        print 'number of successful jobs:'  , ngood_files
        print 'number of generated events: ', neventstot
        print 'generation efficiency: {:.4f}'.format(float(float(neventstot)/(int(len(list_of_files))*int(nevents))))
        
        print 'total cross-section       : {:.4f} pb'.format(float(crosssection))
        print 'branching ratio           : {:.4f}'.format(float(br_ww_2l2v))

        print 'cross-section into leps   : {:.4f} pb'.format(lep_xsec)
        print 'TT cross-section          : {:.4f} pb'.format(float(ftt) * lep_xsec)
        print 'TL cross-section          : {:.4f} pb'.format(float(ftl) * lep_xsec)
        print 'LL cross-section          : {:.4f} pb'.format(float(fll) * lep_xsec)

        print 'TT fraction               : {:.4f}'.format(float(ftt))
        print 'TL fraction               : {:.4f}'.format(float(ftl))
        print 'LL fraction               : {:.4f}'.format(float(fll))

        with open(paramFile, 'a') as jf:
            jf.write("'{}_{}_TT':['','inclusive','','{:.4f}','1.0','1.0'],\n".format(process,k,float(ftt) * lep_xsec))
            jf.write("'{}_{}_TL':['','inclusive','','{:.4f}','1.0','1.0'],\n".format(process,k,float(ftl) * lep_xsec))
            jf.write("'{}_{}_LL':['','inclusive','','{:.4f}','1.0','1.0'],\n".format(process,k,float(fll) * lep_xsec))



    # write check commands for LHE input
    with open(paramFile, 'a') as jf:
	jf.write("\n")
	jf.write("\n")
	jf.write("\n")

	for k in kws:

              jf.write("python bin/run.py --FCC --LHE --check --p {}_{}_TT --force --version fcc_v02\n".format(process,k))
              jf.write("python bin/run.py --FCC --LHE --check --p {}_{}_TL --force --version fcc_v02\n".format(process,k))
              jf.write("python bin/run.py --FCC --LHE --check --p {}_{}_LL --force --version fcc_v02\n".format(process,k))

	for k in kws:

              jf.write("python bin/run.py --FCC --reco --send --type lhep8 --lsf --p {}_{}_TT -N 1000 -q 8nh --version fcc_v02\n".format(process,k))
              jf.write("python bin/run.py --FCC --reco --send --type lhep8 --lsf --p {}_{}_TL -N 1000 -q 8nh --version fcc_v02\n".format(process,k))
              jf.write("python bin/run.py --FCC --reco --send --type lhep8 --lsf --p {}_{}_LL -N 1000 -q 8nh --version fcc_v02\n".format(process,k))

