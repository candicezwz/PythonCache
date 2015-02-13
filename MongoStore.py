#! /usr/bin/env python
#
# \brief     MongoDB store implementation
# \author    Hans Kramer
# \version   0.1
# \date      Feb 2015
#


import pymongo
from   bson.objectid import ObjectId
from   syslog        import openlog, syslog, LOG_INFO, LOG_PERROR, LOG_USER
from   Cache         import CacheImpl



class MongoStore(CacheImpl):
   
    """
        Example implementation of how to implement a connection to a back-end store
        for the Cache Library
    """

    def __init__(self, host = '127.0.0.1', port = 27017):
        """
            Contructor 

            @param[in] host  The host were your MongoDB database server is running
            @param[in] port  The port the MOngoDB server is using
        """
        CacheImpl.__init__(self)
        self._mc = pymongo.Connection(host, port)
        self._db = self._mc.test
        self._c  = self._db.test
    
    def read(self, key):
        """
            Read data identified by key from MongoDB

            @param[in] key   The key identifying the data
            @returns         The data associated by key
        """
        syslog(LOG_INFO, "MongoStore.read %s" % key)
        return [x for x in self._c.find({'_id': ObjectId(key)}, {'_id': 0})]

    def write(self, key, value):
        """
            Write data specified by value and identified by key to MongoDB

            @param[in] key    The key identifying the data
            @param[in] value  The data itself
        """
        syslog(LOG_INFO, "MongoStore.write %s %s" % (key, value))
        return self._c.update({'_id': ObjectId(key)}, {'_id': ObjectId(key), 'name': value}, True)


if __name__ == "__main__":
     import sys
     
     if len(sys.argv) != 2:
         print "specify what to do!"
         sys.exit()

     ms = MongoStore()
     if sys.argv[1] == "clear":
         ms._c.remove()
     elif sys.argv[1] == "write":
         ms.write("54dc80c37b020a219e000000", "Jean Doe")     
         ms.write("54dc80c37b020a219e000001", "John Doe")
         ms.write("54dc798d77f68a6361532d05", "Hans Kramer")
     elif sys.argv[1] == "read":
         print ms.read("54dc80c37b020a219e000000")
         print ms.read("54dc80c37b020a219e000001")
         print ms.read("54dc798d77f68a6361532d05")
     else:
         print "Unknow task"
