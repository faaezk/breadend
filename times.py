import json
import requests
import pandas as pd
from datetime import timedelta
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

def main(days):

    proj_data = get_data("projects")
    projects = [Project(elem['id'], elem['name'], elem['color']) for elem in proj_data]

    # Get file entries
    files_df = pd.read_csv(config.get("TIME_ENTRIES_FP"))
    files_df['tag'] = files_df['tag'].fillna('None')
    files_df['description'] = files_df['description'].fillna('None')
    files_df['start'] = pd.to_datetime(files_df['start'], format="ISO8601", utc=True)
    files_df['start'] = files_df['start'].dt.tz_convert('Australia/Melbourne')
    files_df['stop'] = pd.to_datetime(files_df['stop'], format="ISO8601", utc=True)
    files_df['stop'] = files_df['stop'].dt.tz_convert('Australia/Melbourne')

    now = pd.Timestamp.now(tz='Australia/Melbourne')
    cut_off = now - timedelta(days=days)
    df = df[df['start'] >= cut_off]


    proj_group = df.groupby(['project', 'colour'])['duration'].sum().reset_index()
    graph("Projects", proj_group, proj_group['project'], colours=proj_group['colour'])

    for project in projects:
        if project.name in ['Reading', 'Leisure']:
            tag_group = df[df['project'] == project.name]
            tag_group['tag_desc'] = df['tag'] + ' - ' + df['description']
            tag_group = tag_group.groupby(['tag_desc'])['duration'].sum().reset_index()
            graph(project.name, tag_group, tag_group['tag_desc'])
        else:
            tag_group = df[df['project'] == project.name].groupby(['tag'])['duration'].sum().reset_index()
            graph(project.name, tag_group, tag_group['tag'])
