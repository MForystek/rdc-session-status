import threading
import subprocess

from flask import Flask
from flask_restful import Resource, Api
from waitress import serve
from infi.systray import SysTrayIcon

def get_powershell_path():
    process = subprocess.Popen("where powershell", shell=True,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    stdout, stderr = stdout.decode('utf-8'), stderr.decode('utf-8')
    powershell_path = stdout.strip()
    return powershell_path

def get_remote_user_status(powershell_path):
    process = subprocess.Popen(f"{powershell_path} quser", shell=True,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    stdout, stderr = stdout.decode('utf-8'), stderr.decode('utf-8')
    return stdout

def parse_status(status):
    status = status.replace('IDLE TIME', 'IDLE_TIME') \
                   .replace(' AM', '').replace(' PM', '')
    lines = status.split('\n')
    lines = [line for line in lines if line]
    headers = lines[0].split()
    data = [line for line in lines[1:] if 'rdp-tcp' in line.lower()]
    data = [line.split() for line in data]
    sessions = [{headers[i]: line[i] for i in range(len(headers))} for line in data]    
    return sessions

class RMStatus(Resource):
    def get(self):
        powershell_path = get_powershell_path()
        status = get_remote_user_status(powershell_path)
        sessions = parse_status(status)
        return {'sessions' : sessions} if sessions else {'sessions': 'No active sessions'}
    
def run_flask():
    flask_app = Flask(__name__)
    api = Api(flask_app)    
    api.add_resource(RMStatus, '/')
    serve(flask_app, host="0.0.0.0", port=2137)
    
    
flask_thread = threading.Thread(target=run_flask)
flask_thread.daemon = True
flask_thread.start()

systray = SysTrayIcon("sync.ico", "Session Status", None)
systray.start()