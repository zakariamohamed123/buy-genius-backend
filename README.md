##### BuyGenius APP

#### Overview
This project is a web application built and designed to support a marketplace platform where retailers can manage their products, and users can interact with these products through various features like feedback, wishlists, and messaging. The platform also includes an admin section to manage retailers, approve or reject their requests, and handle notifications.

#### Key Features
Key Features
User Authentication: Users can sign up as either regular users, retailers, or admins. Passwords are securely hashed using bcrypt. Admins are identified by specific email addresses.

Retailer Management: Retailers have dedicated profiles, and their access must be approved by an admin. Retailers can manage their product listings and interact with customers via messages.

Product Management: Retailers can add, edit, and delete products. Each product has fields such as name, price, description, category, and an image URL. Products are associated with categories, and feedback can be left by users.

Feedback and Wishlist: Users can provide feedback on products and add products to their wishlist. Feedback includes comments and is timestamped. Wishlists allow users to save products they are interested in.

Messaging System: A robust messaging system is in place where users can send and receive messages related to products and retailers.

Notifications: The application supports notifications for admin approval requests for new retailers.

#### Setup

### Prerequisites
Python 3.8 or higher
Virtualenv
Flask
SQLAlchemy
PostgreSQL

### Installation
Clone the repository:

`git clone git@github.com:zakariamohamed123/buy-genius-backend.git`
`cd buy-genius-backend`
Create and activate a virtual environment:

`pipenv --python /usr/bin/python`
`pipenv shell`

Install the dependencies:

`pipenv install`
Set up environment variables:

Create a .env file in the root directory and add the following:

SECRET_KEY=your_secret_key
SQLALCHEMY_DATABASE_URI=postgresql://buygeniususer:securepassword@localhost/buygenius
ADMIN_EMAIL_1=admin1@example.com
ADMIN_EMAIL_2=admin2@example.com
ADMIN_EMAIL_3=admin3@example.com

Initialize the database:

`flask db upgrade`

Run the application:

`flask run`

1. #### User Routes

   ### Signup


`@app.route('/signup', methods=['POST'])`
`def signup():`
    `data = request.json`
   ` user = User(username=data['username'], email=data['email'])`
   ` user.password = data['password']`
   ` db.session.add(user)`
   ` db.session.commit()`
    `return jsonify(user.to_dict()), 201`

### Login


`@app.route('/login', methods=['POST'])`
`def login():`
    `data = request.json`
   ` user = User.query.filter_by(email=data['email']).first()`
    `if user and user.verify_password(data['password']):`
       ` # Create a session or token here`
       ` return jsonify(user.to_dict()), 200`
  `  return jsonify({"message": "Invalid credentials"}), 401`

### Get User


   ` @app.route('/users/<int:user_id>', methods=['GET'])`
  `  def get_user(user_id):`
      `  user = User.query.get(user_id)`
        `if user:`
        `   return jsonify(user.to_dict()), 200`
       ` return jsonify({"message": "User not found"}), 404`

2. ### Retailer Routes

    ## Add Retailer

`@app.route('/retailers', methods=['POST'])`
`def add_retailer():`
  `  data = request.json`
   ` retailer = Retailer(name=data['name'], user_id=data``['user_id'], whatsapp_number=data.get('whatsapp_number'))`
   ` db.session.add(retailer)`
   ` db.session.commit()`
   ` return jsonify(retailer.to_dict()), 201`

 ### Get Retailer


   ` @app.route('/retailers/<int:retailer_id>', methods=['GET'])`
    `def get_retailer(retailer_id):`
    `    retailer = Retailer.query.get(retailer_id)`
     `   if retailer:`
     `       return jsonify(retailer.to_dict()), 200`
     `   return jsonify({"message": "Retailer not found"}),` `404`

3. ### Product Routes

## Add Product


