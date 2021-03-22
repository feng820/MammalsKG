import json
from rdflib import Graph, URIRef, Literal, XSD, Namespace, RDF

SCHEMA = Namespace('http://schema.org/')
MAMMAL = Namespace('http://mammal.org/mammalnamespace#')
NON_MAMMAL = Namespace('http://non-mammal.org/non-mammalnamespace#')
ECOREGION = Namespace('http://ecoregion.org/ecoregionnamespace#')


def construct_triples():
    my_kg = Graph()
    my_kg.bind('schema', SCHEMA)
    my_kg.bind('mammal', MAMMAL)
    my_kg.bind('non_mammal', NON_MAMMAL)
    my_kg.bind('ecoregion', ECOREGION)

    with open('species_class.json', 'r') as f_in:
        species_dict = json.load(f_in)
        for key, info_dict in species_dict.items():
            uri = MAMMAL.__getitem__(key)
            my_kg.add((uri, RDF.type, MAMMAL['species']))
            my_kg.add((uri, MAMMAL.taxonName, Literal(info_dict['taxonName'])))
            my_kg.add((uri, MAMMAL.status, Literal(info_dict['status'])))
            my_kg.add((uri, MAMMAL.commonNames, Literal(info_dict['commonNames'])))
            for subspecies_id in info_dict['subspecies']:
                my_kg.add((uri, MAMMAL.subspecies, MAMMAL[subspecies_id]))

            # eol
            my_kg.add((uri, MAMMAL.eol_mass, Literal(info_dict['eol_mass'], datatype=XSD.double)))
            my_kg.add((uri, MAMMAL.eol_length, Literal(info_dict['eol_length'], datatype=XSD.double)))
            my_kg.add((uri, MAMMAL.eol_life_span, Literal(info_dict['eol_life_span'], datatype=XSD.double)))
            my_kg.add((uri, MAMMAL.eol_geographic_distribution, Literal(info_dict['eol_geographic_distribution'])))
            my_kg.add((uri, MAMMAL.img, Literal(info_dict['img'])))
            for predator_id in info_dict['predator']:
                if 'NM' in predator_id:
                    my_kg.add((uri, NON_MAMMAL.predator, NON_MAMMAL[predator_id]))
                else:
                    my_kg.add((uri, MAMMAL.predator, MAMMAL[predator_id]))
            if len(info_dict['predator']) == 0:
                my_kg.add((uri, NON_MAMMAL.predator, Literal(None)))
                my_kg.add((uri, MAMMAL.predator, Literal(None)))

            for prey_id in info_dict['prey']:
                if 'NM' in prey_id:
                    my_kg.add((uri, NON_MAMMAL.prey, NON_MAMMAL[prey_id]))
                else:
                    my_kg.add((uri, MAMMAL.prey, MAMMAL[prey_id]))
            if len(info_dict['prey']) == 0:
                my_kg.add((uri, NON_MAMMAL.predator, Literal(None)))
                my_kg.add((uri, MAMMAL.predator, Literal(None)))

            for competitor_id in info_dict['competitor']:
                if 'NM' in competitor_id:
                    my_kg.add((uri, NON_MAMMAL.competitor, NON_MAMMAL[competitor_id]))
                else:
                    my_kg.add((uri, MAMMAL.competitor, MAMMAL[competitor_id]))
            if len(info_dict['competitor']) == 0:
                my_kg.add((uri, NON_MAMMAL.predator, Literal(None)))
                my_kg.add((uri, MAMMAL.predator, Literal(None)))

            for ecoregion_id in info_dict['ecoregion']:
                my_kg.add((uri, MAMMAL.ecoregion, ECOREGION[ecoregion_id]))

            # adw
            my_kg.add((uri, MAMMAL.Habitat_Regions, Literal(info_dict['Habitat_Regions'])))
            my_kg.add((uri, MAMMAL.Terrestrial_Biomes, Literal(info_dict['Terrestrial_Biomes'])))
            my_kg.add((uri, MAMMAL.Wetlands, Literal(info_dict['Wetlands'])))
            my_kg.add((uri, MAMMAL.Communication_Channels, Literal(info_dict.get('Communication_Channels', []))))
            my_kg.add((uri, MAMMAL.Animal_Foods, Literal(info_dict['Animal_Foods'])))
            my_kg.add((uri, MAMMAL.Plant_Foods, Literal(info_dict['Plant_Foods'])))
            my_kg.add((uri, MAMMAL.Key_Behaviors, Literal(info_dict['Key_Behaviors'])))
            my_kg.add((uri, MAMMAL.Range_mass, Literal(info_dict['Range_mass'])))
            my_kg.add((uri, MAMMAL.Range_length, Literal(info_dict['Range_length'])))
            my_kg.add((uri, MAMMAL.Average_lifespan_wild, Literal(info_dict['Average_lifespan_wild'])))
            my_kg.add((uri, MAMMAL.Average_lifespan_captivity, Literal(info_dict['Average_lifespan_captivity'])))

    with open('non_mammal_class.json', 'r') as f_in:
        non_mammal_dict = json.load(f_in)
        for key, info_dict in non_mammal_dict.items():
            uri = NON_MAMMAL.__getitem__(key)
            my_kg.add((uri, RDF.type, NON_MAMMAL['non_mammal']))
            my_kg.add((uri, NON_MAMMAL.name, Literal(info_dict['name'])))
            my_kg.add((uri, NON_MAMMAL.taxonName, Literal(info_dict['taxonName'])))
            my_kg.add((uri, NON_MAMMAL.icon, Literal(info_dict['icon'])))

    with open('ecoregion_class_new.json', 'r') as f_in:
        ecoregion_dict = json.load(f_in)
        for key, info_dict in ecoregion_dict.items():
            uri = ECOREGION.__getitem__(key)
            my_kg.add((uri, RDF.type, ECOREGION['ecoregion']))
            my_kg.add((uri, ECOREGION.name, Literal(info_dict['name'])))
            my_kg.add((uri, ECOREGION.coordinates, Literal(info_dict['coordinates'])))
            my_kg.add((uri, ECOREGION.url, Literal(info_dict['url'])))
            my_kg.add((uri, ECOREGION.image, Literal(info_dict.get('image', ''))))
            my_kg.add((uri, ECOREGION.Biome, Literal(info_dict.get('Biome', ''))))
            my_kg.add((uri, ECOREGION.Area, Literal(info_dict.get('Area', ''))))
            my_kg.add((uri, ECOREGION.Country, Literal(info_dict.get('Country', ''))))
            my_kg.add((uri, ECOREGION.Conservation_status, Literal(info_dict.get('Conservation_status', ''))))

            for flora_id in info_dict['flora']:
                if 'NM' in flora_id:
                    my_kg.add((uri, NON_MAMMAL.flora, NON_MAMMAL[flora_id]))
            if len(info_dict['flora']) == 0:
                my_kg.add((uri, NON_MAMMAL.flora, Literal(None)))

            for fauna_id in info_dict['fauna']:
                if 'NM' in fauna_id:
                    my_kg.add((uri, NON_MAMMAL.fauna, NON_MAMMAL[fauna_id]))
            if len(info_dict['fauna']) == 0:
                my_kg.add((uri, NON_MAMMAL.fauna_non_mammal, Literal(None)))

            for mammals_id in info_dict['mammals']:
                if 'Q' in mammals_id:
                    my_kg.add((uri, MAMMAL.fauna_mammal, MAMMAL[mammals_id]))
            if len(info_dict['mammals']) == 0:
                my_kg.add((uri, MAMMAL.fauna_mammal, Literal(None)))

            for mammals_subs_id in info_dict['mammals_subs']:
                if 'Q' in mammals_subs_id:
                    my_kg.add((uri, MAMMAL.fauna_mammal_subs, MAMMAL[mammals_subs_id]))
            if len(info_dict['mammals_subs']) == 0:
                my_kg.add((uri, MAMMAL.fauna_mammal_subs, Literal(None)))

    with open('subspecies_class.json', 'r') as f_in:
        subspecies_dict = json.load(f_in)
        for key, info_dict in subspecies_dict.items():
            uri = MAMMAL.__getitem__(key)
            my_kg.add((uri, RDF.type, MAMMAL['subspecies']))
            my_kg.add((uri, MAMMAL.name, Literal(info_dict['name'])))
            my_kg.add((uri, MAMMAL.taxonName, Literal(info_dict['taxonName'])))
            my_kg.add((uri, MAMMAL.location_info, Literal(info_dict['location_info'])))

    my_kg.serialize('mammals_kg.ttl', format="turtle")


if __name__ == '__main__':
    construct_triples()
