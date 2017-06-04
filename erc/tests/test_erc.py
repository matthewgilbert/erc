import unittest
from erc import erc
import numpy as np
from numpy.testing import assert_almost_equal


class TestERC(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_cov_2(self):
        cov = np.array([[2, 0], [0, 1]])
        res = erc.calc_weights(cov)
        pcr = res.dot(cov) * res / (res.dot(cov).dot(res))
        pcr_exp = np.ones(2) / 2
        assert_almost_equal(pcr, pcr_exp)

    def test_cov_10(self):
        np.random.seed(42)
        # this will be PSD in general, for this seed PD was checked manually
        A = np.random.randn(10, 10)
        cov = A.dot(A.transpose())
        res = erc.calc_weights(cov)
        pcr = res.dot(cov) * res / (res.dot(cov).dot(res))
        pcr_exp = np.ones(10) / 10
        assert_almost_equal(pcr, pcr_exp, decimal=6)

    def test_cov_100(self):
        np.random.seed(42)
        # this will be PSD in general, for this seed PD was checked manually
        A = np.random.randn(100, 100)
        cov = A.dot(A.transpose())
        res = erc.calc_weights(cov)
        pcr = res.dot(cov) * res / (res.dot(cov).dot(res))
        pcr_exp = np.ones(100) / 100
        assert_almost_equal(pcr, pcr_exp, decimal=6)

    def test_non_psd(self):
        cov = np.array([[-2, 0], [0, 1]])

        def solve_erc():
            erc.calc_weights(cov)

        self.assertRaises(np.linalg.LinAlgError, solve_erc)
