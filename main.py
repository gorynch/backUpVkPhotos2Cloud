import time
import json
from vars import *
from tokens import *
from tqdm import tqdm
from datetime import datetime
import requests
from urllib.parse import urlencode
class VKapi:
    def __new__(cls, appID, VKtoken, userID, baseUrl, version):
        params = {
            "owner_id": userID,
            "client_id": appID,
            "redirect_uri": "https://oauth.vk.com/blank.html",
            "access_token": VKtoken,
            "display": "page",
            "scope": scope,
            "response_type": "token",
            "v": version
        }
        method_url = "photos.getAlbums"

        get_url = f"{vkBaseUrl + method_url}?{urlencode(params)}"
        response = requests.get(get_url)
        data = response.json()
        if ("error" in data) and (data.get("error", {}).get("error_code", -3) == 5):
            get_url = f"{oAuthBaseURL}?{urlencode(params)}"
            res = f"Error {data.get('error', '').get('error_code', '')}: {data.get('error', '').get('error_msg', '')}"
            print(get_url)
        else:
            res = super().__new__(cls)
        return res

    def __init__(self, appID, VKtoken, userID, baseUrl, version):
        self.appID = appID
        self.VKtoken = VKtoken
        self.userID = userID
        self.version = version
        self.baseUrl = baseUrl
        self.params = {
            "owner_id": self.userID,
            "client_id": self.appID,
            "redirect_uri": "https://oauth.vk.com/blank.html",
            "access_token": self.VKtoken,
            "display": "page",
            "scope": scope,
            "response_type": "token",
            "v": self.version
        }
    def getAlbums(self):
        method_url = "photos.getAlbums"

        get_url = f"{self.baseUrl + method_url}?{urlencode(self.params)}"
        response = requests.get(get_url)
        data = response.json()
        if "error" in data:
            res = f"Error {data.get('error', '').get('error_code', '')}: {data.get('error', '').get('error_msg', '')}"
        else:
            res = data
        return res

    # def checkUserAlbumList(vk, VKalbum):
    #     if albumsName != []:
    #         correctAlbumList = []  # data to upload: no wrong album name no empty album
    #         wrongAlbum = albumsName
    #         emptyAlbum = []
    #         for alb in VKalbum.get("response", {}).get("items", []):
    #             correctAlbumDic = {}
    #             if alb.get("title", "") in wrongAlbum:
    #                 wrongAlbum.remove(alb.get("title", ""))
    #                 if alb.get("size", -3) > 0:
    #                     correctAlbumDic["name"] = alb.get("title", "")
    #                     correctAlbumDic["id"] = alb.get("id", -3)
    #                     correctAlbumDic["count"] = alb.get("size", -3)
    #                     correctAlbumList.append(correctAlbumDic)
    #                 else:
    #                     emptyAlbum.append(alb.get("title", ""))
    #         correctAlbumDic = {}
    #         if "profile" in albumsName:
    #             wrongAlbum.remove("profile")
    #             count = vk.getPhotoCount("profile")
    #             if count > 0:
    #                 correctAlbumDic["name"] = "profile"
    #                 correctAlbumDic["id"] = "profile"
    #                 correctAlbumDic["count"] = count
    #                 correctAlbumList.append(correctAlbumDic)
    #             else:
    #                 emptyAlbum.append("profile")
    #         correctAlbumDic = {}
    #         if "wall" in albumsName:
    #             wrongAlbum.remove("wall")
    #             count = vk.getPhotoCount("wall")
    #             if count > 0:
    #                 correctAlbumDic["name"] = "wall"
    #                 correctAlbumDic["id"] = "wall"
    #                 correctAlbumDic["count"] = count
    #                 correctAlbumList.append(correctAlbumDic)
    #             else:
    #                 emptyAlbum.append("wall")
    #         print(f"{wrongAlbumMsg} {wrongAlbum}")
    #         print(f"{emptyAlbumMsg} {emptyAlbum}")
    #         return correctAlbumList
    #     else:
    #         print(albumListEmptyMsg)
    def getPhotoCount(self, albumID):
        self.params["album_id"] = albumID
        self.params["extended"] = 1
        method_url = "photos.get"
        get_url = f"{self.baseUrl + method_url}?{urlencode(self.params)}"
        response = requests.get(get_url)
        data = response.json()
        if "error" not in data:
            return data.get("response", {}).get("count", -3)
        else:
            return f"error: {data.get('error', '').get('error_code', '')}: {data.get('error', '').get('error_msg', '')}"
    def getPhotoIinfo(self, albumIDlist):
        albumDataList = []
        for alb in albumIDlist:
            # print(f"alb: {alb}")
            time.sleep(0.1)
            photoIlist = []
            photoDataDic = {}
            photoDataDic["albumName"] = alb.get("name", "")
            photoDataDic["albumID"] = alb.get("id", "")
            photoDataDic["photoCount"] = alb.get("count", "")
            self.params["album_id"] = alb.get("id", "")
            # self.params["album_id"] = id
            self.params["extended"] = 1
            method_url = "photos.get"
