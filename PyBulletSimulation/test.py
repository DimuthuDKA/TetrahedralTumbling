import mob as m
import time
import math
import periconfig as p


sim = m.Simulation("snake2", 100, True)
sim.start()


#position and orientation, start 
position = sim.getPosition()
print('position value:')
print(position)
fullPosition = sim.getFullPosition()
print("fullPosition value:")
print(fullPosition)

orientation = sim.getOrientation()
print("orientation")
print(orientation)

'''
The STRENGTH parameter indicates the degree to which the bend occurs, and is defined on [0, 0.3], which is locked in the program
The DIRECTION parameter indicates in what direction the limb will bend, and is defined on (-infinity, infinity) much as #the sine and cosine functions are. Directions chosen are irrespective of the simplest form direction in the range (-pi, pi)
'''



#moving the robot in a particular direction
def strength1(t,i):
	#return (math.sin(t*0.5))
	return (math.sin(t * 3 * math.pi + 1)*0.3)

def strength2(t,i):
	#return (math.cos(t*0.5 - 1.5))
	return (math.sin(t * 3 * math.pi + 0)*-0.3) 

def strength3(t,i):
	return (math.sin(t * 2 * math.pi) * 0.3)
	
def strength31(t,i):
	return (math.sin(t * 2 * math.pi) * -0.3)
	
def strength4(t,i):
	return (math.cos(t * 2 * math.pi) * 0.3)
	
def strength5(t,i):
	return (math.cos(t * 2 * math.pi) * 0.3)

def rest(t,i):
	#return (t + i)
	return(0)

def direction1(t,i):
	return (0)

def direction2(t,i):
	return (0)
#Turning the robot, apply to lower limbs, 1-3
def counterClockwise(t,i):
	return((t * 2)*.3)
	
def clockwise(t,i):
	return((t * 2)*-.3)


#Flipping
def bent(t,i):
	#sim.oneStrength(0.2)
	pass
	
def bent2(t,i):
	return(0.5 * t)

def bent3(t,i):
	return(5) #moving v2

def bent4(t,i):
	return(t)*.3

def bent5(t,i):
	return((t*2)*.3) #moving v2

def bent6(t,i):
	return(-1)

def bent7(t,i):
	return((t*100)*.3)
	
	
def walkfunc(t, i):
	return (t) * math.pi 

def walkfunc2(t, i):
	return (t) * math.pi * -.05

def t(t,i):
	return(t)
    	
# #TURNING
# #counter clockwise direction
f=.5


sim.registerPeriodical(sim.tetraWrapper, p.peri.wrapped_export, f)
# gives at rest position, USE IF YOU WANT ROBOT TO BE "STANDING"
# sim.head(0.3, -1000, 0)  #left limb (1)
# sim.middle(0.3, -1000, 0) #back limb (2)
# sim.tail(0.3, -1000, 0) #limb lower right (3)
# sim.rearRight(0, 0, 0) # top limb (4)
# sim.registerPeriodical(sim.oneStrength, counterClockwise, f) #limb lower left (1)
# sim.registerPeriodical(sim.twoStrength, counterClockwise, f) #limb furthest away (2) (back)
# sim.registerPeriodical(sim.threeStrength, counterClockwise, f)#limb lower right (3)
# sim.registerPeriodical(sim.fourStrength, rest, f) #limb on top (4)

#clockwise direction
# sim.registerPeriodical(sim.oneStrength, clockwise, f) #limb lower left (1)
# sim.registerPeriodical(sim.twoStrength, clockwise, f) #limb furthest away (2) (back)
# sim.registerPeriodical(sim.threeStrength, clockwise, f) #limb lower right (3)
# sim.registerPeriodical(sim.fourStrength, rest, f) #limb on top (4)

# clockwise direction ALT 1 <-- works, notstanding
# f=.5
# sim.registerPeriodical(sim.oneStrength, bent5, f) 
# sim.registerPeriodical(sim.oneDirection, walkfunc, f) 
# sim.registerPeriodical(sim.threeStrength, bent5, f) 
# sim.registerPeriodical(sim.threeDirection, walkfunc, f) 



#attempting counterClockwise ALT2
##f = .7
##sim.registerPeriodical(sim.oneStrength, bent4, f) 
##sim.registerPeriodical(sim.oneDirection, walkfunc2, f) 
##sim.registerPeriodical(sim.threeStrength, bent4, f) 
##sim.registerPeriodical(sim.threeDirection, walkfunc2, f) 



