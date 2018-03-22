#coding:utf-8
import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options
import os.path
import json
import urllib2

from tornado.options import define, options

define("port", default=8000, help="run on the given port", type=int)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render(
            "index.html",
            page_title = "Burt's Books ¦ Home",
            header_text = "Welcome to Burt's Books!",
            books = ['细说php','python','PHP','小时代']
        )


class HelloModule(tornado.web.UIModule):
    def render(self):
        return'<h1>I am yyx and this is an information from module hello!</h1>'

class BookModule(tornado.web.UIModule):
    def render(self,bookname):
        doubanapi = r'https://api.douban.com/v2/book/'
        searchapi = r'https://api.douban.com/v2/book/search?q='
        searchurl = searchapi+bookname
        searchresult = urllib2.urlopen(searchurl).read()
        bookid = json.loads(searchresult)['books'][0]['id']
        bookurl = doubanapi+bookid
        injson = urllib2.urlopen(bookurl).read()
        bookinfo = json.loads(injson)
        return self.render_string('modules/book.html',book = bookinfo)

    def embedded_javascript(self):
        return "document.write(\"hi!\")"

    def embedded_css(self):
        return '''.book {background-color:#F5F5F5}
             .book_body{color:red}
        '''

    def html_body(self):
        return '<script>document.write("Hello!")</script>'

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers = [
          (r'/',MainHandler),
        ],
        template_path = os.path.join(os.path.dirname(__file__),'templates'),
        static_path = os.path.join(os.path.dirname(__file__),'static'),
        debug = True,
        ui_modules={'Hello':HelloModule,'Book':BookModule}
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()