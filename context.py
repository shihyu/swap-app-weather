#!/usr/bin/env python

from __future__ import print_function
from future import standard_library
standard_library.install_aliases()
import urllib.request, urllib.parse, urllib.error
import json
import os
import sys
import psycopg2
import urlparse
import pymongo
import emoji

from flask import Flask
from flask import request, render_template
from flask import make_response
from pymongo import MongoClient


# Flask should start in global layout
context = Flask(__name__)
# Facbook Access Token (For Marvin Facebook Page)
#ACCESS_TOKEN = "EAAXRzkKCxVQBABZCplGeFoMd8uINY0zwqUSKo6y0LMXCpN4dZC8LzaVsrI2BTdhZCYSZBvteNqxx0vUhFY8V22JjNQ6NMUDMS63pYLUo7T5NmqsiZC5UpJclPrMawkdFQfzdxaTiZCaB0DcQ62DzgZBP1cegKbxgK9rdYhaPhwMSQZDZD"
# Facbook Access Token (For SID Facebook Page)
ACCESS_TOKEN = "EAADCpnCTbUoBAMlgDxoEVTifvyD80zCxvfakHu6m3VjYVdS5VnbIdDnZCxxonXJTK2LBMFemzYo2a4DGrz0SxNJIFkMAsU8WBfRS7IRrZAaHRrXEMBEL5wmdUvzawASQWtZAMNBr90Gattw3IGzeJ7pZBBUthMewXDvnmBELCgZDZD"
# Google Access Token
Google_Acces_Token = "key=AIzaSyDNYsLn4JGIR4UaZMFTAgDB9gKN3rty2aM&cx=003066316917117435589%3Avcms6hy5lxs&q="
# NewsAPI Access Token
newspai_access_token = "505c1506aeb94ba69b72a4dbdce31996"
# Weather Update API KeyError
weather_update_key = "747d84ccfe063ba9"

#************************************************************************************#
#                                                                                    #
#    All Webhook requests lands within the method --webhook                          #
#                                                                                    #
#************************************************************************************#
@context.route('/webhook', methods=['POST'])
def webhook():
    reqContext = request.get_json(silent=True, force=True)
    if reqContext.get("result").get("action") == "input.welcome":
       return welcome()
    elif reqContext.get("result").get("action") == "firstIntroductionSureOptionStatement":
       return firstIntroductionSureOptionStatement(reqContext)
    elif reqContext.get("result").get("action") == "firstIntroductionNoOptionStatement":
       return firstIntroductionNoOptionStatement(reqContext)
    elif reqContext.get("result").get("action") == "secondExplanationOKStatement":
       return secondExplanationOKStatement(reqContext)
    elif reqContext.get("result").get("action") == "thirdExplanationOKStatement":
       return thirdExplanationOKStatement(reqContext)
    elif reqContext.get("result").get("action") == "fourthExplanationOKStatement":
       return fourthExplanationOKStatement(reqContext)
    elif reqContext.get("result").get("action") == "weather":
       return weather(reqContext)
    elif reqContext.get("result").get("action") == "yahooWeatherForecast":
       return weatherhook(reqContext)
    elif reqContext.get("result").get("action") == "wikipedia":
       return wikipedia_search(reqContext)
    elif reqContext.get("result").get("action") == "GoogleSearch":
       return searchhook(reqContext)
    elif reqContext.get("result").get("action") == "wikipediaInformationSearch":
       return wikipediaInformationSearch(reqContext)
    elif reqContext.get("result").get("action") == "news.category":
       return newsCategory(reqContext)
    elif reqContext.get("result").get("action") == "topnews":
       return news_category_topnews(reqContext)
    elif reqContext.get("result").get("action") == "topfournewsarticle":
       return topFourNewsArticle(reqContext)
    elif reqContext.get("result").get("action") == "youtubeTopic":
       return youtubeTopic(reqContext)
    elif reqContext.get("result").get("action") == "youtubeVideoSearch":
       return youtubeVideoSearch(reqContext)
    elif reqContext.get("result").get("action") == "contact":
       return contact(reqContext)
    elif reqContext.get("result").get("action") == "Help":
       return help(reqContext)
    else:
       print("Good Bye")

#************************************************************************************#
#                                                                                    #
#   This method is to get the Facebook User Deatails via graph.facebook.com/v2.6     #
#                                                                                    #
#************************************************************************************#
user_name = ""
def welcome():
    print ("within welcome method")
    data = request.json
    print (data)
    if data is None:
        return {}
    entry = data.get('originalRequest')
    dataall = entry.get('data')
    sender = dataall.get('sender')
    id = sender.get('id')
    print ("id :" + id)
    fb_info = "https://graph.facebook.com/v2.6/" + id + "?fields=first_name,last_name,profile_pic,locale,timezone,gender&access_token=" + ACCESS_TOKEN
    print (fb_info)
    result = urllib.request.urlopen(fb_info).read()
    print (result)
    data = json.loads(result)

    # Insert Data into MongoDB table:
    USER_DATA = [
    {
        'id': data.get('id'),
        'first_name': data.get('first_name'),
        'last_name': data.get('last_name'),
        'locale': data.get('locale'),
        'timezone': data.get('timezone'),
        'gender': data.get('gender')
    }]
    uri = 'mongodb://marvinai:marvinai@ds163232.mlab.com:63232/heroku_stgdzdbp'
    #client = pymongo.MongoClient(uri)
    client = MongoClient("mongodb://marvinai:marvinai@ds163232.mlab.com:63232/heroku_stgdzdbp")
    db = client.get_default_database()
    name_table = db['name_table']

    # Check if already the user is present in database
    if name_table.find( { "id" : id } ):
       print ("Data is already PRESENT in the Database")
       #name_table.delete_many({"first_name": "Swapratim"})
       name_table.insert_many(USER_DATA)
    else: 
       print ("IT LANDED IN THE ELSE LOOP")
       name_table.insert_many(USER_DATA)
       print ("Data has been INSERTED")

    #db.name_table.find()
    ###################################
    
    first_name = data.get('first_name')
    print (first_name)
    user_name = data.get('first_name')
    speech1 = "I'm the official chatbot of Marvin.ai but you can call me 'Marvin'"
    res = {
          "speech": speech1,
          "displayText": speech1,
           "data" : {
              "facebook" : [
                   {
                    "sender_action": "typing_on"
                  },
                  {
                 "attachment" : {
                   "type" : "template",
                     "payload" : {
                      "template_type" : "generic",
                       "elements" : [ 
                                 {
                                   "title" : "Welcome " + first_name + "! Thanks for stopping by..." + emoji.emojize(':wave:', use_aliases=True),
                                   "image_url" : "http://gdurl.com/vc1o",
                                 } 
                           ]
                       } 
                   }
                },
                 {
                    "sender_action": "typing_on"
                  },
                 {
                 "text": speech1
                  },
                 {
                    "sender_action": "typing_on"
                  },
                 {
                 "attachment":{
                        "type":"image", 
                        "payload":{
                        "url":"https://media.giphy.com/media/1qO2XGCGx7Rte/giphy.gif"
                       }
                      }
                  },
                 {
                  "text": "Do you want to know more about Marvin.ai?",
                  "quick_replies": [
                 {
                  "content_type": "text",
                  "title": "Ummm, yeah sure",
                  "payload": "Ummm, yeah sure",
                  "image_url": "http://www.thehindubusinessline.com/multimedia/dynamic/02337/bl12_smiley_jpg_2337780e.jpg"
                 },
                 {
                  "content_type": "text",
                  "title": "No, thank you",
                  "payload": "No, thank you",
                  "image_url": "https://www.colourbox.com/preview/7036940-exited-emoticon.jpg"
                   },
                  {
                    "content_type":"location"
                  }
                  ]
                 }
                ]
              }
            };
    print (res)
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    print (r)
    return r

def reply(user_id, msg):
    data = {
        "recipient": {"id": user_id},
        "message": {"text": msg}
    }
    print ("Data.........")
    print (data)
    resp = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + ACCESS_TOKEN, json=data)
    print(resp.content)
 
###################################THIS IS THE START OF FIRST BLOCK OF CUSTOMER ENGAGEMENT#########################################

