import numpy as np
import matplotlib.pyplot as plt


import seaborn
import pandas as pd

from helper_functions import *

class emailData():
    def __init__(self, df):
        
        if df.columns.values[0] == 'time':
            self.transformed_df = df
        
        else:
            self.transformed_df = self._reformat_dataframe(df)
        
        
        self.all_names, self.senders, self.receivers, self.individual_emails = self.get_all_name_list(self.transformed_df)
        self.counts_df = self.name_aggregate_counts(self.transformed_df)
        self.prolific_senders = self.get_prolific_senders(15)
        self.current_time_ag = [self.transformed_df]
        
    def _reformat_dataframe(self, df):
        '''This function takes in the original dataframe and puts it into a more usable format 
           (what I call a transformed dataframe).  Time is in days.'''
        headers = ['time', 'messageid', 'sender', 'recipients', 'topic', 'mode']
        df.columns = headers
        df.drop(['topic', 'mode'], axis = 1, inplace = True)
        df.recipients = df.recipients.astype(str)
        df.recipients = df.recipients.apply(split_emails)
        df.time = (df.time - df.time.min())/(1000*60*60*24)
    
        return df
    
    def get_all_name_list(self, df):
        '''This function takes in a transformed dataframe and returns a list of all names as well as just sender and recipients.
           Also the original df has multiple recipients in one row so I make a list of the form [[sender, receiver1], [sender, receiver2]]'''
        
        sender_names = df.sender.values
        recipient_lists = df.recipients.values

        individual_emails = np.array([[sender_names[i], recipi] for i in xrange(len(recipient_lists)) for recipi in recipient_lists[i]])
        
        sender_names = list(set(sender_names))
        recipient_names = list(set([item for sublist in recipient_lists for item in sublist]))
        
        return list(set(sender_names + recipient_names)), sender_names, recipient_names, individual_emails
    
    def name_aggregate_counts(self, df):
        ''' Here I'm doing counts grouped by name. (hence name_aggregate)'''
        sender_names = list(df.sender.values)
        recipient_lists = df.recipients.values

        recipient_names = [item for sublist in recipient_lists for item in sublist]
   
        recipient_series = pd.Series(recipient_names)
        recp_counts = recipient_series.value_counts()
        send_counts = df.sender.value_counts()
        
        countdf = pd.DataFrame(self.all_names, columns = ['person'], index = self.all_names)
    
        countdf['sent'] = send_counts
        countdf['received'] = recp_counts
        countdf.names = countdf.person.astype(str)
        countdf = countdf.fillna(0)

        countdf.sent = countdf.sent.astype(int)
        countdf.received = countdf.received.astype(int)
    
        countdf.sort_values('sent',  ascending=False, inplace=True)
        return countdf
    
    def time_aggregate(self, start_date, end_date, num_days):
        ''' Here I partition a transformed data frame between start_date (in days) and end_date (in days).
            num_days is the number of days that is in each partition'''
        num_partitions = np.ceil((end_date - start_date)/num_days) + 1

        df = start_end_sep(self.transformed_df, start_date, end_date)

        times = np.linspace(start_date, end_date, num_partitions)
        sub_data = [start_end_sep(df, times[i], times[i+1]) for i in xrange(len(times)-1)]

        self.current_time_ag = sub_data
        return sub_data
    
    def name_time_aggregate(self, start_date, end_date, num_days):
        ''' This combines the last two functions an breaks down the df into other dfs by time
            and then performs sent-received counts on each of those dfs.'''
        sub_data = self.time_aggregate(start_date, end_date, num_days)
        return [self.name_aggregate_counts(data) for data in sub_data]

    def get_prolific_senders(self, num_std):
        ''' The class has a method to get prolific senders based on whether they emailed some number of standard deviations
            above the mean'''
        std_sent = self.counts_df.sent.std()
        mean_sent = self.counts_df.sent.mean()
        return self.counts_df.person[self.counts_df.sent > num_std*std_sent + mean_sent].values