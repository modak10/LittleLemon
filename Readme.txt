Little Lemon API paths for peer review

GET     /
GET     /restaurant/menu/
POST    /restaurant/menu/                 (Token authentication required)
GET     /restaurant/menu/<id>/
PUT     /restaurant/menu/<id>/             (Token authentication required)
PATCH   /restaurant/menu/<id>/             (Token authentication required)
DELETE  /restaurant/menu/<id>/             (Token authentication required)

GET     /restaurant/bookings/              (Token authentication required)
POST    /restaurant/bookings/              (Token authentication required)
GET     /restaurant/bookings/<id>/         (Token authentication required)
PUT     /restaurant/bookings/<id>/         (Token authentication required)
PATCH   /restaurant/bookings/<id>/         (Token authentication required)
DELETE  /restaurant/bookings/<id>/         (Token authentication required)

POST    /restaurant/auth/register/
POST    /restaurant/auth/login/
POST    /restaurant/auth/logout/            (Token authentication required)
POST    /restaurant/auth/token/
GET     /admin/
