def check_db(con):
    table_name: str = "STATS"

    fields_list: list[str] = [
        "ID INTEGER PRIMARY KEY AUTOINCREMENT",
        "DATE INT NOT NULL",
        "TECH TEXT NOT NULL",
        "ANY_TIME INT",
        "PAST_MONTH INT",
        "PAST_WEEK INT",
        "PAST_24_HOURS INT",
        "FULL_TIME INT",
        "PART_TIME INT",
        "CONTRACT INT",
        "TEMPORARY INT",
        "VOLUNTEER INT",
        "INTERNSHIP INT",
        "ENTRY_LEVEL INT",
        "ASSOCIATE INT",
        "MID_SENIOR INT",
        "DIRECTOR INT",
        "ON_SITE INT",
        "HYBRID INT",
        "REMOTE INT"
    ]

    con.execute(f"CREATE TABLE IF NOT EXISTS {table_name}({','.join(map(str, fields_list))});")
    con.commit()