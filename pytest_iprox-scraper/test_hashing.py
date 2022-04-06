from GenericFunctions.Hashing import Hashing


def test_make_md5_hash():
    data = 'mock'
    hashing = Hashing()
    result = hashing.make_md5_hash(data)

    assert result == '17404a596cbd0d1e6c7d23fcd845ab82'


def test_make_sha1_hash():
    data = 'mock'
    hashing = Hashing()
    result = hashing.make_sha1_hash(data)

    assert len(result) == 40
