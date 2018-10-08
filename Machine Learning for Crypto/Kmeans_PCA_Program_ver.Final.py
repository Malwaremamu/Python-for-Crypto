import string
from copy import deepcopy
from random import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.utils import shuffle
from Crypto.Cipher import ARC4, AES
from sklearn.metrics.pairwise import euclidean_distances
import scipy.spatial.distance as metric

#Creating Random String
min_char =256
max_char =256
n=201
random_list = []
for i in range(1,n):
    allchar =string.ascii_letters + string.punctuation + string.digits +""
    randomString = "".join(choice(allchar) for x in range(randint(min_char, max_char)))
    random_list.append(randomString)
#print random_list

arc4key = '0123456789123456'
aeskey = '0123456789123456'

#Encryption of ARC4 List
arc4_cipher_list=[]
for i in range(100):
    arc4_cipher = ARC4.new(arc4key).encrypt(random_list[i])
    arc4_cipher_list.append(arc4_cipher)
label_arc4 = pd.DataFrame(arc4_cipher_list)

#Decryption of ARC4 List
arc4_decrypt_list=[]
for i in range(len(arc4_cipher_list)):
    arc4_decrypt = ARC4.new(arc4key).decrypt(arc4_cipher_list[i])
    arc4_decrypt_list.append(arc4_decrypt)

label_arc4_list = label_arc4.assign(Encryption ='ARC4') #Adding a Label column of ARC4

#Encryption of AES list
aes_cipher_list=[]
for i in range(100, len(random_list)):
    aes_cipher = AES.new(aeskey).encrypt(random_list[i])
    aes_cipher_list.append(aes_cipher)
label_aes = pd.DataFrame(aes_cipher_list)

#Decryption of AES List
aes_decrypt_list=[]
for i in range(len(aes_cipher_list)):
    aes_decrypt = AES.new(aeskey).decrypt(aes_cipher_list[i])
    aes_decrypt_list.append(aes_decrypt)

label_aes_list = label_aes.assign(Encryption = 'AES')  #Adding a Label column of AES

combine_aes_arc4 = label_arc4_list.append(label_aes_list, ignore_index=True) #Combining the AES and ARC4 Cipher Text into one Variable name
combine_nolabel = combine_aes_arc4.drop(['Encryption'], axis=1)

#Coverting the encrypted string to Integers without shuffling the data
mix_int=[]
for i in range(len(combine_nolabel)):
    f = [ord(x) for x in combine_nolabel[0][i]]
    mix_int.append(f)
combine_int_list = pd.DataFrame(mix_int)

#Adding the Label Column to the integer variable
addLabel_aes = combine_int_list[:100].assign(Encryption = 'AES')
addLabel_arc4 = combine_int_list[100:].assign(Encryption = 'ARC4')
addLabel_aes_arc4 = label_arc4_list.append(label_aes_list, ignore_index=True)
combine_int = addLabel_aes.append(addLabel_arc4, ignore_index=True)
#print addLabel_aes
#print combine_int


#PCA Using label (AES and ARC4) Data
pca = np.array(combine_int_list) #Extracting only integer data
cov = np.dot(pca.T, pca) #Calculating the Covariance
eigen_values, eigen_vectors = np.linalg.eig(cov) #Calculating the Eigen vector and value using the linalg library
eigen_2 = eigen_vectors[:,:2] #Selecting 2 coloumns in eigen vector
plotter = np.dot(pca, eigen_2)  #X'W
plotter1 = pd.DataFrame(plotter)
x = plotter1[100:] #First 100 as AES
y = plotter1[:100] #Remaining 100 as ARC4
plt.title('PCA Visulisation with label data of AES and ARC4')
plt.xlabel('PC1')
plt.ylabel('PC2')
plt.scatter(x[0],x[1], color = 'red')
plt.scatter(y[0],y[1], color = 'blue')
plt.show()


combine_forShuffle = pd.DataFrame(combine_int)  #Intialize variable
shuffled_combine = pd.DataFrame(combine_forShuffle).sample(frac=1).reset_index(drop=True) #Shuffling the integer row data with label
shuffle_nolabel = shuffled_combine.drop(['Encryption'], axis=1) #Removing label column