def firstIntroductionSureOptionStatement(reqContext):
    option = reqContext.get("result").get("action")
    res = {
        "speech": "...",
        "displayText": "...",
        "data" : {
        "facebook" : [
                {
                    "sender_action": "typing_on"
                },
               {
                "text": "Marvin.ai is a chatbot development company."
               },
               {
                    "sender_action": "typing_on"
                },
               {
                "text": "We build best Customer Support chatbots for any kind of businesses."
               },
               {
                    "sender_action": "typing_on"
                },
               {
                "text": "For example: Restaurant, Hotel, Retail, Healthcare, Real Estate, Banking, Insurance etc"
               },
               {
                    "sender_action": "typing_on"
               },
               {
                 "attachment":{
                        "type":"image", 
                        "payload":{
                        "url":"https://media.giphy.com/media/3ov9kapGIiW3DQHAM8/giphy.gif"
                     }
                 }
               },
               {
                  "text": "Do you wanna know some secrets?",
                  "quick_replies": [
                 {
                  "content_type": "text",
                  "title": "Okkk, Tell Me",
                  "payload": "Okkk, Tell Me",
                  "image_url": "http://www.thehindubusinessline.com/multimedia/dynamic/02337/bl12_smiley_jpg_2337780e.jpg"
                 },
                 {
                  "content_type": "text",
                  "title": "No, thanks",
                  "payload": "No, thanks",
                  "image_url": "https://www.colourbox.com/preview/7036940-exited-emoticon.jpg"
                  },
                  {
                  "content_type": "text",
                  "title": "Contact us",
                  "payload": "contact",
                  "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT82m3I34RXj5OqXvJUqczmgCWoqS9U2EZmdJKXMjZx24Jpp-Z6lQ"
                   }
                  ]
                 }
             ]
           } 
         };
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

#####################################################################
def firstIntroductionNoOptionStatement(reqContext):
    option = reqContext.get("result").get("action")
    res = {
        "speech": "...",
        "displayText": "...",
        "data" : {
        "facebook" : [
                {
                    "sender_action": "typing_on"
                },
               {
                "text": "Don't worry, still you can enjoy tons of features that I offer."
               },
               {
                    "sender_action": "typing_on"
                },
               {
                "text": "I provide special features to search News (30 Newspapers), Weather, Wikipedia or YouTube within this chat window which is unique is nature." + emoji.emojize(':fire:', use_aliases=True),
               },
               {
                    "sender_action": "typing_on"
                },
               {
                "text": "Give it a try and enjoy my personal assistance."
               },
               {
                    "sender_action": "typing_on"
               },
               {
                  "text": "Also click on 'Menu' option to explore more!!!",
                  "quick_replies": [
                 {
                  "content_type": "text",
                  "title": "News",
                  "payload": "News",
                  "image_url": "http://www.freeiconspng.com/uploads/newspaper-icon-20.jpg"
                 },
                 {
                  "content_type": "text",
                  "title": "Weather",
                  "payload": "Weather",
                  "image_url": "https://www.mikeafford.com/store/store-images/ww01_example_light_rain_showers.png"
                   },
                  {
                  "content_type": "text",
                  "title": "Wikipedia",
                  "payload": "Wikipedia",
                  "image_url": "https://upload.wikimedia.org/wikipedia/en/thumb/8/80/Wikipedia-logo-v2.svg/1122px-Wikipedia-logo-v2.svg.png"
                   },
                  {
                  "content_type": "text",
                  "title": "YouTube",
                  "payload": "YouTube",
                  "image_url": "https://cdn1.iconfinder.com/data/icons/logotypes/32/youtube-512.png"
                   },
                  {
                  "content_type": "text",
                  "title": "Contact Us",
                  "payload": "contact",
                  "image_url": "https://cdn3.iconfinder.com/data/icons/communication-mass-media-news/512/phone_marketing-128.png"
                  }
                  ]
                 }
             ]
           } 
         };
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

################################################THIS IS THE START OF SECOND BLOCK OF CUSTOMER ENGAGEMENT#########################################

def secondExplanationOKStatement(reqContext):
    option = reqContext.get("result").get("action")
    res = {
        "speech": "...",
        "displayText": "...",
        "data" : {
        "facebook" : [
               {
                    "sender_action": "typing_on"
               },
               {
                "text": "Global trend shows that People prefer messaging" + emoji.emojize(':iphone:', use_aliases=True) + "over calling." + emoji.emojize(':telephone_receiver:', use_aliases=True)
               },
               {
                    "sender_action": "typing_on"
               },
               {
                "text": "Customers search in FB pages for your business brand before landing to your website."
               },
               {
                    "sender_action": "typing_on"
               },
               {
                 "text": "Instant reply to customer FAQ helps you to grow customer interaction & satisfaction level" + emoji.emojize(':white_check_mark:', use_aliases=True)
               },
               {
                    "sender_action": "typing_on"
               },
               {
                 "text": "This helps to grow your business with rapid and steady growth" + emoji.emojize(':moneybag:', use_aliases=True) + emoji.emojize(':moneybag:', use_aliases=True)
               },
               {
                    "sender_action": "typing_on"
               },
               {
                 "attachment":{
                        "type":"image", 
                        "payload":{
                        "url":"https://media.giphy.com/media/g4AgRBcatHKve/giphy.gif"
                     }
                 }
               },
               {
                  "text": "Want to know how chatbot can help you?",
                  "quick_replies": [
                 {
                  "content_type": "text",
                  "title": "Tell me right now",
                  "payload": "Tell me right now",
                  "image_url": "https://previews.123rf.com/images/krisdog/krisdog1509/krisdog150900014/44577557-A-cartoon-emoji-emoticon-icon-character-looking-very-happy-with-his-thumbs-up-he-likes-it-Stock-Vector.jpg"
                 },
                 {
                  "content_type": "text",
                  "title": "Maybe later on",
                  "payload": "Maybe later on",
                  "image_url": "https://www.colourbox.com/preview/7036940-exited-emoticon.jpg"
                 },
                 {
                  "content_type": "text",
                  "title": "Contact us",
                  "payload": "contact",
                  "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT82m3I34RXj5OqXvJUqczmgCWoqS9U2EZmdJKXMjZx24Jpp-Z6lQ"
                   }
                  ]
                }
             ]
           } 
         };
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

#####################################################################

def thirdExplanationOKStatement(reqContext):
    option = reqContext.get("result").get("action")
    res = {
        "speech": "...",
        "displayText": "...",
        "data" : {
        "facebook" : [
               {
                    "sender_action": "typing_on"
               },
               {
                "text": "Ok, Ok, I know you're getting impatient" + emoji.emojize(':sunglasses:', use_aliases=True)
               },
               {
                    "sender_action": "typing_on"
               },
               {
                "text": "Chatbots are virtual assistants capable of talking to unlimited number of users simultaneously 24/7/365"
               },
               {
                    "sender_action": "typing_on"
               },
               {
                "text": "So people don't have to wait too long to get simple information like: 'When your restaurant will open today?'"
               },
               {
                    "sender_action": "typing_on"
               },
               {
                 "attachment":{
                        "type":"image", 
                        "payload":{
                        "url":"https://media.giphy.com/media/11sBLVxNs7v6WA/giphy.gif"
                     }
                 }
               },
               {
                    "sender_action": "typing_on"
               },
               {
                 "text": "Chatbots also help in Sales promotion and marketing"
               },
               {
                  "text": "Ready to know more about the deal?",
                  "quick_replies": [
                 {
                  "content_type": "text",
                  "title": "Show it to Me",
                  "payload": "Show it to Me",
                  "image_url": "https://previews.123rf.com/images/krisdog/krisdog1509/krisdog150900014/44577557-A-cartoon-emoji-emoticon-icon-character-looking-very-happy-with-his-thumbs-up-he-likes-it-Stock-Vector.jpg"
                 },
                 {
                  "content_type": "text",
                  "title": "No, Later Sometime",
                  "payload": "No, Later Sometime",
                  "image_url": "https://www.colourbox.com/preview/7036940-exited-emoticon.jpg"
                 },
                 {
                  "content_type": "text",
                  "title": "Contact us",
                  "payload": "contact",
                  "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT82m3I34RXj5OqXvJUqczmgCWoqS9U2EZmdJKXMjZx24Jpp-Z6lQ"
                   }
                  ]
                }
             ]
           } 
         };
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r
##################################################