# #FLIPPING
#doesn't work
# #Flipping the robot over, limb 1 in the place of limb 4. Make the other two limbs use strength1,2 to flip the robot over

##sim.head(0.0, 5.3, 0)  #left limb (1)
##sim.middle(0.0, 5.3, 0) #back limb (2)
##sim.tail(0.0, 5.3, 0) #limb lower right (3)
##sim.rearRight(0.0, 0, 0) # top limb (4)

#VERSION1
##[  
##f=1
##sim.registerPeriodical(sim.oneStrength, bent5, f) #left limb (1)
##sim.registerPeriodical(sim.twoStrength, bent5, f) #back limb (2)
##sim.registerPeriodical(sim.threeStrength, bent5, f)
##] ##turn with two legs
##sim.tail(.3, -1000, 0)
##sim.registerPeriodical(sim.fourStrength, bent5, f) #back limb (2)
##sim.registerPeriodical(sim.fourStrength, t, f) #limb on top (4)
##sim.registerPeriodical(sim.fourDirection, rest, f) #limb on top (4)
##sim.registerPeriodica(sim.threeDirection, t, f)



# #MOVING

#this is what I have that currently "works", for balance purposes it's probably best that it move in the direction opposite of the remaining lower limb at rest
#two limbs (top limb (4) and limb X a ays at rest), moving in the direction of the lower limb at rest
##f=1
##sim.head(0.3, -700, 0)  #right limb (1)
##sim.middle(0.3, -700, 0) #back limb (2)
##sim.tail(0, 0, 0) #limb lower right (3)
##sim.rearRight(.2, 700, 0) # top limb (4)


#VERSION 2
#movement in the negative x direction ----> !!!!
##f = .7
##sim.head(0.3, -900, 0)  #left limb (1)
##sim.middle(0.3, -900, 0) #back limb (2)
##sim.tail(.1, -300, 0) #limb lower right (3)  
##sim.rearRight(.3, 50, 0) # top limb (4)

##sim.registerPeriodical(sim.oneDirection, bent3, f) #left limb (1)
##sim.registerPeriodical(sim.oneStrength, bent5, f) #left limb (1)
##
##sim.registerPeriodical(sim.twoDirection, bent3, f) #back limb (2)
##sim.registerPeriodical(sim.twoStrength, bent5, f) #back limb (2)



#VERSION 3 
#dragging 2 limbs behind, moving in limb3 direction ---> !!!!
##f=.7
##sim.tail(0,-1000,0)
##sim.rearRight(0,500,0)
##sim.registerPeriodical(sim.threeStrength, t, f) #limb lower right (3)
##sim.registerPeriodical(sim.fourStrength, bent2,f)

#VERSION 4
#aquatic movement ---> !!
# f=.8
# sim.tail(0, 1000, 0)

# sim.registerPeriodical(sim.oneStrength, bent5, f) 
# sim.registerPeriodical(sim.oneDirection, walkfunc, f) 
# sim.registerPeriodical(sim.twoStrength, bent5, f) 
# sim.registerPeriodical(sim.twoDirection, walkfunc, f)
# sim.registerPeriodical(sim.threeStrength, t, f)

#VERSION 5
#moving in direction of resting remaining limb, 3 ---> !!
##f=.8
##sim.registerPeriodical(sim.oneStrength, bent5, f) 
##sim.registerPeriodical(sim.oneDirection, walkfunc2, f) 
##sim.registerPeriodical(sim.twoStrength, bent5, f) 
##sim.registerPeriodical(sim.twoDirection, walkfunc2, f)
##sim.registerPeriodical(sim.threeStrength, rest, f)
##sim.registerPeriodical(sim.threeDirection, bent3, f) 
##sim.registerPeriodical(sim.threeStrength, bent4, f) 

#phi as strength
#sim.rearRight(0.2,0, 0)
#sim.registerPeriodical(sim.fourStrength, t, f) 

#theta as direction
# sim.rearRight(0,1000, 0)
# sim.registerPeriodical(sim.fourDirection, t, f) 
# sim.registerPeriodical(sim.fourStrength, t, f) 




#getting the theta values 
fullPosTheta = []
print("fullPosition theta:")
for i in range(len(fullPosition)):
	theta = fullPosition[0][0]
	fullPosTheta.append(theta)
print(fullPosTheta)


while sim.is_alive():
	time.sleep(.1) #speed of simulation
	# position = sim.getPosition()
	# print(position)

input()
