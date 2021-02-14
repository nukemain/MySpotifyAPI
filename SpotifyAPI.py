import json
import requests
from secrets import spotify_token, spotify_user_id
from refresh import Refresh
from pathlib import Path


#C:\\Users\\Sowap\\Desktop\\test\\image

#TODO:
# MAKE THE PICTURE FILE PATH   path only no filename 
# playlist return amount of downloaded items
# automatic code refresh elif response 400 <----- do manually in the program when <Response [400]> or 401

class MySpotifyAPI:
    def __init__(self):
        self.user = spotify_user_id
        self.spotify_token = spotify_token

        home = str(Path.home())
        path_to_file = str(home) + "\\MySpotifyAPITokenVault.txt"
        try:
            logfile = open(path_to_file,'r')
            self.spotify_token = logfile.read()
            logfile.close()
        except FileNotFoundError:
            print("ERROR: NO TOKEN VAULT FILE FOUND")
            print("ERROR: NO TOKEN VAULT FILE FOUND")
            print("ERROR: NO TOKEN VAULT FILE FOUND")
        open(path_to_file, "w").close() # <-- wipe file
    
    def call_token_refresh(self, path_to_file):
        open(path_to_file, "w").close()
        refreshCaller = Refresh()
        self.spotify_token = refreshCaller.get_refreshed_token()
        logfile = open(path_to_file, "w")
        logfile.write(str(self.spotify_token))
        logfile.close()
        return "Spotify token refreshed"


    def download_image_of_currently_playing_song(self, pathtosave):
        self.pathtosave = pathtosave
        status = ''

        query = "https://api.spotify.com/v1/me/player/currently-playing"
        response = requests.get(query,headers={"Accept": "application/json","Content-type": "application/json","Authorization": "Bearer {}".format(self.spotify_token)})

        if(str(response) == '<Response [204]>'):
            status = "ERROR_NOTLISTENING"
            return status
        
        try: 
            response_json = response.json()
        except:
            status = "JSONERROR_JSONERROR"
            return status
        
        if(str(response) == '<Response [200]>'): # rsponse 200 = all is cool and good

            url = str(response_json['item']['album']['images'][0]['url'])
            response = requests.get(url) 
            #fpath = "C:\\Users\\Sowap\\Desktop\\test\\image_current_song_thumbnail.png"
            fpath = str(self.pathtosave)+".png"
            file = open(str(fpath), "wb") #open a new file
            file.write(response.content) #write in file what we get from from the users pfp url
            file.close() #save the file
            return fpath
        elif(str(response) != '<Response [200]>'):
            print(response_json)
            status = "APIERROR_" + str(response) #if 400 then you wasted the previous token
            return status

    def get_currently_playing_songs_name(self):
        query = "https://api.spotify.com/v1/me/player/currently-playing"
        response = requests.get(query,headers={"Accept": "application/json","Content-type": "application/json","Authorization": "Bearer {}".format(self.spotify_token)})
        try:#
            response_json = response.json()
        except:
            status = "JSONERROR_JSONERROR"
            return status
        if(str(response) == '<Response [200]>'):

            songname = response_json['item']['name']
            return songname
        elif(str(response) != 'Response [200]'):
            status = "APIERROR_" + str(response)
            return status


    def download_images_from_playlist(self, playlistID, pathtosave): 
        self.playlistID = playlistID
        self.pathtosave = pathtosave
        query = "https://api.spotify.com/v1/playlists/{}/tracks".format(self.playlistID)
        response = requests.get(query,headers={"Content-type": "application/json","Authorization": "Bearer {}".format(self.spotify_token)})
        
        try:
            response_json = response.json()
        except:
            status = "JSONERROR_JSONERROR"
            return status
        if(str(response) == '<Response [200]>'):
            f = 0
            for i in response_json['items']:
                f = f + 1
                man = i['track']['album']['images']
                #print(i['track']['album']['images'][0]['url'])
                url = str(man[0]['url'])
                response = requests.get(url) 
                #fpath = "C:\\Users\\Sowap\\Desktop\\test\\image" + str(f) +".png"
                fpath = str(self.pathtosave) + str(f) +".png"
                file = open(str(fpath), "wb") #open a new file
                file.write(response.content) #write in file what we get from from the users pfp url
                file.close() #save the file
                if(f==int(response_json['total'])):
                    return response_json['total']
        elif(str(response) != '<Response [200]>'):
            status = "APIERROR_" + str(response)
            print(response_json)
            return status
    
    def name_songs_from_playlist(self, playlistID):
        self.playlistID = playlistID
        query = "https://api.spotify.com/v1/playlists/{}/tracks".format(self.playlistID)
        response = requests.get(query,headers={"Content-type": "application/json","Authorization": "Bearer {}".format(self.spotify_token)})
        songnames = []
        try:
            response_json = response.json()
        except:
            status = "JSONERROR_JSONERROR"
            return status
        if(str(response) == '<Response [200]>'):
            f = 0
            for i in response_json['items']:
                f = f + 1
                songname = i['track']['album']['name']
                songnames.append(str(songname))
                if(f==int(response_json['total'])):
                    return songnames
        elif(str(response) != '<Response [200]>'):
            status = "APIERROR_" + str(response)
            print(response_json)
            return status


a = MySpotifyAPI()
#print(a.spotify_token) spotify:playlist:5g9rbJAmohlvHgrzsiavTN spotify:playlist:5g9rbJAmohlvHgrzsiavTN
print(a.download_image_of_currently_playing_song("C:\\Users\\Sowap\\Desktop\\test\\currently_playing_songs_img")) #5g9rbJAmohlvHgrzsiavTN spotify:playlist:4q94A4F7D07MMMS0dMXZws 1uEANtwEuz82tkzRvo9tW6 50: 37i9dQZEVXbN6itCcaL3Tt 55: 4DAUH0SilB3jiQNJEIFrl6 60: 3gz2CUAcXI7bAX2160GpKJ spotify:album:3gz2CUAcXI7bAX2160GpKJ spotify:album:72XiReSpOBjWiKuF83byA6
print(a.download_images_from_playlist("1uEANtwEuz82tkzRvo9tW6","C:\\Users\\Sowap\\Desktop\\test\\playlist_img"))
print(a.call_token_refresh("C:\\Users\\Sowap\\MySpotifyAPITokenVault.txt"))
print(a.name_songs_from_playlist("1uEANtwEuz82tkzRvo9tW6"))
print(a.get_currently_playing_songs_name())
#print(a.spotify_token)
