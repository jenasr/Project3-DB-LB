# Sharding - Sam Valls, Joseph
    # Make 4 DB's
        # Split games into 3 DB's
            # This split will be done using the user_id
            # user_id is currently an int, and we need to change it to UUID
                # This is the part we need to learn about
                #insert a whole new column
                # use python to create uuid. Insert it into a db
            # To perform the split use modulo 3 on the user_id
        # Add uuid's
        """    ALTER TABLE users ADD unique_id 'UUID'
                Each of the uuid id's will be initialized to NULL we must intialize each one:
                the_tuples = SELECT * from users
                user_id_dict = {}
                for t in the_tuples:
                    uuid = <use python to generate uuid>
                    UPDATE users SET unique_id = uuid WHERE user_id = t[0]
                    user_id_dict[t[0]] = uuid
                    db.commit()
                ALTER TABLE games ADD user_unique_id 'UUID'
                    the_tuples = SELECT * FROM games
                    for t in the_tuples:
                        UPDATE games SET user_unique_id = user_id_dict[t[0]] WHERE user_id = t[0]
                        db.commit()

                        """
                # dataset1: SELECT * FROM games WHERE user_unique_id % 3 = 0; game_records1
                # dataset2: SELECT * FROM games WHERE user_unique_id % 3 = 1; game_records2
                # dataset3: SELECT * FROM games WHERE user_unique_id % 3 = 2; game_records3
                    # Create a new database: make a table using dataseti
        # Then we make a single database containing users
            # dataset4: Select * FROM users
                # Create a new database: make a table using dataset4
                # user_profiles
        # After shardin is implemented, the microservice must be adjusted based
        # on the database split

# How do views change?
    # No need to change, must place views inside each db.


# Load Balancing
    #Harrold, Kevin

# Procfile
