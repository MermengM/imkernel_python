import torch
import torch.nn.functional as F
import matplotlib.pyplot as plt
from torch.utils.data import DataLoader
from alive_progress import alive_bar
import time
import numpy as np
import pandas as pd

class MyDataset(torch.utils.data.Dataset):
    def __init__(self, X, y):
        self.X = X
        self.y = y
        
    def __len__(self):
        return len(self.X)
    
    def __getitem__(self, index):
        return self.X[index], self.y[index]

class Net(torch.nn.Module):      
    def __init__(self, features):
        super(Net, self).__init__() 
        self.h1 = torch.nn.Linear(features, int((features+1)*2/3), bias=True)
        self.a1 = torch.nn.ReLU()
        self.h2 = torch.nn.Linear(int((features+1)*2/3), int((features+1)*4/9))
        self.a2 = torch.nn.ReLU()
        self.regression = torch.nn.Linear(int((features+1)*4/9), 1)
        
    def forward(self, x): 
        x = self.h1(x)
        x = self.a1(x)
        x = self.h2(x)
        x = self.a2(x)
        y_pred = self.regression(x).squeeze(-1)
        return y_pred
    
def data_processing(filename):
    readbook = pd.read_excel(f'{filename}.xlsx', engine='openpyxl')
    nplist = readbook.T.to_numpy()
    parameters = nplist[0:-1].T
    label = nplist[-1]
    parameters = parameters.astype(np.float32)
    label = label.astype(np.float32)
    parameters_n = readbook.columns[:-1].to_numpy()
    return parameters, label, parameters_n

def train_model(X_train, Y_train, features, plot_path, model_name='model', total_epoch=1000, learning_rate=1e-3):
    net = Net(features)
    optimizer = torch.optim.Adam(net.parameters(), lr=learning_rate)
    loss_func = torch.nn.MSELoss()
    dataset = MyDataset(X_train, Y_train)
    dataloader = DataLoader(dataset, batch_size=1, shuffle=True)
    loss_change = np.zeros(total_epoch)
    
    with alive_bar(total_epoch) as bar:
        for epoch in range(total_epoch):
            net.train()
            for inputs, labels in dataloader:
                outputs = net(inputs)
                loss = loss_func(outputs, labels)
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
            bar()
            time.sleep(0.05)
            loss_change[epoch] = loss.item()
            
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.plot(np.arange(total_epoch), loss_change, 'r')
    plt.savefig(plot_path)
    plt.close()
    print(f"loss_iteration saved as {plot_path}")
    # 保存模型
    torch.save(net.state_dict(), model_name + '.pth')
    print(f"Model saved as {model_name}.pth")
    
    return total_epoch, loss_change
    

def train_surrogate_func(parameters, labels, features, plot_path, model_name='model', total_epoch=1000):
    train_model(parameters, labels, features, plot_path, model_name=model_name, total_epoch=total_epoch)
