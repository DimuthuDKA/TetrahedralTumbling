import mob as m
import time
import math

sim = m.Simulation("tetra", 100, True)
sim.start()

#try using pyevolve

#The STRENGTH parameter indicates the degree to which the bend occurs, and is defined on [0, 0.3], which is locked in the program
#The DIRECTION parameter indicates in what direction the limb will bend, and is defined on (-infinity, infinity) much as #the sine and cosine functions are. Directions chosen are irrespective of the simplest form direction in the range (-pi, pi)
#The EXPANSION parameter indicates how far the arm stretches in length, and is defined on [0, 0.05], which is locked in #the program. There are 5 limbs and 4 methods for each, so there are 20 methods.

#QUAD
# sim.frontRight(0.2, 0, 0) ##### strength, direction and expansion
# sim.frontLeft(0.2, 0, 0)
# sim.rearRight(0.2, 0, 0)
# sim.rearLeft(0.2, 0, 0)


# #QUAD
# def walkfunc(t, i):
	# return (i + t) * 2 * math.pi
# def altfunc(t, i):
	# return (i + t) * 2 * math.pi + math.pi

midOffset = 5.14
tailOffset = 5.73

# midOffset = 1.03
# tailOffset = 2.71
#midOffset = #1#5.81#5.77#0.61#4.35
#tailOffset = #4#4.51#1.56#3.97#3.82 # works rather well for turning

def slither(t, i):
	# comment
	return (math.sin(t * 2 * math.pi + 0) * 0.3)

def slither2(t, i):
	return (math.sin(t * 2 * math.pi + midOffset) * 0.3)

def slither3(t, i):
	return (math.sin(t * 2 * math.pi + tailOffset) * 0.3)


	

def recti(t, i):
	return (t + i)

	

#QUAD	
# sim.registerPeriodical(sim.frontRightDirection, walkfunc, 1/6)
# sim.registerPeriodical(sim.rearRightDirection, walkfunc, 1/6)
# sim.registerPeriodical(sim.frontLeftDirection, walkfunc, 1/6)
# sim.registerPeriodical(sim.rearLeftDirection, walkfunc, 1/6)
# time.sleep(5)
#f=0.69;
f = 0.5 #0.84#0.69

# #tetra
# sim.registerPeriodical(sim.oneStrength, slither, f)
# sim.registerPeriodical(sim.twoStrength, slither2, f)
# sim.registerPeriodical(sim.threeStrength, slither2, f)
# sim.registerPeriodical(sim.fourStrength, recti, f)

# #SNAKE
# sim.registerPeriodical(sim.headDirection, recti, f)
# sim.registerPeriodical(sim.middleDirection, recti, f)
# sim.registerPeriodical(sim.tailDirection, recti, f)

def special(t, i):
	return (slither(t, i), recti(t, i), slither2(t, i), recti(t, i), slither3(t, i), recti(t, i))


sim.registerPeriodical(sim.snake2Wrapper, special, f)



while sim.is_alive():
	time.sleep(.1)
	#print(sim.getFullPosition())

	
input()
