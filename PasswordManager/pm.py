import argparse
from getpass import getpass
import hashlib
import pyperclip

from rich import print as printc

import utils.add
import utils.retrieve
import utils.generate
import utils.remove
from utils.dbconfig import dbconfig

parser = argparse.ArgumentParser(description="Description")

parser.add_argument("option", help="(a)dd / (e)xtract / (g)enerate / (r)emove")
parser.add_argument("-s", "--name", help="Site name")
parser.add_argument("-u", "--url", help="Site URL")
parser.add_argument("-e", "--email", help="Email")
parser.add_argument("-l", "--login", help="Username")
parser.add_argument("--length", help="Length of the password to generate", type=int)
parser.add_argument(
    "-c", "--copy", action="store_true", help="Copy password to clipboard"
)
parser.add_argument(
    "-r", "--remove", action="store_true", help="Remove entry from the database"
)


args = parser.parse_args()


def inputAndValidateMasterPassword():
    mp = getpass("MASTER PASSWORD: ")
    hashed_mp = hashlib.sha256(mp.encode()).hexdigest()

    db = dbconfig()
    cursor = db.cursor()
    query = "SELECT * FROM pm.secrets"
    cursor.execute(query)
    result = cursor.fetchall()[0]
    if hashed_mp != result[0]:
        printc("[red][!] WRONG! [/red]")
        return None

    return [mp, result[1]]


def main():
    if args.option in ["add", "a"]:
        if args.name == None or args.url == None or args.login == None:
            if args.name == None:
                printc("[red][!][/red] Site Name (-s) required ")
            if args.url == None:
                printc("[red][!][/red] Site URL (-u) required ")
            if args.login == None:
                printc("[red][!][/red] Site Login (-l) required ")
            return

        if args.email == None:
            args.email = ""

        res = inputAndValidateMasterPassword()
        if res is not None:
            utils.add.addEntry(
                res[0], res[1], args.name, args.url, args.email, args.login
            )

    if args.option in ["extract", "e"]:
        # if args.name == None and args.url == None and args.email == None and args.login == None:
        # 	# retrieve all
        # 	printc("[red][!][/red] Please enter at least one search field (sitename/url/email/username)")
        # 	return
        res = inputAndValidateMasterPassword()

        search = {}
        if args.name is not None:
            search["sitename"] = args.name
        if args.url is not None:
            search["siteurl"] = args.url
        if args.email is not None:
            search["email"] = args.email
        if args.login is not None:
            search["username"] = args.login

        if res is not None:
            utils.retrieve.retrieveEntries(
                res[0], res[1], search, decryptPassword=args.copy
            )

    if args.option in ["generate", "g"]:
        if args.length == None:
            printc(
                "[red][+][/red] Specify length of the password to generate (--length)"
            )
            return
        password = utils.generate.generatePassword(args.length)
        pyperclip.copy(password)
        printc(
            "[green][+][/green] Password [green]generated and copied[/green] to clipboard :) "
        )

    if args.option in ["remove", "r"]:
        if args.name is None and args.login is None:
            printc("[red][!][/red] Site Name (-s) or Username (-l) required ")
            return

        res = inputAndValidateMasterPassword()
        if res is not None:
            utils.remove.removeEntry(res[0], res[1], args.name, args.login)


main()
