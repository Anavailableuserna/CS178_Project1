import pymysql
import creds
import pymysql.cursors
import boto3


def get_conn():
    conn = pymysql.connect(
        host=creds.host,
        user=creds.user,
        password = creds.password,
        db=creds.db,
    )
    return conn

def execute_query(query, args=()):
    cur = get_conn().cursor()
    cur.execute(query, args)
    rows = cur.fetchall()
    cur.close()
    return rows


def display_html(rows):
    html = ""
    html += """<table><tr><th>movie_id</th><th>title</th><th>popularity</th></tr>"""
    for r in rows:
        html += "<tr><td>" + str(r[0]) + "</td><td>" + str(r[1]) + "</td><td>" + str(r[2]) + "</td></tr>"
    html += "</table></body>"
    return html
