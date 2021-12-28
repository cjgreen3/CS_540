from scipy.linalg import eigh
import scipy
import numpy as np
import matplotlib.pyplot as plt


def load_and_center_dataset(filename):
    # TODO: add your code here
    x = np.load(filename)  
    return x - np.mean(x, axis=0)


def get_covariance(dataset):
    # TODO: add your code here
    return np.dot(np.transpose(dataset), dataset)/ (len(dataset)-1)

def get_eig(S, m):
    # TODO: add your code here
    
    Lamda, U = scipy.linalg.eigh(S,eigvals=(len(S)-m,len(S)-1))

    idx = Lamda.argsort()[::-1]
    Lamda = Lamda[idx]
    U = U[:,idx]
    U = U[::-1]
    U = np.flip(U,0)
  
    Lamda = np.diag(Lamda)

    return Lamda, U

def get_eig_perc(S, perc):
    # TODO: add your code here
    Lamda, U = scipy.linalg.eigh(S)
    sums = np.sum(Lamda)
    m = 0
    for i in Lamda:
        if(i/sums)>perc:
            m +=1
    Lamda, U = get_eig(S,m)        


    return Lamda, U


def project_image(img, U):
    # TODO: add your code here
    alpha = np.dot(img,U) 
    return np.dot(U,alpha)
   


def display_image(orig, proj):
    # TODO: add your code here
    origb = orig.reshape([32, 32],order='F')
    projb = proj.reshape([32, 32],order='F')
    
#     fig, (ax1, ax2) = plt.subplots(1,2)
    fig, (ax1, ax2) = plt.subplots(figsize=(9,3), ncols=2)

    origplot = ax1.imshow(origb,aspect='equal')
    fig.colorbar(origplot,ax=ax1)

    ax1.set_title('Original')

   
    
    projplot = ax2.imshow(projb,aspect='equal')
    fig.colorbar(projplot,ax=ax2)


    ax2.set_title('Projection')
    

    plt.show()
                          
    
    
                          
