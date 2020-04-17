# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#

import babel
import dateutil.parser
import logging
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from logging import Formatter, FileHandler

from forms import *

# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)


# DONE: connect to a local postgresql database

# ----------------------------------------------------------------------------#
# Models.
# ----------------------------------------------------------------------------#


# DONE: implement any missing fields, as a database migration using Flask-Migrate


# venuegenres = db.Table('venuegenre',
#                        db.Column('genre_id', db.Integer, db.ForeignKey('Genre.id'), primary_key=True),
#                        db.Column('venue_id', db.Integer, db.ForeignKey('Venue.id'), primary_key=True)
#                        )

# DONE: implement any missing fields, as a database migration using Flask-Migrate
class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(120))
    shows = db.relationship('Show', backref='venue', lazy=True)

    # genres = db.relationship('Genre', secondary=venuegenres, lazy='subquery', backref=db.backref('Venues', lazy=True))

    def __repr__(self):
        return f'<Venue {self.id} -  {self.name}, {self.city}/{self.state}>'


# artistgenres = db.Table('artistgenre',
#                         db.Column('genre_id', db.Integer, db.ForeignKey('Genre.id'), primary_key=True),
#                         db.Column('artist_id', db.Integer, db.ForeignKey('Artist.id'), primary_key=True)
#                         )


class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(120))
    shows = db.relationship('Show', backref='artist', lazy=True)
    # genres = db.relationship('Genre', secondary=artistgenres, lazy='subquery', backref=db.backref('Artists', lazy=True))


# shows = db.Table('Show',
#                  db.Column('id', db.Integer, primary_key=True),
#                  db.Column('venue_id', db.Integer, db.ForeignKey('Venue.id'), primary_key=True),
#                  db.Column('artist_id', db.Integer, db.ForeignKey('Artist.id'), primary_key=True),
#                  db.Column('start_time', db.DateTime, nullable=False)
#                  )

# DONE Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
class Show(db.Model):
    __tablename__ = 'Show'

    id = db.Column(db.Integer, primary_key=True)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)


# class Genre(db.Model):
#     __tablename__ = 'Genre'
#
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(30), nullable=False)


# ----------------------------------------------------------------------------#
# Filters.
# ----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
    date = value
    if type(value) != datetime:
        date = dateutil.parser.parse(value)

    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime


# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#

@app.route('/')
def index():
    return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
    # DONE: replace with real venues data.
    #       num_shows should be aggregated based on number of upcoming shows per venue.

    # With help from the knowledge - https://knowledge.udacity.com/questions/112669
    cities = Venue.query.with_entities(Venue.city, Venue.state).group_by(Venue.city, Venue.state).all()

    data = []
    for city in cities:
        city_venues = Venue.query.filter_by(state=city.state).filter_by(city=city.city).all()
        venues = []
        for venue in city_venues:
            venues.append({
                "id": venue.id,
                "name": venue.name,
                "num_upcoming_shows": len(db.session.query(Show).filter(Show.venue_id == venue.id).filter(
                    Show.start_time > datetime.now()).all())
            })

        data.append({
            "city": city.city,
            "state": city.state,
            "venues": venues
        })

    return render_template('pages/venues.html', areas=data);


@app.route('/venues/search', methods=['POST'])
def search_venues():
    # DONE: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
    search_term = request.form.get('search_term', '')
    venues = Venue.query.filter(Venue.name.like(f"%{search_term}%")).all()
    count = len(venues)
    data = []
    for venue in venues:
        data.append({
            "id": venue.id,
            "name": venue.name,
            "num_upcoming_shows": len(
                db.session.query(Show).filter(Show.venue_id == venue.id).filter(Show.start_time > datetime.now()).all())
        })

    response = {"count": count, "data": data}

    return render_template('pages/search_venues.html', results=response, search_term=search_term)


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    # DONE: replace with real venue data from the venues table, using venue_id
    data = Venue.query.get(venue_id)
    data.genres = [Genres[v].value for v in data.genres.split(", ")]
    data.upcoming_shows = db.session.query(Show).filter(Show.venue_id == venue_id).filter(
        Show.start_time > datetime.now()).all()
    for show in data.upcoming_shows:
        setattr(show, 'artist_name', show.artist.name)
        setattr(show, 'artist_image_link', show.artist.image_link)
    data.past_shows = db.session.query(Show).filter(Show.venue_id == venue_id).filter(
        Show.start_time <= datetime.now()).all()
    for show in data.past_shows:
        setattr(show, 'artist_name', show.artist.name)
        setattr(show, 'artist_image_link', show.artist.image_link)
    data.past_shows_count = len(data.past_shows)
    data.upcoming_shows_count = len(data.upcoming_shows)

    return render_template('pages/show_venue.html', venue=data)


