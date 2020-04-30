from flask import Flask, render_template, request, redirect, session, flash
from wtforms import Form, StringField, validators, TextAreaField, widgets
from models.PostObject import Post, splitCopyToBlocks, parseForLinks
from models.forms import BlogForm, SetPasswordForm, LoginForm, SiteInfoForm
from models.auth import hash_password, verify_password
import data
import json
import os
import math
from datetime import date, datetime

app = Flask(__name__)


post = Post("","","","","","")
app.secret_key = os.urandom(12)

@app.context_processor
def inject_dict_for_all_templates():
    f = open('data/blog_info.json')
    blogData = json.load(f)
    f.close()

    if 'settings' in blogData:
        meta = blogData['settings']
    else:
        meta = {
        "title": "blog name not set"
        }
    return dict(meta=meta)


@app.route('/', defaults={'pageNum':1})
@app.route('/<pageNum>')
def index(pageNum):
    f = open('data/blog_info.json')
    infoJSON = json.load(f)
    f.close()
    if 'username' not in infoJSON:
            return redirect('/set-credentials')
    else:
        f = open('data/posts_metadata.json')
        postsJSON = json.load(f)
        posts = postsJSON['posts']
        f.close()
        loggedIn = session.get("logged_in")
        pageNum = int(pageNum)
        postPerPage = 10
        startIndex = (pageNum - 1) * postPerPage
        endIndex = pageNum * postPerPage
        totalPages = math.ceil(len(posts)/postPerPage)
        return render_template('index.html', posts=posts, startIndex=startIndex, endIndex=endIndex, loggedIn=loggedIn, pageNum=pageNum, totalPages=totalPages)


@app.route("/logout")
def logOut():
    if not session.get("logged_in"):
        return redirect("/")
    session["logged_in"] = False
    return redirect('/')
    

@app.route('/set-credentials', methods=['GET','POST'])
def setInitialCredentials():
    form = SetPasswordForm(request.form)
    if request.method == 'POST':
        form.validate()
        if (request.form['password'] == request.form['passwordVerify']):
            pw_to_store = hash_password(request.form['password'])

            with open('data/blog_info.json') as posts_data:
                data = json.load(posts_data)
                data['username'] = request.form['username']
                data['password'] = pw_to_store
            write_json(data, filename='data/blog_info.json')
            session["logged_in"] = True
            return redirect('/settings')
        else:
            return render_template('set_credentials.html', form=form, errorMessage="Passwords do not match")
    else:
        f = open('data/blog_info.json')
        infoJSON = json.load(f)
        f.close()

        if 'username' in infoJSON:
            return redirect('/')
        else:
            return render_template('set_credentials.html', form=form)

@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if session.get("logged_in"):
        return redirect("/")
    form = LoginForm(request.form)
    form.validate()
    if request.method == 'POST':
        f = open('data/blog_info.json')
        infoJSON = json.load(f)
        pw = infoJSON['password']
        username = infoJSON['username']
        f.close()
        if username == request.form['username']:
            if (verify_password(pw, request.form['password'])):
                session["logged_in"] = True
                return redirect("/")
            else:
                return render_template('login.html', form=form, errorMessage="invalid password")
        else:
            return render_template('login.html', form=form, errorMessage="invalid user")
    else:
        return render_template('login.html', form=form)



@app.route('/settings', methods=['GET','POST'])
def setUp():
    if not session.get("logged_in"):
        return redirect("/")

    if request.method == 'POST':
        aboutBlocks = splitCopyToBlocks(request.form["about"])
        aboutDicts = []
        for p in aboutBlocks:
            pDict = {"block": p}
            aboutDicts.append(pDict)
        aboutDicts = parseForLinks(aboutDicts)
        settingsDict = {
            "title": request.form["title"],
            "tagLine" : request.form["tagLine"],
            "author" : request.form["author"],
            "about" : aboutDicts,
            "authorImage": request.form["authorImage"]
        }
        with open('data/blog_info.json') as posts_data:
            data = json.load(posts_data)
            data['settings'] = settingsDict
        write_json(data, filename='data/blog_info.json')
        return redirect('/')
    
    else:
        f = open('data/blog_info.json')
        blogData = json.load(f)
        f.close()

        form = SiteInfoForm(request.form)

        if 'settings' in blogData:
            copylist = blogData['settings']['about']
            copy = ""
            for c in copylist:
                if 'block' in c:
                    copy += c['block'] + "\n"
                if 'codeBlock' in c:
                    copy += c['codeBlock'] + "\n"

            form.title.data = blogData['settings']['title']
            form.tagLine.data = blogData['settings']['tagLine']
            form.author.data = blogData['settings']['author']
            form.about.data = copy
            form.authorImage.data = blogData['settings']['authorImage']

        return render_template('settings.html', form=form)


@app.route('/post/<slug>')
def load_post(slug):
    f = open('data/posts.json')
    postsJSON = json.load(f)
    postsInfo = postsJSON[slug]
    f.close()
    copy=parseForLinks(postsInfo["copy"])
    return render_template('blog_post.html', title=postsInfo["title"], subhead=postsInfo["subhead"], date=postsInfo["date"], image=postsInfo["imageSrc"], copy=copy)


@app.route('/add-post')
def newPost():
    if not session.get("logged_in"):
        return redirect("/login")

    form = BlogForm(request.form)
    return render_template('new_post.html', form=form)


