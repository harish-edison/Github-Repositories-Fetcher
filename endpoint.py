from flask import Flask, render_template, request, Response
import csv
import psycopg2
import io

app = Flask(__name__)

# Route for the index page with a download button
@app.route('/')
def index():
    return render_template('download.html')

# Route for the endpoint to download the CSV file
@app.route('/download_csv', methods=['POST'])
def download_csv():
    # Get user input from the form
    hostname = request.form['hostname']
    port = request.form['port']
    db_name = request.form['db_name']
    username = request.form['username']
    password = request.form['password']

    # Connect to PostgreSQL
    conn = psycopg2.connect(
            dbname=db_name,
            user=username,
            password=password,
            host=hostname,
            port=port
        )
    cursor = conn.cursor()

    # Fetch data from owners and repositories tables
    cursor.execute('''
        SELECT o.owner_id, o.owner_name, COALESCE(o.owner_email, ''), r.repo_id, r.repo_name, r.status, r.stars_count
        FROM owners o
        INNER JOIN repositories r ON o.owner_id = r.owner_id
        ''')
    data = cursor.fetchall()

    # Create a CSV file in memory
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Owner ID', 'Owner Name', 'Owner Email', 'Repo ID', 'Repo Name', 'Status', 'Stars Count'])
    writer.writerows(data)

    # Prepare response with CSV file
    output.seek(0)
    return Response(output, mimetype='text/csv', headers={'Content-Disposition': 'attachment;filename=repo_data.csv'})

if __name__ == '__main__':
    app.run(debug=True)
