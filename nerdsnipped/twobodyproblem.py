import math
import pylab
import random

G = 6.674*10**(-11)
#if fundamental constants of the universe can't be global variables, what can?
#units are N*(m/kg)**2

class position(object):
	"""this is a position. it has an x coordinate and a y coordinate, both floats.
	you can also get its distance to a different position
	"""
	def __init__(self, xlocation, ylocation):
		self.xlocation=xlocation
		self.ylocation=ylocation

	def getX(self):
		return self.xlocation

	def getY(self):
		return self.ylocation

	def getdist(self, otherposition):
		"""returns euclidean distance to the other position"""
		xdist = self.xlocation - otherposition.getX()
		ydist = self.ylocation - otherposition.getY()
		return math.sqrt(xdist**2+ydist**2)

class force(object):
	"""this object is a force. it has an xcomponent and a ycomponent, each of which is a float >=0"""
	def __init__(self, xcomp, ycomp):
		self.xcomp = xcomp
		self.ycomp = ycomp

	def getXcomp(self):
		return self.xcomp

	def getYcomp(self):
		return self.ycomp

class planet(object):
	""" this is a planet in two dimensional space. it has:

	mass: a float > 0
	position: a position object
	xspeed: a float
	yspeed: a float
	"""
	def __init__(self, mass, position, xspeed=0, yspeed=0):
		self.mass = mass
		self.position = position
		self.xspeed = xspeed
		self.yspeed = yspeed

	def getmass(self):
		return self.mass

	def getposition(self):
		return self.position

	def setposition(self, newposition):
		"""allows you to set the position of the planet to the newposition
		handy if you want to do a number of simulations all starting from the same position
		"""
		self.position = newposition

	def getforce(self, otherplanet):
		"""returns the force that the other planet is putting on self"""
		mass1 = self.mass
		mass2 = otherplanet.getmass()
		firstposition = self.getposition()
		otherposition = otherplanet.getposition()
		distance = firstposition.getdist(otherposition)
		magnitude = G*mass1*mass2/distance**2
		xdir = otherposition.getX() - firstposition.getX()
		ydir = otherposition.getY() - firstposition.getY()
		xforce = float(xdir*magnitude)/float(distance)
		yforce = float(ydir*magnitude)/float(distance)
		theforce = force(xforce,yforce)
		return theforce

	def forwardtime(self, netforce, timestep=60):
		"""updates position and speed for timestep based on the net force acting on the planet.
		units of timestep are in SECONDS.

		note that increasing timestep will decrease the accuracy of the model
		"""
		netx = netforce.getXcomp()
		nety = netforce.getYcomp()
		accx = float(netx)/float(self.mass)
		accy = float(nety)/float(self.mass)
		newx = self.position.getX() + self.xspeed*timestep + 0.5*accx*timestep**2
		newy = self.position.getY() + self.yspeed*timestep + 0.5*accy*timestep**2
		self.position = position(newx, newy)
		self.xspeed +=accx*timestep
		self.yspeed +=accy*timestep

def atrial(listofplanets, doitfaster=1):
	"""put in a list of planets. calculates the forces between them and 
	then outputs where they are after doitfaster minutes if that force is constant during that time.
	"""
	alltheforces = []
	for i in range(len(listofplanets)):
		xfor = 0
		yfor = 0
		for moon in listofplanets:
			if moon != listofplanets[i]:
				newforce = listofplanets[i].getforce(moon)
				xfor += newforce.getXcomp()
				yfor += newforce.getYcomp()
		alltheforces.append(force(xfor,yfor))
	for i in range(len(listofplanets)):
		listofplanets[i].forwardtime(alltheforces[i], doitfaster*60)
	return listofplanets

def simulation(listofplanets, timesteps, doitfaster=1):
	"""runs a simulation of the list of planets and their movement. doitfaster will change how long
	a timestep is (in minutes), i.e. how often the forces are recalculated (by default a minute).
	note this makes calculations easier at the cost of accuracy.

	outputs: a list of lists for each planet
	each planet's list has a list of xvalues and yvalues over time
	"""
	numberofplanets = len(listofplanets)
	allthetime = [[[planet.getposition().getX()],[planet.getposition().getY()]] for planet in listofplanets]
	for i in range(timesteps):
		atsometime = atrial(listofplanets, doitfaster)
		for i in range(numberofplanets):
			allthetime[i][0].append(listofplanets[i].getposition().getX())
			allthetime[i][1].append(listofplanets[i].getposition().getY())
	return allthetime

def graphData(mylist, colors = None):
	"""mylist contains a list for each planet. that list contains a list of x values and y values
	this function takes that list and graphs each of the planets on the same graph

	You can choose what color the planets are or not. If you leave the default, they are random
	"""
	pylab.close()

	howmanyplanets = len(mylist)
	if colors == None:
		colors = []
		for i in range(howmanyplanets):
			newcolor = "#%06x" % random.randint(0, 0xFFFFFF)
			colors.append(newcolor)

	for i in range(howmanyplanets):
		pylab.scatter(mylist[i][0],mylist[i][1], marker='.', color =colors[i])
	pylab.show()