#!/usr/bin/env python
# https://github.com/neurolabusc/dcm_qa_ge/blob/master/slicetime.cpp
import itertools
import fire
import os
import numpy as np

def sliceTimeGE(mb=2,
                dim3=10,
                TR=1.0,
                isInterleaved=True,
                geMajorVersion=28.0,
                is27r3=True,
                groupDelaysec=0):
    sliceTiming = np.zeros(dim3)
    nExcitations = int(np.ceil(float(dim3)/float(mb)))
    if (mb > 1) and (not is27r3) and (nExcitations % 2 == 0):
        nExcitations += 1
    nDiscardedSlices = nExcitations * mb - dim3
    secPerSlice = (TR-groupDelaysec) / (nExcitations)
    if not isInterleaved:
        for i in range(0, nExcitations):
            sliceTiming[i] = i * secPerSlice
    else:
        nOdd = (nExcitations -1)/2
        for i in range(0, nExcitations):
            if i%2==0:
                sliceTiming[i] = (i/2)* secPerSlice
            else:
                sliceTiming[i] = (nOdd + ((i+1)/2)) * secPerSlice

        if (mb>1) and is27r3 and isInterleaved and (nExcitations >2) and (nExcitations%2==0):
            tmp = sliceTiming[nExcitations-1]
            sliceTiming[nExcitations-1] = sliceTiming[nExcitations-3]
            sliceTiming[nExcitations-1] = tmp
    for i in range(0, dim3):
        sliceTiming[i] = sliceTiming[i%nExcitations]

    return sliceTiming


def GE_slicetime(mb,
                 dim3,
                 TR,
                 isInterleaved=True,
                 isDescending=False,
                 geMajorVersion=28.0,
                 is27r3=False,
                 groupDelaysec=0):
    sliceTiming = sliceTimeGE(mb, dim3, TR, isInterleaved, geMajorVersion, is27r3, groupDelaysec)
    if isDescending:
        for i in range(i, dim3/2):
            sliceTiming[i], sliceTiming[dim3-1-i] = sliceTiming[dim3-1-i], sliceTiming[i]

    for t in sliceTiming:
        print(str(t) + ',')

    slice_groups = [ [ str(x[0]) for x in g ] for _, g in itertools.groupby(sorted(enumerate(sliceTiming), key=lambda x:x[1]), key=lambda x:x[1]) ]
    with open('slspec.txt', 'w') as f:
        for sg in slice_groups:
            f.write(' '.join(sg)+'\n')
    print('slspec is saved in ' + os.getcwd())


if __name__ == "__main__":
    fire.Fire(GE_slicetime)
    