def fourthExplanationOKStatement(reqContext):
    option = reqContext.get("result").get("action")
    res = {
        "speech": "...",
        "displayText": "...",
        "data" : {
        "facebook" : [
               {
                    "sender_action": "typing_on"
               },
               {
                "text": "Reaching out to all your customers with effective promotion is difficult" + emoji.emojize(':loudspeaker:', use_aliases=True)
               },
               {
                    "sender_action": "typing_on"
               },
               {
                "text": "Traditional marketing channels like ad, promotions, email marketing have very low sales conversion rate."
               },
               {
                    "sender_action": "typing_on"
               },
               {
                "text": "Chatbot can promote sales offer to all your digital customers with highest opening rate. This helps in creating personal bonding."
               },
               {
                    "sender_action": "typing_on"
               },
               {
                 "attachment":{
                        "type":"image", 
                        "payload":{
                        "url":"https://media.giphy.com/media/p2qX0hzOihmp2/giphy.gif"
                     }
                 }
               },
               {
                    "sender_action": "typing_on"
               },
               {
                 "text": "Marvin AI has the best market expertise to guide and grow your business."
               },
               {
                  "text": "Do you want a chatbot for your business? Ask for a Limited FREE Trial Offer now",
                  "quick_replies": [
                 {
                  "content_type": "text",
                  "title": "Contact Us Now",
                  "payload": "contact",
                  "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT82m3I34RXj5OqXvJUqczmgCWoqS9U2EZmdJKXMjZx24Jpp-Z6lQ"
                 },
                 {
                  "content_type": "text",
                  "title": "No, Later Sometime",
                  "payload": "No, Later Sometime",
                  "image_url": "https://www.colourbox.com/preview/7036940-exited-emoticon.jpg"
                 }
                  ]
                }
             ]
           } 
         };
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r
##################################################
#************************************************************************************#
#                                                                                    #
#   Below method is to get the Facebook Quick Reply Webhook Handling - Weather       #
#                                                                                    #
#************************************************************************************#
def weather(reqContext):
    option = reqContext.get("result").get("action")
    res = {
        "speech": "Please provide a city name for weather report:",
        "displayText": "Please provide a city name for weather report:",
        "data" : {
        "facebook" : [
               {
                "text": "Please provide a city name for weather report:"
               }
             ]
           } 
         };
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

#************************************************************************************#
#                                                                                    #
#   Below 3 methods are to get the Yahoo Weather Report for a location via API       #
#                                                                                    #
#************************************************************************************#
def weatherhook(reqContext):
   result = reqContext.get("result")
   parameters = result.get("parameters")
   city = parameters.get("geo-city")
   if not parameters.get("geo-city"):
      city = parameters.get("geo-city-dk")
   ###########################################################
   data = yahoo_weatherapi(city)
   ############################################################
   query = data.get('query')
   if query is None:
       return {}

   result = query.get('results')
   if result is None:
       return {}

   channel = result.get('channel')
   if channel is None:
       return {}

   item = channel.get('item')
   location = channel.get('location')
   units = channel.get('units')
   if (location is None) or (item is None) or (units is None):
       return {}

   condition = item.get('condition')
   if condition is None:
       return {}

   link = item.get('link')
   link_forecast = link.split("*",1)[1]
   condition_get_code = condition.get('code')
   condition_code = weather_code(condition_get_code)
   image_url = "http://gdurl.com/" + condition_code
 
   speech = "Today in " + location.get('city') + ": " + condition.get('text') + \
            ", the temperature is " + condition.get('temp') + " " + units.get('temperature')
   res = {
         "speech": speech,
         "displayText": speech,
          "data" : {
             "facebook" : [
                 {
                    "sender_action": "typing_on"
                  },
                 {
                    "sender_action": "typing_on"
                  },
                 {
                "text": speech
                 },
                 {
                "attachment" : {
                  "type" : "template",
                    "payload" : {
                     "template_type" : "generic",
                      "elements" : [ 
                                {
                                  "title" : location.get('city') + "-" + location.get('country'),
                                  "image_url" : image_url,
                                  "subtitle" : "",
                                  "buttons": [{
                                       "type": "web_url",
                                       "url": link_forecast,
                                       "title": "Weather Forecast"
                                   }]
                                 } 
                          ]
                      } 
                  }
                },
                 {
                  "text": "Click on the below options to start over again",
                  "quick_replies": [
                 {
                  "content_type": "text",
                  "title": "News",
                  "payload": "news",
                  "image_url": "http://www.freeiconspng.com/uploads/newspaper-icon-20.jpg"
                 },
                 {
                  "content_type": "text",
                  "title": "Weather",
                  "payload": "weather",
                  "image_url": "https://www.mikeafford.com/store/store-images/ww01_example_light_rain_showers.png"
                   },
                  {
                  "content_type": "text",
                  "title": "Wikipedia",
                  "payload": "wikipedia",
                  "image_url": "https://upload.wikimedia.org/wikipedia/en/thumb/8/80/Wikipedia-logo-v2.svg/1122px-Wikipedia-logo-v2.svg.png"
                   },
                  {
                  "content_type": "text",
                  "title": "YouTube",
                  "payload": "youtube",
                  "image_url": "https://cdn1.iconfinder.com/data/icons/logotypes/32/youtube-512.png"
                   },
                  {
                  "content_type": "text",
                  "title": "Contact Us",
                  "payload": "contact",
                  "image_url": "https://cdn3.iconfinder.com/data/icons/communication-mass-media-news/512/phone_marketing-128.png"
                  }
                  ]
                 }
              ]
            } 
        };
   res = json.dumps(res, indent=4)
   r = make_response(res)
   r.headers['Content-Type'] = 'application/json'
   return r

def yahoo_weatherapi(city):

    yql_query = "select * from weather.forecast where woeid in (select woeid from geo.places(1) where text='" + city + "') and u='c'"
    if yql_query is None:
        return {}
    baseurl = "https://query.yahooapis.com/v1/public/yql?"
    yql_url = baseurl + urllib.parse.urlencode({'q': yql_query}) + "&format=json"
    result = urllib.request.urlopen(yql_url).read()
    data = json.loads(result)
    return data

def weather_code(condition_get_code):
# Below block of code is to check for weather condition code and map corresponding http://gdurl.com/#### permalink context

    if condition_get_code == "0":
       condition_code = "EmPG"
    elif condition_get_code == "1":
       condition_code = "mh7N"
    elif condition_get_code == "2":
       condition_code = "jENO"
    elif condition_get_code == "3":
       condition_code = "BTT7"
    elif condition_get_code == "4":
       condition_code = "kTWn"
    elif condition_get_code == "5":
       condition_code = "vBIX"
    elif condition_get_code == "6":
       condition_code = "zuxw"
    elif condition_get_code == "7":
       condition_code = "Vy9A"
    elif condition_get_code == "8":
       condition_code = "cT-0"
    elif condition_get_code == "9":
       condition_code = "M4nr"
    elif condition_get_code == "10":
       condition_code = "8-OZ"
    elif condition_get_code == "11":
       condition_code = "4sN0"
    elif condition_get_code == "12":
       condition_code = "SrHt"
    elif condition_get_code == "13":
       condition_code = "i925"
    elif condition_get_code == "14":
       condition_code = "9WKu"
    elif condition_get_code == "15":
       condition_code = "YjI9B"
    elif condition_get_code == "16":
       condition_code = "Lqmw"
    elif condition_get_code == "17":
       condition_code = "8wXj"
    elif condition_get_code == "18":
       condition_code = "AHL1"
    elif condition_get_code == "19":
       condition_code = "pSfX"
    elif condition_get_code == "20":
       condition_code = "ugKj"
    elif condition_get_code == "21":
       condition_code = "eFL0"
    elif condition_get_code == "22":
       condition_code = "Co_g" 
    elif condition_get_code == "23":
       condition_code = "h8uM"
    elif condition_get_code == "24":
       condition_code = "HBlw"
    elif condition_get_code == "25":
       condition_code = "QHzi"
    elif condition_get_code == "26":
       condition_code = "3IaA"
    elif condition_get_code == "27":
       condition_code = "i-dK"
    elif condition_get_code == "28":
       condition_code = "aIAw"
    elif condition_get_code == "29":
       condition_code = "6z8CS"
    elif condition_get_code == "30":
       condition_code = "xt2C"
    elif condition_get_code == "31":
       condition_code = "3Utr"
    elif condition_get_code == "32":
       condition_code = "YHpS"
    elif condition_get_code == "33":
       condition_code = "Hr4W"
    elif condition_get_code == "34":
       condition_code = "84WQ"
    elif condition_get_code == "35":
       condition_code = "3BH6"
    elif condition_get_code == "36":
       condition_code = "vjLN"
    elif condition_get_code == "37":
       condition_code = "41rl"
    elif condition_get_code == "38":
       condition_code = "8Ibx" 
    elif condition_get_code == "39":
       condition_code = "lIee"
    elif condition_get_code == "40":
       condition_code = "9GNz"
    elif condition_get_code == "41":
       condition_code = "uy77"
    elif condition_get_code == "42":
       condition_code = "15Ou"
    elif condition_get_code == "43":
       condition_code = "P_Jg"
    elif condition_get_code == "45":
       condition_code = "wF0D"
    elif condition_get_code == "46":
       condition_code = "1huQ"
    elif condition_get_code == "47":
       condition_code = "MlO5"
    elif condition_get_code == "3200":
       condition_code = "mgzs"
    else: 
       print ("Condition code did not match the sequence")

    return condition_code

