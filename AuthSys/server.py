import os
import json
import tornado.ioloop
import tornado.websocket
import tornado.options
import webbrowser

from tornado.options import define, options
define("port", default=8080, help="run on the given port", type=int);

import argparse


import SocketServer

import init_model
import makeAuth
import data_process

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        print "Handle GET request";
        self.write("Hello, world");

class WebSocket(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True;

    def open(self, *args, **kwargs):
        print options.port;
        print "WebSocket opened";

    def on_message(self, message):
        print "Handle websocket request"
        print "Received message: ", message;

        self.write_message(u"You said" + message);

    def on_close(self):
        print "WebSocket closed"


if __name__ == "__main__":
    tornado.options.parse_command_line();
    handlers = [(r"/", MainHandler), (r"/websocket", WebSocket)];
    server = tornado.web.Application(handlers);
    server.listen(options.port,address="localhost");

    webbrowser.open("http://localhost:%d/" % options.port, new=2)

    tornado.ioloop.IOLoop.current().start();

