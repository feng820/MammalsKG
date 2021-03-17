import wikipedia
import json
import sys
import spacy
import en_core_web_lg
from spacy.matcher import Matcher


# https://stackoverflow.com/questions/3368969/find-string-between-two-substrings
def find_between(s, first, last):
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return None


def find_between_r(s, first, last):
    try:
        start = s.rindex(first) + len(first)
        end = s.rindex(last, start)
        return s[start:end]
    except ValueError:
        return None


def load_json(ecoregion_info):
    # Opening JSON file
    id_data = {}
    with open(ecoregion_info) as json_file:
        data = json.load(json_file)
        for key in data:
            id_data[key] = data[key]
    json_file.close()
    return id_data


def store_json(id_data, ecoregion_info_plus):
    for id in id_data:
        name = id_data[id]['name']
        flora_fauna = parse_page(name)
        id_data[id].update(flora_fauna)

    out_file = open(ecoregion_info_plus, 'w')
    json.dump(id_data, out_file)
    out_file.close()
    return


def parse_page(name):
    try:
        page = wikipedia.page(name)
    except wikipedia.exceptions.PageError as e:
        print(e)
        return {'flora': [], 'fauna': []}

    print(page.url)
    page_content = page.content

    # 找到下一个标题之间的内容
    flora = find_between(page_content, "== Flora ==", "\n== ")
    fauna = find_between(page_content, "== Fauna ==", "\n== ")
    if flora:
        flora_words = nlp(flora)
    else:
        flora_words = []
    if fauna:
        fauna_words = nlp(fauna)
    else:
        fauna_words = []

    out_dict = {'flora': flora_words, 'fauna': fauna_words}
    return out_dict


def nlp(content):
    nlp = en_core_web_lg.load()
    matcher = Matcher(nlp.vocab)
    p1 = [
        {'POS': 'PROPN'},
        {'POS': 'VERB'},
    ]
    p2 = [
        {'POS': 'PROPN'},
        {'POS': 'NOUN'},
    ]
    p3 = [
        {'POS': 'ADJ', 'OP': '*'},
        {'POS': 'PROPN', 'OP': '*'},
        {'POS': 'NOUN', 'OP': '*'},
        {'ORTH': "("},
        {'IS_ALPHA': True, 'OP': '+'},
        {'ORTH': ")"},
    ]

    matcher.add('science_name', [p1, p2, p3])
    doc = nlp(content)
    phrase_matches = matcher(doc)

    spans = [doc[start:end] for match_id, start, end in phrase_matches]
    spans = spacy.util.filter_spans(spans)

    out_list = []
    for span in spans:
        span = str(span)
        if '(' in span and ')' in span:
            taxonName = find_between(span, "(", ")")
            name = find_between(span, "", " (")
        else:
            taxonName = span
            name = None

        d = {'name': name, 'taxonName': taxonName}
        out_list.append(d)

    return out_list


def main(argv):
    ecoregion_info = "./ecoregion_info.json"
    ecoregion_info_plus = "./ecoregion_info_plus.json"

    id_data = load_json(ecoregion_info)
    store_json(id_data, ecoregion_info_plus)


if __name__ == "__main__":
    main(sys.argv[1:])
