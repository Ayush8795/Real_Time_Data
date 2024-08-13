import pyotp
from dotenv import load_dotenv
import os
load_dotenv()

totpkey= os.getenv('TOTP_KEY')

def get_tfa():
    totp= pyotp.TOTP(totpkey).now()
    return totp

