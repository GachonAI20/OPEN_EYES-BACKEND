from flask import Flask, redirect, render_template, url_for, request
from DB_handler import DBModule
from model import Model

app = Flask(__name__)
app.secret_key = "wjddusdlek!!wjddusdlfkrn!!@"

DB = DBModule()


@app.route("/", methods={"POST", "GET"})
def index():
    M = Model()
    if request.method == 'GET':
        id = str(request.args.get('id'))
    elif request.method == 'POST':
        id = str(request.form['id'])
    path_dlocal, mode, uid, filename = DB.pull(id)
    path_ulocal = path_dlocal.replace("downloads", "uploads")
    print(f"mode={mode}, path_dlocal={path_dlocal}, path_ulocal={path_ulocal}")
    info, summary, error = M.modeling(mode, path_dlocal, path_ulocal)
    DB.push(mode=mode, uid=uid, filename=filename, path_ulocal=path_ulocal, info=info, summary=summary, error=error)
    if error == '': # success
        return '1'
    else:
        return '0'
    # return render_template("base.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)