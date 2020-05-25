import flask
import lib

app = flask.Flask("burse-server")
user = lib.User()
burse = lib.Burse()


@app.route("/quantity_of_money", methods=["GET"])
def quantity_of_money():
    return str(user.quantity_of_money())


@app.route("/get_profit", methods=["GET"])
def get_profit():
    return str(user.get_profit())


@app.route("/put_money", methods=["POST"])
def put_money():
    amount = int(flask.request.args["amount"])
    user.put_money(amount)
    return str(user.quantity_of_money())


@app.route("/get_my_stocks", methods=["GET"])
def get_users_stocks():
    return user.get_users_stocks()


@app.route("/get_prices", methods=["GET"])
def get_prices():
    return burse.get_prices()


@app.route("/buy_stocks", methods=["POST"])
def buy_stocks():
    stock = flask.request.args["stock"]
    amount = int(flask.request.args["amount"])
    return user.buy_stocks(burse, stock, amount)


@app.route("/sell_stocks", methods=["POST"])
def sell_stocks():
    stock = flask.request.args["stock"]
    amount = int(flask.request.args["amount"])
    return user.sell_stocks(burse, stock, amount)


def main():
    app.run("::", port=8000, debug=True)


if __name__ == "__main__":
    main()
