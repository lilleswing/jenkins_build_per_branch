virtualenv jenkins
source jenkins/bin/activate
pip install -r requirements.txt
python clone_master.py settings.json
