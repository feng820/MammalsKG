from utils.db_connection import Neo4jConnection
from utils import constants
import json
from json.decoder import JSONDecodeError
from flask import Flask, jsonify, request


def start_server():
    application = Flask(__name__)

    @application.route('/search')
    def search_mammal():
        """
            request parameters:
                keyword: user-typed search keyword
                status: animal endangered status
                    status_list = {
                        least concern
                        vulnerable
                        critically endangered
                        extinct species
                        near threatened
                        extinct in the wild
                    }
                mass_range: mass range(kg) in [min, max] format
                length_range: length range(m) in [min, max] format
                lifespan_range: animal life(years) span in [min, max] format

            :return list of animal names
        """
        keyword = request.args.get('keyword')
        status = request.args.get('status')
        mass_range = request.args.get('mass_range')
        length_range = request.args.get('length_range')
        lifespan_range = request.args.get('lifespan_range')

        if not keyword:
            keyword = ''

        neo4j_connection = Neo4jConnection(constants.DB_URI, constants.DB_USER, constants.DB_PASSWORD)
        query = 'MATCH (n: mammal__species) ' \
                'WHERE (toLower(n.mammal__name) CONTAINS "' \
                + keyword.lower() + '" OR toLower(n.mammal__commonNames) CONTAINS "' \
                + keyword.lower() + '")'

        if status:
            query += ' AND n.mammal__status = "' + status + '"'

        if mass_range:
            try:
                mass_range = json.loads(mass_range)
                query += ' AND n.mammal__eol_mass > ' + str(mass_range[0]) + \
                         ' AND n.mammal__eol_mass < ' + str(mass_range[1])
            except JSONDecodeError as e:
                print(e)

        if length_range:
            try:
                length_range = json.loads(length_range)
                query += ' AND n.mammal__eol_length > ' + str(length_range[0]) + \
                         ' AND n.mammal__eol_length < ' + str(length_range[1])
            except JSONDecodeError as e:
                print(e)

        if lifespan_range:
            try:
                lifespan_range = json.loads(lifespan_range)
                query += ' AND n.mammal__eol_life_span > ' + str(lifespan_range[0]) + \
                         ' AND n.mammal__eol_life_span < ' + str(lifespan_range[1])
            except JSONDecodeError as e:
                print(e)

        query += ' RETURN n.mammal__name, n.mammal__commonNames, ID(n)'
        print(query)

        result = neo4j_connection.execute(query)
        neo4j_connection.close()

        return jsonify(result)

    @application.route('/detail/<mammal_id>')
    def get_mammal_detail(mammal_id):
        pass

    application.run()


if __name__ == '__main__':
    start_server()
