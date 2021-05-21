from os import times
import requests
import urllib3
import os.path as path
import time
import json

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

auth_url = "https://www.strava.com/oauth/token"
activites_url = "https://www.strava.com/api/v3/athletes/23204625/stats"


payload = {
    'client_id': "66386",
    'client_secret': '426f5e748e6f00f8322fb4ccc9d3ea3857b48f6d',
    'refresh_token': 'b0ed53054ca4b77a79caf083afc4a757bc89701a',
    'grant_type': "refresh_token",
    'f': 'json'
}

strava_json = any
filename = r'resources/json_output/strava_info.json'

def is_file_older_than_5_mins(file):
    file_time = path.getmtime(file)
    print((time.time() - file_time)/60)
    return ((time.time() - (60 * 5)) < file_time)

if path.isfile(filename) and is_file_older_than_5_mins(filename):
    with open(filename) as json_file:
     strava_json = json.load(json_file)
else:
    print("Requesting Token...\n")
    res = requests.post(auth_url, data=payload, verify=False)
    access_token = res.json()['access_token']
    print("Access Token = {}\n".format(access_token))

    header = {'Authorization': 'Bearer ' + access_token}
    param = {'per_page': 200, 'page': 1}
    my_dataset = requests.get(activites_url, headers=header, params=param).json()
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(my_dataset, f, ensure_ascii=False, indent=4)
    with open(filename) as json_file:
     strava_json = json.load(json_file)

all_run_totals = strava_json['all_run_totals']
all_run_totals['distance'] = str((all_run_totals['distance'] / 1000)) + 'km';
print(all_run_totals['distance'])

html_string = """
    <div class="strava-widget">
        <table class="strava-stats">
        <tr>
            <th class="caption" colspan="6">Strava Lifetime Stats</th>
        </tr>
        <tr>
            <td class="heading" colspan="2"></td>
        </tr>
        <tr>
            <td>Runs</td> 
            <td><strong>"""+ str(all_run_totals['count']) + """</strong></td>
        </tr>
        <tr>
            <td>Distance</td> 
            <td><strong>"""+ str(all_run_totals['distance']) +"""</strong></td>
        </tr>
        </table>
    </div>
"""
with open("frontend/table.html", "w") as file:
    file.write(html_string)