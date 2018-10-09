
# coding: utf-8

# # MD5 Hash

# In[13]:


from Crypto.Hash import MD5
message = input().encode('utf-8')
h = MD5.new()
h.update(message)
print(h.hexdigest())


# # SHA512

# In[16]:


from Crypto.Hash import SHA512
message=input().encode('utf-8')
h=SHA512.new()
h.update(message)
print(h.hexdigest())