# get each photo data from current album
            get_url = f"{self.baseUrl + method_url}?{urlencode(self.params)}"
            response = requests.get(get_url)
            data = response.json()
            if "error" not in data:
                print(f"ALbum: {alb.get('name', '')} - {getInfoIphoto}")
                for photo in tqdm(data.get("response", {}).get("items",[])):
                    photoIdataDic = {}
                    photoDateUtc = photo.get("date", -3)
                    sizesList = []
                    for size in photo.get("sizes", []):  # get all sizes of photo to find max width, height and type
                        sizeWidth = size.get("width", -3)
                        sizesList.append(sizeWidth)
                    photoIdataDic["sizeType"] = photo.get("sizes", [])[sizesList.index((max(sizesList)))].get("type", "")
                    photoIdataDic["width"] = photo.get("sizes", [])[sizesList.index((max(sizesList)))].get("width", -3)
                    photoIdataDic["height"] = photo.get("sizes", [])[sizesList.index((max(sizesList)))].get("height", -3)
                    photoIdataDic["url"] = photo.get("sizes", [])[sizesList.index((max(sizesList)))].get("url", "")
                    # photoIdataDic["sizeMb"] = photoSizeMb # looking for info how to get size of photo on vk (Content-Length return 29.9Kb of any photo)
                    photoIdataDic["id"] = photo.get("id", -3)
                    photoIdataDic["likes"] = photo.get("likes", {}).get("count", -3)
                    photoIdataDic["date"] = datetime.utcfromtimestamp(photoDateUtc).strftime('%Y-%m-%d__%H_%M_%S') # yaDisk not like a lot : in file name, that may be a trick to hack yaDisk
                    # logList = [] # bad idea to use like (and date) to file name (probability not zero of same name for lot of files (photo from some (event or trip) uploaded in one day and have the same count of like
                    # if f"{photoDate}_like{photoLikes}_id{photoID}.jpg" not in logList:
                    #     fileName = f"{photoDate}_like{photoLikes}.jpg"
                    #     logList.append(fileName)
                    # else:
                    #     fileName = f"{photoDate}_like{photoLikes}_id{photoID}.jpg"
                    #     logList.append(fileName)
                    photoIdataDic["name"] = f"{datetime.utcfromtimestamp(photoDateUtc).strftime('%Y-%m-%d__%H_%M_%S')}_like{photo.get('likes', {}).get('count', -3)}_id{photo.get('id', -3)}.jpg"
                    photoIlist.append(photoIdataDic)
                    photoDataDic["photoData"] = photoIlist
                albumDataList.append(photoDataDic)
            else:
                albumDataList.append(f"error: {data.get('error', '').get('error_code', '')}: {data.get('error', '').get('error_msg', '')}")
                break
        return albumDataList
class YaApi:
    def __init__(self, YaToken, YaUrl):
        self.YaToken = YaToken
        self.YaUrl = YaUrl
    def createFolder(self,folderName):
        headers = {'Content-Type': 'application/json',
                  'Accept': 'application/json',
                  'Authorization': f'OAuth {self.YaToken}',
                   "path": folderName
                   }
        response = requests.put(f'{yaURL}?path={folderName}', headers=headers)
        if response.status_code == 201:
            res = "Folder created"
        else:
            res = f"Error {response.status_code}: {response.json().get('message', '')}"
        return res
    def uploadFile(self,fileName, folderName, fileURL):
        headers = {'Content-Type': 'application/json',
                   'Accept': 'application/json',
                   'Authorization': f'OAuth {self.YaToken}'
                   }
        params = {
            "path": f"{folderName}/{fileName}",
            "url": {fileURL},
            "disable_redirects": "False"
        }
        response = requests.post(f"{yaURL+'upload?'}", headers=headers, params=params)
        if response.status_code == 202:
            res = "file uploaded successful"
        else:
            res = f"Error {response.status_code}: {response.json().get('message', '')}"
        return res
    def uploadFiles2Folders(self, vkData):
        resUploadList = []  # list of dicts of all uploaded files and albums
        vkF = myYaDisk.createFolder(f"{vkFolder}")
        if "Error" not in vkF:  # check for no error or error 409 (folder while creating vkFolder
        # if ("error" not in vkF) or error409FolderExistsMsg in vkF:  # check for no error or error 409 (folder while creating vkFolder
            fileUplodList = [] # list of dicts of all uploaded files in each albums
            print(upLoad2CloudMsg)
            for dic in tqdm(vkData): # loop through all album in correct album list
                fileUplodDic = {} # dic for each photo in current album
                resUploadDic = {} # dic for all photo in current album
                resUploadDic["albumName"] = dic['albumName']
                subFolder = myYaDisk.createFolder(f"{vkFolder}/{dic['albumName']}")  # create subfolder for album
                if ("Error" or "error") not in subFolder:
                    if str(photosCount) == "all":  # upload all photos from album
                        for d in dic.get("photoData", []):
                            time.sleep(0.25)  # without delay - not all files upload but no error raise up
                            temp = self.uploadFile(d.get("name"),f"{vkFolder}/{dic['albumName']}",d.get("url"))
                            if ("error" or "Error") not in temp:
                                fileUplodDic[d.get("name")] = "Uploded"
                            else:
                                fileUplodDic[d.get("name")] = "Error uploded"
                        # fileUplodList.append(fileUplodDic)
                    else:  # upload N photosCount photos from album
                        if type(photosCount) is int:
                            for i in range(0, photosCount):
                                time.sleep(0.15)  # without delay - not all files upload but no error raise up
                                temp = self.uploadFile(
                                    dic.get("photoData", [])[i].get("name"),
                                    (f"{vkFolder}/{dic['albumName']}"),
                                    dic.get("photoData", [])[i].get("url"))
                                if ("error" or "Error") not in temp:
                                    fileUplodDic[dic.get("photoData", [])[i].get("name")] = "Uploded"
                                else:
                                    fileUplodDic[dic.get("photoData", [])[i].get("name")] = "Error uploded"
                    fileUplodList.append(fileUplodDic)
                else:
                    print(subFolder)
                resUploadDic["uploadData"] = fileUplodList  # add data about uploaded files in current album to result list
                fileUplodList = []
                resUploadList.append(resUploadDic)
            with open(outputFileOfUploadData, 'w') as f:
                json.dump(resUploadList, f)
        else:
            print(vkF)
            resUploadList.append(vkF)
        return resUploadList
