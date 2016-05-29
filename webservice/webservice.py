#!/usr/bin/python
# -*- coding: utf-8 -*-

#############################################################################
#    Webservice :                                                           #
#        Module pour .....                                                  #
#                                                                           #
#                                                                           #
#                                                                           #
#                                                                           #
#############################################################################

'''
    FORMAT XML
    -------------------------------------------------------------------------
    <data timestamp=”timestamp_unix”>
        <server>
            <name></name>
            <ip></ip>
            <uptime></uptime>
        </server>
        <cpu>
                <used></used>
        </cpu>
        <ram>
            <total></total>
            <used></used>
        </ram>
        <disks>
            <disk>
                <mnt></mnt>
                <total></total>
                <used></used>
            </disk>
        <disks>
        <swap>
            <total></total>
            <used></used>
        </swap>
        <users>
            <user>
                <name></name>
                <uid></uid>
                <gid></gid>
                <isroot></isroot>
                <gname></gname>
                <login_time></login_time>
            </user>
        </users>
        <processes>
                <count></count>
                <zombies></zombies>
            <greedy>
                <process>
                    <pid></pid>
                    <cpu></cpu>
                    <ram></ram>
                    <command></command>
                </process>
            </greedy>
        </processes>
    </data>
'''
UPLOAD_FOLDER = '/'
ALLOWED_EXTENSIONS = set(['xml'])

#############################################################################
#    Webservice. Classe principale du module.                               #
#############################################################################
from flask import Flask


class Webservice:
    def __init__(self):
	    self.app = Flask(__name__)
            app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
    w=Webservice()
    w.app.run()

if __name__=='__main__':
    main()

