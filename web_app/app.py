# Веб-приложение с графическим интерфейсом

from flask import Flask, render_template, request, redirect, url_for, flash
import httpx

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'  # Для flash-сообщений

# URL API Gateway
API_GATEWAY_URL = "http://localhost:8000"

# Таймаут для запросов (в секундах)
TIMEOUT = 5.0

@app.route('/')
def index():
    """Главная страница"""
    return render_template('index.html')

@app.route('/products')
def products():
    """Страница списка товаров"""
    try:
        response = httpx.get(f"{API_GATEWAY_URL}/products", timeout=TIMEOUT)
        response.raise_for_status()
        products = response.json()
        return render_template('products.html', products=products)
    except httpx.HTTPError as e:
        flash(f"Ошибка загрузки товаров: {str(e)}", "error")
        return render_template('products.html', products=[])

@app.route('/orders', methods=['GET', 'POST'])
def orders():
    """Страница заказов: просмотр и создание"""
    if request.method == 'POST':
        try:
            # Получаем данные из формы и преобразуем в нужный формат
            order_data = {
                "product_id": int(request.form['product_id']),
                "customer_id": int(request.form['customer_id']),
                "quantity": int(request.form['quantity'])
            }
            response = httpx.post(f"{API_GATEWAY_URL}/orders", json=order_data, timeout=TIMEOUT)
            response.raise_for_status()
            flash("Заказ успешно создан!", "success")
            return redirect(url_for('orders'))
        except (httpx.HTTPError, ValueError) as e:
            flash(f"Ошибка создания заказа: {str(e)}", "error")

    # GET-запрос: показываем список заказов
    try:
        response = httpx.get(f"{API_GATEWAY_URL}/orders", timeout=TIMEOUT)
        response.raise_for_status()
        orders = response.json()
        return render_template('orders.html', orders=orders)
    except httpx.HTTPError as e:
        flash(f"Ошибка загрузки заказов: {str(e)}", "error")
        return render_template('orders.html', orders=[])

@app.route('/customers')
def customers():
    """Страница списка клиентов"""
    try:
        response = httpx.get(f"{API_GATEWAY_URL}/customers", timeout=TIMEOUT)
        response.raise_for_status()
        customers = response.json()
        return render_template('customers.html', customers=customers)
    except httpx.HTTPError as e:
        flash(f"Ошибка загрузки клиентов: {str(e)}", "error")
        return render_template('customers.html', customers=[])

if __name__ == '__main__':
    app.run(port=5004, debug=True)