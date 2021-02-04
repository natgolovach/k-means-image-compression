import numpy as np
import random
import time
from scipy.spatial import distance
import matplotlib.pyplot as plt
from matplotlib import image
import os

def load_image(path):
#loading image from file to list of arrays
#####input:
# path - path to the file, string
#####output:
# image_1 - array of arrays
#reference: https://www.pluralsight.com/guides/importing-image-data-into-numpy-arrays, Method 2 Matplotlib library

    image_1 = image.imread(path)

    #print(image_1.shape)

    return image_1

def initialize_centers(image_reshaped,k=4):
#first initialization of centroids, randomly choosing k points from the pixels
####input:
#1) image_reshaped - np array with image data pixels,
#2) k - clusters qty
####output:
#1) centroid - initial cluster centroids

    n, m = image_reshaped.shape
    idx = np.random.randint(n, size=k)
    #print (idx)
    centroid=image_reshaped[idx,:]
    #print("initial centroid", centroid)

    return centroid

def poor_initialize_centers(image_reshaped,k=4):
#using for checking how poor initialized centroids affect the result
####input:
#1) image_reshaped - np array with image data pixels,
#2) k - clusters qty
####output:
#1) centroid - initial cluster centroids

    n, m = image_reshaped.shape
    idx = np.random.randint(n, size=k)
    #print (idx)

    #experiment 1
    centroid=y=np.array([[0, 0,  1], [0, 0,  2],[0, 0,  3],[0, 0,  4]])
    #experiment 2
    #centroid=y=np.array([[1, 1,  1], [1, 1,  1],[0, 0,  1], [0, 0,  2]])
    #experiment 3
    #centroid=y=np.array([[1, 1,  1], [1, 1,  1],[1, 1,  1],[1, 1,  1]])
    #print("initial centroid", centroid)

    return centroid


def calculate_distance(point, centr):
#retired
#calculating distance between centroids and each point in array
####input:
# 1) point 2) centroid
####output:
#distance_point_centr - euclidean distance
    point=point.reshape(1, point.shape[0])
    centr = centr.reshape(1,centr.shape[0])
    #print ("point", point, point.shape)
    #print ("centr", centr, centr.shape)
    distance_point_centr=distance.cdist(point, centr, metric='euclidean')
    return distance_point_centr

def assign_cluster(image_reshaped, centroid, k):
#retired - unefficient and VERY long, switched to np arrays for better results, see assign_cluster2
    class_=np.zeros((image_reshaped.shape[0],1),dtype=int)
    for i, each_point in enumerate(image_reshaped):
        distances = [None] * k
        for j, each_centroid in enumerate(centroid):
            #print ("each_point",each_point)
            #print ("each_centroid",each_centroid, i)
            distances[j]=calculate_distance(each_point,each_centroid)
        #print ("distances",distances)
        #print ("min(distances)",min(distances))
        cluster_no = distances.index(min(distances))
        #print ("cluster_no",cluster_no )
        class_[i]=cluster_no+1
        #print ("class_[i]",class_[i])
    #print (class_)
    return class_

def assign_cluster2(image_reshaped, centroid, k):
#assigning points to the closest centroid
####input:
# 1) image_reshaped - array with pixels
# 2) centroid - array with centroids
# 3) k - cluster qty
####output:
# 1) class_ - array with the assigned number of the cluster from 1 to... (not from 0) for each point

    class_=np.zeros((image_reshaped.shape[0],1),dtype=int)
    distances = distance.cdist(image_reshaped, centroid, metric='euclidean')
    class_ = np.argmin(distances, axis=1)+1
    return class_