#************************************************************************************#
#                                                                                    #
#   Below method is to get the Facebook Quick Reply Webhook Handling - Wikipedia     #
#                                                                                    #
#************************************************************************************#
def wikipedia_search(reqContext):
    option = reqContext.get("result").get("action")
    res = {
        "speech": "Please provide the topic you want to search in Wikipedia",
        "displayText": "Please provide the topic you want to search in Wikipedia",
        "data" : {
        "facebook" : [
               {
                "text": "Please write the topic you want to search in Wikipedia"
               }
             ]
           } 
         };
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

#************************************************************************************#
#                                                                                    #
#   This method is to get the Wikipedia Information via Google API                   #
#                                                                                    #
#************************************************************************************#
# Searchhook is for searching for Wkipedia information via Google API
def searchhook(reqContext):
    req = request.get_json(silent=True, force=True)
    resolvedQuery = reqContext.get("result").get("resolvedQuery")
    true_false = True
    baseurl = "https://www.googleapis.com/customsearch/v1?"
###########################################################
    result = req.get("result")
    parameters = result.get("parameters")
    search_list0 = parameters.get("any")
    search_u_string_removed = [str(i) for i in search_list0]
    search_list1 = str(search_u_string_removed)
    cumulative_string = search_list1.strip('[]')
    search_string = cumulative_string.replace(" ", "%20")
    search_string_ascii = search_string.encode('ascii')
    if search_string_ascii is None:
        return None
    google_query = "key=AIzaSyDNYsLn4JGIR4UaZMFTAgDB9gKN3rty2aM&cx=003066316917117435589%3Avcms6hy5lxs&q=" + search_string_ascii + "&num=1"
###########################################################
    if google_query is None:
        return {}
    #google_url = baseurl + urllib.parse.urlencode({google_query})
    google_url = baseurl + google_query
    result = urllib.request.urlopen(google_url).read()
    data = json.loads(result)
############################################################
    speech = data['items'][0]['snippet'].encode('utf-8').strip()
    for data_item in data['items']:
        link = data_item['link'],

    for data_item in data['items']:
        pagemap = data_item['pagemap'],

    cse_thumbnail_u_string_removed = [str(i) for i in pagemap]
    cse_thumbnail_u_removed = str(cse_thumbnail_u_string_removed)
    cse_thumbnail_brace_removed_1 = cse_thumbnail_u_removed.strip('[')
    cse_thumbnail_brace_removed_2 = cse_thumbnail_brace_removed_1.strip(']')
    cse_thumbnail_brace_removed_final =  cse_thumbnail_brace_removed_2.strip("'")
    keys = ('cse_thumbnail', 'metatags', 'cse_image')
    for key in keys:
        true_false = 'cse_thumbnail' in cse_thumbnail_brace_removed_final
        if true_false == True:
            for key in pagemap:
                cse_thumbnail = key['cse_thumbnail']
                for image_data in cse_thumbnail:
                    raw_str = image_data['src']
                    break
        else:
            raw_str = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTwdc3ra_4N2X5G06Rr5-L0QY8Gi6SuhUb3DiSN_M-C_nalZnVA"
            
    
    src_brace_removed_final = raw_str
    # Remove junk charaters from URL
    link_u_removal =  [str(i) for i in link]
    link_u_removed = str(link_u_removal)
    link_brace_removed_1 = link_u_removed.strip('[')
    link_brace_removed_2 = link_brace_removed_1.strip(']')
    link_final =  link_brace_removed_2.strip("'")
    # Remove junk character from search item
    search_string_final = cumulative_string.strip("'")
############################################################
    res = {
          "speech": speech,
          "displayText": speech,
           "data" : {
              "facebook" : [
                  {
                    "sender_action": "typing_on"
                  },
                  {
                 "attachment" : {
                   "type" : "template",
                     "payload" : {
                      "template_type" : "generic",
                       "elements" : [ 
                                 {
                                   "title" : search_string_final,
                                   "image_url" : src_brace_removed_final,
                                   "subtitle" : "",
                                   "buttons": [{
                                        "type": "web_url",
                                        "url": link_final,
                                        "title": "More info"
                                    }]
                                 } 
                           ]
                       } 
                   }
                },
                 {
                 "text": speech
                  },
                 {
                  "text": "Click on the below options to start over again",
                  "quick_replies": [
                 {
                  "content_type": "text",
                  "title": "News",
                  "payload": "News",
                  "image_url": "http://www.freeiconspng.com/uploads/newspaper-icon-20.jpg"
                 },
                 {
                  "content_type": "text",
                  "title": "Weather",
                  "payload": "weather",
                  "image_url": "https://www.mikeafford.com/store/store-images/ww01_example_light_rain_showers.png"
                   },
                  {
                  "content_type": "text",
                  "title": "Wikipedia",
                  "payload": "wikipedia",
                  "image_url": "https://upload.wikimedia.org/wikipedia/en/thumb/8/80/Wikipedia-logo-v2.svg/1122px-Wikipedia-logo-v2.svg.png"
                   },
                  {
                  "content_type": "text",
                  "title": "YouTube",
                  "payload": "YouTube",
                  "image_url": "https://cdn1.iconfinder.com/data/icons/logotypes/32/youtube-512.png"
                   },
                  {
                  "content_type": "text",
                  "title": "Contact Us",
                  "payload": "contact",
                  "image_url": "https://cdn3.iconfinder.com/data/icons/communication-mass-media-news/512/phone_marketing-128.png"
                  }
                  ]
                 }
               ]
             } 
         };
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

#************************************************************************************#
#                                                                                    #
#   This method is to get the Wikipedia Information via Google API via Funnel        #
#                                                                                    #
#************************************************************************************#
# Searchhook is for searching for Wkipedia information via Google API
def wikipediaInformationSearch(reqContext):
    #req = request.get_json(silent=True, force=True)
    resolvedQuery = reqContext.get("result").get("resolvedQuery")
    true_false = True
    baseurl = "https://www.googleapis.com/customsearch/v1?"
    resolvedQueryFinal = resolvedQuery.replace(" ", "%20")
    search_string_ascii = resolvedQueryFinal.encode('ascii')
    if search_string_ascii is None:
        return None
    google_query = "key=AIzaSyDNYsLn4JGIR4UaZMFTAgDB9gKN3rty2aM&cx=003066316917117435589%3Avcms6hy5lxs&q=" + search_string_ascii + "&num=1"
###########################################################
    if google_query is None:
        return {}
    google_url = baseurl + google_query
    result = urllib.request.urlopen(google_url).read()
    data = json.loads(result)
