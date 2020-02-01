from flask import Flask, render_template
#import rospy


app = Flask(__name__)

#routes
@app.route('/')
def dashboard():
    return render_template('dashboard.html')

if __name__ == "__main__":
    app.run()