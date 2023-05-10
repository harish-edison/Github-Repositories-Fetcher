# Github-Repositories-Fetcher
The GitHub Repositories Data Fetcher has 2 functions: 1. Data Fetch and Store 2. Data Download as CSV. This web application can fetch public information of any repository of any user on GitHub and store it in a PostgreSQL or CSV file.

GitHub Repositories Data Fetch API

Languages Used:
Python
Flask
HTML

The Data Fetch and Store involves a web application which takes input from the user, the client id and the client secret obtained from
Github OAuth which helps to get access token from the GitHub API in order to fetch data from GitHub.

The user also inputs his/her PostgreSQL database details through the web application. To make this part secure, we can enable SSL mode
in the PostgreSQL database and enable SSL and 'required' when connecting the database with the Flask application.
The user also enters the username of whose Repositories data, the user wants to fetch.

This information is retrieved by the Github_Repo_Fetcher.py which then fetches data and normalizes it and then stores into 2 tables in 
the database, namely: owners and repositories.

The Data Download as CSV involves a web application which takes input from the user, the PostgreSQL detabase details which is then
retrieved by endpoint.py. This maps the data by first joining the owners and repositories tables on owner_id and then is written as a 
CSV file which is then available for download when the user hits the 'Download CSV' button.

Instructions to run the Project:

Download the Project Folder.

Install all the necessary libraries using pip:
flask
csv
psycopg2
io
requests

PostgreSQL:

Note the details of your PostgreSQL Database:
hostname
port
database name
username
password

Create 2 tables 'owners' and 'repositories' in your database in the following manner:

owners{
    owner_id : bigint NOT NULL PRIMARY KEY;
    owner_name : text;
    owner_email : text;
    UNIQUE (owner_id);
}

repositories{
    repo_id : bigint NOT NULL PRIMARY KEY;
    repo_name : text;
    status : text;
    stars_count : integer;
    owner_id : bigint;
    UNIQUE (repo_id, owner_id);
    FOREIGN KEY(owner_id) 
   REFERENCES owners(owner_id);
}

Functionalities:

To Fetch Repository Data:
1. Open terminal and change directory to the Project folder or Open folder in VSCode and run terminal.
2. To fetch repository data, run Github_Repo_Fetcher.py by typing python Github_Repo_Fetcher.py on the terminal.
3. This will redirect you to index.html on localhost server where you have to give your OAuth Client Secret, OAuth Client ID, PostgreSQL Details and the username whose data you want to fetch and click on Fetch Repository Data.
4. The data will be loaded to your PostgreSQL Database.

To Download Data as CSV:
1. Open terminal and change directory to the Project folder or Open folder in VSCode and run terminal.
2. To download data as CSV, run endpoint.py by typing python endpoint.py on the terminal.
3. This will redirect you to download.html on localhost server where you have to give your PostgreSQL Details and click on Download CSV.
4. The CSV File will be ready for download.
