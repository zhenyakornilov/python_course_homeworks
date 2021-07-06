import csv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sales.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


with open('homework3sales.csv') as sales:
    csv_read = list(csv.reader(sales, delimiter=';'))
    new_data = []
    for row in csv_read[1:]:
        value = (row[0], row[1], row[2], row[3])
        new_data.append(value)


class Sales(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    transaction_date = db.Column(db.String, unique=False)
    product = db.Column(db.String(80), unique=False, nullable=False)
    price = db.Column(db.Integer, unique=False, nullable=False)
    payment_type = db.Column(db.String, unique=False, nullable=False)

    def __repr__(self):
        return '<Sales %r>' % self.transaction_date


db.create_all()
for row in new_data:
    sales = Sales(transaction_date=row[0], product=row[1],
                  price=row[2], payment_type=row[3])
    db.session.add(sales)
    db.session.commit()
