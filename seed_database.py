import os                                   # Det här är för att ta bort hundar.db innan filen skapas igen
from app import app, db, hund_klass
import json

def seed_database():                        #Denna skapar en funktion som används för att seeda hundar.db i app.py
    with app.app_context():
        if os.path.exists("hundar.db"):     #Detta tar bort hundar.db utifall det finns en seedad databas sen innan.
            os.remove("hundar.db")          #Så man slipper skapa nytt projekt varje gång man kör seed_database
            db.create_all()                 #Fyller databasen hundar.db från hund.json filen.

            with open("hund.json", "r") as f:   #Öppnar filen hund.json och läser in datan. r står för read och det
                                                #innebär att man läser endast filen hund.json. f är fil objekt
                                                #som används inom with blocket och sen används inte mer när det stängs.
                data = json.load(f)

                for hund_data in data:          #loop genom hund.json filens dictionary och skapar ett nytt objekt
                                                #av hund_klass för varje hund

                    hund = hund_klass(id=hund_data["id"], namn=hund_data["namn"], ras=hund_data["ras"], kon=hund_data["kon"])

                    db.session.add(hund)        #Objektet läggs till db.session som är en temp plats för att lagra
                                                #ändringar i databasen.
                    db.session.commit()         #Detta sparar allt


if __name__ == "__main__":                      #Detta kollar om filen är den filen som körs eller om den är anropad av
                                                #app.py filen eller någon annan fil om jag hade någon. Om den är main
                                                #filen så körs seed_database.
    seed_database()                             #Detta seedar databasen med informationen från hund.json