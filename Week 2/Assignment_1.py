import numpy as np
from argparse import ArgumentParser as ap
import math

parser = ap()
parser.add_argument('--path',type=str,required=True)
file_name=parser.parse_args()

num=0

data=np.genfromtxt(file_name.path)

# data=np.round(data,2)

# print(data)

value_fn=np.zeros(10)

policy_fn=np.zeros((10,5))

policy_name=np.zeros(10)

# print(data[0][0])
# print(data[0][4]*(data[0][3] ))

# print(value_fn[int(data[0][2])])
for iter in range(100):

    for state in range(10):

        for action in range(5):

            for i in data:

                if i[0] == state and i[1] == action:

                    policy_fn[state,action] += i[4]*(i[3] + 0.9*value_fn[int(i[2])])


        value_fn[state] = np.max(policy_fn[state])
        policy_fn[state]=0
    
    # print(value_fn)
        #policy_name = np.where(policy_fn[state]==value_fn[state])


#policy_fn=np.round(policy_fn,decimals=1)

#print(policy_fn)

value_fn= np.round(value_fn,decimals=2)

print(value_fn)