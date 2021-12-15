
import json

dictionary = {}

def load():
   global dictionary
   try:
      with open('junior.dat') as f:
         dictionary = json.load(f)
   except:
      dictionary = {}

def save():
   with open('junior.dat', 'w') as f:
      json.dump(dictionary, f)

def store(key, value):
   dictionary[key] = value
   return f"{key} assigned to {value}"

def clear_dictionary():
   global dictionary  # try to remove this.
   dictionary = {}

def get_dictionary():
   return dictionary