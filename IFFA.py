from flask import Flask, render_template, request
from DecisionEngine import MaltaDecisionEngine, IrelandDecisionEngine
from MockData import fake_Tax

app = Flask(__name__)



@app.route('/', methods=["GET","POST"])
def login():
    if request.method == "POST":
        MDE = MaltaDecisionEngine()
        # Get a fake dataset
        record = fake_Tax(request.form["number"])        
        path, answer = MDE(record)
        
        return render_template("responseBS.html", data=record, path=path, answer=answer)
        #return render_template("response.html", data=record, path=path, answer=answer)
    
    else: #GET
#        record = fake_Tax(request.form["number"])        
#        path = MaltaDecisionEngine(record)
        return render_template("indexBS.html")
        #return render_template("index.html")
    
    
    
