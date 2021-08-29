#!/usr/bin/env python
# -*- coding: utf-8 -*-

import bz2
import sqlite3
import tempfile
from pkg_resources import resource_filename
from pyowm.weatherapi25.location import Location

CITY_ID_DB_PATH = 'cityids/cities.db.bz2'


class CityIDRegistry:

    MATCHINGS = {
        'exact': "SELECT city_id, name, country, state, lat, lon FROM city WHERE name=?",
        'like': r"SELECT city_id, name, country, state, lat, lon FROM city WHERE name LIKE ?"
    }

    def __init__(self, sqlite_db_path: str):
        self.connection = self.__decompress_db_to_memory(sqlite_db_path)

    @classmethod
    def get_instance(cls):
        """
        Factory method returning the default city ID registry
        :return: a `CityIDRegistry` instance
        """
        return CityIDRegistry(CITY_ID_DB_PATH)

    def __decompress_db_to_memory(self, sqlite_db_path: str):
        """
        Decompresses to memory the SQLite database at the provided path
        :param sqlite_db_path: str
        :return: None
        """
        # https://stackoverflow.com/questions/3850022/how-to-load-existing-db-file-to-memory-in-python-sqlite3
        # https://stackoverflow.com/questions/32681761/how-can-i-attach-an-in-memory-sqlite-database-in-python
        # https://pymotw.com/2/bz2/

        # read and uncompress data from compressed DB
        res_name = resource_filename(__name__, sqlite_db_path)
        bz2_db = bz2.BZ2File(res_name)
        decompressed_data = bz2_db.read()

        # dump decompressed data to a temp DB
        with tempfile.NamedTemporaryFile(mode='wb') as tmpf:
            tmpf.write(decompressed_data)
            tmpf_name = tmpf.name

            # read temp DB to memory and return handle
            src_conn = sqlite3.connect(tmpf_name)
            dest_conn = sqlite3.connect(':memory:')
            src_conn.backup(dest_conn)
            src_conn.close()
            return dest_conn

    def __query(self, sql_query: str, *args):
        """
        Queries the DB with the specified SQL query
        :param sql_query: str
        :return: list of tuples
        """
        cursor = self.connection.cursor()
        try:
            return cursor.execute(sql_query, args).fetchall()
        finally:
            cursor.close()

    def ids_for(self, city_name, country=None, state=None, matching='like'):
        """
        Returns a list of tuples in the form (city_id, name, country, state, lat, lon )
        The rule for querying follows the provided `matching` parameter value.
        If `country` is provided, the search is restricted to the cities of
        the specified country, and an even stricter search when `state` is provided as well
        :param city_name: the string toponym of the city to search
        :param country: two character str representing the country where to
        search for the city. Defaults to `None`, which means: search in all
        countries.
        :param state: two character str representing the state where to
        search for the city. Defaults to `None`. When not `None` also `state` must be specified
        :param matching: str. Default is `like`. Possible values:
        `exact` - literal, case-sensitive matching
        `like` - matches cities whose name contains, as a substring, the string
        fed to the function, case-insensitive,
        :raises ValueError if the value for `matching` is unknown
        :return: list of tuples
        """
        if not city_name:
            return []
        if matching not in self.MATCHINGS:
            raise ValueError("Unknown type of matching: "
                             "allowed values are %s" % ", ".join(self.MATCHINGS))
        if country is not None and len(country) != 2:
            raise ValueError("Country must be a 2-char string")
        if state is not None and country is None:
            raise ValueError("A country must be specified whenever a state is specified too")

        q = self.MATCHINGS[matching]
        if matching == 'exact':
            params = [city_name]
        else:
            params = ['%' + city_name + '%']

        if country is not None:
            q = q + ' AND country=?'
            params.append(country)

        if state is not None:
            q = q + ' AND state=?'
            params.append(state)

        rows = self.__query(q, *params)
        return rows

    def locations_for(self, city_name, country=None, state=None, matching='like'):
        """
        Returns a list of `Location` objects
        The rule for querying follows the provided `matching` parameter value.
        If `country` is provided, the search is restricted to the cities of
        the specified country, and an even stricter search when `state` is provided as well
        :param city_name: the string toponym of the city to search
        :param country: two character str representing the country where to
        search for the city. Defaults to `None`, which means: search in all
        countries.
        :param state: two character str representing the state where to
        search for the city. Defaults to `None`. When not `None` also `state` must be specified
        :param matching: str. Default is `like`. Possible values:
        `exact` - literal, case-sensitive matching
        `like` - matches cities whose name contains, as a substring, the string
        fed to the function, case-insensitive,
        :raises ValueError if the value for `matching` is unknown
        :return: list of `Location` objects
        """
        items = self.ids_for(city_name, country=country, state=state, matching=matching)
        return [Location(item[1], item[5], item[4], item[0], country=item[2]) for item in items]

    def geopoints_for(self, city_name, country=None, state=None, matching='like'):
        """
        Returns a list of ``pyowm.utils.geo.Point`` objects corresponding to
        the int IDs and relative toponyms and 2-chars country of the cities
        matching the provided city name.
        The rule for identifying matchings is according to the provided
        `matching` parameter value.
        If `country` is provided, the search is restricted to the cities of
        the specified country.
        :param city_name: the string toponym of the city to search
        :param country: two character str representing the country where to
        search for the city. Defaults to `None`, which means: search in all
        countries.
        :param state: two character str representing the state where to
        search for the city. Defaults to `None`. When not `None` also `state` must be specified
        :param matching: str. Default is `nocase`. Possible values:
        `exact` - literal, case-sensitive matching
        `like` - matches cities whose name contains, as a substring, the string
        fed to the function, case-insensitive,
        :raises ValueError if the value for `matching` is unknown
        :return: list of `pyowm.utils.geo.Point` objects
        """
        locations = self.locations_for(city_name, country=country, state=state, matching=matching)
        return [loc.to_geopoint() for loc in locations]
