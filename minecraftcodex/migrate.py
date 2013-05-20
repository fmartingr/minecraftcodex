from __future__ import absolute_import

from os import environ
environ['DJANGO_SETTINGS_MODULE'] = 'herobrine.settings'

from database.models import Version, Mod
import sqlite3

def main():
    # Connection
    conn = sqlite3.connect('old.sqlite')

    # Magic
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM database_version')

    mod = Mod.objects.get(pk=1)

    for item in cursor.fetchall():
        version_number = item[1]
        status = item[2]
        date = item[3]
        url = item[4]
        name = item[5]
        changelog = item[6]

        version = Version()
        version.mod = mod
        version.version_number = version_number
        version.status = status
        version.date = date
        version.url = url
        version.name = name
        version.changelog = changelog
        version.save()

if __name__=="__main__":
    main()
