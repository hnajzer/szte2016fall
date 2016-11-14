curl -v \
	-H "Content-Type: application/json" \
	--data '{"username":"kacsa2", "password":{"$gt": ""} }' \
	localhost:5000/users/json_login_user
