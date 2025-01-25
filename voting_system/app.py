from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# In-memory storage for candidates and votes
candidates = {}
votes = {}

@app.route('/')
def index():
    return render_template('index.html', candidates=candidates)

@app.route('/add_candidate', methods=['GET', 'POST'])
def add_candidate():
    if request.method == 'POST':
        name = request.form['name']
        if name and name not in candidates:
            candidates[name] = 0
            return redirect(url_for('index'))
    return render_template('add_candidate.html')

@app.route('/vote', methods=['POST'])
def vote():
    name = request.form['candidate']
    if name in candidates:
        candidates[name] += 1
        return redirect(url_for('results'))
    return redirect(url_for('index'))

@app.route('/results')
def results():
    return render_template('results.html', candidates=candidates)

if __name__ == '__main__':
    app.run(debug=True)