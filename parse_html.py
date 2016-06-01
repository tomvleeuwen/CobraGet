#!/usr/bin/env python2
# TODO: Integrate with CURL
# TODO: Parse remove_ags, set_tags and submit from command_line
import sys
import urllib
from HTMLParser import HTMLParser

# create a subclass and override the handler methods
class MyHTMLParser(HTMLParser):
    def __init__(self, remove_tags, set_tags, submit, ):
        self.tags = {}
        self.remove_tags = remove_tags
        self.set_tags = set_tags
        self.submit = submit
        HTMLParser.__init__(self)

    def handle_starttag(self, tag, attrs):
        thistype = None
        if tag == "input":
            require_checked = False
            found_checked = False
            is_submit = False
            data = ""
            name = None
            for attr, value in attrs:
                if attr == "type":
                    if value == "checkbox" or value == "radio":
                        require_checked = True
                    if value == "submit":
                        is_submit = True
                if attr == "checked":
                    found_checked = True
                if attr == "value":
                    data = value
                if attr == "name":
                    name = value
            if is_submit and name != self.submit:
                return
            if require_checked == False or found_checked == True:
                self.tags[name] = data
    def handle_endtag(self, tag):
        pass
    def handle_data(self, data):
        pass
    def get_post_data(self):
        post_tags = self.tags
        for remove_tag in self.remove_tags:
            self.tags.pop(remove_tag, None)
        self.tags.update(self.set_tags)
        return urllib.urlencode(self.tags)

def main():
    # instantiate the parser and fed it some HTML
    parser = MyHTMLParser(remove_tags=[], set_tags={'UserName': 'techno.leut@technolution.nl', 'Password' : 'geheim'}, submit="Inloggen")
    fd = open(sys.argv[1], 'r')
    
    parser.feed(fd.read())
    print parser.get_post_data()

if __name__ == "__main__":
    main()
