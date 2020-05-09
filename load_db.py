from dateutil.parser import parse

from app import Venue, Artist, Show, db

# v1 = Venue(
#     name='The Musical Hop',
#     genres=', '.join(["Jazz", "Reggae", "Swing", "Classical", "Folk"]),
#     address='1015 Folsom Street',
#     city='San Francisco',
#     state='CA',
#     phone='123-123-1234',
#     website='https://www.themusicalhop.com',
#     facebook_link='https://www.facebook.com/TheMusicalHop',
#     seeking_talent=True,
#     seeking_description='We are on the lookout for a local artist to play every two weeks. Please call us.',
#     image_link='https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80'
# )

# v2 = Venue(
#     name='Park Square Live Music & Coffee',
#     genres=', '.join(["Rock n Roll", "Jazz", "Classical", "Folk"]),
#     address='34 Whiskey Moore Ave"',
#     city='San Francisco',
#     state='CA',
#     phone='415-000-1234',
#     website='https://www.parksquarelivemusicandcoffee.com',
#     facebook_link='https://www.facebook.com/ParkSquareLiveMusicAndCoffee',
#     seeking_talent=False,
#     image_link='https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80'
# )

# v3 = Venue(
#     name='The Dueling Pianos Bar',
#     genres=', '.join(["Classical", "R&B", "Hip-Hop"]),
#     address='335 Delancey Street',
#     city='New York',
#     state='NY',
#     phone='914-003-1132',
#     website='https://www.theduelingpianos.com',
#     facebook_link='https://www.facebook.com/theduelingpianos',
#     seeking_talent=False,
#     image_link='https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80'
# )

# a1 = Artist(
#     name='Guns N Petals',
#     genres='Rock n Roll',
#     city='San Francisco',
#     state='CA',
#     phone='326-123-5000',
#     website='https://www.gunsnpetalsband.com',
#     facebook_link='https://www.facebook.com/GunsNPetals',
#     seeking_venue=True,
#     seeking_description='Looking for shows to perform at in the San Francisco Bay Area!',
#     image_link='https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80'
# )

# a2 = Artist(
#     name='Matt Quevedo',
#     genres='Jazz',
#     city='New York',
#     state='NY',
#     phone='300-400-5000',
#     facebook_link='https://www.facebook.com/mattquevedo923251523',
#     seeking_venue=False,
#     image_link='https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80'
# )

# a3 = Artist(
#     name='The Wild Sax Band',
#     genres=', '.join(["Jazz", "Classical"]),
#     city='San Francisco',
#     state='CA',
#     phone='432-325-5432',
#     seeking_venue=False,
#     image_link='https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80'
# )

# s1 = Show(
#     start_time = parse('2019-05-21T21:30:00.000Z'),
#     artist_id = 1,
#     venue_id = 1
# )
#
# s2 = Show(
#     start_time = parse('2019-06-15T23:00:00.000Z'),
#     artist_id = 2,
#     venue_id = 3
# )
#
# s3 = Show(
#     start_time = parse('2035-04-01T20:00:00.000Z'),
#     artist_id = 3,
#     venue_id = 3
# )
#
# s4 = Show(
#     start_time = parse('2035-04-08T20:00:00.000Z'),
#     artist_id = 3,
#     venue_id = 3
# )
#
# s5 = Show(
#     start_time = parse('2035-04-15T20:00:00.000Z'),
#     artist_id = 3,
#     venue_id = 3
# )

# db.session.add(v1)
# db.session.add(v2)
# db.session.add(v3)
# db.session.add(a1)
# db.session.add(a2)
# db.session.add(a3)
# db.session.add(s1)
# db.session.add(s2)
# db.session.add(s3)
# db.session.add(s4)
# db.session.add(s5)
#
# db.session.commit()