import psycopg2

ERRORS = 0

usernames = [
        "Liam"
    ]

phone_numbers = [
        '09172101171', '09172101172', '09172101173', '09172101174', '09172101175',
        '09172101176', '09172101177', '09172101178', '09172101179', '09172101180',
        '09172101181', '09172101182', '09172101183', '09172101184', '09172101185',
    ]


# Connect to your PostgreSQL database
conn = psycopg2.connect(
    dbname="postgresql",
    user="admin",
    password="123",
    host="localhost",
    port="5432"
)

# Create a cursor object to execute SQL queries
cur = conn.cursor()

for username in usernames:
    # Define the SQL query to retrieve the first row from the Transaction table
    sql_query = f"""
        SELECT SUM(t.amount)
        FROM charges_transaction t
        INNER JOIN charges_seller s ON t.seller_id = s.id
        WHERE s.username = '{username}';
    """

    # Execute the SQL query
    cur.execute(sql_query)

    # Fetch the first row from the result set
    sum_transaction = cur.fetchone()[0]
    if not sum_transaction:
        sum_transaction = 0


    sql_query = f"""
        SELECT SUM(t.amount)
        FROM charges_innercharge t
        INNER JOIN charges_seller s ON t.seller_id = s.id
        WHERE s.username = '{username}';
    """

    cur.execute(sql_query)

    sum_inner_charge = cur.fetchone()[0]
    if not sum_inner_charge:
        sum_inner_charge = 0

    sql_query = f"""
        SELECT r.credit
        FROM charges_registrationlog r
        INNER JOIN charges_seller s ON r.seller_id = s.id
        WHERE s.username = '{username}';
    """

    cur.execute(sql_query)
    initial_credit = cur.fetchone()[0]

    sql_query = f"""
        SELECT credit
        FROM charges_seller
        WHERE username = '{username}';
    """

    cur.execute(sql_query)
    present_credit = cur.fetchone()[0]

    if present_credit == initial_credit + sum_inner_charge - sum_transaction:
        pass
    else:
        ERRORS += 1
        print(f"Not successful for seller {username}")
        print(initial_credit + sum_inner_charge - sum_transaction)


for phone_number in phone_numbers:
    sql_query = f"""
            SELECT SUM(t.amount)
            FROM charges_transaction t
            INNER JOIN charges_costumer c ON t.costumer_id = c.id
            WHERE c.phone_number = '{phone_number}';
        """


    cur.execute(sql_query)
    sum_transaction = cur.fetchone()[0]
    if not sum_transaction:
        sum_transaction = 0

    sql_query = f"""
            SELECT credit
            FROM charges_costumer
            WHERE phone_number = '{phone_number}';
        """
    cur.execute(sql_query)
    present_credit = cur.fetchone()[0]

    if present_credit == sum_transaction:
        pass
    else:
        ERRORS += 1
        print(f"Not successful for costumer {phone_number}")


print(f"Total errors: {ERRORS}")

# Close the cursor and connection
cur.close()
conn.close()
