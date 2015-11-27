from twobodyproblem import *

#first, just simulating the earth around the sun
thecenter = position(0,0)
sun = planet(1.989*10**30, thecenter)
earthstarts = position(149.6*10**9,0)
earth = planet(5.972*10**24, earthstarts, 0, 29.8*1000)

def resetSunEarth():
	sun.setposition(thecenter)
	earth.setposition(earthstarts)

def GraphSunEarth(numtrials=60*24*100, doitfaster=1):
	"""plots the sun and earth rotating around each other
	"""
	mylist = simulation([sun,earth],numtrials, doitfaster)
	graphData(mylist, ['orange', 'blue'])#sun is orange cause yellow is hard to see

#adding in mars
marslocation = position(0,227.9*10**9)
mars = planet(6.39*10**23, marslocation, -24130.83,0)

def AMarsSimulation(numtrials=365*24, doitfaster=60):
	"""graphs the sun,earth, and mars orbits"""
	marsplot = simulation([sun,earth,mars],numtrials,doitfaster)
	colors = ['orange', 'blue', 'red']
	graphData(marsplot,colors)

#what if we look at sun,earth,moon?
moonlocation = position(149.6*10**9 + 384.4*10**6, 0) 
moon = planet(7.3476*10**22, moonlocation, 0, 29.8*1000+1023)

#i didn't use the prebuilt code of graphData because I also wanted to zoom in to see the moon
#we make two plots: one of everything, one close up of the moon-earth (with same simulation)
def AMoonSimulation(numtrials=365*24,doitfaster=60):
	resetSunEarth()
	moonplot = simulation([sun,earth,moon],numtrials,doitfaster)
	f, (ax1, ax2) = pylab.subplots(1,2)
	colors = ['orange', 'blue', 'gray']
	markers = ['o','.','.']
	for i in range(3):
		ax1.scatter(moonplot[i][0], moonplot[i][1], marker = markers[i], color=colors[i])
	ax1.set_xlim([-5*10**9,200*10**9])
	ax1.set_ylim([-10**10,1.5*10**11])
	ax1.set_title('80-day path of Earth-Moon around the Sun',y=1.05)
	for i in [1,2]:
		ax2.scatter(moonplot[i][0], moonplot[i][1], marker = '.', color=colors[i])
	myxmin = 149.6*10**9 - 25*384.4*10**6
	myxmax = 149.6*10**9 + 2*384.4*10**6
	ax2.set_xlim([myxmin, myxmax])
	ax2.set_ylim([0,5*10**10])
	ax2.set_title('Close up of the Earth and Moon', y=1.05)
	pylab.tight_layout()
	pylab.show()

#if we look at a planet going too slowly around the sun, it swings around and gathers momentum, like a comet
def Comet(numtrials=24*365*5,doitfaster=60):
	"""simulates and graphs the sun and a body that has the wrong velocity for a stable orbit"""
	comet = planet(5.972*10**24, earthstarts, 0, 15000)
	mylist = simulation([sun,comet],numtrials, doitfaster)
	graphData(mylist)

def TwoSuns(numtrials=24*800, doitfaster=60):
	""" two bodies with large mass orbiting each other"""
	sunone = planet(10**30, thecenter, 0, 10000)
	double = position(300*10**9,0)
	suntwo = planet(10**(30),double,0,-10000)
	mylist = simulation([sunone,suntwo],numtrials,doitfaster)
	colors = ['yellow', 'red']
	graphData(mylist, colors)

def CrazySuns(numtrials=60*24*20, doitfaster=60):
	""" same two bodies as TwoSuns but one starts out with no velocity, so instead they spiral!"""
	sunone = planet(10**30, thecenter, 0, 0)
	double = position(300*10**9,0)
	suntwo = planet(10**(30),double,0,-10000)
	mylist = simulation([sunone,suntwo],numtrials,doitfaster)
	colors = ['yellow', 'red']
	graphData(mylist, colors)	
