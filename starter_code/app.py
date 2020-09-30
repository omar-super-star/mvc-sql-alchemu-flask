#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)
# TODO: connect to a local postgresql database
#finish this todo
app.config["SQLALCHEMY_DATABASE_URI"]='postgresql://postgres:omar@localhost:5432/project2data'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    website = db.Column(db.String(500))
    seeking_talent=db.Column(db.Boolean())
    seeking_description=db.Column(db.String(500))
    show = db.relationship("Show",backref="Venue")

   
    
    

    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    #finsih this todo

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    website = db.Column(db.String(500))
    seeking_talent=db.Column(db.Boolean)
    seeking_description=db.Column(db.String(500))
    show_a = db.relationship("Show",backref="Artist")
    

    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    #finish this todo
class Show(db.Model):
  __tablename__="SHow"
  id=db.Column(db.Integer, primary_key=True)
  venu_id=db.Column(db.Integer, db.ForeignKey('Venue.id'))
  artist_id=db.Column(db.Integer, db.ForeignKey('Artist.id'))
  start_time= db.Column(db.String(120))
  past_show=db.Column(db.Boolean)
  #venu= db.relationship("Venue",backref="Show")


# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
db.create_all()
#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#


def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  # finish this todo
  data_v=db.session.query(Venue).all()
  data_city=db.session.query(Venue.city,Venue.state).all()
  data=[]
  for city,state in set(data_city):
    data.append({
    "city": city,
    "state": state,
    "venues":db.session.query(Venue).filter_by(city=city).all()
    })
  
  return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  #finish this todo
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  search_word=request.form.get("search_term").upper()
  data_search=db.session.query(Venue).all()
  data_show=[]
  for i in data_search:
    if search_word in i.name.upper():
      data_show.append(i)
  response={
    "count": len(data_show),
    "data": [{"id": i.id,"name": i.name,"num_upcoming_shows": len(list(filter(lambda x:x.past_show==False,i.show)))} for i in data_show]
  }
  return render_template('pages/search_venues.html', results=response, search_term=search_term)

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  #finish this todo
  data=db.session.query(Venue).filter_by(id=venue_id).all()
  data_f=[]
  for data_s in data:
    past_show_list=list(filter(lambda x:x.past_show==True,data_s.show))
    upcoming_show_list=list(filter(lambda x:x.past_show==False,data_s.show))
    data_f.append({
    "id": data_s.id,
    "name": data_s.name,
    "genres": data_s.genres,
    "address": data_s.address,
    "city": data_s.city,
    "state": data_s.state,
    "phone": data_s.phone,
    "website": data_s.website,
    "facebook_link":data_s.facebook_link,
    "seeking_talent": data_s.seeking_talent,
    "seeking_description": data_s.seeking_description,
    "image_link": data_s.image_link,
    "past_shows":past_show_list ,
    "upcoming_shows": upcoming_show_list,
    "past_shows_count": len(past_show_list),
    "upcoming_shows_count": len(upcoming_show_list),
    })
  data = list(filter(lambda d: d['id'] == venue_id, data_f))[0]
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  #finish this todo
  # TODO: modify data to be the data object returned from db insertio
  # i do not understand this
  try:
    name=request.form.get("name")
    city=request.form.get("city")
    state=request.form.get("state")
    address = request.form.get("address")
    phone = request.form.get("phone")
    image_link = request.form.get(" image_link")
    facebook_link = request.form.get("facebook_link")
    genres = request.form["genres"]
    website = request.form.get("website")
    seeking_talent=request.form.get("seeking_talent")
    seeking_description=request.form.get("seeking_description")
    venue=Venue(name=name,city=city,
    state=state,address=address,
    phone=phone,image_link=image_link,
    facebook_link=facebook_link,
    genres=genres,website=website,
    seeking_talent=seeking_talent,
    seeking_description=seeking_description)  
    db.session.add(venue)
    
    # on successful db insert, flash success
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
    # TODO: on unsuccessful db insert, flash an error instead.
    #finish this todo
  except:
    db.session.rollback()  
    flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  finally:
    db.session.commit()
    # # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  #finish this todo
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  data=db.session.query(Venue).filter_by(id=venue_id).first()
  db.session.delete(data)
  db.session.commit()
  print("delete")
  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  #finish this todo
  # clicking that button delete it from the db then redirect the user to the homepage
  return redirect(url_for("index"))

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  #finish this todo
  
  data=db.session.query(Artist).all()
  print(data)
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  #finish this todo
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  search_word=request.form.get("search_term").upper()
  data_search=db.session.query(Artist).all()
  data_show=[]
  for i in data_search:
    if search_word in i.name.upper():
      data_show.append(i)
  response={
    "count": len(data_show),
    "data": [{"id": i.id,"name": i.name,"num_upcoming_shows": len(list(filter(lambda x:x.past_show==False,i.show_a)))} for i in data_show]
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  #finish this todo
  data=db.session.query(Artist).filter_by(id=artist_id).all()
  data_f=[]
  for data_s in data:
    past_show_list=list(filter(lambda x:x.past_show==True,data_s.show_a))
    upcoming_show_list=list(filter(lambda x:x.past_show==False,data_s.show_a))
    data_f.append({
    "id": data_s.id,
    "name": data_s.name,
    "genres": data_s.genres,
    "address": data_s.address,
    "city": data_s.city,
    "state": data_s.state,
    "phone": data_s.phone,
    "website": data_s.website,
    "facebook_link":data_s.facebook_link,
    "seeking_talent": data_s.seeking_talent,
    "seeking_description": data_s.seeking_description,
    "image_link": data_s.image_link,
    "past_shows":past_show_list ,
    "upcoming_shows": upcoming_show_list,
    "past_shows_count": len(past_show_list),
    "upcoming_shows_count": len(upcoming_show_list),
    })
  
  data = list(filter(lambda d: d['id'] == artist_id, data_f))[0]
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  # TODO: populate form with fields from artist with ID <artist_id>
  # i do not understand this todo
  return render_template('forms/edit_artist.html', form=form)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  #finish this todo
  # artist record with ID <artist_id> using the new attributes
  data=db.session.query(Artist).filter_by(id=artist_id).first()
  data.name=request.form.get("name")
  data.city=request.form.get("city")
  data.state=request.form.get("state")
  data.address = request.form.get("address")
  data.phone = request.form.get("phone")
  data.image_link = request.form.get(" image_link")
  data.facebook_link = request.form.get("facebook_link")
  data.genres = request.form["genres"]
  data.website = request.form.get("website")
  data.seeking_talent=request.form.get("seeking_talent")
  data.seeking_description=request.form.get("seeking_description")
  db.session.commit()
  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
 
  # TODO: populate form with values from venue with ID <venue_id>
  # i do not under stand this todo
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  #finish this todo
  # venue record with ID <venue_id> using the new attributes
  data=db.session.query(Venue).filter_by(id=venue_id).first()
  data.name=request.form.get("name")
  data.city=request.form.get("city")
  data.state=request.form.get("state")
  data.address = request.form.get("address")
  data.phone = request.form.get("phone")
  data.image_link = request.form.get(" image_link")
  data.facebook_link = request.form.get("facebook_link")
  data.genres = request.form["genres"]
  data.website = request.form.get("website")
  data.seeking_talent=request.form.get("seeking_talent")
  data.seeking_description=request.form.get("seeking_description")
  db.session.commit()
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()

  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  #finish this todo
  # TODO: modify data to be the data object returned from db insertion
  try:
     name=request.form.get("name")
     city=request.form.get("city")
     state=request.form.get("state")
     address = request.form.get("address")
     phone = request.form.get("phone")
     image_link = request.form.get(" image_link")
     facebook_link = request.form.get("facebook_link")
     genres = request.form.get("genres")
     website = request.form.get("website")
     seeking_talent=True
     seeking_description=request.form.get("seeking_description")
     if seeking_description is None:
          seeking_talent=False
    artist=Artist(name=name,city=city,
    state=state,address=address,
    phone=phone,image_link=image_link,
    facebook_link=facebook_link,
    genres=genres,website=website,
    seeking_talent=seeking_talent,
    seeking_description=seeking_description)
    db.session.add(artist)
    
    # on successful db insert, flash success
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
    # TODO: on unsuccessful db insert, flash an error instead.
    #finish this todo
  except:
    db.session.rollback()  
    flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  finally:
    db.session.commit()
    # # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    # on successful db insert, flash success
  
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., 
 
  return render_template('pages/home.html')  
 
 
 

#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  #finish this todo
  show_data=db.session.query(Show).all()
  data=[]
  for i in show_data:
    data.append({
    "venue_id": i.venu_id,
    "venue_name": i.Venue.name,
    "artist_id": i.artist_id,
    "artist_name": i.Artist.name,
    "artist_image_link": i.Artist.image_link,
    "start_time": i.start_time
    })
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  venueid=request.form.get("venue_id")
  print(venueid)
  artistid=request.form.get("artist_id")
  starttime=request.form.get("start_time")
  start_time=datetime.strptime(starttime,"%Y-%m-%d %H:%M:%S")
  if start_time >= datetime.today():
    past_show=False
  else:
    past_show=True
  print(past_show)
  show=Show(venu_id=venueid,
  artist_id= artistid,
  start_time=starttime,
  past_show= past_show)
  db.session.add(show)
  db.session.commit()
  # on successful db insert, flash success
  flash('Show was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
