from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/user/<username>')  # <username> captures any text from URL, visit: /user/Alice, /user/Bob
def user_profile(username):
    return render_template('user.html', username=username)


@app.route('/post/<int:post_id>')  # <int:post_id> captures only integers, /post/abc returns 404
def show_post(post_id):
    posts = {  # Simulated post data (in real apps, this comes from a database)
        1: {'title': 'Getting Started with Flask', 'content': 'Flask is a micro-framework...'},
        2: {'title': 'Understanding Routes', 'content': 'Routes map URLs to functions...'},
        3: {'title': 'Working with Templates', 'content': 'Jinja2 makes HTML dynamic...'},
    }
    post = posts.get(post_id)  # Get the post or None if not found
    return render_template('post.html', post_id=post_id, post=post)


@app.route('/user/<username>/post/<int:post_id>')  # Multiple dynamic segments, visit: /user/Alice/post/1
def user_post(username, post_id):
    return render_template('user_post.html', username=username, post_id=post_id)


@app.route('/about/')  # Trailing slash means both /about and /about/ work
def about():
    return render_template('about.html')


@app.route('/links')  # Demonstrates url_for() - generates URLs dynamically (better than hardcoding!)
def show_links():
    links = {
        'home': url_for('home'),
        'about': url_for('about'),
        'user_alice': url_for('user_profile', username='Alice'),
        'user_bob': url_for('user_profile', username='Bob'),
        'post_1': url_for('show_post', post_id=1),
        'post_2': url_for('show_post', post_id=2),
    }
    return render_template('links.html', links=links)

products = {
        1: {'id': 1, 'name': 'Laptop', 'price': 70000},
        2: {'id': 2, 'name': 'Mobile', 'price': 20000},
        3: {'id': 3, 'name': 'Airbuds', 'price': 1000}
    }

@app.route('/product/<int:product_id>')
def show_products(product_id):
    product = products.get(product_id)
    if product:
        return render_template('product.html', product=product)
    else:
        return "<h1>Product Not Found</h1>", 404
    
@app.route('/category/<category_name>/product/<int:product_id>')
def category_product(category_name, product_id):
    product = products.get(product_id)
    if product:
        return render_template('category.html',category=category_name,product=product)
    else:
        return "<h2>Product Not Found</h2>", 404

@app.route('/search/<query>')
def search(query):
    query_lower = query.lower()
    results = [p for p in products.values() if query_lower in p['name'].lower()]
    if results:
        return render_template('search.html', query=query, results=results)
    else:
        return "<h2>Product Not Found</h2>", 404



@app.route('/search', methods=['GET', 'POST'])
def search_form():
    if request.method == 'POST':
        query = request.form.get('query')
        return redirect(url_for('search', query=query))
    return render_template('search.html')

if __name__ == '__main__':
    app.run(debug=True)