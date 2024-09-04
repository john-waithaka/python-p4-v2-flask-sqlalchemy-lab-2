from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin


metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)



# class Customer(db.Model):
#     __tablename__ = 'customers'

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String)

#     def __repr__(self):
#         return f'<Customer {self.id}, {self.name}>'

"""edited the customer model to add a relationship named reviews that establishes a relationship with the Review model. 
Assign the back_populates parameter to match the property name defined to the reciprocal relationship in Review."""
class Customer(db.Model, SerializerMixin):
    __tablename__ = "customers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    serialize_rules = ("-reviews.customer",)

    reviews = db.relationship("Review", back_populates="customer")

    # Association proxy to get items for this customer through reviews
    items = association_proxy(
        "reviews", "item", creator=lambda item_obj: Review(item=item_obj)
    )

    def __repr__(self):
        return f"<Customer {self.id}, {self.name}>"




# class Item(db.Model):
#     __tablename__ = 'items'

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String)
#     price = db.Column(db.Float)

#     def __repr__(self):
#         return f'<Item {self.id}, {self.name}, {self.price}>'

"""Edit the Item model to add a relationship named reviews that establishes a relationship with the Review model. 
Assign the back_populates parameter to match the property name defined to the reciprocal relationship in Review."""


class Item(db.Model, SerializerMixin):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Float)

    serialize_rules = ("-reviews.item",)

    reviews = db.relationship("Review", back_populates="item")

    def __repr__(self):
        return f"<Item {self.id}, {self.name}, {self.price}>"


"""added a Review model that inherits from db model and add: 
a string named __tablename__ assigned to the value 'reviews'.
a column named id to store an integer that is the primary key.
a column named comment to store a string.
a column named customer_id that is a foreign key to the 'customers' table.
a column named item_id that is a foreign key to the 'items' table.
a relationship named customer that establishes a relationship with the Customer model and 
Assign the back_populates parameter to match the property name defined to the reciprocal relationship in Customer.
a relationship named item that establishes a relationship with the Item model and
Assign the back_populates parameter to match the property name defined to the reciprocal relationship in Item.

"""
class Review(db.Model, SerializerMixin):
    __tablename__ = "reviews"

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String)

    serialize_rules = ("-customer.reviews", "-item.reviews")

    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"))
    item_id = db.Column(db.Integer, db.ForeignKey("items.id"))

    customer = db.relationship("Customer", back_populates="reviews")
    item = db.relationship("Item", back_populates="reviews")

    def __repr__(self):
        return f"<Review {self.id}, {self.comment}, {self.customer.name}, {self.item.name}>"



"""solution"""
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import MetaData
# from sqlalchemy.ext.associationproxy import association_proxy
# from sqlalchemy_serializer import SerializerMixin


# metadata = MetaData(
#     naming_convention={
#         "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
#     }
# )

# db = SQLAlchemy(metadata=metadata)


# class Customer(db.Model, SerializerMixin):
#     __tablename__ = "customers"

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String)

#     serialize_rules = ("-reviews.customer",)

#     reviews = db.relationship("Review", back_populates="customer")

#     # Association proxy to get items for this customer through reviews
#     items = association_proxy(
#         "reviews", "item", creator=lambda item_obj: Review(item=item_obj)
#     )

#     def __repr__(self):
#         return f"<Customer {self.id}, {self.name}>"


# class Item(db.Model, SerializerMixin):
#     __tablename__ = "items"

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String)
#     price = db.Column(db.Float)

#     serialize_rules = ("-reviews.item",)

#     reviews = db.relationship("Review", back_populates="item")

#     def __repr__(self):
#         return f"<Item {self.id}, {self.name}, {self.price}>"


# class Review(db.Model, SerializerMixin):
#     __tablename__ = "reviews"

#     id = db.Column(db.Integer, primary_key=True)
#     comment = db.Column(db.String)

#     serialize_rules = ("-customer.reviews", "-item.reviews")

#     customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"))
#     item_id = db.Column(db.Integer, db.ForeignKey("items.id"))

#     customer = db.relationship("Customer", back_populates="reviews")
#     item = db.relationship("Item", back_populates="reviews")

#     def __repr__(self):
#         return f"<Review {self.id}, {self.comment}, {self.customer.name}, {self.item.name}>"