# test the Event Registry api. This code uses Event Registry's api to collect articles that fall
# into the category: "video games"

from eventregistry import *
import json
from slugify import slugify
import short_url

def getNews(apikey):
	er = EventRegistry(apiKey = "a9f1a681-546e-43b1-96aa-24443c47a837")
	# prepare the category URI to be used in the queries
	video_games_uri = QueryItems.OR([er.getCategoryUri("Video Games"), er.getCategoryUri("Video Games Conventions")])
	#print(video_games_uri)
	# query articles that match the category: "video games" and then print the articles out in json format
	q = QueryArticlesIter(
		keywords = QueryItems.OR(["Video Games", "esports"]),
		categoryUri = video_games_uri)
	dicklist = []
	for article in q.execQuery(er, sortBy = "date", maxItems = 10):
		dicktionary = {}
		dicktionary["url"] = article["url"]
		dicktionary["date"] = article["date"]
		dicktionary["title"] = article["title"]
		dicklist.append(dicktionary)
	print("done")
	return dicklist
