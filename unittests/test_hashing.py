""" UNITTESTS """
import unittest
from GenericFunctions.Hashing import Hashing


class Unittests(unittest.TestCase):
    """ Unittests """
    @staticmethod
    def test_make_md5_hash():
        """ Test create md5 hash """
        data = 'mock'
        hashing = Hashing()
        result = hashing.make_md5_hash(data)

        assert result == '17404a596cbd0d1e6c7d23fcd845ab82'

    @staticmethod
    def test_make_sha1_hash():
        """ Test create sha1 hash """
        data = 'mock'
        hashing = Hashing()
        result = hashing.make_sha1_hash(data)

        assert len(result) == 40
