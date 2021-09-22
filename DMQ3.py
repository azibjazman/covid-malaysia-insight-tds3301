#General libraries
import streamlit as st 
import numpy as np
import pandas as pd
import altair as alt 
from streamlit_folium import folium_static
import folium

#Visualisation libraries
import altair as alt
import seaborn as sns
import missingno as msno
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(layout="wide")
#Read files
cases_malaysia = pd.read_csv('cases_malaysia.csv')
cases_states = pd.read_csv('cases_state.csv')
test_malaysia = pd.read_csv('tests_malaysia.csv')
test_states = pd.read_csv('tests_state.csv')
clusters = pd.read_csv('clusters.csv')
pahangFS = pd.read_csv('PahangFS.csv')
kedahFS = pd.read_csv('KedahFS.csv')
johorFS = pd.read_csv('JohorFS.csv')
selangorFS = pd.read_csv('SelangorFS.csv')
clfP = pd.read_csv('clfPahangMetrics.csv')
clfK = pd.read_csv('clfKedahMetrics.csv')
clfJ = pd.read_csv('clfJohorMetrics.csv')
clfS = pd.read_csv('clfSelangorMetrics.csv')
regP = pd.read_csv('regPahangMetrics.csv')
regK = pd.read_csv('regKedahMetrics.csv')
regJ = pd.read_csv('regJohorMetrics.csv')
regS = pd.read_csv('regSelangorMetrics.csv')

st.title('Data Mining Assignment Question 3 Findings')
st.caption('By: 1181100438 (AzibJazman) and 1171103938 (NurinaIzzati)')

st.header('Exploratory Data Analysis')
st.write('For this assignment, we have conducted EDA on 5 datasets provided by the MOH')



st.image('./newCases_recoveredCases.png')
st.write('The plots shows that the number of new and recovered cases have increased steadily up until May 2021. Starting on June 2021, Malaysia had a spike in new Covid cases and recovered patients. New covid cases has a faster rate of increase rather than recovered cases.')
st.write('----------------------------------------------------------------------------------------------------------------------------------------------')

col1, col2 = st.columns(2)

col1.image('./dailyClustersCases.png')

col2.write('')
col2.write('In 2021, most Covid cases came from workplace clusters. Although it went down around early March, it started to rise again in May 2021. When the government stated that only a small percentage of workers are allowed to be in the office around mid-March, number of workplace clusters also decreases.')
col2.write('')
col2.write('Number of community clusters shown a big increase on the second half of 2021')
col2.write('')
col2.write('Relious clusters also had a significant number of cases around end of May. This could be due to when people are allowed to went for prayers at mosques, churchs etc.')

st.write('----------------------------------------------------------------------------------------------------------------------------------------------')

states = cases_states.groupby(["state"]).agg({"cases_new":"sum"})
states = states.reset_index()

#Sidebar - States selector
unique_states = sorted(cases_states['state'].unique())
selected_states = st.sidebar.multiselect('States', unique_states)

#Filter states data
df_cases_states = cases_states[(cases_states['state'].isin(selected_states))]

#Show dataframe based on states selected


st.header('Cases by states')
st.caption('Please select the states at the sidebar to display the data')
st.dataframe(df_cases_states)

st.write('For this dataset, we found out the average and distribution of new Covid cases for each state')
col1, col2 = st.columns(2)
col1.image('./avgCasesStates.png')
col2.image('./distributionCasesStates.png')
st.write('Selangor has the highest average cases per day. Perlis, WP Labuan and Putrajaya has less than 20 cases per day in average. Looking at the boxplot, we found out every state have a lot of outliers. This is could be due to the different situation of Covid cases in Malaysia. Although there are clear outliers in our dataset, we decided to not remove them as it may show potential trends.')
st.write('')
st.image('./distributionCasesStatesDaily.png')
st.write('Based on the graph above, Selangor has recorded the most daily new Covid cases. However, starting around August 2021, Selangor has shown a decrement in number of cases. Sarawak, on the other hand, has shown a gradual increase in number of cases starting from August 2021.')
st.write('')
st.write('WP Labuan recorded the least number of cases throughout the pandemic.')

st.header('Tests malaysia')
col1, col2 = st.columns(2)
col1.image('./testKits.png')
col2.write('')
col2.write('In the early of the pandemic, Malaysia only use PCR testkits for Covid19 detection. At the end of 2020, RTK-AG testkits started to rose. PCR tests was conducted more up to mid July of 2021 and not until this past few months, RTK-AG then started to be used more to detect covid-19 cases.')

st.header('Tests states')
st.write('We plot the boxplot for each type of tests conducted to see outliers')

