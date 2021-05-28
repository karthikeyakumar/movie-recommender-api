import pickle
from flask import Flask
from flask import request,jsonify,render_template
import pandas as pd

filename = "finalized_model.sav"
cosine_sim = pickle.load(open(filename, 'rb'))
maindf=pd.read_csv("maindf.csv")
updf=pd.read_csv("updateddf.csv")
app = Flask(__name__)
titles = maindf['movie']
links=maindf['link']
indices = pd.Series(maindf.index, index=titles)
def get_cosines(a,n):
    print(a,n,"get_cosines")
    out=[]
    for title in a:
        idx = indices[title]
        try:
            if len(idx)>1:
                idx=idx[-1]
        except:
            idx=idx
        out.extend( list(enumerate(cosine_sim[idx])))
    out = sorted(out, key=lambda x: x[1], reverse=True)
    return out[len(a):(int(n)+len(a))]

@app.route("/")
def main():
    return render_template('index.html')

@app.route("/recommend")
def recommend():
    title = request.args.get('movie')
    title=title.split(",")
    number= request.args.get("number")
    if number is None:
        number=10
    similar_scores=get_cosines(title,int(number))
    total=sum([i[1] for i in similar_scores])
    output = []
    for index,k in similar_scores:
        output.append({"title":titles.iloc[index],"link":links.iloc[index],"percentage":(k/total)*100,"images":{"image1":str(updf["0"].iloc[index]),"image2":str(updf["1"].iloc[index])}})
    return jsonify(output)
@app.route("/genres")
def genre():
    title = request.args.get('genres')
    out=[]
    for k,genres in enumerate(maindf['genre']):
        if title in genres:
            out.append({"movie":titles.iloc[k],"genres":genres,"cast":maindf['cast'].iloc[k].split(","),"images":{"image1":str(updf["0"].iloc[k]),"image2":str(updf["1"].iloc[k])}})
    return (jsonify(out))

if __name__=="__main__":
    app.run(debug=True)
    

#"images":{"image1":str(updf["0"].iloc[index]),"image2":str(updf["1"].iloc[index])}