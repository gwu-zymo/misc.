# Define the start and end colors
start_color <- "red"
mid_color <- "green"
end_color <- "red"

# Generate a color gradient function
gradient_fun <- colorRampPalette(c(start_color, mid_color, end_color))

# Generate the color gradient
num_colors <- 100  # Number of colors in the gradient
colors <- gradient_fun(num_colors)

# Display the color gradient
image(1:num_colors, 1, as.matrix(1:num_colors), col = colors, xlab = "", ylab = "", xaxt = "n", yaxt = "n")

# Place a black dot
dot_position <- 10
points(dot_position, 1, pch = 19, col = "black")





###enterotype###
#Uncomment next two lines if R packages are already installed
#install.packages("cluster")
#install.packages("clusterSim")
library(cluster)
library(clusterSim)

#Download the example data and set the working directory
#setwd('<path_to_working_directory>')
data=read.table("sample_entero.data.txt", header=T, row.names=1, dec=".", sep="\t")
data=data[-1,]

dist.JSD <- function(inMatrix, pseudocount=0.000001, ...) {
  KLD <- function(x,y) sum(x *log(x/y))
  JSD<- function(x,y) sqrt(0.5 * KLD(x, (x+y)/2) + 0.5 * KLD(y, (x+y)/2))
  matrixColSize <- length(colnames(inMatrix))
  matrixRowSize <- length(rownames(inMatrix))
  colnames <- colnames(inMatrix)
  resultsMatrix <- matrix(0, matrixColSize, matrixColSize)
  
  inMatrix = apply(inMatrix,1:2,function(x) ifelse (x==0,pseudocount,x))
  
  for(i in 1:matrixColSize) {
    for(j in 1:matrixColSize) { 
      resultsMatrix[i,j]=JSD(as.vector(inMatrix[,i]),
                             as.vector(inMatrix[,j]))
    }
  }
  colnames -> colnames(resultsMatrix) -> rownames(resultsMatrix)
  as.dist(resultsMatrix)->resultsMatrix
  attr(resultsMatrix, "method") <- "dist"
  return(resultsMatrix) 
}

data.dist=dist.JSD(data)

pam.clustering=function(x,k) { # x is a distance matrix and k the number of clusters
  require(cluster)
  cluster = as.vector(pam(as.dist(x), k, diss=TRUE)$clustering)
  return(cluster)
}

data.cluster=pam.clustering(data.dist, k=3)

require(clusterSim)
nclusters = index.G1(t(data), data.cluster, d = data.dist, centrotypes = "medoids")

nclusters=NULL

for (k in 1:20) { 
  if (k==1) {
    nclusters[k]=NA 
  } else {
    data.cluster_temp=pam.clustering(data.dist, k)
    nclusters[k]=index.G1(t(data),data.cluster_temp,  d = data.dist,
                          centrotypes = "medoids")
  }
}

plot(nclusters, type="h", xlab="k clusters", ylab="CH index",main="Optimal number of clusters")

obs.silhouette=mean(silhouette(data.cluster, data.dist)[,3])
cat(obs.silhouette) #0.1899451

write.csv(data.cluster, 'r_output.txt')
                   
                   
#data=noise.removal(data, percent=0.01)

## plot 1
obs.pca=dudi.pca(data.frame(t(data)), scannf=F, nf=10)
obs.bet=bca(obs.pca, fac=as.factor(data.cluster), scannf=F, nf=k-1) 
dev.new()
s.class(obs.bet$ls, fac=as.factor(data.cluster), grid=F,sub="Between-class analysis")

#plot 2
obs.pcoa=dudi.pco(data.dist, scannf=F, nf=3)
dev.new()
s.class(obs.pcoa$li, fac=as.factor(data.cluster), grid=F,sub="Principal coordiante analysis")
                   
                   
