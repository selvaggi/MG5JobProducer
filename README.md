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
