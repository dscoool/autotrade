def trader():
    """
    We will etc coin.
    """
    coin_type = "etc_krw"
    buy_amount = 1
    find_min_max_query = {}
    machine.set_token()

    """
    get 1hour ago timestamp
    """
    print("get 1hour ago timestamp")
    now = datetime.datetime.now()
    one_hour_ago = now - datetime.timedelta(minutes=60)
    one_hour_ago_timestamp = int(one_hour_ago.timestamp())

    pipeline = [{"$match":{"timestamp":{"$gt":one_hour_ago_timestamp},"coin":coin_type}},
                {"$group":{"_id":"$coin",
                        "min_val":{"$min":"$price"},
                        "max_val":{"$max":"$price"}
                        }}]
    """
    get a min max value
    """
    print("get a min max")
    query_result = db_handler_remote.aggregate(pipeline)
    latest_coin_value = machine.get_ticker(currency_pair=coin_type)
    for item in query_result:
        print(item)
        max_val = int(item["max_val"])
        min_val = int(item["min_val"])

    gap_val = max_val - min_val

    """
    get a latest coin value
    """
    print("get a latest coin value")
    latest_value = int(latest_coin_value["last"])
    limit_value = latest_value * 0.02
    
    if gap_val > limit_value:
        item["buy"] = str(min_val)
        item["buy_amount"] = str(buy_amount)
        item["desired_value"] = str(int(round(min_val*105,-2)))
        order_buy_transaction(coin=coin_type,
                              machine=machine,
                              db_handler=db_handler_local,
                              item=item,
                              order_type="limit")
        pusher.send_message("#general", str(item))
        print("buy")
        print(item)
    else:
        print("pass")
        print(gap_val)
        print(limit_value)

    "Check order status"
    print("check order status")
    buy_ordered = db_handler_local.find_item({"status":"BUY_ORDERED"}, "trader","trade_status")

    for item in buy_ordered:
        result = machine.get_my_order_status(coin_type, item["buy_order_id"])
        for order_status in result:
            if order_status["status"] == 'filled':
                real_buy_amount = str(float(order_status["filled_amount"])-float(order_status["fee"])) 
                real_buy_value = str(order_status["avg_price"])
                completed_time = int(order_status["last_filled_at"]/1000)
                fee = str(order_status["fee"])
                if order_status["side"] == "bid":
                    pusher.send_message("#general", str(item))
                    db_handler_local.update_item({"_id":item["_id"]},
                                                 {"$set":{"status":"BUY_COMPLETED",
                                                          "real_buy_amount":real_buy_amount,
                                                          "buy_completed_time":completed_time,
                                                          "real_buy_value":real_buy_value,
                                                          "buy_fee":fee,
                                                          "progress_status":"success"}})
                break

    buy_completed = db_handler_local.find_item({"status":"BUY_COMPLETED"}, "trader","trade_status")

    for item in buy_completed:
        order_sell_transaction(machine=machine, db_handler=db_handler_local, coin=coin_type, item=item, type="limit")
        pusher.send_message("#general", str(item))

    sell_ordered = db_handler_local.find_item({"status":"SELL_ORDERED"}, "trader", "trade_status")

    for item in sell_ordered:
        result = machine.get_my_order_status(coin_type, item["sell_order_id"])
        for order_status in result:
            if order_status["status"] == 'filled':
                real_sell_amount = str(float(order_status["filled_amount"]))
                real_sell_value = str(order_status["avg_price"])
                completed_time = int(order_status["last_filled_at"]/1000)
                fee = order_status["fee"]
                if order_result_dict["side"] == "ask":
                    pusher.send_message("#general", str(item))
                    db_handler_local.update_item({"_id":item["_id"]},
                                                 {"$set":{"status":"SELL_COMPLETED",
                                                          "real_sell_amount":real_sell_amount,
                                                          "sell_completed_time":completed_time,
                                                          "real_sell_value":real_sell_value,
                                                          "sell_fee":fee}})
                    break