############################################################
    speech = data['items'][0]['snippet'].encode('utf-8').strip()
    for data_item in data['items']:
        link = data_item['link'],

    for data_item in data['items']:
        pagemap = data_item['pagemap'],

    cse_thumbnail_u_string_removed = [str(i) for i in pagemap]
    cse_thumbnail_u_removed = str(cse_thumbnail_u_string_removed)
    cse_thumbnail_brace_removed_1 = cse_thumbnail_u_removed.strip('[')
    cse_thumbnail_brace_removed_2 = cse_thumbnail_brace_removed_1.strip(']')
    cse_thumbnail_brace_removed_final =  cse_thumbnail_brace_removed_2.strip("'")
    keys = ('cse_thumbnail', 'metatags', 'cse_image')
    for key in keys:
        true_false = 'cse_thumbnail' in cse_thumbnail_brace_removed_final
        if true_false == True:
            for key in pagemap:
                cse_thumbnail = key['cse_thumbnail']
                for image_data in cse_thumbnail:
                    raw_str = image_data['src']
                    break
        else:
            raw_str = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTwdc3ra_4N2X5G06Rr5-L0QY8Gi6SuhUb3DiSN_M-C_nalZnVA"
           
    src_brace_removed_final = raw_str
    # Remove junk charaters from URL
    link_u_removal =  [str(i) for i in link]
    link_u_removed = str(link_u_removal)
    link_brace_removed_1 = link_u_removed.strip('[')
    link_brace_removed_2 = link_brace_removed_1.strip(']')
    link_final =  link_brace_removed_2.strip("'")
    # Remove junk character from search item
    search_string_final = resolvedQuery.strip("'")
############################################################
    res = {
          "speech": speech,
          "displayText": speech,
           "data" : {
              "facebook" : [
                  {
                    "sender_action": "typing_on"
                  },
                  {
                 "attachment" : {
                   "type" : "template",
                     "payload" : {
                      "template_type" : "generic",
                       "elements" : [ 
                                 {
                                   "title" : search_string_final,
                                   "image_url" : src_brace_removed_final,
                                   "subtitle" : "",
                                   "buttons": [{
                                        "type": "web_url",
                                        "url": link_final,
                                        "title": "More info"
                                    }]
                                 } 
                           ]
                       } 
                   }
                },
                 {
                 "text": speech
                  },
                 {
                  "text": "Click on the below options to start over again",
                  "quick_replies": [
                 {
                  "content_type": "text",
                  "title": "News",
                  "payload": "News",
                  "image_url": "http://www.freeiconspng.com/uploads/newspaper-icon-20.jpg"
                 },
                 {
                  "content_type": "text",
                  "title": "Weather",
                  "payload": "Weather",
                  "image_url": "https://www.mikeafford.com/store/store-images/ww01_example_light_rain_showers.png"
                   },
                  {
                  "content_type": "text",
                  "title": "Wikipedia",
                  "payload": "Wikipedia",
                  "image_url": "https://upload.wikimedia.org/wikipedia/en/thumb/8/80/Wikipedia-logo-v2.svg/1122px-Wikipedia-logo-v2.svg.png"
                   },
                  {
                  "content_type": "text",
                  "title": "YouTube",
                  "payload": "YouTube",
                  "image_url": "https://cdn1.iconfinder.com/data/icons/logotypes/32/youtube-512.png"
                   },
                  {
                  "content_type": "text",
                  "title": "Contact Us",
                  "payload": "contact",
                  "image_url": "https://cdn3.iconfinder.com/data/icons/communication-mass-media-news/512/phone_marketing-128.png"
                  }
                  ]
                 }
               ]
             } 
         };
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


#************************************************************************************#
#                                                                                    #

#   Below method is to get the Facebook Quick Reply Webhook Handling - YOUTUBE       #
#                                                                                    #
#************************************************************************************#
def youtubeTopic(reqContext):
    option = reqContext.get("result").get("action")
    res = {
        "speech": "Please provide a topic to search in YouTube:",
        "displayText": "Please provide a topic to search in YouTube:",
        "data" : {
        "facebook" : [
               {
                "text": "Please provide a topic to search in YouTube:"
               }
             ]
           } 
         };
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

#************************************************************************************#
#                                                                                    #
#   This method is for searching YouTube videos via YouTube API via Funnel           #
#                                                                                    #
#************************************************************************************#

def youtubeVideoSearch(reqContext):
    resolvedQuery = reqContext.get("result").get("resolvedQuery")
    true_false = True
    baseurl = "https://www.googleapis.com/youtube/v3/search?part=id&q="
    resolvedQueryFinal = resolvedQuery.replace(" ", "%20")
    search_string_ascii = resolvedQueryFinal.encode('ascii')
    if search_string_ascii is None:
        return None
    youtube_query = "&type=video&fields=items%2Fid&key=AIzaSyDNYsLn4JGIR4UaZMFTAgDB9gKN3rty2aM&cx=003066316917117435589%3Avcms6hy5lxs&num=5"
    if youtube_query is None:
        return {}
    youtube_query = baseurl + search_string_ascii + youtube_query
    result = urllib.request.urlopen(youtube_query).read()
    data = json.loads(result)
    
    items = data['items']
    id_list = []

    for id_block in items:
        id = id_block['id']
        id_list.append(id)

    
    res = {
          "speech": "Video",
          "displayText": "Video",
           "data" : {
              "facebook" : [
                  {
                    "sender_action": "typing_on"
                  },
                  {
                    "attachment":{
                    "type":"template",
                    "payload":{
                       "template_type":"open_graph",
                       "elements":[
                        {
                          "url":"https://www.youtube.com/watch?v=" + id_list[0].get('videoId')
                        }
                    ]
                   }
                 }
                },
                {
                    "attachment":{
                    "type":"template",
                    "payload":{
                       "template_type":"open_graph",
                       "elements":[
                        {
                          "url":"https://www.youtube.com/watch?v=" + id_list[1].get('videoId')
                        }
                    ]
                   }
                 }
                },
                {
                    "attachment":{
                    "type":"template",
                    "payload":{
                       "template_type":"open_graph",
                       "elements":[
                        {
                          "url":"https://www.youtube.com/watch?v=" + id_list[2].get('videoId')
                        }
                    ]
                   }
                 }
                },
                {
                    "attachment":{
                    "type":"template",
                    "payload":{
                       "template_type":"open_graph",
                       "elements":[
                        {
                          "url":"https://www.youtube.com/watch?v=" + id_list[3].get('videoId')
                        }
                    ]
                   }
                 }
                },
                {
                    "attachment":{
                    "type":"template",
                    "payload":{
                       "template_type":"open_graph",
                       "elements":[
                        {
                          "url":"https://www.youtube.com/watch?v=" + id_list[4].get('videoId')
                        }
                    ]
                   }
                 }
                },
                 {
                  "text": "Click on the below options to start over again",
                  "quick_replies": [
                 {
                  "content_type": "text",
                  "title": "News",
                  "payload": "News",
                  "image_url": "http://www.freeiconspng.com/uploads/newspaper-icon-20.jpg"
                 },
                 {
                  "content_type": "text",
                  "title": "Weather",
                  "payload": "Weather",
                  "image_url": "https://www.mikeafford.com/store/store-images/ww01_example_light_rain_showers.png"
                   },
                  {
                  "content_type": "text",
                  "title": "Wikipedia",
                  "payload": "Wikipedia",
                  "image_url": "https://upload.wikimedia.org/wikipedia/en/thumb/8/80/Wikipedia-logo-v2.svg/1122px-Wikipedia-logo-v2.svg.png"
                   },
                  {
                  "content_type": "text",
                  "title": "YouTube",
                  "payload": "YouTube",
                  "image_url": "https://cdn1.iconfinder.com/data/icons/logotypes/32/youtube-512.png"
                   },
                  {
                  "content_type": "text",
                  "title": "Contact Us",
                  "payload": "contact",
                  "image_url": "https://cdn3.iconfinder.com/data/icons/communication-mass-media-news/512/phone_marketing-128.png"
                  }
                  ]
                 }
               ]
             } 
         };
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

