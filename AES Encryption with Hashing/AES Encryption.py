#!/usr/bin/env python
# coding: utf-8

# In[35]:


from Crypto.Cipher import AES
from Crypto.Hash import MD5
from Crypto import Random
import base64

class AESCrypto:
    
    def md5_hash(self, text):
        h = MD5.new()
        h.update(text.encode('utf-8'))
        return h.hexdigest()
    
    def __init__(self,key):#Constructer
        self.key = self.md5_hash(key) #Intitalize Key and Size as 128 bits
         
    def encrypt(self, cleartext):
        Block_size = AES.block_size #Block size should be equal to 128 bits
        pad = lambda s: s + (Block_size - len(s) % Block_size) * chr (Block_size - len(s) % Block_size)
        cleartext_blocks = pad(cleartext)
        
        iv = Random.new().read(Block_size)# Creating a Random IV value
        crypto = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + crypto.encrypt(cleartext_blocks))
    
    def decrypt(self, enctext):
        enctext = base64.b64decode(enctext)
        iv = enctext[:16]
        crypto = AES.new(self.key, AES.MODE_CBC, iv)
        unpad = lambda s : s[0:-ord(s[-1:])] #Unpading the blocks before decrypting
        return unpad(crypto.decrypt(enctext[16:]))
    
aes = AESCrypto(input("Password: "))
encrypted = aes.encrypt(input("Encrypt Text: "))
print('Encrypted Text: ',encrypted)
decrypted = aes.decrypt(encrypted)
print('Decrypted Text: ',decrypted)
    
        

