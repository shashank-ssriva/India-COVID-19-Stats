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
    table = soup.find('div', {'class': 'data-table table-responsive'})
    date_div_element = soup.findAll('div', attrs={"class": "status-update"})
    #print(date_div_element)

    for x in date_div_element:
        stats_as_on_date = x.find('h2').text.strip("COVID-19 INDIA")
    #print(stats_as_on_date)
        
    state_wise_stats = []
    all_rows = table.select('tbody tr')
    #print(all_rows)
    for row in all_rows:
        stat = extract_contents(row.find_all('td'))
        #print("STAT", stat)
        state_wise_stats.append(stat)

    print(state_wise_stats)
    print("-----")
    print(state_wise_stats[0])
    num_cases = []
    country_states = []
    num_casualties = []
    num_cured = []
    num_people_cured = state_wise_stats[-3][2]
    #print(state_wise_stats[-1])
    total_casualties = state_wise_stats[-3][3]
    total_cases_temp = state_wise_stats[-3][1]
    print(total_cases_temp)
    total_cases = total_cases_temp.replace("*", "")

    #state_wise_stats.remove(state_wise_stats[0])
    #print("new list", state_wise_stats)

    #num_elements_to_remove = 1
    #new_state_wise_stats_list = state_wise_stats[: -num_elements_to_remove or None]
    #del new_state_wise_stats_list[-3]
    state_wise_stats = state_wise_stats[: len(state_wise_stats) -3]
    #print("hehe")
    #for i in new_state_wise_stats_list:
    for i in state_wise_stats:
        print("hehe", i)
        num_cases.append(i[2])
        country_states.append(i[1])
        num_casualties.append(i[4])
        num_cured.append(i[3])

    #print(country_states)
    #print("hehe", country_s
    #state_wise_stats.remove(state_wise_stats[-1])
    #country_states.remove(country_states[-1])
    #num_cases.remove(num_cases[-1])
    #num_casualties.remove(num_casualties[-1])


    max = 0
    max_value_index = 0
    for j in num_cases:
        k = j
        k = int(k)
        if k > max:
            max = k
            max_value_index = num_cases.index(j)
    state_with_max_cases = country_states[max_value_index]

    max_casualties = 0

    for j in num_casualties:
        k = j
        k = int(k)
        if k >= max_casualties:
            max_casualties = k
            max_casualties_value_index = num_casualties.index(j)

    state_with_max_casualties = country_states[max_casualties_value_index]

    return render_template('index.html', country_states=country_states,
                           num_cases=num_cases, num_casualties=num_casualties,
                           num_people_cured=num_people_cured,
                           total_casualties=total_casualties,
                           total_cases=total_cases,
                           max=max, state_with_max_cases=state_with_max_cases,
                           max_casualties=max_casualties,
                           state_with_max_casualties=state_with_max_casualties,
                           stats_as_on_date=stats_as_on_date, num_cured=num_cured)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5002)), debug=True)
