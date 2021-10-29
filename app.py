import os
from flask import Flask  

def create_app():
    app = Flask(__name__)

    app.secret_key = os.urandom( 24 )

    from views import main

    app.register_blueprint(main)

    app.run( host='127.0.0.1', port =443, ssl_context=('micertificado.pem', 'llaveprivada.pem'))

    return app 


if __name__ == '__main__':

    create_app()
