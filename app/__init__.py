from os import name

from flask import Flask
app = Flask(name)
from app import routes