#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    # DONE: insert form data as a new Venue record in the db, instead
    # DONE: modify data to be the data object returned from db insertion
    form = VenueForm()
    print(request.form.getlist('genres'));
    if not form.validate():
        flash(form.errors)
        return redirect(url_for('create_venue_form'))

    try:
        venue = Venue(name=request.form.get('name'), city=request.form.get('city'), state=request.form.get('state'),
                      address=request.form.get('address'), phone=request.form.get('phone'),
                      facebook_link=request.form.get('facebook_link'), genres=", ".join(request.form.getlist('genres')),
                      website=request.form.get('website'), image_link=request.form.get('image_link'),
                      seeking_talent=request.form.get('seeking_talent') == 'True',
                      seeking_description=request.form.get('seeking_description'))
        db.session.add(venue)
        db.session.commit()
        # on successful db insert, flash success
        # on successful db insert, flash success
        flash('Venue ' + request.form['name'] + ' was successfully listed!')
    except:
        # DONE: on unsuccessful db insert, flash an error instead.
        # e.g.,flash('An error occurred. Venue ' + data.name + ' could not be listed.')
        flash('An error occurred. Venue ' + venue.name + ' could not be listed.')
    finally:
        db.session.close()

    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return render_template('pages/home.html')


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    # DONE: Complete this endpoint for taking a venue_id, and using
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
    try:
        Venue.query.filter_by(id=venue_id).delete()
        db.session.commit()
        flash(f"Venue with id= {venue_id} has been successfully deleted.")
    except:
        db.session.rollback()
        flash(f"Unable to delete venue {venue_id}.")
    finally:
        db.session.close()
    # DONE: BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage
    return redirect(url_for('venues'))


#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
    # DONE: replace with real data returned from querying the database

    data = Artist.query.with_entities(Artist.id, Artist.name)

    return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    # DONE: implement search on artists with partial string search. Ensure it is case-insensitive.
    # search for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".
    search_term = request.form.get('search_term', '')
    artists = Artist.query.filter(Artist.name.like(f"%{search_term}%")).all()
    count = len(artists)
    data = []
    for artist in artists:
        data.append({
            "id": artist.id,
            "name": artist.name,
            "num_upcoming_shows": len(
                db.session.query(Show).filter(Show.artist_id == artist.id).filter(
                    Show.start_time > datetime.now()).all())
        })

    response = {"count": count, "data": data}

    return render_template('pages/search_artists.html', results=response, search_term=search_term)


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    # shows the artist page with the given artist_id
    # DONE: replace with real artist data from the artist table, using artist_id
    data = Artist.query.get(artist_id)
    data.genres = [Genres[v].value for v in data.genres.split(", ")]
    data.upcoming_shows = db.session.query(Show).filter(Show.artist_id == artist_id).filter(
        Show.start_time > datetime.now()).all()
    for show in data.upcoming_shows:
        setattr(show, 'venue_name', show.venue.name)
        setattr(show, 'venue_image_link', show.venue.image_link)
    data.past_shows = db.session.query(Show).filter(Show.artist_id == artist_id).filter(
        Show.start_time <= datetime.now()).all()
    for show in data.past_shows:
        setattr(show, 'venue_name', show.venue.name)
        setattr(show, 'venue_image_link', show.venue.image_link)
    data.past_shows_count = len(data.past_shows)
    data.upcoming_shows_count = len(data.upcoming_shows)

    return render_template('pages/show_artist.html', artist=data)


