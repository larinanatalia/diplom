from pprint import pprint
import requests
import json
import time
from tqdm import tqdm

class PhotoUploader:
    def __init__(self, user_id, token):
        self.user_id = user_id
        self.token = token

    def vk(self):

        folder_name = input(str('Enter folder name: '))
        headers = {'Authorization': self.token}
        params_folder = {'path': folder_name}
        resp_folder = requests.put('https://cloud-api.yandex.net/v1/disk/resources',
                            headers=headers, params=params_folder)
        resp_get_folder = resp_folder.json()

        params_folder_info = {'path': folder_name}
        resp_folder_info_get = requests.get('https://cloud-api.yandex.net/v1/disk/resources',
                                 headers=headers, params=params_folder_info)
        resp_folder_info = resp_folder_info_get.json()
        files_names_old = list()
        info_photos = resp_folder_info['_embedded']['items']
        for info in info_photos:
            files_names_old.append(int(info['name']))

        params = {
            'owner_id': self.user_id,
            'album_id': 'profile',
            'rev': 1,
            'extended': 1,
            'photo_sizes': 1,
            'count': 6,
            'access_token': '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++',
            'v': 5.122
        }
        response = requests.get('https://api.vk.com/method/photos.get', params=params)
        resp_photos = response.json()
        photos = resp_photos['response']['items']

        names_list = list()
        count = 0
        for photo in photos:
            title = photo['likes']['count']
            title_date = photo['date']
            if title in files_names_old:
                title = title_date
            if title in names_list:
                title = f'{title}_{title_date}'
            urls = list()
            for size in photo['sizes']:
                size['full_s'] = size['height'] * size['width']
                urls.append([size['full_s'],size['url']])
            fastest_id = max(urls)[1]
            count += 1
            params_uplink = {'path': f'{folder_name}/{title}',
                                 'url': fastest_id}
            resp = requests.post('https://cloud-api.yandex.net/v1/disk/resources/upload',
                                headers=headers, params=params_uplink)
            names_list.append(title)
            for i in tqdm(range(count), desc=f'Photo {title}.jpg is loading'):
                time.sleep(0.1)

