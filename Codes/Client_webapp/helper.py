import pandas
import numpy

def dftolist(dataf, pass_rate):
    
    """
    
    This function gets the raw data from overall_Scores SQL DB and prepares it for rendering it in the HTML

    Functionality :

    1. Round of the score obtained and total score to 2 decimal places.
    2. Calculate the percentage marks obtained
    3. Compute whether the aspirant has passed


    
    """

    dataf['Scores_Obtained'] = dataf['Scores_Obtained'].astype('int')
    dataf['MaxMarks'] = dataf['MaxMarks'].astype('int')
    dataf['percentage'] = (dataf['Scores_Obtained']/dataf['MaxMarks']*100).astype('int')

    dataf['passed'] = dataf['percentage'].apply(lambda x: 'Yes' if x>pass_rate else 'No')

    list_of_dict=[]
    cols = dataf.columns.tolist()

    for i in range(dataf.shape[0]):
        internal_dict={}

        for j, val in enumerate(dataf.iloc[i,:].values):
            internal_dict[cols[j]] = val

        list_of_dict.append(internal_dict) 
    return list_of_dict


def formatter(dataf):

    """
    
    This function accepts the dataframe for the multiple aspirants case and returns a list of emails and a dictionary of emails:[list of topics]
    
    Functionality:

    1. Replace blank entries by 'No'
    2. Replace 'Yes' in the topic columns by the topic name, i.e. 'Yes' in 'Statistics' -> 'Statistics'
       A demo is there in the test_pad.ipynb
    3. Store the list of emails
    4. Create the dictionary of {email:[list of topics]} for different aspirants
    5. Return the list of emails and the dictionary created above

    """
    dataf.fillna('No', inplace=True)
    for i in range(len(dataf)):
        for col in dataf.columns[1:]:
            dataf[col][i] = col if dataf[col][i]=='Yes' else ''
    emails = dataf.iloc[:,0].tolist()
    topics={}
    vals = {0:'Email',1:'Statistics',2:'Linear Regression',3:'Logistic Regression',4:'KNN',5:'SVM',6:'Kmeans',7:'Decision Tree',8:'Naive Bayes'}

    for i in range(dataf.shape[0]):
        topics[emails[i]]=[vals[kk] for kk in [x for x in dataf.iloc[i,:].tolist()[1:] if x!='']]
    emails = emails[1:]
    return emails, topics

