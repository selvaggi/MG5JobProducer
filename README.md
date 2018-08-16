[]() MG5JobProducer
====================

Wraps MG5 and sends jobs on the LSF cluster. Examples:

```
python bin/submitMGjobs.py --mg5card examples/pp_ee.mg5 --outdir ./testLSF --procname pp_ee --njobs 10 --nev 100 --queue 8nh
```

Or with an external model:

```
python bin/submitMGjobs.py --mg5card examples/pp_hh.mg5 --model models/loop_sm_hh.tar --outdir ./test_hh --procname pp_hh --njobs 10 --nev 100 --queue 8nh
```


To generate Vector boson scattering with modified HWW coupling and splitting the final state into LL, TL, and TT polarisations, need to add the ```--pol``` flag:

```
python bin/submitMGjobs.py --mg5card examples/pp_vbs_wwss_kw_090.mg5  --model models/sm_kw.tar --outdir /eos/experiment/fcc/hh/generation/lhe/ --procname mg_pp_vbs_wwss_kw_090 --njobs 200 --nev 5000 --queue 2nw --pol
```
