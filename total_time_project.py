#####################################################################################################
#  Total time spent working on the project (including all the dead ends :D) based on my Toggl tracker
#####################################################################################################

import pandas as pd
import matplotlib.pyplot as plt


def format_time(pct, allvals):
    '''Format time labels for the chart as HH:MM'''
    total = sum(allvals)
    val = pct * total / 100.0
    h = int(val // 60)
    m = int(val % 60)
    return f'{h:02d}:{m:02d}'


# CALC TOTAL TIMES FOR THE PROJECT TASKS

# Read data
df = pd.read_csv("data/_toggl_proj_stats.csv", encoding='utf-8')

# Convert all times in the Duration column to timedelta
df['Duration'] = pd.to_timedelta(df['Duration'])

# Only keep records for 'DA Project':
df = df[df['Description'].str.contains('da project', case=False, na=False)]

# Calc total time for each category of tasks that I tracked:
tasks = ['ADMIN', 'BLOG', 'DATA CHECK', 'DATA SEARCH', 'DATA TRANSFORM', 'PRES', 'PY', 'VIZ', 'ZOOM']
tasks_minutes = {}

total_proj_min = 0
for task in tasks:
    df_task = df[df['Description'].str.contains(task, case=False, na=False)]
    time = df_task['Duration'].sum()

    # Convert time to minutes
    total_minutes = int(time.total_seconds()) // 60    
    tasks_minutes[task.capitalize()] = total_minutes
    total_proj_min += total_minutes

###################

# BUILD A PIE CHART

# Get labels and values
labels = ['Admin', 'Blog', 'Data Validation', 'Data Search', 'Cleaning &\n Transformations', 'Presentation', 'Python (Streamlit)', 'Vizzes', 'Zoom']
# labels = list(tasks_minutes.keys())
wdgs = list(tasks_minutes.values())

# Build the chart
fig, ax = plt.subplots()
wedges, texts, autotexts = ax.pie(
                                wdgs, # values for the wedges
                                labels=labels,
                                autopct=lambda pct: format_time(pct, wdgs), # nice formatting for my times
                                startangle=40, # angle of the first slice
                                wedgeprops=dict(width=0.6), # hole in the middle for the donut
                                pctdistance=0.75, # move percentage labels further out
                                colors=['#c45161', '#e094a0', '#f2b6c0', '#f2dde1', '#cbc7d8', '#8db7d2', '#5e81a9', '#646594', '#a1a1bc'], # pretty wedge colors
                                textprops={'color': '#303030'} # text color
                                )

# Catchy title ;)
plt.title('DA Project Stats', fontsize=24, fontweight='bold', color='#616161', y=1.1)

# Equal aspect ratio = pie is a circle
ax.axis('equal')

# Add extra label in the middle with total time
h = total_proj_min // 60
m = total_proj_min % 60
total_proj_time = f'{h:02}:{m:02}'


total_time_label = f'TOTAL TIME\n{total_proj_time}'
ax.text(0, 0, total_time_label, fontsize=10, fontweight='bold', color='#505050', ha='center', va='center')

# Adjust the position of the subplot so the entire header is visible
plt.subplots_adjust(top=0.8, bottom=0.1)

# Display the chart
plt.show()