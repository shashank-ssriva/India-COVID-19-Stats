# Import the necessary modules
import os
from flask import Flask, render_template, json, request
import requests
import urllib.request
app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def main():
    with urllib.request.urlopen("https://api.apify.com/v2/key-value-stores/toDWvRj1JpTXiM8FF/records/LATEST?disableRedirect=true") as url:
        data = json.loads(url.read().decode())
        total_cases = data['totalCases']
        num_people_cured = data['recovered']
        total_casualties = data['deaths']
        stats_as_on_date = data['lastUpdatedAtApify'] 
        regionData = data['regionData'] 
    print("Total number of confirmed cases in India\n ", total_cases)
    print("Total number of deaths in India\n ", total_casualties)
    print("Total number of people who have been recovered in India\n ", num_people_cured)
    split_string = stats_as_on_date .split("T", 1)

    stats_as_on_date = split_string[0]
    #print(stats_as_on_date)
    state_wise_stats = []
    state_wise_cases = [['stateName' , 'totalInfected' , 'recovered' , 'deceased']]
    state_wise_totalInfected = []
    state_wise_deceased = []
    covidData = []
    num_cases = []
    country_states = []
    num_casualties = []
    num_cured = []
    #covidData.append(state_wise_cases)
    objectCount = 0
    state_wise_stats.append(regionData)
    #print(state_wise_stats)
    #state_wise_activeCases = []
    #state_wise_activeCases = state_wise_stats[0][1]
    #print(state_wise_activeCases)

    #region = data['regionData'][0]['region']  
    #print(region)

    #int id = jsonObj.getInt("id");
    for i in data['regionData']:
        stateName = data['regionData'][objectCount]['region']  
        totalInfected = data['regionData'][objectCount]['totalInfected']  
        recovered = data['regionData'][objectCount]['recovered']
        deceased = data['regionData'][objectCount]['deceased']    
        #state_wise_cases.append(stateName)
        #state_wise_cases.append(totalInfected)
        #state_wise_cases.append(recovered)
        state_wise_cases.append([stateName, totalInfected, recovered, deceased])
        state_wise_totalInfected.append([stateName, totalInfected])
        state_wise_deceased.append([stateName, deceased])
        num_cured.append(recovered)
        num_cases.append(totalInfected)
        country_states.append(stateName)
        num_casualties.append(deceased)
        objectCount +=1
    covidData.append(state_wise_cases)    
    #print(state_wise_totalInfected)
    #print(state_wise_deceased)
    for record in covidData:
        for x in record:
                print(x),
        print

    for element in state_wise_totalInfected:
        element[1] = int(element[1])
    result1 = max(state_wise_totalInfected, key=lambda x: x[1])
    print("State with maximum cases:\n ", result1)
    state_with_max_cases = result1[0]
    max_cases = result1[1]

    for element in state_wise_deceased:
        element[1]=int(element[1])
    result2 = max(state_wise_deceased, key = lambda x: x[1])
    print("State with maximum number of deaths:\n ", result2)
    state_with_max_casualties = result2[0]
    max_casualties = result2[1]
    #print(state_with_max_cases)

    return render_template('index.html', country_states = country_states,
        num_cases= num_cases, num_casualties = num_casualties,
        num_people_cured = num_people_cured,
        total_casualties = total_casualties,
        total_cases = total_cases,
        max = max_cases, state_with_max_cases = state_with_max_cases,
        max_casualties = max_casualties,
        state_with_max_casualties = state_with_max_casualties,
        num_cured = num_cured, stats_as_on_date = stats_as_on_date)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5002)), debug=True)