def checkUserAlbumList(vk, VKalbum):
    correctAlbumList = []  # data to upload: no wrong album name no empty album
    wrongAlbum = albumsName
    emptyAlbum = []
    if albumsName != []:
        print(checkVKdataMsg)
        for alb in tqdm(VKalbum.get("response", {}).get("items", [])):
            correctAlbumDic = {}
            if alb.get("title", "") in wrongAlbum:
                wrongAlbum.remove(alb.get("title", ""))
                if alb.get("size", -3) > 0:
                    correctAlbumDic["name"] = alb.get("title", "")
                    correctAlbumDic["id"] = alb.get("id", -3)
                    correctAlbumDic["count"] = alb.get("size", -3)
                    correctAlbumList.append(correctAlbumDic)
                else:
                    emptyAlbum.append(alb.get("title", ""))
        correctAlbumDic = {}
        if "profile" in albumsName:
            wrongAlbum.remove("profile")
            count = vk.getPhotoCount("profile")
            if count > 0:
                correctAlbumDic["name"] = "profile"
                correctAlbumDic["id"] = "profile"
                correctAlbumDic["count"] = count
                correctAlbumList.append(correctAlbumDic)
            else:
                emptyAlbum.append("profile")
        correctAlbumDic = {}
        if "wall" in albumsName:
            wrongAlbum.remove("wall")
            count = vk.getPhotoCount("wall")
            if count > 0:
                correctAlbumDic["name"] = "wall"
                correctAlbumDic["id"] = "wall"
                correctAlbumDic["count"] = count
                correctAlbumList.append(correctAlbumDic)
            else:
                emptyAlbum.append("wall")
    else:
        print(albumListEmptyMsg)
        wrongAlbum = []
    if (correctAlbumList == []):
        print(nothing2backUpMsg)
    return correctAlbumList, wrongAlbum, emptyAlbum
def mainLoop(ya, vk):
    vkData = []
    if isinstance(vk, VKapi):
        VKalbum = vk.getAlbums() # get info (title, id, photo count) in all album on vk
        albumList, wrongList, emttyList = checkUserAlbumList(vk, VKalbum)
        print(f"{wrongAlbumMsg} {wrongList}")
        print(f"{emptyAlbumMsg}: {emttyList}")
        vkData = vk.getPhotoIinfo(albumList) # info about all photo in given user albums list
        # uploadData = []
        if vkData != []:
            uploadData = ya.uploadFiles2Folders(vkData)
        else:
            uploadData = vkData = f"{nothing2backUpMsg}, {wrongAlbumMsg}: {wrongList}, {emptyAlbumMsg}: {emttyList}"
        vkData.insert(0, {"info":f"{wrongAlbumMsg}: {wrongList}, {emptyAlbumMsg}: {emttyList}"})
        with open(outputFileOfInputData, 'w') as f:
            json.dump(vkData, f)
        uploadData.insert(0, {"info":f"{wrongAlbumMsg}: {wrongList}, {emptyAlbumMsg}: {emttyList}"})
        with open(outputFileOfUploadData, 'w') as f:
            json.dump(uploadData, f)
    else:
        print(vk)
    return vkData


if __name__ == '__main__':
    print("let's start!")
    print()
    myYaDisk = YaApi(yaToken, yaURL)
    myVK = VKapi(vkAppID, vkToken, vkUserID, vkBaseUrl, vkVersion)
    mainLoop(myYaDisk, myVK)
    print(f"Done.")