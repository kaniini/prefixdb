# prefixdb - a database server for IPv4/IPv6 prefixes

prefixdb is a database server which stores non-persistent information about IPv4 and IPv6 prefixes.
It is intended to be a memcache-like service that is oriented towards storing JSON documents about
specific prefixes.

A plugin interface enables extending prefixdb with other features, such as using MQTT for clustering
and bulk data ingestion, datastore persistence and additional APIs.  For more information, see
[the plugin API documentation](doc/plugin.md).

Unlike redis or memcache, there is a simple HTTP-based API layer similar to Elasticsearch.  For more
information, see [the base API documentation](doc/api.md).

With a clustering plugin, it is possible to deploy prefixdb under an aiohttp.web process manager, such
as [gunicorn](http://github.com/benoitc/gunicorn).  Using [uvloop](http://github.com/magicstack/uvloop)
with gunicorn (`gunicorn -k aiohttp.worker.GUnicornUVLoopWorker`) enables very high performance prefixdb
database I/O that will very easily horizontally scale across an entire machine.
