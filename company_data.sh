#!/bin/bash

previous_close=$(curl -s https://fr.finance.yahoo.com/quote/TSLA/ | grep -oP '(?<=data-test="PREV_CLOSE-value">)[\d,]+' | sed 's/,/./')

cap_boursiere=$(curl -s https://fr.finance.yahoo.com/quote/TSLA/ | grep -oP '(?<=data-test="MARKET_CAP-value">)[\d,]+' | sed 's/,/./')

ouverture=$(curl -s https://fr.finance.yahoo.com/quote/TSLA/ | grep -oP '(?<=data-test="OPEN-value">)[\d,]+' | sed 's/,/./')

volume=$(curl -s https://fr.finance.yahoo.com/quote/TSLA/ | grep -oP '(?<=data-test="AVERAGE_VOLUME_3MONTH-value">)[\d, ]+' | sed 's/,/./')

target=$(curl -s https://fr.finance.yahoo.com/quote/TSLA/ | grep -oP '(?<=data-test="ONE_YEAR_TARGET_PRICE-value">)[\d,]+' | sed 's/,/./')

timestamp=$(date +%s)

# Spécifiez le nom du fichier CSV
CSV_FILE="report.csv"

# Vérifiez si le fichier CSV est vide
if [ ! -s "$CSV_FILE" ]; then
  # Ajoutez les noms des colonnes si le fichier est vide
  echo "timestamp,prev_close,open_price,cap_boursiere,volume,target" > $CSV_FILE
fi

echo $timestamp,$previous_close,$ouverture,$cap_boursiere,$volume,$target >> $CSV_FILE
