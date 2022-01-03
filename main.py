#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Charge Station Data Converter (CSV to JSON):
# 
# The script normalizes and simplifies charge station data provided by Bundesnetzagentur.de under the CC-BY 4.0.
#
# Usage: 'python3 main.py input.csv'

import os
import sys
import csv
import json
import decimal
import locale
import pathlib
from datetime import date, datetime
	
# Helper:
def make_dict(identifier, dct):
	res = dct
	res = rename_key(res, 'Betreiber', 'operator')
	res = rename_key(res, 'Straße', 'street')
	res = rename_key(res, 'Hausnummer', 'streetNumber')
	res = rename_key(res, 'Adresszusatz', 'additionalInfo')
	res = rename_key(res, 'Postleitzahl', 'postcode')
	res = rename_key(res, 'Ort', 'city')
	res = rename_key(res, 'Bundesland', 'state')
	res = rename_key(res, 'Kreis/kreisfreie Stadt', 'district')
	res = rename_key(res, 'Breitengrad', 'latitude')
	res = rename_key(res, 'Längengrad', 'longitude')
	res = rename_key(res, 'Art der Ladeeinrichung', 'type')
	res = rename_key(res, 'Inbetriebnahmedatum', 'creationDate')
	res = drop_column(res, 'Anschlussleistung')
	res = add_identifier(identifier, res)
	res = drop_blanks(res)
	res = parse_creationDate(res)
	res = parse_coordinate(res)
	res = parse_address(res)
	res = parse_chargePoints(res)
	return res

def parse_creationDate(dct):
	res = dct
	res['creationDate'] = datetime.strptime(res['creationDate'], '%d.%m.%y')
	return res

def add_identifier(identifier, dct):
	res = dct
	res['id'] = identifier
	return res
	
def parse_coordinate(dct):
	res = dct
	
	if res['latitude'] and res['longitude']:
		location = {}
		location['latitude'] = float(res['latitude'].replace(',', '.'))
		location['longitude'] = float(res['longitude'].replace(',', '.'))
		res['location'] = location
	
	res = drop_column(res, 'latitude')
	res = drop_column(res, 'longitude')
	return res

def parse_address(dct):
	res = dct
	address = {}
	address['street'] = res['street']
	address['streetNumber'] = res['streetNumber']
	address['additionalInfo'] = res['additionalInfo']
	address['postcode'] = res['postcode']
	address['city'] = res['city']
	address['state'] = res['state']
	address['district'] = res['district']
	
	res['address'] = address

	res = drop_column(res, 'street')
	res = drop_column(res, 'streetNumber')
	res = drop_column(res, 'additionalInfo')
	res = drop_column(res, 'postcode')
	res = drop_column(res, 'city')
	res = drop_column(res, 'state')
	res = drop_column(res, 'district')
	return res

def parse_chargePoints(dct):
	res = dct
	chargePoints = []
	
	for index in range(1, 4):
		if res[f'P{index} [kW]'] and res[f'Steckertypen{index}']:
			chargePoint = {}
			chargePoint['plugTypes'] = res[f'Steckertypen{index}']
			chargePoint['maxPowerInKw'] = float(res[f'P{index} [kW]'].replace(',', '.'))
			chargePoints.append(chargePoint)

	res['chargePoints'] = chargePoints

	res = drop_column(res, 'Anzahl Ladepunkte')
	res = drop_column(res, 'Public Key1')
	res = drop_column(res, 'Public Key2')
	res = drop_column(res, 'Public Key3')
	res = drop_column(res, 'Public Key4')
	res = drop_column(res, 'P1 [kW]')
	res = drop_column(res, 'P2 [kW]')
	res = drop_column(res, 'P3 [kW]')
	res = drop_column(res, 'P4 [kW]')
	res = drop_column(res, 'Steckertypen1')
	res = drop_column(res, 'Steckertypen2')
	res = drop_column(res, 'Steckertypen3')
	res = drop_column(res, 'Steckertypen4')
	return res

def drop_column(dct, key):
	res = dct
	del res[key]
	return res

def drop_blanks(dct):
	return {k: None if not v else v for k, v in dct.items() }

def rename_key(dct, oldKey, newKey):
	res = dct
	res[newKey] = res[oldKey]
	del res[oldKey]
	return res

def json_serial(obj):	
	if isinstance(obj, (datetime, date)):
		return obj.isoformat()
	raise TypeError ("Type %s not serializable" % type(obj))
	
def generate_json(csvFilePath, jsonFilePath):
	data = []
	
	with open(csvFilePath, encoding='utf-8') as file:
		# Skip the first lines
		csvFile = file.read().splitlines(True)[5:]
		
		csvReader = csv.DictReader(csvFile, delimiter=';')
		
		for index, row in enumerate(csvReader):
			identifier = index + 1
			modifiedRow = make_dict(identifier, row)
			data.append(modifiedRow)
			
	with open(jsonFilePath, 'w', encoding='utf-8') as jsonFile:
		jsonFile.write(json.dumps(data, indent=4, sort_keys=True, separators=(',', ':'), default=json_serial))
		
		
# Main:
locale.setlocale(locale.LC_ALL, 'de_DE')
csv.field_size_limit(sys.maxsize)
outputFilePath = 'output.json'

if len(sys.argv) <= 1 or not os.path.exists(sys.argv[1]):
    print('Please provide the input CSV file\'s path as first argument, e.g., \'python3 main.py input.csv\'')
else:
	generate_json(sys.argv[1], outputFilePath)
	print(f'SUCCESS: JSON written to: {pathlib.Path(outputFilePath).resolve()}')
