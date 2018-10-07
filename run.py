# -*- coding: utf-8 -*-

import connexion
from flask import render_template

# Create the application instance
app = connexion.App(__name__, specification_dir='./')

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
