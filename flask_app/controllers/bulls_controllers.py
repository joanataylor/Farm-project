from flask_app.models.bull_model import Bull
from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models import user_model


@app.route("/bulls")
def dashboard():
    if not 'uid' in session:
        flash("access denied")
        return redirect("/")
    results = user_model.User.all_bulls_with_users()
    print(results)
    print(session['uid'])
    return render_template('dashboard.html', results=results)

@app.route("/bull/all")
def all_bulls():
    return render_template('add_bull.html')

@app.route("/videos/")
def all_weather():
    return render_template('video.html')

@app.route("/bull/alls")
def all_bullls():
    results = user_model.User.all_bulls_with_users()
    return render_template('view_all.html', results=results)

@app.route("/bull/color")
def color_bull():
    results = user_model.User.all_bulls_with_color()
    return render_template('view_all.html', results=results)

@app.route("/bull/name")
def name_bull():
    results = user_model.User.all_bulls_with_name()
    return render_template('view_all.html', results=results)

@app.route("/bull/dob")
def dob_bull():
    results = user_model.User.all_bulls_with_dob()
    return render_template('view_all.html', results=results)

@app.route('/bulls/destroy/<int:id>')
def distroy_bulls(id):
    data = {
        "id": id
    }
    bulls = Bull.destroy(data)
    return redirect("/bull/alls")

@app.route('/bulls/display/<int:id>')
def display_bulls(id):
    data = {
        "id": id
    }
    bulls = Bull.get_one(data)
    return render_template('show_bull.html', bulls = bulls)

@app.route('/bulls/edit/<int:id>')
def edit_bulls(id):

    data = {
        "id": id
    }
    result = Bull.get_bull_by_id(data)
    return render_template('edit_bull.html', result = result)


@app.route("/add_bull", methods=["POST"])
def new_bull():

    if not Bull.validates_bull_creation_updates(request.form):
        return redirect("/bull/all")

    data={
        **request.form,
        "user_id": session['uid']
    }
    Bull.save(data)
    return redirect("/bull/alls")

@app.route("/edit_bulls/<int:id>", methods=["POST"])
def updated_bull(id):

    if not Bull.validates_bull_creation_updates(request.form):
        return redirect("/bulls/edit/"+str(id))

    data={
        **request.form,
        "id": id
    }
    Bull.update(data)
    return redirect("/bull/alls")