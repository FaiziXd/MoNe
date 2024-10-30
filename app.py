from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# In-memory storage for requests
requests = []
is_pending = False

@app.route('/')
def home():
    return render_template('index.html', message="")

@app.route('/submit_request', methods=['POST'])
def submit_request():
    global is_pending
    name = request.form['name']
    description = request.form['description']

    if is_pending:
        return render_template('index.html', message="Your request is pending, wait!")

    requests.append({'name': name, 'description': description})
    is_pending = True  # Set request as pending
    return render_template('index.html', message="Request submitted!")

@app.route('/admin')
def admin():
    return render_template('admin.html', requests=requests)

@app.route('/accept_request/<int:index>')
def accept_request(index):
    global is_pending
    if 0 <= index < len(requests):
        requests.pop(index)  # Remove the accepted request
        is_pending = False  # Reset pending status
        return redirect(url_for('welcome'))  # Redirect to welcome page
    return redirect(url_for('admin'))

@app.route('/reject_request/<int:index>')
def reject_request(index):
    global is_pending
    if 0 <= index < len(requests):
        requests.pop(index)  # Remove the rejected request
        is_pending = False  # Reset pending status
    return redirect(url_for('admin'))

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
