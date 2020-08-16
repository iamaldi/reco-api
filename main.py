from typing import List
from fastapi import FastAPI, HTTPException
import pylast

import models
import os
import json

app = FastAPI(
    title = "Reco Demo FastAPI Service",
    description = "WARNING! This is a demo API service for the Reco android application. This service is NOT recommended for production.",
    version = "v0.1.0-demo",
    docs_url = None
)

# DISCLAIMER! This API is a test/demo data provider and 
#             shouldn't be used in production

# demo user object
demo_user = {
    "username": "demo",
    "display_name": "Demo User", 
    "img_url": "https://cdn.mos.cms.futurecdn.net/VSy6kJDNq2pSXsCzb6cvYF.jpg",
    "messenger_url" : "https://m.me/demo-usr-dont-click"
}

# demo user recommendations
# data provided by https://www.mockaroo.com/
demo_recommendations = [{
    "username": "ecapner0",
    "display_name": "Ernest Capner",
    "img_url": "http://dummyimage.com/188x249.png/ff4444/ffffff",
    "messenger_url": "https://m.me/demo-usr-ecapner0",
    "similarity_match": 61
    }, {
    "username": "feagan1",
    "display_name": "Florina Eagan",
    "img_url": "http://dummyimage.com/145x166.png/ff4444/ffffff",
    "messenger_url": "https://m.me/demo-usr-feagan1",
    "similarity_match": 81
    }, {
    "username": "tgarth2",
    "display_name": "Travis Garth",
    "img_url": "http://dummyimage.com/179x231.bmp/ff4444/ffffff",
    "messenger_url": "https://m.me/demo-usr-tgarth2",
    "similarity_match": 77
    }, {
    "username": "sgrimsditch3",
    "display_name": "Salmon Grimsditch",
    "img_url": "http://dummyimage.com/171x137.jpg/ff4444/ffffff",
    "messenger_url": "https://m.me/demo-usr-sgrimsditch3",
    "similarity_match": 100
    }, {
    "username": "cjerdein4",
    "display_name": "Clare Jerdein",
    "img_url": "http://dummyimage.com/110x247.png/5fa2dd/ffffff",
    "messenger_url": "https://m.me/demo-usr-cjerdein4",
    "similarity_match": 97
    }, {
    "username": "sluckwell5",
    "display_name": "Sibyl Luckwell",
    "img_url": "http://dummyimage.com/174x192.png/ff4444/ffffff",
    "messenger_url": "https://m.me/demo-usr-sluckwell5",
    "similarity_match": 88
    }, {
    "username": "ewarkup6",
    "display_name": "Ediva Warkup",
    "img_url": "http://dummyimage.com/177x167.png/5fa2dd/ffffff",
    "messenger_url": "https://m.me/demo-usr-ewarkup6",
    "similarity_match": 100
    }, {
    "username": "niacopini7",
    "display_name": "Nichole Iacopini",
    "img_url": "http://dummyimage.com/144x186.png/cc0000/ffffff",
    "messenger_url": "https://m.me/demo-usr-niacopini7",
    "similarity_match": 90
    }, {
    "username": "hbenyan8",
    "display_name": "Hendrik Benyan",
    "img_url": "http://dummyimage.com/194x109.jpg/ff4444/ffffff",
    "messenger_url": "https://m.me/demo-usr-hbenyan8",
    "similarity_match": 62
    }, {
    "username": "ctown9",
    "display_name": "Concettina Town",
    "img_url": "http://dummyimage.com/206x210.bmp/ff4444/ffffff",
    "messenger_url": "https://m.me/demo-usr-ctown9",
    "similarity_match": 76
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

# utility functions - INSECURE - USE DATABASE INSTEAD & HASH PASSWORDS
async def get_users_from_file():
    users = []
    try:
        with open('users.json', 'r') as users_file:
                users = json.loads(users_file.read())
        users_file.close()
        return users
    except FileNotFoundError:
        return users

async def save_user_to_file(user: models.UserProfileModel):
    users = await get_users_from_file()
    users.extend([dict(user)])
    with open('users.json', 'w') as users_file:
        json.dump(users, users_file)
    users_file.close()
    return user

# root endpoint
@app.get("/")
async def default_endpoint():
    return "Reco demo API service!"

# users endpoints
@app.post("/users/register", response_model = models.UserProfileModel)
async def register_user(user: models.UserRegisterModel):
    if user not in await get_users_from_file():
        return await save_user_to_file(user)
    else:
        raise HTTPException(status_code = 409, detail = {"error" : "Username is not available!"})

@app.post("/users/login", response_model = models.UserProfileModel)
async def login_user(user: models.UserLoginModel):
    users = await get_users_from_file()
    user_logged_in = False
    if users:
        for usr in users:
            print(usr)
            if user.username == usr['username'] and user.password == usr['password']:
                user_logged_in = True
                return usr
            else:
                user_logged_in = False
        if not user_logged_in:
            raise HTTPException(status_code = 401, detail = {"error" : "Wrong username or password!"})
    else:
        raise HTTPException(status_code = 401, detail = {"error" : "Wrong username or password!"})

@app.get("/users/me", response_model = models.UserProfileModel)
async def get_user_profile():
    return demo_user

@app.put("/users/me", response_model = models.UserProfileModel)
async def update_user_profile(user: models.UserProfileModel):
    return {
        "username": user.username
        "display_name": user.display_name,
        "img_url": user.img_url,
        "messenger_url" : user.messenger_url
    }

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