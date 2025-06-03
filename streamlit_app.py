import streamlit as st
import requests
import pandas as pd
from snowflake.snowpark import Session
from snowflake.snowpark.functions import col

# Título de la aplicación
st.title("🥤 Customize Your Smoothie! 🥤")
st.write("Choose the fruits you want in your custom Smoothie!")

# Nombre del pedido
name_on_order = st.text_input("Name on Smoothie:")
if name_on_order:
    st.write("The name on your Smoothie will be:", name_on_order)

# Conexión a Snowflake usando secrets.toml
conn = st.connection("snowflake")
session = conn.session()

# Obtener opciones de fruta desde Snowflake
my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME")).collect()
fruit_options = [row["FRUIT_NAME"] for row in my_dataframe]

# Multiselección limitada a 5 frutas
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    fruit_options,
    max_selections=5
)

# Botón para realizar pedido con validaciones
if st.button("Submit Order"):
    if not name_on_order.strip():
        st.error("❌ Please enter a name for your smoothie.")
    elif not ingredients_list:
        st.error("❌ Please select at least one fruit.")
    else:
        ingredients_string = " ".join(ingredients_list)
        safe_name = name_on_order.replace("'", "''")

        insert_stmt = f"""
            INSERT INTO smoothies.public.orders (ingredients, name_on_order, order_filled)
            VALUES ('{ingredients_string}', '{safe_name}', FALSE)
        """

        session.sql(insert_stmt).collect()
        st.success(f"✅ Your Smoothie is ordered, {name_on_order}!")

# Mostrar información nutricional para cada fruta elegida
if ingredients_list:
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        
        # Añadir título para cada fruta
        st.subheader(f"{fruit_chosen} Nutrition Information")
        
        # Llamada a API con validación
        smoothiefroot_response = requests.get(f"https://my.smoothiefroot.com/api/fruit/{fruit_chosen}")
        
        if smoothiefroot_response.status_code == 200:
            sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
        else:
            st.error(f"❌ Nutrition information for {fruit_chosen} is not available.")
