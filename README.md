# k-means-image-compression from scratch

k-means algorithm for image compression

Generalized K-means algorithm that was used:
  Initialize k cluster centers, {<img src="https://latex.codecogs.com/gif.latex?c_1"/>, <img src="https://latex.codecogs.com/gif.latex?c_2"/>,..., <img src="https://latex.codecogs.com/gif.latex?c_k"/>}, randomly

  Do:
  
   1. Decide the cluster memberships of each data point, <img src="https://latex.codecogs.com/gif.latex?x_i"/> , by assigning it to the nearest cluster center
    
   2. Adjust the cluster centers
    
  While any cluster center has been changed.

Original image:

![alt text](https://github.com/natgolovach/k-means-image-compression/blob/main/_data/ng.jpg)

2 clusters,<\br> 0.12900209426879883 sec runtime<\br>Total iterations:  12

![alt text](https://github.com/natgolovach/k-means-image-compression/blob/main/ng.jpg_Compressed_2_clusters.png)

4 clusters, 

0.11100125312805176 sec runtime

Total iterations:  7

![alt text](https://github.com/natgolovach/k-means-image-compression/blob/main/ng.jpg_Compressed_4_clusters.png)

8 clusters, 

0.5759994983673096 sec runtime

Total iterations:  66

![alt text](https://github.com/natgolovach/k-means-image-compression/blob/main/ng.jpg_Compressed_8_clusters.png)

16 clusters, 

2.13899564743042 sec runtime

Total iterations:  168

![alt text](https://github.com/natgolovach/k-means-image-compression/blob/main/ng.jpg_Compressed_16_clusters.png)
