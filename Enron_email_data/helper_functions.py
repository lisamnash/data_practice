import numpy as np
import pandas as pd

def start_end_sep(df, start, end):
    '''just a function to return the data from the specified time period'''
    return df[(df.time >= start) & (df.time<= end)]
    
def get_senders_set(individual_emails, name):
    '''find the unique people who sent emails to name.  individual_emails list as referred to in comment in class '''
    
    try: 
        if len(individual_emails)>0:
        
            return list(set(individual_emails[:,0][individual_emails[:,1]==name]))
        else: 
            
            return []
    except:
        return individual_emails 
    
def get_receivers_set(individual_emails, name):
    '''find the unique people who received emails from name.  individual_emails list as referred to in comment in class '''
    try:
        if len(individual_emails)>0:
            return list(set(individual_emails[:,1][individual_emails[:,0]==name]))
        else:
            return []
    except:
        return individual_emails
        
        
def split_emails(val):
    '''just a helper function for transforming'''
    return val.split('|')
    
def get_individual_emails(df):
    sender_names = df.sender.values
    recipient_lists = df.recipients.values
    return np.array([[sender_names[i], recipi] for i in xrange(len(recipient_lists)) for recipi in recipient_lists[i]])
     
def get_unique_sent_received_counts(individual_emails, names_list):

    received_from = [len(get_senders_set(individual_emails, name)) for name in names_list]
    sent_to = [len(get_receivers_set(individual_emails, name)) for name in names_list]

    return pd.DataFrame(np.array([names_list, sent_to, received_from]).T, columns = ['person', 'unique_sent_to', 'unique_received_from'])



