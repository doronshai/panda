import tarfile, time, requests
import urllib.request, urllib3
from subprocess import Popen, PIPE
from termcolor import colored

# Settings
urllib3.disable_warnings()
url = 'https://s3.eu-central-1.amazonaws.com/devops-exercise/pandapics.tar.gz'
fileName = r"pandapics.tar.gz"
healthUrl="http://localhost:3000/health"

def download_file():
  with urllib3.PoolManager() as http:
      r = http.request('GET', url)
      with open(fileName, 'wb') as fout:
          fout.write(r.data)

def extract_tar(location):
  tar = tarfile.open(fileName)
  tar.extractall(location)
  tar.close()

def start_docker_compose():
  process = Popen(['docker-compose', 'up','-d'], shell=False)
  process.communicate()

def kill_docker_compose():
  killProcess = Popen(['docker-compose', 'down'], shell=False)
  killProcess.communicate()

################################

download_file()
extract_tar("public/images")
start_docker_compose()

# Check if App is Healthy
try:
  time.sleep(2)
  r = requests.get(healthUrl)
  if r.status_code == requests.codes.ok:
    print ("Response code is ", colored(r.status_code, 'green'))
  else:
    print("Healthcheck test", colored('FAILED','red')," since response code is different than 200. Therefore process will exit and Dockers will be stopped")
    kill_docker_compose()
except:
  print("Healthcheck test", colored('FAILED','red'),", Process will exit and Dockers will be stopped")
  kill_docker_compose()
