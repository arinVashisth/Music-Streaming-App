# 22f3001906
# Importing work is here
import os
import datetime
import mutagen
from mutagen import mp3,mp4,ogg
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4
from mutagen.ogg import OggFileType
# audio=mutagen(file_name)
# audio.length()
from werkzeug.utils import secure_filename
from flask import Flask,render_template,request,redirect,url_for,flash
from modal import * # importing from modal

############################################################################################################
#curr_dir = os.path.abspath(os.path.dirname(__file__))  # Directory Path
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///Music.sqlite3" # Database connection for using database values
app.config['SECRET_KEY'] = 'secret' # Admin session available
app.config ['UPLOAD_FOLDER'] = 'static/uploads'
app.app_context().push()
db.init_app(app)
############################################################################################################
# Extra Functions start from here
# Genres=['Pop','Rock','Hip&Hop','Rap','Country','R & B','Folk','Jazz','Heavy Metal','EDM','Soul','Funk','Raggae','Disco','Punk Rock','Classical','House','Techno','Indie Rock']
Languages=['Hindi','English','Punjabi','Marathi','Bengali']
Ratings = [1,2,3,4,5]
ALLOWED_EXTENSIONS = {'.png','.jpg','.jpeg','.ogg','.mp3'}
def get_duration(file_name,file_path):
    if file_path.endswith('.mp3'):
        audio = MP3(file_name)
    elif file_path.endswith('.mp4'):
        audio = MP4(file_name)
    elif file_path.endswith('.ogg'):
        audio = OggFileType(file_name)
    return audio.info.length
def verify_user(list1,email_address,password):
    for i in list1:
        if i.email_address == email_address and i.password==password:
            return 1
    return 0
def allowed_file(filename):
    global ALLOWED_EXTENSIONS
    return '.'in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS
def verify(email,password):
    if(email=='arinvashisth@gmail.com' and password=='2004'):
        return True
    else:
        return False
def check_gender(var):
    if var=='1':
        return 'Male'
    elif var=='2':
        return 'Female'
    else:
        return 'Rather not say'
def applogg(ver):
    if ver:
        inputs = User()
        db.session.add(inputs)
        db.session.commit()
def verify2(logg):
    if logg=='1':
        return 1
    else:
        return 0
def verlogin(us):
    if us is None:
        return 0
    else:
        return 1
# def check(creator_or_user):
    


# WEBPAGE Functions start from here
""" HOME PAGE"""
@app.route('/',methods=["GET","POST"])
def Home():
    return render_template('baselogin.html')


@app.route('/logout/<int:n>',methods=["GET","POST"])
def logout(n):
    userl = User.query.filter_by(id=n).first()
    cuserl = Creator.query.filter_by(id=n).first()
    if userl:
        inputs = User.query.get_or_404(n)
        inputs.logg=0
        db.session.commit()
        lsit.pop()
        return redirect(url_for('Home'))
    elif cuserl:
        inputs = Creator.query.get_or_404(n)
        inputs.logg=0
        db.session.commit()
        clsit.pop()
        return redirect(url_for('Home'))





@app.route('/new/<string:email>/<string:pass1>',methods=["GET","POST"])
def New(email,pass1):
    songs=Song.query.all()
    list3=[]
    for i in songs:
        if(i.creator_id):
            continue
        else:
            list3.append(i)
    if email==0 and pass1==0:
        listuser=[]
    else:
        listuser=User.query.filter_by(email_address=email).first()
    return render_template('new.html',songs=list3,userl=listuser)


@app.route('/new2/<string:email>/<string:pass1>',methods=["GET","POST"])
def New2(email,pass1):
    songs=Song.query.all()
    # user2 = User.
    list3=[]
    for i in songs:
        if(i.creator_id):
            continue
        else:
            list3.append(i)
    if email==0 and pass1==0:
        listuser=[]
    else:
        listuser=Creator.query.filter_by(email_address=email).first()
    return render_template('new2.html',songs=list3,userl=listuser)




