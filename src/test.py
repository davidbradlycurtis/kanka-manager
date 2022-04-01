import requests
import yaml
import json
import os
import sys
import logging
from kankaclient.client import KankaClient

logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s')
LOGGER = logging.getLogger('KankaManagement')

class SpaceDumper(yaml.SafeDumper):
    # HACK: insert blank lines between top-level objects
    # inspired by https://stackoverflow.com/a/44284819/3786245
    def write_line_break(self, data=None):
        super().write_line_break(data)

        if len(self.indents) == 1:
            super().write_line_break('# ============================================================================================\n')

def write_data(file, data):
    success = False
    if os.path.isfile(file):
        try:
            with open(file, 'w') as output_yaml:
                output_yaml.write(yaml.dump(data, Dumper=SpaceDumper, sort_keys=False))
            success = True
        except FileNotFoundError:
            pass
            #LOG ERROR
    return success

def read_data(file):
    data = None
    if os.path.isfile(file):
        try:
            with open(file, 'r') as input_yaml:
                data = yaml.safe_load(input_yaml.read())
        except FileNotFoundError:
            pass
            #LOG ERROR
    return data

token = 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxIiwianRpIjoiNjUxYzNkNDk1ZjVjZTUzMWQxMjc3MTk5Y2NlMzE1N2U4ZTFkMzZlOWRiYWZiOTY1ZGEyYmI5MTVkZjhkZDFkNTNkZGZlNDhmZTFmZWMzYjMiLCJpYXQiOjE2NDY0NTU3MDguMDA2Mjc4LCJuYmYiOjE2NDY0NTU3MDguMDA2MjgzLCJleHAiOjE2Nzc5OTE3MDcuOTk1NDY5LCJzdWIiOiIzMzM2MiIsInNjb3BlcyI6W119.BsK_qRFoPIlDnNG7DemtD_cVfN98LS-i3f9QUhfm_J7mS7_ltzuJ3typrPL_4lyqbnkrjjx0r5oICRqvgs902AmIDzt-bCGxsyesMWGQcQXFfoahGyJlYfRe4QSNsjlj3cLsM22dn0limMtnKB0I-7XcrbmNU15UJAN0MYJDOZ2pfCmjpn-5GnhgJQNwZrCZc33afUZSVvN_FAYT54GMPExMY0z1J1Zo49uUfs6FQhSG_SNrQ8zbPArCaGgH9hwMIEEhk0dn8-Kv-7SjJu1y4utWs3i9F08-WmIZ9YjDerJsrySc_N6TCgFn2GIeEnb_c-S3RpG4K3PMCTSrOGIKvy_S5zLYZOn6lNXaJ2RTaOhpZvHQHX_OeccoRJ5H9_K5ma1DXBPWaXgujCdaAi5S860ZRqsa8OUSQvHEsq03TNaOKupImBSKLGN6r3Qc57iBTfk6VrOIAO3cFG5Qej7t0gKQdpkDDPAK8dnLvC9QxrfKQCJcfwOrXz7dmUNb-XAKydU2brpqRzJyP3EScShrwPpYgXvE1BJNxtejpPhpE8GCM5TS6-qmHymHILYG0SsoM5HMrA70vFGu3DAJVkRzRavGEBsh_0mFzKR64zNT4hFFEzLyLha5c0FnkgKIFjUfZyrmskRW0t0DifJF5ZGX95PRezeNQHpRZ4yM5G3YseQ'
campaign = 'Journey to Morrivir'
kanka_client = KankaClient(token=token, campaign=campaign, verbose=True)
characters = kanka_client.characters.get_characters()
print()



# camp_id = 107538
# base_url = 'https://kanka.io/api/1.0/campaigns'
# char_url = '%s/%s/characters' % (base_url, camp_id)
# header = {'Authorization': token, 'Content-type': 'application/json'}
# result = requests.get(url=char_url, headers=header)
# if result.reason == 'OK':
#     _characters = json.loads(result.text)['data']

# characters = list()
# for char in _characters:
#     character = {
#         "id" : char.get('id', None),
#         "name" : char.get('name', None),
#         "entry" : char.get('entry', None),
#         "entry_parsed" : char.get('entry_parsed', None),
#         "image" : char.get('image', None),
#         "image_full" : char.get('image_full', None),
#         "image_thumb" : char.get('image_thumb', None),
#         "is_private" : char.get('is_private', None),
#         "tags" : char.get('tags', []),
#         "title" : char.get('title', None),
#         "age" : char.get('age', None),
#         "pronouns" : char.get('pronouns', None),
#         "type" : char.get('type', None),
#         "family_id" : char.get('family_id', None),
#         "location_id" : char.get('location_id', None),
#         "races" : char.get('races', []),
#         "is_dead" : char.get('is_dead', None),
#         "image_url" : char.get('image_url', None),
#         "personality_name" : char.get('personality_name', []),
#         "personality_entry" : char.get('personality_entry', []),
#         "appearance_name" : char.get('appearance_name', []),
#         "appearance_entry" : char.get('appearance_entry', []),
#         "is_personality_visible" : char.get('is_personality_visible', None),
#     }
#     # Prep character for dump
#     for field in character.copy():
#         if character[field] == None or character[field] == []:
#             del character[field]
#     del character['id']
#     characters.append(character)
# file = 'C:\\Users\\quazn\\Documents\\dev\\kanka-manager\\morrivir\\characters.yaml'
# code = write_data(file, characters)   
# file_characters = read_data(file)

#print(file_characters)