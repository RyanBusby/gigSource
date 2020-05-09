import json
import dateutil.parser
import babel
import logging
from datetime import datetime as dt
from logging import Formatter, FileHandler

from flask import Flask, render_template, request, Response, flash, redirect, url_for, abort
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import Form
from flask_migrate import Migrate

from forms import *

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Show(db.Model):
    __tablename__ = 'Show'
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, nullable=False)
    artist_id = db.Column(
        db.Integer,
        db.ForeignKey('Artist.id'),
        nullable=False
    )
    venue_id = db.Column(
        db.Integer,
        db.ForeignKey('Venue.id'),
        nullable=False
    )

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    genres = db.Column(db.String(), nullable=True)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    website = db.Column(db.String(), nullable=True)
    image_link = db.Column(db.String(500), nullable=True)
    facebook_link = db.Column(db.String(120), nullable=True)
    seeking_talent = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(), nullable=True)
    shows = db.relationship('Show', backref='venue')

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120), nullable=True)
    state = db.Column(db.String(120), nullable=True)
    phone = db.Column(db.String(120), nullable=True)
    genres = db.Column(db.String(120), nullable=True)
    image_link = db.Column(db.String(500), nullable=True)
    facebook_link = db.Column(db.String(120), nullable=True)
    website = db.Column(db.String(), nullable=True)
    seeking_venue = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(), nullable=True)
    shows = db.relationship('Show', backref='artist')

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

@app.route('/')
def index():
  return render_template('pages/home.html')

#  Venues
#  ---------------------------------------------------------------
@app.route('/venues')
def venues():
    data =\
    [
        {
            'city': area.city,
            'state': area.state,
            'venues':
            [
                {
                    'id': venue.id,
                    'name': venue.name,
                    'num_upcoming_shows':\
                        Show.query\
                        .filter_by(venue_id=venue.id)\
                        .filter(Show.start_time > dt.now())\
                        .count()
                }
                for venue in Venue.query\
                .filter_by(city=area.city)\
                .filter_by(state=area.state)\
                .all()
            ]
        } for area in Venue.query\
        .with_entities(
            Venue.city,
            Venue.state
        )\
        .group_by(
            Venue.state,
            Venue.city
        ).all()
    ]
    return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  search_term = request.form.get('search_term')
  results =\
  Venue.query.filter(Venue.name.ilike(f'%{search_term}%')).all()
  response = {
    "count": len(results),
    "data":
        [
            {
                "id": result.id,
                "name": result.name,
                "num_upcoming_shows": Show.query\
                    .filter_by(venue_id=result.id)\
                    .filter(Show.start_time > dt.now())\
                    .count(),
            } for result in results
        ]
  }
  return render_template(
    'pages/search_venues.html',
    results=response,
    search_term=request.form.get('search_term', '')
)

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    venue = Venue.query.get(venue_id)
    venue.genres = venue.genres.split(',')
    upcoming_shows = Show.query.with_entities(
        Artist.id,
        Artist.name,
        Artist.image_link,
        Show.start_time
    ).join(Artist)\
    .filter(Show.venue_id==venue_id)\
    .filter(Show.start_time > dt.now())\
    .all()
    past_shows = Show.query.with_entities(
        Artist.id,
        Artist.name,
        Artist.image_link,
        Show.start_time
    ).join(Artist)\
    .filter(Show.venue_id==venue_id)\
    .filter(Show.start_time < dt.now())\
    .all()
    venue.upcoming_shows = [
        {
            'artist_id': show[0],
            'artist_name': show[1],
            'artist_image_link': show[2],
            'start_time': str(show[3])
        }
        for show in upcoming_shows
    ]
    venue.upcoming_shows_count = len(upcoming_shows)
    venue.past_shows = [
        {
            'artist_id': show[0],
            'artist_name': show[1],
            'artist_image_link': show[2],
            'start_time': str(show[3])
        }
        for show in past_shows
    ]
    venue.past_shows_count = len(past_shows)

    return render_template('pages/show_venue.html', venue=venue)

#  Create Venue
#  ---------------------------------------------------------------
@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    new_venue = Venue()
    new_venue.__dict__.update(request.form) # this doesn't work on update
    genres = ', '.join(request.form.getlist('genres'))
    new_venue.genres = genres
    if 'seeking_talent' in request.form:
        new_venue.seeking_talent = True
    else:
        new_venue.seeking_talent = False
    try:
        db.session.add(new_venue)
        db.session.commit()
        flash(f'Venue {new_venue.name} was successfully listed!')
    except:
        flash(f'An error occurred. Venue {new_venue.name} could not be listed.')
        db.session.rollback()
    finally:
        db.session.close()
    return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['POST'])
