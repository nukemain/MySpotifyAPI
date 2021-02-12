import json
import requests
from secrets import spotify_token, spotify_user_id, discover_weekly_id

class MySpotifyAPI:
    def __init__(self):
        self.user = spotify_user_id
        self.spotify_token = spotify_token
        self.discover_weekly_id = discover_weekly_id 

    def download_image_of_currently_playing_song(self, returntype):
        self.returntype = returntype
        self.error = False
        self.status = ''

        query = "https://api.spotify.com/v1/me/player/currently-playing"
        response = requests.get(query,headers={"Accept": "application/json","Content-type": "application/json","Authorization": "Bearer {}".format(spotify_token)})

        if(str(response) == '<Response [200]>'):

            response_json = response.json()
            self.songname = response_json['item']['name']

            url = str(response_json['item']['album']['images'][0]['url'])
            response = requests.get(url) #get pinged users pfp
            fpath = "C:\\Users\\Sowap\\Desktop\\test\\image_current_song_thumbnail.png"
            file = open(str(fpath), "wb") #open a new file
            file.write(response.content) #write in file what we get from from the users pfp url
            file.close() #save the file

            if(self.returntype == '1'):
                return fpath
            elif(self.returntype == '2'):
                return self.songname
        elif(str(response) != 'Response [200]'):
            self.status = "API_ERROR"
            return self.status


    def find_songs(self): 
        query = "https://api.spotify.com/v1/playlists/{}/tracks".format(discover_weekly_id)
        response = requests.get(query,headers={"Content-type": "application/json","Authorization": "Bearer {}".format(spotify_token)})
        response_json = response.json()
        f = 0
        for i in response_json['items']:
            f = f + 1
            man = i['track']['album']['images']
            print(man[0]['url'])
            url = str(man[0]['url'])
            response = requests.get(url) #get pinged users pfp
            fpath = "C:\\Users\\Sowap\\Desktop\\test\\image" + str(f) +".png"
            file = open(str(fpath), "wb") #open a new file
            file.write(response.content) #write in file what we get from from the users pfp url
            file.close() #save the file


a = MySpotifyAPI()
#a.find_songs()
print(a.download_image_of_currently_playing_song(str(1)))