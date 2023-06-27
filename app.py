from flask import Flask,render_template
from scrapper import Scrapper

app = Flask(__name__)


        

url ='https://www.youtube.com/@PW-Foundation/videos'

sc = Scrapper(url)
sc.scrape()
sc.to_csv()

@app.route('/')
def home():
    return render_template('index.html',headings=sc.headings,videos=sc.videos)


if __name__=='__main__':
    app.run()