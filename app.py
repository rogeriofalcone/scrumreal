from flask import Flask
import settings

app = Flask('scrumreal')
app.config.from_object('settings')


