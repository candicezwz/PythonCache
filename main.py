#! /usr/bin/env python
#
# \brief     Demo code for Cache class with MongoDB
# \author    Hans Kramer
# \version   0.1
# \date      Feb 2015
#


from   syslog        import openlog, syslog, LOG_INFO, LOG_PERROR, LOG_USER
from   Cache         import CacheImpl, CachePipe, CacheImplWriteBackMemory, md_cache
from   MongoStore    import MongoStore


def factory_mongo_cache(host = "localhost", port = 27017, cache_size = 3):
    # perhaps do a singleton thingy here... feature creep 
    mdc_front  = CachePipe()
    mdc_middle = CachePipe()
    mdc_end    = CachePipe()
    mdc_front.attach(CacheImpl)
    mdc_middle.attach(CacheImplWriteBackMemory, cache_size=cache_size)
    mdc_end.attach(MongoStore, host=host, port=port, db="test", collection="test")
    mdc_front.connect(mdc_middle)
    mdc_middle.connect(mdc_end)
    return mdc_front
    

if __name__ == "__main__":
    openlog("MD", LOG_PERROR, LOG_USER)

    mdc = factory_mongo_cache()

    print mdc.read("54dc80c37b020a219e000001")
    print mdc.read("54dc80c37b020a219e000001")
    mdc.flush()

    mdc = md_cache(MongoStore, cache_size = 3, collection = "test2")
    mdc.write("54dc80c37b020a219e000001", "John Doe 1")
    mdc.write("54dc80c37b020a219e000002", "John Doe 2")
    mdc.flush()
    mdc.write("54dc80c37b020a219e000003", "John Doe 3")
    mdc.write("54dc80c37b020a219e000004", "John Doe 4")

    print mdc.read("54dc80c37b020a219e000001")
    print mdc.read("54dc80c37b020a219e000001")
    print mdc.read("54dc80c37b020a219e000003")
    print mdc.read("54dc80c37b020a219e000007")
    print mdc.read("54dc80c37b020a219e000003")
    print mdc.read("54dc80c37b020a219e000008")
    print mdc.read("54dc80c37b020a219e000009")

