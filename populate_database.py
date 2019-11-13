from database import Item
from sys import stderr
from app import db
from os import path
import xlrd

def populate_database():
    DATABASE_FILE = "ustore_inventory.xlsx"

    if not (path.isfile(DATABASE_FILE)):
        raise Exception("UStore inventory spreadsheet not found")

    loc = (DATABASE_FILE)
    wb = xlrd.open_workbook(loc)
    sheet = wb.sheet_by_index(0)
    try:
        for i in range(sheet.nrows):
            #print(sheet.cell_value(i, 0))

            item_to_add = Item(
                name=sheet.cell_value(i, 0),
                price=sheet.cell_value(i, 1),
                category=sheet.cell_value(i, 2),
                )

            db.session.add(item_to_add)
    except Exception as e:
        print("Error: %s" % str(e), file=stderr)
        db.session.rollback
        raise Exception(e)
    
    db.session.commit()
    print("Added items to database")

if __name__ == "__main__":
    populate_database()