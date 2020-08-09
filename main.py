from typing import List
from fastapi import FastAPI
import pylast

import models
import os

app = FastAPI()

# DISCLAIMER! This API is a test/demo data provider and 
#             shouldn't be used in production

# demo user object

demo_user = {
    "username": "demo",
    "display_name": "Demo User", 
    "img_url": "https://cdn.mos.cms.futurecdn.net/VSy6kJDNq2pSXsCzb6cvYF.jpg",
    "messenger_url" : "https://m.me/demo-usr-dont-click"
}

demo_recommendations = []

for i in range(0, 10):
    demo_recommendations.append({
        "username": "demo_" + str(i),
        "display_name": "Demo User " + str(i), 
        "img_url": "https://cdn.mos.cms.futurecdn.net/VSy6kJDNq2pSXsCzb6cvYF.jpg",
        "messenger_url" : "https://m.me/demo-" + str(i) + "-usr-dont-click",
        "similarity_match": (i + 20 * i) % 100 
    })


demo_tracks = [
    {
    "title": "Starboy",
    "artist": "The Weeknd"
    },{
    "title": "Shape of You",
    "artist": "Ed Sheeran"
    },{
    "title": "DNA.",
    "artist": "Kendrick Lamar"
    },{
    "title": "Blinding Lights",
    "artist": "The Weeknd"
    },{
    "title": "Dance Monkey",
    "artist": "Tones & I"
    },{
    "title": "Roses",
    "artist": "Saint JHN"
    },{
    "title": "Don't start now",
    "artist": "Dua Lipa"
    },{
    "title": "Ride It",
    "artist": "Regard"
    },{
    "title": "3 Nights",
    "artist": "Dominic Fike"
    },{
    "title": "Good Day",
    "artist": "Broiler"
    },{
    "title": "Crime",
    "artist": "Vax"
    },{
    "title": "Smart Love",
    "artist": "Drax Project"
    },{
    "title": "Beach House",
    "artist": "The Chainsmokers"
    },{
    "title": "Goofy",
    "artist": "MishCatt"
    },{
    "title": "Lovefool",
    "artist": "twocolors"
    },{
    "title": "Just a Litle Longer",
    "artist": "SHY Martin"
    },{
    "title": "Lost",
    "artist": "Clean Bandit"
    },{
    "title": "REMEDY",
    "artist": "Alesso"
    },{
    "title": "Late Night",
    "artist": "Shakewell"
    },{
    "title": "Tales From Tha Guttah",
    "artist": "Ramirez"
    }
]

demo_library = [
    {
    "title": "3 Nights",
    "artist": "Dominic Fike"
    },{
    "title": "Good Day",
    "artist": "Broiler"
    },{
    "title": "Crime",
    "artist": "Vax"
    },{
    "title": "Smart Love",
    "artist": "Drax Project"
    },{
    "title": "Beach House",
    "artist": "The Chainsmokers"
    },{
    "title": "Goofy",
    "artist": "MishCatt"
    },{
    "title": "Lovefool",
    "artist": "twocolors"
    },{
    "title": "Just a Litle Longer",
    "artist": "SHY Martin"
    },{
    "title": "Lost",
    "artist": "Clean Bandit"
    },{
    "title": "REMEDY",
    "artist": "Alesso"
    },{
    "title": "Late Night",
    "artist": "Shakewell"
    },{
    "title": "Tales From Tha Guttah",
    "artist": "Ramirez"
    }
]
# root endpoint
@app.get("/")
async def default_endpoint():
    return "RECO Demo Backend API Service!"

# users endpoints
@app.post("/users/register", response_model = models.UserProfileModel)
async def register_user(user: models.UserRegisterModel):
    return demo_user

@app.post("/users/login", response_model = models.UserProfileModel)
async def login_user(user: models.UserLoginModel):
    return demo_user

@app.get("/users/me", response_model = models.UserProfileModel)
async def get_user_profile():
    return demo_user

@app.put("/users/me", response_model = models.UserProfileModel)
async def update_user_profile(user: models.UserProfileUpdateModel):
    return demo_user

@app.delete("/users/me")
async def delete_user_profile():
    pass

@app.patch("/users/password")
async def change_password(user: models.UserPasswordChangeModel):
    pass

@app.post("/users/logout")
async def logout_user():
    pass

# search
@app.get("/search", response_model = List[models.TrackModel])
async def search_tracks(q: str = None):
    if q != '':
        return await lastfm_search(q)
    else:
        return []

# library endpoints

@app.get("/library", response_model = List[models.TrackModel])
async def get_user_library():
    # return demo_library
    return []

@app.post("/library", response_model = models.TrackModel)
async def add_track(track: models.TrackModel):
    return track

@app.delete("/library/{track_id}")
async def delete_track(track_id: int):
    pass

# recommendations endpoints

@app.get("/recommendations", response_model = List[models.RecommendedUserModel])
async def get_recommendations():
    return demo_recommendations

@app.get("/recommendations/latest", response_model = List[models.RecommendedUserModel])
async def get_latest_recommendations():
    return demo_recommendations[6:]


async def lastfm_search(q: str):
    lastfm_service = pylast.LastFMNetwork(api_key = os.environ['LASTFM_API_KEY'], api_secret=os.environ['LASTFM_API_SECRET'])
    search_results = lastfm_service.search_for_track("", q).get_next_page()
    tracks_results = []
    for result in search_results:
        track = str(result).split("-")
        track_artist = track[0]
        track_title = track[1]
        tracks_results.append({
            "title": track_title,
            "artist": track_artist
        })
    return tracks_results