#Average of RTK and PCR test
avgTestRTK = test_states.groupby(["state"]).agg({"rtk-ag": "mean"}).sort_values("state")
avgTestRTK = avgTestRTK.reset_index()
avgTestPCR = test_states.groupby(["state"]).agg({"pcr": "mean"}).sort_values("state")
avgTestPCR = avgTestPCR.reset_index()

col1, col2 = st.columns(2)

fig = go.Figure(data=[
    go.Bar(name='RTK-AG', x=avgTestRTK['state'], y=avgTestRTK['rtk-ag'],text=avgTestRTK['rtk-ag'],textposition='auto'),
    go.Bar(name='PCR', x=avgTestPCR['state'], y=avgTestPCR['pcr'],text=avgTestPCR['pcr'],textposition='auto')])

col1.write(fig)

col2.image('./totalTests.png')
st.write('Based on the plots above, Selangor conducted the most tests for both RTK-AG Testkits and PCR Testkits, Kedah, Perak, Pulau Pinang, Sabah and WP Labuan conducted more RTK-AG tests than PCR tests.')

st.header('Clusters')
st.write('Most of clusters in Malaysia are from workplace and community.')
st.image('./clustersType.png')
col1, col2 = st.columns(2)

col1.image('./casesClusters.png')
col2.image('deathsCluster.png')
col1.write('In general, the plot above shows that WP Kuala Lumpur, WP Putrajaya, Selangor, Negeri Sembilan, Perak and Melaka have many workplace clusters that recorded more than 1000 cases per cluster')
col2.write('However, the highest deaths recorded by a cluster was at Pahang and Perak with more than 35 deaths. Interestingly, those high deaths were from a community cluster type and not a workplace cluster, despite the amount of new cases as shown on the left side plot.')

st.header('Question 2')
st.write('In order to find states that exhibits strong correlation with Pahang and Johor, we decided to use the cleaned cases_states dataset and use the correlation matrix.')
col1, col2 = st.columns(2)
col1.subheader("New Cases")
col1.image('newCasesCorr.png')
col1.write('In terms of new Covid cases, Pahang is highly positively correlated with states like Johor (0.89), Kedah (0.94), Kelantan(0.89), Melaka(0.88), Perak(0.91), Pulau Pinang(0.90), Sabah(0.84), Selangor(0.87) and Terengganu(0.91)')
col1.write('For Johor, it is highly correlated with 8 other states including Kedah(0.90), Kelantan(0.89), Pahang(0.89), Perak(0.92), Pulau Pinang(0.92), Sabah(0.87), Sarawak(0.84) and Terengganu(0.91)')
    
col2.subheader('Import Cases')
col2.image('importCasesCorr.png')
col2.write('In terms of Import cases, Pahang and Johor both have weak correlation with other states.')
col2.write('For Pahang, Perak has the highest correlation of 0.24 if to compare with other states.')

col1, col2 = st.columns(2)
col1.subheader('RTK-AG Tests')
col1.image('rtkCorr.png')
col1.write('In terms of RTK-AG tests, Pahang has weak positive correlation with every state where Selangor is the highest(0.57)')
col1.write('Johor is strongly positively related with Perak(0.81) and Sabah(0.81).')

col2.subheader('PCR Tests')
col2.image('pcrCorr.png')
col2.write('Pahang has a moderate positive relationship with Johor and Kedah with 0.66 each, while Johor has a strong positive correlation with Pulau Pinang(0.83) and Kedah(0.82) when it comes to PCR Testing.')

col1, col2 = st.columns(2)
col1.subheader('Recovered Cases')
col1.image('recoveredCasesCorr.png')
col2.write('')
col2.write('')
col2.write('')
col2.write('In terms of recovered Covid cases, Kedah(0.92), Kelantan(0.85), Perak(0.89), Selangor(0.88) and Terengganu(0.85) is positively correlated with Pahang.In terms of Import cases, Pahang and Johor both have weak correlation with other states.')
col2.write('While for Johor, Perak(0.81) and Kedah(0.80) is strongly positively correlated with each other.')

st.write('----------------------------------------------------------------------------------------------------------------------------------------------')
st.header('Question 3')
st.write('We created a function featureSelectionModels(), where it will run multiple feature selection models (Boruta, RFE, Feature Importance, LASSO) and get the score of each feature and return a dataframe of average scores.')
st.write('For each state, we decided to select the top 20 features with the highest average score to be included in our models. We did not select the features based on those that meets the minimum average score in order to avoid there are little or no features that achieved the requirement.')

col1, col2, col3, col4 = st.columns(4)
col1.header('Pahang Top Features Selection')
col1.dataframe(pahangFS.head(20))


col2.header('Kedah Top Features Selection')
col2.dataframe(kedahFS.head(20))

col3.header('Johor Top Features Selection')
col3.dataframe(johorFS.head(20))