# if 'file' not in request.files:
#     flash('No file part')
# name = request.form.get("name") 
# file = request.files['picture']
# if file.filename == '':
#     flash('No selected file')
# if file and allowed_file(file.filename):
#     filename = secure_filename(file.filename)
#     file_path = os.path.join(app.config['UPLOAD_FOLDER'],filename)
#     file.save(file_path)




# Logging Functions
""" SIGNUP PAGES"""
@app.route('/bothsignup',methods=["GET","POST"])
def Bothsignup():
    return render_template('/login/bothsignup.html')

@app.route('/signup',methods=["GET","POST"])
def Signup():
    if request.method == "POST":
        username = request.form.get('uname')
        fullname = request.form.get('fname')
        email_address = request.form.get('email')
        pass1 = request.form.get('pass')
        gender = request.form.get('gender')
        gender = check_gender(gender)
        phonum = request.form.get('phonum')
        profile = request.files['profile']
        if 'file' not in request.files['profile']:
            flash('No file part')
        if profile.filename == '':
            flash('No selected file')
        if profile and allowed_file(profile.filename):
            filename = secure_filename(profile.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'],filename)
            profile.save(file_path)

        dob = request.form.get('dob')
        dob=datetime.datetime.strptime(dob, "%Y-%m-%d").date()
        inputs = User(username=username,Fullname=fullname,email_address=email_address,password=pass1,gender=gender,phone_Number=phonum,dob=dob,profile=file_path,logg=0)
        db.session.add(inputs)
        db.session.commit()
        return redirect(url_for('Login'))
    return render_template('/login/signup.html')

@app.route('/csignup',methods=["GET","POST"])
def Csignup():
    if request.method == "POST":
        username = request.form.get('uname')
        fullname = request.form.get('fname')
        dob = request.form.get('dob')
        dob=datetime.datetime.strptime(dob, "%Y-%m-%d").date()
        gender = request.form.get('gender')
        gender = check_gender(gender)
        nationality = request.form.get('nationality')
        pass1 = request.form.get('pass')
        phone_Number = request.form.get('phonum')
        email_address = request.form.get('email')
        # adate = request.form.get('adate')
        # adate=datetime.datetime.strptime(adate, "%Y-%m-%d").date()
        adate = datetime.datetime.now()
        profile = request.files['profile']
        if 'file' not in request.files['profile']:
            flash('No file part')
        if profile.filename == '':
            flash('No selected file')
        if profile and allowed_file(profile.filename):
            filename = secure_filename(profile.filename)
            file_path1 = os.path.join(app.config['UPLOAD_FOLDER'],filename)
            profile.save(file_path1)
        bio = request.form.get('bio')
        inputs = Creator(username=username,Fullname=fullname,dob=dob,gender=gender,nationality=nationality,password=pass1,phone_Number=phone_Number,email_address=email_address,account_creationdate=adate.date(),profile=file_path1,bio=bio)
        db.session.add(inputs)
        db.session.commit()
        record = User.query.filter_by(username=username).first()
        db.session.delete(record)
        db.session.commit()
        return redirect(url_for('Clogin'))
    return render_template('/login/csignup.html')





""" FORGOT PAGE"""
@app.route('/forgot',methods=["GET","POST"])
def Forgot():
    return render_template('/login/forgotpassword.html')





""" LOGIN PAGES"""
@app.route('/bothlogin',methods=["GET","POST"])
def bothlogin():
    return render_template('/login/bothlogin.html')


lsit = []

@app.route('/login',methods=["GET","POST"])
def Login():
    if request.method == "POST":
        email_address = request.form.get('email')
        pass1 = request.form.get('pass')
        list1=User.query.all()
        if verify_user(list1,email_address,pass1):
            list2=User.query.filter_by(email_address=email_address).first()
            inputs = User.query.get_or_404(list2.id)
            inputs.logg=1
            return redirect(url_for('New',email=email_address,pass1=pass1))
    if(len(lsit)>0):
        if(lsit[0].logg==1):
            return redirect(url_for('New',email=clsit[0].email_address,pass1=clsit[0].password))
    return render_template('/login/login.html')



clsit = []

@app.route('/clogin',methods=["GET","POST"])
def Clogin():
    if request.method == "POST":
        email_address = request.form.get('email')
        pass1 = request.form.get('pass')
        list1=Creator.query.all()
        if verify_user(list1,email_address,pass1):
            list2=Creator.query.filter_by(email_address=email_address).first()
            clsit.append(list2)
            # list2.logg=1
            inputs = Creator.query.get_or_404(list2.id)
            inputs.logg=1
            # db.session.add(inputs)
            db.session.commit()
            return redirect(url_for('New2',email=email_address,pass1=pass1))
    if(len(clsit)>0):
        if(clsit[0].logg==1):
            return redirect(url_for('New2',email=clsit[0].email_address,pass1=clsit[0].password))
    # cuserl = Creator.query.filter_by()
    return render_template('/login/clogin.html')

@app.route('/alogin',methods=["GET","POST"])
def Alogin():
    if request.method == "POST":
        email = request.form.get('email')
        pass1 = request.form.get('pass')
        if verify(email,pass1):
            return redirect(url_for('Admin'))
    return render_template('/login/alogin.html')

# 
# 
# 
# 
# 
# USER Browse Section
@app.route('/release/<int:n>',methods=["GET","POST"])
def New_release(n):
    login1 = User.query.filter_by(id=n).first()
    return render_template("/browse/new_releases.html",cred=login1)

@app.route('/tplaylists/<int:n>',methods=["GET","POST"])
def Tplaylists(n):
    login1 = User.query.filter_by(id=n).first()
    return render_template("/browse/top_playlists.html",cred=login1)

@app.route('/tartists/<int:n>',methods=["GET","POST"])
def Tartists(n):
    login1 = User.query.filter_by(id=n).first()
    return render_template("/browse/top_artists.html",cred=login1)



# CREATOR Browse Section
@app.route('/crelease/<int:n>',methods=["GET","POST"])
def CNew_release(n):
    login1 = Creator.query.filter_by(id=n).first()
    return render_template("/cbrowse/C_new_releases.html",cred=login1)

@app.route('/ctplaylists/<int:n>',methods=["GET","POST"])
def CTplaylists(n):
    login1 = Creator.query.filter_by(id=n).first()
    return render_template("/cbrowse/C_top_playlists.html",cred=login1)

@app.route('/ctartists/<int:n>',methods=["GET","POST"])
def CTartists(n):
    login1 = Creator.query.filter_by(id=n).first()
    return render_template("/cbrowse/C_top_artists.html",cred=login1)



# USER Library Section 
@app.route('/likedsongs/<int:n>',methods=["GET","POST"])
def Liked_songs(n):
    login1 = User.query.filter_by(id=n).first()
    return render_template("/library/liked_songs.html",cred=login1)

@app.route('/playlists/<int:n>',methods=["GET","POST"])
def Playlists(n):
    list1 = Playlist.query.all()
    list2=[]
    for i in list1:
        if(i.user_id):
            continue
        else:
            list2.append(i)
    login1 = User.query.filter_by(id=n).first()
    return render_template("/library/playlists.html",playlists=list2,cred=login1)

@app.route('/artists/<int:n>',methods=["GET","POST"])
def Artists(n):
    albums = Album.query.all()
    login1 = User.query.filter_by(id=n).first()
    return render_template("/library/artists.html",albums=albums,cred=login1)

@app.route('/albums/<int:n>',methods=["GET","POST"])
def Albums(n):
    albums = Album.query.all()
    login1 = User.query.filter_by(id=n).first()
    return render_template("/library/albums.html",albums=albums,cred=login1)

@app.route('/history/<int:n>',methods=["GET","POST"])
def History(n):
    login1 = User.query.filter_by(id=n).first()
    return render_template("/library/history.html",cred=login1)



# CREATOR Library Section 
@app.route('/clikedsongs/<int:n>',methods=["GET","POST"])
def CLiked_songs(n):
    login1 = Creator.query.filter_by(id=n).first()
    return render_template("/clibrary/C_liked_songs.html",cred=login1)

@app.route('/cplaylists/<int:n>',methods=["GET","POST"])
def CPlaylists(n):
    list1 = Playlist.query.all()
    list2=[]
    for i in list1:
        if(i.user_id):
            continue
        else:
            list2.append(i)
    login1 = Creator.query.filter_by(id=n).first()
    return render_template("/clibrary/C_playlists.html",playlists=list2,cred=login1)

@app.route('/cartists/<int:n>',methods=["GET","POST"])
def CArtists(n):
    albums = Album.query.all()
    login1 = Creator.query.filter_by(id=n).first()
    return render_template("/clibrary/C_artists.html",albums=albums,cred=login1)

@app.route('/calbums/<int:n>',methods=["GET","POST"])
def CAlbums(n):
    albums = Album.query.all()
    login1 = Creator.query.filter_by(id=n).first()
    return render_template("/clibrary/C_albums.html",albums=albums,cred=login1)

@app.route('/chistory/<int:n>',methods=["GET","POST"])
def CHistory(n):
    login1 = Creator.query.filter_by(id=n).first()
    return render_template("/clibrary/C_history.html",cred=login1)





# PLAYLISTS ADDING AND DELETING
@app.route('/addplaylist',methods=["GET","POST"])
def Add_playlist():
    if request.method == "POST":
        playlist_name = request.form.get('pname')
        user_name = request.form.get('uname')
        u_id = User.query.filter_by(username=user_name).first()
        u_id = u_id.id
        genre = request.form.get('genre')
        genre2 = Genre.query.filter_by(name=genre).first()
        # print(genre)
        genre3 = genre2.id
        # date_joined = request.form.get('djoined')
        # date_joined=datetime.datetime.strptime(date_joined, "%Y-%m-%d").date()
        t = datetime.datetime.now()
        inputs = Playlist(name=playlist_name,genre_id=genre3,date_created=t.date(),user_id=u_id)
        db.session.add(inputs)
        db.session.commit()
        return redirect(url_for('Dashboard',n=u_id))
    genre = Genre.query.all()
    return render_template('/add/add_playlist.html',genre=genre)
@app.route('/addcplaylist',methods=["GET","POST"])
def Add_C_playlist():
    if request.method == "POST":
        playlist_name = request.form.get('pname')
        user_name = request.form.get('uname')
        u_id = Creator.query.filter_by(username=user_name).first()
        u_id = u_id.id
        genre = request.form.get('genre')
        genre2 = Genre.query.filter_by(name=genre).first()
        # print(genre)
        genre3 = genre2.id
        # date_joined = request.form.get('djoined')
        # date_joined=datetime.datetime.strptime(date_joined, "%Y-%m-%d").date()
        t = datetime.datetime.now()
        inputs = Playlist(name=playlist_name,genre_id=genre3,date_created=t.date(),user_id=u_id)
        db.session.add(inputs)
        db.session.commit()
        return redirect(url_for('Cdashboard',n=u_id))
    genre = Genre.query.all()
    return render_template('/add/add_C_playlist.html',genre=genre)
@app.route('/addadminplaylist',methods=["GET","POST"])
def Add_Admin_playlist():
    if request.method == "POST":
        playlist_name = request.form.get('pname')
        # user_name = request.form.get('uname')
        # u_id = User.query.filter_by(username=user_name).first()
        # u_id = u_id.id
        genre = request.form.get('genre')
        genre2 = Genre.query.filter_by(name=genre).first()
        # print(genre)
        genre3 = genre2.id
        # date_joined = request.form.get('djoined')
        # date_joined=datetime.datetime.strptime(date_joined, "%Y-%m-%d").date()
        t = datetime.datetime.now()
        # ,user_id=u_id
        inputs = Playlist(name=playlist_name,genre_id=genre3,date_created=t.date())
        db.session.add(inputs)
        db.session.commit()
        return redirect(url_for('Admin_Playlists'))
    genre = Genre.query.all()
    return render_template('/add/add_admin_playlist.html',genre=genre)
@app.route('/admindeleteplaylist/<int:n>',methods=["GET","POST"])
def Admin_Delete_playlist(n):
    record = Playlist.query.filter_by(id=n).first()
    db.session.delete(record)
    db.session.commit()
    return redirect(url_for('Admin_Playlists'))
@app.route('/admincretedeleteplaylist/<int:n>',methods=["GET","POST"])
def Admin_creator_Delete_playlist(n):
    record = Playlist.query.filter_by(id=n).first()
    db.session.delete(record)
    db.session.commit()
    return redirect(url_for('Admin_User_playlists'))
@app.route('/cdeleteplaylist/<int:n>',methods=["GET","POST"])
def Creator_Delete_playlist(n):
    record = Playlist.query.filter_by(id=n).first()
    id1 = record.user_id
    db.session.delete(record)
    db.session.commit()
    return redirect(url_for('Cdashboard',n=id1))
@app.route('/udeleteplaylist/<int:n>',methods=["GET","POST"])
def User_Delete_playlist(n):
    record = Playlist.query.filter_by(id=n).first()
    id1 = record.user_id
    db.session.delete(record)
    db.session.commit()
    return redirect(url_for('Dashboard',n=id1))





# SONG ADDING AND DELETING
@app.route('/addsong',methods=["GET","POST"])
def Add_song():
    if request.method == "POST":
        sname = request.form.get('sname')
        cname = request.form.get('cname')
        cname = Creator.query.filter_by(username=cname).first()
        creator_id = cname.id
        genre = request.form.get('genre')
        genre = Genre.query.filter_by(name=genre).first()
        genre_id = genre.id
        song = request.files['spath']
        filename1 = secure_filename(song.filename)
        file_path1 = os.path.join(app.config['UPLOAD_FOLDER'],filename1)
        song.save(file_path1)
        language = request.form.get('language')
        Cover_art = request.files['coverart']
        filename2 = secure_filename(Cover_art.filename)
        file_path2 = os.path.join(app.config['UPLOAD_FOLDER'],filename2)
        Cover_art.save(file_path2)
        d = get_duration(song,file_path1)
        d = datetime.timedelta(d)
        t = datetime.datetime.now()
        inputs = Song(s_name=sname,genre_id=genre_id,creator_id=creator_id,language=language,s_path=file_path1,cover_art=file_path2,duration=d,creation_date=t.date())
        db.session.add(inputs)
        db.session.commit()
        cred = Creator.query.filter_by(id=creator_id).first()
        cred = cred.id
        return redirect(url_for('Cdashboard',n=cred))
    genress = Genre.query.all() 
    return render_template('/add/add_song.html',lang=Languages,genress=genress)
@app.route('/addadminsong',methods=["GET","POST"])
def Add_Admin_song():
    if request.method == "POST":
        sname = request.form.get('sname')
        cname = request.form.get('cname')
        # cname = Creator.query.filter_by(username=cname).first()
        # creator_id = cname.id
        genre = request.form.get('genre')
        genre = Genre.query.filter_by(name=genre).first()
        genre_id = genre.id
        song = request.files['spath']
        filename1 = secure_filename(song.filename)
        file_path1 = os.path.join(app.config['UPLOAD_FOLDER'],filename1)
        song.save(file_path1)
        language = request.form.get('language')
        Cover_art = request.files['coverart']
        filename2 = secure_filename(Cover_art.filename)
        file_path2 = os.path.join(app.config['UPLOAD_FOLDER'],filename2)
        Cover_art.save(file_path2)
        d = get_duration(song,file_path1)
        d = datetime.timedelta(d)
        t = datetime.datetime.now()
        # ,creator_id=creator_id
        inputs = Song(s_name=sname,genre_id=genre_id,language=language,s_path=file_path1,cover_art=file_path2,duration=d,creation_date=t.date())
        db.session.add(inputs)
        db.session.commit()
        return redirect(url_for('Admin_Songs'))
    genress = Genre.query.all() 
    return render_template('/add/add_admin_song.html',lang=Languages,genress=genress)
@app.route('/deleteadminsong/<int:n>',methods=["GET","POST"])
def Admin_Delete_song(n):
    # sname = request.form.get('sname')
    record = Song.query.filter_by(id=n).first()
    db.session.delete(record)
    db.session.commit()
    return redirect(url_for('Admin_Songs'))
@app.route('/cdeletesong/<int:n>',methods=["GET","POST"])
def Delete_song(n):
    record = Song.query.filter_by(id=n).first()
    db.session.delete(record)
    db.session.commit()
    cred = record.creator_id
    return redirect(url_for('Cdashboard',n=cred))
# @app.route('/deletesong/<int:n>',methods=["GET","POST"])
# def CDelete_song():
#     record = Song.query.filter_by(id=n).first()
#     db.session.delete(record)
#     db.session.commit()
#     return redirect(url_for('Admin_Songs'))






# GENRE DELETING AND ADDING
@app.route('/addgenre',methods=["GET","POST"])
def Add_genre():
    if request.method == "POST":
        genre_name = request.form.get('gname')
        inputs = Genre(name=genre_name)
        db.session.add(inputs)
        db.session.commit()
        return redirect(url_for('Admin_Genre'))
    return render_template('/add/add_genre.html')
@app.route('/delgenre/<int:n>',methods=["GET","POST"])
def Delelte_genre(n):
    # genre = request.form.get(n)
    record = Genre.query.filter_by(id=n).first()
    db.session.delete(record)
    db.session.commit()
    return redirect(url_for('Admin_Genre'))
# l=[]






# GENRE DELETING AND ADDING

@app.route('/addalbums',methods=["GET","POST"])
def Add_album():
    if request.method == "POST":
        name = request.form.get('aname')
        artist = request.form.get('artname')
        genre = request.form.get('genre')
        genre = Genre.query.filter_by(name=genre).first()
        genre_id = genre.id
        song_n = request.form.get('sname')
        song = Song.query.filter_by(s_name=song_n).first()
        song_id = song.id
        cname = request.form.get('cname')
        creator = Creator.query.filter_by(username=cname).first()
        creator_id = creator.id 
        inputs=Album(name=name,genre_id=genre_id,artist=artist,song_id=song_id,creator_id=creator_id)
        db.session.add(inputs)
        db.session.commit()
        return redirect(url_for('Admin_albums'))
    genre = Genre.query.all()
    return render_template('/add/add_albums.html',genre=genre)
@app.route('/deleteadminalbum/<int:n>',methods=["GET","POST"])
def Delete_Admin_album(n):
    record = Album.query.filter_by(id=n).first()
    db.session.delete(record)
    db.session.commit()
    return redirect(url_for('Admin_albums'))
@app.route('/deleteuser/<int:n>',methods=["GET","POST"])
def Delete_User(n):
    record = User.query.filter_by(id=n).first()
    db.session.delete(record)
    db.session.commit()
    return redirect(url_for('Admin_Users'))










# Admin Panel Pages
@app.route('/adminusers',methods=["GET","POST"])
def Admin_Users():
    list1=User.query.all()
    # for u in list1:
    #     L,l=[],[]
    #     l.append(u.sr_no)
    #     l.append(u.name)
    #     l.append(u.email)
    #     l.append(u.password)
    #     L.append(l)
    # l2=len(L)
    return render_template("/admin/admin_users.html",list1=list1)

@app.route('/adminsongs',methods=["GET","POST"])
def Admin_Songs():
    list1=Song.query.all()
    list2=[]
    for i in list1:
        if(i.creator_id):
            continue
        else:
            list2.append(i)
    return render_template("/admin/admin_songs.html",list1=list2)

@app.route('/adminplaylists',methods=["GET","POST"])
def Admin_Playlists():
    list1 = Playlist.query.all()
    list2=[]
    for i in list1:
        if(i.user_id):
            continue
        else:
            list2.append(i)
    return render_template("/admin/admin_playlists.html",list1=list2)

@app.route('/adminuserplaylists',methods=["GET","POST"])
def Admin_User_playlists():
    list1 = Playlist.query.all()
    list2=[]
    for i in list1:
        if(i.user_id):
            list2.append(i)
    return render_template("/admin/admin_user_playlists.html",list1=list2)

@app.route('/admincreators',methods=["GET","POST"])
def Admin_Creators():
    list1=Creator.query.all()
    return render_template("/admin/admin_creators.html",list1=list1)

@app.route('/adminalbums',methods=["GET","POST"])
def Admin_albums():
    list1 = Album.query.all()
    return render_template("/admin/admin_albums.html",list1=list1)

@app.route('/adminartists',methods=["GET","POST"])
def Admin_Carousel():
    return render_template("/admin/admin_artists.html")

@app.route('/admingenre',methods=["GET","POST"])
def Admin_Genre():
    list1=Genre.query.all()

    return render_template("/admin/admin_genre.html",list1=list1)








@app.route('/search',methods=["GET","POST"])
def Search():
    if request.form == "POST":
        return render_template('search.html')
    return render_template('search.html')
@app.route('/csearch',methods=["GET","POST"])
def Csearch():
    if request.form == "POST":
        return render_template('csearch.html')
    return render_template('csearch.html')


""" ADMIN PAGE"""

@app.route('/admin',methods=["GET","POST"])
def Admin():
    return render_template('/admin/admin.html')


# @app.route('/addsong',methods=["GET","POST"])
# def Add_song():
#     if request.method == "POST":

#     return render_template("add_song.html")







# SONG

@app.route('/song/<int:n>/<string:str>',methods=["GET","POST"])
def song(n,str):
    used_song = Song.query.filter_by(id=n).first()
    # udetails = User.query.all()
    # cdetails = Creator.query.all()
    user_name = User.query.filter_by(username=str).first()
    cuser_name = Creator.query.filter_by(username=str).first()
    # if(user_name):
    #     cred=user_name
    # elif(cuser_name):
    #     cred=cuser_name
    return render_template('song.html',usong=used_song,cname=cuser_name,uname=user_name)

@app.route('/paddsong/<int:n>',methods=["GET","POST"])
def Paddsong(n):
    if request.method == "POST":
        playname = request.form.get('playlist')
        playlistid = Playlist.query.filter_by(name=playname).first()
        playlistid = playlistid.id
        songid = Song.query.filter_by(id=n).first()
        bi = songid.creator_id
        songid = songid.id
        inputs = Playlistsong(playlist_id=playlistid,song_id=songid)
        db.session.add(inputs)
        db.session.commit()
        
        return redirect(url_for('Dashboard',n=bi))
    ni = Playlist.query.all()
    return render_template('/playlistadd/padd_song.html',genress=ni,n=n)

@app.route('/pcaddsong',methods=["GET","POST"])
def Pcaddsong():
    ni = Playlist.query.all()
    return render_template('/playlistadd/pcadd_song.html',genress=ni)


#PLAY LIST MORE DETAILS
@app.route('/playmoredetails/<int:n>',methods=["GET","POST"])
def Playmoredetails(n):
    list1=Song.query.filter_by(creator_id=n).all()
    list3=[]
    for i in list1:
        if(i.creator_id):
            list3.append(i)
    login1 = User.query.filter_by(id=n).first()
    return render_template('/playlistadd/playmoredetails.html',cred=login1)


@app.route('/cplaymoredetails/<int:n>',methods=["GET","POST"])
def Cplaymoredetails(n):
    list1=Song.query.filter_by(creator_id=n).all()
    list3=[]
    for i in list1:
        if(i.creator_id):
            list3.append(i)
    login1 = Creator.query.filter_by(id=n).first()
    return render_template('/playlistadd/cplaymoredetails.html',cred=login1)




@app.route('/addrating/<string:str>/<int:n>',methods=["GET","POST"])
def Give_rating(str,n):
    used_song_name = Song.query.filter_by(s_name=str).first()

    user_id = User.query.filter_by(id=n).first()
    cuser_id = Creator.query.filter_by(id=n).first()
    if request.method == "POST":
        used_song_name = Song.query.filter_by(s_name=str).first()
        song_id = used_song_name.id
        user_id = User.query.filter_by(id=n).first()
        cuser_id = Creator.query.filter_by(id=n).first()

        rate = request.form.get('genre')

        t = datetime.datetime.now()
        if user_id:
            user_name = user_id.username
            u_id = user_id.id
            inputs = Rating(song_id=song_id,rating=rate,date_created=t.date(),user_id=u_id)
            db.session.add(inputs)
            db.session.commit()
            return redirect(url_for('song',n=song_id,str=user_name))
        elif cuser_id:
            cuser_name = cuser_id.username
            cu_id = cuser_id.id
            inputs = Rating(song_id=song_id,rating=rate,date_created=t.date(),cuser_id=cu_id)
            db.session.add(inputs)
            db.session.commit()
            return redirect(url_for('song',n=song_id,str=cuser_name))
        
    return render_template('/add/add_rating.html',Ratings=Ratings,usong=used_song_name,uname=user_id,cname=cuser_id)





# DASHBOARD
@app.route('/dashboard/<int:n>',methods=["GET","POST"])
def Dashboard(n):
    if n==0:
        list1 = Playlist.query.all()
    else:
        list1 = Playlist.query.filter_by(user_id=n)
    list2=[]
    for i in list1:
        if(i.user_id):
            list2.append(i)
    login1 = User.query.filter_by(id=n).first()
    return render_template('dashboard.html',list1=list2,cred=login1)


@app.route('/cdashboard/<int:n>',methods=["GET","POST"])
def Cdashboard(n):
    if n==0:
        list1 = Playlist.query.all()
    else:
        list1 = Playlist.query.filter_by(user_id=n)
    list2=[]
    for i in list1:
        if(i.user_id):
            list2.append(i)
    list1=Song.query.filter_by(creator_id=n).all()
    list3=[]
    for i in list1:
        if(i.creator_id):
            list3.append(i)
    login1 = Creator.query.filter_by(id=n).first()
    return render_template('cdashboard.html',list1=list2,songs=list3,cred=login1)



if __name__ == "__main__":
    app.run(debug = True)






# @app.route ('/upload', methods=['GET',"POST"])



    # def upload_file ():
    # if request.method == 'POST':
    #     creator = request.form.get("artist")
    #     name= request.form.get("title")
    #     song = request.files ['song']
    #     cover_art =request.files['cover']
    #     genre = request.form.get("genre")
    #     lang=request.form.get("language")
    #     c = Creator.query.filter_by(username=creator).first()
    #     c_file = secure_filename(cover_art.filename)
    #     s_file = secure_filename (song.filename)
    #     song_path = os.path.join (app.config ['UPLOAD_FOLDER'], s_file)
    #     c_path  = os.path.join(app.config['UPLOAD_FOLDER'],c_file)
    #     d = get_duration(song,song_path)
    #     g= Genre.query.filter_by(name=genre).first()
    #     print(genre)
    #     song.save (song_path)
    #     cover_art.save(c_path)
    #     t = datetime.datetime.now()
    #     s = Song(s_name=name,creator_id=c.id,genre_id=g.id,duration=timedelta(d),creation_date=t.date(),s_path=song_path,language=lang)
    #     db.session.add(s)
    #     db.session.commit()
    #     return redirect(url_for('creator',name=creator))

    # return render_template("upload.html")