"""Models for Cupcake app."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


class Cupcake(db.Model):
    """Class for cupcake items."""

    __tablename__ = "cupcakes"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
    )

    flavor = db.Column(
        db.String(),
        nullable=False
    )

    size = db.Column(
        db.String(),
        nullable=False
    )

    rating = db.Column(
        db.Float(),
        nullable=False
    )

    image = db.Column(
        db.String(),
        nullable=False,
        default="https://tinyurl.com/demo-cupcake"
    )

    def __repr__(self):
        """Displays info about an individual cupcake instance."""

        c = self
        return f"<Cupcake {c.id} {c.flavor} {c.size} {c.rating} {c.image}>"
    
    def serialize_cupcake(self):
        """Serialize a cupcake SQLAlchemy obj to dictionary."""

        return {
            "id": self.id,
            "flavor": self.flavor,
            "size": self.size,
            "rating": self.rating,
            "image": self.image
        }
    
    def serialize_deleted_cupcake(self):
        """Serialize a deleted cupcake SQLAlchemy obj message."""

        return {
            "message": "Deleted",
            "id": self.id
        }

