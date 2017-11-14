# -*- coding: utf-8 -*-
import sys, glob, os, zipfile
import ConfigParser
from qbittorrent_client import QBClient
from datetime import datetime, timedelta

zip_extension_list = ('.rar', '.zip', '.7z')
configParser = ConfigParser.RawConfigParser()  
configFilePath = r'extract.ini'
configParser.read(configFilePath)
dest_path = configParser.get('zip', 'dest_path')
torrent_url = configParser.get('torrent', 'url')
username = configParser.get('auth', 'username')
password = configParser.get('auth', 'password')
today = int(configParser.get('zip', 'today'))
delete_after_unzip = int(configParser.get('zip', 'delete_after_unzip'))

def unzip(source_filename, dest_dir):
    with zipfile.ZipFile(source_filename) as zf:
        zf.extractall(dest_dir)
        
def extract_file(zipPath, dest_path):
    d_list = []
    for root, dirs, files in os.walk(zipPath):
        for file in files:
            if file.endswith(zip_extension_list):
                d_list.append(file)
    return d_list

def torrent_hash(file_obj):
    hash_file = file_obj.get('hash')
    return {'hash' : hash_file}

def remove_extension(file_name):
    if file_name[-3:] == ".7z":
        file_name = file_name[:len(file_name)-3]
    else:
        file_name = file_name[:len(file_name)-4]
    return file_name

def extract_compress_file(file_obj):
    file_name = file_obj.get('name')
    save_path = file_obj.get('save_path')
    if file_name.endswith(zip_extension_list):
        mod_file_name = remove_extension(file_name)
        absolute_source_path = os.path.join(save_path, file_name)
        absolute_dest_path = os.path.join(dest_path, mod_file_name)
        print u'upziping file : %s ' % (absolute_source_path)
        try:
            unzip(absolute_source_path, absolute_dest_path)
            print u'upziped file : %s' % (file_name) 
            result = 1
        except Exception as e:
            print u'cannot upzip file : %s, %s' % (absolute_source_path, e)
            result = 0
    else:
        print u'%s is not compress file' %(file_name)
        result = 0
    return result


if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding("utf-8")
    qClient = QBClient(torrent_url)
    qClient.login(username, password)
    get_torrent = qClient.get_torrent_list('?filter=completed&sort=added_on')
    for each_torr in get_torrent:
        extract_result = 0
        if today:
            today_date = datetime.now()
            torrent_added_on = each_torr.get('added_on')
            if (today_date.date() ) == (datetime.fromtimestamp(torrent_added_on).date()): #if (today_date.date() - timedelta(1) ) for the previous day
                extract_result = extract_compress_file(each_torr)            
                print u'extract_result=',extract_result     
        else:
            extract_result = extract_compress_file(each_torr)  
            print 'extract_result=',extract_result
        if extract_result:
            if delete_after_unzip:
                hash_file = torrent_hash(each_torr)
                delete_result = qClient.delete_torrent(hash_file)
                print u'deleted file : %s, hash : %s, result : %s' % (each_torr.get('name'), hash_file, delete_result)              
    del qClient