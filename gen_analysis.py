import pandas as pd
import streamlit as st
import numpy as np
import plotly.express as px
from sklearn import preprocessing
import altair as alt

data=pd.read_csv('final_occgroup_10000_no_stop.csv')

transposed=data.T
transposed=transposed.reset_index()
transposed.columns=transposed.iloc[0,:]
transposed=transposed.iloc[1:,:]
transposed.columns=['word','Critical_Thinking', 'Instructing', 
                     'Management_of_Financial_Resources',  'Mathematics',
                      'Quality_Control_Analysis',  'Service_Orientation', 
                     'Speaking','Technology_Design']
                     
means=[np.median(np.array(transposed.iloc[i,1:])) for i in range (0,len(transposed))]
means=[int(float(i)) for i in means]
means=pd.Series(means, name='word_mean').copy()

transposed['mean']=means
transposed=transposed.fillna(0)
relevant=transposed[transposed['mean']>500]

df=relevant.T
df=df.reset_index()
df.columns=df.iloc[0,:]
df=df.iloc[1:,:]
df=df.rename(columns={'word':'skill_category'})
df=df.iloc[:8,:]

st.write('Words Having a Mean Occurence Greater Than 22 for each Skill Category')

st.subheader('Data')
default_type=st.multiselect('Select a Skill Category', list(df.skill_category.unique()), 
                            default=['Critical_Thinking', 'Instructing', 'Management_of_Financial_Resources',
                                      'Mathematics', 'Quality_Control_Analysis', 'Service_Orientation', 'Speaking'])
new_data=df[df.skill_category.isin(default_type)]
st.write(new_data)

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


st.subheader('Word Comparison Within Skill Group')
pred=st.selectbox('X', df.columns[:],index=1)
deft=st.selectbox('Y', df.columns[:],index=3)
fig = px.scatter(new_data, x =pred,y=deft, color='skill_category')
st.plotly_chart(fig)


st.subheader('Skill Group Cluster Analysis')
relevant_c=relevant.iloc[:,1:9]
val=relevant_c.values
relevant_scaled=preprocessing.normalize(val,norm='l2')
relevant_scaled=pd.DataFrame(relevant_scaled)
relevant_scaled.columns=relevant_c.columns


cls_X=st.selectbox('X', relevant_scaled.columns[:],index=1)
cls_Y=st.selectbox('Y', relevant_scaled.columns[:],index=4)
c = alt.Chart(relevant_scaled).mark_circle().encode(x=cls_X, y=cls_Y)
st.altair_chart(c, use_container_width=True)

df_full=pd.read_csv('df_full_10000.csv')

st.subheader('Skill Category Alignment by Ranked Order for Each ID')
default_type=st.selectbox('Select an ID', list(df_full.ids.unique()))
                          
                          
new_data=df_full[df_full.ids==default_type]
st.write(new_data.iloc[:,1:])
