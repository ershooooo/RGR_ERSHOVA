from flask import Flask
app = Flask(__name__)

app.register_blueprint(main)



@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        search_gender = request.form['search_gender']
        about = request.form['about']
        photo = request.form['photo']
        user = User(name=name, age=age, gender=gender, search_gender=search_gender, about=about, photo=photo)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('index'))

    users = User.query.all()
    return render_template('index.html', users=users)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Perform user login
        return redirect(url_for('index'))
    else:
        return render_template('login.html')

@app.route('/edit/<int:user_id>', methods=['GET', 'POST'])
def edit(user_id):
    user = User.query.get(user_id)
    if request.method == 'POST':
        user.name = request.form['name']
        user.age = request.form['age']
        user.gender = request.form['gender']
        user.search_gender = request.form['search_gender']
        user.about = request.form['about']
        user.photo = request.form['photo']
        db.session.commit()
        return redirect(url_for('index'))
    else:
        return render_template('edit.html', user=user)

@app.route('/hide/<int:user_id>')
def hide(user_id):
    user = User.query.get(user_id)
    user.hidden = True
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:user_id>')
def delete(user_id):
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        users = User.query.filter_by(name=name, age=age, search_gender=gender).limit(3)
        return render_template('search.html', users=users)
    else:
        return render_template('search.html', users=[])

if __name__ == '__main__':
    app.run(debug=True)