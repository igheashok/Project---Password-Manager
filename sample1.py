import hashlib

ash = b'Redhatss@44'

hash1 = hashlib.md5()
hash1.update(ash)
print(hash1.hexdigest())
