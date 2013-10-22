class PostsController:

    def index(parameters):
        return '''<html><head><title>Testing Title</title></head>
        <body><h2>Posts</h2><p>I'm in the posts controller!</p></body>
        </html>'''

    def show(parameters):
        return '''<html><head><title>Testing Title</title></head>
        <body><h2>Posts</h2><p>You've requested post #{0}</p></body>
        </html>'''.format(parameters["id"])
