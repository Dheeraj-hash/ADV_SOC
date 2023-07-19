import math
import numpy as np

value_matrix=np.zeros((72**2)*11)

state_matrix=np.zeros((72**2)*11)
        # from -75 to 75 and x=-350
for y in range(-70,75,10):
            x=-345
            value=-1000
            for i in range(11):
                index = (72**2)*i + math.floor((x+360-i)/10) + math.floor((y+360-i)/10)*72
                state_matrix[index]=1
            value_matrix=value_matrix+(value-np.dot(np.transpose(value_matrix),state_matrix))*state_matrix
            state_matrix=np.zeros((72**2)*11)

            #for coordinates at the start of the road
            x=355
            value=1000
            for i in range(11):
                index = (72**2)*i + math.floor((x+360-i)/10) + math.floor((y+360-i)/10)*72
                state_matrix[index]=1
            value_matrix=value_matrix+(value-np.dot(np.transpose(value_matrix),state_matrix))*state_matrix
            state_matrix=np.zeros((72**2)*11)

        # for coordinate in the middle of the grid
for x in range(-335,350,10):
            for y in range(-70,75,10):            
                value= -100 + 200 * (x+335)/(345+335)                
                for i in range(11):
                    index = (72**2)*i + math.floor((x+360-i)/10) + math.floor((y+360-i)/10)*72
                    state_matrix[index]=1
                value_matrix=value_matrix+(value-np.dot(np.transpose(value_matrix),state_matrix))*state_matrix
                state_matrix=np.zeros((72**2)*11)

        # for coordinate in the upeer half
for x in range(-335,340,10):
            for y in range(80,345,10):
                value= -100 + 200 * (x+335)/(345+335) + -100 + -100 * (y-80)/(330-80)
                for i in range(11):
                    index = (72**2)*i + math.floor((x+360-i)/10) + math.floor((y+360-i)/10)*72
                    state_matrix[index]=1
                value_matrix=value_matrix+(value-np.dot(np.transpose(value_matrix),state_matrix))*state_matrix
                state_matrix=np.zeros((72**2)*11)

        #for coordinates in the lower half
for x in range(-335,340,10):
            for y in range(-80,-345,-10):
                value= -100 + 200 * (x+335)/(345+335) + -100 + -100 * (y+80)/(-330+80)
                for i in range(11):
                    index = (72**2)*i + math.floor((x+360-i)/10) + math.floor((y+360-i)/10)*72
                    state_matrix[index]=1
                value_matrix=value_matrix+(value-np.dot(np.transpose(value_matrix),state_matrix))*state_matrix
                state_matrix=np.zeros((72**2)*11)

        #for coordinat on the upper boundary
for x in range(-335,340,10):
            y=345
            value = -1000+ -100 + 200 * (x+335)/(345+335) 
            for i in range(11):
                index = (72**2)*i + math.floor((x+360-i)/10) + math.floor((y+360-i)/10)*72
                state_matrix[index]=1
            value_matrix=value_matrix+(value-np.dot(np.transpose(value_matrix),state_matrix))*state_matrix
            state_matrix=np.zeros((72**2)*11)

            #for coord on the lower boundary
            y=-345
            value = -1000+ -100 + 200 * (x+335)/(345+335) 
            for i in range(11):
                index = (72**2)*i + math.floor((x+360-i)/10) + math.floor((y+360-i)/10)*72
                state_matrix[index]=1
            value_matrix=value_matrix+(value-np.dot(np.transpose(value_matrix),state_matrix))*state_matrix
            state_matrix=np.zeros((72**2)*11)   

        #for coordinate on the upper-left and upper-right boundary
for y in range(80,345,10):
            x=-345
            value= -1000 + -1000 * (y-80)/(340-80)
            for i in range(11):
                index = (72**2)*i + math.floor((x+360-i)/10) + math.floor((y+360-i)/10)*72
                state_matrix[index]=1
            value_matrix=value_matrix+(value-np.dot(np.transpose(value_matrix),state_matrix))*state_matrix
            state_matrix=np.zeros((72**2)*11)  

            x=345
            value= -1000 + -1000 * (y-80)/(340-80)
            for i in range(11):
                index = (72**2)*i + math.floor((x+360-i)/10) + math.floor((y+360-i)/10)*72
                state_matrix[index]=1
            value_matrix=value_matrix+(value-np.dot(np.transpose(value_matrix),state_matrix))*state_matrix
            state_matrix=np.zeros((72**2)*11) 

        #for coordinate on the lower-left and lower-right boundary
for y in range(-80,-345,-10):
            x=-345
            value= -1000 + -1000 * (y+80)/(-340+80)
            for i in range(11):
                index = (72**2)*i + math.floor((x+360-i)/10) + math.floor((y+360-i)/10)*72
                state_matrix[index]=1
            value_matrix=value_matrix+(value-np.dot(np.transpose(value_matrix),state_matrix))*state_matrix
            state_matrix=np.zeros((72**2)*11) 
 
            x=345
            value=-1000 + -1000 * (y+80)/(-340+80)
            for i in range(11):
                index = (72**2)*i + math.floor((x+360-i)/10) + math.floor((y+360-i)/10)*72
                state_matrix[index]=1
            value_matrix=value_matrix+(value-np.dot(np.transpose(value_matrix),state_matrix))*state_matrix
            state_matrix=np.zeros((72**2)*11)   
# for index in range(73,73*4,1):
#     print(value_matrix[index])
print(value_matrix[149])