from flask import Flask, render_template, request
import requests
import psycopg2

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def fetch_repo_data():
    # Get user input from the form
    client_id = request.form['client_id']
    client_secret = request.form['client_secret']
    hostname = request.form['hostname']
    port = request.form['port']
    db_name = request.form['db_name']
    username = request.form['username']
    password = request.form['password']
    github_username = request.form['github_username']

    # Make API request to fetch data from GitHub API
    url = f'https://api.github.com/users/{github_username}/repos'
    headers = {'Authorization': f'client_id {client_id}, client_secret {client_secret}'}
    response = requests.get(url, headers=headers)

    # Check response status code and parse JSON response
    if response.status_code == 200:
        repo_data = response.json()
    else:
        error_message = f'Failed to fetch data from GitHub API. Status code: {response.status_code}'
        return render_template('index.html', error_message=error_message)

    # Connect to PostgreSQL database
    conn = psycopg2.connect(
        host=hostname,
        port=port,
        dbname=db_name,
        user=username,
        password=password
    )

    # Create a cursor object to interact with the database
    cur = conn.cursor()

    # Loop through repo data and insert into PostgreSQL database
    for repo in repo_data:
        # Extract data from repo data
        owner_id = repo['owner']['id']
        owner_name = repo['owner']['login']
        owner_email = repo['owner']['email'] if 'email' in repo['owner'] else None
        repo_id = repo['id']
        repo_name = repo['name']
        status = 'public' if repo['private'] is False else 'private'
        stars_count = repo['stargazers_count']

        # Prepare SQL queries to normalize and store data in database
        # Insert owner data into owners table
        owner_sql = "INSERT INTO owners (owner_id, owner_name, owner_email) VALUES (%s, %s, %s) ON CONFLICT (owner_id) DO UPDATE SET owner_name = EXCLUDED.owner_name, owner_email = EXCLUDED.owner_email"
        cur.execute(owner_sql, (owner_id, owner_name, owner_email))

        # Insert repository data into repositories table
        repo_sql = "INSERT INTO repositories (repo_id, repo_name, status, stars_count, owner_id) VALUES (%s, %s, %s, %s, %s) ON CONFLICT (repo_id, owner_id) DO UPDATE SET repo_name = EXCLUDED.repo_name, status = EXCLUDED.status, stars_count = EXCLUDED.stars_count"
        cur.execute(repo_sql, (repo_id, repo_name, status, stars_count, owner_id))

    # Commit the changes and close the cursor and connection
    conn.commit()
    cur.close()
    conn.close()

    success_message = "Data has been stored in the PostgreSQL database successfully!"
    return render_template('index.html', success_message=success_message)


if __name__ == '__main__':
    app.run(debug=True)