#Kmeans Library
#kmeans = KMeans(n_clusters = 2, random_state=1).fit(shuffle_nolabel)

#Kmeans Clustering without Library
X = np.array(shuffle_nolabel)
#print len(X[0])


#Compute the distance between centroids and data
def compute_Distances(centroid, data):
    #return euclidean_distances(centroid, [data])
    return metric.euclidean(centroid, data)


#Initialize the random centeroids
centeroid_random = np.random.randint(1, np.max(X), size = (2, len(X[0])))
print centeroid_random
#print centeroid_random[0] - centeroid_random[1]
error1 = all(centeroid_random[0])
error2 = all(centeroid_random[1])
error = error1 | error2
print error


first_centeroid = centeroid_random[0]
second_centeroid = centeroid_random[1]

while error != 0:

    clusters = np.zeros(len(X))

    #print 1
    index = 0
    for sample in X:
        c0_distance = compute_Distances(first_centeroid, sample)
        c1_distance = compute_Distances(second_centeroid, sample)

        #print c0_distance
        #print c1_distance

        #Compare the distance & Instance Clusters
        if c0_distance > c1_distance:
            #print index
            clusters[index] = 1
            #index += 1

        index += 1

    cluster_label = np.array([clusters], dtype=np.int)
    print cluster_label
    #print cluster_label.T
    #Concatenate shuffle data & cluster_label
    cluster_dataSet = np.concatenate((X, cluster_label.T), axis=1)
    #print cluster_dataSet

    #Rearrange data for each cluster
    data_c0 = []
    data_c1 = []
    for cluster in cluster_dataSet:
        if cluster[-1] == 0:
            data_c0.append(cluster[:-1])
        else:
            data_c1.append(cluster[:-1])

    c0 = np.array(data_c0)
    c1 = np.array(data_c1)


    #Recompute Centeroids
    next_firstCenteroid = []
    next_secondCenteroid = []
    for i in range(len(c0[0])):
        next_firstCenteroid.append(np.mean(c0[:,i], dtype=np.int))
        next_secondCenteroid.append(np.mean(c1[:,i], dtype=np.int))

    next_firstCenteroid = np.array(next_firstCenteroid)
    next_secondCenteroid = np.array(next_secondCenteroid)
    print first_centeroid
    print next_firstCenteroid


    change1 = first_centeroid - next_firstCenteroid
    change2 = second_centeroid - next_secondCenteroid
    

    first_centeroid = next_firstCenteroid
    second_centeroid = next_secondCenteroid
    #print next_firstCenteroid

    error = np.sum(change1) + np.sum(change2)
    

clusterData = np.concatenate((c0, c1), axis=0)
print clusterData
print len(clusterData)
print len(clusterData[0])
            

#PCA Using shuffle with cluster label
kmean_pca = clusterData #Extracting only integer data
kmeans_cov = np.dot(kmean_pca.T, kmean_pca) #Calculating the Covariance
kmeans_cov
kmeans_eigen_values, kmeans_eigen_vectors = np.linalg.eig(kmeans_cov) #Calculating the Eigen vector and value using the linalg library
kmeans_eigen_2 = kmeans_eigen_vectors[:,:2]  #Selecting 2 coloumns in eigen vector
kmeans_plotter = np.dot(kmean_pca, kmeans_eigen_2)  #X'W
kmeans_plotter1 = pd.DataFrame(kmeans_plotter)
kmeans_x = kmeans_plotter1[:100] #First 100 as cluser0
kmeans_y = kmeans_plotter1[100:] #Remaining 100 as clulster1
plt.title('PCA Visulisation with Kmeans labels of 0 and 1') #Plotting the data for PCA Visulisation
plt.xlabel('PC1')
plt.ylabel('PC2')
plt.scatter(kmeans_x[0], kmeans_x[1], color = 'red')
plt.scatter(kmeans_y[0], kmeans_y[1], color = 'blue')
plt.show()

