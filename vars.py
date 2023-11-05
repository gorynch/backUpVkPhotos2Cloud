scope = 'photos'

outputFileOfInputData = "output.json"
outputFileOfUploadData = "upload.json"

photosCount = 5 #count of photos in each album to backup
# photosCount = "all" # all photos in each album to backup

# albumsName = ["test6","wall","profile","test4","test3","test2","test1","test5"] #list of albums for backup (temp3-temp6 - wrong names)
albumsName = ["profile"] #list of albums for backup
# albumsName = ["profile", "wall"] #list of albums for backup
# albumsName = [] #list of albums for backup (empty list)
# albumsName = ["wall"] #list of albums for backup (1 album with no photos)
# albumsName = ["wal"] #list of albums for backup (1 album with wrong name)
# albumsName = ["wal", "test1", "wrong", "Wrong"] #list of albums for backup (several albums with wrong name and just one with correct name)

######################## vk info
vkAppID = "51764984"
vkUserID = "295191561"
vkBaseUrl = "https://api.vk.com/method/"
oAuthBaseURL = "https://oauth.vk.com/authorize"
vkVersion = "5.154"

######################## yandex info
yaURL = 'https://cloud-api.yandex.net/v1/disk/resources/'
#will be create new folder "vk" with subfolders to each albums
vkFolder = "vk"
yaFolder = "same" #same - folders name will be like in album on vk.com

######################## info messages
wrongAlbumMsg = "Wrong album name"
emptyAlbumMsg = "Almubs contains no photo: "
albumListEmptyMsg = "Error - Albums list is empty. Fill in the list of albums name in vars.py, please"
nothing2backUpMsg = "No photos found: nothing to backup"
getAlbumListMsg = "Get album list"
checkVKdataMsg = "Check data on vk"
upLoad2CloudMsg = "Uploading files to YaDisk"
getInfoIphoto = "Get info about each photo on vk"