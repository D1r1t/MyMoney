import streamlit as st
import pandas    as pd

import calendar

import core.service.currency_processing       as serv_cur_proc 
import core.service.account_processing        as serv_acc_proc 
import core.service.categories_processing     as serv_cat_proc
import core.service.exchange_rates_processing as serv_ex_rat_proc 
import core.service.moves_processing          as serv_mov_proc
import core.service.views_processing          as serv_view_proc

from core.exceptions import *
from datetime        import date, datetime

st.set_page_config(page_title="Маи деняки", layout="wide")

accounts   = serv_acc_proc.get_all_accounts()
categories = serv_cat_proc.get_all_categories()

# ===CURRENCY_DIALOG===

@st.dialog("Основная валюта уже существует")
def replace_main_currency_dialog():
    st.write(
        "Основная валюта уже существует. "
        "Хотите переназначить основную валюту?"
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Да"):
            serv_cur_proc.create_new_currency(name, (is_main == "Да"), True)
            st.session_state["replace_main"] = True
            st.rerun()
        
    with col2:
        if st.button("Нет"):
            st.session_state["replace_main"] = False
            st.rerun()

# ===SIDEBAR===

with st.sidebar:
    st.title("Навигация")

    st.markdown("---")

    page = st.radio("Навигация", ["Главная","Счета","Валюты","Категории","Курсы"])

    st.markdown("---")

# ===MAIN===

if page == "Главная":
    st.title("Главная")

    st.subheader("Аналитика")

    today = date.today()

    start = today.replace(day=1)

    last_day = calendar.monthrange(today.year, today.month)[1]
    end = today.replace(day=last_day)

    analitic_dates = st.date_input(
        "Период аналитики",
        value=(start, end)
    )

    if len(analitic_dates) == 2:
        start_date, end_date = analitic_dates

        with st.expander("По дням (общая)", expanded = False):
            table_data = serv_view_proc.get_analitic_by_day(start_date, end_date)
            df = pd.DataFrame([
                {
                    "Дата": row.rec_date.strftime("%d.%m.%Y"),
                    "Счет": row.acc_name,
                    "Категория": row.cat_name,
                    "Доходы план": row.income_plan,
                    "Доходы факт": row.income_fact,
                    "Расхождение доходов": row.income_deviation,
                    "Расходы план": row.expense_plan,
                    "Расходы факт": row.expense_fact,
                    "Расхождения расходов": row.expense_deviation
                } 
                for row in table_data
            ])

            height = 40 + 36 * len(df)
            
            st.dataframe(df, use_container_width=True, height = height)

        with st.expander("По категориям"):
            table_data = serv_view_proc.get_expenses_by_day(start_date, end_date)
            df = pd.DataFrame([
                {
                    "Дата": row.rec_date.strftime("%d.%m.%Y"),
                    "Счет": row.acc_name,
                    "Категория": row.cat_name,
                    "Траты": row.expense
                } 
                for row in table_data
            ])

            pivot_df = df.pivot_table(
                index = "Дата",   
                columns = ["Счет","Категория"],       
                values = "Траты",            
                aggfunc = "sum",             
                fill_value = 0             
            )

            pivot_df = pivot_df.reset_index()

            height = 40 + 36 * len(df)

            # выбираем только числовые колонки для суммирования
            numeric_cols = pivot_df.select_dtypes(include="number").columns

            # итого по колонкам (строка внизу)
            total_row = pivot_df[numeric_cols].sum(axis=0)
            total_row["Дата"] = "Итого"
            total_row.update(pivot_df[numeric_cols].sum(axis=0).to_dict())
            
            pivot_df = pd.concat([pivot_df, pd.DataFrame([total_row])], ignore_index=True)
            
            

            st.dataframe(pivot_df, use_container_width=True, height = height)


    st.subheader("Транзакции")

    moves_dates = st.date_input(
        "Период транзакций",
        value=(start, end)
    )

    with st.expander("Обработка транзакций", expanded = False):
        with st.form("add_move"):
            if len(moves_dates) == 2:
                start_date, end_date = moves_dates

                moves      = serv_mov_proc.get_moves(start_date, end_date)
                #accounts   = serv_acc_proc.get_all_accounts()
                #categories = serv_cat_proc.get_all_categories()

                if moves:
                    df = pd.DataFrame([
                        {
                            "_id":         m.id,
                            "Плановая":    m.plan_rec,
                            "Дата":        m.rec_date,
                            "Счёт":        m.account.acc_name,
                            "Вид":         "Приход" if m.move_is_income else "Расход",
                            "Категория":   m.category.cat_name,
                            "Сумма":       m.move_sum,
                            "Комментарий": m.comment
                        } for m in moves   
                    ])
                else:
                    df = pd.DataFrame(
                        columns = [
                            "_id",
                            "Плановая",
                            "Дата",
                            "Счёт",
                            "Вид",
                            "Категория",
                            "Сумма",
                            "Комментарий"
                        ]
                    ) 

                    #df = df.set_index("_id")

                editable_df = st.data_editor(
                    df,
                    width               = 'content',
                    num_rows            = "dynamic",
                    column_config={
                        "_id":         st.column_config.Column(disabled=True),  # скрываем от редактирования
                        "Плановая":    st.column_config.CheckboxColumn("Плановая"),
                        "Дата":        st.column_config.DateColumn("Дата"),
                        "Вид":         st.column_config.SelectboxColumn(
                                        "Вид", options=["Приход", "Расход"]
                                    ),
                        "Счёт":        st.column_config.SelectboxColumn(
                                        "Счёт", options=[a.acc_name for a in accounts]
                                    ),
                        "Категория":   st.column_config.SelectboxColumn(
                                        "Категория", options=[c.cat_name for c in categories]
                                    ),
                        "Сумма":       st.column_config.NumberColumn(
                                        "Сумма", min_value=0.0, format="%.2f"
                                    ),
                        "Комментарий": st.column_config.TextColumn(
                                        "Комментарий",
                                        max_chars = 200,
                                        default = ""
                                    )                                
                    },
                    hide_index=True
                )

                submitted = st.form_submit_button("Сохранить")

                if submitted:
                    try:
                        for _, row in editable_df.iterrows():
                            if pd.isna(row["_id"]):
                                serv_mov_proc.create_new_move(
                                    plan_rec       = row["Плановая"], 
                                    rec_date       = row["Дата"], 
                                    account        = serv_acc_proc.get_account_by_name(row["Счёт"]), 
                                    move_is_income = row["Вид"] == "Приход", 
                                    category       = serv_cat_proc.get_category_by_name(row["Категория"]), 
                                    move_sum       = row["Сумма"], 
                                    comment        = row["Комментарий"]
                                )
                            else:
                                serv_mov_proc.update_move(
                                    id             = int(row["_id"]),
                                    plan_rec       = row["Плановая"], 
                                    rec_date       = row["Дата"], 
                                    account        = serv_acc_proc.get_account_by_name(row["Счёт"]), 
                                    move_is_income = row["Вид"] == "Приход", 
                                    category       = serv_cat_proc.get_category_by_name(row["Категория"]), 
                                    move_sum       = row["Сумма"], 
                                    comment        = row["Комментарий"]
                                )

                        original_id_set = set(df[df["_id"].notna()]["_id"].astype(int).tolist())
                        new_id_set      = set(editable_df[editable_df["_id"].notna()]["_id"].astype(int).tolist())

                        deleted_id_set  = original_id_set - new_id_set
                        for deleted_id in deleted_id_set:
                            serv_mov_proc.delete_move(deleted_id)

                        st.success("Транзакции успешно изменены!")
                        st.rerun()
                    except MoveDoesntExists as e:
                        st.error(str(e))
                    except MovesError as e:
                        st.error(str(e))
                    except AppError as e:
                        st.error(str(e))


    #with st.expander("Периодические транзакции", expanded = False):


# ===ACCOUNTS===

elif page == "Счета":
    st.title("Счета")

    st.subheader("Текущие счета")

    df = pd.DataFrame([
            {
                "Счет": row.acc_name,
                "Валюта": row.currency.cur_name
            } 
            for row in accounts
        ])

    height = 40 + 36 * len(df)

    st.dataframe(df, use_container_width=True, height = height)

    with st.expander("Добавить новый счет", expanded=False):
        with st.form("add_account", clear_on_submit=True):
            currecies = serv_cur_proc.get_all_currencies()

            name = st.text_input("Наименование счета")

            selected_currency = st.selectbox(
                "Валюта",
                options = currecies,
                format_func = lambda c: c.cur_name
            )

            submitted = st.form_submit_button("Создать")

            if submitted and name:
                try:
                    serv_acc_proc.create_new_account(name, selected_currency)
                    st.success(f"Счет '{name}' успешно создан!")
                    st.rerun()
                except AccountAlreadyExistsError as e:
                    st.error(str(e))
                except AccountError as e:
                    st.error(str(e))
                except AppError as e:
                    st.error(str(e))

            
# ===CURRENCY===

elif page == "Валюты":
    st.title("Валюты")

    with st.expander("Добавить новую валюту", expanded=False):
        with st.form("add_currency"):
            name = st.text_input("Наименование валюты")
            is_main = st.selectbox("Является основной", ["Да", "Нет"])

            submitted = st.form_submit_button("Создать")
            if submitted and name:
                try:
                    serv_cur_proc.create_new_currency(name, (is_main == "Да"))
                    st.success(f"Валюта '{name}' успешно добавлена!")
                    #st.rerun()
                except CurrencyMainAlreadyExistsError as e:
                    replace_main_currency_dialog()
                    #st.error(str(e))
                except CurrencyAlreadyExistsError as e:
                    st.error(str(e)) 
                except CurrencyError as e:
                    st.error(str(e))  
                except AppError as e:
                    st.error(str(e))         

# ===CATEGORIES===

elif page == "Категории":
    st.title("Категории")

    st.subheader("Текущие категории")

    df = pd.DataFrame([
            {
                "Категория": row.cat_name,
            } 
            for row in categories
        ])

    height = 40 + 36 * len(df)

    st.dataframe(df, use_container_width=True, height = height)

    with st.expander("Добавить новую категорию", expanded=False):
        with st.form("add_category", clear_on_submit=True):
            name = st.text_input("Наименование категории")

            submitted = st.form_submit_button("Создать")
            if submitted and name:
                try:
                    serv_cat_proc.create_new_category(name)
                    st.success(f"Категория '{name}' успешно добавлена!")
                    st.rerun()
                except CategoryAlreadyExistsError as e:
                    st.error(str(e)) 
                except AppError as e:
                    st.error(str(e))

# ===EXCHANGE_RATES===

elif page == "Курсы":
    st.title("Курсы")

    with st.expander("Добавить новый курс", expanded=False):
        with st.form("add_exchange_rate"):
            currecies = serv_cur_proc.get_all_currencies()

            date = st.date_input("Дата курса") 

            selected_main_currency = st.selectbox(
                "Расчетная валюта",
                options = currecies,
                format_func = lambda c: c.cur_name
            )

            selected_sub_currency = st.selectbox(
                "Расчитываемая валюта",
                options = currecies,
                format_func = lambda c: c.cur_name
            )

            rare = st.number_input("Курс")

            submitted = st.form_submit_button("Добавить")
            if submitted:

                if selected_main_currency.id == selected_sub_currency.id:
                    st.warning("Расчетная и расчитываемая валюты одинаковы. Замените одну из них")
                elif rare <= 0:
                    st.warning("Курс не может быть меньше или равен 0") 
                else:
                    try:
                        serv_ex_rat_proc.create_new_exchange_rate(
                            date, 
                            selected_main_currency,
                            selected_sub_currency,
                            rare
                        )
                        st.success(f"Новый курс для пары {selected_main_currency.cur_name}-{selected_sub_currency.cur_name} успешно добавлен!")
                    except ExchangeRatesError as e:
                        st.error(str(e)) 
                    except AppError as e:
                        st.error(str(e))
