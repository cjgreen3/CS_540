import numpy as np
from matplotlib import pyplot as plt
from csv import reader
import math

from numpy.lib import DataSource


# Feel free to import other packages, if needed.
# As long as they are supported by CSL machines.


def get_dataset(filename):
    """
    TODO: implement this function.

    INPUT: 
        filename - a string representing the path to the csv file.

    RETURNS:
        An n by m+1 array, where n is # data points and m is # features.
        The labels y should be in the first column.
    """
    dataset = []
    

    file = open(filename)
    with open(filename,'r') as read_obj:
        csv_reader = reader(read_obj)
        next(csv_reader)
        for row in csv_reader:
            row = row[1:len(row)]
            temp = []
            for i in row:
                i = float(i)
                temp.append(i)
                
            dataset.append(temp)

    # data = dataset.to_numpy()
    data = np.array(dataset)
    return data
 


def print_stats(dataset, col):
    """
    TODO: implement this function.

    INPUT: 
        dataset - the body fat n by m+1 array
        col     - the index of feature to summarize on. 
                  For example, 1 refers to density.


    RETURNS:
        None
    """
    print(len(dataset))

    count = 0.0
    sum = 0.0
    sd = 0.0
    dev = 0
    n = len(dataset)
    for i in range(n):
        if (not (np.isnan(dataset[i][col]))):
            count+= 1
            sum = sum + dataset[i][col]
    mean = sum/count

   

    for i in range(n):
        if (not (np.isnan(dataset[i][col]))):
            dev = (dataset[i][col]-mean)**2 + dev

    temp = dev/(count-1)
    sd = math.sqrt(temp)

   
    f_m = "{:.2f}".format(mean)
    f_sd = "{:.2f}".format(sd)

    
    print(f_m)
    print(f_sd)


def regression(dataset, cols, betas):
    """
    TODO: implement this function.

    INPUT: 
        dataset - the body fat n by m+1 array
        cols    - a list of feature indices to learn.
                  For example, [1,8] refers to density and abdomen.
        betas   - a list of elements chosen from [beta0, beta1, ..., betam]

    RETURNS:
        mse of the regression model
    """
    mse = 0.0
    
    error = []
    SE = 0.0
    sum = 0.0
    for data in dataset:
        fx = betas[0]
        for c in range(len(cols)):
            fx+=data[cols[c]]*betas[c+1]
        fx = (fx - data[0])**2
        sum += fx
    mse = sum / len(dataset)

    return mse


def gradient_descent(dataset, cols, betas):
    """
    TODO: implement this function.

    INPUT: 
        dataset - the body fat n by m+1 array
        cols    - a list of feature indices to learn.
                  For example, [1,8] refers to density and abdomen.
        betas   - a list of elements chosen from [beta0, beta1, ..., betam]

    RETURNS:
        An 1D array of gradients
    """
    grads = []

    counter = 0
   

   
    z = []
    z = np.array(z)
    X = np.array(dataset)
    Y = np.array(dataset)
    z = np.ones((len(dataset), 1))
    
    arr = np.hstack((z,X[:,cols]))
    arr2 = Y[:,0]

    return_val = np.sum((arr @ betas - arr2).reshape((-1, 1)) * arr,axis = 0)
    return_val = (return_val* 2) / len(dataset)

    return return_val


def iterate_gradient(dataset, cols, betas, T, eta):
    """
    TODO: implement this function.

    INPUT: 
        dataset - the body fat n by m+1 array
        cols    - a list of feature indices to learn.
                  For example, [1,8] refers to density and abdomen.
        betas   - a list of elements chosen from [beta0, beta1, ..., betam]
        T       - # iterations to run
        eta     - learning rate

    RETURNS:
        None
    """
    t = 0
    betaN =[]
    mse = []
    betaPrior = []
    
    grads = []
   
    for t in range(T):
        grads = gradient_descent(dataset,cols,betas)

        betas = betas -  eta*grads
        mse = regression(dataset,cols,betas)

        iter = str(t+1)
  
        print( iter + " " + "{:.2f}".format(mse), end = ' ')
        for l in betas:
            print("{:.2f}".format(l), end = ' ')
        print()
        
  


