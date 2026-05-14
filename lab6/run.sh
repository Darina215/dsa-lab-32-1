#!/bin/bash
python currency_manager.py &
python data_manager.py &
python gateway.py
wait