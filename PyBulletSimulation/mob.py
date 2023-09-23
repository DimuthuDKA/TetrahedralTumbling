import pybullet as p
import time
import pybullet_data #this apparently contains the plane and r2d2
import math
import threading
import sys
import time


class Periodical():
	def __init__(self, segfunc, shape, hz):
		self.segmentFunction = segfunc
		self.shapeFunction = shape
		self.hz = hz
		self.rate = 1/hz
		self.iterations = 0
		self.tick = 0
		self.returntype = shape(0, 0) #determine the return type of the shape function so we can use cooler segment functions
	

class Simulation(threading.Thread):
	def __init__(self, sim, maxForce = 100, gui=False):
		threading.Thread.__init__(self)
		self.s_str = 0
		self.s_dir = 0
		self.s_exp = 0

		self.fr_str = 0
		self.fr_dir = 0
		self.fr_exp = 0

		self.fl_str = 0
		self.fl_dir = 0
		self.fl_exp = 0

		self.rr_str = 0
		self.rr_dir = 0
		self.rr_exp = 0

		self.rl_str = 0
		self.rl_dir = 0
		self.rl_exp = 0
		
		self.periodicals = []
		
		self.ur = None
		self.valid = False
		
		self.followcam = False
		self.zoom = 4
		self.gui = gui
		self.simtype = sim
		
		self.maxForce = maxForce
		
		
	#walker	
	def spineStrength(self, str):
		self.s_str = str
	def spineDirection(self, dir):
		self.s_dir = dir
	def spineExpansion(self, exp):
		self.s_exp = exp

	def spine(self, str, dir, exp):
		self.s_str = str
		self.s_dir = dir
		self.s_exp = exp
		
	def frontRightStrength(self, str):
		self.fr_str = str
	def frontRightDirection(self, dir):
		self.fr_dir = -dir + math.pi
	def frontRightExpansion(self, exp):
		self.fr_exp = exp

	def frontRight(self, str, dir, exp):
		self.fr_str = str
		self.fr_dir = -dir + math.pi
		self.fr_exp = exp
		
	def frontLeftStrength(self, str):
		self.fl_str = str
	def frontLeftDirection(self, dir):
		self.fl_dir = dir
	def frontLeftExpansion(self, exp):
		self.fl_exp = exp

	def frontLeft(self, str, dir, exp):
		self.fl_str = str
		self.fl_dir = dir
		self.fl_exp = exp
		
	def rearRightStrength(self, str):
		self.rr_str = str
	def rearRightDirection(self, dir):
		self.rr_dir = -dir + math.pi
	def rearRightExpansion(self, exp):
		self.rr_exp = exp

	def rearRight(self, str, dir, exp):
		self.rr_str = str
		self.rr_dir = -dir + math.pi
		self.rr_exp = exp
		
	def rearLeftStrength(self, str):
		self.rl_str = str
	def rearLeftDirection(self, dir):
		self.rl_dir = dir
	def rearLeftExpansion(self, exp):
		self.rl_exp = exp

	def rearLeft(self, str, dir, exp):
		self.rl_str = str
		self.rl_dir = dir
		self.rl_exp = exp
		
		
		
	#snake
	def headStrength(self, str):
		self.s_str = str
	def headDirection(self, dir):
		self.s_dir = dir
	def headExpansion(self, exp):
		self.s_exp = exp

	def head(self, str, dir, exp):
		self.s_str = str
		self.s_dir = dir
		self.s_exp = exp
		
	def middleStrength(self, str):
		self.fr_str = str
	def middleDirection(self, dir):
		self.fr_dir = dir
	def middleExpansion(self, exp):
		self.fr_exp = exp

	def middle(self, str, dir, exp):
		self.fr_str = str
		self.fr_dir = dir
		self.fr_exp = exp
		
	def tailStrength(self, str):
		self.fl_str = str
	def tailDirection(self, dir):
		self.fl_dir = dir
	def tailExpansion(self, exp):
		self.fl_exp = exp

	def tail(self, str, dir, exp):
		self.fl_str = str
		self.fl_dir = dir
		self.fl_exp = exp
		
	def snake2Wrapper(self, str1, dir1, str2, dir2, str3, dir3):
		self.head(str1, dir1, 0)
		self.middle(str2, dir2, 0)
		self.tail(str3, dir3, 0)
		
	#tetra
	def oneStrength(self, str):
		self.s_str = str
	def oneDirection(self, dir):
		self.s_dir = dir
	def oneExpansion(self, exp):
		self.s_exp = exp

	def one(self, str, dir, exp):
		self.s_str = str
		self.s_dir = dir
		self.s_exp = exp
		
	def twoStrength(self, str):
		self.fr_str = str
	def twoDirection(self, dir):
		self.fr_dir = -dir + math.pi
	def twoExpansion(self, exp):
		self.fr_exp = exp

	def two(self, str, dir, exp):
		self.fr_str = str
		self.fr_dir = -dir + math.pi
		self.fr_exp = exp
		
	def threeStrength(self, str):
		self.fl_str = str
	def threeDirection(self, dir):
		self.fl_dir = dir
	def threeExpansion(self, exp):
		self.fl_exp = exp

	def three(self, str, dir, exp):
		self.fl_str = str
		self.fl_dir = dir
		self.fl_exp = exp
		
	def fourStrength(self, str):
		self.rr_str = str
	def fourDirection(self, dir):
		self.rr_dir = -dir + math.pi
	def fourExpansion(self, exp):
		self.rr_exp = exp

	def four(self, str, dir, exp):
		self.rr_str = str
		self.rr_dir = -dir + math.pi
		self.rr_exp = exp
		
	
		
		
	def tetraWrapper(self, str1, dir1, str2, dir2, str3, dir3, str4, dir4):
		self.head(str1, dir1, 0)
		self.middle(str2, dir2, 0)
		self.tail(str3, dir3, 0)
		self.rearRight(str4, dir4, 0)
	
	def setFollowCamera(self, newval, zoom=4):
		self.followcam = newval
		self.zoom = zoom
	
	def getPosition(self):
		if self.valid:
			return p.getLinkState(self.ur, 0)[0]
		else:
			return [0, 0, 0]
	def getFullPosition(self):
		if self.valid:
			xy1 = p.getLinkState(self.ur, 0)[0]
			xy2 = p.getLinkState(self.ur, 15)[0]
			xy3 = p.getLinkState(self.ur, 31)[0]
			xy4 = p.getLinkState(self.ur, 47)[0]
			
			return ((xy1[0], xy1[1]), (xy2[0], xy2[1]), (xy3[0], xy3[1]), (xy4[0], xy4[1]))
		else:
			return ((0, 0), (0, 0), (0, 0), (0, 0))
		
	def getOrientation(self):
		if self.valid:
			return p.getEulerFromQuaternion(p.getLinkState(self.ur, 0)[1])
		else:
			return [0, 0, 0]
			
	def registerPeriodical(self, segmentFunction, shape, hz):
		self.periodicals.append(Periodical(segmentFunction, shape, hz))
	def endSimulation(self):
		print("Ending Simulation...")
		p.disconnect()
	def run(self):
		print ("Starting Simulation...")
		
		#physicsClient = p.connect(p.GUI)#or p.DIRECT for non-graphical version
		cid = 0
		
		if self.gui:
			cid = p.connect(p.GUI)
		else:
			cid = p.connect(p.DIRECT)
		#if (cid<0):
			#p.connect(p.GUI)
		p.resetDebugVisualizerCamera(cameraDistance = self.zoom, cameraYaw = 60, cameraPitch = -45, cameraTargetPosition = (0,0,1))
		p.setAdditionalSearchPath(pybullet_data.getDataPath()) #optionally
		p.setGravity(0,0,-20)
		planeId = p.loadURDF("plane.urdf")
		
		
		p.changeDynamics(planeId, -1, lateralFriction = 1)
		#make the floor larger
		#make the camera follow
		#https://www.oreilly.com/library/view/hands-on-reinforcement-learning/9781788836524/941db051-2104-4499-a48d-45c680a6c0e1.xhtml
		if self.simtype == "walker":
			spineStartPos = [0,0,0.8]
			spineStartOrientation = p.getQuaternionFromEuler([math.pi / 2,0,0])

			self.ur = p.loadURDF("./walker_tim.urdf",spineStartPos, spineStartOrientation, flags=p.URDF_USE_SELF_COLLISION)
		elif self.simtype == "snake":
			spineStartPos = [0,0,0.15]
			spineStartOrientation = p.getQuaternionFromEuler([math.pi / 2,0,0])

			self.ur = p.loadURDF("./snake2.urdf",spineStartPos, spineStartOrientation, flags=p.URDF_USE_SELF_COLLISION)
		elif self.simtype == "snake2":
			spineStartPos = [0,0,0.15]
			spineStartOrientation = p.getQuaternionFromEuler([math.pi / 2,0,0])
			self.ur = p.loadURDF("./snake3.urdf",spineStartPos, spineStartOrientation, flags=p.URDF_USE_SELF_COLLISION)
		elif self.simtype == "tetra":
			spineStartPos = [0,0,1]
			spineStartOrientation = p.getQuaternionFromEuler([math.pi,0,0])
			self.ur = p.loadURDF("./tetra.urdf",spineStartPos, spineStartOrientation, flags=p.URDF_USE_SELF_COLLISION)
		self.valid = True
		#wall = p.loadURDF("C:/python/wall.urdf",[0, 2, .75], spineStartOrientation)
		#box = p.loadURDF("C:/python/box.urdf",[0, 2, 1.75], spineStartOrientation)
		#box2 = p.loadURDF("C:/python/box.urdf",[1, 2, 1.75], spineStartOrientation)
		#box3 = p.loadURDF("C:/python/box.urdf",[-1, 2, 1.75], spineStartOrientation)

		i = 1
		'''t0 = p.addUserDebugParameter("Section 1 direction", -3.14159265, 3.14159265, 0)
		t1 = p.addUserDebugParameter("Section 1 strength", 0, .3, 0)
		t4 = p.addUserDebugParameter("Section 1 extension", 0, .05, 0)

		t2 = p.addUserDebugParameter("Section 2 direction", -3.14159265, 3.14159265, 0)
		t3 = p.addUserDebugParameter("Section 2 strength", 0, .3, 0)
		t5 = p.addUserDebugParameter("Section 2 extension", 0, .05, 0)'''
		rel1 = 0
		rel2 = 0
		tau = 6.28318531
		prev1 = 0
		prev2 = 0
		lock = True

		def jType(enum):
			if enum == p.JOINT_REVOLUTE:
				return "revolute"
			if enum == p.JOINT_PRISMATIC:
				return "prismatic"
			if enum == p.JOINT_FIXED:
				return "fixed"

		#for i in range(p.getNumJoints(bodyUniqueId=self.ur)):
		#	print(i, jType(p.getJointInfo(self.ur, i)[2]))

		while True:
			#start_ts = time.time()
			p.stepSimulation()
			#print("Step time:", time.time()-start_ts)
			if self.gui:
				time.sleep(1./240.)
			#if i % 240 == 0:
				#print("Second")
			i = i + 1
			if self.followcam and self.valid :
				p.resetDebugVisualizerCamera(cameraDistance = self.zoom, cameraYaw = 60, cameraPitch = -45, cameraTargetPosition = p.getLinkState(self.ur, 0)[0])
			keys = p.getKeyboardEvents()
			maxForce = self.maxForce
			#if (p.B3G_RETURN in keys and keys[p.B3G_RETURN]&p.KEY_WAS_TRIGGERED) or lock:
				#twist the arm
				#lock = False #this step engages all motors to put discs on starting points. disallows initial movement and free movement.
			
			for pe in self.periodicals:
				pe.tick = pe.tick + 1
				if pe.tick / 240 >= pe.rate:
					pe.tick = 0
					pe.iterations = pe.iterations + 1
				if isinstance(pe.returntype, (tuple, list)):
					pe.segmentFunction(*pe.shapeFunction(pe.tick / 240 * pe.hz, pe.iterations))
					#print(pe.tick / 240 * pe.hz, *pe.shapeFunction(pe.tick / 240 * pe.hz, pe.iterations))
				else:
					pe.segmentFunction(pe.shapeFunction(pe.tick / 240 * pe.hz, pe.iterations))
			
			if self.s_str < -math.pi / 8:
				self.s_str = -math.pi / 8
			if self.s_str > math.pi / 8:
				self.s_str = math.pi / 8
			
			if self.fr_str < -math.pi / 8:
				self.fr_str = -math.pi / 8
			if self.fr_str > math.pi / 8:
				self.fr_str = math.pi / 8
			
			if self.fl_str < -math.pi / 8:
				self.fl_str = -math.pi / 8
			if self.fl_str > math.pi / 8:
				self.fl_str = math.pi / 8
				
			if self.rr_str < -math.pi / 8:
				self.rr_str = -math.pi / 8
			if self.rr_str > math.pi / 8:
				self.rr_str = math.pi / 8
				
			if self.rl_str < -math.pi / 8:
				self.rl_str = -math.pi / 8
			if self.rl_str > math.pi / 8:
				self.rl_str = math.pi / 8
				
				
			if self.s_exp < 0:
				self.s_exp = 0
			if self.s_exp > 0.05:
				self.s_exp = 0.05
			
			if self.fr_exp < 0:
				self.fr_exp = 0
			if self.fr_exp > 0.05:
				self.fr_exp = 0.05
			
			if self.fl_exp < 0:
				self.fl_exp = 0
			if self.fl_exp > 0.05:
				self.fl_exp = 0.05
				
			if self.rr_exp < 0:
				self.rr_exp = 0
			if self.rr_exp > 0.05:
				self.rr_exp = 0.05
				
			if self.rl_exp < 0:
				self.rl_exp = 0
			if self.rl_exp > 0.05:
				self.rl_exp = 0.05
			#left and right are relative to the "head" when the legs are pointing down
			#0			fixed
			#1-24		spine
			#25-27		fixed
			#28-51		right hindleg
			#52			fixed
			#53-76		left hindleg
			#77			fixed
			#78-101		right foreleg
			#102		fixed
			#103-126	left foreleg
			#THE ABSOLUTE LIMIT FOR A URDF IS 127 JOINTS, 128 LINKS
			if self.simtype == "walker":
				for k in range(1,25): #spine
					j = math.floor((k - 1) / 3)
					p.setJointMotorControl2(bodyUniqueId=self.ur, jointIndex=j * 3 + 1, controlMode=p.POSITION_CONTROL, targetPosition = math.cos(self.s_dir) * -self.s_str, force = maxForce)
					p.setJointMotorControl2(bodyUniqueId=self.ur, jointIndex=j * 3 + 1 + 1, controlMode=p.POSITION_CONTROL, targetPosition = math.sin(self.s_dir) * -self.s_str, force = maxForce)
					p.setJointMotorControl2(bodyUniqueId=self.ur, jointIndex=j * 3 + 2 + 1, controlMode=p.POSITION_CONTROL, targetPosition = -self.s_exp, force = maxForce)
				for k in range(28,52): #right hindleg
					j = math.floor((k - 28) / 3)
					p.setJointMotorControl2(bodyUniqueId=self.ur, jointIndex=j * 3 + 28, controlMode=p.POSITION_CONTROL, targetPosition = math.cos(self.rr_dir) * -self.rr_str, force = maxForce)
					p.setJointMotorControl2(bodyUniqueId=self.ur, jointIndex=j * 3 + 1 + 28, controlMode=p.POSITION_CONTROL, targetPosition = math.sin(self.rr_dir) * -self.rr_str, force = maxForce)
					p.setJointMotorControl2(bodyUniqueId=self.ur, jointIndex=j * 3 + 2 + 28, controlMode=p.POSITION_CONTROL, targetPosition = -self.rr_exp, force = maxForce)
				for k in range(53,77): #left hindleg
					j = math.floor((k - 53) / 3)
					p.setJointMotorControl2(bodyUniqueId=self.ur, jointIndex=j * 3 + 53, controlMode=p.POSITION_CONTROL, targetPosition = math.cos(self.rl_dir) * -self.rl_str, force = maxForce)
					p.setJointMotorControl2(bodyUniqueId=self.ur, jointIndex=j * 3 + 1 + 53, controlMode=p.POSITION_CONTROL, targetPosition = math.sin(self.rl_dir) * -self.rl_str, force = maxForce)
					p.setJointMotorControl2(bodyUniqueId=self.ur, jointIndex=j * 3 + 2 + 53, controlMode=p.POSITION_CONTROL, targetPosition = -self.rl_exp, force = maxForce)
				for k in range(78,102): #right foreleg
					j = math.floor((k - 78) / 3)
					p.setJointMotorControl2(bodyUniqueId=self.ur, jointIndex=j * 3 + 78, controlMode=p.POSITION_CONTROL, targetPosition = math.cos(self.fr_dir) * -self.fr_str, force = maxForce)
					p.setJointMotorControl2(bodyUniqueId=self.ur, jointIndex=j * 3 + 1 + 78, controlMode=p.POSITION_CONTROL, targetPosition = math.sin(self.fr_dir) * -self.fr_str, force = maxForce)
					p.setJointMotorControl2(bodyUniqueId=self.ur, jointIndex=j * 3 + 2 + 78, controlMode=p.POSITION_CONTROL, targetPosition = -self.fr_exp, force = maxForce)
				for k in range(103,127): #left foreleg
					j = math.floor((k - 103) / 3)
					p.setJointMotorControl2(bodyUniqueId=self.ur, jointIndex=j * 3 + 103, controlMode=p.POSITION_CONTROL, targetPosition = math.cos(self.fl_dir) * -self.fl_str, force = maxForce)
					p.setJointMotorControl2(bodyUniqueId=self.ur, jointIndex=j * 3 + 1 + 103, controlMode=p.POSITION_CONTROL, targetPosition = math.sin(self.fl_dir) * -self.fl_str, force = maxForce)
					p.setJointMotorControl2(bodyUniqueId=self.ur, jointIndex=j * 3 + 2 + 103, controlMode=p.POSITION_CONTROL, targetPosition = -self.fr_exp, force = maxForce)
			
			elif self.simtype == "snake":
				for k in range(0,8): #spine
					j = math.floor((k - 0))
					p.setJointMotorControl2(bodyUniqueId=self.ur, jointIndex=j + 0, controlMode=p.POSITION_CONTROL, targetPosition = self.s_str, force = maxForce)
				for k in range(8,16): #right hindleg
					j = math.floor((k - 8))
					p.setJointMotorControl2(bodyUniqueId=self.ur, jointIndex=j + 8, controlMode=p.POSITION_CONTROL, targetPosition = self.fr_str, force = maxForce)
				for k in range(16,24): #left hindleg
					j = math.floor((k - 16))
					p.setJointMotorControl2(bodyUniqueId=self.ur, jointIndex=j + 16, controlMode=p.POSITION_CONTROL, targetPosition = self.fl_str, force = maxForce)
			
			elif self.simtype == "snake2":
				for k in range(0,16): #spine
					j = math.floor((k - 0) / 2)
					p.setJointMotorControl2(bodyUniqueId=self.ur, jointIndex=j * 2 + 0, controlMode=p.POSITION_CONTROL, targetPosition = math.cos(self.s_dir) * -self.s_str, force = maxForce)
					p.setJointMotorControl2(bodyUniqueId=self.ur, jointIndex=j * 2 + 0 + 1, controlMode=p.POSITION_CONTROL, targetPosition = math.sin(self.s_dir) * -self.s_str, force = maxForce)
				for k in range(16,32): #right hindleg
					j = math.floor((k - 16) / 2)
					p.setJointMotorControl2(bodyUniqueId=self.ur, jointIndex=j * 2 + 16, controlMode=p.POSITION_CONTROL, targetPosition = math.cos(self.fr_dir) * -self.fr_str, force = maxForce)
					p.setJointMotorControl2(bodyUniqueId=self.ur, jointIndex=j * 2 + 16 + 1, controlMode=p.POSITION_CONTROL, targetPosition = math.sin(self.fr_dir) * -self.fr_str, force = maxForce)
				for k in range(32,48): #left hindleg
					j = math.floor((k - 32) / 2)
					p.setJointMotorControl2(bodyUniqueId=self.ur, jointIndex=j * 2 + 32, controlMode=p.POSITION_CONTROL, targetPosition = math.cos(self.fl_dir) * -self.fl_str, force = maxForce)
					p.setJointMotorControl2(bodyUniqueId=self.ur, jointIndex=j * 2 + 32 + 1, controlMode=p.POSITION_CONTROL, targetPosition = math.sin(self.fl_dir) * -self.fl_str, force = maxForce)
			elif self.simtype == "tetra":
				for k in range(1,17): #spine
					j = math.floor((k - 1) / 2)
					p.setJointMotorControl2(bodyUniqueId=self.ur, jointIndex=j * 2 + 1, controlMode=p.POSITION_CONTROL, targetPosition = math.cos(self.s_dir) * -self.s_str, force = maxForce)
					p.setJointMotorControl2(bodyUniqueId=self.ur, jointIndex=j * 2 + 1 + 1, controlMode=p.POSITION_CONTROL, targetPosition = math.sin(self.s_dir) * -self.s_str, force = maxForce)
				for k in range(18,34): #right hindleg
					j = math.floor((k - 18) / 2)
					p.setJointMotorControl2(bodyUniqueId=self.ur, jointIndex=j * 2 + 18, controlMode=p.POSITION_CONTROL, targetPosition = math.cos(self.fr_dir) * -self.fr_str, force = maxForce)
					p.setJointMotorControl2(bodyUniqueId=self.ur, jointIndex=j * 2 + 1 + 18, controlMode=p.POSITION_CONTROL, targetPosition = math.sin(self.fr_dir) * -self.fr_str, force = maxForce)
				for k in range(35,51): #left hindleg
					j = math.floor((k - 35) / 2)
					p.setJointMotorControl2(bodyUniqueId=self.ur, jointIndex=j * 2 + 35, controlMode=p.POSITION_CONTROL, targetPosition = math.cos(self.fl_dir) * -self.fl_str, force = maxForce)
					p.setJointMotorControl2(bodyUniqueId=self.ur, jointIndex=j * 2 + 1 + 35, controlMode=p.POSITION_CONTROL, targetPosition = math.sin(self.fl_dir) * -self.fl_str, force = maxForce)
				for k in range(51,67): #right foreleg
					j = math.floor((k -51) / 2)
					p.setJointMotorControl2(bodyUniqueId=self.ur, jointIndex=j * 2 + 51, controlMode=p.POSITION_CONTROL, targetPosition = math.cos(self.rr_dir) * -self.rr_str, force = maxForce)
					p.setJointMotorControl2(bodyUniqueId=self.ur, jointIndex=j * 2 + 1 + 51, controlMode=p.POSITION_CONTROL, targetPosition = math.sin(self.rr_dir) * -self.rr_str, force = maxForce)

		sys.exit()	
