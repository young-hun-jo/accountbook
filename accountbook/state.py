import reflex as rx


class UserInputs(rx.State):
    actions: list[str] = ["지출", "수입"]
    categories: list[str] = ["생활비", "데이트비", "문화비", "법인카드", "모임비", "교통카드캐시백",
                             "병원비", "공과금", "캐시백", "통신비", "가족곗돈", "적금", "생활비 이월", "급여",
                             "비상금 이체", "여행비"]
    banks: list[str] = ["신한은행", "하나은행", "키움증권"]


class Balance(rx.State):
    balance: int = 0

    def handle_submit(self, form_data: dict):
        form_data["price"] = self.convert_str_to_int(form_data["price"])
        self.validate_form_data(form_data)

        actions = form_data["actions"]
        # 가계부 최초 작성시 잔액은 0
        if self.balance is None and actions == "수입":
            self.balance = form_data['price']
        elif actions == "수입":
            self.balance += form_data['price']
        elif actions == "지출":
            self.balance -= form_data['price']
        else:
            raise ValueError(f"invalid situation occurs: {form_data} | balance: {self.balance}")

    def validate_form_data(self, form_data: dict):
        if not isinstance(form_data["price"], int):
            raise TypeError(f"price must be integer not {type(form_data['price'])}")

    def convert_str_to_int(self, price: str):
        try:
            return int(price)
        except ValueError:
            raise ValueError(f"Cannot convert it to integer. form(`price`) dtype is {type(price)}")
