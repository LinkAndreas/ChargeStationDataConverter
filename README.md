# Charge Station Data Converter

This script normalizes and simplifies charge station data provided by Bundesnetzagentur.de under the CC-BY 4.0.

## Usage

You can run the script with the CSV file as input using the following command:

```console
python3 main.py input.csv
```

The output will be genrated in the same directory:

### Example:
Sample input CSV file:
```csv
Ladesäulenregister Bundesnetzagentur;;;;;;;;;;;;;;;;;;;;;;;;;
;;;;;;;;;;;;;;;;;;;;;;;;;
Stand: 01.12.2021;;;;;;;;;;;;;;;;;;;;;;;;;
;;;;;;;;;;;;;;;;;;;;;;;;;
Allgemeine Informationen;;;;;;;;;;;;;;1. Ladepunkt;;;2. Ladepunkt;;;3. Ladepunkt;;;4. Ladepunkt;;
Betreiber;Straße;Hausnummer;Adresszusatz;Postleitzahl;Ort;Bundesland;Kreis/kreisfreie Stadt;Breitengrad;Längengrad;Inbetriebnahmedatum;Anschlussleistung;Art der Ladeeinrichung;Anzahl Ladepunkte;Steckertypen1;P1 [kW];Public Key1;Steckertypen2;P2 [kW];Public Key2;Steckertypen3;P3 [kW];Public Key3;Steckertypen4;P4 [kW];Public Key4
Albwerk GmbH & Co. KG;Ennabeurer Weg;0;;72535;Heroldstatt;Baden-Württemberg;Landkreis Alb-Donau-Kreis;48,442398;9,659075;11.01.20;22;Normalladeeinrichtung;2;AC Steckdose Typ 2;22;;AC Steckdose Typ 2;22;;;;;;;
```

Resulting JSON:
```json
[
    {
        "address":{
            "additionalInfo":null,
            "city":"Heroldstatt",
            "district":"Landkreis Alb-Donau-Kreis",
            "postcode":"72535",
            "state":"Baden-W\u00fcrttemberg",
            "street":"Ennabeurer Weg",
            "streetNumber":"0"
        },
        "chargePoints":[
            {
                "maxPowerInKw":22.0,
                "plugTypes":"AC Steckdose Typ 2"
            },
            {
                "maxPowerInKw":22.0,
                "plugTypes":"AC Steckdose Typ 2"
            }
        ],
        "creationDate":"2020-01-11T00:00:00",
        "id":1,
        "location":{
            "latitude":48.442398,
            "longitude":9.659075
        },
        "operator":"Albwerk GmbH & Co. KG",
        "type":"Normalladeeinrichtung"
    }
]
```

## Reference

- [Bundesnetzagentur.de](https://www.bundesnetzagentur.de/DE/Sachgebiete/ElektrizitaetundGas/Unternehmen_Institutionen/E-Mobilitaet/start.html)