col4.header('Selangor Top Features Selection')
col4.dataframe(selangorFS.head(20))
st.write('----------------------------------------------------------------------------------------------------------------------------------------------')


st.header('Question 4')
st.subheader('Classification Models')
st.write('For classification models, we implemented Naive Bayers, K-Nearest Neighbors, Support Vector Machines(SVM), Logistic Regression(Logit) and CART-Decision Tree.')
st.write('We combined all the results into one table for ease of view')

col1, col2 = st.columns(2)
col1.subheader('Pahang')
#col1.dataframe(clfP)

#Chart
x = clfP['Model_Name']
y = clfP['Precision']

fig = go.Figure(data=[
    go.Bar(name='Precision', x=x, y=clfP['Precision'],text=clfP['Precision'],textposition='auto',),
    go.Bar(name='Recall', x=x, y=clfP['Recall'],text=clfP['Recall'],textposition='auto',),
    go.Bar(name='F1_Score', x=x, y=clfP['F1_Score'],text=clfP['F1_Score'],textposition='auto',),
    go.Bar(name='Accuracy', x=x, y=clfP['Accuracy'],text=clfP['Accuracy'],textposition='auto',)])

col1.write(fig)

col2.header(' ')
col2.header(' ')
col2.header(' ')
col2.header(' ')
col2.write('For Pahang state with classification models, KNN model shows the best performance with accuracy value, precision, recall and F1 score of 0.91 compared to other classifier models. Although KNN model performs the best, other models still perform quite well.Thus, KNN Classifier model performs the best in predicting the daily cases for Pahang. ')
st.write('----------------------------------------------------------------------------------------------------------------------------------------------')

col1, col2 = st.columns(2)
col1.subheader('Kedah')
x = clfK['Model_Name']

fig = go.Figure(data=[
    go.Bar(name='Precision', x=x, y=clfK['Precision'],text=clfK['Precision'],textposition='auto',),
    go.Bar(name='Recall', x=x, y=clfK['Recall'],text=clfK['Recall'],textposition='auto',),
    go.Bar(name='F1_Score', x=x, y=clfK['F1_Score'],text=clfK['F1_Score'],textposition='auto',),
    go.Bar(name='Accuracy', x=x, y=clfK['Accuracy'],text=clfK['Accuracy'],textposition='auto',)])

col1.write(fig)

col2.header(' ')
col2.header(' ')
col2.header(' ')
col2.header(' ')
col2.write('For Kedah state with classification models, KNN model shows the best performance with accuracy value, F1 score and recall of 0.94 and precision with 0.93 compared to other classifier models. Although KNN model performs the best, other models still perform quite well. This means that KNN classifier model performs the best in predicting daily cases for Kedah.')
st.write('----------------------------------------------------------------------------------------------------------------------------------------------')

col1, col2 = st.columns(2)
col1.subheader('Johor')

x = clfJ['Model_Name']

fig = go.Figure(data=[
    go.Bar(name='Precision', x=x, y=clfJ['Precision'],text=clfJ['Precision'],textposition='auto',),
    go.Bar(name='Recall', x=x, y=clfJ['Recall'],text=clfJ['Recall'],textposition='auto',),
    go.Bar(name='F1_Score', x=x, y=clfJ['F1_Score'],text=clfJ['F1_Score'],textposition='auto',),
    go.Bar(name='Accuracy', x=x, y=clfJ['Accuracy'],text=clfJ['Accuracy'],textposition='auto',)])

col1.write(fig)
col2.header(' ')
col2.header(' ')
col2.header(' ')
col2.header(' ')
col2.write('For Johor state with classification models, KNN model shows the best performance with accuracy value, F1 score, and recall of 0.79 and precision value of 0.78 compared to other classifier models. Although KNN model is quite moderate, other models also are not quite far. Thus, KNN classifier model performs well in predicting daily cases for Johor.')
st.write('----------------------------------------------------------------------------------------------------------------------------------------------')

col1, col2 = st.columns(2)
col1.subheader('Selangor')
x = clfS['Model_Name']

fig = go.Figure(data=[
    go.Bar(name='Precision', x=x, y=clfS['Precision'],text=clfS['Precision'],textposition='auto',),
    go.Bar(name='Recall', x=x, y=clfS['Recall'],text=clfS['Recall'],textposition='auto',),
    go.Bar(name='F1_Score', x=x, y=clfS['F1_Score'],text=clfS['F1_Score'],textposition='auto',),
    go.Bar(name='Accuracy', x=x, y=clfS['Accuracy'],text=clfS['Accuracy'],textposition='auto',)])

col1.write(fig)

