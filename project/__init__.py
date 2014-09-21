from flask import Flask

app = Flask("project")
app.secret_key = "SECRET_KEY"

import project.routes
