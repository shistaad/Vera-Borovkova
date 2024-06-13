from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

# Конфігурація підключення до бази даних
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'hotel'

mysql = MySQL(app)

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Hotels")
    hotels = cur.fetchall()
    cur.close()
    return render_template('index.html', hotels=hotels)

@app.route('/rooms/<int:hotel_id>')
def rooms(hotel_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Rooms WHERE hotel_id = %s", (hotel_id,))
    rooms = cur.fetchall()
    cur.close()
    return render_template('rooms.html', rooms=rooms)

@app.route('/book/<int:room_id>', methods=['GET', 'POST'])
def book(room_id):
    if request.method == 'POST':
        user_id = request.form['user_id']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Bookings(user_id, room_id, start_date, end_date, status) VALUES (%s, %s, %s, %s, %s)", (user_id, room_id, start_date, end_date, 'confirmed'))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('index'))
    return render_template('book.html', room_id=room_id)

@app.route('/payment/<int:booking_id>', methods=['GET', 'POST'])
def payment(booking_id):
    if request.method == 'POST':
        amount = request.form['amount']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Payments(booking_id, amount, date, status) VALUES (%s, %s, CURDATE(), %s)", (booking_id, amount, 'paid'))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('index'))
    return render_template('payment.html', booking_id=booking_id)

if __name__ == '__main__':
    app.run(debug=True)