def delete_venue(venue_id):
    try:
        v = Venue.query.get(venue_id)
        db.session.delete(v)
        db.session.commit()
        flash(f'Venue {v.name} was successfully removed.')
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return render_template('pages/home.html')

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  data = Artist.query.all()
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
    search_term = request.form.get('search_term')
    results =\
    Artist.query.filter(Artist.name.ilike(f'%{search_term}%')).all()
    response = {
    "count": len(results),
    "data":
        [
            {
                "id": result.id,
                "name": result.name,
                "num_upcoming_shows": Show.query\
                    .filter_by(artist_id=result.id)\
                    .filter(Show.start_time > dt.now())\
                    .count(),
            } for result in results
        ]
    }
    return render_template(
    'pages/search_venues.html',
    results=response,
    search_term=request.form.get('search_term', '')
    )

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    artist = Artist.query.get(artist_id)
    artist.genres = artist.genres.split(',')
    upcoming_shows = Show.query.with_entities(
        Venue.id,
        Venue.name,
        Venue.image_link,
        Show.start_time
    ).join(Venue)\
    .filter(Show.artist_id==artist_id)\
    .filter(Show.start_time > dt.now())\
    .all()
    past_shows = Show.query.with_entities(
        Venue.id,
        Venue.name,
        Venue.image_link,
        Show.start_time
    ).join(Venue)\
    .filter(Show.artist_id==artist_id)\
    .filter(Show.start_time < dt.now())\
    .all()
    artist.upcoming_shows = [
        {
            'venue_id': show[0],
            'venue_name': show[1],
            'venue_image_link': show[2],
            'start_time': str(show[3])
        }
        for show in upcoming_shows
    ]
    artist.upcoming_shows_count = len(upcoming_shows)
    artist.past_shows = [
        {
            'venue_id': show[0],
            'venue_name': show[1],
            'venue_image_link': show[2],
            'start_time': str(show[3])
        }
        for show in past_shows
    ]
    artist.past_shows_count = len(past_shows)
    return render_template('pages/show_artist.html', artist=artist)

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    new_artist = Artist()
    new_artist.__dict__.update(request.form)
    genres = ', '.join(request.form.getlist('genres'))
    new_artist.genres = genres
    if 'seeking_venue' in request.form:
        new_artist.seeking_venue = True
    else:
        new_artist.seeking_venue = False
    try:
        db.session.add(new_artist)
        db.session.commit()
        flash(f'{new_artist.name} is now listed!')
    except:
        flash(f'An error occurred. {new_artist.name} could not be listed.')
        db.session.rollback()
    finally:
        db.session.close()
    return render_template('pages/home.html')

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()
    artist = Artist.query.get(artist_id)
    return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    edit_artist =  Artist.query.get(artist_id)
    for key, value in request.form.items():
        setattr(edit_artist, key, value)
    genres = ', '.join(request.form.getlist('genres'))
    edit_artist.genres = genres
    if 'seeking_venue' in request.form:
        edit_artist.seeking_venue = True
    else:
        edit_artist.seeking_venue = False
    try:
        db.session.commit()
        flash(f'{edit_artist.name} successfully updated!')
    except:
        flash(f'{edit_artist.name} was not updated.')
        db.session.rollback()
    finally:
        db.session.close()
    return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()
    venue = Venue.query.get(venue_id)
    return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    edit_venue =  Venue.query.get(venue_id)
    for key, value in request.form.items():
        setattr(edit_venue, key, value)
    genres = ', '.join(request.form.getlist('genres'))
    edit_venue.genres = genres
    if 'seeking_talent' in request.form:
        edit_venue.seeking_venue = True
    else:
        edit_venue.seeking_venue = False
    try:
        db.session.commit()
        flash(f'{edit_venue.name} successfully updated!')
    except:
        flash(f'{edit_venue.name} was not updated.')
        db.session.rollback()
    finally:
        db.session.close()
    return redirect(url_for('show_venue', venue_id=venue_id))


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    data = [
        {
            'venue_id': show.venue_id,
            'venue_name': show.venue.name,
            'artist_id': show.artist_id,
            'artist_name': show.artist.name,
            'artist_image_link': show.artist.image_link,
            'start_time': str(show.start_time)
        }
        for show in Show.query.join(Artist).join(Venue).all()
    ]
    return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    new_show = Show(
        artist_id = request.form['artist_id'],
        venue_id = request.form['venue_id'],
        start_time = request.form['start_time']
    )
    try:
        db.session.add(new_show)
        db.session.commit()
        flash('Show was successfully listed!')
    except:
        db.session.rollback()
        flash('An error occurred. Show could not be listed.')
    finally:
        db.session.close()
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

# Default port:
if __name__ == '__main__':
    app.run(debug=True)
