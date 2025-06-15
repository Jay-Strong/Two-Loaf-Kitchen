from flask import Flask, render_template, request, redirect, flash
from flask_mail import Mail, Message
import stripe
import os
from dotenv import load_dotenv
# import gunicorn


app = Flask(__name__)

env_path = "C:\\Users\\jayal\\OneDrive\\Coding Projects\\Python\\keys.env"
load_dotenv(dotenv_path=env_path)  # Loads variables from .env
app.secret_key = os.getenv("SECRET_KEY")
email_password = os.getenv("EMAIL_PASSWORD")
stripe_key = os.getenv("STRIPE_API_KEY")
email_user = os.getenv("EMAIL_USERNAME")
app.config['EMAIL_USERNAME'] = email_user
app.config['MAIL_DEFAULT_SENDER'] = email_user

# Email Configuration (Gmail example)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = email_user  # Replace
app.config['MAIL_PASSWORD'] = email_password     # Use App Password if using Gmail
mail = Mail(app)
print(email_user)
# Stripe Configuration
stripe.api_key = stripe_key  # Replace with your Stripe secret key
YOUR_DOMAIN = "https://two-loaf-kitchen.onrender.com"      # Replace when deploying

@app.route("/", methods=["GET", "POST"])
def order():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        bread_type = request.form["bread_type"]
        quantity = int(request.form["quantity"])
        price_per_loaf = 10  # in dollars
        # Here you can add logic to process the order, e.g., save to database, send email, etc.
        flash('Order placed successfully!', 'success')
    #     return redirect(url_for('order'))
    # return render_template('order.html')

        # Send confirmation email
        msg = Message(
            subject = "Two Loaf Kitchen – Order Confirmation",
            sender=email_user,
            recipients=[email],
            body=f"""Hi {name},

Thanks for ordering {quantity} loaf/loaves of {bread_type} bread!

We'll be in touch soon to confirm pickup/delivery details.

Warm regards,  
Jay – Two Loaf Kitchen"""
        )
        mail.send(msg)

        # Create Stripe Checkout Session
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": f"{bread_type} Bread"
                    },
                    "unit_amount": price_per_loaf * 100,
                },
                "quantity": quantity,
            }],
            mode="payment",
            success_url=YOUR_DOMAIN + "/success",
            cancel_url=YOUR_DOMAIN + "/cancel",
        )

        if checkout_session.url is not None:
            return redirect(checkout_session.url, code=303)
        else:
            return "<h2>There was an error creating the payment session. Please try again later.</h2>", 500

    return render_template("order.html")

@app.route("/success")
def success():
    return "<h2>Thank you! Your payment was successful.</h2>"

@app.route("/cancel")
def cancel():
    return "<h2>Payment canceled. No worries, come back anytime!</h2>"

if __name__ == "__main__":
    app.run(debug=True)