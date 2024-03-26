import reflex as rx
from sqlmodel import create_engine

from accountbook.logger import logger
from accountbook.state import UserInputs, Balance


def create_history_table():
    sqlite_filename = "accountbook.db"
    sqlite_url = f"sqlite:///{sqlite_filename}"
    engine = create_engine(sqlite_url, echo=True)
    rx.Model.metadata.create_all(engine)
    logger.info(f"successfully create database and table({sqlite_url})")


def index() -> rx.Component:
    # create table
    create_history_table()
    return rx.vstack(
        rx.form(
            rx.vstack(
                rx.heading("영훈의 가계부"),
                rx.select(placeholder="지출/수입", name="actions", items=UserInputs.actions),
                rx.select(placeholder="연도", name="years", items=UserInputs.years),
                rx.select(placeholder="월", name="months", items=UserInputs.months),
                rx.select(placeholder="카테고리", name="categories", items=UserInputs.categories),
                rx.select(placeholder="은행종류", name="banks", items=UserInputs.banks),
                rx.input(placeholder="금액", name="price"),
                rx.input(placeholder="지출/수입 내용", name="reason"),
                rx.button("제출", type="submit")
            ),
            on_submit=Balance.handle_submit,
            reset_on_submit=False
        ),
        rx.divider(),
        rx.heading("가계부 현재 잔액"),
        rx.text(Balance.balance.to_string())
    )


app = rx.App()
app.add_page(index)
