import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms

def get_data_loader(training=True):
    custom_transform= transforms.Compose([transforms.ToTensor(),transforms.Normalize((0.1307,), (0.3081,))])
    train_set = datasets.MNIST('./data', train=True, download=True, transform=custom_transform)
    test_set = datasets.MNIST('./data', train=False,transform=custom_transform)
    if(training==False):
        loader = torch.utils.data.DataLoader(test_set, batch_size = 50)
        return loader
    else:
        loader = torch.utils.data.DataLoader(train_set, batch_size = 50)
        return loader
    
def build_model():
    input_size = 784
    hidden_sizes = [128,64]
    output_size = 10
    model =  nn.Sequential(
        nn.Flatten(), 
        nn.Linear(input_size,hidden_sizes[0]),
        nn.ReLU(),
        nn.Linear(hidden_sizes[0], hidden_sizes[1]),
        nn.ReLU(),
        nn.Linear(hidden_sizes[1],output_size)
        
    )
    return model

def train_model(model, train_loader, criterion, T):
    opt = optim.SGD(model.parameters(), lr=0.001, momentum=0.9)
    model.train()
    for e in range(T):
        ans = 0
        # for data in train_loader:
        for batch_idx, (data, labels) in enumerate(train_loader):
            
            outputs = model(data)

            opt.zero_grad()
            loss = criterion(outputs, labels)
            v = outputs.argmax(dim=1,keepdim=True)
            ans += v.eq(labels.view_as(v)).sum().item()
            loss.backward()
            opt.step()
            # running_loss += loss.item()

            
        print('Train Epoch: {} \t Accuracy: {}/{}({:.2f}%)\tLoss: {:.3f}'.format(

                        e, ans, len(train_loader.dataset),

                        100. * ans / len(train_loader.dataset), loss.item()))


    return

def evaluate_model(model, test_loader, criterion, show_loss=True):
    model.eval()

    # correct = 0
    # total = 0
    avg_loss = 0.0
    sum_loss = 0.0
    with torch.no_grad():
        ans = 0.0
        for batch_idx, (data, labels) in enumerate(test_loader):
            outputs = model(data)
            loss = criterion(outputs, labels)
            v = outputs.argmax(dim=1,keepdim=True)
            ans += v.eq(labels.view_as(v)).sum().item()

            sum_loss += loss.item()

   
    avg_loss = sum_loss / len(test_loader.dataset)

    if(show_loss):
        print('Average loss: {:.4f}'.format(avg_loss))
    print('Accuracy: {:.2f}%'.format(100. * ans / len(test_loader.dataset)))
    
            
    return

def predict_label(model, test_images, index):
    class_names = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
    
    #logits = model(test_images)
    logits = model(test_images[index])


    prob = F.softmax(logits,dim=1)

    t = torch.argsort(prob, descending=True)
    # print(t)
    # torch.set_printoptions(precision=2)
    

    formatted_float0 = "{:.2f}".format(prob[0][t[0][0]].item()*100)
    formatted_float1 = "{:.2f}".format(prob[0][t[0][1]].item()*100)
    formatted_float2 = "{:.2f}".format(prob[0][t[0][2]].item()*100)
   
    print('{}: {}%'.format(class_names[t[0][0]],formatted_float0 ))
    print('{}: {}%'.format(class_names[t[0][1]],formatted_float1 ))
    print('{}: {}%'.format(class_names[t[0][2]],formatted_float2 ))

    return



# def test():
#     train_loader = get_data_loader()
#     print(type(train_loader))
#     print(train_loader.dataset)
#     test_loader = get_data_loader(False)
#     model = build_model()
#     print(model)
#     criterion = nn.CrossEntropyLoss()
#     train_model(model, train_loader, criterion, T = 5)
#     evaluate_model(model, test_loader, criterion, show_loss = True)

#     pred_set, _ = iter(train_loader).next()
#     pred_set = torch.empty(0, 1, 28, 28)
#     for i, (images, labels) in enumerate(test_loader.dataset):
#         if i >= 20:
#             break
#         pred_set = torch.cat((pred_set, images.unsqueeze(0)), dim=0)
#     predict_label(model, pred_set, 1)
#     for i, data in enumerate(test_loader,0):
#         predict_label(model, data[0], 0)
#         break

# test()
