from sys import argv
import re

from flask import Flask, render_template
from flask_flatpages import FlatPages
from flask_frozen import Freezer

DEBUG = True
FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION = '.md'

# Monkey-Patching Flatpages for the benefit of Netlify CMS

old_parse = FlatPages._parse
def new_parse(self, content, path):
    new_content = re.sub(r'\s*---\s*(.*?)\s*---\s*', r'\1\n\n', content, flags=re.DOTALL)
    return old_parse(self, new_content, path)
FlatPages._parse = new_parse

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
