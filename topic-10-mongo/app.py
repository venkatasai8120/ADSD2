from flask import Flask, render_template, request, redirect, url_for
import database

app = Flask(__name__)

# -----------------------------
# PET ROUTES
# -----------------------------

@app.route("/")
@app.route("/list")
def get_list():
    pets = database.retrieve_pets()
    return render_template("list.html", pets=pets)


@app.route("/create", methods=["GET", "POST"])
def get_post_create():

    if request.method == "GET":
        kinds = database.retrieve_kinds()
        return render_template("create.html", kinds=kinds)

    if request.method == "POST":
        data = dict(request.form)

        # Convert age safely
        try:
            data["age"] = int(data["age"])
        except:
            data["age"] = 0

        # color is included automatically from form
        database.create_pet(data)
        return redirect(url_for("get_list"))


@app.route("/update/<id>", methods=["GET", "POST"])
def get_update(id):

    if request.method == "GET":
        kinds = database.retrieve_kinds()
        pet = database.retrieve_pet(id)

        if pet is None:
            return "Pet not found"

        return render_template("update.html", pet=pet, kinds=kinds)

    if request.method == "POST":
        data = dict(request.form)

        try:
            data["age"] = int(data["age"])
        except:
            data["age"] = 0

        database.update_pet(id, data)
        return redirect(url_for("get_list"))


@app.route("/delete/<id>")
def get_delete(id):
    database.delete_pet(id)
    return redirect(url_for("get_list"))


# -----------------------------
# KIND ROUTES
# -----------------------------

@app.route("/kind/list")
def list_kinds():
    kinds = database.retrieve_kinds()
    return render_template("kind_list.html", kinds=kinds)


@app.route("/kind/create", methods=["GET", "POST"])
def create_kind():
    if request.method == "POST":
        data = dict(request.form)
        database.create_kind(data)
        return redirect(url_for("list_kinds"))

    return render_template("kind_create.html")


@app.route("/kind/update/<id>", methods=["GET", "POST"])
def update_kind(id):
    if request.method == "POST":
        data = dict(request.form)
        database.update_kind(id, data)
        return redirect(url_for("list_kinds"))

    kind = database.retrieve_kind(id)
    if kind is None:
        return "Kind not found"

    return render_template("kind_update.html", kind=kind)


@app.route("/kind/delete/<id>")
def delete_kind(id):
    error_message = database.delete_kind(id)
    if error_message:
        kinds = database.retrieve_kinds()
        return render_template("kind_list.html", kinds=kinds, error_message=error_message)

    return redirect(url_for("list_kinds"))


# -----------------------------
# START FLASK SERVER
# -----------------------------
if __name__ == "__main__":
    print("Starting Flask...")
    app.run(host="0.0.0.0", port=5000, debug=True)
