#!/usr/bin/python
# -*- coding: utf-8 -*-

#############################################################################
#    Webservice :                                                           #
#        Module qui crée un Webservice avec Flask, pour pouvoir réaliser    #
#        la communication entre plusieurs machines distantes.               #
#                                                                           #
#############################################################################


UPLOAD_FOLDER = 'data/'
ALLOWED_EXTENSIONS = set(['xml'])



#############################################################################
#    Webservice. Classe principale du module.                               #
#############################################################################
from flask import Flask


class Webservice:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

        @self.app.route("/",methods=['GET', 'POST'])
        def hello():
            return "Hello World!"

        @self.app.route("/upload")
        def upload_file():
            if request.method == 'POST':
                file = request.files['file']
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    return redirect(url_for('uploaded_file',filename=filename))
            return '''
                    <!doctype html>
                    <title>Upload fichier</title>
                    <h1>upload fichier data.xml</h1>
                '''


#############################################################################
#    Main pour tester le module.                                            #
#############################################################################

def main():
    try:
        w=Webservice()
        w.app.run()

    except Exception, e:
        print "Webservice : ", e


if __name__=='__main__':
    main()

