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
                        endangered species
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

    @application.route('/mammal/<mammal_id>')
    def get_mammal_detail(mammal_id):
        neo4j_connection = Neo4jConnection(constants.DB_URI, constants.DB_USER, constants.DB_PASSWORD)

        # mammal info + all mammal prey, predator and competitors
        # TODO: SYNC eol_ecoregion mammal and wikipedia mammal
        mammal_info = neo4j_connection.execute('''
            MATCH (n:mammal__species)-[:mammal__subspecies]->(subs)
            WHERE ID(n) = ''' + mammal_id + ''' 
            WITH n, COLLECT(subs) as subspecies
            OPTIONAL MATCH (n)-[:mammal__prey]->(prey)
            WITH n, subspecies, COLLECT([id(prey), prey.mammal__name, prey.mammal__taxonName]) as preys
            OPTIONAL MATCH (n)-[:mammal__predator]->(pred)
            WITH n, subspecies, preys, COLLECT([id(pred), pred.mammal__name, pred.mammal__taxonName]) as predators
            OPTIONAL MATCH (n)-[:mammal__competitor]->(comp)
            RETURN n, subspecies, preys, predators, 
                COLLECT([id(comp), comp.mammal__name, comp.mammal__taxonName]) as competitors
        ''')

        # non-mammal prey, predator and competitors
        non_mammal_info = neo4j_connection.execute('''
            MATCH (n:mammal__species)-[:non_mammal__prey]->(prey)
            WHERE ID(n) = ''' + mammal_id + ''' 
            WITH n, COLLECT(prey) as nm_preys
            OPTIONAL MATCH (n)-[:non_mammal__predator]->(pred)
            WITH n, nm_preys, COLLECT(pred) as nm_predators
            OPTIONAL MATCH (n)-[:non_mammal__competitor]->(comp)
            RETURN nm_preys, nm_predators, COLLECT(comp) as nm_competitors
        ''')

        # ecoregion id and name
        ecoregion_info = neo4j_connection.execute('''
            MATCH (n:mammal__species)-[:mammal__ecoregion]->(ecoregion)
            WHERE ID(n) = ''' + mammal_id + ''' 
            RETURN COLLECT([ID(ecoregion), ecoregion.ecoregion__name]) as ecoregions
        ''')

        neo4j_connection.close()
        return jsonify({**mammal_info[0], **non_mammal_info[0], **ecoregion_info[0]}) \
            if len(mammal_info) > 0 and len(non_mammal_info) > 0 and len(ecoregion_info) > 0 \
            else jsonify({'error': 'Invalid id'})

    @application.route('/ecoregion/<ecoregion_id>')
    def get_ecoregion_detail(ecoregion_id):
        neo4j_connection = Neo4jConnection(constants.DB_URI, constants.DB_USER, constants.DB_PASSWORD)
        ecoregion_info = neo4j_connection.execute('''
            OPTIONAL MATCH (n:ecoregion__ecoregion)-[:non_mammal__flora]->(flora)
            WHERE ID(n) = ''' + ecoregion_id + ''' 
            WITH n, COLLECT(flora) as floras
            OPTIONAL MATCH (n)-[:mammal__fauna_mammal]->(fauna_mammal)
            WITH n, floras, COLLECT([ID(fauna_mammal), fauna_mammal.mammal__name]) as fauna_mammals
            OPTIONAL MATCH (n)-[:non_mammal__fauna]->(fauna_non_mammal)
            WITH n, floras, fauna_mammals, COLLECT(fauna_non_mammal) as fauna_non_mammals
            OPTIONAL MATCH (n)-[:mammal__fauna_mammal_subs]->(fauna_mammal_sub)
            RETURN n, floras, fauna_mammals, fauna_non_mammals, COLLECT(fauna_mammal_sub) as fauna_mammal_subs
        ''')
        neo4j_connection.close()
        return jsonify(ecoregion_info[0]) if len(ecoregion_info) > 0 else jsonify({'error': 'Invalid id'})

    return application


application = start_server()
