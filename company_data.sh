#!/bin/bash

previous_close=$(curl -s https://fr.finance.yahoo.com/quote/TSLA/ | grep -oP '(?<=data-test="PREV_CLOSE-value">)[\d,]+')

cap_boursiere=$(curl -s https://fr.finance.yahoo.com/quote/TSLA/ | grep -oP '(?<=data-test="MARKET_CAP-value">)[\d,]+')

ouverture=$(curl -s https://fr.finance.yahoo.com/quote/TSLA/ | grep -oP '(?<=data-test="OPEN-value">)[\d,]+')

volume=$(curl -s https://fr.finance.yahoo.com/quote/TSLA/ | grep -oP '(?<=data-test="AVERAGE_VOLUME_3MONTH-value">)[\d, ]+')

target=$(curl -s https://fr.finance.yahoo.com/quote/TSLA/ | grep -oP '(?<=data-test="ONE_YEAR_TARGET_PRICE-value">)[\d,]+')

#echo -e "Prev.Close : $previous_close \nOpen.Price : $ouverture \nCap.Boursière : $cap_boursiere \nVolume : $volume M \nTarget Price : $target"


# Spécifiez le nom du fichier CSV
CSV_FILE="report.csv"

# Vérifiez si le fichier CSV est vide
if [ ! -s "$CSV_FILE" ]; then
  # Ajoutez les noms des colonnes si le fichier est vide
  echo "prev_close,open_price,cap_boursiere,volume,target" > $CSV_FILE
fi

echo $previous_close,$ouverture,$cap_boursiere,$volume,$target >> $CSV_FILE
