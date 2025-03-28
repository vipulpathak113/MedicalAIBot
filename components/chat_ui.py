import streamlit as st

# Constants for styling
CHAT_STYLES = {
    "container": """
        <div style='display: flex; flex-direction: column;'>
    """,
    "user": {
        "wrapper": "display: flex; justify-content: flex-start; margin: 10px;",
        "message": "background-color: #e6f7ff; padding: 10px; border-radius: 10px; color: black; max-width: 70%;",
        "name": "You"
    },
    "bot": {
        "wrapper": "display: flex; justify-content: flex-end; margin: 10px;",
        "message": "background-color: #d9f7be; padding: 10px; border-radius: 10px; color: black; max-width: 70%;",
        "name": "MediBot"
    }
}

def create_message_html(message: dict) -> str:
    """
    Create HTML for a single chat message
    
    Args:
        message (dict): Message dictionary containing sender and text
        
    Returns:
        str: Formatted HTML string for the message
    """
    style = CHAT_STYLES["user"] if message["sender"] == "user" else CHAT_STYLES["bot"]
    
    return f"""
        <div style='{style["wrapper"]}'>
            <div style='{style["message"]}'>
                <strong>{style["name"]}:</strong> {message['text']}
            </div>
        </div>
    """

def render_chat_ui(chat_memory):
    """
    Render the chat UI with message history
    
    Args:
        chat_memory: Chat memory object containing message history
    """
    # Start chat container
    st.markdown(CHAT_STYLES["container"], unsafe_allow_html=True)
    
    # Render each message
    for message in chat_memory.get_history():
        st.markdown(
            create_message_html(message),
            unsafe_allow_html=True
        )
    
    # Close chat container
    st.markdown("</div>", unsafe_allow_html=True)