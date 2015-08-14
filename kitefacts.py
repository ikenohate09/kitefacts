from flask import Flask, render_template
from requests import get
from urllib import urlencode
from bs4 import BeautifulSoup
from json import loads
from re import compile
from random import sample

app = Flask(__name__)
app.debug = True
app.template_folder = "."

@app.route("/")
def home():
	fact = get_random_fact("kite")
	return render_template('home.html', fact=fact)

def search(term):
	query = urlencode({'q': term})
	url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s' % query
	response = get(url)

	return response

def extract_urls(results):

	result_dict = loads(results)
	result_list = result_dict["responseData"]["results"]

	return [item["url"] for item in result_list]

def extract_facts(url):
	content = get(url).text
	soup = BeautifulSoup(content, "html.parser")
	return soup.find_all(text=compile("(?i).* ?kite .*\."))

def get_random_fact(term):
	results = extract_urls(search(term).text)
	picked = sample(results, 1)[0]
	content = extract_facts(picked)
	fact = sample(content, 1)[0]

	return fact

app.run()