# Connection to private server's database to execute queries through the bot.
# Put your database credentials in .env

import pymysql, os

env = lambda n: os.environ.get(n)

connection = pymysql.connect(host=env('DBHOST'),
                             user=env('DBUSER'),
                             password=env('DBPASS'),
                             database=env('DBNAME'),
                             autocommit=True,
                             # port=3306 | uncomment to use custom port
                             cursorclass=pymysql.cursors.DictCursor)


def execute(query: str, limit: int = 2000):
    '''
    #### Execute a SQL query in your private server's MySQL database
    Returns fetched data based on data length or "OK" if no data.
    '''
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(query)
            r = cursor.fetchall()
            if len(r) == 0:
                return 'OK'
            if len(r) == 1:
                return r[0]

            multiline_data = '\n\n'.join((str(x) for x in r))
            return multiline_data if len(multiline_data) < limit else multiline_data[:limit-3] + '...'         
            # to not exceed the 2000 character limit of discord
            # 4096 is the limit for embed description so set the limit accordingly

