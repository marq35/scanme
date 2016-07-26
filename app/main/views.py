from flask import Flask, render_template, session
from . import main

@main.route('/')
def index():
    return render_template('index.html')

@main.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@main.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500