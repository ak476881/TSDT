import uuid
from flask import Flask, request, redirect, url_for, render_template_string, session

app = Flask(__name__)
app.secret_key = "tsdt-2024-demo"
db = {}


#1

INDEX_HTML = '''
<!doctype html>
<html lang="en">
<head>
  <title>To-Do lists</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    body {
      background: #e9ecef;
      min-height: 100vh;
      margin: 0;
      font-family: 'Segoe UI', Arial, sans-serif;
    }
    .center-box {
      margin: 60px auto;
      background: #f5f7fa;
      border-radius: 12px;
      box-shadow: 0 4px 32px 0 #dde4ea70;
      max-width: 600px;
      min-width: 350px;
      padding: 48px 42px 36px 42px;
      text-align: center;
    }
    h1 {
      color: #23272f;
      font-size: 2.8rem;
      margin-bottom: 32px;
      font-weight: 600;
      letter-spacing: .02em;
    }
    form {
      margin-bottom: 30px;
    }
    input[type=text] {
      width: 78%;
      padding: 12px 14px;
      border: 1px solid #ccd6e0;
      border-radius: 6px;
      font-size: 1.2rem;
      transition: border 0.2s;
      background: #fff;
      outline: none;
    }
    input[type=text]:focus {
      border-color: #86b7fe;
      box-shadow: 0 0 0 1px #228be622;
    }
    button {
      padding: 12px 26px;
      margin-left: 10px;
      font-size: 1.1rem;
      background: #228be6;
      border: none;
      border-radius: 6px;
      color: #fff;
      cursor: pointer;
      font-weight: 500;
      transition: background 0.2s;
    }
    button:hover {
      background: #1971c2;
    }
    table {
      margin: 38px auto 0 auto;
      border-collapse: separate;
      border-spacing: 0;
      width: 100%;
      max-width: 440px;
      background: none;
      box-shadow: none;
    }
    th, td {
      text-align: left;
      padding: 13px 14px;
      font-size: 1.16rem;
      background: #fff;
      border-bottom: 1px solid #e3e8ef;
      border-radius: 0;
    }
    th {
      background: #f1f3f5;
      font-weight: 600;
      color: #228be6;
      border-top: 1px solid #dde4ea;
      font-size: 1.05rem;
    }
    tr:last-child td {
      border-bottom: none;
    }
    .url-tip {
      margin-top: 20px;
      color: #555;
      font-size: 1.02rem;
    }
    .user-url {
      color: #888;
      font-size: 0.97rem;
      margin-left: 8px;
      word-break: break-all;
    }
    @media (max-width: 700px) {
      .center-box { max-width: 98vw; min-width: unset; padding: 22px 3vw 18px 3vw;}
      table { max-width: 97vw;}
      input[type=text] { width: 60vw;}
    }
  </style>
</head>
<body>
  <div class="center-box">
    <h1>{{ h1_text }}</h1>
    <form method="post">
      <input type="text" name="todo" placeholder="Enter a to-do item" autocomplete="off" required>
      <button type="submit">Add</button>
    </form>
    {% if todos %}
      <table>
        <tr><th style="width:2em">#</th><th>To-Do</th></tr>
        {% for t in todos %}
          <tr><td>{{ loop.index }}</td><td>{{ t }}</td></tr>
        {% endfor %}
      </table>
      <div class="url-tip">
        <b>Your URL:</b> <span class="user-url">{{ user_url }}</span>
      </div>
    {% endif %}
  </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_id = session.get('user_id')
        if not user_id:
            user_id = str(uuid.uuid4())
            session['user_id'] = user_id
        todo = request.form['todo'].strip()
        if todo:
            db.setdefault(user_id, []).append(todo)
        return redirect(url_for('user', user_id=user_id))
    session.pop('user_id', None)
    return render_template_string(INDEX_HTML, h1_text="Start a new To-Do list", todos=None, user_url=None)

@app.route('/<user_id>', methods=['GET', 'POST'])
def user(user_id):
    if request.method == 'POST':
        todo = request.form['todo'].strip()
        if todo:
            db.setdefault(user_id, []).append(todo)
        return redirect(url_for('user', user_id=user_id))
    todos = db.get(user_id, [])
    h1 = "Your To-Do list" if todos else "Start a new To-Do list"
    return render_template_string(INDEX_HTML, h1_text=h1, todos=todos, user_url=request.url)

if __name__ == '__main__':
    app.run(debug=True)
