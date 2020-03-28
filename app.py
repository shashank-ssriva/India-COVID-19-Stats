# Import the necessary modules
import os
from flask import Flask, render_template, json, request
from bs4 import BeautifulSoup
import requests
app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def main():
    def extract_contents(row): return [x.text.replace('\n', '') for x in row]
    URL = 'https://www.mohfw.gov.in/'
    response = requests.get(URL).content
    soup = BeautifulSoup(response, 'html.parser')
    state_wise_stats = []
    all_rows = soup.find_all('tr')
    for row in all_rows:
        stat = extract_contents(row.find_all('td'))
        if stat:
            if len(stat) == 5:
                # last row
                stat = ['', *stat]
                state_wise_stats.append(stat)
            elif len(stat) == 6:
                state_wise_stats.append(stat)

    num_cases = []
    country_states = []
    num_casualties = []
    num_people_cured = state_wise_stats[-1][4]
    total_casualties = state_wise_stats[-1][5]
    total_cases1 = state_wise_stats[-1][2]
    total_cases = total_cases1.replace("#", "")
    for i in state_wise_stats:
        num_cases.append(i[2])
        country_states.append(i[1])
        num_casualties.append(i[5])
        #num_people_cured.append(i[4])

    state_wise_stats.remove(state_wise_stats[-1])
    country_states.remove(country_states[-1])
    num_cases.remove(num_cases[-1])
    num_casualties.remove(num_casualties[-1])
    #num_people_cured.remove(num_people_cured[-1])

    print(num_people_cured)

    for j in country_states:
        if j   == country_states[-1]:
            break
    max = 0
    for j in num_cases:
        if j == num_cases[-1]:
            break
        k = j
        k = int(k)
        if k > max:
            max = k
            max_value_index = num_cases.index(j)
    state_with_max_cases = country_states[max_value_index]

    max_casualties = 0
    #max_casualties_value_index = 0
    for j in num_casualties:
        print(j[0])
    print("last element", country_states[-1])    
    for j in num_casualties:
        #if j == num_casualties[-1]:
            #break
        k = j
        k = int(k)
        if k >= max_casualties:
            max_casualties = k
            print("max casualties..........inner block", max_casualties)
            print("iteration number", j) 
            max_casualties_value_index = num_casualties.index(j)
    print("max casualties", max_casualties)    
    
    state_with_max_casualties = country_states[max_casualties_value_index]
    print("state", state_with_max_casualties)
    '''performance = []
for row in stats :
	performance.append(int(row[2]) + int(row[3]))
#print(performance)'''

    return render_template('index.html', country_states=country_states,
                           num_cases=num_cases, num_casualties=num_casualties, num_people_cured=num_people_cured,
                           total_casualties=total_casualties, total_cases=total_cases, max=max, state_with_max_cases=state_with_max_cases,
                           max_casualties=max_casualties, state_with_max_casualties=state_with_max_casualties)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5002)))