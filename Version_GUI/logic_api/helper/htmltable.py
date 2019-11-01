''' Handles writing to html '''

def to_html(table):
    #TODO
    pass

class HTMLTable:
    def __init__(self, rows=[]):
        self.rows = []
        for row in rows:
            self.append_row(row)

    def __setitem__(self, i, v):
        self.rows[i] = v

    def __getitem__(self, i):
        return self.rows[i]

    def __str__(self):
        trs = '    '+'    '.join(str(r) for r in self.rows)
        return f'<table>\n{trs}</table>'

    def merge(self, axis_val, start, end, axis='rows'):
        if axis == 'rows':
            self[start][axis_val].attributes['rowspan'] = str(end-start+1)
            for i in range(start+1, end+1):
                self[i][axis_val] = ''
        elif axis == 'cols':
            self[axis_val].merge_cols(start, end)
        else:
            raise ValueError('Invalid axis, it can only be rows or cols')

    def append_row(self, row=None):
        self.rows.append(tr())
        if row:
            for data in row:
                self[-1].add_td(data)

class tr:
    def __init__(self, data=[]):
        self.data = []
        self.classes = []
        for d in data:
            self.add_td(d)

    def __setitem__(self, i, v):
        self.data[i] = v

    def __getitem__(self, i):
        return self.data[i]

    def __str__(self):
        classes = ' '.join(self.classes)
        tds = '    '*2+'        '.join(str(t) for t in self.data if t)
        return f'''<tr class="{classes}">\n{tds}    </tr>\n'''

    def merge_cols(self, start, end):
        self[start].attributes['colspan'] = str(end-start+1)
        for i in range(start+1, end+1):
            self[i] = ''

    def add_td(self, data=''):
        self.data.append(td(data))

class td:
    def __init__(self, content=''):
        self.content = content
        self.attributes = {}
        self.classes = []

    def __str__(self):
        classes = ' '.join(self.classes)
        attributes = ' '.join(f'{k}="{v}"' for k,v in self.attributes.items())
        return f'<td class="{classes}" {attributes}>{self.content}</td>\n'