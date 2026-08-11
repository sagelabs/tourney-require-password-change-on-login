from Tourney.utils.crypto import hash_password as hp
from Tourney.utils.crypto import sha256 as sha
from Tourney.utils.crypto import verify_password as vp


def hash_password(p):
    print(
        "This function will be deprecated in a future release. Please update to Tourney.utils.crypto.hash_password"
    )
    return hp(p)


def check_password(p, hash):
    print(
        "This function will be deprecated in a future release. Please update to Tourney.utils.crypto.verify_password"
    )
    return vp(p, hash)


def sha256(p):
    print(
        "This function will be deprecated in a future release. Please update to Tourney.utils.crypto.sha256"
    )
    return sha(p)
