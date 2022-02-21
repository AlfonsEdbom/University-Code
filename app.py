from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# Define a model
# Not strictly needed, but simplifies this example.
class Snack:
    def __init__(self, name, amount, price):
        self.name = name
        self.amount = amount
        self.price = price

    def __str__(self):
        return f'Name: {self.name}, Amount: {self.amount}, Price: {self.price}'

# Base snacks
snacks = [Snack('Carrot', 10, 5),
          Snack('Chocolate', 5, 10),
          Snack('Sunflower seeds', 150, 1)]

# The first page the user will see
@app.route('/')
def index():
    # render_template automatically looks for templates in the "templates" directory
    return render_template('index.html')


# Shows all the available snacks
@app.route('/snacks', methods=['GET'])
def language():
    global snacks

    return render_template('snacks.html', snacks=snacks)


# Adds a new snack, or updates an existing snack
@app.route('/snacks', methods=['POST'])
def add_snack():
    global snacks

    snack_name = request.form['snack_name'] 
    amount = int(request.form['amount'])
    price = int(request.form['price'])

    new_snack = Snack(snack_name, amount, price)
    print('Adding snack:', new_snack)
    
    # If snack already exists, update values
    for index, old_snack in enumerate(snacks):
        if old_snack.name == new_snack.name:
            snacks[index] = snack
            break
    else:

        # Else, add the new snack to the list of snacks
        snacks.append(new_snack)

    return render_template('snacks.html', snacks=snacks)

# Deletes a snack
@app.route('/snacks/delete', methods=['POST'])
def delete_language():
    global snacks 

    snack_to_delete = request.form['snack_name']

    print(f'Deleting snack {snack_to_delete}')
    
    snacks = [snack for snack in snacks if snack.name != snack_to_delete] 
    
    # Send user back to snacks page
    return redirect('/snacks')