def new_centroid(image_reshaped,class_,k):
#calculating new centroid of the cluster
####input:
# 1) image_reshaped - array with pixels
# 2) class_ - array with the assigned number of the cluster from 1 to... (not from 0) for each point
# 3) k - cluster qty
####output: array with new centroids
    new_centr = np.zeros((k, 3), dtype=int)
    for j in range (k):
        indexes = np.argwhere(class_ == j+1)
        cluster_points=image_reshaped[indexes]
        new_centr[j]=cluster_points.mean(axis=0)[0]

    #print("new_centr",new_centr)
    return new_centr

def kmeans_from_scratch(image, k=4):
#k-means algorithm, main function
####input:
# 1) pixels (pixels: the input image representation. Each row contains one data point (pixel). For image dataset, it
#contains 3 columns, each column corresponding to Red, Green, and Blue component. Each component
#has an integer value between 0 and 255.)
#2) k: the number of desired clusters. Too high value of K may result in empty cluster error. Then, you need to reduce it.
####output:
#1) class: cluster assignment of each data point in pixels. The assignment should be 1, 2, 3, etc. For
#k = 5, for example, each cell of class should be either 1, 2, 3, 4, or 5. The output should be a column
#vector with size(pixels, 1) elements.
#2) centroid: location of k centroids (or representatives) in your result. With images, each centroid
#corresponds to the representative color of each cluster. The output should be a matrix with K rows
#and 3 columns. The range of values should be [0, 255], possibly
#oating point numbers.

    #reshaping image: (number of pixels, number of channels)
    #image_reshaped = image_1.reshape(image_1.shape[0]*image_1.shape[1],image_1.shape[2])
    image_reshaped = image.reshape(image.shape[0] * image.shape[1], image.shape[2])
    #print ("image_reshaped.shape", image_reshaped.shape)
    ##initial step: randomly choose first cluster centers
    #centroid=initialize_centers(image_reshaped,k=k)
    #use second option for experiments with poor centroids assigments
    centroid=initialize_centers(image_reshaped,k=k)

    #then iterate until no changes:
    iter=0
    while True:
        ##first step: assign points to the closest cluster centers
        class_=assign_cluster2 (image_reshaped,centroid, k=k)

        ##second step: move cluster centers into center of the cluster
        new_centroid_=new_centroid(image_reshaped,class_,k=k)
        if np.array_equal(centroid,new_centroid_):
            break
        else:
            centroid = new_centroid_
            iter=iter+1
    #print ("final centroid", centroid)
    print ("Total iterations: ", iter)
    return class_, centroid

def compress_image(filename, path,k=4):
#compressing image by replacing it with the cluster center
####input:
# 1) path - path to the file
# 2) k - qty of clusters
####output:
##
    image = load_image(path)
    class_, centroid=kmeans_from_scratch(image, k)
    #print ("final centroid 2", centroid)
    compressed_image=np.zeros((len(class_), 3), dtype=np.uint8)
    for i, each_point in enumerate(class_):
        compressed_image[i]=centroid[each_point-1]
    #print (compressed_image)
    #reshaping it back
    compressed_image_reshaped = compressed_image.reshape(image.shape[0] , image.shape[1], image.shape[2])
    #print ("compressed_image_reshaped.shape", compressed_image_reshaped.shape)
    plt.imsave("{}_Compressed_{}_clusters.png".format(filename,k), compressed_image_reshaped)
    return


#start = time.time()
##assign path to the image and qty of clusters (k):
#path='C:/Users/golovach/Desktop/ISYE-6740-OAN - Homework/HW1/data/up.jpg'
#compress_image(path, k=4)

#end = time.time()
#print(f"Runtime of the program is {end - start}")



directory = 'data\\'
i = 1
for filename in os.listdir(directory):

    if filename.endswith(".jpg") or filename.endswith(".bmp"):
        path=os.path.join(directory, filename)
        for k in [2,4,8,16]:
            start = time.time()
            print(f"{i} Starting compressing the file {filename} with {k} clusters")
            compress_image(filename,path, k)
            end = time.time()
            print(f"Runtime of the program for {filename}, {k} clusters is {end - start}")
            i=i+1
    else:
        continue



