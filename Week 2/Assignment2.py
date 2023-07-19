import numpy as np
from argparse import ArgumentParser as ap
import math

parser = ap()
parser.add_argument('--path',type=str,required=True)
file_name=parser.parse_args()

num=0

data=np.genfromtxt(file_name.path)

start=np.where(data==2)

start=[start[0][0],start[1][0]]

end=np.where(data==3)

end=[end[0][0],end[1][0]]

# policy=np.zeros(((data.size-1) * 4,5))

# policy=[]
index=0
l=[]
for state_x in range(data.shape[0]):
    for state_y in range(data.shape[0]):
        if data[state_x,state_y]==1 or data[state_x,state_y]==3:
            continue
        # l=[]
        l.append([[state_x,state_y]])
        l[index].append("UP")
        if state_x==0 or data[state_x-1,state_y]==1:
            l[index].append([state_x,state_y])
            l[index].append(-1)
            l[index].append(1)    
            index+=1
               
        elif data[state_x-1,state_y]==3:
            l[index].append([state_x-1,state_y])
            l[index].append(0)
            l[index].append(1)    
            index+=1
              
        else:
            l[index].append([state_x-1,state_y])
            l[index].append(-1)
            l[index].append(1)    
            index+=1
        

        l.append([[state_x,state_y]])
        l[index].append("DOWN")
        if state_x==data.shape[0]-1 or data[state_x+1,state_y]==1:
            l[index].append([state_x,state_y])
            l[index].append(-1)
            l[index].append(1)    
            index+=1
                
        elif data[state_x+1,state_y]==3:
            l[index].append([state_x+1,state_y])
            l[index].append(0)
            l[index].append(1)    
            index+=1
             
        else:
            l[index].append([state_x+1,state_y])
            l[index].append(-1)
            l[index].append(1)    
            index+=1

        l.append([[state_x,state_y]])
        l[index].append("LEFT")
        if state_y==0 or data[state_x,state_y-1]==1:
            l[index].append([state_x,state_y])
            l[index].append(-1)
            l[index].append(1)    
            index+=1
                
        elif data[state_x,state_y-1]==3:
            l[index].append([state_x,state_y-1])
            l[index].append(0)
            l[index].append(1)    
            index+=1
             
        else:
            l[index].append([state_x,state_y-1])
            l[index].append(-1)
            l[index].append(1)    
            index+=1

        l.append([[state_x,state_y]])
        l[index].append("RIGHT")
        if state_y==data.shape[0]-1 or data[state_x,state_y+1]==1:
            l[index].append([state_x,state_y])
            l[index].append(-1)
            l[index].append(1)    
            index+=1
                
        elif data[state_x,state_y+1]==3:
            l[index].append([state_x,state_y+1])
            l[index].append(0)
            l[index].append(1)    
            index+=1
             
        else:
            l[index].append([state_x,state_y+1])
            l[index].append(-1)
            l[index].append(1)    
            index+=1

# print(l)

value_fn=np.zeros((data.shape[0],data.shape[0]))

policy_fn=np.zeros((data.shape[0],data.shape[0],4))

policy_name=np.zeros((data.shape[0],data.shape[0]))

for iter in range(100):

    for state_x in range(data.shape[0]):

        for state_y in range(data.shape[0]):

            # num=0

            for action in ["UP","DOWN","RIGHT","LEFT"]:

                # num=0

                for i in l:

                    if i[0] == [state_x,state_y] and i[1] == action:
                        
                        if action=="UP":

                            policy_fn[state_x,state_y,0] += i[4]*(i[3] + value_fn[i[2][0],i[2][1]])

                        if action=="DOWN":

                            policy_fn[state_x,state_y,1] += i[4]*(i[3] + value_fn[i[2][0],i[2][1]])

                        if action=="RIGHT":

                            policy_fn[state_x,state_y,2] += i[4]*(i[3] + value_fn[i[2][0],i[2][1]])

                        if action=="LEFT":

                            policy_fn[state_x,state_y,3] += i[4]*(i[3] + value_fn[i[2][0],i[2][1]])

                    # num+=1

            value_fn[state_x,state_y] = np.max(policy_fn[state_x,state_y])
            
            x=np.where(policy_fn[state_x,state_y]==np.max(policy_fn[state_x,state_y]))
            
            policy_name[state_x,state_y]=x[0][0]
            
            policy_fn[state_x,state_y]=0
    
policy=[]

state=start

while state != end:

    x=policy_name[state[0],state[1]]

    policy.append(x)

    if x==0:

        state=[state[0]-1,state[1]]

    elif x==1:

        state=[state[0]+1,state[1]]

    elif x==2:

        state=[state[0],state[1]+1]

    else:

        state=[state[0],state[1]-1]

print(policy)

            
 


