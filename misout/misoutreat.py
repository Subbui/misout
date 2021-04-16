import numpy as np

class VariableTreat:
    '''Class method to treat the outliers and impute missing values'''
    def __init__(self,df):
        self.df = df

    def outlier_treat(self,lower_percentile=0,upper_percentile=99,var_list=[]):
        '''To treat the outliers either by lower or upper percentile values mentioned as parameters
            This funciton has the following parameters:
            lower_percentile: A percentile value, for ex: 1, 2 etc. The outliers at the lower end will be
                                replaced with the value of lower_percentile number provided
                                
            upper_percentile: A percentile value, for ex: 98, 99 etc. The outliers at the upper end will be
                                replaced with the value of upper_percentile number provided
                                
            var_list: list of columns to perform the outerlier treatment.'''
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
        """This function deletes the columns with missing values > missing_percent when drop=True and
        imputes the missing values in reaminig columns with either Mean, Median, Mode or a spedified value
        
        num_impute : possible values mean, median, mode, other. If provided other, user need to provide the
                    custom number to replace the missing values.

        char_impute: possible values are mode, other. If provided other, user need to provide the custom
                    string to replace the missing values.

        missing_percent : possible values are between 0 and 1. Should be used in combination with drop

        drop : possible values are True, False. If true, all the columns with missing value percent greater than
                missing_percent value will be removed from the data set.
                If False, missing_percent value wouldn't have any affect.

        num_impute_value : if num_impute == 'other', user needs to specifiy a number to replace the missing 
                            values. If num_impute <> 'other', then this parameter wouldn't have any affect.
                            default value for this parameter is 9999

        char_impute_value: if char_impute == 'other', user needs to specifiy a string to replace the missing 
                            values. If char_impute <> 'other', then this parameter wouldn't have any affect.
                            Default value for this parameter is 'missing'

        exclude_var : list of column names user want to exclude from the missing value treatment, like the target
                        variable.
        
        missing_percent: Threshold beyond which the variables will be removed
            For ex: missing_percent = 0.3 indicates the varialbes with more than 30% missing
            values will be removed from the data
            """
        
        try:
            if drop==True:
                for i in self.df.columns:
                    if ((i not in exclude_var) and 
                        (self.df[i].isnull().sum()/self.df[i].shape[0]>missing_percent)):
                        self.df.drop(i,axis=1,inplace=True)
            else:
                pass
        except:

            print('missing percent value should be between 0 and 1')
        
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
