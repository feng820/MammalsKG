import wikipedia
from bs4 import BeautifulSoup
import requests
import json
import re
import sys
import spacy
import en_core_web_lg
import en_core_web_sm
from spacy.matcher import Matcher


def parse_page(name):
    page = wikipedia.page(name)
    print(page.url)
    page_content = page.content
    # print(page_content)
    nlp(page_content)


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
    print(spans)


def test_nlp():
    nlp = en_core_web_lg.load()
    matcher = Matcher(nlp.vocab)
    pattern = [{"LOWER": "hello"}, {"LOWER": "world"}]
    matcher.add("HelloWorld", [pattern])
    doc = nlp("hello world!")
    matches = matcher(doc)
    print(matches)


def token_label():
    nlp = en_core_web_lg.load()
    doc = nlp("At lowest elevations the forests are characterized by the sclerophyllous evergreen holm oak (Quercus "
              "ilex) and cork oak (Quercus suber), coniferous stone pine (Pinus pinea), and the decidous trees "
              "Quercus pubescens, Fraxinus ornus, and Ostrya carpinifolia.")
    # doc = nlp("Large mammals include roe deer (Capreolus capreolus), European wildcat (Felis silvestris), and crested "
    #           "porcupine (Hystrix cristata). The Italian wolf (Canis lupus italicus) lives in the peninsular portion "
    #           "of the ecoregion, and Sila and Pollino national parks are home to Italy's largest wolf population. "
    #           "Wolves are absent from Sicily.")
    # doc = nlp("North-facing plant communities: On north-facing slopes Silver fir (Abies alba) and European beech ("
    #           "Fagus sylvatica) mix with Pinus nigra subsp. larico.")
    doc = nlp("Indian grey hornbill (Ocyceros birostris), and Oriental pied hornbill (Anthracoceros "
              "albirostris).Wetlands along the Ganges River and its tributaries support communities of resident and "
              "migrant waterfowl, along with mugger crocodile (Crocodylus palustris) and gharial (Gavialis "
              "gangeticus).")

    # for ent in doc.ents:
    #     print(f'{ent.text:15s} [{ent.label_}]')

    # for match_id, start, end in phrase_matches:
    #     string_id = nlp.vocab.strings[match_id]
    #     span = doc[start:end]
    #     print(match_id, string_id, start, end, span.text)

    for token in doc:
        print(token.text, token.pos_)




def main(argv):
    ecoregion_info = "./ecoregion_info.json"

    # name = "Southern Andean steppe"
    # name = "South Apennine mixed montane forests"
    name = "Upper Gangetic Plains moist deciduous forests"
    parse_page(name)

    # test_nlp()
    # token_label()


if __name__ == "__main__":
    main(sys.argv[1:])
