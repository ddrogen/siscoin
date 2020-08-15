import gspread


class GoogleSpread:
    def __init__(self, sheet, worksheet):
        self.client = gspread.service_account(filename='siscoin-f6bf903a5c41.json')
        self.sheet = self.client.open(sheet).worksheet(worksheet)

    def append(self, row):
        self.sheet.append_row(row,insert_data_option="INSERT_ROWS", table_range="A1")


    def process_form_header(self, form_header):

        offset = int(form_header.pop(0))
        form = [form_header.pop(0)]
        empty = ["" for i in range(offset)]

        return form + empty + form_header

    def process_form_table(self, form_table):

        rows = []
        for tr in form_table.split("</tr>"):
            row = [ r.replace("</td>","") for r in tr.split("<td>") if "</td>" in r and 'button' not in r]
            if row:
                rows.append(row)
        return rows
