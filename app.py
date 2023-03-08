from flask import Flask,url_for,request,jsonify,render_template

app=Flask(__name__)

@app.route("/", methods=["POST","GET"])
def testindex():
  return render_template("index.html")


@app.route("/append",methods=['POST'])
def appendtest():
  if (request.method=="POST"):
    first_name=request.form["fname"]
    last_name=request.form["lname"]
    result=first_name+"DhirajDhiraj"+last_name
    print(result)

    return render_template("results.html",result=result)

@app.route("/PostManTesting",methods=['POST'])
def testpostman():
  if (request.method=="POST"):
    nameof=request.json["name"]
    if (nameof=="Dhiraj"):
      return render_template("results.html",result=nameof)
if __name__=="__main__":
  app.run(host="0.0.0.0")