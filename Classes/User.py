class User:
    def __init__(
            self,
            user_id,
            first_name,
            second_name,
            last_name,
            image,
            city,
            department,
            position,
            office_phone,
            email,
            achievements

    ):
        self.user_id = user_id
        self.first_name = first_name
        self.second_name = second_name
        self.last_name = last_name
        self.image = image
        self.city = city
        self.department = department
        self.position = position
        self.office_phone = office_phone
        self.email = email
        self.achievements = achievements