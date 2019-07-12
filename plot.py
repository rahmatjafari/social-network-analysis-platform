import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib.patches as mpatches

df = pd.read_csv("ABCnews.csv")

new = df["posted_at"].str.split(" ", n = 1, expand = True) 
date = new[0]
time=new[1]

new2 = date.str.split("/", n = 2, expand = True)
year=new2[2] 
month=new2[0]
day=new2[1]

df['year']=year
df['month']=month

new3 = time.str.split(":", n = 1, expand = True)
hour = new3[0]
df['hour']=hour

# =============================================================================
fig0, ax0 = plt.subplots()

link = df[df['post_type']=='link']['year']
status = df[df['post_type']=='status']['year']
photo = df[df['post_type']=='photo']['year']
video = df[df['post_type']=='video']['year']

labels=['link', 'photo', 'status' , 'video']
ax0.hist([link,status,photo,video],5, label=labels)
ax0.legend(prop={'size': 12})
ax0.set_title('Activity Recent History by year')

plt.xlabel('year')
plt.ylabel('number of posts')
plt.show()

# =============================================================================
fig1, ax1 = plt.subplots()

link = df[df['post_type']=='link']['month']
status = df[df['post_type']=='status']['month']
photo = df[df['post_type']=='photo']['month']
video = df[df['post_type']=='video']['month']

labels=['link', 'photo', 'status' , 'video']
ax1.hist([link,status,photo,video],12, label=labels)
ax1.legend(prop={'size': 12})
ax1.set_title('Activity Recent History by year')

month_lst = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
              'August', 'September', 'October', 'November', 'December']
plt.xticks(range(12), month_lst)

plt.xlabel('month')
plt.ylabel('number of posts')
plt.show()

# =============================================================================

count=df.groupby('post_type')['id'].nunique()
# Pie chart
# only "explode" the 2nd slice (i.e. 'Hogs')
explode = (0, 0.1, 0, 0)  
fig2, ax2 = plt.subplots()
ax2.pie(count, explode=explode, labels=count.index, autopct='%1.1f%%',
        shadow=True, startangle=90)

# Equal aspect ratio ensures that pie is drawn as a circle
ax2.axis('equal')  
plt.tight_layout()
plt.show()

# =============================================================================

fig3, ax3 = plt.subplots()

days = ("Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday")

time_format = '%m/%d/%Y %H:%M'
time = [datetime.strptime(i, time_format) for i in df['posted_at']]

weekdays=[]
for i in range(len(time)):
    weekdays.insert(i,days[datetime.date(time[i]).weekday()])
    
df['weekDays']=weekdays

monday = df[df['weekDays']=='Monday']
#monday=pd.Series.to_frame(monday)
id=np.arange(len(monday))
monday['id']=id
monday_count_h=monday.groupby('hour')['id'].nunique()

colors=['blue','orange','green','red']

def draw_pie(ax,ratios=[0.4,0.3,0.3,0.1], X=0, Y=0, size = 1000):
    xy = []
    start = 0.
    for ratio in ratios:
        x = [0] + np.cos(np.linspace(2*math.pi*start,2*math.pi*(start+ratio), 30)).tolist()
        y = [0] + np.sin(np.linspace(2*math.pi*start,2*math.pi*(start+ratio), 30)).tolist()
        xy.append(list(zip(x,y)))
        start += ratio
    for i, xyi in enumerate(xy):
        ax.scatter([X],[Y] , marker=(xyi,0), s=size, facecolor=colors[i])

      
mon_count=[]        
        
for i in range(24):
    mon = monday[monday['hour']==str(i)]
    mon_count.append(mon.groupby('post_type')['id'].nunique())
    
    
w = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
q = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]

tm=['12 am', '1 am', '2 am', '3 am', '4 am', '5 am', '6 am', '7 am', 
    '8 am', '9 am', '10 am', '11 am', '12 pm', '1 pm', '2 pm', '3 pm', 
    '4 pm', '5 pm', '6 pm', '7 pm', '8 pm', '9 pm', '10 pm', '11 pm']

for i in range(24):
    index=int(monday_count_h.index[i])
    summ = mon_count[i].link + mon_count[i].photo + mon_count[i].status + mon_count[i].video
    draw_pie(ax3,[mon_count[i].link/summ, mon_count[i].photo/summ, mon_count[i].status/summ, 
                  mon_count[i].video/summ], q[index], w[i],size=monday_count_h[i]*3)

blue_patch = mpatches.Patch(color='blue', label='link')
orange_patch = mpatches.Patch(color='orange', label='photo')
green_patch = mpatches.Patch(color='green', label='status')
red_patch = mpatches.Patch(color='red', label='video')

plt.legend(handles=[blue_patch,orange_patch,green_patch,red_patch])

plt.xticks(q, tm)
plt.yticks(w, ['monday'])

ax3.set_title('Activity Weekly Distribution')
plt.show()

