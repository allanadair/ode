"""
ode module

A simple Flask application with geospatial capability
"""
from .models import Listing
from flask import Flask, json, jsonify, request
from geoalchemy2.elements import WKTElement
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker

# Flask initialization
app = Flask(__name__)

# Database stuff
engine = create_engine('postgresql:///listings')
Session = sessionmaker(bind=engine)


@app.route('/listings', methods=['GET'])
def listings():
    """
    GET request handler for listings.
    """
    if request.method == 'GET':
        # get the request arguments
        min_price = request.args.get('min_price')
        max_price = request.args.get('max_price')
        min_bed = request.args.get('min_bed')
        max_bed = request.args.get('max_bed')
        min_bath = request.args.get('min_bath')
        max_bath = request.args.get('max_bath')
        min_x = request.args.get('min_x')
        min_y = request.args.get('min_y')
        max_x = request.args.get('max_x')
        max_y = request.args.get('max_y')

        # new empty feature collection
        feature_collection = {'type': 'FeatureCollection',
                              'features': []}
        session = Session()
        query = session.query(Listing)
        if min_price:
            query = query.filter(Listing.price >= min_price)
        if max_price:
            query = query.filter(Listing.price <= max_price)
        if min_bed:
            query = query.filter(Listing.bedrooms >= min_bed)
        if max_bed:
            query = query.filter(Listing.bedrooms <= max_bed)
        if min_bath:
            query = query.filter(Listing.bathrooms >= min_bath)
        if max_bath:
            query = query.filter(Listing.bathrooms <= max_bath)
        if min_x and min_y and max_x and max_y:
            polygon = 'POLYGON(({min_x} {min_y}, {min_x} {max_y}, ' \
                                       '{max_x} {max_y}, {max_x} {min_y}, ' \
                                       '{min_x} {min_y}))'.format(min_x=min_x,
                                                                  min_y=min_y,
                                                                  max_x=max_x,
                                                                  max_y=max_y)
            query = query.filter(Listing.geom.ST_Intersects(WKTElement(polygon,
                                                                       srid=4326)))

        for row in query.all():
            properties = {'id': row.id,
                          'price': row.price,
                          'street': row.street,
                          'bedrooms': row.bedrooms,
                          'bathrooms': row.bathrooms,
                          'sq_ft': row.sq_ft}
            geometry = json.loads(session.scalar(row.geom.ST_AsGeoJSON()))
            listing = {'type': 'Feature',
                       'geometry': geometry,
                       'properties': properties}
            feature_collection['features'].append(listing)
        return jsonify(feature_collection)
    return bad_request()


@app.errorhandler(404)
def not_found(error=None):
    """
    Custom JSON error handler for not found.
    """
    # NOTE: This is a quick and dirty approach.
    message = {'message': 'Not found: {0}'.format(request.url)}
    response = jsonify(message)
    response.status_code = 404
    return response


@app.errorhandler(400)
def bad_request(error=None):
    """
    Custom JSON error handler for bad request.
    """
    # NOTE: This is a quick and dirty approach.
    message = {'message': 'Bad request: {0}'.format(request.url)}
    response = jsonify(message)
    response.status_code = 400
    return response
