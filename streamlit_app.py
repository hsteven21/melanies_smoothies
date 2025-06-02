# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# App title
st.title("🥤 Customize Your Smoothie! 🥤")
st.write("Choose the fruits you want in your custom Smoothie!")

# Input para nombre del pedido
name_on_order = st.text_input("Name on Smoothie:")
if name_on_order:
    st.write("The name on your Smoothie will be:", name_on_order)

# Conectar sesión a Snowflake - Se actualizará posteriormente para conexión externa
# session = get_active_session()  # Esto ya no se usa

# Nota: En Streamlit externo necesitarás configurar la conexión manualmente luego

# DataFrame (Pendiente configurar conexión)
# my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"))
my_dataframe = None  # temporal, deberás configurarlo con conexión externa a Snowflake

if my_dataframe:
    ingredients_list = st.multiselect(
        "Choose up to 5 ingredients:",
        my_dataframe.collect(),
        max_selections=5
    )
else:
    ingredients_list = []

# Botón submit y validaciones adicionales
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
        
        # Ejecutar insert (pendiente de implementar con conexión externa)
        st.success(f"✅ Your Smoothie is ordered, {name_on_order}!")
        #