#************************************************************************************#
#                                                                                    #
#   Below method is to get the Facebook Quick Reply Webhook Handling - NEWS          #
#                                                                                    #
#************************************************************************************#
def newsCategory(reqContext):
    res = {
            "speech": "Please select the category",
            "displayText": "Please select the category",
            "data" : {
            "facebook" : [
                 {
                  "text": "Please select your favourite category:",
                  "quick_replies": [
                 {
                  "content_type": "text",
                  "title": "Latest News",
                  "payload": "topnews",
                  "image_url": "http://www.freeiconspng.com/uploads/news-icon-13.png"
                  },
                 {
                  "content_type": "text",
                  "title": "Sports",
                  "payload": "sports",
                  "image_url": "http://thebridgeconference.com/wp-content/uploads/2014/05/main_paragraph_icon.png"
                  },
                  {
                  "content_type": "text",
                  "title": "Finance",
                  "payload": "business",
                  "image_url": "https://phil.ca/wp-content/uploads/2015/12/funraising-icons_fundraising.png"
                  },
                  {
                  "content_type": "text",
                  "title": "Technology",
                  "payload": "technology",
                  "image_url": "https://cdn.pixabay.com/photo/2015/12/04/22/20/gear-1077550_640.png"
                  },
                  {
                  "content_type": "text",
                  "title": "Entertainment",
                  "payload": "entertainment",
                  "image_url": "https://userscontent2.emaze.com/images/2afc7b67-eba3-41c8-adce-b1e2b1c34b02/99782968e977045b1f88f94d0c4e00cf.png"
                  },
                  {
                  "content_type": "text",
                  "title": "Science & Nature",
                  "payload": "science",
                  "image_url": "https://www.designmate.com/images/biology1.png"
                  }
                  ]
                 }
              ]
            } 
         };
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

#************************************************************************************#
#                                                                                    #
#   Below method is to get the provide News Category Quick Replies - Top News        #
#                                                                                    #
#************************************************************************************#
def news_category_topnews(reqContext):
    resolvedQuery = reqContext.get("result").get("resolvedQuery")
    if resolvedQuery == "topnews":
        res = {
            "speech": "Please select your favourite Newspaper:",
            "displayText": "Please select your favourite Newspaper:",
            "data" : {
            "facebook" : [
                 {
                  "text": "Please select the Newspaper of your choice:",
                  "quick_replies": [
                 {
                  "content_type": "text",
                  "title": "The Times Of India",
                  "payload": "the-times-of-india",
                  "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTGUM0uhwsV3vp9ZzMEnjJo4MDZRSC3cgp32qH64zZlWFsAiGNv"
                  },
                 {
                  "content_type": "text",
                  "title": "BBC News",
                  "payload": "bbc-news",
                  "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSWrLeudSaMDHDclbCjfvVoOdIK9q3XKqbWG5G1aDJzO3z6YZUP"
                  },
                  {
                  "content_type": "text",
                  "title": "CNN",
                  "payload": "cnn",
                  "image_url": "https://qph.ec.quoracdn.net/main-qimg-583846beabeef96102a6f18fc2096a82-c"
                  },
                  {
                  "content_type": "text",
                  "title": "Time",
                  "payload": "time",
                  "image_url": "https://s0.wp.com/wp-content/themes/vip/time2014/img/time-touch_icon_152.png"
                  },
                  {
                  "content_type": "text",
                  "title": "USA Today",
                  "payload": "usa-today",
                  "image_url": "http://www.gmkfreelogos.com/logos/U/img/U_Bahn.gif"
                  },
                  {
                  "content_type": "text",
                  "title": "The Telegraph",
                  "payload": "the-telegraph",
                  "image_url": "https://media.glassdoor.com/sqll/700053/the-telegraph-calcutta-squarelogo-1475068747795.png"
                  },
                  {
                  "content_type": "text",
                  "title": "The Washington Post",
                  "payload": "the-washington-post",
                  "image_url": "https://static1.squarespace.com/static/58505df4579fb348904cdf5f/t/58ab141b20099e74879fe27f/1487606851497/wp.jog"
                  },
                  {
                  "content_type": "text",
                  "title": "The Guardian (UK)",
                  "payload": "the-guardian-uk",
                  "image_url": "http://a2.mzstatic.com/eu/r30/Purple62/v4/0b/a9/56/0ba956de-3621-3585-285e-1141b53d4d51/icon175x175.png"
                  },
                  {
                  "content_type": "text",
                  "title": "The Guardian (AU)",
                  "payload": "the-guardian-au",
                  "image_url": "http://a2.mzstatic.com/eu/r30/Purple62/v4/0b/a9/56/0ba956de-3621-3585-285e-1141b53d4d51/icon175x175.png"
                  },
                  {
                  "content_type": "text",
                  "title": "Reuters",
                  "payload": "reuters",
                  "image_url": "http://www.adweek.com/wp-content/uploads/sites/9/2013/09/reuters-logo.jpg"
                  },
                  {
                  "content_type": "text",
                  "title": "The Hindu",
                  "payload": "the-hindu",
                  "image_url": "https://lh4.ggpht.com/_wAwneNQFfcruC-YiUpWKPtBTpzfdqLVTIArJyYRt52xGm4ABVQKT5eeLb_rl6em42kO=w300"
                  }
                  ]
                 }
              ]
            } 
         };
    elif resolvedQuery == "sports":
        res = {
            "speech": "Please select the Newspaper of your choice:",
            "displayText": "Please select the Newspaper of your choice:",
            "data" : {
            "facebook" : [
                 {
                  "text": "Please select the Newspaper of your choice:",
                  "quick_replies": [
                 {
                  "content_type": "text",
                  "title": "ESPN",
                  "payload": "espn",
                  "image_url": "https://www.brandsoftheworld.com/sites/default/files/styles/logo-thumbnail/public/052016/untitled-1_242.png?itok=vy3l2HxD"
                  },
                  {
                  "content_type": "text",
                  "title": "Fox Sports",
                  "payload": "fox-sports",
                  "image_url": "http://i48.tinypic.com/rwroy1.gif"
                  },
                  {
                  "content_type": "text",
                  "title": "BBC Sport",
                  "payload": "bbc-sport",
                  "image_url": "http://yellingperformance.com/wp-content/uploads/2014/08/bbc-sport.png"
                  },
                  {
                  "content_type": "text",
                  "title": "Four Four Two",
                  "payload": "four-four-two",
                  "image_url": "http://www.free-icons-download.net/images/football-icon-53581.png"
                  },
                  {
                  "content_type": "text",
                  "title": "NFL",
                  "payload": "nfl-news",
                  "image_url": "http://orig09.deviantart.net/4d3f/f/2013/087/7/e/nfl_icon_by_slamiticon-d5zbovo.png"
                  },
                  {
                  "content_type": "text",
                  "title": "The Sport Bible",
                  "payload": "the-sport-bible",
                  "image_url": "https://pbs.twimg.com/profile_images/528682495923859456/yuXwYzR4.png"
                  }
                  ]
                 }
              ]
            } 
         };
    elif resolvedQuery == "business":
        res = {
            "speech": "Please select the Newspaper of your choice:",
            "displayText": "Please select the Newspaper of your choice:",
            "data" : {
            "facebook" : [
                 {
                  "text": "Please select the Newspaper of your choice:",
                  "quick_replies": [
                 {
                  "content_type": "text",
                  "title": "The Economist",
                  "payload": "the-economist",
                  "image_url": "https://gs-img.112.ua/original/2016/04/01/221445.jpg"
                  },
                 {
                  "content_type": "text",
                  "title": "Financial Times",
                  "payload": "financial-times",
                  "image_url": "http://www.adweek.com/wp-content/uploads/sites/10/2014/03/financial_times_logo304x200.jpg"
                  },
                  {
                  "content_type": "text",
                  "title": "CNBC",
                  "payload": "cnbc",
                  "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e3/CNBC_logo.svg/961px-CNBC_logo.svg.png"
                  },
                  {
                  "content_type": "text",
                  "title": "Business Insider",
                  "payload": "business-insider",
                  "image_url": "https://pbs.twimg.com/profile_images/661313209605976064/EjEK7KeO.jpg"
                  },
                  {
                  "content_type": "text",
                  "title": "Fortune",
                  "payload": "fortune",
                  "image_url": "https://fortunedotcom.files.wordpress.com/2014/05/f_icon_orange_1.png"
                  },
                  {
                  "content_type": "text",
                  "title": "The Wall Street Journal",
                  "payload": "the-wall-street-journal",
                  "image_url": "https://www.wsj.com/apple-touch-icon.png"
                  }
                  ]
                 }
              ]
            } 
         };
    elif resolvedQuery == "technology":
        res = {
            "speech": "Please select the Newspaper of your choice:",
            "displayText": "Please select the Newspaper of your choice:",
            "data" : {
            "facebook" : [
                 {
                  "text": "Please select the Newspaper of your choice:",
                  "quick_replies": [
                 {
                  "content_type": "text",
                  "title": "TechRadar",
                  "payload": "techradar",
                  "image_url": "http://www.ittiam.com/vividhdr/img/techradar.jpg"
                  },
                 {
                  "content_type": "text",
                  "title": "TechCrunch",
                  "payload": "techcrunch",
                  "image_url": "https://tctechcrunch2011.files.wordpress.com/2014/04/tc-logo.jpg"
                  },
                  {
                  "content_type": "text",
                  "title": "T3N",
                  "payload": "t3n",
                  "image_url": "https://pbs.twimg.com/profile_images/2267864145/8oalkkbzq6davn5snoi4.png"
                  },
                  {
                  "content_type": "text",
                  "title": "Hacker News",
                  "payload": "hacker-news",
                  "image_url": "https://pbs.twimg.com/profile_images/659012257985097728/AXXMa-X2.png"
                  },
                  {
                  "content_type": "text",
                  "title": "Buzzfeed",
                  "payload": "buzzfeed",
                  "image_url": "https://static-s.aa-cdn.net/img/ios/352969997/d5f0fe265f21af1cffd41964bc7b46ab"
                  },
                  {
                  "content_type": "text",
                  "title": "Recode",
                  "payload": "recode",
                  "image_url": "https://cdn.vox-cdn.com/uploads/hub/sbnu_logo/633/large_mark.64395.png"
                  }
                  ]
                 }
              ]
            } 
         };
    elif resolvedQuery == "entertainment":
        res = {
            "speech": "Please select the Newspaper of your choice:",
            "displayText": "Please select the Newspaper of your choice:",
            "data" : {
            "facebook" : [
                 {
                  "text": "Please select the Newspaper of your choice:",
                  "quick_replies": [
                 {
                  "content_type": "text",
                  "title": "MTV News",
                  "payload": "mtv-news",
                  "image_url": "http://imagesmtv-a.akamaihd.net/uri/mgid:file:http:shared:mtv.com/news/wp-content/uploads/2016/07/staff-author-250-1468362828.png?format=jpg&quality=.8"
                  },
                  {
                  "content_type": "text",
                  "title": "MTV News (UK)",
                  "payload": "mtv-news-uk",
                  "image_url": "http://imagesmtv-a.akamaihd.net/uri/mgid:file:http:shared:mtv.com/news/wp-content/uploads/2016/07/staff-author-250-1468362828.png?format=jpg&quality=.8"
                  }
                  ]
                 }
              ]
            } 
         };
    elif resolvedQuery == "science":
        res = {
            "speech": "Please select the Newspaper of your choice:",
            "displayText": "Please select the Newspaper of your choice:",
            "data" : {
            "facebook" : [
                 {
                  "text": "Please select the Newspaper of your choice:",
                  "quick_replies": [
                 {
                  "content_type": "text",
                  "title": "National Geographic",
                  "payload": "national-geographic",
                  "image_url": "https://pbs.twimg.com/profile_images/798181194202566656/U8QbCBdH_400x400.jpg"
                  },
                 {
                  "content_type": "text",
                  "title": "New Scientist",
                  "payload": "new-scientist",
                  "image_url": "http://www.peteraldhous.com/Images/ns.jpg"
                  }
                  ]
                 }
              ]
            } 
         };
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

