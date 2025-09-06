#!/usr/bin/env python3
"""
Basic Chat Example for Luminis AI Library Assistant

This example demonstrates how to integrate the chat functionality
into your application using the REST API.

Requirements:
- Backend server running on http://localhost:8000
- OpenAI API key configured
- User authentication (optional for basic chat)
"""

import requests
import json
import time
from typing import Dict, List, Optional


class LuminisChatClient:
    """Simple client for interacting with Luminis AI Library Assistant"""

    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.chat_history: List[Dict] = []

    def send_message(self, message: str, user_id: Optional[str] = None) -> Dict:
        """
        Send a message to the chat API

        Args:
            message: The user's message
            user_id: Optional user ID for authentication

        Returns:
            API response with chat response
        """
        url = f"{self.base_url}/api/chat"

        payload = {"message": message, "user_id": user_id, "chat_history": self.chat_history}

        headers = {"Content-Type": "application/json"}

        try:
            response = self.session.post(url, json=payload, headers=headers)
            response.raise_for_status()

            result = response.json()

            # Store in chat history
            self.chat_history.append({"role": "user", "content": message, "timestamp": time.time()})
            self.chat_history.append(
                {"role": "assistant", "content": result.get("response", ""), "timestamp": time.time()}
            )

            return result

        except requests.exceptions.RequestException as e:
            return {"error": f"Request failed: {str(e)}"}

    def get_chat_history(self) -> List[Dict]:
        """Get the current chat history"""
        return self.chat_history

    def clear_history(self):
        """Clear the chat history"""
        self.chat_history = []

    def health_check(self) -> bool:
        """Check if the API is healthy"""
        try:
            response = self.session.get(f"{self.base_url}/api/health")
            return response.status_code == 200
        except:
            return False


def main():
    """Example usage of the LuminisChatClient"""

    print("🤖 Luminis AI Library Assistant - Basic Chat Example")
    print("=" * 60)

    # Initialize client
    client = LuminisChatClient()

    # Check if API is available
    if not client.health_check():
        print("❌ Error: Backend API is not available!")
        print("Please make sure the backend server is running on http://localhost:8000")
        return

    print("✅ Backend API is available!")
    print("\n💬 Starting chat session...")
    print("Type 'quit' to exit, 'clear' to clear history, 'history' to see chat history")
    print("-" * 60)

    while True:
        try:
            # Get user input
            user_input = input("\n👤 You: ").strip()

            if user_input.lower() == 'quit':
                print("👋 Goodbye!")
                break

            elif user_input.lower() == 'clear':
                client.clear_history()
                print("🧹 Chat history cleared!")
                continue

            elif user_input.lower() == 'history':
                history = client.get_chat_history()
                if not history:
                    print("📝 No chat history yet.")
                else:
                    print("📝 Chat History:")
                    for i, msg in enumerate(history):
                        role = "👤 You" if msg["role"] == "user" else "🤖 Assistant"
                        print(f"  {i+1}. {role}: {msg['content'][:100]}...")
                continue

            elif not user_input:
                continue

            # Send message to API
            print("🤖 Assistant: ", end="", flush=True)
            response = client.send_message(user_input)

            if "error" in response:
                print(f"❌ Error: {response['error']}")
            else:
                assistant_response = response.get("response", "No response received")
                print(assistant_response)

        except KeyboardInterrupt:
            print("\n\n👋 Chat interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Unexpected error: {str(e)}")


def example_requests():
    """Example of making direct API requests"""

    print("\n🔧 Direct API Request Examples:")
    print("-" * 40)

    # Example 1: Health check
    print("1. Health Check:")
    try:
        response = requests.get("http://localhost:8000/api/health")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   Error: {e}")

    # Example 2: Send a chat message
    print("\n2. Chat Message:")
    try:
        payload = {"message": "Hello! Can you recommend a good book about Python programming?", "chat_history": []}
        response = requests.post(
            "http://localhost:8000/api/chat", json=payload, headers={"Content-Type": "application/json"}
        )
        print(f"   Status: {response.status_code}")
        result = response.json()
        print(f"   Response: {result.get('response', 'No response')[:100]}...")
    except Exception as e:
        print(f"   Error: {e}")


if __name__ == "__main__":
    # Run the interactive chat
    main()

    # Show direct API examples
    example_requests()
