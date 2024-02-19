import os
import sys
import string
import random
import hashlib
import sys
from getpass import getpass

from utils.dbconfig import dbconfig

from rich import print as printc
from rich.console import Console

console = Console()


def generateDeviceSecret(length=10):
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=length))


def checkConfig():
    db = dbconfig()
    cursor = db.cursor()
    query = (
        "SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA  WHERE SCHEMA_NAME = 'pm'"
    )
    cursor.execute(query)
    results = cursor.fetchall()
    db.close()
    if len(results) != 0:
        return True
    return False


def make():
    if checkConfig():
        printc("[red][!] Already Configured! [/red]")
        return

    printc("[green][+] Creating new config... [/green]\n")

    # Create database
    db = dbconfig()
    cursor = db.cursor()
    try:
        cursor.execute("CREATE DATABASE pm")
    except Exception as e:
        printc(
            "[red][!] An error occurred while trying to create db. Check if database with name 'pm' already exists - if it does, delete it and try again."
        )
        console.print_exception(show_locals=True)
        sys.exit(0)

    printc("[green][+][/green] Database 'pm' created :)\n")

    # Create tables
    query = "CREATE TABLE pm.secrets (masterkey_hash TEXT NOT NULL, device_secret TEXT NOT NULL)"
    res = cursor.execute(query)
    printc("[green][+][/green] Table 'secrets' created ")

    query = "CREATE TABLE pm.entries (sitename TEXT NOT NULL, siteurl TEXT NOT NULL, email TEXT, username TEXT, password TEXT NOT NULL)"
    res = cursor.execute(query)
    printc("[green][+][/green] Table 'entries' created ")

    mp = ""
    printc(
        "[+] A strong [green]MASTER PASSWORD[/green] is crucial as it unlocks all your passwords. Choose one with upper and lower case letters, numbers, and special characters. Remember, [green]it's not stored anywhere[/green] and [red]cannot be changed once set[/red].\n"
    )

    while 1:
        mp = getpass("Choose a MASTER PASSWORD: ")
        if mp == getpass("Re-type: ") and mp != "":
            break
        printc("[yellow][-] Please try again.[/yellow]")

    # Hash the MASTER PASSWORD
    hashed_mp = hashlib.sha256(mp.encode()).hexdigest()
    printc("[green][+][/green] Generated hash of MASTER PASSWORD")

    # Generate a device secret
    ds = generateDeviceSecret()
    printc("[green][+][/green] Device Secret generated")

    # Add them to db
    query = "INSERT INTO pm.secrets (masterkey_hash, device_secret) values (%s, %s)"
    val = (hashed_mp, ds)
    cursor.execute(query, val)
    db.commit()

    printc("[green][+][/green] Added to the database")

    printc("[green][+] Configuration done![/green]")

    db.close()


make()
