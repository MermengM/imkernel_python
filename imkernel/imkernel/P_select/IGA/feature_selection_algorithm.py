# -*- coding: utf-8 -*
import torch
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from imkernel.P_select.IGA import surrogate_model 
from alive_progress import alive_bar
import time

# 遗传算法相关函数
def GA(features_number, net, fit_data, upper_bound, lower_bound, pc, t, n):
    population = np.random.randint(2, size=(n, features_number))
    fitness = np.zeros(n)
    for i in range(n):
        fitness[i] = fit_func(population[i], features_number, net, fit_data, upper_bound, lower_bound)
    fitness_change = np.zeros(t)
    with alive_bar(len(range(t))) as bar:
        for i in range(t):
            trial_fitness = np.zeros(n)
            trial_population = selection(population, fitness, features_number)
            trial_population = crossover(trial_population, features_number)
            trial_population = mutation(trial_population, features_number, pc)
            for j in range(n):
                trial_fitness[j] = fit_func(trial_population[j], features_number, net, fit_data, upper_bound, lower_bound)
            fitness = np.append(fitness, trial_fitness)
            population = np.concatenate([population, trial_population])
            sorted_index = np.argsort(fitness)
            fitness = fitness[sorted_index]
            population = population[sorted_index]
            population = population[0:n, :]
            fitness = fitness[0:n]
            fitness_change[i] = max(fitness)
            bar()
            time.sleep(0.05)

    best_fitness = max(fitness)
    best_people = population[fitness.argmax()]
    return best_people, best_fitness, fitness_change, population

def selection(population, fitness, features_number):
    fitness_sum = np.zeros(len(population))
    for i in range(len(population)):
        if i == 0:
            fitness_sum[i] = fitness[i]
        else:
            fitness_sum[i] = fitness[i] + fitness_sum[i-1]
    for i in range(len(population)):
        fitness_sum[i] = fitness_sum[i] / sum(fitness)

    population_new = np.zeros((len(population), features_number))
    for i in range(len(population)):
        rand = np.random.uniform(0, 1)
        for j in range(len(population)):
            if j == 0:
                if rand <= fitness_sum[j]:
                    population_new[i] = population[j]
            else:
                if fitness_sum[j-1] < rand and rand <= fitness_sum[j]:
                    population_new[i] = population[j]
    return population_new

def crossover(population, features_number):
    father = population[0:len(population)//2, :]
    mother = population[len(population)//2:, :]
    np.random.shuffle(father)
    np.random.shuffle(mother)
    for i in range(len(father)):
        father_1 = father[i]
        mother_1 = mother[i]
        difference = []
        for j in range(features_number):
            if father_1[j] != mother_1[j]:
                difference.append(j)
        np.random.shuffle(difference)
        length = len(difference)
        half_length = int(length / 2)
        for k in range(half_length):
            temp = mother_1[difference[k]]
            mother_1[difference[k]] = father_1[difference[k]]
            father_1[difference[k]] = temp
        father[i] = father_1
        mother[i] = mother_1
    population = np.append(father, mother, axis=0)
    return population

def mutation(population, features_number, pc):
    for i in range(len(population)):
        c = np.random.uniform(0, 1)
        if c <= pc:
            mutation_s = population[i]
            zero = []
            one = []
            for j in range(features_number):
                if mutation_s[j] == 0:
                    zero.append(j)
                else:
                    one.append(j)

            if (len(zero) != 0) and (len(one) != 0):
                a = np.random.randint(0, len(zero))
                b = np.random.randint(0, len(one))
                e = zero[a]
                f = one[b]
                mutation_s[e] = 1
                mutation_s[f] = 0
                population[i] = mutation_s

    return population

def fit_func(x, features_number, net, fit_data, upper_bound, lower_bound):
    f1 = sum(x) / (20000 * features_number)
    temp_parameters = np.tile(fit_data, (10, 1))
    for k in range(len(x)):
        if x[k] == 0:
            temp_parameters[:, k] = np.random.random(10) * (upper_bound[k] - lower_bound[k]) + lower_bound[k]
    f2_result = np.zeros(10)
    for k in range(10):
        f2_result[k] = net(torch.from_numpy(np.asarray(temp_parameters[k, :])).float())
    f2 = np.var(f2_result) / 10
    final_fitness = f1 + f2
    return final_fitness

def data_processing(filename):
    readbook = pd.read_excel(f'{filename}.xlsx', engine='openpyxl')
    nplist = readbook.T.to_numpy()
    parameters = nplist[0:-1].T
    label = nplist[-1]
    parameters = parameters.astype(np.float32)
    label = label.astype(np.float32)
    return parameters, label

def plot_fitness_change(fitness_change, t, plot_path, filename="fitness_iteration.png"):
    x = np.arange(0, t, 1)
    plt.xlabel('Iterations')
    plt.ylabel('Fitness')
    plt.plot(x, fitness_change, 'b')
    plt.savefig(filename)
    plt.close()
    print(f"fitness_iteration saved as {plot_path}")

def GA_func(parameters, net, pc, t, n):
    fit_data = parameters[0, :]
    upper_bound = np.max(parameters, axis=0)
    lower_bound = np.min(parameters, axis=0)
    best_people, best_fitness, fitness_change, best_population = GA(
        parameters.shape[1], net, fit_data, upper_bound, lower_bound, pc, t, n
    )
    return best_people, best_fitness, fitness_change, best_population

def load_surrogate_func(model_name, parameters):
    print('-----------------------代理模型加载中---------------------------')
    net = surrogate_model.Net(parameters.shape[1])
    net.load_state_dict(torch.load(model_name))
    print('-----------------------代理模型加载完毕---------------------------')
    return net

def GA_select_model(parameters_n, parameters, net, pc, t, n):
    print('-----------------------特征选择中---------------------------')

    best_people, best_fitness, fitness_change, best_population = GA_func(parameters, net, pc, t, n)

#     feature_name = ['主轴转矩（Nm）', 'B轴温度[℃]', 'C轴温度[℃]', '主轴温度[℃]', '切削液温度[℃]', '温度（℃）', '湿度%', '露点温度（℃）']
    feature_name =parameters_n
    feature_index = [i for i, v in enumerate(best_people) if v == 1]
    print('特征选择结果为：')
    print(' '.join(feature_name[i] for i in feature_index))
    print('-----------------------特征选择完毕---------------------------')
    select_feature = [feature_name[i] for i in feature_index]

    return select_feature, fitness_change, t

# def inference():
#     print('-----------------------数据读取中---------------------------')
#     parameters, labels = data_processing('../dataset/Scenario_4')
#     print('-----------------------数据读取完毕---------------------------')

#     net = load_agent_func(parameters)
    
#     fitness_change, t = P_select_model(parameters, net)

#     return fitness_change, t
