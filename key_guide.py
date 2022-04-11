# Create A Key For The Desired Password #

import hashlib

password = b'Redhatss@44'

hash1 = hashlib.md5()
hash1.update(password)
print(hash1.hexdigest())
