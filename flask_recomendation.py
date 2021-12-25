from flask import Flask, redirect, url_for, render_template, request, session
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import LabelEncoder

da = pd.read_csv("Github_data.csv")
encoder=LabelEncoder()
da.url_id=encoder.fit_transform(da.url_id)
columns = ["topic", "user", "star1","fork1", "watch1", "topic_tag","commits"]

def combined_feature(data):
  features = []
  for i in range(0, data.shape[0]):
    features.append(data["topic"][i] +" "+ data["user"][i] +" "+ str(data["star1"][i]) +" "+str(data["fork1"][i]) +" "+str(data["watch1"][i]) +" "+data["topic_tag"][i]+" "+data["commits"][i] ) 
  return features

da["combined"] = combined_feature(da)
cm = CountVectorizer().fit_transform(da["combined"])
cs = cosine_similarity(cm)

def recom(prname):
    url_id = da[da.name == prname]["url_id"].values[0]
    scores = list(enumerate(cs[url_id]))
    sorted_scores = sorted(scores, key=lambda x:x[1], reverse = True)
    print("5 recomended projects to "+prname+"are : \n")
    j=0;
    
    final_list = []
    
    for i in sorted_scores:
      project_name = da[da.url_id == i[0]]["name"].values[0]
      reco_url = da[da.url_id ==i[0]]["url"].values[0]
      user_name = da[da.url_id == i[0]]["user"].values[0]
      description = da[da.url_id == i[0]]["discription_text"].values[0]
      final_list.append(project_name)
      final_list.append(user_name)
      final_list.append(description)
      final_list.append(reco_url)
      
      j = j+1
      if j>=6:
           break
    return final_list
#result = recom(project)

app = Flask(__name__)

app.secret_key = "heyy"

@app.route("/", methods=["POST", "GET"])
def search():
    if request.method == "POST":
        ip = request.form["fname"]
        recoms= recom(ip)
        session["home"] = recoms
        session["ip"] = ip
        return redirect(url_for("home"))
    else:
        return render_template("search.html")

@app.route("/result")
def home():  
    if "home" in session:
        home = session["home"]
        ip = session["ip"]
        return render_template("index.html", content=home, pro_name=ip)
    else:
        return (url_for("search"))
     
if __name__ == "__main__":
    app.run()