col2.header(' ')
col2.header(' ')
col2.header(' ')
col2.header(' ')
col2.write('For Selangor state with classification models, KNN model shows the best performance with accuracy value, F1 score and recall of 0.83 and precision of 0.86 compared to other classifier models. Although KNN is quite good, other models are also not quite far. Thus, KNN classifier model performs well in predicting daily cases for Selangor.')

st.subheader('In conclusion, we found that KNN Classifier has the best performance to predict new cases for all 4 states. However, other classifier models produce results that is quite close to KNN classifier model.')

st.write('----------------------------------------------------------------------------------------------------------------------------------------------')


st.subheader('Regression Models')
st.write('For regression models, we implemented Linear Regression, Decision Tree Regression and XGBoost Regressor')
st.write('We combined all the results into one table for ease of view')

col1, col2 = st.columns(2)
col1.subheader('Pahang')
col1.dataframe(regP)

x = regP['Model_Name']
fig = go.Figure(data=[
    go.Bar(name='R2-Score', x=x, y=regP['R2-Score'],text=regP['R2-Score'],textposition='auto',)])

col1.write(fig)
col2.header(' ')
col2.write('For Pahang state with regressor models, Linear Regression model shows high performance of R2-Score with 0.88. When compared to other regressor models, Linear Regression shows a low errors of MAE and RMSE with 24.84 and 57.22 error respectively. This means that there are an average difference between predict daily cases value and actual daily cases values of 24.84. Thus, Linear Regression performs well in predicting daily cases for Pahang.')
st.write('----------------------------------------------------------------------------------------------------------------------------------------------')

col1, col2 = st.columns(2)
col1.subheader('Kedah')
col1.dataframe(regK)
fig = go.Figure(data=[
    go.Bar(name='R2-Score', x=regK['Model_Name'], y=regK['R2-Score'],text=regK['R2-Score'],textposition='auto',)])

col1.write(fig)
col2.header(' ')
col2.write('For Kedah state with regressor models, Linear Regression model shows high performance of R2-Score with 0.96. When compared to other regressor models, Linear Regression shows a low errors of MAE and RMSE with 43.34 and 82.29 error respectively. This means that there are an average difference between predict Kedah daily cases value and actual Kedah daily cases values of 43.34. Thus, Linear Regression performs well in predicting daily cases for Kedah.')
st.write('----------------------------------------------------------------------------------------------------------------------------------------------')

col1, col2 = st.columns(2)
col1.subheader('Johor')
col1.dataframe(regJ)
fig = go.Figure(data=[
    go.Bar(name='R2-Score', x=regJ['Model_Name'], y=regJ['R2-Score'],text=regJ['R2-Score'],textposition='auto',)])

col1.write(fig)

col2.header(' ')
col2.write('For Johor state with regressor models, Linear Regression and Decision Tree Regression model seems to have the same high performance of R2-Score with 0.88 for both models. On average, Decision Tree gives an average of 69.66 MAE errors while Linear Regression gives 81.80 MAE errors. Therefore, Decision Tree Regression model performs the best when predicting daily cases in Johor.')
st.write('----------------------------------------------------------------------------------------------------------------------------------------------')

col1, col2 = st.columns(2)
col1.subheader('Selangor')
col1.dataframe(regS)
fig = go.Figure(data=[
    go.Bar(name='R2-Score', x=regS['Model_Name'], y=regS['R2-Score'],text=regS['R2-Score'],textposition='auto',)])

col1.write(fig)
col2.header(' ')
col2.write('For Selangor state with regressor models, Linear Regression model shows a high performance of R2-Score with 0.99. When compared to other regressor models, Linear Regression shows a low errors of MAE and RMSE with 116.43 and 190.64 error respectively. This means that there is an average difference between predict Selangor daily cases value and actual Selangor daily cases values of 116.43. However, the model errors seems to be moderately high. Therefore, it is recommended to improve Linear Regression to achieve lower errors. Thus, Linear Regression performs well in predicting daily cases for Selangor.')
st.write('----------------------------------------------------------------------------------------------------------------------------------------------')

st.subheader('To summarize, our experiments shows that Linear Regression have the best performance for predicting new cases in Pahang, Kedah and Selangor. In the case of Johor,we think that Decision Tree Regression produces the best result in predicting new cases although Linear Regression has similar R2-Score. This is because Johor Decision Tree Regression gives a lower Mean Average Error than Linear Regression with 69.66 and 81.80 respectively.')

st.header('Final Conclusion')
st.write('To finish it off, we think that both classification and regression models are good in predicting the new Covid cases. The main difference would be, the desired output. If we want to predict a class label or range of new covid cases, then classification would be the best option. Otherwise, if we want to predict a specific number of new cases for the next day, then regression models would do the trick. Based on our analysis, we found out that for Classification, KNN Classifier works best while Linear Regression produces the best output in regression modelling.')