@app.route('/preview', methods=['POST'])
def approvePost():
    if not session.get("logged_in"):
        return redirect("/login")

    slug = request.form['title'].replace(" ", "-")

    f = open('data/posts_metadata.json')
    data = json.load(f)
    f.close()

    form = BlogForm(request.form)
    today = datetime.now()
    fToday = today.strftime("%B %d, %Y %l:%M %p")

    form.validate()

    for p in data['posts']:
        if p['slug'] == slug:
            form.title.data = request.form['title']
            form.subhead.data = request.form['subhead']
            form.preview.data = request.form['preview']
            form.image.data = request.form['image']
            form.copy.data = request.form['copy']
            return render_template('new_post.html', form=form, errorMessage="Invalid Title: A post has already used this title")


    if request.method == 'POST' and form.validate():
        post.setTitle(request.form['title'])
        post.setSubhead(request.form['subhead'])
        post.setPreview(request.form['preview'])
        post.setDate(fToday)
        post.setImageSrc(request.form['image'])
        post.setCopy(request.form['copy'])
        return render_template('approve_new_post.html', post=post)
    return render_template('index.html', form=form)


@app.route('/confirmation')
def confirmation():
    if not session.get("logged_in"):
        return redirect("/login")

    copyDicts = []
    slug = post.title.replace(" ", "-")
    for p in post.getCopy():
        pDict = {"block": p}
        copyDicts.append(pDict)

    postDict = {
        "title": post.title,
        "date": post.date,
        "subhead": post.subhead,
        "imageSrc": post.imageSrc,
        "copy": copyDicts
    }

    postDataDict = {
        "title": post.title,
        "preview": post.preview,
        "date": post.date,
        "imageSrc": post.imageSrc,
        "slug": slug,
    }

    with open('data/posts_metadata.json') as posts_data:
        data = json.load(posts_data)
        temp = data['posts']
        temp.insert(0,postDataDict)
    write_json(data, filename='data/posts_metadata.json')

    with open('data/posts.json') as posts_file:
        data = json.load(posts_file)
        data[slug] = postDict
    write_json(data)
    return redirect("/")


@app.route('/delete/<slug>/<index>')
def deletePost(slug, index):
    if not session.get("logged_in"):
        return redirect("/login")

    with open('data/posts_metadata.json') as posts_data:
        data = json.load(posts_data)
        temp = data['posts']
        del temp[int(index)]
    write_json(data, filename='data/posts_metadata.json')

    with open('data/posts.json') as posts_file:
        data = json.load(posts_file)
        if slug in data:
            del data[slug]
    write_json(data)

    return redirect('/')


@app.route('/edit/<slug>/<index>')
def editPost(slug, index):
    if not session.get("logged_in"):
        return redirect("/login")

    form = BlogForm(request.form)
    today = datetime.now()
    fToday = today.strftime("%B %d, %Y %l:%M %p")

    with open('data/posts_metadata.json') as posts_data:
        data = json.load(posts_data)
        temp = data['posts']
        metadata = temp[int(index)]

    with open('data/posts.json') as posts_file:
        data = json.load(posts_file)
        if slug in data:
            postdata = data[slug]
    
    copylist = postdata['copy']
    copy = ""
    for c in copylist:
        copy += c['block'] + "\n"

    dateString = postdata['date'] + " - edited: " + fToday

    post.setTitle(postdata['title'])
    post.setSubhead(postdata['subhead'])
    post.setPreview(metadata['preview'])
    post.setDate(dateString)
    post.setImageSrc(postdata['imageSrc'])
    post.setCopy(copy)   
    
    form.title.data = postdata['title']
    form.subhead.data = postdata['subhead']
    form.preview.data = metadata['preview']
    form.image.data = postdata['imageSrc']
    form.copy.data = copy
    return render_template('edit_post.html', form=form, slug=slug, index=index)


@app.route('/preview/<slug>/<index>', methods=['POST'])
def approveEdit(slug, index):
    if not session.get("logged_in"):
        return redirect("/login")

    form = BlogForm(request.form)
    form.validate()
    if request.method == 'POST' and form.validate():
        post.setTitle(request.form['title'])
        post.setSubhead(request.form['subhead'])
        post.setPreview(request.form['preview'])
        post.setImageSrc(request.form['image'])
        post.setCopy(request.form['copy'])
        return render_template('approve_edit_post.html', post=post, slug=slug, index=index)
    return render_template('index.html', form=form)


@app.route('/confirmation/<slug>/<index>')
def editConfirmation(slug, index):
    if not session.get("logged_in"):
        return redirect("/")

    copyDicts = []
    for p in post.getCopy():
        pDict = {"block": p}
        copyDicts.append(pDict)
    postDict = {
        "title": post.title,
        "date": post.date,
        "subhead": post.subhead,
        "imageSrc": post.imageSrc,
        "copy": copyDicts
    }
    postDataDict = {
        "title": post.title,
        "preview": post.preview,
        "date": post.date,
        "imageSrc": post.imageSrc,
        "slug": slug,
    }
    with open('data/posts_metadata.json') as posts_data:
        data = json.load(posts_data)
        temp = data['posts']
        temp[int(index)] = postDataDict
    write_json(data, filename='data/posts_metadata.json')
    with open('data/posts.json') as posts_file:
        data = json.load(posts_file)
        data[slug] = postDict
    write_json(data)
    return redirect("/")


if __name__ == '__main__':
    app.run(debug=True)

def write_json(data, filename='data/posts.json'): 
    with open(filename,'w') as f: 
        json.dump(data, f, indent=4) 
