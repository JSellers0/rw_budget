activate_this = "/var/www/flask/rw_budget/env_rw_budget/bin/activate_this.py"
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

import sys
sys.path.insert(0, "/var/www/flask/rw_budget/")

from app import app

application = app
