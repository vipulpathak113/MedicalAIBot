import streamlit as st
from components.chat_ui import render_chat_ui
from memory import ChatMemory
from llm_connect_memory import qa_chain

# Constants
CSS = """
    <style>
        /* Button styling */
        .stButton > button {
            border-radius: 20px;
            background-color: #2e7d32;
            color: white;
            padding: 0.25rem 0.75rem;
            font-size: 0.875rem;
            margin: 0;
            height: auto;
            line-height: 1.5;
        }
        
        /* Main container */
        .main-container {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 1rem;
            padding: 1rem;
        }
        
        /* Input styling */
        .stTextInput > div > div > input {
            border-radius: 20px;
            padding-left: 20px;
        }
    </style>
"""

HEADER = """
    <div class="main-container">
        <div style='text-align: center; flex-grow: 1;'>
            <h1>🏥 Medical Assistant Bot</h1>
            <p style='font-size: 1.2em; color: #666;'>Your AI-powered healthcare companion</p>
        </div>
    </div>
"""

AUTO_FOCUS_JS = """
    <script>
        function setFocus() {
            var input = window.parent.document.querySelector('input[type=text]');
            if (input) {
                input.focus();
            }
        }
        setFocus();
        setTimeout(setFocus, 100);
        const observer = new MutationObserver(() => {
            setFocus();
        });
        observer.observe(window.parent.document.body, {
            childList: true,
            subtree: true
        });
    </script>
"""

def init_session_state():
    """Initialize all session state variables"""
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = ChatMemory()
    if "input_key" not in st.session_state:
        st.session_state.input_key = "user_input_1"
    if "spinner_placeholder" not in st.session_state:
        st.session_state.spinner_placeholder = st.empty()

def clear_input():
    """Toggle input key to clear input field"""
    st.session_state.input_key = "user_input_2" if st.session_state.input_key == "user_input_1" else "user_input_1"

def reset_chat():
    """Reset chat history and input"""
    st.session_state.chat_history = ChatMemory()
    clear_input()
    st.rerun()

def handle_user_input(user_message):
    """Process user input and generate response"""
    try:
        output = qa_chain.invoke({"query": user_message})
        return output.get("result", "Sorry, I couldn't generate a response.")
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

def handle_input():
    """Handle input submission"""
    if st.session_state[st.session_state.input_key]:
        user_message = st.session_state[st.session_state.input_key]
        st.session_state.chat_history.add_message("user", user_message)
        
        with st.session_state.spinner_placeholder:
            with st.spinner("Generating response..."):
                response = handle_user_input(user_message)
                if response:
                    st.session_state.chat_history.add_message("bot", response)
        clear_input()

def render_ui():
    """Render all UI components"""
    # Add CSS
    st.markdown(CSS, unsafe_allow_html=True)
    
    # Add header
    st.markdown(HEADER, unsafe_allow_html=True)
    
    # Add sidebar reset button
    with st.sidebar:
        if st.button("🔄 Reset Chat", key="reset_btn"):
            reset_chat()
    
    # Render chat history
    render_chat_ui(st.session_state.chat_history)
    
    # Add input field
    with st.container():
        st.text_input(
            "Type your message:", 
            key=st.session_state.input_key,
            on_change=handle_input
        )
    
    # Add spinner placeholder
    with st.container():
        st.session_state.spinner_placeholder = st.empty()
    
    # Add auto-focus JavaScript
    st.components.v1.html(AUTO_FOCUS_JS, height=0)

def main():
    """Main application entry point"""
    init_session_state()
    render_ui()

if __name__ == "__main__":
    main()
