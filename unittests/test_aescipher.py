from GenericFunctions.AESCipher import AESCipher


def test_encryption_ok():
    test_string = 'test string'
    aes = AESCipher(test_string, 'secret')
    encrypted = aes.encrypt()
    aes.data = encrypted
    cleartext = aes.decrypt()
    assert test_string == cleartext


def test_encrypt_fail():
    aes = AESCipher(b'', 'secret')
    result = aes.encrypt()
    assert result is None


def test_decrypt_fail():
    aes = AESCipher(b'', 'secret')
    result = aes.decrypt()
    assert result is None
