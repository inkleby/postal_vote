import os
import sys
import SimpleHTTPServer
import BaseHTTPServer
import posixpath
import urllib


class MyHTTPRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    
    serve_location = ""
    
    
    def translate_path(self, path):
        """Translate a /-separated PATH to the local filename syntax.
        Components that mean special things to the local file system
        (e.g. drive or directory names) are ignored.  (XXX They should
        probably be diagnosed.)
        """
        # abandon query parameters
        path = path.split('?',1)[0]
        path = path.split('#',1)[0]
        path = posixpath.normpath(urllib.unquote(path))
        words = path.split('/')
        words = filter(None, words)
        path = self.__class__.serve_location
        for word in words:
            drive, word = os.path.splitdrive(word)
            head, word = os.path.split(word)
            if word in (os.curdir, os.pardir): continue
            path = os.path.join(path, word)
            
            
        if path[-1] <> "\\":
            file = os.path.basename(path)
            if "." not in file:
                path += ".html"
        return path
    

def serve():
    
    MyHTTPRequestHandler.serve_location = "E:\\lintic\\"
    
    BaseHTTPServer.test(MyHTTPRequestHandler, BaseHTTPServer.HTTPServer)


if __name__ == '__main__':
    serve()