#************************************************************************************#
#                                                                                    #
#   Below method is to get the News Details in JSON Format and put as List Template  #
#                                                                                    #
#************************************************************************************#
newspaper_url = ''
data = ''
def topFourNewsArticle(reqContext):
    resolvedQuery = reqContext.get("result").get("resolvedQuery")
    newsAPI = "https://newsapi.org/v1/articles?source=" + resolvedQuery + "&sortBy=top&apiKey=" + newspai_access_token
    result = urllib.request.urlopen(newsAPI).read()
    data = json.loads(result)
    newspaper_url = newsWebsiteIdentification(resolvedQuery)
    res = {
            "speech": "NewsList",
            "displayText": "NewsList",
            "data" : {
            "facebook" : [
                 {
                    "sender_action": "typing_on"
                  },
                 {
                "attachment" : {
                  "type" : "template",
                    "payload" : {
                     "template_type" : "list",
                     "elements" : [ 
                        {
                            "title": data['articles'][0]['title'],
                            "image_url": data['articles'][0]['urlToImage'],
                            "default_action": {
                               "type": "web_url",
                               "url": data['articles'][0]['url'],
                                "webview_height_ratio": "tall",
                                },
                            "buttons": [
                            {
                               "title": "Read Article",
                               "type": "web_url",
                               "url": data['articles'][0]['url'],
                               "webview_height_ratio": "tall",
                            }
                          ]
                        },
                        {
                            "title": data['articles'][1]['title'],
                            "image_url": data['articles'][1]['urlToImage'],
                            "subtitle": data['articles'][1]['description'],
                            "default_action": 
                                {
                                    "type": "web_url",
                                    "url": data['articles'][1]['url'],
                                    "webview_height_ratio": "tall"
                                },
                                "buttons": [
                                {
                                     "title": "Read Article",
                                     "type": "web_url",
                                     "url": data['articles'][1]['url'],
                                     "webview_height_ratio": "tall"
                                }
                               ]
                        },
                        {
                            "title": data['articles'][2]['title'],
                            "image_url": data['articles'][2]['urlToImage'],
                            "subtitle": data['articles'][2]['description'],
                            "default_action": 
                               {
                                   "type": "web_url",
                                   "url": data['articles'][2]['url'],
                                   "webview_height_ratio": "tall"
                                },
                                "buttons": [
                                {
                                   "title": "Read Article",
                                   "type": "web_url",
                                   "url": data['articles'][2]['url'],
                                   "webview_height_ratio": "tall"
                                }
                              ]
                       },
                       {
                            "title": data['articles'][3]['title'],
                            "image_url": data['articles'][3]['urlToImage'],
                            "subtitle": data['articles'][3]['description'],
                            "default_action": 
                            {
                                "type": "web_url",
                                "url": data['articles'][3]['url'],
                                "webview_height_ratio": "tall"
                            },
                            "buttons": [
                            {
                                "title": "Read Article",
                                "type": "web_url",
                                "url": data['articles'][3]['url'],
                                "webview_height_ratio": "tall"
                            }
                           ]
                        }
                        ],
                        "buttons": [
                         {
                            "title": "View Site",
                            "type": "web_url",
                            "url": newspaper_url
                        }
                       ]  
                     } 
                   }
                 },
                 {
                  "text": "Click on the below options to start over again",
                  "quick_replies": [
                 {
                  "content_type": "text",
                  "title": "News",
                  "payload": "News",
                  "image_url": "http://www.freeiconspng.com/uploads/newspaper-icon-20.jpg"
                 },
                 {
                  "content_type": "text",
                  "title": "Weather",
                  "payload": "Weather",
                  "image_url": "https://www.mikeafford.com/store/store-images/ww01_example_light_rain_showers.png"
                   },
                  {
                  "content_type": "text",
                  "title": "Wikipedia",
                  "payload": "Wikipedia",
                  "image_url": "https://upload.wikimedia.org/wikipedia/en/thumb/8/80/Wikipedia-logo-v2.svg/1122px-Wikipedia-logo-v2.svg.png"
                   },
                  {
                  "content_type": "text",
                  "title": "YouTube",
                  "payload": "YouTube",
                  "image_url": "https://cdn1.iconfinder.com/data/icons/logotypes/32/youtube-512.png"
                   },
                  {
                  "content_type": "text",
                  "title": "Contact Us",
                  "payload": "contact",
                  "image_url": "https://cdn3.iconfinder.com/data/icons/communication-mass-media-news/512/phone_marketing-128.png"
                  }
                  ]
                 }
               ]
             } 
           };
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


