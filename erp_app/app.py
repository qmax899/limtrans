from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# In-memory storage for products
products = []

# simple id generator
_next_id = 1

def get_next_id():
    global _next_id
    result = _next_id
    _next_id += 1
    return result

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/inventory')
def inventory():
    return render_template('inventory.html', products=products)

@app.route('/inventory/new', methods=['GET', 'POST'])
def new_product():
    if request.method == 'POST':
        name = request.form['name']
        quantity = int(request.form['quantity'])
        price = float(request.form['price'])
        products.append({'id': get_next_id(), 'name': name, 'quantity': quantity, 'price': price})
        return redirect(url_for('inventory'))
    return render_template('new_product.html')

@app.route('/inventory/<int:product_id>/edit', methods=['GET', 'POST'])
def edit_product(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    if not product:
        return 'Product not found', 404
    if request.method == 'POST':
        product['name'] = request.form['name']
        product['quantity'] = int(request.form['quantity'])
        product['price'] = float(request.form['price'])
        return redirect(url_for('inventory'))
    return render_template('edit_product.html', product=product)

@app.route('/inventory/<int:product_id>/delete', methods=['POST'])
def delete_product(product_id):
    global products
    products = [p for p in products if p['id'] != product_id]
    return redirect(url_for('inventory'))

if __name__ == '__main__':
    app.run(debug=True)
