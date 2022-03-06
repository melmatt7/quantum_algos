#!/usr/bin/env python
# coding: utf-8

# In[7]:


import sys
import numpy as np


# In[130]:


import pennylane as qml

dev1 = qml.device("default.qubit", wires=2, shots=1)
dev2 = qml.device("default.qubit", wires=2, shots=1)
dev3 = qml.device("default.qubit", wires=2, shots=1)


# In[133]:


#Part a and b
@qml.qnode(dev1)
def circuit1():
    qml.BasisState(np.array([0, 0]), wires=[0, 1])
    qml.Hadamard(wires=0)
    qml.CNOT(wires=[0, 1])
    return qml.sample(qml.PauliZ(0)),  qml.sample(qml.PauliZ(1))

print(circuit1())


# In[137]:


#Part c
xbit = 1
ybit = 1
@qml.qnode(dev2)
def circuit2():
    #Bell Pair created
    qml.BasisState(np.array([0, 0]), wires=[0, 1])
    qml.Hadamard(wires=0)
    qml.CNOT(wires=[0, 1])
    
    msg = [xbit, ybit]
    if msg == [0,0]:
        pass        # To send 00 we do nothing
    elif msg == [1,0]:
        qml.PauliX(0) # To send 10 we apply an X-gate
    elif msg == [0,1]:
        qml.PauliZ(0) # To send 01 we apply a Z-gate
    elif msg == [1,1]:
        qml.PauliZ(0) # To send 11, we apply a Z-gate
        qml.PauliX(0) # followed by an X-gate
    
    return qml.probs(wires=[0, 1])  

result = circuit2() 
y = False

print(result)

if result[0] and result[3]!= 0:
    y = 0
elif result[1] and result[2]!= 0:
    y = 1


print("Bob knows y = ", y)


# In[138]:


#Part d
xbit = 1
ybit = 1
@qml.qnode(dev3)
def circuit3():
    #Bell Pair created
    qml.BasisState(np.array([0, 0]), wires=[0, 1])
    qml.Hadamard(wires=0)
    qml.CNOT(wires=[0, 1])
    
    msg = [xbit, ybit]
    if msg == [0,0]:
        pass        # To send 00 we do nothing
    elif msg == [1,0]:
        qml.PauliX(0) # To send 10 we apply an X-gate
    elif msg == [0,1]:
        qml.PauliZ(0) # To send 01 we apply a Z-gate
    elif msg == [1,1]:
        qml.PauliZ(0) # To send 11, we apply a Z-gate
        qml.PauliX(0) # followed by an X-gate
    
    qml.CNOT(wires=[0, 1])
    qml.Hadamard(wires=0)  
    return qml.probs(wires=[0, 1])   
    
result = circuit3() 
state = False

print(result)

if result[0] != 0:
    state = [0,0]
elif result[1] != 0:
    state = [0,1]
elif result[2] != 0:
    state = [1,0]
elif result[3] != 0:
    state = [1,1]


print("Bob knows y = ", state[0])
print("Bob knows x = ", state[1])