#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()
    artist = Artist.query.get(artist_id)
    artist.genres = artist.genres.split(", ")
    # DONE: populate form with fields from artist with ID <artist_id>
    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    # DONE: take values from the form submitted, and update existing
    # artist record with ID <artist_id> using the new attributes
    try:
        artist = Artist.query.get(artist_id)
        if not artist:
            abort(404)
        artist.name = request.form['name']
        artist.city = request.form['city']
        artist.state = request.form['state']
        artist.phone = request.form['phone']
        artist.genres = ", ".join(request.form.getlist('genres'))
        artist.facebook_link = request.form['facebook_link']
        artist.image_link = request.form['image_link']
        artist.website = request.form['website']
        artist.seeking_venue = request.form['seeking_venue'] == 'True'
        artist.seeking_description = request.form['seeking_description']
        db.session.commit()
        flash('Success!')
    except:
        db.session.rollback()
        flash(f'Could not update artist with id = {artist_id}')
    finally:
        db.session.close()

    return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()
    venue = Venue.query.get(venue_id)
    venue.genres = venue.genres.split(", ")
    # DONE: populate form with values from venue with ID <venue_id>
    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    # DONE: take values from the form submitted, and update existing
    # venue record with ID <venue_id> using the new attributes
    try:
        venue = Venue.query.get(venue_id)
        if not venue:
            return abort(404)
        venue.name = request.form['name']
        venue.city = request.form['city']
        venue.state = request.form['state']
        venue.address = request.form['address']
        venue.phone = request.form['phone']
        venue.genres = ", ".join(request.form.getlist('genres'))
        venue.facebook_link = request.form['facebook_link']
        venue.image_link = request.form['image_link']
        venue.website = request.form['website']
        venue.seeking_talent = request.form['seeking_talent'] == 'True'
        venue.seeking_description = request.form['seeking_description']
        print(venue)
        db.session.commit()
        flash('Success!')
    except:
        db.session.rollback()
        flash(f'Could not update venue with id = {venue_id}')
    finally:
        db.session.close()
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
    # DONE: insert form data as a new Artist record in the db, instead
    # DONE: modify data to be the data object returned from db insertion //?
    try:
        artist = Artist(name=request.form.get('name'), city=request.form.get('city'), state=request.form.get('state'),
                        phone=request.form.get('phone'), facebook_link=request.form.get('facebook_link'),
                        genres=", ".join(request.form.getlist('genres')), website=request.form.get('website'),
                        image_link=request.form.get('image_link'),
                        seeking_venue=request.form.get('seeking_venue') == 'True',
                        seeking_description=request.form.get('seeking_description'))
        db.session.add(artist)
        db.session.commit()
        # on successful db insert, flash success
        flash('Artist ' + request.form['name'] + ' was successfully listed!')
    except e:
        # DONE: on unsuccessful db insert, flash an error instead.
        # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
        print(e)
        flash('An error occurred. Artist ' + artist.name + ' could not be listed.')
    finally:
        db.session.close()

    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    # displays list of shows at /shows
    # DONE: replace with real venues data.
    #       num_shows should be aggregated based on number of upcoming shows per venue.
    all_shows = Show.query.all()

    for show in all_shows:
        setattr(show, 'artist_name', show.artist.name)
        setattr(show, 'artist_image_link', show.artist.image_link)
        setattr(show, 'venue_name', show.venue.name)
    return render_template('pages/shows.html', shows=all_shows)


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing form
    # DONE: insert form data as a new Show record in the db, instead
    form = ShowForm()
    if not form.validate():
        flash(form.errors)
        return redirect(url_for('create_shows'))

    try:
        new_show = Show(artist_id=request.form.get('artist_id'), venue_id=request.form.get('venue_id'),
                        start_time=request.form.get('start_time'))
        db.session.add(new_show)
        db.session.commit()
        # on successful db insert, flash success
        flash('Show was successfully listed!')
    except:
        db.session.rollback()
        # DONE: on unsuccessful db insert, flash an error instead.
        # e.g., flash('An error occurred. Show could not be listed.')
        # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
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

# ----------------------------------------------------------------------------#
# Launch.
# ----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
