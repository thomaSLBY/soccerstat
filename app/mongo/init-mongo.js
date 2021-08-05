db.createUser(
    {
        user: "mongodbuser",
        pwd: "mongodbpassword",
        roles: [
            {
                role: "readWrite",
                db: "flaskdb"
            }
        ]
    }
)