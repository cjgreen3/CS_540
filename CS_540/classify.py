import os
import math
#import numpy
print('Colin Green')
#These first two functions require os operations and so are completed for you
#Completed for you
def load_training_data(vocab, directory):
    """ Create the list of dictionaries """
    top_level = os.listdir(directory)
    dataset = []
    for d in top_level:
        if d[-1] == '/':
            label = d[:-1]
            subdir = d
        else:
            label = d
            subdir = d+"/"
        files = os.listdir(directory+subdir)
        for f in files:
            bow = create_bow(vocab, directory+subdir+f)
            dataset.append({'label': label, 'bow': bow})
            
    return dataset


#Completed for you
def create_vocabulary(directory, cutoff):
    """ Create a vocabulary from the training directory
        return a sorted vocabulary list
    """
    top_level = os.listdir(directory)
    vocab = {}
    for d in top_level:
        subdir = d if d[-1] == '/' else d+'/'
        files = os.listdir(directory+subdir)
        for f in files:
            with open(directory+subdir+f,'r',encoding='utf-8') as doc:
                for word in doc:
                    word = word.strip()
                    if not word in vocab and len(word) > 0:
                        vocab[word] = 1
                    elif len(word) > 0:
                        vocab[word] += 1
    return sorted([word for word in vocab if vocab[word] >= cutoff])



#The rest of the functions need modifications ------------------------------
#Needs modifications
def create_bow(vocab, filepath):
    """ Create a single dictionary for the data
        Note: label may be None
    """
    bow = {}
    # TODO: add your code here
    file = open(filepath,'r', encoding='utf-8')
    lines = file.readlines()
  
 
    
    for line in lines:
        line = line.strip()
        
        if line in vocab:
            
            if (line in bow): 
                bow[line] += 1
            else: 
                bow[line] = 1
        else:
            
            if None in bow:
                bow[None] += 1
            else:
                bow[None] = 1
       
    return bow
  

#Needs modifications
def prior(training_data, label_list):
    """ return the prior probability of the label in the training set
        => frequency of DOCUMENTS
    """

    smooth = 1 # smoothing factor
    logprob = {}
    # TODO: add your code here
    #list = os.listdir()
    #number_files = len(list)
    #print(number_files)
    
    
    for label in label_list:
        count = 0

        for title in training_data:
            if title['label'] == label:
                count +=1
                    
        count=1+count
        num_files = len(training_data)
        p_label = math.log(count) - math.log(len(label_list) + num_files)

        logprob[label] = p_label

    return logprob

#Needs modifications
def p_word_given_label(vocab, training_data, label):
    """ return the class conditional probability of label over all words, with smoothing """

    smooth = 1 # smoothing factor
    word_prob = {}
    # TODO: add your code here
    #wc is total words
    #count is total vocab words
    
    wc= 0        
    count = {}
    count = {word: 0 for word in vocab}
    count[None] = 0
    
    for dic in training_data:
        if dic['label'] == label:
            for word, word_count in dic['bow'].items():
                    wc += word_count
                    count[word] += word_count 
                    
    
    num_vocabs = len(vocab)
    word_prob = {k: math.log(v + 1) - math.log(wc + num_vocabs + 1) for k, v in count.items()}
   
    return word_prob


##################################################################################
#Needs modifications
def train(training_directory, cutoff):
    """ return a dictionary formatted as follows:
            {
             'vocabulary': <the training set vocabulary>,
             'log prior': <the output of prior()>,
             'log p(w|y=2016)': <the output of p_word_given_label() for 2016>,
             'log p(w|y=2020)': <the output of p_word_given_label() for 2020>
            }
    """
    retval = {}
    label_list = os.listdir(training_directory)
    
    # TODO: add your code here
    vocab = create_vocabulary(training_directory, cutoff)
    training_data = load_training_data(vocab, training_directory)
    log_prior = prior(training_data, label_list)
    
    #count = {word: 0 for word in vocab}
    retval = {'vocabulary': vocab, 'log prior': log_prior}
    
    for label in label_list:
        retval['log p(w|y='+ label + ')'] = p_word_given_label(vocab, training_data, label)
    
    return retval

#Needs modifications
def classify(model, filepath):
    """ return a dictionary formatted as follows:
            {
             'predicted y': <'2016' or '2020'>,
             'log p(y=2016|x)': <log probability of 2016 label for the document>,
             'log p(y=2020|x)': <log probability of 2020 label for the document>
            }
    """
    retval = {}
      # TODO: add your code here
    prob_2016 = model['log prior']['2016']
 
    prob_2020 = model['log prior']['2020']
  

    file = open(filepath,'r', encoding='utf-8')
    lines = file.readlines()
    for line in lines:
        line = line.strip()
        if line in model['vocabulary']:
            prob_2016 += model['log p(w|y=2016)'][line]
            prob_2020 += model['log p(w|y=2020)'][line]
        else:
            prob_2016 += model['log p(w|y=2016)'][None]
            prob_2020 += model['log p(w|y=2020)'][None]
            

    retval['log p(y=2016|x)'] = prob_2016 
    retval['log p(y=2020|x)'] = prob_2020
    
    if retval['log p(y=2016|x)'] > retval['log p(y=2020|x)']:
        retval['predicted y'] = '2016'
    else:
        retval['predicted y'] = '2020'

    return retval


