from html.parser import HTMLParser

class AgdaHTMLParser(HTMLParser):
    def __init__(self):
        super(AgdaHTMLParser, self).__init__()
        self.body = False
        self.tags = []
        self.row = []
        self.rows = []
        
    def handle_starttag(self, tag, attrs):
        if tag == 'pre':
            self.body = True

        if self.body:
            self.tags.append( (tag, attrs) )
        #print("Encountered a start tag:", tag)

    def handle_endtag(self, tag):
        if len(self.tags) > 0:
            self.tags.pop()
        #print("Encountered an end tag :", tag)

    def handle_data(self, data):
        if self.body:
            classes = []
            for attr in self.tags[-1][1]:
                if attr[0] == 'class':
                   classes.append( attr[1] )
            kinds = []
            if classes[0] != 'Agda':
                kinds = classes[0].split(' ') 
                
            if "\n" in data:
                for t in data.split('\n')[:-1]:
                    self.row.append( (kinds, t) )
                    self.rows.append( self.row )
                    self.row = []
            else:
                self.row.append( (kinds, data) )
                    

# infile = 'board1645894512114.html'
# f = open(infile, "r")

# def clean(x):
#     if x.startswith(' '):
#         return '<a></a>' + x
#     return x

# html = [clean(x.rstrip("\n")) for x in f.readlines()]
# html = "\n".join(html)
# f.close()

# parser = AgdaHTMLParser()
# parser.feed(html)
# print(parser.rows[-5])

def parse(html):
    parser = AgdaHTMLParser()
    parser.feed(html)
    return parser.rows
