from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse
import sqlite3

app = FastAPI()

def getcolvo():
    connection = sqlite3.connect('fastapidataset.db')
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS dataset(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    status TEXT,
    desc TEXT,
    priority INTEGER,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    connection.commit()
    cursor.execute("SELECT * FROM dataset")
    rows = cursor.fetchall()
    connection.close()
    return len(rows)

def html(rows1 = [],rows2 = []):
    html = "<h1>Супер-пупер мега проект чтобы взяли на работу на 300к в наносекунду</h1>"
    html += "<h3>Удалить задачу по её id</h3>"
    html += """<form method="post" action="/delete">
        <input type="number" name="item_id" placeholder="id" min="1" required><br><br>
        <button type="submit">Удалить</button><br><br>
    </form>"""
    html += "<h3>Создать задачу</h3>"
    html += """<form method="post" action="/create">
        <input type="text" name="field1" placeholder="Имя" required><br><br>
        <select name="options" required>
            <option value=""disabled selected>Выберите вариант</option>
            <option value="В ожидании">В ожидании</option>
            <option value="Активный">Активный</option>
            <option value="Завершен">Завершена</option>
        </select><br><br>
        <input type="text" name="field3" placeholder="Описание" required><br><br>
        <input type="number" name="field4" placeholder="Приоритет" min="1" required><br><br>
        <button type="submit">Отправить</button><br><br>
    </form>"""
    html += """<form method="post" action="/sorted-by-priority">
            <input type="number" name="n" placeholder="n-самых приоритетных" min="1" required><br><br>
            <button type="submit">Отсортировать топ n самых приоритетных</button><br><br>
        </form>"""
    html += '<a href="/sorted-by-data"><button>Отсортировать по дате создания имеющиеся задачи</button></a>'
    html += '<a href="/sorted-by-name"><button>Отсортировать по имени имеющиеся задачи</button></a>'
    html += '<a href="/sorted-by-status"><button>Отсортировать по статусу имеющиеся задачи</button></a>'
    for row in rows1:
        html += f"<li>id: {row[0]} Имя: {row[1]} Статус: {row[2]} Описание: {row[3]} Приоритетность: {row[4]} Дата-создания: {row[5]}</li>"
    html += f"<h4>Всего задач: {getcolvo()}</h4>"
    html += "<h3>Найти задачу</h3>"
    html += """<form method="post" action="/find">
            <input type="text" name="stroka" placeholder="Поиск" required><br><br>
            <button type="submit">Найти</button><br><br>
        </form>"""
    for row in rows2:
        html += f"<li>id: {row[0]} Имя: {row[1]} Статус: {row[2]} Описание: {row[3]} Приоритетность: {row[4]} Дата-создания: {row[5]}</li>"
    return html

@app.get("/")
def start(q: list = None):
    connection = sqlite3.connect('fastapidataset.db')
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS dataset(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    status TEXT,
    desc TEXT,
    priority INTEGER,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    connection.commit()
    cursor.execute("SELECT * FROM dataset")
    if q is None:
        rows = cursor.fetchall()
        connection.close()
    else:
        rows = q
    return HTMLResponse(content=html(rows))


@app.post("/create")
def create(field1: str = Form(...), options: str = Form(...), field3: str = Form(...), field4: int = Form(...)):
    connection = sqlite3.connect('fastapidataset.db')
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS dataset(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    status TEXT,
    desc TEXT,        
    priority INTEGER,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    cursor.execute("INSERT INTO dataset (name, status, desc, priority) VALUES (?, ?, ?, ?)",(field1, options, field3, field4))
    connection.commit()
    connection.close()
    return RedirectResponse(url="/", status_code=303)

@app.post("/delete")
def delete(item_id: int = Form(...)):
    connection = sqlite3.connect('fastapidataset.db')
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS dataset(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    status TEXT,
    desc TEXT,
    priority INTEGER,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    connection.commit()
    cursor.execute("SELECT * FROM dataset")
    rows = cursor.fetchall()
    f = False
    for row in rows:
        if row[0] == item_id:
            f = True
    if f:
        cursor.execute("DELETE FROM dataset WHERE id=?", (item_id,))
        connection.commit()
        connection.close()
        return RedirectResponse(url="/", status_code=303)
    else:
        return RedirectResponse(url="/", status_code=303)

@app.post("/sorted-by-priority")
def priority(n: int = Form(...)):
    connection = sqlite3.connect('fastapidataset.db')
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS dataset(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    status TEXT,
    desc TEXT,
    priority INTEGER,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    connection.commit()
    cursor.execute("SELECT * FROM dataset ORDER BY priority")
    rows = cursor.fetchall()
    connection.close()
    rows2 = []
    for i in range(n):
        rows2.append(rows[i])
    return HTMLResponse(content=html(rows2))


@app.get("/sorted-by-name")
def name():
    connection = sqlite3.connect('fastapidataset.db')
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS dataset(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    status TEXT,
    desc TEXT,
    priority INTEGER,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    connection.commit()
    cursor.execute("SELECT * FROM dataset ORDER BY name")
    rows = cursor.fetchall()
    connection.close()
    return HTMLResponse(content=html(rows))


@app.get("/sorted-by-status")
def status():
    connection = sqlite3.connect('fastapidataset.db')
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS dataset(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    status TEXT,
    desc TEXT,
    priority INTEGER,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    connection.commit()
    cursor.execute("SELECT * FROM dataset ORDER BY status")
    rows = cursor.fetchall()
    connection.close()
    return HTMLResponse(content=html(rows))


@app.get("/sorted-by-data")
def data():
    connection = sqlite3.connect('fastapidataset.db')
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS dataset(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    status TEXT,
    desc TEXT,
    priority INTEGER,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    connection.commit()
    cursor.execute("SELECT * FROM dataset ORDER BY timestamp")
    rows = cursor.fetchall()
    connection.close()
    return HTMLResponse(content=html(rows))

@app.post("/find")
def find(stroka: str = Form(...)):
    connection = sqlite3.connect('fastapidataset.db')
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS dataset(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    status TEXT,
    desc TEXT,      
    priority INTEGER,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    connection.commit()
    cursor.execute("SELECT * FROM dataset")
    rows = cursor.fetchall()
    connection.close()
    rows2 = []
    for row in rows:
        print(row)
        if (stroka in row[1]) or (stroka in row[3]):
            rows2.append(row)
    return HTMLResponse(content=html(rows,rows2))





