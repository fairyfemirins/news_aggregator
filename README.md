# Community-Driven News & Blog Aggregator

An open-source platform for submitting, tagging, and discussing news/blog articles.

## Features
- **User Submissions**: Submit articles with titles, URLs, descriptions, and tags.
- **Tagging System**: Filter articles by topic (e.g., #tech, #politics).
- **Voting**: Upvote/downvote articles.
- **Comments**: Threaded discussions per article.
- **Responsive UI**: Bootstrap for mobile/desktop compatibility.

## Technical Architecture
- **Backend**: Flask (Python)
- **Database**: SQLite
- **Frontend**: Bootstrap
- **Dependencies**: `flask`, `flask-sqlalchemy`, `flask-bootstrap`, `python-dotenv`

## Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/Femirins/news_aggregator.git
   cd news_aggregator
   ```
2. Install dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
3. Initialize the database:
   ```bash
   python -c "from app import db, app; app.app_context().push(); db.create_all()"
   ```
4. Run the app:
   ```bash
   python app.py
   ```
5. Open `http://localhost:5000` in your browser.

## License
MIT