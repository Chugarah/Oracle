from mongoengine import DynamicDocument, connect, StringField, EmbeddedDocument, ListField, EmbeddedDocumentField, IntField
from mongoengine.errors import ValidationError
from pymongo import MongoClient
from bson.objectid import ObjectId
import json
import os
from modules.load_settings import get_config
from modules.functions import get_files_info, check_file_exists
from modules.mongo_db import search_video_id_collection, update_document

get_config = get_config()
connect(
    db='oracleYoutubeDB',
    host='localhost',
    port=27017,
    username='admin',
    password='secret'
)


class FileInfo(EmbeddedDocument):
    file_id = StringField()
    file_name = StringField()
    file_extension = StringField()
    file_size = IntField()
    file_location = StringField()


def create_document_class(collection_name):
    class DynamicDocumentClass(DynamicDocument):
        meta = {'collection': collection_name}
        video_id = StringField()
        title = StringField()
        files = ListField(EmbeddedDocumentField(FileInfo))
        thumbnail = StringField()
        description = StringField()
        channel_id = StringField()
    return DynamicDocumentClass


base_folder = get_config['INPUT_DIR']
whisper_folder = get_config['WHISPER_DIR']
json_scan = str(get_config['JSON_SCAN'])
folders = [base_folder, whisper_folder]

file_counter = 0
data = []
files_info = []
DestDocumentClass = None
add_files = False

total_folders = len(folders)
folder_counter = 0

for folder in folders:
    for dirpath, dirnames, filenames in os.walk(folder):
        files_info = list(get_files_info(dirpath))
        for filename in filenames:
            if filename.endswith(json_scan):
                file_path = os.path.join(dirpath, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)

                    DestDocumentClass = create_document_class(
                        data.get('channel_id', 'default_collection'))

                    files_info = list(get_files_info(dirpath))

                    channel_id = data.get('channel_id', 'default_collection')
                    chapters = data.get('chapters', 'default_collection')

                    like_count = data.get('like_count', 'default_collection')
                    heatmap = data.get('heatmap', 'default_collection')
                    channel_is_verified = data.get(
                        'channel_is_verified', 'default_collection')

                    data['files'] = files_info
                    data.pop('channel_id', None)
                    data['video_id'] = data.pop('id')

                    for file_info in files_info:
                        if os.path.exists(file_info['file_location']):
                            # Use the dynamic class for the update_one operation
                            DestDocumentClass.objects(
                                video_id=data['video_id']).update_one(
                                set__title=data['title'],
                                set__files=data['files'],
                                set__thumbnail=data['thumbnail'],
                                set__description=data['description'],
                                set__channel_id=channel_id,
                                set__channel_url=data['channel_url'],
                                set__duration=data['duration'],
                                set__view_count=data['view_count'],
                                set__age_limit=data['age_limit'],
                                set__webpage_url=data['webpage_url'],
                                set__categories=data['categories'],
                                set__tags=data['tags'],
                                set__comment_count=data['comment_count'],
                                set__chapters=chapters,
                                set__heatmap=heatmap,
                                set__like_count=like_count,
                                set__channel=data['channel'],
                                set__channel_follower_count=data['channel_follower_count'],
                                set__channel_is_verified=channel_is_verified,
                                set__uploader=data['uploader'],
                                set__upload_date=data['upload_date'],
                                set__availability=data['availability'],
                                set__fulltitle=data['fulltitle'],
                                set__duration_string=data['duration_string'],
                                set__filesize=data['filesize'],
                                upsert=True)
                            print(
                                f"Progress: File {file_counter} processed with video_id {data['video_id']} was updated.")
                            file_counter += 1

                        else:
                            DestDocumentClass.objects(
                                video_id=data['video_id']).delete()
                            print(
                                f"Progress: File with video_id {data['video_id']} was deleted.")

                except (ValidationError, Exception) as e:
                    print(f"An error happened with file {filename}: {e}")
    folder_counter += 1


# This is only when we have an custom directory for Whisper
if get_config['CUSTOM_WHISPER_DIR']:
    if (total_folders == folder_counter):
        database_name = "oracleYoutubeDB"

        for file_info in files_info:
            if os.path.exists(file_info['file_location']):

                collection_name = search_video_id_collection(
                    database_name, file_info['file_name'])

                # Use the dynamic class for the update_one operation
                update_document(database_name, collection_name,
                                file_info['file_name'], file_info)
                print(
                    f"File {file_info['file_name']}{file_info['file_extension']}  added")
                file_counter += 1
            else:
                DestDocumentClass.objects(
                    video_id=data['video_id']).delete()
                print(
                    f"File with video_id {data['video_id']} was deleted.")
