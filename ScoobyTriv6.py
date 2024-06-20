
#libraries
import math
from matplotlib import pyplot as plt
import re
import os

#varibles
pi = 3.14
r270 = 4.71
r180 = 3.14
r90 = 1.57

signFlag = 0

units = 'ft'
Fdis = 10

planeAxis = [-40, 40, -40, 40]

#in the real code we would instead use the right functions to read the serial port


##########################################################################
# Open the text file
def getAngleSCB1(filename):
  with open(filename, 'r') as file:
    for line in file:
      if 'Total angle:' in line:
        match = re.search(r'\d+', line)
        if match:
          angle1 = int(match.group())
          return angle1


def getAngleSCB2(filename):
  with open(filename, 'r') as file:
    for line in file:
      if 'Total angle:' in line:
        match = re.search(r'\d+', line)
        if match:
          angle2 = int(match.group())
          return angle2


#calculations
def calculateXandYcase1(phi, theta, Fdis, units):
  print("Case 1 Calcuation:")
  print()

  x = math.tan(theta) * Fdis / (math.tan(theta) - math.tan(phi))
  y = math.tan(theta) * (x - Fdis)

  x = round(x, 2)
  y = round(y, 2)

  coordinateChecker(phi, x, y)
  if signFlag == 0:

    print("The gunshot coordinates are at: (", x, units, ",", y, units, ")")  
    xScbys = [0, x, Fdis]
    yScbys = [0, y, 0]

    fig,ax=plt.subplots()

    ax.plot(xScbys, yScbys)
    
    label=[x,y]
    x1 = [0, Fdis]
    y1 = [0, 0]
    
    
    plt.plot(x1, y1, 'r*')

    ax.text(xScbys[1],yScbys[1],label)
    
    plt.grid()

   
    plt.axis(planeAxis)
    
    plt.title('Where is the gunshot?')
    plt.xlabel(units)
    plt.ylabel(units)

    
    plt.show()



def calculateXandYcase2(phi, theta, Fdis, units):
  print("Case 2 Calculation:")
  print()

  x = math.tan(theta) * Fdis / (math.tan(theta) - math.tan(phi))
  y = math.tan(phi) * x

  x = round(x, 2)
  y = round(y, 2)

  coordinateChecker(phi, x, y)
  if signFlag == 0:

    print("The gunshot coordinates are at: (", x, units, ",", y, units, ")")

    
    xScbys = [0, x, Fdis]
    yScbys = [0, y, 0]


    fig,ax=plt.subplots()

    ax.plot(xScbys, yScbys)
    
    label=[x,y]
    x1 = [0, Fdis]
    y1 = [0, 0]
    
    
    plt.plot(x1, y1, 'r*')

    ax.text(xScbys[1],yScbys[1],label)
    
    plt.grid()

   
    plt.axis(planeAxis)
    
    plt.title('Where is the gunshot?')
    plt.xlabel(units)
    plt.ylabel(units)

    
    plt.show()


#########################################################################
#Now we check for errors
def coordinateChecker(phi, x, y):
  #We have this to make sure the coords make sense, IE in the
  #correct quadrant of the coordinate plane
  global signFlag

  if phi > r270:
    if x < 0 and y > 0:
      print("The lines did not intersect at the right point! CALCUATION ERROR")
      signFlag += 1
      
  elif phi > r180:
    if x > 0 and y > 0:
      print("The lines did not intersect at the right point! CALCUATION ERROR")
      signFlag += 1
      
  elif phi > r90:
    if x > 0 and y < 0:
      print("The lines did not intersect at the right point! CALCUATION ERROR")
      signFlag += 1

  elif phi > 0:
    if x < 0 and y < 0:
      print("The lines did not intersect at the right point! CALCUATION ERROR")
      signFlag += 1
      


def errorDetector(phi, theta):
  #These are the two cases where the calculation could fail
  if math.tan(phi) == 0 and math.tan(theta) == 0:
    print("The sound is along the X axis")
    return True
  elif math.tan(phi) == math.tan(theta):
    print("The two lines are parrallel, very far away from the two units!")
    return True


#########################################################################
#now scooby does its reads the ports"
phi = getAngleSCB1("SCBY1serialport.TXT")
theta = getAngleSCB2("SCBY2serialport.txt")

#this is to imitate reading the serial port
#print(theta,phi)
print("The angle of the first unit is: ", phi, "degrees")
print("The angle of the second unit is: ", theta, "degrees")
print()
print("Phi =", phi)
print('Theta =', theta)
print()
print("The units are", Fdis, units, "apart")
print()
phi = phi * pi / 180  #we have to convert it to radians first
theta = theta * pi / 180  

#
if errorDetector(phi, theta) == True:
  print("Error, please try again")
elif abs(math.tan(theta)) < abs(math.tan(phi)):
  calculateXandYcase1(phi, theta, Fdis, units)
elif abs(math.tan(theta)) > abs(math.tan(phi)):
  calculateXandYcase2(phi, theta, Fdis, units)