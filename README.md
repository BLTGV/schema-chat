# Schema Chat

A Streamlit-based chat interface for analyzing database schemas using LangChain and GPT-4. This tool helps developers and database administrators explore and understand database schemas through natural language conversations.

## Features

- Interactive chat interface for database schema analysis
- Support for PostgreSQL and MySQL databases
- Maintains conversation context across queries
- Real-time SQL query execution and explanation
- Secure credential handling
- Comprehensive schema inspection capabilities

## Prerequisites

- Python 3.11 or higher
- OpenAI API key
- Access to a PostgreSQL or MySQL database

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/BLTGV/schema-chat.git
   cd schema-chat
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Unix/MacOS
   # or
   venv\Scripts\activate  # On Windows
   ```

3. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and add your OpenAI API key.

## Usage

1. Start the application:
   ```bash
   streamlit run app.py
   ```

2. In the sidebar, enter your database connection details:
   - Select database type (PostgreSQL/MySQL)
   - Enter host, port, database name
   - Provide username and password

3. Click "Connect" to establish the database connection

4. Start chatting with the AI about your database schema!

## Example Queries

- "List all tables in the database"
- "Describe the structure of the users table"
- "What foreign key relationships exist?"
- "Show me the indexes on the orders table"
- "Explain the relationship between customers and orders"

## Security Notes

- Database credentials are only stored in memory during the session
- The .env file containing your OpenAI API key should never be committed to version control
- Use appropriate database user permissions

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
