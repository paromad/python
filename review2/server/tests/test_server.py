def test_quantity_of_money(client):
    assert client.get("/quantity_of_money").data.decode() == "10000"


def test_put_money(client):
    money = int(client.get("/quantity_of_money").data)
    money = str(money + 100)
    client.post("/put_money?amount=100")
    assert client.get("/quantity_of_money").data.decode() == money


def test_get_profit(client):
    assert client.get("/get_profit").data.decode() == "0"
    client.post("/put_money?amount=100")
    assert client.get("/get_profit").data.decode() == "0"


def test_type(client):
    assert isinstance(client.get("/get_stocks").json, dict)
    assert isinstance(client.get("/get_prices").json, dict)


def test_sell_nothing(client):
    assert (
        client.post("/sell_stocks?stock={}&amount={}".format("hor5", 1)).data.decode()
        == "Failed"
    )


def test_buy(client):
    price_dict = client.get("/get_prices").json
    price = price_dict["hor5"]
    money = int(client.get("/quantity_of_money").data)
    money = str(money - price)
    client.post("/buy_stocks?stock={}&amount={}".format("hor5", 1))
    assert client.get("/quantity_of_money").data.decode() == money
    price_dict = client.get("/get_prices").json
    price = price_dict["hor5"]
    money = str(int(money) + price)
    client.post("/sell_stocks?stock={}&amount={}".format("hor5", 1))
    assert client.get("/quantity_of_money").data.decode() == money
