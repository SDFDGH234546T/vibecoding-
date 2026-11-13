
if __name__ == '__main__':

    # 构建测试数据
    data = {
        "slots":{
            "product":"100"
        }
    }

    # 调用eval方法
    res = bool(
        eval('slots.get("product_id")',{},data))
    print(res)