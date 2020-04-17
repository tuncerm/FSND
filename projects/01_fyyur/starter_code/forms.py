from datetime import datetime
from enum import Enum
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField
from wtforms.validators import DataRequired, AnyOf, URL, Regexp, ValidationError, Length, Optional


def check_multiple(form, field):
    error = False
    for genre in field.data:
        if not Genres[genre]:
            error = True
            break

    print(field.data)
    if error:
        raise ValidationError('Genre does not exist')


class Genres(Enum):
    Alternative = 'Alternative'
    Blues = 'Blues'
    Classical = 'Classical'
    Country = 'Country'
    Electronic = 'Electronic'
    Folk = 'Folk'
    Funk = 'Funk'
    HipHop = 'Hip-Hop'
    HeavyMetal = 'Heavy Metal'
    Instrumental = 'Instrumental'
    Jazz = 'Jazz'
    MusicalTheatre = 'Musical Theatre'
    Pop = 'Pop'
    Punk = 'Punk'
    RnB = 'R&B'
    Reggae = 'Reggae'
    RockNRoll = 'Rock n Roll'
    Soul = 'Soul'
    Other = 'Other'

    @classmethod
    def choices(cls):
        return tuple((c.name, c.value) for c in cls)


class States(Enum):
    AL = 'AL'
    AK = 'AK'
    AZ = 'AZ'
    AR = 'AR'
    CA = 'CA'
    CO = 'CO'
    CT = 'CT'
    DE = 'DE'
    DC = 'DC'
    FL = 'FL'
    GA = 'GA'
    HI = 'HI'
    ID = 'ID'
    IL = 'IL'
    IN = 'IN'
    IA = 'IA'
    KS = 'KS'
    KY = 'KY'
    LA = 'LA'
    ME = 'ME'
    MT = 'MT'
    NE = 'NE'
    NV = 'NV'
    NH = 'NH'
    NJ = 'NJ'
    NM = 'NM'
    NY = 'NY'
    NC = 'NC'
    ND = 'ND'
    OH = 'OH'
    OK = 'OK'
    OR = 'OR'
    MD = 'MD'
    MA = 'MA'
    MI = 'MI'
    MN = 'MN'
    MS = 'MS'
    MO = 'MO'
    PA = 'PA'
    RI = 'RI'
    SC = 'SC'
    SD = 'SD'
    TN = 'TN'
    TX = 'TX'
    UT = 'UT'
    VT = 'VT'
    VA = 'VA'
    WA = 'WA'
    WV = 'WV'
    WI = 'WI'
    WY = 'WY'

    @classmethod
    def choices(cls):
        return tuple((s.name, s.value) for s in cls)


class ShowForm(FlaskForm):
    artist_id = StringField('artist_id')
    venue_id = StringField('venue_id')
    start_time = DateTimeField('start_time', validators=[DataRequired()], default=datetime.today())


class VenueForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    city = StringField('city', validators=[DataRequired()])
    state = SelectField('state', validators=[DataRequired()], choices=States.choices())
    address = StringField('address', validators=[DataRequired()])
    phone = StringField('phone', validators=[Regexp(r"^\d{3}-\d{3}-\d{4}$")])
    image_link = StringField('image_link', validators=[DataRequired()])
    # DONE implement enum restriction
    genres = SelectMultipleField('genres', validators=[DataRequired(), check_multiple], choices=Genres.choices())
    facebook_link = StringField('facebook_link', validators=[Optional(), URL()])
    website = StringField('website', validators=[Optional(), URL()])
    seeking_talent = SelectField('seeking_talent', choices=[('False', 'No'), ('True', 'Yes')])
    seeking_description = StringField('seeking_description', validators=[Optional(), Length(max=120)])


class ArtistForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    city = StringField('city', validators=[DataRequired()])
    state = SelectField('state', validators=[DataRequired()], choices=States.choices())
    # DONE implement validation logic for state
    phone = StringField('phone', validators=[Regexp(r"^\d{3}-\d{3}-\d{4}$")])
    image_link = StringField('image_link')
    # DONE implement enum restriction
    genres = SelectMultipleField('genres', validators=[DataRequired(), check_multiple], choices=Genres.choices())
    # DONE implement enum restriction
    facebook_link = StringField('facebook_link', validators=[Optional(), URL()])
    website = StringField('website', validators=[Optional(), URL()])
    seeking_venue = SelectField('seeking_venue', choices=[('False', 'No'), ('True', 'Yes')])
    seeking_description = StringField('seeking_description', validators=[Optional(), Length(max=120)])

# DONE IMPLEMENT NEW ARTIST FORM AND NEW SHOW FORM
