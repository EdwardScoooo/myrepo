

## Balloon pop vs common loud sounds for our project SCOOBY
from os import write
import pandas as pd
import csv
import os
from matplotlib import pyplot as plt

##This function looks for when the sound reaches its peak, loops till it 
##Finds a number greater than 2000 or just the greatest number
def startOfPeak(t, wfm):
  for s in wfm:
      if s >= t:
        return s

  return max(wfm)

##This function looks for the end of peak:
def endOfPeak(t, slice):
  for e in slice:              
      if e < t:   
          
          return e

#This function looks for when the sound starts to curve up, leading edge start
def lookForLES(wfm):     
  for les in wfm:
      if les > 150:
        return les

#TESTS
#this test checks if the leading edge (LE) time is correct
def leadingEdgeTimeTest(wfm, pk, time): 
  print()
  leStart = lookForLES(wfm)
  print("Leading Edge Start:",leStart)

  print("Start of Peak:",pk)
  leStartTime = time[wfm.index(leStart)]
  pkTime = time[wfm.index(pk)]
  print("Leading Edge Start Time:",leStartTime,"us")
  print("Peak Time:",pkTime,"us")
  leAvgTime = (leStartTime + pkTime)//2 
  leAvgTimes.append(leAvgTime)
  print("Leading Edge Average Time:",leAvgTime,"us")
  if leAvgTime >= 250 and leAvgTime <= 420: 
      print("Leading Edge Average Time has correct length")
      return True
  elif leAvgTime < 250:
      print("Leading Edge Average Time is too short in length, too quiet")
      return False
  elif leAvgTime > 420:
      print("Leading Edge Average Time is too long in length, too loud")
      return False
  else:
    print("something is not right")
    return False

#This test calculates the duration of the peak:
def testDurationPeak(time, start, end):
  print()
  print("Start of Peak Time",time[start],"us")
  print("End of Peak Time:",time[end],"us")
  durationOfPeak=(time[end]-time[start])
  print("Duration of the Peak:",durationOfPeak,'us')
  peakDurations.append(durationOfPeak)
  if durationOfPeak > 100 and durationOfPeak < 700:
    print("Peak has correct length.")
    return True
  elif durationOfPeak < 100:
    print("Peak is too short, maybe not loud enough. Could be balloon.")
    return False
  elif durationOfPeak > 700:
    print("Peak was too long, maybe too loud. Could be balloon.")
    return False

#This part of code will see if the soundwave goes ZeroCrossing
def testForZeroCrossing(wfm, endIndex):
  print()
  for n in wfm:
    if n < 0:
      negIndex = wfm.index(n)
      if negIndex > endIndex:
        ZeroCrossingWFMs.append(n)
        print("The sound goes crosses zero")
        #print(n)
        return True
  print("Sound does not past zero, either too loud or too quiet")
  ZeroCrossingWFMs.append(n)
  return False

def testForPeak():
  print()
  if startPeak >= threshold:
    print('The peak is',startPeak)
    print("It's loud enough for a balloon!")
    return True
  else:
    print('The peak is only',startPeak)
    print("It is not loud enough for a balloon! Test failed.")
    return False

##################################################################
#this list is used to create like a data log of the soundwaves we have tested
fileNames = [] #use this list to append the name of each file


startPeakValue = [] #use this list to append each peak

endPeakValue = []

leAvgTimes = [] #use this list to append each leading edge average time


peakDurations = [] #use this list to append each duration of the peak


ZeroCrossingWFMs = [] #use this list to append either 0 (for non ZeroCrossing values) or 1 (for ZeroCrossing values)


fileName = input("Enter the name of the csv file you want to use: ")
df = pd.read_csv(fileName)
#print("Printing data frame from Scooby's file:")
#print(df)
fileNames.append(fileName)
time = []
for j,row in df.iterrows():
  time.append(row["Time"])
#print(time)

wfm = []
for i,row in df.iterrows():
  wfm.append(row["WFM"])


threshold = 1800
startPeak = startOfPeak(threshold, wfm)
startIndex = wfm.index(startPeak)

endPeak = endOfPeak(threshold, wfm[startIndex :]) #list slicing starts at startIndex and goes to the end (:) of list
endIndex = wfm.index(endPeak)

startPeakValue.append(startPeak)
endPeakValue.append(endPeak)


print("\nResults:")

balloon = [] 



isPeak = testForPeak()
isTestDurPeak = testDurationPeak(time, startIndex, endIndex)
isZeroCross = testForZeroCrossing(wfm, endIndex)
isLeadingEdgeTT = leadingEdgeTimeTest(wfm, startPeak, time)
if isPeak == True and isTestDurPeak == True and isZeroCross == True and isLeadingEdgeTT == True:
  print()
  print("The soundwave is probably a balloon!")
  print("Test Passed!")
  balloon.append(1)


  plt.plot(time, wfm)  
  

  plt.plot(time, wfm, 'r*')

  plt.grid()

  plt.axis([0,2000,-3000,3000])

  plt.title('Detected Waveform')
  plt.xlabel("Time (usecs)")
  plt.ylabel("Amplitude")
  
  plt.show()
else:
  print()
  print("Test Failed!")
  print("The soundwave is not a balloon")
  balloon.append(0)


#This part of the code writes the file name and important values into another csv file called "data.csv", which is our data log of the soundwaves we have tested.
rows = [zip(fileNames, startPeakValue, endPeakValue, leAvgTimes, peakDurations, ZeroCrossingWFMs, balloon)]

#Test to see if we already created a file and if we did we write to it
file_exists=os.path.exists("data.csv")
csvfile=open('data.csv','a',newline='')
csv_writer=csv.writer(csvfile)

#if it does not exist, we create a file with appropiate headers
if not file_exists:
  headers=["File Names","Start Peak Value", "End Peak Value", "Leading Edge Average Time", "Peak Duration", "Zero Crossing Values", "Balloon"]
  csv_writer.writerow(headers)

#We write the data to the file after it has been created or it exist already
csv_writer.writerows(rows)

csvfile.close()
