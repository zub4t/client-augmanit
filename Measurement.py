import sys
import os
import json

cwd = os.getcwd()
sys.path.insert(0, os.path.join(cwd, "..", "commons"))


class Measurement:

    def __init__(self, timestamp, bssid, distance, ground_truth, ap_location,source='synthetic',exp='EXP_None'):
        self.timestamp = timestamp
        self.bssid = bssid
        self.distance = distance
        self.ground_truth = ground_truth
        self.ap_location = ap_location  
        self.source = source
        self.exp= exp
    def __repr__(self):
        return (f"Timestamp: {self.timestamp:.1f}, BSSID: {self.bssid}, Distance: {self.distance:.2f}, Ground Truth Distance: {self.ground_truth}, Source: {self.source}, EXP: {self.exp}")
