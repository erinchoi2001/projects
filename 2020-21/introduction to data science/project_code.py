import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from matplotlib import style
style.use('seaborn')

data = pd.read_csv('middleSchoolData.csv')

#%%
# 1: correlation btwn # applications and admissions
q1 = np.corrcoef(data['applications'], data['acceptances'])
# correlation = 0.802
q1_sq = q1[0][1]**2 # R^2 = 0.643

# plot 
plt.scatter(data['applications'], data['acceptances'])
plt.title('Number of Applications vs. Acceptances to HSPHS - '
          + 'R^2 = {:.3f}'.format(q1_sq))
plt.xlabel('Applications to HSPHS')
plt.ylabel('Acceptances to HSPHS')

#%%
# 2: better predictor - # of applications or application *rate*?
# raw # of applications:
q2a = q1[0][1]**2 # R^2 = 0.643

# clean data: missing school size data
data2 = data.copy()
data2 = data2[data2['school_size'].notnull()]
data2 = data2.reset_index(drop=True)

# application rate:
data2['application_rate'] = data2['applications']/data2['school_size']
data2['acceptance_rate'] = data2['acceptances']/data2['school_size']
rate_r = np.corrcoef(data2['application_rate'], data2['acceptance_rate'])
# correlation = 0.697
q2b = rate_r[0][1]**2 # R^2 = 0.485
# it appears that application # is a better predictor.

# plot rates
plt.scatter(data2['application_rate'], data2['acceptance_rate'])
plt.title('Rate of Applications vs. Acceptances to HSPHS - '
          + 'R^2 = {:.3f}'.format(q2b))
plt.xlabel('Rate of Applications to HSPHS')
plt.ylabel('Rate of Acceptances to HSPHS')

#%%
# 3: which school has best *per student* odds of sending someone to HSPHS?
# odds = happening vs not happening ratio. p : ~p

data3 = data.copy()
data3['odds'] = data3['acceptances']/(data3['applications']
                                      -data3['acceptances'])
bestodds = data3['odds'].max()
q3 = data.loc[data3['odds']==bestodds, 'school_name']
# THE CHRISTA MCAULIFFE SCHOOL\I.S. 187 has the best odds

data3['psodds'] = data3['odds']/data3['acceptances']
bestpsodds = data3['psodds'].max()
q3a = data.loc[data3['psodds']==bestpsodds, 'school_name']
# SPECIAL MUSIC SCHOOL if normalized by # of applications

n = data3.shape[0]
data3 = data3.sort_values(by='psodds', ascending=False)

# plot:
plt.bar(np.linspace(1,n,n), data3['psodds'], width=0.9)
plt.title('Per Student Odds of Going to HSPHS')
plt.xlabel('Schools, ordered by decreasing per student odds')
plt.ylabel('Per Student Odds')

#%%
# 4: is there a relationship btwn how students perceive their school (L-Q) and
# how school performs objectively (V-X)?

from sklearn.decomposition import PCA

