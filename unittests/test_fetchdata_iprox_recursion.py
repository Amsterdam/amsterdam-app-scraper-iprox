""" UNITTESTS """
import unittest
from unittests.mock_data import TestData
from FetchData.IproxRecursion import IproxRecursion


class Unittests(unittest.TestCase):
    """ Unittests """
    @staticmethod
    def test_recursion():
        """ Test recursion """
        data = TestData()
        iprox_recursion = IproxRecursion()
        result = iprox_recursion.filter(data.iprox_recursion, [], targets=['Target'])
        expected_result = [{'Target': []}, {'Target': {'Nam': 'Target', 'veld': {}}}]

        assert result == expected_result