`@app.route('/products', methods=['POST'])`
`def add_product():`
  `  data = request.json`
    `product = Product(`
        `name=data['name'],`
       ` price=data['price'],`
       ` description=data.get('description'),`
       ` delivery_cost=data.get('delivery_cost'),`
       ` payment_mode=data.get('payment_mode'),`
      `  retailer_id=data['retailer_id'],`
      `  category_id=data['category_id'],`
     `   image_url=data.get('image_url'),`
     `   estimated_value=data.get('estimated_value'),`
     `   marginal_benefit=data.get('marginal_benefit')`
    
   ` db.session.add(product)`
   ` db.session.commit()`
  `  return jsonify(product.to_dict()), 201`

### Get Product


   ` @app.route('/products/<int:product_id>', methods=['GET'])`
    `def get_product(product_id):`
       ` product = Product.query.get(product_id)`
        `if product:`
            `return jsonify(product.to_dict()), 200`
       ` return jsonify({"message": "Product not found"}), 404`

4. ### Feedback Routes

    ## Add Feedback

`@app.route('/feedback', methods=['POST'])`
`def add_feedback():`
   ` data = request.json`
   ` feedback = Feedback(`
   `     user_id=data['user_id'],`
   `     product_id=data['product_id'],`
   `     comment=data.get('comment')`
   ` )`
   ` db.session.add(feedback)`
    `db.session.commit()`
   ` return jsonify(feedback.to_dict()), 201`

### Get Feedback



   ` @app.route('/feedback/<int:feedback_id>', methods=``['GET'])`
    `def get_feedback(feedback_id):`
        `feedback = Feedback.query.get(feedback_id)`
        `if feedback:`
       `     return jsonify(feedback.to_dict()), 200`
        `return jsonify({"message": "Feedback not found"}),` `404`

5. ### Message Routes

   ## Send Message

    

`@app.route('/messages', methods=['POST'])`
`def send_message():`
   ` data = request.json`
  `  message = Message(`
   `     sender_id=data['sender_id'],`
   `     receiver_id=data['receiver_id'],`
   `     product_id=data.get('product_id'),`
   `     retailer_id=data.get('retailer_id'),`
   `     content=data['content']`
   ` )`
   ` db.session.add(message)`
   ` db.session.commit()`
   ` return jsonify(message.to_dict()), 201`

### Get Messages


    `@app.route('/messages/<int:message_id>', methods=` ['GET'])`
   ` def get_message(message_id):`
      `  message = Message.query.get(message_id)`
       ` if message:`
       `     return jsonify(message.to_dict()), 200`
       ` return jsonify({"message": "Message not found"}), 404`

6. ### Wishlist Routes

    ## Add to Wishlist

`@app.route('/wishlists', methods=['POST'])`
`def add_to_wishlist():`
  `  data = request.json`
  `  wishlist = Wishlist(user_id=data['user_id'], `product_id=data`['product_id']`
   ` db.session.add(wishlist)`
   ` db.session.commit()`
  `  return jsonify(wishlist.to_dict()), 201`

### Get Wishlist


`@app.route('/wishlists/<int:wishlist_id>', methods=['GET'])`
`def get_wishlist(wishlist_id):`
   ` wishlist = Wishlist.query.get(wishlist_id)`
   ` if wishlist:`
   `     return jsonify(wishlist.to_dict()), 200`
    `return jsonify({"message": "Wishlist item not found"}),` 404`


#### Contributing
We welcome contributions to the BuyGenius! If you'd like to contribute, please follow these guidelines:

Fork the Repository

Click on the "Fork" button at the top right of the repository page to create your own copy of the project.
Create a New Branch

Navigate to your forked repository and create a new branch for your feature or bug fix. Use a descriptive name for your branch, e.g., feature/new-feature.
Make Your Changes

Implement your changes and make sure to write clear and concise commit messages. Follow the existing code style and conventions of the project.
Test Thoroughly

Ensure that your changes are well-tested. Run all existing tests and write new tests if necessary to cover your modifications.
Submit a Pull Request

Go to the "Pull Requests" section of the original repository and click "New Pull Request." Select your branch and provide a detailed description of your changes. Explain why the changes are necessary and how they improve the project.
Review Process

Your pull request will be reviewed. Be prepared to make additional changes if requested.
Thank you for contribution BuyGenius!