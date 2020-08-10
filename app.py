from flask import Flask, request, render_template
from database import DataBase

app = Flask(__name__)
database = DataBase()
database.setup_db()


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/<string:tag>')
def get(tag):
    data = database.tag_check(tag)
    if data != []:
        return render_template('link.html', url=data[0][1])
    else:
        return render_template('404.html')


@app.route('/new/')
def new_short():
    return render_template('form.html')


@app.route('/new/', methods=['POST'])
def new_short_post():
    alias = request.form['alias']
    url = request.form['url']
    if 'http' not in url:
        url = 'https://' + url
    write = database.write(url, alias)
    if write:
        return render_template('success.html', _alias=alias, _url=url)
    else:
        return render_template('error.html', _alias=alias)


@app.route('/console/<string:data>')
def console(data):
    page = ""
    def field(alias, url): return f"<p><b>{alias}</b> -> {url}</p>"
    if data == "all":
        all_links = database.read_all()
        for links in all_links:
            page += field(links[2], links[1])
        return page
    return render_template('nodata.html')


if __name__ == '__main__':
    app.run()
