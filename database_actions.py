import pymongo
import os
import dns
import constants
import json
import functions
from bson.objectid import ObjectId
#Run pip3 install pymongo[srv]


class MongoDBConnection(object):
    """MongoDB Connection"""
    def __init__(self):
        self.connection = None

    def __enter__(self):
        self.connection = pymongo.MongoClient(os.getenv('Mongo_URL'))
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()


def add_notif(options):
    try:
        mongo = MongoDBConnection()
        with mongo:
            if mongo.connection.TMDB.notifications.find(options).count() == 0:
                mongo.connection.TMDB.notifications.insert_one(options)
                return "Added Sucessfully"
            else:
                return "Notification Exists"
        #for initial testing
        #print(mongo.connection.TMDB.users.replace_one({'_id': author.id}, tuser, True))   #Maybe don't print this in the future?
    except:
        print("Database is down!")
        return -2


def db_check():
    try:
        mongo = MongoDBConnection()
        output = ""
        with mongo:
            collection = mongo.connection.TMDB.users
            serverStatusResult = mongo.connection.TMDB.command("serverStatus")
            output = "MongoDB is live at: " + str(serverStatusResult['localTime']) + '\n' + "Host: " + str(serverStatusResult['host']) + '\n' + "version: " + str(serverStatusResult['version'])
            print(serverStatusResult)
            return output
    except:
        print("Database is down!")
        return "Database is down!"


def get_notif(options):
    try:
        mongo = MongoDBConnection()
        #print("get_notif-----")
        #print(options)
        output = ""
        with mongo:
            if mongo.connection.TMDB.notifications.find(options).count() > 0:
                for results in mongo.connection.TMDB.notifications.find(options, constants.proj_omissions):
                    output = functions.table_builder(results, output)
                #print(output)
                return "```\n" + output + "\n```"
            else:
                print("No Results")
    except:
        print("Database is down!")
        return -2

def delete_notif(options):
    try:
        mongo = MongoDBConnection()
        output = ""
        with mongo:
            if mongo.connection.TMDB.notifications.find(options).count() > 0:
                for results in mongo.connection.TMDB.notifications.find(options, constants.proj_omissions):
                    output = functions.table_builder(results, output)
            mongo.connection.TMDB.notifications.delete_many(options)
            return "Deleted Records:\n```\n" + output + "\n```"
    except:
        print("Database is down!")
        return -2

def check_notif():
    try:
        #Returns a list of results
        mongo = MongoDBConnection()
        output = []
        with mongo:
            if mongo.connection.TMDB.notifications.find({}).count() > 0:
                for results in mongo.connection.TMDB.notifications.find({}):
                    #key = str(results.get('_id'))
                    output.append(results)
                    #output.update(results)
                print(str(len(output)) + " notifications exist.")
                return output
            else:
                print("No Results")
                return -1
    except:
        print("Database is down!")

def update_by_id(id, updates):
    # try:
        #Returns a list of results
        mongo = MongoDBConnection()
        with mongo:
            mongo.connection.TMDB.notifications.update_one({"_id": ObjectId(id)}, {"$set":updates})
            return 1
    # except:
    #     print("Database is down!")
    #     return -2

    
