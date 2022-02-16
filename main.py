import os
import sys
import urllib.error
from flask import Flask, render_template, request, url_for, flash, redirect
import user_location
import user_locator


app = Flask(__name__)
app.config['SECRET_KEY'] = '7b6615d0aac860150ac2fd11e98f30bd84182aa360176b8c'


messages = [{'title': '@user1',
             'content': '(latitude1, longitude1)'},
            {'title': '@user2',
             'content': '(latitude2, longitude2)'}
            ]


@app.route('/')
def index():
    return redirect(url_for('create'))


@app.route('/create/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        if not title:
            flash('Username is required!')
        elif not content:
            flash('Number of friends is required!')
        elif not content.isdigit():
            flash('Please enter a digit!')
        elif ' ' in title:
            flash('Please enter a valid username')
        else:
            try:
                content = int(content)
            except ValueError:
                content = 20
            try:
                data = user_location.fr_list(title, content)
                dct = dict()
                for user in range(len(data['users'])):
                    dct[data['users'][user]['screen_name']] = data['users'][user]['location']
                new_dct = {}
                for user in dct:
                    try:
                        location = user_locator.locate(dct[user])
                        if location not in dct:
                            new_dct[location] = [user]
                        else:
                            new_dct[location].append(user)
                    except:
                        location = dct[user]
                    messages.append({'title': user, 'content': location})
                    user_locator.put_on_map(new_dct)
            except urllib.error.HTTPError:
                flash('User not found!')
            return render_template('friends_map.html', messages=messages)
    return render_template('create.html')


