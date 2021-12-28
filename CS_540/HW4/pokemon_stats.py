import numpy as np
import math
from numpy import inf
import csv
import random
import matplotlib.pyplot as plt



def load_data(filepath):
    l = []
    with open(filepath, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        i = 0
        for row in reader:
#           for row in reader:
            r_dic = {}
            if(i==20):
                break
            for k,v in row.items():
                if((k == 'Name') or (k =='Type 1')or(k == 'Type 2')):
                    r_dic[k] = v
                elif((k == 'Generation') or (k == 'Legendary')):
                    pass  
                else:
                    r_dic[k] = int(v)
                    
            l.append(r_dic)
            i += 1
    return l
def calculate_x_y(stats):
    x = stats['Attack'] + stats['Sp. Atk'] + stats['Speed']
    y = stats['Defense'] + stats['Sp. Def'] + stats['HP']
    tup = (x,y)
    
    return tup

def find_distance(tup1, tup2):
    return pow(((tup1[0]-tup2[0])**2+(tup1[1]-tup2[1])**2),0.5)


def create_dist_list(dataset):
    distance_list=[]
    sorted_by_second=[]
    for i in range(0,len(dataset)):    
        for j in range(i+1, len(dataset)):

                temp_dis = find_distance(dataset[i], dataset[j])
                distance_list.append([i,j,temp_dis,2,i,j])
 
    # sorted_by_second = sorted(distance_list, key=lambda tup: tup[2])
    sorted_by_second = sorted(distance_list, key=lambda tup: (tup[2],tup[0],tup[1]))
   
    return sorted_by_second

def create_Z_matrix(distance_list,dataset):
#     Z = np.zeros((len(dataset) - 1, 4))
    index_lines = []
    
    Z = ([])
    removal_count=0
    
    for i in range(0,len(distance_list)):
       
        if((distance_list[i][0] == distance_list[i][1])or not math.isfinite(distance_list[i][2])):
            removal_count =removal_count+1
        if((distance_list[i][0] != distance_list[i][1])and math.isfinite(distance_list[i][2])):
            if distance_list[i][0] >= len(dataset) and distance_list[i][1] >= len(dataset):
                distance_list[i][3] = Z[distance_list[i][0] - len(dataset)][3] + Z[distance_list[i][1] - len(dataset)][3]
            elif distance_list[i][0] >= len(dataset):
                distance_list[i][3] = Z[distance_list[i][0] - len(dataset)][3] + 1
            elif distance_list[i][1] >= len(dataset):
                distance_list[i][3] = Z[distance_list[i][1] - len(dataset)][3] + 1
            else:
                distance_list[i][3] = 2
            Z.append([distance_list[i][0],distance_list[i][1],distance_list[i][2],distance_list[i][3]])  
            index_lines.append([distance_list[i][4], distance_list[i][5]])

            for j in range(i+1,len(distance_list)):
                

                if(distance_list[j][0] == distance_list[i][0]):
                   
                    distance_list[j][0] = i + len(dataset)-removal_count
                   
                    if(distance_list[i][0] > len(dataset) and distance_list[i][1] > len(dataset)):
                        distance_list[j][3] = distance_list[i][3] + distance_list[j][3]
                        if(distance_list[i][0] != distance_list[i][1]):
                            distance_list[j][3] = distance_list[i][3] + distance_list[j][3]
                    else:
                        distance_list[j][3] = distance_list[i][3] + 1

                   
                   
            for j in range(i+1,len(distance_list)):
                if(distance_list[j][1] == distance_list[i][1]):
                   
                    distance_list[j][1] = i + len(dataset) -removal_count
                    if(distance_list[i][0] > len(dataset) and distance_list[i][1] > len(dataset)):
                        distance_list[j][3] = distance_list[i][3] + distance_list[j][3]
                        if(distance_list[i][0] != distance_list[i][1]):
        
                            distance_list[j][3] = distance_list[i][3] + distance_list[j][3]

                    else:
                        distance_list[j][3] = distance_list[i][3] + 1

                   
               
                   
            for j in range(i+1,len(distance_list)):
                if(distance_list[j][0] == distance_list[i][1]):
                    distance_list[j][0] = i + len(dataset)-removal_count
                    if(distance_list[i][0] > len(dataset) and distance_list[i][1] > len(dataset)):
                        distance_list[j][3] = distance_list[i][3] + distance_list[j][3]
                        
                        if(distance_list[i][0] == distance_list[i][1]):
                            distance_list[j][3] = distance_list[i][3] + distance_list[j][3]
                    else:
                        distance_list[j][3] = distance_list[i][3] + 1

                   
                 
                       
            for j in range(i+1,len(distance_list)):
                if(distance_list[j][1] == distance_list[i][0]):
                    distance_list[j][1] = i + len(dataset)-removal_count
                    if(distance_list[i][0] > len(dataset) and distance_list[i][1] > len(dataset)):
                        distance_list[j][3] = distance_list[i][3] + distance_list[j][3]
                        
                        if(distance_list[i][0] != distance_list[i][1]):
                            distance_list[j][3] = distance_list[i][3] + distance_list[j][3]

                    else:
                        distance_list[j][3] = distance_list[i][3] + 1

            distance_list = sorted(distance_list, key=lambda tup: (tup[2],tup[0],tup[1]))
    for k in range(0,len(Z)):
        if Z[k][1]<Z[k][0]:
            temp2 = Z[k][1]
            Z[k][1] = Z[k][0]
            Z[k][0] = temp2
            
    return Z, index_lines
       
def hac(dataset):
    # for l in dataset:
    #     if(not(isinstance(l[0],int))):
    #         dataset.remove(l)
    #     elif(not (isinstance(l[1],int))):
    #         dataset.remove(l)
    for l in dataset:
        if(math.isnan(l[0])or math.isinf(l[0])):
            dataset.remove(l)
        elif(math.isnan(l[1])or math.isinf(l[1])):
            dataset.remove(l)

    return_list = []
    distance_list = []
    cluster_number = len(dataset)

    distance_list = create_dist_list(dataset)
   
    Z,index_lines = create_Z_matrix(distance_list,dataset)

    returned_matrix = np.array(Z)
    
    return returned_matrix

def random_x_y(m):
        return_val = []
        for n in range(m):
            x = random.randint(1,359)
            y = random.randint(1,359)
            tup = (x,y)
            return_val.append(tup)
        # return_val=[(random.randint(1,359),random.randint(1,359)) for i in in range(m)]

        return return_val
    
def imshow_hac(dataset):
#     Z = main()
    for l in dataset:
        if(not(isinstance(l[0],int))):
            dataset.remove(l)
        elif(not (isinstance(l[1],int))):
            dataset.remove(l)

    return_list = []
    distance_list = []
    cluster_number = len(dataset)

    distance_list = create_dist_list(dataset)
   
    Z,index_lines = create_Z_matrix(distance_list,dataset)
    fig = plt.figure(figsize=(25,10))
    plt.axis([0,400,0,350])
    for i in range(len(dataset)):
        plt.scatter(dataset[i][0],dataset[i][1])
    for index in index_lines:

        x = [dataset[index[0]][0],dataset[index[1]][0]]
        y = [dataset[index[0]][1],dataset[index[1]][1]]
        plt.plot(x,y)
        plt.pause(0.1)

    plt.pause(0.5)
    plt.show()

if __name__=="__main__":
    data = load_data('pokemon.csv')
    mt = []
    for d in data:
        (x,y) = calculate_x_y(d)
        mt.append([x,y])
    hac(mt)
    imshow_hac(mt)
# def test():
#     data = load_data('pokemon.csv')
#     mt = []
#     for d in data:
#         (x,y) = calculate_x_y(d)
#         mt.append([x,y])
#     print(linkage(np.array(mt)))
    
