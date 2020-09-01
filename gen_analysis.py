#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import streamlit as st
import numpy as np
import plotly.express as px


# In[15]:


data=pd.read_csv('final_occgroup_10000.csv')


# In[72]:


transposed=data.T


# In[74]:


transposed=transposed.iloc[1:,]


# In[75]:


means=[np.mean(np.array(transposed.iloc[i,:])) for i in range (0,len(transposed))]


# In[77]:


means=[int(float(i)) for i in means]
means=pd.Series(means, name='word_mean').copy()


# In[79]:


means.mean()


# In[80]:


transposed=transposed.reset_index()


# In[81]:


transposed['mean']=means


# In[83]:


list(data.skill_category)


# In[94]:


transposed.columns=['word','Critical_Thinking',  'Instructing', 
                    'Management_of_Financial_Resources',
                     'Mathematics',  'Quality_Control_Analysis',
                     'Service_Orientation',  'Speaking',
                     'Technology_Design','mean']


# In[95]:


relevant=transposed[transposed['mean']>22]


# In[116]:


df=relevant.T
df=df.iloc[1:8,:]


# In[117]:


df.columns=relevant.T.iloc[0,:]


# In[118]:


df=df.reset_index()


# In[119]:


df=df.rename(columns={'index':'skill_category'})


# In[ ]:





# In[ ]:





# In[ ]:


st.write('Words Having a Mean Occurence Greater Than 22 for each Skill Category')


# In[ ]:


st.subheader('Data')
default_type=st.multiselect('Select a Skill Category', list(df.skill_category.unique()), 
                            default=['Critical_Thinking',
 'Instructing',
 'Management_of_Financial_Resources',
 'Mathematics',
 'Quality_Control_Analysis',
 'Service_Orientation',
 'Speaking'])
new_data=df[df.skill_category.isin(default_type)]
st.write(new_data)


# In[ ]:
relevant2=relevant.set_index('word')
trimmed_data=[]
for i in relevant2:
    trimmed_data.append(relevant2[i].sort_values(ascending=False)[:50])

bar_data=pd.DataFrame(trimmed_data[0]).join(pd.DataFrame(trimmed_data[1]), how='outer')\
.join(pd.DataFrame(trimmed_data[2]), how='outer')\
.join(pd.DataFrame(trimmed_data[3]), how='outer')\
.join(pd.DataFrame(trimmed_data[4]), how='outer')\
.join(pd.DataFrame(trimmed_data[5]), how='outer')\
.join(pd.DataFrame(trimmed_data[6]), how='outer')\
.join(pd.DataFrame(trimmed_data[7]), how='outer')
bar_data=bar_data.fillna(0)
bar_data=bar_data.reset_index()

st.subheader('Top 50 Word Occurrences for Skill Category')
bar_x=st.selectbox('X', bar_data.columns[1:])
bar_fig=px.bar(bar_data, x =bar_data.word, y=bar_x)
st.plotly_chart(bar_fig)



# In[ ]:


st.subheader('Chart')
pred=st.selectbox('X', df.columns[:],index=1)
deft=st.selectbox('Y', df.columns[:],index=4)
fig = px.scatter(new_data, x =pred,y=deft, color='skill_category')
st.plotly_chart(fig)


# In[ ]:





# In[ ]:




