from utils.dbconfig import dbconfig
from rich import print as printc
from rich.table import Table


def checkEntryExistence(cursor, sitename, username):
    # Check if an entry with the specified sitename and username exists
    query = "SELECT * FROM pm.entries WHERE sitename = %s AND username = %s"
    cursor.execute(query, (sitename, username))
    result = cursor.fetchone()
    return result is not None


def removeEntry(mp, ds, sitename, username):
    db = dbconfig()
    cursor = db.cursor()

    # Check if the entry exists
    if not checkEntryExistence(cursor, sitename, username):
        printc("[red][!][/red] Entry does not exist.")

        # Show full table
        showFullTable(cursor)

        db.close()
        return

    # Construct the query to delete the entry
    query = "DELETE FROM pm.entries WHERE sitename = %s AND username = %s"

    # Execute the delete query
    cursor.execute(query, (sitename, username))
    db.commit()

    printc("[green][+][/green] Entry removed successfully.")

    # Show full table
    showFullTable(cursor)

    db.close()


def showFullTable(cursor):
    # Fetch all entries from the table
    cursor.execute("SELECT * FROM pm.entries")
    results = cursor.fetchall()

    # Display the entries in a table
    table = Table(title="All Entries")
    table.add_column("Sitename")
    table.add_column("URL")
    table.add_column("Email")
    table.add_column("Username")

    for entry in results:
        table.add_row(entry[0], entry[1], entry[2], entry[3])

    printc(table)
