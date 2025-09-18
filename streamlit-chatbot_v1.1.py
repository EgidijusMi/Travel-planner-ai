import streamlit as st
import google.generativeai as genai

# Page config
st.set_page_config(page_title="Travel Planning Assistant", page_icon="✈️")
st.title("✈️ Travel Planning Assistant")

# API Key input
api_key = st.text_input("Enter your Google AI Studio API Key:", type="password")

if api_key:
    genai.configure(api_key=api_key)

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Travel planner section
    st.header("Plan Your Trip")
    with st.form("travel_form"):
        country = st.text_input("Enter the country you will travel to:")
        days = st.number_input("Number of days for your trip:", min_value=1, value=3)
        activities = st.text_input("Enter your preferred activities (comma-separated):")
        submitted = st.form_submit_button("Generate Itinerary")

        if submitted and country and activities:
            prompt = f"""
            Plan a detailed {days}-day travel itinerary for a trip to {country}.
            The traveler is interested in these activities: {activities}.
            For each day, suggest main activities, places to visit, and a brief description.
            """
            try:
                model = genai.GenerativeModel('gemini-2.0-flash-001')
                response = model.generate_content(prompt)
                itinerary = response.text
                
                # Add itinerary to chat history
                st.session_state.messages.append({"role": "assistant", "content": f"Here's your itinerary for {country}:\n\n{itinerary}"})
            except Exception as e:
                st.error(f"Error generating itinerary: {str(e)}")

    # Chat section
    st.header("Chat about your Trip")

    # Display chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat input
    if prompt := st.chat_input("Ask questions about your itinerary or travel plans..."):
        if not api_key:
            st.warning("Please enter your API key.")
        else:
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            try:
                # Get AI response
                model = genai.GenerativeModel('gemini-2.0-flash-001')
                response = model.generate_content(prompt)
                
                # Add AI response to chat history
                ai_message = response.text
                st.session_state.messages.append({"role": "assistant", "content": ai_message})
                with st.chat_message("assistant"):
                    st.markdown(ai_message)

            except Exception as e:
                st.error(f"Error: {str(e)}")

else:
    st.warning("Please enter your API key to start planning your trip.")