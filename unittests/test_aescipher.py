""" UNITTESTS """
import unittest
from GenericFunctions.AESCipher import AESCipher


class Unittests(unittest.TestCase):
    """ Unittests """

    @staticmethod
    def test_encryption_ok():
        """ Test encrypt ok """
        test_string = 'test string'
        aes = AESCipher(test_string, 'secret')
        encrypted = aes.encrypt()
        aes.data = encrypted
        cleartext = aes.decrypt()
        assert test_string == cleartext

    @staticmethod
    def test_encrypt_fail():
        """ Test encrypt fails """
        aes = AESCipher(b'', 'secret')
        result = aes.encrypt()
        assert result is None

    @staticmethod
    def test_decrypt_fail():
        """ Test decrypt fails """
        aes = AESCipher(b'', 'secret')
        result = aes.decrypt()
        assert result is None
