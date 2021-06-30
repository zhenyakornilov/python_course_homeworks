import flask
from flask import Flask
from faker import Faker
import csv
import requests


app = Flask(__name__)


@app.route('/')
def base_page():
    return 'Python course homework №2!'


@app.route('/requirements/')
def show_requirements_file():
    return flask.send_file('requirements.txt')


@app.route('/generate-users/<number>')
def generate_fake_users(number):
    fake = Faker()
    users = {}
    for i in range(int(number)):
        user = fake.name()
        mail = fake.email()
        users[user] = mail

    return users


@app.route('/mean/')
def average_height_and_weight():
    with open("hw.csv", "r") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        counter = 0
        height_sum, weight_sum = 0, 0
        for row in csv_reader:
            height_sum += float(row[' "Height(Inches)"'])
            weight_sum += float(row[' "Weight(Pounds)"'])
            counter += 1

    average_height = round((height_sum / counter) * 2.54, 3)
    average_weight = round((weight_sum / counter) * 0.45359, 3)

    return f'Medium height: {average_height} sm, ' \
           f'Medium weight: {average_weight} kg'


@app.route('/space/')
def show_astronauts_in_space():
    r = requests.get('http://api.open-notify.org/astros.json')
    number_of_astronauts = r.json()['number']

    return f'Number of astronauts in space right now: {number_of_astronauts}'


if __name__ == '__main__':
    app.run(debug=True)
