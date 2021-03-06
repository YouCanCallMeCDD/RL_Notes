#encoding:utf-8
from __future__ import print_function
from __future__ import division

from bandit import Bandit
import numpy as np
import matplotlib.pyplot as plt

def experiment_1(k, nb_bandits, epochs, epsilons, step=None, UCB=False):
    c = 2

    bd = [Bandit(k) for _ in range(nb_bandits)]
    #记录画图参数
    #plt.axis([0, epochs+10, 0, 5])
    #plt.ion()
    rewards = []
    optimals = []
    for epsilon in epsilons:
        if epsilon < 0:
            values = np.zeros(shape=(nb_bandits, k), dtype=np.float32) #记录当前每个action的估值
            UCB = True
        elif epsilon <=0.00001:
            values = np.ones(shape=(nb_bandits, k), dtype=np.float32) #记录当前每个action的估值
            values *= 5
            UCB = False
        else:
            values = np.zeros(shape=(nb_bandits, k), dtype=np.float32) #记录当前每个action的估值
            UCB = False
        counts = np.zeros(shape=(nb_bandits, k), dtype=np.float32) #记录每个action被选择了多少次

        print("Epsilon: ", epsilon)
        record_rewards = []
        record_actions = []
        for epoch in range(epochs):
            total_rewards = np.zeros(nb_bandits) #记录每个老虎机的总rewards
            count_opitmal = np.zeros(nb_bandits) #记录每个老虎机最优action被选择的次数
            for i in range(nb_bandits):
                if UCB is True:
                    action = np.argmax(values[i] + c * np.sqrt(np.log(epoch+1) / (counts[i]+0.0000001)))

                elif epsilon > 1:
                    #作弊，直接选择最优动作
                    action = bd[i].get_optimal_action()
                elif np.random.rand() <= epsilon:
                    #randomly selected
                    action = np.random.randint(0, k)
                else:
                    action = np.argmax(values[i])

                reward = bd[i].step(action)

                total_rewards[i] += reward
                count_opitmal[i] += 1 if action == bd[i].get_optimal_action() else 0

                #updates
                counts[i][action] += 1
                if step is None:
                    values[i][action] += (reward - values[i][action]) / counts[i][action]
                else:
                    values[i][action] += (reward - values[i][action]) * step #固定步长


            #此时所有bandit都更新了一遍了
            mean_rewards= np.mean(total_rewards)
            record_rewards.append(mean_rewards)
            record_actions.append(np.mean(count_opitmal))
            #实时画图
            """
            plt.scatter(epoch, mean_rewards, marker=".")
            plt.pause(0.005)
            """

        """
        while True:
            plt.pause(0.05)
        """
        rewards.append(record_rewards)
        optimals.append(record_actions)

    lines = {}
    labels = [i if i<=1 else "groundtruth" for i in epsilons]
    for i in range(len(rewards)):
        lines[i], = plt.plot(range(epochs), rewards[i], label=str(labels[i]))
    plt.legend(handles=list(lines.values()), loc=4)
    plt.show()

    for i in range(len(optimals)):
        lines[i], = plt.plot(range(epochs), optimals[i], label=str(labels[i]))
    plt.legend(handles=list(lines.values()), loc=4)
    plt.show()

def experiment2(k, nb_bandits, epochs):


    epsilon = 0.1

    alpha = 0.1 #固定步长

    rewards = []
    optimals = []

    methods =["avg", "weight"]
    for method in methods:
        bd = [Bandit(k, stationary=False) for _ in range(nb_bandits)]
        values = np.zeros(shape=(nb_bandits, k), dtype=np.float32) #记录当前每个action的估值
        counts = np.zeros(shape=(nb_bandits, k), dtype=np.float32) #记录每个action被选择了多少次
        #print("Epsilon: ", epsilon)
        print("Method: ", method)
        record_rewards = []
        record_actions = []
        for epoch in range(epochs):
            total_rewards = np.zeros(nb_bandits) #记录每个老虎机的总rewards
            count_opitmal = np.zeros(nb_bandits) #记录每个老虎机最优action被选择的次数
            for i in range(nb_bandits):
                if epsilon > 1:
                    #作弊，直接选择最优动作
                    action = bd[i].get_optimal_action()
                elif np.random.rand() <= epsilon:
                    #randomly selected
                    action = np.random.randint(0, k)
                else:
                    action = np.argmax(values[i])

                reward = bd[i].step(action)

                total_rewards[i] += reward
                count_opitmal[i] += 1 if action == bd[i].get_optimal_action() else 0

                #updates
                counts[i][action] += 1
                if method=="avg":
                    values[i][action] += (reward - values[i][action]) / counts[i][action]
                else:
                    values[i][action] += alpha * (reward - values[i][action])

            #此时所有bandit都更新了一遍了
            mean_rewards= np.mean(total_rewards)
            record_rewards.append(mean_rewards)
            record_actions.append(np.mean(count_opitmal))
            #实时画图
            """
            plt.scatter(epoch, mean_rewards, marker=".")
            plt.pause(0.005)
            """

        """
        while True:
            plt.pause(0.05)
        """
        rewards.append(record_rewards)
        optimals.append(record_actions)

    lines = {}
    labels = [i for i in methods]
    for i in range(len(rewards)):
        lines[i], = plt.plot(range(epochs), rewards[i], label=str(labels[i]))
    plt.legend(handles=list(lines.values()), loc=4)
    plt.show()

    for i in range(len(optimals)):
        lines[i], = plt.plot(range(epochs), optimals[i], label=str(labels[i]))
    plt.legend(handles=list(lines.values()), loc=4)
    plt.show()

def run_1():
    k = 10 #10 armed
    nb_bandits = 2000
    epochs = 1000 #每个bandit实验1000次

    #epsilons = [0.0, 0.01, 0.1, 0.5, 1, 10] #10表示groundtruth
    #epsilons = [0.0, 0.1, 10]
    epsilons = [-1.0, 0.1, 10]


    #experiment_1(k, nb_bandits, epochs, epsilons, step=0.1)
    experiment_1(k, nb_bandits, epochs, epsilons)


def run_2():
    k = 10
    nb_bandits = 2000
    epochs = 10000


    experiment2(k, nb_bandits, epochs)

if __name__ == "__main__":
    run_1()
