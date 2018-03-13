from sys import argv

from flask import Flask, render_template
from flask_flatpages import FlatPages
from flask_frozen import Freezer

DEBUG = True
FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION = '.md'

app = Flask(__name__)
app.config.from_object(__name__)
pages = FlatPages(app)
freezer = Freezer(app)

@app.route('/robots.txt')
def robots():
    return 'User-agent: *\nDisallow: /'


@app.route('/')
def index():
    return render_template('page.html', page=pages.get('accueuil'))


@app.route('/admin/')
def admin():
    return render_template('admin.html')


@app.route('/admin/config.yml')
def admin_config():
    return render_template('admin-config.yaml')


@app.route('/<path:path>/')
def page(path):
    page = pages.get_or_404(path)
    return render_template('page.html', page=page)


if __name__ == "__main__":
    if len(argv) > 1 and argv[1] == "build":
        freezer.freeze()
    else:
        app.run()
