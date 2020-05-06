from typing import List, Dict
import simplejson as json
from flask import Flask, request, Response, redirect
from flask import render_template
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor

app = Flask(__name__)
mysql = MySQL(cursorclass=DictCursor)

app.config['MYSQL_DATABASE_HOST'] = 'db'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_DB'] = 'CarsDB'
mysql.init_app(app)


@app.route('/', methods=['GET'])
def index():
    user = {'username': 'Arif Project'}
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblFordImport')
    result = cursor.fetchall()
    return render_template('index.html', title='Home', user=user, cars=result)


@app.route('/view/<int:car_id>', methods=['GET'])
def record_view(car_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblFordImport WHERE id=%s', car_id)
    result = cursor.fetchall()
    return render_template('view.html', title='View Form', car=result[0])


@app.route('/edit/<int:car_id>', methods=['GET'])
def form_edit_get(car_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblFordImport WHERE id=%s', car_id)
    result = cursor.fetchall()
    return render_template('edit.html', title='Edit Form', car=result[0])


@app.route('/edit/<int:car_id>', methods=['POST'])
def form_update_post(car_id):
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('Year'), request.form.get('Mileage'), request.form.get('Price'), car_id)
    sql_update_query = """UPDATE tblFordImport t SET t.Year= %s, t.Mileage = %s, t.Price = %s WHERE t.id = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/cars/new', methods=['GET'])
def form_insert_get():
    return render_template('new.html', title='New Car Form')


@app.route('/cars/new', methods=['POST'])
def form_insert_post():
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('Year'), request.form.get('Mileage'), request.form.get('Price'))
    sql_insert_query = """INSERT INTO tblFordImport (Year, Mileage, Price) VALUES (%s, %s,%s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/delete/<int:car_id>', methods=['POST'])
def form_delete_post(car_id):
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM tblFordImport WHERE id = %s """
    cursor.execute(sql_delete_query, car_id)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/api/v1/cars', methods=['GET'])
def api_browse() -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblFordImport')
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/cars/<int:car_id>', methods=['GET'])
def api_retrieve(car_id) -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblFordImport WHERE id=%s', car_id)
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/cars/<int:car_id>', methods=['PUT'])
def api_edit(car_id) -> str:
    cursor = mysql.get_db().cursor()
    content = request.json
    inputData = (content['Year'], content['Mileage'], content['Price'])
    sql_update_query = """UPDATE tblFordImport t SET t.Year = %s, t.Mileage = %s, t.Price = %s WHERE t.id = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    resp = Response(status=201, mimetype='application/json')
    return resp


@app.route('/api/v1/cars/', methods=['POST'])
def api_add() -> str:
    content = request.json
    cursor = mysql.get_db().cursor()
    inputData = (content['Year'], content['Mileage'], content['Price'])
    sql_insert_query = """INSERT INTO tblFordImport (Year,Mileage,Price) VALUES (%s, %s,%s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    resp = Response(status=201, mimetype='application/json')
    return resp


@app.route('/api/cars/<int:car_id>', methods=['DELETE'])
def api_delete(car_id) -> str:
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM tblFordImport WHERE id = %s """
    cursor.execute(sql_delete_query, car_id)
    mysql.get_db().commit()
    resp = Response(status=210, mimetype='application/json')
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
