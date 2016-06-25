from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
import test
import re


class webServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Hello!</h1>"
                output += '''<form method='POST' enctype='multipart/form-data'
                action='/hello'><h2>What would you like me to say?
                </h2><input name="message" type="text" >
                <input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>&#161 Hola !</h1>"
                output += '''<form method='POST' enctype='multipart/form-data'
                action='/hello'><h2>What would you like me to say?
                </h2><input name="message" type="text" >
                <input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                result = test.result_query()
                output = ""
                output += "<html><body>"
                output += "<h1>Success</h1>"
                output += "<ul style='list-style-type:none; padding: 0'>"
                for i in result:
                    output += "<li style='margin-bottom: 20px'>%s<br/>"\
                        "<a href='%s/edit'>Edit</a><br/>"\
                        "<a href='%s/delete'>Delete</a></li>" \
                        % (i.name, i.id, i.id)
                output += "</ul>"
                output += "</body></html>"
                self.wfile.write(output)
                print output
                print result
                return

            if self.path.endswith("/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Add a Restaurant</h1>"
                output += '''<form method='POST' enctype='multipart/form-data'
                action='/hello'><h2>Restaurant Name
                </h2><input name="restaurant" type="text" >
                <input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                print output
                self.wfile.write(output)
                return

            if self.path.endswith("/edit"):
                self.send_response(200)
                self.send_header('Content-type', 'text-html')
                self.end_headers()
                id = re.findall(r'\d+', self.path)
                a_restaurant = test.search_by_id(id[0])
                output = ""
                output += "<html><body>"
                output += "<h1>Edit a Restaurant Name</h1>"
                output += ''' <form method='POST'enctype='multipart/form-data' '''
                output += '''action = "/%s/edit">''' \
                    % id[0]
                output += ''' <h3> Current Restaurant Name: %s
                </h3 > <input name = "restaurant_update" type = "text" value = "%s" > ''' \
                % (a_restaurant.name, a_restaurant.name)
                output += ''' <input type="hidden" name="id" value="%s"> ''' % id[
                    0]
                output += ''' <input type = "submit" value = "Submit" > </form>'''
                output += ''' <a href="/restaurants">Back</a>'''
                output += "</body></html>"
                print output
                self.wfile.write(output)
                print id
                return

            if self.path.endswith("/delete"):
                self.send_response(200)
                self.send_header('Content-type', 'text-html')
                self.end_headers()
                id = re.findall(r'\d+', self.path)
                if(id):
                    id = id[0]
                    a_restaurant = test.search_by_id(id)
                output = "<html><body>"
                if id and a_restaurant:
                    output += "<h1>Are you sure you want to delete<h1>"
                    output += ''' <form method='POST'enctype='multipart/form-data' '''
                    output += ''' action = "/%s/delete">'''\
                        % id
                    output += '''<input type="hidden" name="delete_id" value=%s> '''\
                        % id
                    output += ''' <input type="submit" value="Submit"> '''
                    output += "</form>"
                else:
                    output += "There was no id in the url"
                output += "</body></html>"
                self.wfile.write(output)
                print output
        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:
            self.send_response(301)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            ctype, pdict = cgi.parse_header(
                self.headers.getheader('content-type'))
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('message')
                new_restaurant_name = fields.get('restaurant')
                restaurant_update = fields.get('restaurant_update')
                restaurant_update_id = fields.get('id')
                delete_id = fields.get('delete_id')
                output = "Failure"

                if(messagecontent):
                    output = ""
                    output += "<html><body>"
                    output += " <h2> Okay, how about this: </h2>"
                    output += "<h1> %s </h1>" % messagecontent[0]
                    output += ''' < form method = 'POST' enctype = 'multipart/form-data'
                    action = '/hello' > <h2 > What would you like me to say?
                    </h2 > <input name = "message" type = "text" >
                    <input type = "submit" value = "Submit" > < / form > '''
                    output += "</body></html>"
                elif(new_restaurant_name):
                    result = test.search_for_existing(new_restaurant_name[0])
                    output = ""
                    output += "<html><body>"
                    output += "<h2>Successful post</h2>"
                    if result:
                        output += "<h3>%s already is in the database</h3>" \
                            % result[0]
                    else:
                        test.insert_new(new_restaurant_name[0])
                        output += "<h3>%s has been added</h3>"\
                            % new_restaurant_name[0]
                        output += "<h3><a href='/restaurants'>Back</a></h3>"
                    output += "</body></html>"
                elif(restaurant_update and restaurant_update_id):
                    output = ""
                    output += "<html><body>"
                    output += "<h1>Edit a Restaurant Name</h1>"
                    output += ''' <form method = 'POST' enctype = 'multipart/form-data'
                    action = '/%s/edit'> <h3> Current Restaurant Name: %s
                    </h3> <input name = "restaurant_update" type = "text" value = "%s"> ''' \
                    % (restaurant_update_id[0], restaurant_update[0], restaurant_update[0])
                    output += ''' <input type="hidden" name="id" value="%s"> ''' % restaurant_update_id[
                        0]
                    output += ''' <input type = "submit" value = "Submit"> </form>'''
                    output += ''' <a href="/restaurants"> Back </a> '''
                    output += "</body></html>"
                    test.update_name(restaurant_update_id[
                                     0], restaurant_update[0])

                elif(delete_id):
                    if(test.delete_entry(delete_id[0])):
                        output = ""
                        output += "<html><body>"
                        output += "<h1>Deleted Entry</h1>"
                        output += '''<a href="/restaurants">Back</a>'''
                        output += "</body></html>"
                self.wfile.write(output)
                print output
        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webServerHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print "Stopping web server...."
        server.socket.close()

if __name__ == '__main__':
    main()
