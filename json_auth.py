
import json

from tornado import gen
from jupyterhub.auth import Unicode
from jupyterhub.auth import Authenticator

class JsonAuthenticator(Authenticator):

    passwords_file = Unicode(config=True,
        help="""json encoded file of username:password for authentication"""
    )
    
    @gen.coroutine
    def authenticate(self, handler, data):
        print('JsonAuthenticator.authenticate 0')
        with open(self.passwords_file, 'r') as f:
            print('JsonAuthenticator.authenticate 1')
            d = json.load(f)
            print('JsonAuthenticator.authenticate 2')
            if d.get(data['username']) == data['password']:
                print('JsonAuthenticator.authenticate 3')
                return data['username']
