
# coding: utf-8

# In[61]:


from Crypto.Hash import SHA256


# In[62]:


def calculate_hash(password):
    h = SHA256.new()
    h.update((password).encode('utf-8'))
    return h.hexdigest()


# In[63]:


def subscribe(user_name, password):
    account = user_name + ':' + calculate_hash(password)
    f = open('Accounts.txt', 'w')
    f.write(account)
    f.close()
    print('[!] You are Registered')


# In[64]:


def login(user_name, password):
    f = open('Accounts.txt', 'r')
    account_file = f.read()
    s = account_file.split(':')
    user_name_file = s[0]
    password_file = s[1]
    hashed_password = calculate_hash(password)
    
    if user_name == user_name_file and hashed_password == password_file:
        print("You are Authenticated!")
    else:
        print('[!Invalid Username or Password]')


# In[65]:


def main():
    Text = input("Enter:\n 1] to subscribe\n 2] to login\n Choice: ")
    
    if Text =='1':
        user_name = input("Enter User name: ")
        password = input("Enter Password: ")
        subscribe(user_name, password)
    elif Text =='2':
        user_name = input("Enter User name: ")
        password = input("Enter Password: ")
        login(user_name, password)
    else:
        print('[!]Invalid Choice')
main()

