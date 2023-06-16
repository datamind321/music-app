import streamlit as st 
import spotipy
import requests
import base64
from spotipy.oauth2 import SpotifyClientCredentials


def get_token(clientId,clientSecret):
    url = "https://accounts.spotify.com/api/token"
    headers={}
    data={}
    msg = f"{clientId}:{clientSecret}"
    msgbyte = msg.encode('ascii')
    base64byte = base64.b64encode(msgbyte)
    base64msg = base64byte.decode('ascii')
    headers['Authorization'] = 'Basic ' + base64msg
    data['grant_type'] = 'client_credentials'
    r = requests.post(url,headers=headers,data=data)
    token = r.json()['access_token']
    return token 

token = get_token("de31ae50f7b34a5396fc3e3cf2b51e30","10b822915bd44459a11b0c6922dca538")
print(token) 

def get_artist_data(artist_id,token):
    limit=10

    
    reurl = f"https://api.spotify.com/v1/artists/{artist_id}"
    headers = { 'Authorization':'Bearer ' + token }
    res=requests.get(url=reurl,headers=headers)
    json = res.json()
    # print(json)
    return json  










spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id='de31ae50f7b34a5396fc3e3cf2b51e30',client_secret='10b822915bd44459a11b0c6922dca538',))
st.title("Spotipy Search Engine") 
st.sidebar.write('Menu') 
search_choices = ['Song','Album','Artist',]
search_selected = st.sidebar.selectbox('your search choice please',search_choices)
search_keyword = st.text_input(search_selected + " (keyword search)")
button = st.button('Search')
    
if search_keyword is not None and len(str(search_keyword))>0:
    if search_selected=="Song":
        track = spotify.search(q='tracks'+search_keyword,type='track',limit=5)
        track_list = track['tracks']['items']
        
       
            
          
      
        
        

        
        
        col1,col2=st.columns(2)
        with col1:
            st.image(track['tracks']['items'][0]['album']['images'][0]['url'])
        with col2:
            st.subheader(f"[{track['tracks']['items'][0]['name']}]({track['tracks']['items'][0]['album']['external_urls']['spotify']})")
            try:
                st.write(f"Artists : {track['tracks']['items'][0]['album']['artists'][0]['name']}")
            except:
                pass
            st.write()
            st.write("Release Date : ",track['tracks']['items'][0]['album']['release_date'])
            st.write("Popularity: ",track['tracks']['items'][0]['popularity'])
           
            st.subheader("Preview Song Available Here...")
            st.audio(track['tracks']['items'][0]['preview_url'])
            

        st.header("Singer")
        col1,col2,col3=st.columns(3)
        with col1:
            try:
                artist_id_1 = track['tracks']['items'][0]['artists'][0]['id']
                artist_data = get_artist_data(artist_id_1,token)
  
                st.image(artist_data['images'][0]['url'],width=240)
                st.write(f"[{artist_data['name']}]({artist_data['external_urls']['spotify']})")
            except:
                pass
        with col2:
            try:
                artist_id_2 = track['tracks']['items'][0]['artists'][1]['id']
                artist_data2 = get_artist_data(artist_id_2,token)
                st.image(artist_data2['images'][1]['url'],width=220)
                st.write(f"[{artist_data2['name']}]({artist_data2['external_urls']['spotify']})")
            except:
                pass
        
        with col3:
            try:
                artist_id_3 = track['tracks']['items'][0]['artists'][2]['id']
        
        
                artist_data3 = get_artist_data(artist_id_3,token)
                st.image(artist_data3['images'][1]['url'])
                st.write(f"[{artist_data3['name']}]({artist_data3['external_urls']['spotify']})")
            except:
                pass

        st.header("Similar Song")
        col1,col2,col3=st.columns(3)
        
        if len(track_list)>0:
            for track in track_list :
                st.image(track['album']['images'][0]['url'])
                st.header(f"[{track['name']}]({track['album']['external_urls']['spotify']})")
                st.audio(track['preview_url'])

        
    

        
        

        # st.header(f"[{track['name']}]({track['album']['external_urls']['spotify']})") 
                
        
    elif search_selected == 'Album':
        
        albums = spotify.search(q='albums'+search_keyword,type='album',limit=20)
        album_list = albums['albums']['items']
        if len(album_list)>0:
            for album in album_list:
                st.image(album['images'][0]['url'])
                st.write(f"[{album['name'] }]({album['external_urls']['spotify']})") 


    elif search_selected=="Artist":
       
        artist = spotify.search(q='artist:'+search_keyword,type='artist',limit=10)
        artist_url = artist['artists']['items'][0]['uri']
        result = spotify.artist_top_tracks(artist_url)
        for track in result['tracks'][:10]:
            st.image(track['album']['images'][0]['url'])
            st.header(f"[{track['name']}]({track['external_urls']['spotify']})")
            st.audio(track['preview_url'])
            
