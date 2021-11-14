import requests
import json

def servercheck():

    counter = 0
    report = ""
    regions = {"ap" : "Asia Pacific", "eu" : "Europe", "kr" : "Korea", "na" : "North America"}

    for elem in regions.keys():
        
        url = f'https://api.henrikdev.xyz/valorant/v1/status/{elem}'

        r = requests.get(url)

        if str(r) == "<Response [204]>":
            break

        john = json.loads(r.text)

        if 'status' in john:
            if john['status'] != '200':
                break
        
        if 'statusCode' in john:
            if john['statusCode'] != 200:
                break
        
        maintenances = len(john['data']['maintenances'])
        incidents = len(john['data']['incidents'])
        counter += maintenances + incidents

        report += f'{regions[elem]}:\nMaintenances - {maintenances}\nIncidents - {incidents}\n'
        report += f'{regions[elem]}:\n{maintenances} maintenances and {incidents} incidents\n'

    if counter == 0:
        return "no maintenances or incidents reported"
        
    return report


print(servercheck())