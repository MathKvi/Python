from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)       #Detta är en instans (blueprint) av Flask klassen som är min web applikation

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///hundar.db" #Det här är vilken typ av databas och vart den finns
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False          #Stänger av en funktion som kan ge ett error vid kompilering


db = SQLAlchemy(app)        #Instans(blueprint) av SQLAlchemy för databasen.


class hund_klass(db.Model):                         #Detta skapar klassen hund_klass
    id =db.Column(db.Integer, primary_key=True)     #Dessa är i referens till json dokumented och respresenterar
    namn = db.Column(db.String)                     #tabellen med hundar.
    ras = db.Column(db.String)
    kon = db.Column(db.String)



    def to_dict(self):          #Flask metod som omvandlar ett objekt av klassen
                                #hund_klass. self är ett specialord som används som första
                                #parameter i en metod. Man kan använda det för att anropa
                                #och omvandla ett object till dictionary. Istället för
                                #hund_klass.to_dict så kan man använda hund.to_dict.


        return {"id": self.id, "namn": self.namn, "ras": self.ras, "kon": self.kon}




@app.route("/hundar", methods=["GET"])  #Adressen/URL och GET metoden för att anropa
def get_hundar():                       #funktionen get_hundar.
    hundar = hund_klass.query.all()     #Hämtar alla objekt från hund_klass
    return jsonify([hund.to_dict() for hund in hundar]) #Detta ger en json represenation
                                                        #av alla objekt. Den sparas i minnet


@app.route("/hundar/<int:hund_var_id>", methods=["GET"])    #Adress/URL och GET metoden igen.
                                                            #<int:hund_var_id>" är en parameter för att hitta en
                                                            #specifik hund.
def get_hund(hund_var_id):                                  #specifik hund genom sitt id som lagras i hund_var.
    hund_var = hund_klass.query.get(hund_var_id)            #query.get hämtar en specifik hund.
    return jsonify (hund_var.to_dict())                     #Samma som tidigare. Retunerar json-objekt som sparas i minne.

@app.route("/hundar", methods=["POST"])                     #Adress/URL och metoden POST.
def post_hund():
    data = request.get_json()                               #Detta hämtar info som kommer från websidan till servern
                                                            #och ändrar om det till ett python objekt. Den läggs i data.
    ny_hund = hund_klass(**data)                            #ny_hund skapas genom **data som är en syntax som skickar
                                                            #alla kolumner ifrån json filen istället för att räkna upp
                                                            #dem 1 och 1. **data packar upp data'n som omvandlas till en
                                                            #dictionary.
    db.session.add(ny_hund)                                 #Lägger till nytt objekt till databasen.
    db.session.commit()                                     #sparar
    return jsonify (ny_hund.to_dict())


@app.route("/hundar/<int:hund_var_id>", methods=["PUT"])    #Adress/URL och metoden PUT. <int:hund_var_id>"= specifik hund
def update_hund(hund_var_id):
    hund_var = hund_klass.query.get(hund_var_id)            #Samma som tidigare. Söker en specifik hund så ..._id
                                                            #som sparas i hund_var
    data = request.get_json()                               #hämtar info från websidan till servern.
    hund_var.namn = data["namn"]                            #uppdaterar information i hund_var variablen.
    hund_var.ras = data["ras"]
    db.session.commit()                                     #sparar
    return jsonify(hund_var.to_dict())


@app.route("/hundar/<int:hund_var_id>", methods=["DELETE"]) #Adress/URL och DELETE metoden.
def delete_hund_var(hund_var_id):
    hund_var = hund_klass.query.get(hund_var_id)            #Specifik hund
    db.session.delete(hund_var)                             #ta bort hunden
    db.session.commit()                                     #sparar
    return jsonify({})                                      #detta ger tillbaka ett tomt json objekt.

if __name__ == "__main__":                                  #Samma som på seed_database. Kollar om det är den som körs.
        app.run(debug=True)                                 #startar flask servern i debug läge.