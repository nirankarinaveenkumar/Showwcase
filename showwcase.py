# -*- coding: utf-8 -*-
"""showwcase.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1_1r50QLd2kt5--EkGwvRXmyafsR5w1d5

# **User Engagement Analysis**
"""

data = pd.read_csv("/content/drive/My Drive/showwcase_sessions.csv")

data.head(5)

"""**Dropping the null values as there are only 3 rows with null values**"""

data.dropna(inplace=True)
data.reset_index(drop=True,inplace=True)

#Converting the login date to date format

data['login_date'] = pd.to_datetime(data['login_date'])

"""**Creating a new Day variable to find trends according to days of week**"""

data['day'] = data['login_date'].dt.weekday

#Creating a function to plot the graphs
def plot_trends(columns):
    days = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
    
    for columns in columns:
        plt.figure(figsize=(6,6))
        plt.plot(days,data.groupby('day')[columns].sum(),color='black',marker="o")
        plt.xlabel("Days")
        plt.ylabel(columns)
        plt.show()

"""**Creating Trends with respect to days**"""

plot_trends(['projects_added','likes_given','comment_given','inactive_status','bug_occured','inactive_duration'])

"""**From the Trends we can see that the projects added, likes given and comments do not follow a linear relationship and increases more towards the weekends**

**Hence we should give offers or provide new features to customers during the weekends as the probability of conversion during that time is more**

# **We can clearly conclude that as the number of session in a day increased the bugs in the system as well as the inactive time increased**

### **But on Mondays we can see more inactive time that means the users normally open up the website and simultaneously do other work as well.**

Let Us analyze the trends according to the week
"""

data['week']= data['login_date'].dt.week

trend = data.groupby(['week'])['projects_added','likes_given','comment_given'].sum()

plt.figure(figsize=(12,8))
plt.plot([40,41,42,43],trend[0:4],marker='o')
plt.xlabel('Week Number')
plt.ylabel("Number of user engagement activites")
plt.legend(trend.columns)

"""**We can see that as the month proceeds towards the end, the engagement also
increases, but you can see that in week 44 engagement is less because there were only 4 days in that particular week**
"""

session_trend = data.groupby('week')['session_id'].count().reset_index(name="week_session")
session_trend

import seaborn as sns
plt.figure(figsize=(12,8))
sns.barplot(x="week",y="week_session",data=session_trend)

bugs_trend = data.groupby('week')['bug_occured'].sum().reset_index(name='week_bugs')
plt.figure(figsize=(12,8))
sns.barplot(x="week",y="week_bugs",data=bugs_trend)

"""# **Hence we can conclude that as the session increases people are more engaged with adding projects, giving likes, comments and hence there are possibility of bug occuring as seen from graph above**"""

trends = data.groupby(['week'])['session_projects_added','session_likes_given','session_comments_given'].sum()

plt.figure(figsize=(12,8))
plt.plot([40,41,42,43],trends[0:4],marker='o')
plt.xlabel('Week Number')
plt.ylabel("Number of user engagement activites")
plt.legend(trends.columns)

"""### **People are more likely to give a like as compared to commenting and adding projects**"""

data['daily'] = data['login_date'].dt.day

trend_daily = data.groupby(['daily'])['session_projects_added','session_likes_given','session_comments_given'].sum()

plt.figure(figsize=(12,8))
plt.plot([*range(0,30)],trend_daily[0:30],marker='o')
plt.xlabel('Week Number')
plt.ylabel("Number of user engagement activites")
plt.legend(trend_daily.columns)

"""## **All user engagements have increased during the end of the month and were more during the start whereas decreased during the mid month.**


1.   The number of projects and comments added were moreover constant
2.   The engagement through likes kept on changing 
3.   Engagement through projects and comments are less as compared to likes given

## **Inactive Duration**
"""

plt.figure(figsize=(12,8))
inac = data.groupby('daily')['inactive_duration'].sum().reset_index()
sns.barplot(x="daily",y="inactive_duration",data=inac)

"""## **Session Duration**"""

plt.figure(figsize=(12,8))
sessn = data.groupby('daily')['session_duration'].sum().reset_index(name="Sessn")
sns.barplot(x="daily",y="Sessn",data=sessn)

"""## **Bug**"""

