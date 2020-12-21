#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import json
import pandas as pd
import numpy as np
import re
import math

response = requests.get('https://care.personcentredsoftware.com/mcm/api/v1/dc7d2fea-29a0-4a3d-98cc-b63789242bad/organisationapi/Get/serviceusers?includecontacts=true').text;
response_info = json.loads(response)


# In[2]:


# # returns the full name of the first service user
# userName = serviceUser['firstName'] + " " + serviceUser['lastName']

# # returns the room of the first service user
# userRoom = serviceUser['room']

# # returns an array with phone numbers of the first relationship of the first service user
# relationshipPhones = response_info[0]['serviceUsers'][0]['relationships'][0]['telephone']

# # returns true if the relationship is for an emergency contact
# isEmergencyContact = relationship['emergencyContact']

# # returns an array of the email of the first relationship of the first service user
# relationshipEmail = response_info[0]['serviceUsers'][0]['relationships'][0]['email']


# In[3]:


firstNames = []
lastNames = []
userRooms = []
telephones = []
emergency = []
email = []

def getUserInformation(): 
    for serviceUser in response_info[0]['serviceUsers']:
        for relationship in serviceUser['relationships']:
            firstName = serviceUser['firstName']
            lastName = serviceUser['lastName']
            userRoom = serviceUser['room']
            relationshipPhones = relationship['telephone']
            isEmergencyContact = relationship['emergencyContact']
            relationshipEmail = relationship['email']
            
            firstNames.append(firstName)
            lastNames.append(lastName)
            userRooms.append(userRoom)
            telephones.append(relationshipPhones)
            emergency.append(isEmergencyContact)
            email.append(relationshipEmail)   


# In[4]:


getUserInformation()


# In[5]:


flex_df = pd.DataFrame(columns=['FirstName','Last Name','Room','Emergency Contact','Phones','Email','Notes'])


# In[6]:


flex_df['FirstName'] = firstNames
flex_df['Last Name'] = lastNames
flex_df['Room'] = userRooms
flex_df['Phones'] = telephones
flex_df['Emergency Contact'] = emergency
flex_df['Email'] = email


# In[7]:


flex_df


# In[8]:


phone_data1 = []
phone_data2 = []

for index, row in flex_df.iterrows():
    if len(row['Phones']) > 1: 
        phone_data1.append(row['Phones'][0])
        phone_data2.append(row['Phones'][1])      
    elif len(row['Phones']) == 1:
      
        if len(row['Phones'][0]) > 0:
            phone_data1.append(row['Phones'][0])
            phone_data2.append(0) 
        else:
            phone_data1.append(0)
            phone_data2.append(0)

flex_df["Phone1"] = phone_data1
flex_df["Phone2"] = phone_data2


# In[ ]:





# In[9]:


flex_df


# In[10]:


del flex_df['Phones']


# In[11]:


flex_df


# In[12]:


email_list=[]

def emailChecker():

    for email in flex_df['Email']:
        if len(email[0])==0:
            email_list.append(0)
        else:
            email_list.append(email[0])
            
emailChecker()


# In[13]:


del flex_df['Email']
flex_df['Email']= email_list
flex_df.head(15)


# In[14]:


mobile_list = []
landline_list = []

def telephoneChecker():
    for index, row in flex_df.iterrows():
# 0,0
        if row['Phone1'] == 0:
            mobile_list.append("Check Mobile")
            landline_list.append("Check Landline")
# Mobile + ?
        elif re.search("^07", row['Phone1']) is not None:
            if row['Phone2'] == 0:
# Mobile + 0
                mobile_list.append(row['Phone1'])
                landline_list.append("Check Landline")
# Mobile + Landline (or Mobile2)
            else:
                mobile_list.append(row['Phone1'])
                landline_list.append(row['Phone2'])  
        else:
# Landline + ?
            if row['Phone2'] == 0:
# Landline + 0
                landline_list.append(row['Phone1'])
                mobile_list.append("Check Mobile")
# Landline + Mobile (or Landline2)
            else:
                landline_list.append(row['Phone1'])
                mobile_list.append(row['Phone2'])


# In[15]:


telephoneChecker()


# In[16]:


flex_df['Mobile'] = mobile_list
flex_df['Landline'] = landline_list
del flex_df['Phone1']
del flex_df['Phone2']
flex_df.head()


# In[17]:


flex_df.to_csv(r'flex.csv')


# In[ ]:




