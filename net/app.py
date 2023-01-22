from flask import Flask, request, render_template
import os
import pickle
import pandas as pd
import numpy as np

top_book=pickle.load(open('top_book','rb'))
app = Flask(__name__)

picFolder = os.path.join('static', 'images')
app.config['UPLOAD_FOLDER'] = picFolder

with open("pickled_folder/dist.pkl","rb") as p:
    dist_obj= pickle.load(p)

with open("pickled_folder/final.pkl","rb") as f:
    final_obj= pickle.load(f)

with open("pickled_folder/book.pkl","rb") as b:
    book_obj= pickle.load(b)

def recommend(book_name):
    # fetching the index of input book
    print(np.where(final_obj.index==book_name))

    num=np.where(final_obj.index==book_name)[0][0]
    recc=pd.DataFrame(sorted(list(enumerate(dist_obj[num])),key=lambda x:x[1],reverse=True)[1:6])
    recommended_book=[]
    books_urls=[]
    for i in recc[0]:
        b_name=final_obj.index[i]
        img_url = book_obj.loc[book_obj["Book-Title"] == b_name, :][["Image-URL-M"]]
        img_url = img_url.iloc[0, :].values[0]
        recommended_book.append(b_name)
        books_urls.append(img_url)

    return recommended_book,books_urls


@app.route('/',methods =["GET", "POST"])
def index():

    pic1= os.path.join(app.config['UPLOAD_FOLDER'], 'logo.png')

    return render_template('index.html', user_image=pic1,
                           book_name =list(top_book['Book-Title'].values),
                           author = list(top_book['Book-Author'].values),
                           year = list(top_book['Year-Of-Publication'].values),
                           image = list(top_book['Image-URL-M'].values),

                           )

@app.route('/recommended_books',methods =["GET", "POST"])
def book_recommendation():
    if request.method == "POST":
        book_needed = request.form.get("rec_book")


    recommended_books,books_urls=recommend(book_needed)
    pic1 = os.path.join(app.config['UPLOAD_FOLDER'], 'logo.png')
    return render_template('recommended_books.html', user_image=pic1,
                           rec_book_name=recommended_books,
                           # author = list(top_book['Book-Author'].values),
                           # year = list(top_book['Year-Of-Publication'].values),
                           image = books_urls,

                           )

if __name__=='__main__':
    app.run(debug=True)
