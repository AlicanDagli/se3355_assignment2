from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
db = SQLAlchemy(app)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(50), nullable=False)




@app.route('/')
def home():
    products = Product.query.all()
    return render_template('home.html', products=products)



@app.route('/search_results', methods=['GET', 'POST'])
def search_results():
    if request.method == 'GET':
        query = request.args.get('query', '')
    
        search_results = Product.query.filter((Product.name.ilike(f"%{query}%")) | (Product.description.ilike(f"%{query}%")) | (Product.category.ilike(f"%{query}%"))).all()

        return render_template('search_results.html', search_results=search_results, query=query)

    return redirect(url_for('search_results'))



@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get(product_id)
    if product:
        breadcrumb = [{"url": "/", "name": "Ana Sayfa"}, {"url": "", "name": product.name}]
        return render_template('product_detail.html', product=product, breadcrumb=breadcrumb)
    else:
        return "Ürün bulunamadı", 404


if __name__ == '__main__':
    with app.app_context():
       
        db.drop_all()
        db.create_all()

      
        if not Product.query.first():
            sample_products = [
                {"name": "Lacoste", "description": "Erkek Regular Fit Bisiklet Yaka Organik Pamuk Lacivert Sweatshirt", "price": 3.799, "image": "product1.jpg", "category": "Erkek Giyim Sweatshirt Lacoste Sweatshirt"},
                {"name": "Apple", "description": "iPhone 15 Pro 128 GB Natürel Titanyum Telefon", "price": 69999, "image": "product2.jpg", "category": "Elektronik Telefon Cep Telefonu Akıllı Cep Telefonu Apple iPhone IOS Cep Telefonları"},
                {"name": "Samsung", "description": " Galaxy Z Flip4 128 GB Gri Cep Telefonu", "price": 25999, "image": "product3.jpg", "category": "Elektronik Telefon Cep Telefonu Akıllı Cep Telefonu Samsung Android Cep Telefonları"},
                {"name": "Lacoste", "description": "Kadın Relaxed Fit Bisiklet Yaka Baskılı Beyaz Sweatshirt ", "price": 4.999, "image": "product4.jpg", "category": "Kadın Giyim Sweatshirt Lacoste Sweatshirt"},
                {"name": "Pandora", "description": "Işıltılı Kalp Tenis Bilezik", "price": 2329, "image": "product5.jpg", "category": "Kadın Aksesuar Takı & Mücevher Bileklik Gümüş Bileklik Pandora Gümüş Bileklik"},
                {"name": "Nike", "description": "Airforce 1 Unisex Günlük Spor Ayakkabı", "price": 2159, "image": "product6.jpg", "category": "Unisex Ayakkabı Spor Ayakkabı Sneaker Nike Sneaker"},
                {"name": "Lacoste", "description": "Erkek Loose Fit Bisiklet Yaka Renk Bloklu Siyah Sweatshirt ", "price": 4.999, "image": "product7.jpg", "category": "Erkek Giyim Sweatshirt Lacoste Sweatshirt"},
                {"name": "Swarovski", "description": "Swarovski Taşlı Kuğu Gümüş Kolye", "price": 1450, "image": "product8.jpg", "category": "Kadın Aksesuar Takı & Mücevher Kolye Gümüş Kolye Swarovski Gümüş Kolye"},
                {"name": "Tommy Hilfiger", "description": "Kadın Marka Logolu Düz Taban Kaydırmaz Günlük Kullanım Beyaz Sneaker ", "price": 2999, "image": "product9.jpg", "category": "Kadın Ayakkabı Spor Ayakkabı Sneaker Tommy Hilfiger Sneaker"},
                {"name": "Tommy Hilfiger", "description": "Kadın Marka Logolu Ayarlanabilir Krem Omuz Çantası", "price": 3100, "image": "product10.jpg", "category": "Kadın Aksesuar Çanta Omuz Çantası Tommy Hilfiger Omuz Çantası"}
            ]

            for product_data in sample_products:
                product = Product(**product_data)
                db.session.add(product)

            db.session.commit()

    app.run(debug=True)