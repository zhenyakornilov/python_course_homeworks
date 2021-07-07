import csv
from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sales.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

with open('homework3sales.csv') as sales:
    csv_read = list(csv.reader(sales, delimiter=';'))
    sales_data = []
    for row in csv_read[1:]:
        datetime_obj = datetime.strptime(row[0], '%m/%d/%Y %H:%M')
        value = (datetime_obj, row[1], row[2], row[3])
        sales_data.append(value)


class Sales(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    transaction_date = db.Column(db.DateTime, unique=False, nullable=False)
    product = db.Column(db.String(80), unique=False, nullable=False)
    price = db.Column(db.Integer, unique=False, nullable=False)
    payment_type = db.Column(db.String, unique=False, nullable=False)

    def __repr__(self):
        return '<Sales %r>' % self.transaction_date


# db.create_all()
# for row in sales_data:
#     sales = Sales(transaction_date=row[0], product=row[1],
#                   price=row[2], payment_type=row[3])
#     db.session.add(sales)
#     db.session.commit()


price_sum = db.session.query(db.func.sum(Sales.price),
                             db.func.strftime('%Y-%m-%d', Sales.transaction_date)).\
    group_by(db.func.strftime('%Y-%m-%d', Sales.transaction_date)).all()

sums_dict = {}
for row in price_sum:
    sums_dict.update({row[1]: row[0]})
print(sums_dict)


@app.route("/")
def main_page():
    return "Python course homework №3!"


@app.route("/summary")
def show_sums_of_transactions():
    return sums_dict


if __name__ == "__main__":
    app.run()
