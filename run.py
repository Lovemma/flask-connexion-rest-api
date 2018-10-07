# -*- coding: utf-8 -*-

from flask import render_template

import config

app = config.connex_app

# Read the swagger.yml file to configure the endpoints
app.add_api('swagger.yml')


@app.route('/')
def home():
    """
    This function just responds to the browser ULR
    localhost:8000/
    :return:    the rendered template 'home.html'
    """
    return render_template('home.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
