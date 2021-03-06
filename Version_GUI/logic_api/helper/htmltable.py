""" Handles writing to html """

import decimal


def table_to_html_table(table):
    def drange(x, y, jump):
        x = decimal.Decimal(str(x))
        while x < y:
            yield float(x)
            x += decimal.Decimal(str(jump))

    # get range of times
    min_time, max_time = 24, 0
    for day in table:
        for start, end, *_ in day:
            if min_time > start:
                min_time = start
            if max_time < end:
                max_time = end

    # Initialize table
    html_table = HTMLTable()
    html_table.classes.append("table")
    html_table.append_row(
        ["Time", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
        headers=list(range(6)),
    )
    html_table[-1].classes.append("table-header")
    for i in drange(min_time, max_time + 1, 0.5):
        html_table.append_row([format_hour(i), "", "", "", "", ""], headers=[0])

        if int((i - min_time) * 2) % 2 == 1:
            # according to html viewing in browser
            html_table[-1].classes.append("even-row")

    # put classes in table, merges cells to show time
    for col, day in enumerate(table):
        col += 1  # account for time column

        for start, end, course, section in day:

            start = int((start - min_time) * 2) + 1
            end = int((end - min_time) * 2) + 1

            html_table[start][col] = f"{course} {section}"
            html_table[start][col].classes.append("course-entry")
            html_table.merge(col, start, end-1)

    return html_table


def format_hour(d):
    """
    Takes float:
        1, 12.5, 13
    and returns it formatted into am/pm time:
        1 am, 12:30 pm, 1 pm
    """
    am_pm = "am" if d < 12 else "pm"
    minutes = "00" if d.is_integer() else "30"
    hour = int(d - 12 if d > 12.5 else d)

    return f"{hour}:{minutes} {am_pm}"


class HTMLTable:
    def __init__(self, rows=[]):
        self.rows = []
        self.classes = []
        for row in rows:
            self.append_row(row)

    def __setitem__(self, i, v):
        self.rows[i] = v if type(v) == tr else tr(v)

    def __getitem__(self, i):
        return self.rows[i]

    def __str__(self):
        trs = "    " + "    ".join(str(r) for r in self.rows)
        classes = " ".join(self.classes)
        return f'<table class="{classes}">\n{trs}</table>'

    def merge(self, axis_val, start, end, axis="rows"):
        if axis == "rows":
            self[start][axis_val].attributes["rowspan"] = str(end - start + 1)
            for i in range(start + 1, end + 1):
                self[i][axis_val] = None
        elif axis == "cols":
            self[axis_val].merge_cols(start, end)
        else:
            raise ValueError("Invalid axis, it can only be rows or cols")

    def append_row(self, row=None, headers=[]):
        self.rows.append(tr())
        if row:
            for i, data in enumerate(row):
                if i in headers:
                    self[-1].add_th(data)
                else:
                    self[-1].add_td(data)


class tr:
    def __init__(self, data=[]):
        self.data = []
        self.classes = []
        for d in data:
            self.add_td(d)

    def __setitem__(self, i, v):
        if type(v) == str:
            self.data[i].content = v
        else:
            self.data[i] = v

    def __getitem__(self, i):
        return self.data[i]

    def __str__(self):
        classes = " ".join(self.classes)
        tds = "    " * 2 + "        ".join(str(t) for t in self.data if t)
        return f"""<tr class="{classes}">\n{tds}    </tr>\n"""

    def merge_cols(self, start, end):
        self[start].attributes["colspan"] = str(end - start + 1)
        for i in range(start + 1, end + 1):
            self[i] = None

    def add_td(self, data=""):
        self.data.append(td(data))

    def add_th(self, data=""):
        self.data.append(th(data))


class td:
    def __init__(self, content=""):
        self.content = content
        self.attributes = {}
        self.classes = []

    def __repr__(self):
        return f"td({self.content})"

    def __str__(self):
        if self.content is None:
            return ""

        classes = " ".join(self.classes)
        attributes = " ".join(f'{k}="{v}"' for k, v in self.attributes.items())
        return f'<td class="{classes}" {attributes}>{self.content}</td>\n'


class th(td):
    def __str__(self):
        return super().__str__().replace("<td", "<th").replace("</td>", "</th>")
