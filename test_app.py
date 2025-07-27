import streamlit as st

st.title("Secrets Test Page")

# Check if the specific test key exists and is correct
if "TEST_KEY" in st.secrets and st.secrets["TEST_KEY"] == "sk-123456789-this-is-a-safe-temporary-test-key-987654321":
    st.success("SUCCESS: The Streamlit secrets system is working correctly.")
else:
    st.error("FAILURE: The secrets system is not working or the key is incorrect.")
    st.write("Here are the secrets the app can see:")
    st.write(st.secrets.to_dict())