# clean the rows of interest of the data
data4 = data.copy()
data4 = data4.loc[:,'rigorous_instruction':'trust'.join(data4.loc[:,'student_achievement':'math_scores_exceed'])
 
data4 = data4[data4.loc[:,'rigorous_instruction':'trust'].notnull().all(1)]
data4 = data4[data4.loc[:,'student_achievement':'math_scores_exceed'].notnull().all(1)]

#%%
# 4a: PCA on first 6 factors

data4a = data4.loc[:,'rigorous_instruction':'trust']

zscored_data = stats.zscore(data4a)
 
pca = PCA()
pca.fit(zscored_data)

eig_vals = pca.explained_variance_
loadings = pca.components_
rotated_data1 = pca.fit_transform(zscored_data)
covar_explained = eig_vals/sum(eig_vals)*100

num_classes = len(eig_vals)
plt.bar(np.linspace(1,num_classes,num_classes),eig_vals)
plt.xlabel('Principal component')
plt.ylabel('Eigenvalue')
plt.title('Scree Plot for School Climate Factors PCA')
plt.plot([0,num_classes],[1,1],color='red',linewidth=1) # Kaiser criterion line

#%%
# interpret factors: plot principal components
which_principal_component = 0
pc = which_principal_component+1
plt.bar(np.linspace(1,6,6),loadings[which_principal_component])
plt.xlabel('Columns L-Q')
plt.ylabel('Loading')
plt.title('Loadings for PC {}'.format(pc))

#%%
# 4b: PCA on last 3 factors

data4b = data4.loc[:,'student_achievement':'math_scores_exceed']
zscored_data = stats.zscore(data4b)
pca = PCA()
pca.fit(zscored_data)
eig_vals = pca.explained_variance_
loadings = pca.components_
rotated_data2 = pca.fit_transform(zscored_data)
covar_explained = eig_vals/sum(eig_vals)*100

num_classes = len(eig_vals)
plt.bar(np.linspace(1,num_classes,num_classes),eig_vals)
plt.xlabel('Principal component')
plt.ylabel('Eigenvalue')
plt.title('Scree Plot for Objective Measures of Achievement Factors PCA')
plt.plot([0,num_classes],[1,1],color='red',linewidth=1) # Kaiser criterion line

#%%
# interpret factors: plot principal components
which_principal_component = 0
pc = which_principal_component+1
plt.bar(np.linspace(1,3,3),loadings[which_principal_component])
plt.xlabel('Columns V-X')
plt.ylabel('Loading')
plt.title('Loadings for PC {}'.format(pc))

#%%
# 4c = correlate the two PCs
q4 = np.corrcoef(rotated_data1[:,0], rotated_data2[:,0])
# r = -0.367
# plot:
plt.scatter(rotated_data1[:,0], rotated_data2[:,0])
plt.title('PC: School Climate vs. PC: Objective Measures of Achievement')
plt.xlabel('School Climate')
plt.ylabel('Objective Measures of Achievement')
# weak negative relationship

#%%
# 5: do charter schools have higher average standardized test (ST) scores?
# hypothesis test! use the framework

# H0 = There is no significant difference between the average ST scores of 
# charter and non-charter schools.
# Test: independent samples t-test

# clean, set up data
data5 = data.copy()
data5 = data5.loc[:,'dbn':'school_name'].join(data5.loc[:,'student_achievement'])
data5 = data5[data5['student_achievement'].notnull()]
data5 = data5.reset_index(drop=True)

regschool = data5[0:470]
charter = data5[470:]

meanreg = np.mean(regschool['student_achievement']) # 3.37
meanchart = np.mean(charter['student_achievement']) # 3.63
t1,p1 = stats.ttest_ind(regschool['student_achievement'],
                        charter['student_achievement'])
# t = -3.071
# p = 0.002 < 0.01
# so at the 0.01 significance level, we can reject the H0
# and conclude that charter schools have significantly different
# ST scores than other schools.

# plot bars:
regschool_mean = np.mean(regschool['student_achievement'])
regschool_std = np.std(regschool['student_achievement'])
charter_mean = np.mean(charter['student_achievement'])
charter_std = np.std(charter['student_achievement'])

plt.bar(['Non-charter Schools','Charter Schools'],[regschool_mean, charter_mean])
#        yerr=[regschool_std, charter_std], capsize=10)
plt.title('Student Achievement at Non-charter vs. Charter Schools')
plt.xlabel('Type of School')
plt.ylabel('Average Standardized Test Score')

#%%
# 6: is there any evidence that the availability of material resources 
# (e.g. per student spending or class size) impacts objective measures of 
# achievement or admission to HSPHS?
# correlate spending with achievement 

# spending & class size vs average ST score
data6 = data.copy()
data6 = data6.loc[:,'dbn':'avg_class_size'].join(data6.loc[:,'student_achievement'])
data6 = data6[data6['per_pupil_spending'].notnull()]
data6 = data6[data6['student_achievement'].notnull()]
data6 = data6[data6.dbn != '02M347']

q6a = np.corrcoef(data6['per_pupil_spending'],data6['student_achievement'])
# -0.158 --> -0.218 when outlier removed
q6b = np.corrcoef(data6['avg_class_size'],data6['student_achievement'])
# 0.209

# ... vs acceptance rate
data6a = data.copy()
data6a = data6a.loc[:,'dbn':'avg_class_size'].join(data6a.loc[:,'school_size'])
data6a = data6a[data6a['per_pupil_spending'].notnull()]
data6a['rate'] = data6a['acceptances']/data6a['school_size']
data6a['rate'] = data6a['rate'].fillna(0)
data6a = data6a[data6a.dbn != '02M347']

q6c = np.corrcoef(data6a['per_pupil_spending'],data6a['rate'])
# -0.307 without outlier
q6d = np.corrcoef(data6a['avg_class_size'],data6a['rate'])
# 0.348

# ... vs # of acceptances
q6e = np.corrcoef(data6a['per_pupil_spending'],data6a['acceptances'])
# -0.360 --> -0.356 without outlier
q6f = np.corrcoef(data6a['avg_class_size'],data6a['acceptances'])
# 0.350

# ... vs reading score
data6b = data.copy()
data6b = data6b[data6b['per_pupil_spending'].notnull()]
data6b = data6b[data6b['reading_scores_exceed'].notnull()]
data6b = data6b[data6b['math_scores_exceed'].notnull()]
data6b = data6b[data6b.dbn != '02M347']

q6g = np.corrcoef(data6b['per_pupil_spending'],data6b['reading_scores_exceed'])
# -0.498 --> -0.529 without outlier
q6h = np.corrcoef(data6b['avg_class_size'],data6b['reading_scores_exceed'])
# 0.537

# ... vs math score
q6i = np.corrcoef(data6b['per_pupil_spending'],data6b['math_scores_exceed'])
# -0.485 --> -0.515 without outlier
q6j = np.corrcoef(data6b['avg_class_size'],data6b['math_scores_exceed'])
# 0.558

#%%
# plot 
plt.scatter(data6b['avg_class_size'], data6b['math_scores_exceed'])
plt.title('Average Class Size vs. Math Scores')
plt.xlabel('Average Class Size')
plt.ylabel('Proportion of Math Scores Above State Standards')

#%%
plt.scatter(data6b['per_pupil_spending'], data6b['reading_scores_exceed'])
plt.title('Per Pupil Spending vs. Reading Scores')
plt.xlabel('Per Pupil Spending')
plt.ylabel('Proportion of Reading Scores Above State Standards')

#%%
'''
Spending seems to be negatively correlated with objective measures 
of achievement, while class size is positively correlated with 
objective achievement. This is strange to me... 
You would think more spending along with smaller class sizes leads to 
better results, but both of these correlations point the opposite way.
Correlations with reading/math scores are stronger (in either direction)
than correlations with acceptances (by # or rate) and ST scores.

Strange... I will try a hypothesis test with the factors that
yielded the greatest correlations for each material resource
factor.
'''

#%%
# Do schools with larger classes have different results 
# in math than schools with smaller classes?
# H0: No difference.

data6h = data.copy()
data6h = data6h.loc[:,'dbn':'avg_class_size'].join(data6h.loc[:,'math_scores_exceed'])
data6h = data6h[data6h['avg_class_size'].notnull()]
data6h = data6h[data6h['math_scores_exceed'].notnull()]
data6h = data6h.reset_index(drop=True)

medsize = np.median(data6h['avg_class_size'])
data6h['larger_avg_class_size'] = 0
data6h['larger_avg_class_size'] = (data6h['avg_class_size']>=medsize).astype(int)

larger = data6h.loc[data6h['larger_avg_class_size']==1]
smaller = data6h.loc[data6h['larger_avg_class_size']==0]

# acceptance rate
t5,p5 = stats.ttest_ind(larger['math_scores_exceed'], smaller['math_scores_exceed'])
# t = 13.05, p = 0 (1.897892698546232e-33)
# The p-value is essentially zero. We can reject the null hypothesis.

# plot bars
larger_mean = np.mean(larger['math_scores_exceed'])
smaller_mean = np.mean(smaller['math_scores_exceed'])

plt.bar(['Larger (Above Median)','Smaller (Below Median)'],
        [larger_mean, smaller_mean])
plt.title('Math Scores Exceeding State Expectations Based on Average Class Size')
plt.xlabel('Average Class Size')
plt.ylabel('Proportion of Math Scores Exceeding Standards')

#%%
# Do schools with greater spending per student have 
# different reading score achievements than schools that spend
# less per student?
# H0: No difference.

data6ha = data.copy()
data6ha = data6ha.loc[:,'dbn':'per_pupil_spending'].join(data6ha.loc[:,'reading_scores_exceed'])
data6ha = data6ha[data6ha['per_pupil_spending'].notnull()]
data6ha = data6ha[data6ha['reading_scores_exceed'].notnull()]
data6ha = data6ha.reset_index(drop=True)

medspend = np.median(data6ha['per_pupil_spending'])
data6ha['rich'] = 0
data6ha['rich'] = (data6ha['per_pupil_spending']>=medspend).astype(int)

rich = data6ha.loc[data6ha['rich']==1]
poor = data6ha.loc[data6ha['rich']==0]

# acceptance rate
t6,p6 = stats.ttest_ind(rich['reading_scores_exceed'],poor['reading_scores_exceed'])
# t = -12.31, p = 0 (2.1383053064464824e-30)
# The p-value is essentially zero. We can reject the null hypothesis.

# plot bars
rich_mean = np.mean(rich['reading_scores_exceed'])
poor_mean = np.mean(poor['reading_scores_exceed'])

plt.bar(['Richer (Above Median)','Poorer (Below Median)'],
        [rich_mean, poor_mean])
plt.title('Reading Scores Exceeding State Expectations Based on Per Pupil Spending')
plt.xlabel('Per Pupil Spending')
plt.ylabel('Proportion of Reading Scores Exceeding Standards')

#%%
# 7: what proportion of schools accounts for 90% of all students
# accepted to HSPHS? 
data7 = data.copy()
data7 = data7.sort_values(by='acceptances', ascending=False)
data7 = data7.reset_index(drop=True)
total = sum(data7['acceptances'])
threshold = total*0.9
sum_accept = 0
for i in range(len(data7['acceptances'])):
    sum_accept += data7['acceptances'][i]
    if sum_accept > threshold:
        threshold_index = i
        break
# index = 122,
# so 123 schools account for 90% of all students accepted.
sum_90 = sum(data7['acceptances'][0:123])
proportion_90 = 123/594
# proportion = 0.207 --> 20.7% of schools
# account for 90% of all students accepted.

#%%
# bar graph for #7
# rank-ordered by decreasing # of acceptances to HSPHS.
n = data7.shape[0]
# plot:
plt.bar(np.linspace(1,n,n), data7['acceptances'], width=0.9)
plt.title('Schools, ordered by decreasing number of acceptances to HSPHS')
plt.xlim(-10,n)
plt.xlabel('School rank (most to least acceptances)') 
plt.ylabel('Number of acceptances')  
plt.axvline(x=threshold_index+1, label='90% of acceptances', color='r')
plt.legend()

#%%
# 8: build a model including all factors as to what school characteristics 
# are most important in sending students to HSPHS (acceptance # or rate)
# and achieving high scores on objective measures of achievement (V-W).

from sklearn.decomposition import PCA

# select rows
data8 = data.copy()
data8 = data8.dropna()
data8a = data8.loc[:,'per_pupil_spending':'avg_class_size']
data8b = data8.loc[:,'multiple_percent':'white_percent'].join(data8.loc[:,'asian_percent'])
data8bb = data8.loc[:,'black_percent':'hispanic_percent']
data8c = data8.loc[:,'rigorous_instruction':'trust']
data8d = data8.loc[:,'disability_percent':'ESL_percent']
data8e = data8.loc[:,'student_achievement':'math_scores_exceed']

#%%
# z-score data:
zscored_data = stats.zscore(data8e) #change data #
 
# run the PCA:
pca = PCA()
pca.fit(zscored_data)

# return outputs:
eig_vals = pca.explained_variance_
loadings = pca.components_
rotated_data6 = pca.fit_transform(zscored_data) # change # after rotated_data
covar_explained = eig_vals/sum(eig_vals)*100
# scree plot:
num_classes = len(eig_vals)
plt.bar(np.linspace(1,num_classes,num_classes),eig_vals)
plt.xlabel('Principal component')
plt.ylabel('Eigenvalue')
plt.plot([0,num_classes],[1,1],color='red',linewidth=1)

#%%
# interpret factors: plot principal components
which_principal_component = 0
pc = which_principal_component+1
plt.bar(np.linspace(1,3,3),loadings[which_principal_component]) # change #s
plt.xlabel('Object Achievement Factors') # change to combined variable name
plt.ylabel('Loading')
plt.title('Loadings for PC {}'.format(pc))

#%%
# put all combined factors in one df
df = pd.DataFrame({'applications': data8['applications'],
                   'acceptances': data8['acceptances'],
                   'per_pupil_spending': data8['per_pupil_spending'],
                   'avg_class_size': data8['avg_class_size'],
                   'material_resources': rotated_data2[:,0],
                   'diversity_amw': rotated_data3a[:,0],
                   'diversity_bh': rotated_data3b[:,0],
                   'school_climate': rotated_data4[:,0],
                   'disadvantages': rotated_data5[:,0],
                   'school_size': data8['school_size'],
                   'objective_achievement': rotated_data6[:,0]})

#%%
# multiple regression #1: number of acceptances
style.use('seaborn')
# Descriptives:
D1 = np.mean(df,axis=0) # take mean of each column
D2 = np.median(df,axis=0) # take median of each column
D3 = np.std(df,axis=0) # take std of each column

# Model: All factors
from sklearn import linear_model 
X = np.transpose([df['per_pupil_spending'], df['avg_class_size'],
                  df['diversity_amw'], df['diversity_bh'], 
                  df['school_climate'], df['disadvantages'], 
                  df['school_size']]) # predictors
Y = df['acceptances'] # 
regr1 = linear_model.LinearRegression()
regr1.fit(X,Y) # use fit method 
r_sqr1 = regr1.score(X,Y) # R^2
betas1 = regr1.coef_ # m
y_int1 = regr1.intercept_  # b

# Visualize:
y_hat1 = (betas1[0]*df['per_pupil_spending'] + betas1[1]*df['avg_class_size']
          + betas1[2]*df['diversity_amw'] + betas1[3]*df['diversity_bh'] 
          + betas1[4]*df['school_climate'] + betas1[5]* df['disadvantages'] 
          + betas1[6]*df['school_size'] + y_int1)
plt.plot(y_hat1,df['acceptances'],'o',markersize=7) # acceptances
plt.xlabel('Prediction from model') 
plt.ylabel('Actual number of acceptances')  
plt.title('Predicting Number of Acceptances - R^2: {:.3f}'.format(r_sqr1)) 

#%%
# multiple regression #2: objective measures of achievement

# Model
from sklearn import linear_model 
X = np.transpose([df['per_pupil_spending'], df['avg_class_size'],
                  df['diversity_amw'], df['diversity_bh'], 
                  df['school_climate'], df['disadvantages'], 
                  df['school_size']]) # predictors
Y = df['objective_achievement'] # 
regr2 = linear_model.LinearRegression() 
regr2.fit(X,Y) # use fit method 
r_sqr2 = regr2.score(X,Y) # R^2
betas2 = regr2.coef_ # m
y_int2 = regr2.intercept_  # b

# Visualize: 
y_hat2 = (betas2[0]*df['per_pupil_spending'] + betas2[1]*df['avg_class_size']
          + betas2[2]*df['diversity_amw'] + betas2[3]*df['diversity_bh'] 
          + betas2[4]*df['school_climate'] + betas2[5]* df['disadvantages'] 
          + betas2[6]*df['school_size'] + y_int2)
plt.plot(y_hat2,df['objective_achievement'],'o',markersize=7) # achievement
plt.xlabel('Prediction from model') 
plt.ylabel('Actual achievement')  
plt.title('Predicting Objective Achievement - R^2: {:.3f}'.format(r_sqr2)) 

#%%
# multiple regression #3: number of applications

# Model
from sklearn import linear_model 
X = np.transpose([df['per_pupil_spending'], df['avg_class_size'],
                  df['diversity_amw'], df['diversity_bh'], 
                  df['school_climate'], df['disadvantages'], 
                  df['school_size']]) # predictors
Y = df['applications'] # 
regr3 = linear_model.LinearRegression() 
regr3.fit(X,Y) # use fit method 
r_sqr3 = regr3.score(X,Y) # R^2
betas3 = regr3.coef_ # m
y_int3 = regr3.intercept_  # b

# Visualize:
y_hat3 = (betas3[0]*df['per_pupil_spending'] + betas3[1]*df['avg_class_size']
          + betas3[2]*df['diversity_amw'] + betas3[3]*df['diversity_bh'] 
          + betas3[4]*df['school_climate'] + betas3[5]* df['disadvantages'] 
          + betas3[6]*df['school_size'] + y_int3)
plt.plot(y_hat3,df['applications'],'o',markersize=7) # y_hat, applications
plt.xlabel('Prediction from model') 
plt.ylabel('Actual number of applications')  
plt.title('Predicting Number of Applications - R^2: {:.3f}'.format(r_sqr3)) 

