#!/bin/bash

price=$(curl -s https://fr.finance.yahoo.com/quote/TSLA/ | grep -o '<fin-streamer[^>]*data-symbol="TSLA"[^>]*data-field="regularMarketPrice"[^>]*>[^<]*</fin-streamer>' | grep -o '[0-9]*\.[0-9]*')

timestamp=$(date +%s)

echo $timestamp,$price >> /home/ubuntu/ProjetLinux/history.csv
