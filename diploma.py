from pprint import pprint
import requests
import json
import time
from tqdm import tqdm
from urllib.parse import urlencode
import hashlib

class PhotoUploader:
    def __init__(self, user_id, token):
        self.user_id = user_id
        self.token = token

    def new_folder(self):
        folder_name = input(str('Enter folder name: '))
        headers = {'Authorization': self.token}
        params_folder = {'path': folder_name}
        resp_folder = requests.put('https://cloud-api.yandex.net/v1/disk/resources',
                                   headers=headers, params=params_folder)

        headers = {'Authorization': self.token}
        params_folder_info = {'path': folder_name}
        resp_folder_info_get = requests.get('https://cloud-api.yandex.net/v1/disk/resources',
                                            headers=headers, params=params_folder_info)
        resp_folder_info = resp_folder_info_get.json()
        files_names_old = list()
        info_photos = resp_folder_info['_embedded']['items']
        for info in info_photos:
            files_names_old.append(int(info['name']))
        return folder_name, files_names_old

    def uploading(self, folder_name, title, pic_max):
        headers = {'Authorization': self.token}
        params_uplink = {'path': f'{folder_name}/{title}',
                         'url': pic_max}
        resp = requests.post('https://cloud-api.yandex.net/v1/disk/resources/upload',
                             headers=headers, params=params_uplink)

    def vk(self):
        folder_name = self.new_folder()
        params = {
            'owner_id': self.user_id,
            'album_id': 'profile',
            'rev': 1,
            'extended': 1,
            'photo_sizes': 1,
            'count': 6,
            'access_token': '+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++',
            'v': 5.122
        }
        response = requests.get('https://api.vk.com/method/photos.get', params=params)
        resp_photos = response.json()
        photos = resp_photos['response']['items']
        files_names_old = folder_name[1]
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
            pic_max = max(urls)[1]
            count += 1
            self.uploading(folder_name[0], title, pic_max)
            names_list.append(title)
            for i in tqdm(range(count), desc=f'Photo {title}.jpg is loading'):
                time.sleep(0.1)

    def ok(self):
        folder_name = self.new_folder()
        application_key = '+++++++++++++++++++'
        count = 5
        fid = self.user_id
        fields = 'user_photo.PIC_MAX, user_photo.LIKE_COUNT, photo.ID'
        format = 'json'
        method = 'photos.getPhotos'
        secret_key = '++++++++++++++++++++++++++++++++'
        access_token = '++++++++++++++++++++++++++++++++++++++++'
        f = f"application_key={application_key}count={count}fid={fid}fields={fields}format=jsonmethod={method}{secret_key}"
        hash_object = hashlib.md5(f.encode())
        sig = hash_object.hexdigest()
        params = {'application_key': application_key,
                  'count': count,
                  'fid': fid,
                  'fields': fields,
                  'format': format,
                  'method': method,
                  'sig': sig,
                  'access_token': access_token
                  }
        resp_ph = requests.get('https://api.ok.ru/fb.do', params=params)
        resp_photos = resp_ph.json()
        photos = resp_photos['photos']
        files_names_old = folder_name[1]
        names_list = list()
        for i in tqdm(photos, desc=f'Photos are loading'):
            title = i['like_count']
            title_id = i['id']
            if title in files_names_old:
                title = title_id
            if title in names_list:
                title = f'{title}_{title_id}'
            pic_max = i['pic_max']
            self.uploading(folder_name[0],title,pic_max)
            names_list.append(title)
