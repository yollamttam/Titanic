#!/usr/bin/python

import sqlite3
import sys
import numpy as np
import numpy.ma as ma


### We would like to read in the training database and output our feature matrix and answer vector ###
conn = sqlite3.connect('titanicTrain.db')
cursor = conn.cursor()
print "Successfully loaded training database..."

#initialize X and y matrices 
cursor.execute("select count(*) from trainData")
nrowsTuple = cursor.fetchall()
nrowsTuple = nrowsTuple[0]
nrows = nrowsTuple[0]
print nrows
ncols = 8
X = np.zeros((nrows,ncols))
y = np.zeros((nrows,1))

cursor = conn.execute("select * from trainData;")
i = 0;
for row in cursor:
    y[i] = row[1]
    X[i,0] = 1
    X[i,1] = row[2]
    sex = row[4]
    sex = sex.encode('ascii','ignore')
    if (sex == 'male'):
        X[i,2] = -0.5
    else:
        X[i,2] = .5

    X[i,3] = row[5]
    X[i,4] = row[6]
    X[i,5] = row[7]
    X[i,6] = row[8]
    X[i,7] = row[9]
    i = i + 1

print "assembled matrices...closing database"
conn.close()


### OK, so now we have made our features matrix and results matrix###



