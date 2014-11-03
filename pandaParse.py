import pandas as pd
import numpy as np
import sys


###### Select Classification Algorithm ######

print "Please Select Classification Algorithm:"
print "1: Logistic Regression (L2 Regularization)"
print "2: Random Forest"
algorithm = input("Selection: ")
crossValidate = input("Would you like to cross validate? (0/1)")

###### LOAD AND CLEAN TRAINING DATA ######
df = pd.read_csv('train.csv',header=0)

# Let's make gender an int
df['Gender'] = df['Sex'].map({'female':0, 'male':1}).astype(int)

# Fill in missing ages with median ages from the gender/class
df['AgeFill'] = df['Age']
# Calculate averages
median_ages = np.zeros((2,3))
for i in range(0,2):
    for j in range(0,3):
        median_ages[i,j] = df[(df['Gender']==i)&\
        (df['Pclass']==j+1)]['Age'].dropna().median()

#Fill in averages
for i in range(0,2):
    for j in range(0,3):
        df.loc[(df['Age'].isnull())&(df['Gender']==i)&\
        (df['Pclass']==j+1),'AgeFill'] = median_ages[i,j]


df = df[~df['Age'].isnull()]
# Drop rows we don't care about
df = df.drop(['Name','Sex','Ticket','Age','PassengerId','Cabin','Embarked'],axis=1)
# ...and rows with null values

# train data!
train_data = df.values
X = train_data[0::,1::]
Y = train_data[0::,0]

############################################

####### LOAD AND CLEAN THE TEST DATA #######
df = pd.read_csv('test.csv',header=0)
df['Gender'] = df['Sex'].map({'female':0, 'male':1}).astype(int)
df['AgeFill'] = df['Age']


median_ages = np.zeros((2,3))
for i in range(0,2):
    for j in range(0,3):
        median_ages[i,j] = df[(df['Gender']==i)&\
        (df['Pclass']==j+1)]['Age'].dropna().median()

for i in range(0,2):
    for j in range(0,3):
        df.loc[(df['Age'].isnull())&(df['Gender']==i)&\
        (df['Pclass']==j+1),'AgeFill'] = median_ages[i,j]

median_fares = np.zeros((1,3))
for i in range(0,3):
    median_fares[0,i] = df[df['Pclass']==i+1]['Fare'].dropna().median()

for i in range(0,3):
    df.loc[df['Fare'].isnull(),'Fare'] = median_fares[0,i]


newdf = df
df = df.drop(['Name','Sex','Ticket','Age','PassengerId','Cabin','Embarked'],axis=1)

#df = df.dropna()
test_data = df.values
Xtest = test_data
############################################

if (crossValidate):
    Xfull = X
    Yfull = Y
    m = len(X[:,0])
    ntrain = np.floor(2*m/3)
    ntest = m - ntrain;
    X = Xfull[0:(ntrain-1),:]
    Y = Yfull[0:(ntrain-1)]
    Xtest = Xfull[ntrain::,:]
    Ytest = Yfull[ntrain::]
    
if (algorithm == 1):
    from sklearn.linear_model import LogisticRegression
    
    #presumably, the settings for the logistic regression
    #logistic = LogisticRegression(penalty='l2', dual=False, tol=0.0001, C=1.0, fit_intercept=True, intercept_scaling=1, class_weight=None, random_state=None)
    logistic = LogisticRegression(penalty='l2')

    #fit
    logistic.fit(X,Y)
    
    #predict
    output = logistic.predict(Xtest)

elif (algorithm == 2):

    # Import the random forest package
    from sklearn.ensemble import RandomForestClassifier 
    
    # Create the random forest object which will include all the parameters
    # for the fit
    forest = RandomForestClassifier(n_estimators = 300)

    # Fit the training data to the Survived labels and create the decision trees
    forest = forest.fit(X,Y)

    # Take the same decision trees and run it on the test data
    output = forest.predict(Xtest)


if (crossValidate):
    print np.shape(Ytest)
    print np.shape(Xtest)
    print np.shape(output)
    success = Ytest*output
    success = sum(success)/len(success)
    print "your success rate was:",success



outfile = open('MattSubmission.txt','w')
outfile.write("PassengerID,Survived\n")
for a,b in zip(newdf['PassengerId'],output):
    outfile.write("%d,%d\n"%(a,b))

outfile.close()
