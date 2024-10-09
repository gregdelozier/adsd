from flask import Flask, request, jsonify, render_template_string, redirect, url_for
from peewee import SqliteDatabase, Model, CharField

# Initialize Flask app
app = Flask(__name__)

# Initialize PeeWee and connect to a SQLite database
db = SqliteDatabase('my_app.db')

# Define a model to represent a table in the database
class BaseModel(Model):
    class Meta:
        database = db

class Message(BaseModel):
    name = CharField()  # Column to store the name of the person
    content = CharField()  # Column to store the message content

# Recreate the database and tables
db.connect()
db.drop_tables([Message])  # Drop the table if it already exists (for development purposes)
db.create_tables([Message])  # Create the table again with the updated schema

# HTML templates as strings
index_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Home Page</title>
</head>
<body>
    <h1>Welcome to the Message Manager</h1>
    <button onclick="window.location.href='/add_message'">Add a Message</button>
    <button onclick="window.location.href='/messages'">View Messages</button>
</body>
</html>
"""

add_message_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Add Message</title>
</head>
<body>
    <h2>Add a New Message</h2>
    <form method="POST" action="/add_message">
        <label for="name">Name:</label>
        <input type="text" id="name" name="name" required><br><br>
        <label for="content">Message:</label>
        <textarea id="content" name="content" rows="4" cols="50" required></textarea><br><br>
        <button type="submit">Submit</button>
    </form>
</body>
</html>
"""

messages_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Messages</title>
</head>
<body>
    <h2>All Messages</h2>
    <ul>
        {% for message in messages %}
            <li><strong>{{ message.name }}:</strong> {{ message.content }} 
                <button onclick="window.location.href='/delete/{{ message.id }}'">Delete</button>
            </li>
        {% endfor %}
    </ul>
    <button onclick="window.location.href='/add_message'">Add More Messages</button>
    <button onclick="window.location.href='/goodbye'">Finish Editing</button>
</body>
</html>
"""

delete_message_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Delete Message</title>
</head>
<body>
    <h2>Delete Message</h2>
    {% if message %}
        <p>Are you sure you want to delete the message: <strong>{{ message.content }}</strong> by <em>{{ message.name }}</em>?</p>
        <form method="POST" action="">
            <button type="submit">Confirm Delete</button>
        </form>
    {% else %}
        <p>Message not found!</p>
    {% endif %}
</body>
</html>
"""

goodbye_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Goodbye</title>
</head>
<body>
    <h2>Goodbye! Have a nice day!</h2>
    <button onclick="window.location.href='/'">Return to Home</button>
</body>
</html>
"""

# Flask routes using render_template_string with embedded templates
@app.route("/")
@app.route("/hello")
def hello_world():
    return render_template_string(index_template)

# Route to display the add message form
@app.route("/add_message", methods=["GET", "POST"])
def add_message():
    if request.method == "POST":
        name = request.form.get("name")
        content = request.form.get("content")
        if not content or not name:
            return jsonify({"error": "Both name and content are required"}), 400

        # Insert the message into the database using PeeWee
        Message.create(name=name, content=content)
        return redirect(url_for("get_messages"))

    return render_template_string(add_message_template)

# Route to display and edit messages
@app.route("/messages", methods=["GET"])
def get_messages():
    messages = Message.select()
    return render_template_string(messages_template, messages=messages)

# Route to delete a message by ID
@app.route("/delete/<int:id>", methods=["GET", "POST"])
def delete_message(id):
    if request.method == "POST":
        query = Message.delete().where(Message.id == id)
        deleted = query.execute()

        if deleted:
            return redirect(url_for("goodbye"))
        else:
            return jsonify({"error": "Message not found"}), 404

    message = Message.get_or_none(Message.id == id)
    return render_template_string(delete_message_template, message=message)

@app.route("/goodbye")
def goodbye():
    return render_template_string(goodbye_template)

# Run the Flask application
if __name__ == "__main__":
    app.run(debug=True)
