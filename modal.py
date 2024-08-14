from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
class User(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    username = db.Column(db.String(20), nullable=False,unique=True)
    Fullname = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(80),nullable = False)
    gender  = db.Column(db.String(1),nullable=False)
    email_address = db.Column(db.String(200),nullable=False,unique=True)
    phone_Number = db.Column(db.Integer,nullable =False)
    dob = db.Column(db.Date, nullable=False)
    account_status = db.Column(db.String(20))
    account_type =db.Column(db.String(20))
    profile = db.Column(db.String(200))
    Favourites = db.Column(db.String, db.ForeignKey('song.id'))
    logg = db.Column(db.Integer)
    playlists = db.relationship('Playlist', secondary='userplaylist',backref='users',cascade='all, delete')
    rating=db.relationship('Rating',backref='user',cascade='all, delete')
    def _repr_(self,username):
        return '<User %r>' % (self.username)

# album and creator many to one
class Creator(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    username = db.Column(db.String(20), nullable=False,unique=True)
    Fullname = db.Column(db.String(20), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    gender  = db.Column(db.String(1),nullable=False)
    nationality =  db.Column(db.String, nullable=False)
    password = db.Column(db.String(80),nullable = False)
    phone_Number = db.Column(db.Integer,nullable =False)
    email_address = db.Column(db.String(200),nullable=False,unique=True)
    account_creationdate = db.Column(db.Date, nullable=False)
    profile = db.Column(db.String(200))
    bio = db.Column(db.String(200))
    playlists = db.relationship('Playlist', secondary='creatorplaylist',backref='creators',cascade='all, delete')
    logg = db.Column(db.Integer)
    albums = db.relationship('Album', backref='creator',cascade='all, delete-orphan')
    rating=db.relationship('Rating',backref='creator',cascade='all, delete')
    songs = db.relationship('Song',backref='creator',cascade='all, delete-orphan')
    def _repr_(self,username):
        return '<User %r>' % (self.username)
#  Album and genre ------ > Many to one
class Genre(db.Model):#ok
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(20), nullable=False,unique=True)
    albums = db.relationship('Album',backref='genre',cascade='all, delete-orphan')
    songs = db.relationship('Song',backref='genre',cascade='all, delete-orphan')
#  song and album --------------------> one song can belong to only one album one to one done
class Album(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(20), nullable=False,unique=True)
    genre_id  = db.Column(db.Integer,db.ForeignKey('genre.id'))
    artist = db.Column(db.String(20),nullable=False,unique=True)
    songs = db.relationship('Song',uselist=False,backref='album',cascade='all, delete-orphan',single_parent=True)
    song_id = db.Column(db.Integer, db.ForeignKey('song.id'), nullable=False)
    creator_id = db.Column(db.Integer, db.ForeignKey('creator.id'))

#  song and genre -------------------> Many song can belong to one genre done
# song and creator ---------------------> many to one done
class Song(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    s_name = db.Column(db.String(200), nullable=False,unique=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('creator.id'))
    genre_id  = db.Column(db.Integer,db.ForeignKey('genre.id'))
    duration = db.Column(db.Interval, nullable=False)
    creation_date = db.Column(db.Date,nullable = False)
    s_path = db.Column(db.String (200), nullable=False)
    language = db.Column(db.String(20), nullable=False)
    cover_art = db.Column(db.String(200))
    playlists = db.relationship('Playlist', secondary='playlistsong', backref="songs",cascade='all, delete')
    ratings = db.relationship('Rating',backref='song',secondary='songrating')
    def _repr_(self,s_name):
        return '<Song %r>' % (self.s_name)

class Playlist(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    playlist_duration = db.Column(db.Time)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    creator_id = db.Column(db.Integer, db.ForeignKey('creator.id'))
    name = db.Column(db.String(200), nullable=False)
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.id'),nullable= False)
    date_created = db.Column(db.Date, nullable=False)

class Rating(db.Model):
    rating_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    song_id = db.Column(db.Integer, db.ForeignKey('song.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    cuser_id = db.Column(db.Integer, db.ForeignKey('creator.id'))
    rating =db.Column(db.Integer(), nullable=False)
    date_created = db.Column(db.Date)
# user and playlist ----------------> Many to Many done
class Userplaylist(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    playlist_id = db.Column(db.Integer, db.ForeignKey('playlist.id'), nullable=False)
class creatorplaylist(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('creator.id'),nullable=False)
    playlist_id = db.Column(db.Integer, db.ForeignKey('playlist.id'), nullable=False)
# song and playlist ----------------> Many to Many done
class Playlistsong(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    playlist_id = db.Column(db.Integer, db.ForeignKey('playlist.id'))
    song_id = db.Column(db.Integer, db.ForeignKey('song.id'))
#  song and rating ---------------------> many to many done
class Songrating(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    song_id = db.Column(db.Integer, db.ForeignKey('song.id'))
    rating_id = db.Column(db.Integer, db.ForeignKey('rating.rating_id'))