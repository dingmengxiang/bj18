from tornado.web import RequestHandler
import tornado.ioloop

class test(RequestHandler):
    def get(self):

if __name__ == "__main__":

    app = tornado.web.Application([
        (r"/test",test),



    ])
    app.listen(8610)
    tornado.ioloop.IOLoop.current().start()