'''
elif self.simtype == "snake":
	for k in range(0,24): #spine
		j = math.floor((k - 0) / 3)
		p.setJointMotorControl2(bodyUniqueId=self.ur, jointIndex=j * 3 + 0, controlMode=p.POSITION_CONTROL, targetPosition = math.cos(self.s_dir) * -self.s_str, force = maxForce)
		p.setJointMotorControl2(bodyUniqueId=self.ur, jointIndex=j * 3 + 1 + 0, controlMode=p.POSITION_CONTROL, targetPosition = math.sin(self.s_dir) * -self.s_str, force = maxForce)
		p.setJointMotorControl2(bodyUniqueId=self.ur, jointIndex=j * 3 + 2 + 0, controlMode=p.POSITION_CONTROL, targetPosition = -self.s_exp, force = maxForce)
	for k in range(24,48): #right hindleg
		j = math.floor((k - 24) / 3)
		p.setJointMotorControl2(bodyUniqueId=self.ur, jointIndex=j * 3 + 24, controlMode=p.POSITION_CONTROL, targetPosition = math.cos(self.fr_dir) * -self.fr_str, force = maxForce)
		p.setJointMotorControl2(bodyUniqueId=self.ur, jointIndex=j * 3 + 1 + 24, controlMode=p.POSITION_CONTROL, targetPosition = math.sin(self.fr_dir) * -self.fr_str, force = maxForce)
		p.setJointMotorControl2(bodyUniqueId=self.ur, jointIndex=j * 3 + 2 + 24, controlMode=p.POSITION_CONTROL, targetPosition = -self.fr_exp, force = maxForce)
	for k in range(48,72): #left hindleg
		j = math.floor((k - 48) / 3)
		p.setJointMotorControl2(bodyUniqueId=self.ur, jointIndex=j * 3 + 48, controlMode=p.POSITION_CONTROL, targetPosition = math.cos(self.fl_dir) * -self.fl_str, force = maxForce)
		p.setJointMotorControl2(bodyUniqueId=self.ur, jointIndex=j * 3 + 1 + 48, controlMode=p.POSITION_CONTROL, targetPosition = math.sin(self.fl_dir) * -self.fl_str, force = maxForce)
		p.setJointMotorControl2(bodyUniqueId=self.ur, jointIndex=j * 3 + 2 + 48, controlMode=p.POSITION_CONTROL, targetPosition = -self.fl_exp, force = maxForce)
'''