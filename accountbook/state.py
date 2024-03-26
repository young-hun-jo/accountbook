import reflex as rx

from datetime import datetime
from pytz import timezone

from accountbook.logger import logger


class UserInputs(rx.State):
    actions: list[str] = ["지출", "수입"]
    years: list[str] = ['2024', '2025', '2026']
    months: list[str] = [str(i) for i in range(1, 13)]
    categories: list[str] = ["생활비", "데이트비", "문화비", "법인카드", "모임비", "교통카드캐시백",
                             "병원비", "공과금", "캐시백", "통신비", "가족곗돈", "적금", "생활비 이월", "급여",
                             "비상금 이체", "여행비"]
    banks: list[str] = ["신한은행", "하나은행", "키움증권"]


class History(rx.Model, table=True):
    actions: str
    years: int
    months: int
    categories: str
    banks: str
    price: int
    reason: str
    created_at: datetime = datetime.now(timezone("Asia/Seoul"))


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

        self.add_history_to_db(
            form_data['actions'],
            int(form_data['years']),
            int(form_data['months']),
            form_data['categories'],
            form_data['banks'],
            form_data['price'],
            form_data['reason']
        )

    def validate_form_data(self, form_data: dict):
        if not isinstance(form_data["price"], int):
            raise TypeError(f"price must be integer not {type(form_data['price'])}")

    def convert_str_to_int(self, price: str):
        try:
            return int(price)
        except ValueError:
            raise ValueError(f"Cannot convert it to integer. form(`price`) dtype is {type(price)}")

    def add_history_to_db(self, actions, years, months, categories, banks, price, reason):
        # db_url = "sqlite:///accountbook.db"
        row = History(
            actions=actions,
            years=years,
            months=months,
            categories=categories,
            banks=banks,
            price=price,
            reason=reason
        )
        with rx.session() as session:
            session.add(row)
            session.commit()
            logger.info(f"finish inserting row to db - ROW:{row.actions, row.years, row.months, row.categories, row.banks, row.price, row.reason, row.created_at}")
