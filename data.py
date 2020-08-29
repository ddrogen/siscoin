import os
import gspread


class GoogleSpread:
    def __init__(self, sheet, worksheet=None):

        siscoin_service_account = os.getenv("SISCOIN_SERVICE_ACCOUNT")
        with open("siscoin-service-account.json", "w") as f:
            f.write(siscoin_service_account)
        self.client = gspread.service_account(filename='siscoin-service-account.json')
        self.sheet = self.client.open(sheet)
        if worksheet:
            self.worksheet = self.sheet.worksheet(worksheet)

    def append(self, row):
        self.worksheet.append_row(row,insert_data_option="INSERT_ROWS", table_range="A1")

    def get_option_list(self):
        result = self.sheet.values_get(range="Lista Insumos!A:A")

        options = [ option[0] for option in result['values'] ]
        return options

    def process_form_header(self, form_header):

        offset = int(form_header.pop(0))
        form = [form_header.pop(0)]
        empty = ["" for i in range(offset)]

        return form + empty + form_header

    def process_form_table(self, form_table):

        rows = []
        for tr in form_table.split("</tr>"):
            row = [ r.replace("</td>","").replace(" ", "") for r in tr.split("<td>") if "</td>" in r and 'button' not in r]
            if row:
                # convert numeric values to numbers whenever possible
                converted = []
                for r in row:
                    try:
                        number = float(r)
                    except:
                        number = r
                    converted.append(number)

                rows.append(converted)
        return rows
