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
    table = soup.find('div', {'id': 'cases'})
    date_div_element = soup.findAll('div', attrs={"class": "content newtab"})

    for x in date_div_element:
        stats_as_on_date_temp = x.find('p').text.split("Nationals, ")[1]
        stats_as_on_date = stats_as_on_date_temp.replace(")", "")

    state_wise_stats = []
    all_rows = table.find_all('tr')
    # print(all_rows)
    for row in all_rows:
        stat = extract_contents(row.find_all('td'))
        if stat:
            if len(stat) == 5:
                # last row
                #stat = ['', *stat]
                state_wise_stats.append(stat)
            elif len(stat) == 6:
                state_wise_stats.append(stat)

    print(state_wise_stats)
    print(stat[1])
    num_cases = []
    country_states = []
    num_casualties = []
    num_people_cured = stat[2]
    total_casualties = stat[3]
    total_cases = stat[1]
    # total_cases = total_cases1.replace("#", "")
    print(total_cases)
    for i in state_wise_stats:
        num_cases.append(i[2])
        country_states.append(i[1])
        num_casualties.append(i[4])
    print(country_states)
    print("hehe", country_states[-1])
    # state_wise_stats.remove(state_wise_stats[-1])
    # country_states.remove(country_states[-1])
    # num_cases.remove(num_cases[-1])
    # num_casualties.remove(num_casualties[-1])

    for j in country_states:
        if j == country_states[-1]:
            break
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
                           stats_as_on_date=stats_as_on_date)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5002)), debug=True)
