from channels import route
from posts.consumers import connect_blog, disconnect_blog

# The channels routing defines what the channels get handled by what consumers,
# including optional matching on message attributes. Websocket messages of all
# types have a 'path' attribute, so we're using that to route the socket.
# While this is under stream/ compared to the HTML page, we could have it on the
# same URL if we wanted; Daphne separates by protocol as it negotiates with a browser

channel_routing = [
    # called when incoming Websockets connect
    route('websocket.connect', connect_blog, path=r'/liveblog/(?P<slug>[^/]+)/stream/$'),

    # called when the client closes the socket
    route('websocket.disconnet', disconnect_blog, path=r'^/liveblog/(?P<slug>[^/]+/stream/$'),

]