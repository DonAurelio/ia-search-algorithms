# use masked arrays to plot a line with different colors by y-value
from __future__ import division, print_function
import sys
sys.path.append("../pylab_examples")
import matplotlib
matplotlib.use("agg")
from pylab import savefig
import numpy
numpy.seterr(invalid="ignore")
# use masked arrays to plot a line with different colors by y-value
from numpy import logical_or, arange, sin, pi
from numpy import ma
from matplotlib.pyplot import  plot, show

t = arange(0.0, 2.0, 0.01)
s = sin(2*pi*t)

upper = 0.77
lower = -0.77


supper = ma.masked_where(s < upper, s)
slower = ma.masked_where(s > lower, s)
smiddle = ma.masked_where(logical_or(s<lower, s>upper), s)

plot(t, slower, 'r', t, smiddle, 'b', t, supper, 'g')

savefig(r"agg/color_by_yvalue", dpi=150)