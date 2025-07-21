import streamlit as st

import util, model


def main():
    st.header("Модель эффективности")
    opio_name = st.selectbox("Выберите ОПиО", util.get_opio_list(), index=None)

    option_action = {
        0: "Загрузить",
        1: "Создать"
    }
    action = st.segmented_control(
        "Выберите действие",
        options=option_action.keys(),
        format_func=lambda option: option_action[option],
        selection_mode="single",
        width="stretch"
    )

    match action:
        case 0:
            model.load(opio_name)
        case 1:
            model.create(opio_name)

if __name__ == "__main__":
    main()
