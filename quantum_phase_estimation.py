#!/usr/bin/env python
# coding: utf-8

# In[369]:


import sys
import numpy as np
import pennylane as qml


# In[373]:


# Part A.1

def fractional_binary_to_float(s):
    """Helper function to expand fractional binary numbers as floats
    
    Parameters:
        s (string): A string in the form "0.xxxx" where x are 0 and 1s
        
    Returns:
        The numerical value of s when converted from fractional binary
    """
    
    nums = s[s.find(".")+1:]
    
    sum = 0
    for i in range(len(nums)):
        sum = sum + int(nums[i])*2**-(i+1)
        
    return sum

print(fractional_binary_to_float("0.1011")==0.6875)    


# In[374]:


# Part A.2

def float_to_fractional_binary(x, max_bits=10):
    """Helper function to turn a float to a string binary digit
    
    Parameters:
        x (float): A numerical value between 0 < x < 1, with a decimal point.
        max_bits (int): The maximum number of bits in the expansion. For x that require
            fewer than max_bits for the expansion, terminate immediately.
        
    Returns:
        A string that is the fractional binary representation, formatted as 0.bbbb
        where there are up to max_bits b.
    """
    
    bin_val = "0."
    val = x
    bit = 0
    while val != 0 and bit <= max_bits:
        val = val * 2
        if (val >= 1):
            bin_val = bin_val + "1"
            val = val - 1
        else:
            bin_val = bin_val + "0"
        bit = bit + 1
        
    return bin_val
    
print(float_to_fractional_binary(0.6875)=="0.1011")


# In[352]:


# Helper function for part B and C

def generate_prob_dict(prob_list):
    prob_dict = {}
    
    for i in range(len(prob_list)):
        bin_val = bin(i)
        bin_val = bin_val[bin_val.find('b')+1:]

        while(len(bin_val) < 3):
            bin_val = '0' + bin_val
            
        prob_dict[bin_val] = prob_list[i]
            
    return prob_dict


# In[362]:


# Part B.1

dev1 = qml.device('default.qubit', wires=['wire1' ,'wire2', 'wire3'], analytic=True)

def qft_3():
    """ 3 qubit Quantum Fourier Transform.
    
    Returns:
        the probabilities of each of the basis states from qml.probs
    """
    
    # The following 2 for loops represent the Quantum Fourier Transform
    for n in range(3,0,-1):
        qml.Hadamard(wires=('wire'+str(n)))
        for k in range(n-1,0,-1):
            b = n-1
            U = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, np.exp((np.pi/float(2**(n-k)))*1j)]])
            qml.QubitUnitary(U, wires=[('wire'+str(k)),('wire'+str(b+1))])  

    qml.SWAP(wires=['wire1','wire3'])
    
    return qml.probs(wires=['wire3', 'wire2', 'wire1'])
    
circuit1 = qml.QNode(qft_3, dev1)
circuit1()

prob_dict = generate_prob_dict(circuit1())

print(prob_dict)


# In[363]:


print(circuit1.draw())


# In[364]:


# Part B.2

dev2 = qml.device('default.qubit', wires=['wire1' ,'wire2', 'wire3'], analytic=False)

def qft_3_with_inverse_check():
    """ 3 qubit Quantum Fourier Transform as well as a 3 Qubit Inverse Fourier Transform
        used to verify QFT implementation        
    
    Returns:
        the probabilities of each of the basis states from qml.probs
    """
        
    # Lets test with 100
    qml.PauliX('wire1')
    
    # The following 2 for loops represent the Quantum Fourier Transform
    for n in range(3,0,-1):
        qml.Hadamard(wires=('wire'+str(n)))
        for k in range(n-1,0,-1):
            b = n-1
            U1 = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, np.exp((np.pi/float(2**(n-k)))*1j)]])
            qml.QubitUnitary(U1, wires=[('wire'+str(k)),('wire'+str(b+1))])  
    
    # The following 2 for loops represent the Inverse Quantum Fourier Transform used to ensure that
    # we can return to the original state after the Quantum Fourier Transform
    for n in range(3):
        for k in range(n):
            U2 = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, np.exp((-np.pi/float(2**(n-k)))*1j)]])
            qml.QubitUnitary(U2, wires=[('wire'+str(k+1)),('wire'+str(n+1))])
        qml.Hadamard(wires=('wire'+str(n+1)))
        
    qml.SWAP(wires=['wire1','wire3'])
    
    #return qml.probs(wires=['wire1' ,'wire2', 'wire3'])
    return qml.probs(wires=['wire3', 'wire2', 'wire1'])
    
circuit2 = qml.QNode(qft_3_with_inverse_check, dev2)
circuit2()

prob_dict = generate_prob_dict(circuit2())

print(prob_dict)


# In[365]:


print(circuit2.draw())


# In[375]:


# Part C

dev3 = qml.device('default.qubit', wires=['wire1' ,'wire2', 'wire3', 'wire4'], shots=5000, analytic=False)

def qpe():
    """ Quantum phase estimation on a single-qubit unitary with 3-bit prcision.
    
    Returns:
        the probabilities of each of the basis stats from qml.probs
    """
    # Initialize qubit 4 to state 1
    qml.PauliX(wires='wire4')
    
    # Transform the other 3 qubits into the Hadamard basis
    qml.Hadamard(wires='wire3')
    qml.Hadamard(wires='wire2')
    qml.Hadamard(wires='wire1')
    
    angle = 5*(np.pi/4)
    U1 = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, np.exp(angle*1j)]])
    
    # The following two for loops represent the relevant controlled unitary operations
    iterations = 1
    for i in range(3):
        for j in range(iterations):
            qml.QubitUnitary(U1, wires=[('wire'+str(i+1)),'wire4'])
        iterations = iterations * 2
    
    qml.SWAP(wires=['wire1','wire3'])
    
    # The following two for loops represent the Inverse Quantum Fourier Transform
    for n in range(3):
        for k in range(n):
            U2 = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, np.exp((-np.pi/float(2**(n-k)))*1j)]])
            qml.QubitUnitary(U2, wires=[('wire'+str(k+1)),('wire'+str(n+1))])
        qml.Hadamard(wires=('wire'+str(n+1)))
            
    return qml.probs(wires=['wire3', 'wire2', 'wire1'])

circuit3 = qml.QNode(qpe, dev3)
prob_dict = generate_prob_dict(circuit3())

def results_to_eigenvalue(prob_dict):
    # Determine the state with the highest probability of  
    # occuring after the Phase Estimation Circuit
    max_key = max(prob_dict, key=prob_dict.get)
    print(max_key)


    # Convert the state to the fractional binary
    print(fractional_binary_to_float("0." + max_key))    


results_to_eigenvalue(prob_dict)
# In[368]:


print(circuit3.draw())

