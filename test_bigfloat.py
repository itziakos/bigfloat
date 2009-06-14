import unittest
import operator
from bigfloat import *

class BigFloatTests(unittest.TestCase):
    def test_creation_from_integer(self):
        test_values = [-23, 0, 100, 7**100, -23L, 0L, 100L]
        test_precisions = [2, 20, 53, 2000]
        for value in test_values:
            for p in test_precisions:
                with precision(p):
                    bf = BigFloat(value)
                    self.assertEqual(type(bf), BigFloat)
                    self.assertEqual(bf.precision, p)

    def test_creation_from_float(self):
        test_values = [-12.3456, -0.0, 0.0, 5e-310, -1e308,
                        float('nan'), float('inf'), float('-inf')]
        test_precisions = [2, 20, 53, 2000]
        for value in test_values:
            for p in test_precisions:
                with precision(p):
                    bf = BigFloat(value)
                    self.assertEqual(type(bf), BigFloat)
                    self.assertEqual(bf.precision, p)

    def test_creation_from_string(self):
        test_values = ['123.456',
                       '-1.23',
                       '1e456',
                       '+nan',
                       'inf',
                       '-inf',
                       u'-451.001']
        test_precisions = [2, 20, 53, 2000]
        for value in test_values:
            for p in test_precisions:
                with precision(p):
                    bf = BigFloat(value)
                    self.assertEqual(type(bf), BigFloat)
                    self.assertEqual(bf.precision, p)

    def test_creation_from_BigFloat(self):
        test_values = [BigFloat(1.0),
                       BigFloat('nan'),
                       BigFloat('inf'),
                       const_pi()]
        # add a few extra values at other precisions
        with precision(200):
            test_values.append(const_catalan())
        with precision(15):
            test_values.append(sqrt(3))
        test_precisions = [2, 20, 53, 2000]
        for value in test_values:
            for p in test_precisions:
                with precision(p):
                    bf = BigFloat(value)
                    self.assertEqual(type(bf), BigFloat)
                    self.assertEqual(bf.precision, p)

    def test_binary_operations(self):
        # check that BigFloats can be combined with themselves,
        # and with integers and floats, using the 6 standard
        # arithmetic operators:  +, -, *, /, **, %

        x = BigFloat('17.29')
        other_values = [2, 3L, 1.234, BigFloat('0.678')]
        test_precisions = [2, 20, 53, 2000]
        # note that division using '/' should work (giving true division)
        # whether or not 'from __future__ import division' is enabled.
        # So we test both operator.div and operator.truediv.
        operations = [operator.add, operator.mul, operator.div,
                      operator.sub, operator.pow, operator.truediv,
                      operator.mod]
        for value in other_values:
            for p in test_precisions:
                with precision(p):
                    for op in operations:
                        bf = op(x, value)
                        self.assertEqual(type(bf), BigFloat)
                        self.assertEqual(bf.precision, p)
                        bf = op(value, x)
                        self.assertEqual(type(bf), BigFloat)
                        self.assertEqual(bf.precision, p)


    def test_subnormalization(self):
        # check that subnormalization doesn't result in
        # double rounding
        with double_precision:
            self.assertEqual(div(2**53+1, 2**1128), pow(2, -1074))

        # check that results are integer multiples of
        # 2**-1074
        with double_precision:
            self.assertEqual(BigFloat('3e-324'), pow(2, -1074))
            self.assertEqual(BigFloat('7.4e-324'), pow(2, -1074))
            self.assertEqual(BigFloat('7.5e-324'), pow(2, -1073))

def test_main():
    unittest.main()

if __name__ == '__main__':
    test_main()
