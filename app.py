from flask import Flask,render_template, url_for, request
import spacy
from spacy import displacy
HTML_WRAPPER = """<div style="overflow-x: auto; border: 1px solid #e6e9ef; border-radius: 0.25rem; padding: 1rem">{}</div>"""

from flaskext.markdown import Markdown

nlp = spacy.load('en_core_web_md')

app = Flask(__name__)
Markdown(app)

@app.route('/')
def index():
	return render_template("index.html")

@app.route('/process',methods=["POST"])
def process():
	if request.method == 'POST':
		#choice = request.form['taskoption']
		rawtext = request.json['commentText']
		#print(rawtext)
		doc = nlp(rawtext)
		html = displacy.render(doc,style="ent")
		html = html.replace("\n\n","\n")
		displacy_res = HTML_WRAPPER.format(html)


		entities = dict([(str(x), x.label_) for x in doc.ents])
		list1=list(entities.values())
		results =[]
		for name in set(list1):
			values=[]
			for key, value in entities.items():
				if value==name:
					values.append(key)

			results.append({"name":name,"labels":list1.count(name),"results": values })       
    #print(list1.count(name))
	final_result =[{"display": displacy_res, "summary":results}]
	return final_result


if __name__ == '__main__':
	app.run(debug=True)