#************************************************************************************#
#                                                                                    #
#   Identifying Newspaper Website                                                    #
#                                                                                    #
#************************************************************************************#
def newsWebsiteIdentification(resolvedQuery):

    if resolvedQuery == "the-times-of-india":
       newspaper_url = "http://timesofindia.indiatimes.com"
    elif resolvedQuery == "bbc-news":
       newspaper_url = "http://www.bbc.com/news"
    elif resolvedQuery == "cnn":
       newspaper_url = "http://edition.cnn.com"
    elif resolvedQuery == "time":
       newspaper_url = "http://time.com"
    elif resolvedQuery == "usa-today":
       newspaper_url = "https://www.usatoday.com"
    elif resolvedQuery == "the-telegraph":
       newspaper_url = "http://www.telegraph.co.uk"
    elif resolvedQuery == "the-washington-post":
       newspaper_url = "https://www.washingtonpost.com"
    elif resolvedQuery == "the-guardian-uk":
       newspaper_url = "https://www.theguardian.com/uk"
    elif resolvedQuery == "the-guardian-au":
       newspaper_url = "https://www.theguardian.com/au"
    elif resolvedQuery == "reuters":
       newspaper_url = "http://www.reuters.com"
    elif resolvedQuery == "the-hindu":
       newspaper_url = "http://www.thehindu.com"
    elif resolvedQuery == "espn":
       newspaper_url = "http://espn.go.com"
    elif resolvedQuery == "espn-cric-info":
       newspaper_url = "http://www.espncricinfo.com"
    elif resolvedQuery == "four-four-two":
       newspaper_url = "https://www.fourfourtwo.com/"
    elif resolvedQuery == "bbc-sport":
       newspaper_url = "http://www.bbc.com/sport"
    elif resolvedQuery == "fox-sports":
       newspaper_url = "http://www.foxsports.com"
    elif resolvedQuery == "the-sport-bible":
       newspaper_url = "http://www.sportbible.com"
    elif resolvedQuery == "the-economist":
       newspaper_url = "https://www.economist.com"
    elif resolvedQuery == "financial-times":
       newspaper_url = "https://www.ft.com"
    elif resolvedQuery == "cnbc":
       newspaper_url = "http://www.cnbc.com"
    elif resolvedQuery == "business-insider":
       newspaper_url = "http://nordic.businessinsider.com"
    elif resolvedQuery == "fortune":
       newspaper_url = "http://fortune.com"
    elif resolvedQuery == "the-wall-street-journal":
       newspaper_url = "https://www.wsj.com"
    elif resolvedQuery == "techradar":
       newspaper_url = "http://www.techradar.com"
    elif resolvedQuery == "techcrunch":
       newspaper_url = "https://techcrunch.com"
    elif resolvedQuery == "t3n":
       newspaper_url = "http://t3n.de"
    elif resolvedQuery == "hacker-news":
       newspaper_url = "http://thehackernews.com"
    elif resolvedQuery == "buzzfeed":
       newspaper_url = "https://www.buzzfeed.com"
    elif resolvedQuery == "entertainment-weekly":
       newspaper_url = "http://ew.com"
    elif resolvedQuery == "mtv-news":
       newspaper_url = "http://www.mtv.com"
    elif resolvedQuery == "mtv-news-uk":
       newspaper_url = "http://www.mtv.co.uk/news"
    elif resolvedQuery == "national-geographic":
       newspaper_url = "http://www.nationalgeographic.com"
    elif resolvedQuery == "new-scientist":
       newspaper_url = "https://www.newscientist.com"
    elif resolvedQuery == "nfl-news":
       newspaper_url = "https://www.nfl.com"

    else: 
       print ("Newspaper name did not match the input")

    return newspaper_url

#************************************************************************************#
#                                                                                    #
#   Help Information Providing                                                       #
#                                                                                    #
#************************************************************************************#
def help(resolvedQuery):
    speech = "I'm sorry if I make you confused. Please select Quick Reply or Menu to chat with me. \n\n 1. Click on 'News' to read latest news from 33 globally leading newspapers \n 2. Click on 'Weather' and write a city name to get weather forecast \n 3. Click on 'Wikipedia' and write a topic you want to know about. No need to ask a full question. \n 4. Click on 'YouTube' and search for your favourite videos. \n 5. You can still chat directly with Marvin without the quick replies like before for - Weather, Wikipedia & Small Talk."
    res = {
        "speech": speech,
        "displayText": speech,
        "data" : {
        "facebook" : [
               {
                "text": speech
               }
             ]
           } 
         };
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r
#************************************************************************************#
#                                                                                    #
#   Contact Information                                                              #
#                                                                                    #
#************************************************************************************#
def contact(resolvedQuery):
    print ("Within CONTACT US method")
    speech = "Our company is now present in Denmark & Australia. \nGrow your business with AI Chatbot. \nRequest for a free Demo now."
    res = {
        "speech": speech,
        "displayText": speech,
        "data" : {
        "facebook" : [
                {
                 "text": speech
                },
                {
                 "attachment" : {
                   "type" : "template",
                     "payload" : {
                      "template_type" : "generic",
                       "elements" : [ 
                                 {
                                   "title" : "Swapratim Roy",
                                   "image_url" : "https://marvinchatbot.files.wordpress.com/2017/06/swapratim-roy-founder-owner-of-marvin-ai.jpg?w=700&h=&crop=1",
                                   "subtitle" : "Founder & Owner of Marvin.ai \nAarhus, Denmark \nCall: +45-7182-5584",
                                   "buttons": [{
                                        "type": "web_url",
                                        "url": "https://www.messenger.com/t/swapratim.roy",
                                        "title": "Connect on Messenger"
                                    },
                                    {
                                        "type": "web_url",
                                        "url": "https://marvinai.live",
                                        "title": "View Website"
                                    }]
                                 },
                                 {
                                   "title" : "Arnab Dasgupta",
                                   "image_url" : "https://marvinchatbot.files.wordpress.com/2017/06/arnab-dasgupta-ceo-of-marvin-ai.jpg?w=700&h=&crop=1",
                                   "subtitle" : "CEO of Marvin.ai \nMelbourne, Australia \nCall: +61-469-029-387",
                                   "buttons": [{
                                        "type": "web_url",
                                        "url": "https://www.messenger.com/t/arnabdasgupta.uk",
                                        "title": "Connect on Messenger"
                                    },
                                    {
                                        "type": "web_url",
                                        "url": "https://marvinai.live",
                                        "title": "View Website"
                                    }]
                                 } 
                           ]
                       } 
                   }
                },
                {
                  "text": "Start over again",
                  "quick_replies": [
                 {
                  "content_type": "text",
                  "title": "News",
                  "payload": "News",
                  "image_url": "http://www.freeiconspng.com/uploads/newspaper-icon-20.jpg"
                 },
                 {
                  "content_type": "text",
                  "title": "Weather",
                  "payload": "Weather",
                  "image_url": "https://www.mikeafford.com/store/store-images/ww01_example_light_rain_showers.png"
                   },
                  {
                  "content_type": "text",
                  "title": "Wikipedia",
                  "payload": "Wikipedia",
                  "image_url": "https://upload.wikimedia.org/wikipedia/en/thumb/8/80/Wikipedia-logo-v2.svg/1122px-Wikipedia-logo-v2.svg.png"
                   },
                  {
                  "content_type": "text",
                  "title": "YouTube",
                  "payload": "YouTube",
                  "image_url": "https://cdn1.iconfinder.com/data/icons/logotypes/32/youtube-512.png"
                   },
                  {
                  "content_type": "text",
                  "title": "Contact Us",
                  "payload": "contact",
                  "image_url": "https://cdn3.iconfinder.com/data/icons/communication-mass-media-news/512/phone_marketing-128.png"
                  }
                  ]
                 }
             ]
           } 
         };
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("Starting APPLICATION on port %d" % port)
    context.run(debug=True, port=port, host='0.0.0.0')