
# coding: utf-8

# In[58]:


import numpy as np
import string
from itertools import chain
import re
alphabets = (list((string.ascii_lowercase).replace("j","i")))
#alphabets
input_key = (raw_input('please enter key:').lower().replace("j", "i"))
key = np.array(list(input_key.replace(" ",""))) 
key

#Build a play fair matrix with Key and alphabets
matrix = []
for x in chain(key, alphabets):
  if not x in matrix: matrix.append(x)

#Get matrix as play cipher key matrix
shape = (5,5)
play_matrix = np.matrix(matrix).reshape(shape)
#play_matrix = np.matrix(play_matrix1)
#lst = matrix
#play_matrix= np.array_split(lst,5)

print "Play Matrix:"
print play_matrix


#Take input as text 
sentence = raw_input('Please enter text to Encrypt:').lower()

input_text = sentence = sentence.replace(' ', '')
    #Check if even or odd
length_text = len(input_text)
if length_text % 2 != 0:
     input_text +='x'
text = input_text.replace("j", "i")

#Split text into 2 for Encryption
text_split = []
while text:
    text_split.append(text[:2])
    text = text[2:]
print text_split

select_char = []
for i in text_split:
       select_char.append(np.array(list(i)))
select_char = np.array(select_char)
print "Divide in to sets for Encryption:"
print select_char

#Encryption of the string
encrypt= []
g =[]
for i in select_char:
    a = np.where(play_matrix == i[0])
    b = np.where(play_matrix == i[1])
    
    #print a,b

    if a[0] == b[0]:
        #If they are in both in same rows
        encrypt.append(play_matrix[a[0],(a[1]+1) % 5])
        encrypt.append(play_matrix[b[0],(b[1]+1) % 5])
         
    elif a[1] == b[1]:
        #If they are in both columns
        encrypt.append(play_matrix[(a[0]+1) % 5, a[1]])
        encrypt.append(play_matrix[(b[0]+1) % 5, b[1]])
        
    else:
        k = np.matrix(a)
        l = np.matrix(b)
        z = (k[0], l[1])
        x = (l[0], k[1])
        encrypt.append(play_matrix[z])
        encrypt.append(play_matrix[x])
        

encryted = ''.join(map(str, encrypt))
result1 = re.findall(r"(?i)\b[a-z]+\b", encryted)
result = ''.join(result1)
#print play_matrix      
#print select_char
print "Encryption string into sets",result1
print result

#Take input as text 
dec_sentence = raw_input('Please enter text to Decrypt:').lower()
print dec_sentence
decInput_text = dec_sentence = dec_sentence.replace(' ', '')
    #Check if even or odd
decLength_text = len(decInput_text)
if decLength_text % 2 != 0:
     decInput_text +='x'
dec_text = decInput_text.replace("j", "i")


#Split text into 2 for Decryption
decText_split = []
while dec_text:
    decText_split.append(dec_text[:2])
    dec_text = dec_text[2:]
print decText_split

decSelect_char = []
for i in decText_split:
       decSelect_char.append(np.array(list(i)))
decSelect_char = np.array(decSelect_char)
print "Divide in to sets for Decryption:"
print decSelect_char


#Decryption of the message
decrypt= []

for i in decSelect_char:
    x = np.where(play_matrix == i[0])
    y = np.where(play_matrix == i[1])
    
    #print a,b

    if x[0] == y[0]:
        #If they are in both in same rows
        decrypt.append(play_matrix[x[0],(x[1]-1) % 5])
        decrypt.append(play_matrix[y[0],(y[1]-1) % 5])
        
    elif x[1] == y[1]:
        decrypt.append(play_matrix[(x[0]-1) % 5, x[1]])
        decrypt.append(play_matrix[(y[0]-1) % 5, y[1]])
        
    else:
        m = np.matrix(x)
        n = np.matrix(y)
        g = (m[0], n[1])
        h = (n[0], m[1])
        decrypt.append(play_matrix[g])
        decrypt.append(play_matrix[h])
        

decrypted = ''.join(map(str, decrypt))
decResult1 = re.findall(r"(?i)\b[a-z]+\b", decrypted)
decResult = ''.join(decResult1)
#print play_matrix      
#print decSelect_char
print decResult1
print decResult     
                  



                  

