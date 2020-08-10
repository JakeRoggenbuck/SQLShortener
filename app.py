from flask import Flask, send_file, jsonify, request, render_template
from database import DataBase

app = Flask(__name__)
database = DataBase()
database.setup_db()


@app.route('/')
def index():
    return "<h1>no page, cry</h1>"


@app.route('/<string:tag>')
def get(tag):
    data = database.tag_check(tag)
    if data != []:
        return render_template('index.html', url=data[0][1])
    else:
        return "<h1>no page, cry</h1>"


@app.route('/new/<string:new>')
def write(new):
    new = new.split("!")
    new_tag = database.write("https://" + new[0], new[1])
    if new_tag:
        return f"<h1>Yay! {new[0]} is now a page!</h1>"
    else:
        return f"<h1>Yikes, {new[0]} is taken</h1>"


if __name__ == '__main__':
    app.run()
