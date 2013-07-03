#!/usr/bin/python

# Written by Sam Russell in July 2013

import unittest
import sys
import os.path
from copy import copy
sys.path.append(os.path.dirname(__file__) + "/../..")

from miniflow import *

class linkgraph_test(unittest.TestCase):
    def test_testone(self):
        sampleoutputs = {
            ('a', 'b'),
        }
        for one, two in sampleoutputs:
            expected = one
            actual = two # some function likely
            self.assertEquals(expected, actual, "Function(%(rrdfilename)s): expected %(expected)s (but is %(actual)s)" % locals())