def compute_betas(dataset, cols):
    """
    TODO: implement this function.

    INPUT: 
        dataset - the body fat n by m+1 array
        cols    - a list of feature indices to learn.
                  For example, [1,8] refers to density and abdomen.

    RETURNS:
        A tuple containing corresponding mse and several learned betas
    """
    X = np.array(dataset)
    Y = np.array(dataset)
    betas = []
    mse = None

  
    z = np.ones((len(dataset), 1))
    arr = np.hstack((z,X[:,cols]))
    
    a = np.linalg.inv(np.transpose(arr) @ arr)
    betas = a @  (arr.T) @ Y[:,0]
    
    mse = regression(dataset,cols,betas)

    return (mse, *betas)


def predict(dataset, cols, features):
    """
    TODO: implement this function.

    INPUT: 
        dataset - the body fat n by m+1 array
        cols    - a list of feature indices to learn.
                  For example, [1,8] refers to density and abdomen.
        features- a list of observed values

    RETURNS:
        The predicted body fat percentage value
    """
    betas = []
    F = np.array(features)
    a = [1]
    fx = np.concatenate((a,F),axis = None)
    _,*betas = compute_betas(dataset,cols)
    result = np.sum(fx @ betas)
    
    
    return result


def synthetic_datasets(betas, alphas, X, sigma):
    """
    TODO: implement this function.

    Input:
        betas  - parameters of the linear model
        alphas - parameters of the quadratic model
        X      - the input array (shape is guaranteed to be (n,1))
        sigma  - standard deviation of noise

    RETURNS:
        Two datasets of shape (n,2) - linear one first, followed by quadratic.
    """
    ldataset = []
    qdataset = []
    a = [1]


    
    for r in X:
        fx = np.concatenate((a,r), axis = None)
        fx =  fx @ betas
        z = np.random.normal(0, sigma,size=1)
        fx = fx + z      
        ldataset.append([fx[0], r[0]])

    ldataset = np.array(ldataset)
    
    # Xs = np.square(X)

    for r in X:
        fx = (np.concatenate((a,r*r), axis = None))
        fx =  fx @ alphas
        z = np.random.normal(0, sigma,size=1)
        fx = fx + z      
        qdataset.append([fx[0], r[0]])

    qdataset = np.array(qdataset)
    

    return ldataset, qdataset


def plot_mse():
    from sys import argv
    if len(argv) == 2 and argv[1] == 'csl':
        import matplotlib
        matplotlib.use('Agg')

    # TODO: Generate datasets and plot an MSE-sigma graph
    X = np.random.randint(-100, 100, size=(1000,1))
    sigmas=[10**-4, 10**-3, 10**-2, 10**-1,1,10, 10**2, 10**3, 10**4, 10**5]
  
    betas = np.array([1,2])
    alphas= np.array([1,2])
    msely = []
    mseqy = []
   
    for s in sigmas:    
        # *ldata,_=synthetic_datasets(betas, alphas, X, s)
        # _,*qdata=synthetic_datasets(betas, alphas, X, s)
        ldata,qdata=synthetic_datasets(betas, alphas, X, s)

        msel=compute_betas(ldata, cols=[1])
        msely.append(msel[0])
        mseq=compute_betas(qdata, cols=[1])
        mseqy.append(mseq[0])
         
    plt.plot(sigmas, msely, '-o', label="Linear")
    plt.plot(sigmas, mseqy, '-o', label="Quadratic")   
    # plt.title('MSE by Sigmas', size=18)
    plt.ylabel('MSEs', size=10, labelpad=10)
    plt.xlabel('SIGMAS', size=10, labelpad=10)

    plt.yscale('log')
    plt.xscale('log')

    plt.legend()
    plt.savefig('mse.pdf')


if __name__ == '__main__':
    ### DO NOT CHANGE THIS SECTION ###
    plot_mse()
# def test():
#     filename = 'bodyfat.csv'
#     dataset = get_dataset(filename)
    # print(dataset)
    # print(dataset.shape)
    # print_stats(dataset, 1)
    # print(regression(dataset,cols=[2,3], betas=[0,0,0]))
    # print(regression(dataset,cols=[2,3,4], betas=[0,-1.1,-.2,3]))
    # print(gradient_descent(dataset, cols=[2,3], betas=[0,0,0]))
    #  iterate_gradient(dataset, cols=[1,8], betas=[400,-400,300], T=10, eta=1e-4)
    # print(compute_betas(dataset, cols=[1,2]))
    # print(predict(dataset, cols=[1,2], features=[1.0708, 23]))
    # print(synthetic_datasets(np.array([0,2]), np.array([0,1]), np.array([[4]]), 1))

# test()