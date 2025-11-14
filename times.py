import json
import requests
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from requests.auth import HTTPBasicAuth

import config

class Project:
    def __init__(self, id, name, colour):
        self.id = id
        self.name = name
        self.colour = colour
 
def get_data(endpoint):
    workspace_id = config.get("WORKSPACE_ID")
    endpoints = {"me" : "me", "workspaces" : f"workspaces/{workspace_id}",
                 "projects" : f"workspaces/{workspace_id}/projects",
                 "tags" : f"workspaces/{workspace_id}/tags",
                 "time_entries" : "me/time_entries"}
    
    url = f"https://api.track.toggl.com/api/v9/{endpoints[endpoint]}"
    headers = {'content-type': 'application/json'}
    
    r = requests.get(url, headers=headers, auth=HTTPBasicAuth(config.get("TOGGL_KEY"), 'api_token'))
    return json.loads(r.text)

def get_project(projects, id):
    for project in projects:
        if project.id == id:
            return project

def graph(title, df, labels, colours=""):

    if df.empty:
        return

    plt.figure(figsize=(8, 8))
    if title == "Projects":
        plt.pie(df['duration'], labels=labels, autopct = '%.0f%%', colors=colours)
        plt.title("title")
    else:
        plt.pie(df['duration'], labels=labels, autopct = '%.0f%%')
        plt.title(f"Project: {title}")
    
    plt.axis('equal')

    if "/" in title:
        title = title.replace("/", "-")
    
    plt.savefig(f"{config.get('TIME_PLOTS_FP')}/{title}.png", bbox_inches='tight')

def update_file_entries():
    proj_data = get_data("projects")
    projects = [Project(elem['id'], elem['name'], elem['color']) for elem in proj_data]

    # Get entries from API
    entries_data = get_data("time_entries")
    new_entries = []
    for elem in entries_data:
        if elem['duration'] > 0:
            tag = "None" if len(elem['tags']) == 0 else elem['tags'][0]
            project = get_project(projects, int(elem['project_id']))
            new_entries.append({"id" : elem['id'], "project_id" : project.id, "project" : project.name, 
                                "tag" : tag, "description" : elem['description'], "start" : elem['start'], 
                                "stop" : elem['stop'], "duration" : elem['duration'], "colour" : project.colour})
    
    new_df = pd.DataFrame(new_entries)
    new_df["duration"] = pd.to_numeric(new_df["duration"])
    new_df['tag'] = new_df['tag'].replace('', 'None')
    new_df['description'] = new_df['description'].replace('', 'None')
    new_df['start'] = pd.to_datetime(new_df['start'], format="ISO8601", utc=True)
    new_df['start'] = new_df['start'].dt.tz_convert('Australia/Melbourne')
    new_df['stop'] = pd.to_datetime(new_df['stop'], format="ISO8601", utc=True)
    new_df['stop'] = new_df['stop'].dt.tz_convert('Australia/Melbourne')

    # Get file entries
    files_df = pd.read_csv(config.get("TIME_ENTRIES_FP"))
    files_df['tag'] = files_df['tag'].fillna('None')
    files_df['description'] = files_df['description'].fillna('None')
    files_df['start'] = pd.to_datetime(files_df['start'], format="ISO8601", utc=True)
    files_df['start'] = files_df['start'].dt.tz_convert('Australia/Melbourne')
    files_df['stop'] = pd.to_datetime(files_df['stop'], format="ISO8601", utc=True)
    files_df['stop'] = files_df['stop'].dt.tz_convert('Australia/Melbourne')

    # Add new entries to file
    df = pd.concat([new_df, files_df]).drop_duplicates().reset_index(drop=True)
    df = df.sort_values(by=['start']).reset_index(drop=True)
    df.to_csv(config.get("TIME_ENTRIES_FP"), index=False)

    new_entries = len(df) - len(files_df)
    payload = {"username": "The Updater", "content": f'Added {new_entries} time entries'}
    requests.post(config.get("WEBHOOK_URL"), json=payload)

def create_sunburst(start_date=None, end_date=None):

    # Load time entries data
    df = pd.read_csv('/Users/faaezkamal/Code/database/time_tracking/time_entries.csv')
    
    # Convert start column to datetime
    df['start'] = pd.to_datetime(df['start'], utc=True)
    
    # Apply date filters if provided
    if start_date:
        start_dt = pd.to_datetime(start_date, utc=True)
        df = df[df['start'] >= start_dt]
    
    if end_date:
        end_dt = pd.to_datetime(end_date, utc=True)
        df = df[df['start'] <= end_dt]
    
    if df.empty:
        print("No data in the specified date range")
        return
    
    # Fill NaN values
    df['tag'] = df['tag'].fillna(df['project'])
    df['description'] = df['description'].fillna(df['tag'])
    
    # Create title with date range
    title = 'Time Tracking by Project and Tag'
    if start_date or end_date:
        start_str = start_date if start_date else df['start'].min().strftime('%Y-%m-%d')
        end_str = end_date if end_date else df['start'].max().strftime('%Y-%m-%d')
        title += f'<br><sub>{start_str} to {end_str}</sub>'
    
    fig = px.sunburst(
        df,
        path=['project', 'tag', 'description'],
        values='duration',
        color='project',
        color_discrete_map={      
            'General Work': '#d92b2b',
            'Personal Work': '#06a893',
            'Exploration': '#3b81d2',
            'University': '#2da608',
            'Leisure': '#e36a00', 
            'Reading': '#c7af14',
            'Transit': '#525266',
            'Fitness': '#c9806b',
            'People': '#d94182',
            'Islam': '#9e5bd9',
            'Work': '#465bb3'
        },
        title=title
    )
    
    # Add percentage labels
    fig.update_traces(
        textinfo='label+percent entry',
        insidetextorientation='radial',
        texttemplate='%{label}<br>%{percentEntry:.1%}'
    )
    
    total_hours = df['duration'].sum() / 3600
    print(f"Total duration: {total_hours:.1f} hours")
    print(f"Number of entries: {len(df)}")
    
    fig.show()

# create_sunburst()
create_sunburst(start_date='2025-07-01', end_date='2025-07-07')
# create_sunburst(start_date='2025-01-01')