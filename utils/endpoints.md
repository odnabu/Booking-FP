# API Endpoints

| Method(s) | Path | View |
|-----------|------|------|
| <span style='color:#2ecc71'>GET</span> <span style='color:#f1c40f'>POST</span> | `api/v1/users/^$` | `apps.users.views.UserViewSet` |
| <span style='color:#2ecc71'>GET</span> <span style='color:#f1c40f'>POST</span> | `api/v1/users/^\.(?P<format>[a-z0-9]+)/?$` | `apps.users.views.UserViewSet` |
| <span style='color:#2ecc71'>GET</span> <span style='color:#3498db'>PUT</span> <span style='color:#7f8c8d'>PATCH</span> <span style='color:#e74c3c'>DELETE</span> | `api/v1/users/^(?P<pk>[^/.]+)/$` | `apps.users.views.UserViewSet` |
| <span style='color:#2ecc71'>GET</span> <span style='color:#3498db'>PUT</span> <span style='color:#7f8c8d'>PATCH</span> <span style='color:#e74c3c'>DELETE</span> | `api/v1/users/^(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$` | `apps.users.views.UserViewSet` |
| <span style='color:#7f8c8d'>ANY</span> | `api/v1/users/` | `rest_framework.routers.view` |
| <span style='color:#7f8c8d'>ANY</span> | `api/v1/users/<drf_format_suffix:format>` | `rest_framework.routers.view` |
| <span style='color:#2ecc71'>GET</span> <span style='color:#f1c40f'>POST</span> | `api/v1/addresses/^$` | `apps.addresses.views.AddressViewSet` |
| <span style='color:#2ecc71'>GET</span> <span style='color:#f1c40f'>POST</span> | `api/v1/addresses/^\.(?P<format>[a-z0-9]+)/?$` | `apps.addresses.views.AddressViewSet` |
| <span style='color:#2ecc71'>GET</span> <span style='color:#3498db'>PUT</span> <span style='color:#7f8c8d'>PATCH</span> <span style='color:#e74c3c'>DELETE</span> | `api/v1/addresses/^(?P<pk>[^/.]+)/$` | `apps.addresses.views.AddressViewSet` |
| <span style='color:#2ecc71'>GET</span> <span style='color:#3498db'>PUT</span> <span style='color:#7f8c8d'>PATCH</span> <span style='color:#e74c3c'>DELETE</span> | `api/v1/addresses/^(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$` | `apps.addresses.views.AddressViewSet` |
| <span style='color:#7f8c8d'>ANY</span> | `api/v1/addresses/` | `rest_framework.routers.view` |
| <span style='color:#7f8c8d'>ANY</span> | `api/v1/addresses/<drf_format_suffix:format>` | `rest_framework.routers.view` |
| <span style='color:#2ecc71'>GET</span> <span style='color:#f1c40f'>POST</span> | `api/v1/offers/^$` | `apps.offers.views.OfferViewSet` |
| <span style='color:#2ecc71'>GET</span> <span style='color:#f1c40f'>POST</span> | `api/v1/offers/^\.(?P<format>[a-z0-9]+)/?$` | `apps.offers.views.OfferViewSet` |
| <span style='color:#2ecc71'>GET</span> <span style='color:#3498db'>PUT</span> <span style='color:#7f8c8d'>PATCH</span> <span style='color:#e74c3c'>DELETE</span> | `api/v1/offers/^(?P<pk>[^/.]+)/$` | `apps.offers.views.OfferViewSet` |
| <span style='color:#2ecc71'>GET</span> <span style='color:#3498db'>PUT</span> <span style='color:#7f8c8d'>PATCH</span> <span style='color:#e74c3c'>DELETE</span> | `api/v1/offers/^(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$` | `apps.offers.views.OfferViewSet` |
| <span style='color:#f1c40f'>POST</span> | `api/v1/offers/^(?P<pk>[^/.]+)/toggle_active/$` | `apps.offers.views.OfferViewSet` |
| <span style='color:#f1c40f'>POST</span> | `api/v1/offers/^(?P<pk>[^/.]+)/toggle_active\.(?P<format>[a-z0-9]+)/?$` | `apps.offers.views.OfferViewSet` |
| <span style='color:#7f8c8d'>ANY</span> | `api/v1/offers/` | `rest_framework.routers.view` |
| <span style='color:#7f8c8d'>ANY</span> | `api/v1/offers/<drf_format_suffix:format>` | `rest_framework.routers.view` |
| <span style='color:#2ecc71'>GET</span> <span style='color:#f1c40f'>POST</span> | `api/v1/bookings/^$` | `apps.bookings.views.BookingViewSet` |
| <span style='color:#2ecc71'>GET</span> <span style='color:#f1c40f'>POST</span> | `api/v1/bookings/^\.(?P<format>[a-z0-9]+)/?$` | `apps.bookings.views.BookingViewSet` |
| <span style='color:#2ecc71'>GET</span> | `api/v1/bookings/^active/$` | `apps.bookings.views.BookingViewSet` |
| <span style='color:#2ecc71'>GET</span> | `api/v1/bookings/^active\.(?P<format>[a-z0-9]+)/?$` | `apps.bookings.views.BookingViewSet` |
| <span style='color:#2ecc71'>GET</span> | `api/v1/bookings/^completed/$` | `apps.bookings.views.BookingViewSet` |
| <span style='color:#2ecc71'>GET</span> | `api/v1/bookings/^completed\.(?P<format>[a-z0-9]+)/?$` | `apps.bookings.views.BookingViewSet` |
| <span style='color:#2ecc71'>GET</span> | `api/v1/bookings/^landlord/$` | `apps.bookings.views.BookingViewSet` |
| <span style='color:#2ecc71'>GET</span> | `api/v1/bookings/^landlord\.(?P<format>[a-z0-9]+)/?$` | `apps.bookings.views.BookingViewSet` |
| <span style='color:#2ecc71'>GET</span> <span style='color:#3498db'>PUT</span> <span style='color:#7f8c8d'>PATCH</span> <span style='color:#e74c3c'>DELETE</span> | `api/v1/bookings/^(?P<pk>[^/.]+)/$` | `apps.bookings.views.BookingViewSet` |
| <span style='color:#2ecc71'>GET</span> <span style='color:#3498db'>PUT</span> <span style='color:#7f8c8d'>PATCH</span> <span style='color:#e74c3c'>DELETE</span> | `api/v1/bookings/^(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$` | `apps.bookings.views.BookingViewSet` |
| <span style='color:#f1c40f'>POST</span> | `api/v1/bookings/^(?P<pk>[^/.]+)/cancel/$` | `apps.bookings.views.BookingViewSet` |
| <span style='color:#f1c40f'>POST</span> | `api/v1/bookings/^(?P<pk>[^/.]+)/cancel\.(?P<format>[a-z0-9]+)/?$` | `apps.bookings.views.BookingViewSet` |
| <span style='color:#f1c40f'>POST</span> | `api/v1/bookings/^(?P<pk>[^/.]+)/cancel/$` | `apps.bookings.views.BookingViewSet` |
| <span style='color:#f1c40f'>POST</span> | `api/v1/bookings/^(?P<pk>[^/.]+)/cancel\.(?P<format>[a-z0-9]+)/?$` | `apps.bookings.views.BookingViewSet` |
| <span style='color:#f1c40f'>POST</span> | `api/v1/bookings/^(?P<pk>[^/.]+)/confirm/$` | `apps.bookings.views.BookingViewSet` |
| <span style='color:#f1c40f'>POST</span> | `api/v1/bookings/^(?P<pk>[^/.]+)/confirm\.(?P<format>[a-z0-9]+)/?$` | `apps.bookings.views.BookingViewSet` |
| <span style='color:#7f8c8d'>ANY</span> | `api/v1/bookings/` | `rest_framework.routers.view` |
| <span style='color:#7f8c8d'>ANY</span> | `api/v1/bookings/<drf_format_suffix:format>` | `rest_framework.routers.view` |
| <span style='color:#2ecc71'>GET</span> <span style='color:#f1c40f'>POST</span> | `api/v1/reviews/^$` | `apps.reviews.views.ReviewViewSet` |
| <span style='color:#2ecc71'>GET</span> <span style='color:#f1c40f'>POST</span> | `api/v1/reviews/^\.(?P<format>[a-z0-9]+)/?$` | `apps.reviews.views.ReviewViewSet` |
| <span style='color:#2ecc71'>GET</span> | `api/v1/reviews/^offer/(?P<offer_id>[^/.]+)/$` | `apps.reviews.views.ReviewViewSet` |
| <span style='color:#2ecc71'>GET</span> | `api/v1/reviews/^offer/(?P<offer_id>[^/.]+)\.(?P<format>[a-z0-9]+)/?$` | `apps.reviews.views.ReviewViewSet` |
| <span style='color:#2ecc71'>GET</span> <span style='color:#3498db'>PUT</span> <span style='color:#7f8c8d'>PATCH</span> <span style='color:#e74c3c'>DELETE</span> | `api/v1/reviews/^(?P<pk>[^/.]+)/$` | `apps.reviews.views.ReviewViewSet` |
| <span style='color:#2ecc71'>GET</span> <span style='color:#3498db'>PUT</span> <span style='color:#7f8c8d'>PATCH</span> <span style='color:#e74c3c'>DELETE</span> | `api/v1/reviews/^(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$` | `apps.reviews.views.ReviewViewSet` |
| <span style='color:#7f8c8d'>ANY</span> | `api/v1/reviews/` | `rest_framework.routers.view` |
| <span style='color:#7f8c8d'>ANY</span> | `api/v1/reviews/<drf_format_suffix:format>` | `rest_framework.routers.view` |
| <span style='color:#7f8c8d'>ANY</span> | `api/v1/home/` | `apps.views.hello_user` |
| <span style='color:#7f8c8d'>ANY</span> | `api/v1/registration/` | `apps.users.views.view` |
| <span style='color:#7f8c8d'>ANY</span> | `api/v1/login/` | `apps.users.views.view` |
| <span style='color:#7f8c8d'>ANY</span> | `api/v1/logout/` | `apps.users.views.view` |
| <span style='color:#7f8c8d'>ANY</span> | `get-token/` | `rest_framework.authtoken.views.view` |
| <span style='color:#7f8c8d'>ANY</span> | `api/token/` | `rest_framework_simplejwt.views.view` |
| <span style='color:#7f8c8d'>ANY</span> | `api/token/refresh/` | `rest_framework_simplejwt.views.view` |
| <span style='color:#7f8c8d'>ANY</span> | `schema/` | `drf_spectacular.views.view` |
| <span style='color:#7f8c8d'>ANY</span> | `swagger/` | `drf_spectacular.views.view` |
| <span style='color:#7f8c8d'>ANY</span> | `redoc/` | `drf_spectacular.views.view` |