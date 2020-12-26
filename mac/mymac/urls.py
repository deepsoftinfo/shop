from django.urls import path
from .import views

urlpatterns = [
    path('',views.index,name="mymachome"),
    path('about/',views.about,name="mymacabout"),
    path('contact/',views.contact,name="mymaccontact"),
    path('login/',views.login,name="login"),
    path('logout/',views.logout,name="logout"),
    path('signup/',views.signup,name="signup"),
    path('tracker/',views.tracker,name="mymactracker"),
    path('search/',views.search,name="mymacsearch"),
    path('productView/<int:myid>',views.productView,name="mymacproductView"),
    path('checkout/<int:myid>/<int:qty>',views.checkout,name="mymaccheckout"),
    path('cart/',views.cart,name="mycart"),
    path('checkout2/<int:myid>/<int:price>',views.checkout2,name="checkout2"),
    path('checkout_all/',views.checkout_all,name="checkout_all"),
    path('handle_request/',views.handle_request,name="handle_request")
    
]





# for backup

# from django.urls import path
# from .import views

# urlpatterns = [
#     path('',views.index,name="mymachome"),
#     path('about/',views.about,name="mymacabout"),
#     path('contact/',views.contact,name="mymaccontact"),
#     path('tracker/',views.tracker,name="mymactracker"),
#     path('search/',views.search,name="mymacsearch"),
#     path('productView/<int:myid>',views.productView,name="mymacproductView"),
#     path('checkout/<int:myid>',views.checkout,name="mymaccheckout"),
#     path('cart/',views.cart,name="mycart"),
#     path('checkout2/<int:myid>',views.checkout2,name="checkout2"),
#     path('checkout_all/',views.checkout_all,name="checkout_all"),
#     path('handle_request/',views.handle_request,name="handle_request")
    
# ]