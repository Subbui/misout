import numpy as np

class VariableTreat:
    '''Class method to impute missing values'''
    def __init__(self,df):
        self.df = df

    def outlier_treat(self,lower_percentile=0,upper_percentile=99,var_list=[]):
        try:
            if ((len(var_list)>0) and (upper_percentile <= 100) and (lower_percentile>=0)):                    
                for i in self.df.select_dtypes(include=np.number).columns:
                    if i in var_list:
                        ll,ul = np.nanpercentile(self.df[i],[lower_percentile,upper_percentile])
                        self.df[i].loc[self.df[i]<ll]=ll
                        self.df[i].loc[self.df[i]>ul] = ul
                    else:
                        pass
            elif not var_list:
                print("Variable list can't be empty")
            elif ((upper_percentile>100) or (lower_percentile<0)):
                print("Percentile values should be betweeen 0 and 100")
            else:
                print('Unknown error')
        except:
            print("Error in the values")
            
        return self.df

    def missing_treat(self,num_impute='other',char_impute='other',missing_percent=0.7,drop=False,
                     num_impute_value=9999, char_impute_value='missing',exclude_var=[]):
        """This function deletes the columns with missing values > missing_percent and
        imputes the remaining missing values with either Mean, Median or Mode
        
        missing_percent: Threshold beyond which the variables will be removed
            For ex: missing_percent = 0.3 indicates the varialbes with more than 30% missing
            values will be removed from the data
            
        num_impute: Values could be mean, median or mode
        
        char_impute: value will be mode always"""
        
        try:
            if drop==True:
                for i in self.df.columns:
                    if ((i not in exclude_var) and 
                        (self.df[i].isnull().sum()/self.df[i].shape[0]>missing_percent)):
                        self.df.drop(i,axis=1,inplace=True)
            else:
                pass
        except:

            print('missing percent value should be grater than 0')
        
        try:
            for i in self.df.select_dtypes(include=np.number).columns:
                if (((self.df[i].isnull().sum()>0)) and (i not in exclude_var)):
                    if num_impute=='other':
                        self.df[i].fillna(num_impute_value,inplace=True)
                    elif num_impute=='mean':
                        self.df[i].fillna(self.df[i].mean(),inplace=True)
                    elif num_impute=='median':
                        self.df[i].fillna(self.df[i].median(),inplace=True)
                    else:
                        self.df[i].fillna(self.df[i].mode()[0],inplace=True)
                        
                elif ((self.df[i].isnull().sum()>0) and (i not in exclude_var)):
                    if char_impute=='other':
                        self.df[i].fillna(char_impute_value,inplace=True)
                    else:
                        self.df[i].fillna(self.df[i].mode()[0],inplace=True)
                else:
                    continue
        except:
            
            print('Check the impute values')
            
        return self.df
