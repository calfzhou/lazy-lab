import sys
import rsa

YUECHE_PRIV_KEY = {'q': 3004727651L, 'p': 781435729, 'd': 620827009530618763L}
YUECHE_PUB_KEY = {'e': 15427, 'n': 2348001542405642579L}

def Main(uid):
  sid = rsa.sign(uid, YUECHE_PRIV_KEY).encode('base64')
  print rsa.verify(sid.decode('base64'), YUECHE_PUB_KEY)
  print sid

if __name__ == '__main__':
  if len(sys.argv) != 2:
    print 'Usage: python keygen.py <DFSS_UID>'
    sys.exit(0)
  uid = sys.argv[1]
  Main(uid)
