
import hashlib, binascii, os

def hash_password(password):
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    hashedPW = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), 
                                salt, 100000)
    hashedPW = binascii.hexlify(hashedPW)
    return (salt + hashedPW).decode('ascii')

def verify_password(stored, provided):
    salt = stored[:64]
    stored = stored[64:]
    hashedPW = hashlib.pbkdf2_hmac('sha512', 
                                  provided.encode('utf-8'), 
                                  salt.encode('ascii'), 
                                  100000)
    hashedPW = binascii.hexlify(hashedPW).decode('ascii')
    return hashedPW == stored