buggg =  data.groupby('daily')['bug_occured'].sum().reset_index(name="bug")
plt.figure(figsize=(12,8))
sns.barplot(x="daily",y="bug",data=buggg)

"""### **As the number of session increases frequency of bugs is high leading to an increased inactive/idle time of users**

# **Point based system for Engagement**
"""

session_likes_points = (data.groupby(['customer_id'])['session_likes_given'].sum()/data.groupby(['customer_id'])['session_id'].count()).reset_index(name="like")
session_projects_points = (data.groupby(['customer_id'])['session_projects_added'].sum()/data.groupby(['customer_id'])['session_id'].count()).reset_index(name="projects")
session_comments_points = (data.groupby(['customer_id'])['session_comments_given'].sum()/data.groupby(['customer_id'])['session_id'].count()).reset_index(name="comments")
session_bugs_points = (data.groupby(['customer_id'])['bugs_in_session'].sum()/data.groupby(['customer_id'])['session_id'].count()).reset_index(name="bugs")

hue = pd.DataFrame(data['session_duration'].describe())
hue

"""## **Classifying the Session duration according to the percentile wherein**

1.   duration < 25% = 1
2.   duration > 25% and duration < 50% = 2
3.   duration > 50% and duration < 75% = 3
4.   duration > 75% = 4
"""

data['session_points']=0

for i in range(0,data.shape[0]):

    if data['session_duration'][i] <= hue['session_duration']['25%'] :
        data['session_points'][i] = 1
    elif ((data['session_duration'][i] > hue['session_duration']['25%']) & (data['session_duration'][i] <= hue['session_duration']['50%'])):
        data['session_points'][i] = 2
    elif ((data['session_duration'][i] > hue['session_duration']['50%']) & (data['session_duration'][i] <= hue['session_duration']['75%'])):
        data['session_points'][i] = 3
    elif data['session_duration'][i] > hue['session_duration']['75%']:
        data['session_points'][i] = 4

inacti = pd.DataFrame(data['inactive_duration'].describe())
inacti

"""## **Classifying the Session duration according to the percentile wherein**

1.   inactivity < 25% = 1
2.   inactivity > 25% and inactivity < 50% = 2
3.   inactivity > 50% and inactivity < 75% = 3
4.   inactivity > 75% = 4
"""

data['inactive_points']=0

for i in range(0,data.shape[0]):

    if data['inactive_duration'][i] <= inacti['inactive_duration']['25%'] :
        data['inactive_points'][i] = 1
    elif ((data['inactive_duration'][i] > inacti['inactive_duration']['25%']) & (data['inactive_duration'][i] <= inacti['inactive_duration']['50%'])):
        data['inactive_points'][i] = 2
    elif ((data['inactive_duration'][i] > inacti['inactive_duration']['50%']) & (data['inactive_duration'][i] <= inacti['inactive_duration']['75%'])):
        data['inactive_points'][i] = 3
    elif data['inactive_duration'][i] > inacti['inactive_duration']['75%']:
        data['inactive_points'][i] = 4

inactive_points = (data.groupby(['customer_id'])['inactive_points'].mean()).reset_index(name="inactive")

session_points = (data.groupby(['customer_id'])['session_points'].mean()).reset_index(name="session")

final = pd.DataFrame({'Customers' : session_likes_points.customer_id,
 'Projects'      : session_projects_points.projects,
 'Likes'         : session_likes_points.like  ,
 'Comments'      : session_comments_points.comments,
 'bugs'          : session_bugs_points.bugs,
 'session_pts'   : session_points.session,
 'inactive_pts'  : inactive_points.inactive})

final

"""# **User Engagement Analysis**

## **Adding the points from Projects, Likes, Comments, Bugs, Session and Inactive Duration**
"""

final['score'] = final.Projects + final.Likes + final.Comments + final.bugs + final.session_pts - final.inactive_pts

percent_25 = final['score'].describe()[4]

plt.figure(figsize=(12,8))
plt.plot(range(0,len(final)),final.score,color='blue',marker = 'o')
plt.axhline(y=percent_25,color='red')

"""## **Each customers score can be seen above. I have considered the 25 percentile for minimum score. Customers with more than 25 percentile can be considered as those with more engagement as well**

## **Recommendation : User engagement can be increased by decreasing the number of bugs and making the UI smooth for users.**
"""