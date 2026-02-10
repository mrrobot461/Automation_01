from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    #return render_template(home.html)
    pass

if __name__ == "__main__":
    app.run()





C:\Users/Leul/OneDrive/المستندات/Automation/config.yaml