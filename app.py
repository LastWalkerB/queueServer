import streamlit as st

import pandas as pd 
import numpy as np  

import os
#import joblib

#import matplotlib.pyplot as plt
import seaborn as sns

#matplotlib.use("Agg")
def computeProbOfnCustomers(n, queue):
    count = 0
    for i in queue:
        if i == n:
            count+=1
    return count/len(queue)

def generateUniform(min, max, size):
    return np.random.uniform(min,max,size)
def generateGaussian(mean, sd, size):
    return np.random.normal(mean, sd, size) #generating Gaussian distribution

#Function to produce the table based on arrival and service times
def createTable(arrivalTime, serviceTime, n = 0):
    delay = np.zeros(len(arrivalTime))
    interArrivalTime = np.zeros(len(arrivalTime))
    timeOfService = np.zeros(len(arrivalTime))
    exitTime = np.zeros(len(arrivalTime))
    queueLength = np.zeros(len(arrivalTime))
    waitingTime = np.zeros(len(arrivalTime))
    averageWaitingTime = np.zeros(len(arrivalTime))
    averageNumberQueue = np.zeros(len(arrivalTime))
    probOfnCustomers = np.zeros(len(arrivalTime))
    probOfBusyServers = np.zeros(len(arrivalTime))
    zeroQueueCount = 0 #number of times queue length is zero
    flag = 1 #arival times must be ascendigly sorted.
    for i in range(0, len(arrivalTime)):
        print(flag)
        if i == 0:
            interArrivalTime[0] = arrivalTime[0]
            delay[0] = 0
            timeOfService[0] = arrivalTime[0]
            waitingTime[0] = 0
            exitTime[0] = timeOfService[0] + serviceTime[0]
        else:
            queueLength[i] = queueLength[i - 1]
            if queueLength[i] == 0: 
                zeroQueueCount = zeroQueueCount + 1
            interArrivalTime[i] = arrivalTime[i] - arrivalTime[i-1]
            delay[i] = exitTime[i-1] - arrivalTime[i]
            timeOfService[i] = exitTime[i-1]
            exitTime[i] = timeOfService[i] + serviceTime[i]
            waitingTime[i] = exitTime[i-1] - arrivalTime[i]
            #computing cumilative average of waiting time
            averageWaitingTime[i] = (averageWaitingTime[i-1]*(i-1)
            + waitingTime[i])/(i+1)
            #computing cumilative average of queue length
            averageNumberQueue[i] = (averageNumberQueue[i-1]*(i-1)
            + queueLength[i])/(i+1)
            for j in arrivalTime[flag:]:
                if j < exitTime[i]:
                    queueLength[i] = queueLength[i] + 1
                    flag = flag +1  
            
            queueLength[i] = queueLength[i] - 1
            probOfnCustomers[i] = computeProbOfnCustomers(n, queueLength[0:i])
            #server is idle
            if (exitTime[i-1] < arrivalTime[i]):
                probOfBusyServers[i] = 0
            else:
                probOfBusyServers[i] = 1
             
    dataset = pd.DataFrame({'inter Arrival Time': interArrivalTime, 'Arrival time': arrivalTime, 
                            'waiting Time': waitingTime,
                            'delay': delay, 'Time of service': timeOfService, 'Service Time': serviceTime, 
                           'exit time': exitTime, 'queue length': queueLength,
                           '(Wq) average waiting time': averageWaitingTime,
                            '(Lq) average queue length': averageNumberQueue,
                           '(Pn) probability of n customers': probOfnCustomers,
                           '(roh) probability of busy server': probOfBusyServers})
    return dataset
            
            
def main():

    st.title("SMS Assignment 1")
    menu = ["GivenTable", "custom"]
    choice = st.sidebar.selectbox("Menu",menu)
    if choice =="GivenTable":
        st.subheader("Home")
        #arrival times
        arrivalTime = np.array([0.5,4.1,5.5,5.9,10.5,22])         
        serviceTime = np.array([10.4,5.4,5.2,12.3,9.4,5])
        ans = createTable(arrivalTime, serviceTime)
        st.write(ans)
    if choice == "custom":
        size = st.sidebar.text_input("Choose size", 10)
        submenu = ["Uniform", "Gaussian"]
        choice1 = st.sidebar.selectbox("arrival time", submenu)
        
        if choice1 == "Uniform":
            min = st.sidebar.text_input("minimum", 4,1)
            max = st.sidebar.text_input("maximum", 6, 2)
            arrivalTimes = generateUniform(int(min),int(max),int(size)) 
        if choice1 == "Gaussian":
            mean = st.sidebar.text_input("mean", 10, 3)
            sd = st.sidebar.text_input("standard deviation", 5, 4)
            arrivalTimes = generateGaussian(int(mean), int(sd), int(size))

        choice2 = st.sidebar.selectbox("service time", submenu)
        if choice2 == "Uniform":
            min1 = st.sidebar.text_input("minimum", 4, 5)
            max1 = st.sidebar.text_input("maximum", 6, 6)
            serviceTimes = generateUniform(int(min1),int(max1),int(size)) 
        if choice2 == "Gaussian":
            mean1 = st.sidebar.text_input("mean", 10, 7)
            sd1 = st.sidebar.text_input("standard deviation", 5, 8)
            serviceTimes = generateGaussian(int(mean1), int(sd1), int(size))
        if st.sidebar.button("Generate Table", 9):
            st.write(createTable(arrivalTimes, serviceTimes))
    
if __name__ == '__main__':
    main()