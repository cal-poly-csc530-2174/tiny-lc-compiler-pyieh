#!/usr/bin/python
# -*- coding: utf-8 -*-
from sexpdata import loads, dumps

def formatArgs(argList):
   ret = ""
   for i in range(0, len(argList)):
      if (i != 0):
         ret += ","

      ret += " " + dumps(argList[i])

   return ret

def getStringRep(x):
   stringFin = ""
   #  Checks if it's a list and if we need to break it up more recursively
   if type(x) is list:
      # Case of print and (LC LC)
      if (len(x) == 2):
         if (dumps(x[0]) == "println"):
            #print "-PRINTLN-"
            stringFin +=  "(println (" + getStringRep(x[1]) + "))"
         else:
            #print "-(M M)-"
            stringFin += "(" + getStringRep(x[0])
            if type(x[1]) is list:
               stringFin += getStringRep(x[1]) + ")"
            else:
               stringFin += " (" + getStringRep(x[1]) + "))"
      # Case f +, *, or λ
      elif (len(x) == 3):
         if (dumps(x[0]) == "+"):
            #print "-(+)-"
            stringFin += "(" + getStringRep(x[1]) + " + " + getStringRep(x[2]) + ")"
         elif (dumps(x[0]) == "*"):
            #print "-(*)-"
            stringFin += "(" + getStringRep(x[1]) + " * " + getStringRep(x[2]) + ")"
         else:
            #print "-(lambda)-"
            stringFin += "(lambda " + formatArgs(x[1]) + ": " + getStringRep(x[2]) + ")"
      # Case of ifleq0
      elif (len(x) == 4):
         if (dumps(x[0]) == "ifleq0"):
            #print "-<=0-"
            stringFin += "(" + getStringRep(x[2]) + " if (" + getStringRep(x[1]) + " <= 0) else " + getStringRep(x[3]) + ")"

   #  If it isn't a list, it can be a num or id in that case just return the num or id text
   else:
      #print "-ID || Num-"
      stringFin = (dumps(x))
   return stringFin

#Main
inputFile = "INPUT"
obj = open(inputFile, "r")
tok = obj.read()
outF = open("OUTPUT", "w")

toks = loads(tok)

#print(toks)

printFunc = "def println(str):\n   print(str)\n   return 0\n\n"

outputStr = getStringRep(toks)
print outputStr
outF.write(printFunc + outputStr + "\n")
outF.close()

