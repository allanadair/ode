#!/usr/bin/env python
"""
This script imports listing information from a csv file and inserts the data
into a spatially-enabled listings table within a PostgreSQL database.
"""
import argparse
import csv
import logging
from ode.models import Listing
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def listings(csv_file, table):
    """
    Generator function for yielding listings from csv.

    :param csv_file: path to a csv file
    :type csv_file: string
    :param table: table name
    :type table: string
    """
    with open(csv_file, 'r') as csvfd:
        reader = csv.reader(csvfd)
        header = next(reader)
        for row in reader:
            record = dict(zip(header, row))
            listing = Listing(id=record.get('id'),
                              street=record.get('street'),
                              status=record.get('status'),
                              price=record.get('price'),
                              bedrooms=record.get('bedrooms'),
                              bathrooms=record.get('bathrooms'),
                              sq_ft=record.get('sq_ft'),
                              geom='SRID=4326;POINT({0} {1})'.format(record.get('lng'),
                                                                     record.get('lat')))
            yield listing


if __name__ == '__main__':
    # Argument parser
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('csv', type=str, help='path to the listing csv file')
    parser.add_argument('--engine_url', type=str,
                        default='postgresql:///listings',
                        help='string that indicates database dialect and '
                             'connection arguments')
    parser.add_argument('--append', action='store_true',
                        help='append listing data to an existing table')
    args = parser.parse_args()

    # Logger
    logger = logging.getLogger(__file__)
    formatter = logging.Formatter('%(levelname)s, %(name)s, %(message)s')
    logger.setLevel(logging.INFO)

    # Create console handler and set level
    ch = logging.StreamHandler()
    ch.setLevel(logger.level)

    # Add formatter to ch
    ch.setFormatter(formatter)

    # Add ch to loggers
    logger.addHandler(ch)

    try:
        # Create engine and Session class
        engine = create_engine(args.engine_url)
        Session = sessionmaker(bind=engine)

        if not engine.has_table(Listing.__tablename__):
            # We want to create a new table
            logger.info('Creating listings')
            Listing.__table__.create(engine)
            logger.info('Inserting listing records')
            session = Session()
            session.add_all(listings(csv_file=args.csv,
                                     table=Listing.__tablename__))
            session.commit()

        elif engine.has_table(Listing.__tablename__) and args.append:
            # Table exists and we want to append to it
            logger.info('Inserting listing records')
            session = Session()
            session.add_all(listings(csv_file=args.csv,
                                     table=Listing.__tablename__))
            session.commit()

        else:
            # Do nothing
            logger.info('listings table already exists')

    except Exception as e:
        logger.critical(e)
