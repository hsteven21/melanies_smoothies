# Import python packages
import streamlit as st
import snowflake.connector
from snowflake.snowpark import Session
from snowflake.snowpark.functions import col

# App title
st.title("🥤 Customize Your Smoothie! 🥤")
st.write("Choose the fruits you want in your custom Smoothie!")

# Input para nombre del pedido
name_on_order = st.text_input("Name on Smoothie:")
if name_on_order:
    st.write("The name on your Smoothie will be:", name_on_order)

# Configurar conexión con Snowflake usando secrets
conn_params = st.secrets["connections"]["snowflake"]
session = Session.builder.configs(conn_params).create()

# DataFrame con opciones de frutas desde Snowflake
my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"))

# Lista de selección limitada a 5 elementos
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    [row["FRUIT_NAME"] for row in my_dataframe.collect()],
    max_selections=5
)

# Botón submit y validaciones adicionales
if st.button("Submit Order"):
    if not name_on_order.strip():
        st.error("❌ Please enter a name for your smoothie.")
    elif not ingredients_list:
        st.error("❌ Please select at least one fruit.")
    else:
        ingredients_string = " ".join(ingredients_list)
        safe_name = name_on_order.replace("'", "''")

        # Crear sentencia insert
        insert_stmt = f"""
            INSERT INTO smoothies.public.orders (ingredients, name_on_order, order_filled)
            VALUES ('{ingredients_string}', '{safe_name}', FALSE)
        """

        # Ejecutar insert en Snowflake
        session.sql(insert_stmt).collect()

        # Mostrar mensaje de éxito
        st.success(f"✅ Your Smoothie is ordered, {name_on_order}!")

