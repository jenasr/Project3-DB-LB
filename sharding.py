# Sharding - Sam Valls, Joseph
    # Make 4 DB's
        # Split games into 3 DB's
            # This split will be done using the user_id
            # user_id is currently an int, and we need to change it to UUID
                #This is the part we need to learn about
            # To perform the split us modulo 3 on the user_id
                # dataset1: SELECT * FROM games WHERE user_id % 3 = 0; game_records1
                # dataset2: SELECT * FROM games WHERE user_id % 3 = 1; game_records2
                # dataset3: SELECT * FROM games WHERE user_id % 3 = 2; game_records3
                    # Create a new database: make a table using dataseti
        # Then we make a single database containing users
            # dataset4: Select * FROM users
                # Create a new database: make a table using dataset4
                # user_profiles
        # After shardin is implemented, the microservice must be adjusted based
        # on the database split


# Do you want us to select from the origianl databse and shard that? Or use inserts?
    # If we do, do it the first way, should we ba able to make the single db first and the the 3 from it?
# Are we supposed to change the original tables to use UUID and then shard them using modulo 3?
# How do views change?

# Load Balancing
    #Harrold, Kevin

# Procfile
