"""
Insta485 accounts view.

URLs include:
/accounts/login/
/accounts/logout/
/accounts/create/
/accounts/delete/
/accounts/edit/
/accounts/password/

"""
from flask import render_template, session, request, redirect, url_for
import insta485


@insta485.app.route('/accounts/login/')
def show_login():
    """Show login."""
    # Check if logged in
    if 'username' in session:
        return redirect(url_for('show_index'))

    return render_template('login.html')


@insta485.app.route('/accounts/logout/', methods=['POST'])
def post_logout():
    """Post logout."""
    session.clear()
    return redirect(url_for('show_login'))


@insta485.app.route('/accounts/create/')
def show_create():
    """Show create."""
    if 'username' in session:
        return redirect(url_for('show_edit'))
    return render_template('create.html')


@insta485.app.route('/accounts/delete/')
def show_delete():
    """Show delete."""
    if 'username' not in session:
        return redirect(url_for('show_login'))

    logname = session['username']
    context = {'logname': logname}
    return render_template('delete.html', **context)


@insta485.app.route('/accounts/edit/')
def show_edit():
    """Show edit."""
    if 'username' not in session:
        return redirect(url_for('show_login'))

    logname = session['username']
    current_url = request.path

    connection = insta485.model.get_db()

    cur = connection.execute(
        "SELECT fullname, email, filename "
        "FROM users "
        "WHERE username = ? ",
        (logname, )
    )
    userdata = cur.fetchall()[0]

    context = {'logname': logname, 'email': userdata['email'],
               'user_img_url': userdata['filename'],
               'current_url': current_url, 'fullname': userdata['fullname']}

    return render_template('edit.html', **context)


@insta485.app.route('/accounts/password/')
def show_password():
    """Show password."""
    if 'username' not in session:
        return redirect(url_for('show_login'))

    logname = session['username']

    context = {'logname': logname}

    return render_template('password.html', **context)
