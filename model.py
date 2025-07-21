import json
import logging
import redis
import streamlit as st

# r = redis.Redis(
#     host=os.getenv("REDIS_IP"),
#     port=os.getenv("REDIS_PORT"),
#     username=os.getenv("REDIS_USER"),
#     password=os.getenv("REDIS_PASSWORD")
# )

r = redis.Redis(
    host="80.90.187.172",
    port="6379",
    username="default",
    password="J#nr{BkS9Zjh"
)


def create(opio_name: str):
    with st.form("Создание модели эффективности"):
        st.subheader("Введите планы по эффективности на месяц")
        tvo = st.number_input("ТВО", value=0)
        accessories = st.number_input("Аксессуары", value=0)
        fy = st.number_input("ФУ", value=0)
        ga = st.number_input("GA", value=0)
        abonement = st.number_input("Абонементы", value=0)

        data_goal = {
            "tvo": tvo,
            "accessories": accessories,
            "fy": fy,
            "ga": ga,
            "abonement": abonement
        }

        data_result_month = {
            "tvo": 0,
            "accessories": 0,
            "fy": 0,
            "ga": 0,
            "abonement": 0
        }

        if st.form_submit_button("Отправить", type="primary", use_container_width=True):
            logging.info("Create model data and load into memory")
            r.set(f"{opio_name}_goal", json.dumps(data_goal))
            r.set(f"{opio_name}_result_month", json.dumps(data_result_month))
            st.write("send")

def _calculate(opio_name: str, data_result_day: dict) -> dict:
    data_result_month_json = r.get(f"{opio_name}_result_month")
    data_result_month = json.loads(data_result_month_json)

    data_result_month["tvo"] += data_result_day["tvo"]
    data_result_month["accessories"] += data_result_day["accessories"]
    data_result_month["fy"] += data_result_day["fy"]
    data_result_month["ga"] += data_result_day["ga"]
    data_result_month["abonement"] += data_result_day["abonement"]

    return data_result_month

def _send_result(opio_name: str):
    data_goal_json = r.get(f"{opio_name}_goal")
    data_result_month_json = r.get(f"{opio_name}_result_month")

    data_goal = json.loads(data_goal_json)
    data_result_month = json.loads(data_result_month_json)

    data_text = {
        "ТВО": f'{data_goal["tvo"]}\\{data_result_month["tvo"]}\\{abs(data_goal["tvo"] - data_result_month["tvo"])}',
        "Аксессуары": f'{data_goal["accessories"]}\\{data_result_month["accessories"]}\\{data_goal["accessories"] - data_result_month["accessories"]}',
        "ФУ": f'{data_goal["fy"]}\\{data_result_month["fy"]}\\{abs(data_goal["fy"] - data_result_month["fy"])}',
        "GA": f'{data_goal["ga"]}\\{data_result_month["ga"]}\\{abs(data_goal["ga"] - data_result_month["ga"])}',
        "Абонементы": f'{data_goal["abonement"]}\\{data_result_month["abonement"]}\\{abs(data_goal["abonement"] - data_result_month["abonement"])}'
    }

    text = f"{opio_name}\n" + "".join(f"{key} - {value}\n" for key, value in data_text.items())

    st.write(text)

def load(opio_name: str):
    with st.form("Загрузка данных по модели эффективности"):
        st.subheader("Введите данные за прошлый день")
        tvo = st.number_input("ТВО", value=0)
        accessories = st.number_input("Аксессуары", value=0)
        fy = st.number_input("ФУ", value=0)
        ga = st.number_input("GA", value=0)
        abonement = st.number_input("Абонементы", value=0)

        data_result_day = {
            "tvo": tvo,
            "accessories": accessories,
            "fy": fy,
            "ga": ga,
            "abonement": abonement
        }

        if st.form_submit_button("Отправить", type="primary", use_container_width=True):
            logging.info(f"Calculate model effective for opio {opio_name}.")
            data_result_month = _calculate(opio_name, data_result_day)
            r.set(f"{opio_name}_result_month", json.dumps(data_result_month))
            _send_result(opio_name)
