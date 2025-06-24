from flask import Flask, render_template , request , jsonify
import shortenerModule

app= Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/shorten",methods=['POST'])
def shorten():
    data = request.get_json()
    original_url = data.get('url')
    shortened_url = shortenerModule.url_shortener(original_url)

    if shortened_url:
        return jsonify({"shortened_url": shortened_url})
    else:
        return jsonify({"error": "Failed to shorten URL"}), 400

if __name__=="__main__":
    app.run(port = 5000)