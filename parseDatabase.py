#!/usr/bin/python

import sqlite3
import sys
import numpy as np
import numpy.ma as ma


### We would like to read in the training database and output our feature matrix and answer vector ###

conn = sqlite3.connect('titanicTrain.db')
print "Successfully loaded training database..."

#initialize X and y matrices 
nrows = select count(*) from trainData
ncols = 7
X = np.zeros((nrows,ncols))
y = np.zeros((nrows,1))

cursor = conn.execute("select * from trainData;")







### Below here, you'll find some potentially useful old code ###
#let's load the database using this module thing
conn = sqlite3.connect('matt.db')
print "Successfully loaded database...";

#let's show the contents of the database
cursor = conn.execute("select * from wall;")
print "\n **** DISPLAYING CONTENTS OF TABLE **** \n"
for row in cursor:
    print "PersonID: ", row[0]
    print "Wall Post: ", row[1]
print "\n **** DISPLAYED CONTENTES SUCCESSFULLY **** \n";


#let's add something to the database.
IDtemp = raw_input("Please enter Person ID:")
walltemp = raw_input("What is your post?")
conn.execute("insert into wall values (?, ?)",[IDtemp, walltemp])

cursor = conn.execute("select * from wall;")
print "\n **** ADDING CONTENT TO TABLE **** \n"
for row in cursor:
    print "PersonID: ", row[0]
    print "Wall Post: ", row[1]
print "\n **** SUCCESSFULLY ADDED CONTENT **** \n"

PersonLookup = raw_input("Who would you like to look up?")
#cursor = conn.execute('''select * from wall where "PersonID" = (?)''',PersonLookup)
cursor = conn.execute('''select * from wall where "PersonID" = ?;''',(PersonLookup,))
print "\n **** LOOKING UP ENTRIES IN TABLE **** \n"
for row in cursor:
    print "Wall Post: ", row[1]
print "\n **** SUCCESSFULLY LOOKED UP ENTRIES **** \n"


savebool = raw_input("Would you like to save changes? (0/1)")
savebool = int(savebool)
if (savebool == 1):
    conn.commit()
    print "saved changes..."
conn.close()




