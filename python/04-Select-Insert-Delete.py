>>> from yourapp import User
>>> me = User('admin', 'admin@example.com')
>>> db.session.add(me)
>>> db.session.commit()

>>> me.id
1

>>> db.session.delete(me)
>>> db.session.commit()

>>> peter = User.query.filter_by(username='peter').first()
>>> peter.id
2
>>> peter.email
u'peter@example.org'

>>> missing = User.query.filter_by(username='missing').first()
>>> missing is None
True

>>> User.query.filter(User.email.endswith('@example.com')).all()
[<User u'admin'>, <User u'guest'>]

>>> User.query.order_by(User.username).all()
[<User u'admin'>, <User u'guest'>, <User u'peter'>]

>>> User.query.limit(1).all()
[<User u'admin'>]

>>> User.query.get(1)
<User u'admin'>

@app.route('/user/<username>')
def show_user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('show_user.html', user=user)

>>> User.query.filter_by(username=username).first_or_404(description='There is no data with {}'.format(username))