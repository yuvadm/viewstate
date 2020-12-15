from enum import Enum

class Encryption(Enum):
    DES = 'des'
    DES3 = '3des'
    AES = 'aes'

    def __str__(self):
        return self.value

class MAC(Enum): #https://referencesource.microsoft.com/#System.Web/Configuration/MachineKeyValidation.cs,a357c185ad2e9c71
    HMACMD5 = 'hmac_md5'
    HMACSHA1 = 'hmac_sha1'
    HMACSHA256 = 'hmac_sha256'
    HMACSHA384 = 'hmac_sha384'
    HMACSHA512 = 'hmac_sha512'

    def __str__(self):
        return self.value
