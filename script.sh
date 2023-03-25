#!/bin/bash

price=$(curl -s https://fr.finance.yahoo.com/quote/TSLA/ | grep -o '<fin-streamer[^>]*data-symbol="TSLA"[^>]*data-field="regularMarketPrice"[^>]*>[^<]*</fin-streamer>' | grep -o '[0-9]*\.[0-9]*')

timestamp=$(date +%s)


# Spécifiez le nom du fichier CSV
CSV_FILE="/home/ec2-user/ProjetLinux/history.csv"

# Vérifiez si le fichier CSV est vide
if [ ! -s "$CSV_FILE" ]; then
  # Ajoutez les noms des colonnes si le fichier est vide
  echo "timestamp,count" > $CSV_FILE
fi

echo $timestamp,$price >> $CSV_FILE
# /home/ec2-user/ProjetLinux/history.csv
