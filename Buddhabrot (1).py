#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#Author:Shyaam Prasadh
import png
import numpy as np
from random import random
 
def c_set(num_samples, iterations):
    
    non_msets = np.zeros(num_samples, dtype=np.complex128)
    non_msets_found = 0
    c = (np.random.random(num_samples)*4-2 +         (np.random.random(num_samples)*4-2)*1j)
 
    print "%d random c points chosen" % len(c)
    p = (((c.real-0.25)**2) + (c.imag**2))**.5
    c = c[c.real > p- (2*p**2) + 0.25]
    print "%d left after filtering the cardioid" % len(c)
    c = c[((c.real+1)**2) + (c.imag**2) > 0.0625]
    print "%d left after filtering the period-2 bulb" % len(c)
    z = np.copy(c)
 
    for i in range(iterations):
        z = z ** 2 + c
        mask = abs(z) < 2
        new_non_msets = c[mask == False]
        non_msets[non_msets_found:non_msets_found+len(new_non_msets)]                  = new_non_msets
        non_msets_found += len(new_non_msets
        c = c[mask]
        z = z[mask]
 
        print "iteration %d: %d points have escaped!"\
        % (i + 1, len(new_non_msets))
    return non_msets[:non_msets_found]
 
def buddhabrot(c, size):
    img_array = np.zeros([size, size], int)
    z = np.copy(c)
 
    while(len(z)):
 
        print "%d orbits in play" % len(z)
        x = np.array((z.real + 2.) / 4 * size, int)
        y = np.array((z.imag + 2.) / 4 * size, int)
        img_array[x, y] += 1
        z = z ** 2 + c
        mask = abs(z) < 2
        c = c[mask]
        z = z[mask]
 
    return img_array
 
if __name__ == "__main__":
 
    size = 400 
    iterations = 200 
    samples = 10000000 
 
    img_array = np.zeros([size, size], int)
 
    i = 0
 
    while True:
 
        print "get c set..."
        c = c_set(samples, iterations)
        print "%d non-mset c points found." % len(c)
 
        print "render buddha..."
        img_array += buddhabrot(c, size)
 
        print "adjust levels..."
        e_img_array = np.array(img_array/float(img_array.max())*((2**16)-1), int)
 
        print "saving buddhabrot_n_%di_%03d.png" % (iterations,i)
        imgWriter = png.Writer(size, size, greyscale=True, alpha=False, bitdepth=16)
        f = open("buddhabrot_n_%di_%03d.png" % (iterations,i), "wb")
        imgWriter.write(f, e_img_array)
        f.close()
 
        print "Done."
        i += 1

