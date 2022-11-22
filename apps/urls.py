from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [ 
    path('',views.index),
    path('insert/',views.insert),
    path('user_login/',views.user_login),
    path('signout/',views.signout,name='signout'),
    path('products',views.products),
    path('admin_login/',views.admin_login),
    path('admin_dash/',views.admin_dash),
    path('admin_logout/',views.admin_logout),
    path('otp/',views.otp),
    path('smslogin',views.smslogin),
    path('admin_userinfo/',views.admin_userinfo),
    path('unblock/<int:id>',views.unblock,name='unblock'),
    path('block/<int:id>',views.block,name='block'),
    path('admin_addproduct/',views.admin_addproduct),
    path('admin_listproduct/',views.admin_listproduct),
    path('updatepro/<int:id>',views.updatepro,name='updatepro'),
    path('deletepro/<int:id>',views.deletepro,name='deletepro'),
    path('admin_addcategory',views.admin_addcategory),
    path('filter_product/<int:id>',views.filter_product, name='filter_product'), 
    path('product_details/<int:id>',views.product_details, name='product_details'), 
    path('add_cart_guest/<int:pid>',views.add_cart_guest, name='add_cart_guest'),
    path('gcart_remove/<int:id>',views.gcart_remove, name='gcart_remove'),
    path('gcart_view/', views.gcart_view, name="gcart_view"),
    path('gcart_update/', views.gcart_update, name="gcart_update"),
    path('apply_coupan/',views.apply_coupan, name='apply_coupan'),
    path('razor_pay/<int:id>', views.razor_pay, name="razor_pay"),
    path('user_order_returned/<id>',views.user_order_returned,name='user_order_returned'),
    path('cart_update/', views.cart_update, name="cart_update"),
    path('user_order_detailed_view/<int:id>',views.user_order_detailed_view, name='user_order_detailed_view'),
    path('payment_methods/<int:order_total>',views.payment_methods, name='payment_methods'), 
    path('payment_confirm/<int:order_total>',views.payment_confirm, name='payment_confirm'), 
    path('payment_complete/', views.payment_complete, name="payment_complete"),
    path('payment_methods_razorpay/<int:id>',views.payment_methods_razorpay, name='payment_methods'),
    path('view_cart/',views.view_cart, name='view_cart'),
    path('add_quantity/<int:id>',views.add_quantity, name='add_quantity'), 
    path('sub_quantity/<int:id>',views.sub_quantity, name='sub_quantity'), 
    path('delete_from_cart/<int:id>',views.delete_from_cart, name='delete_from_cart'),
    path('checkout/',views.checkout,name="checkout"),
    path('add_address/',views.add_address,name="add_address"),
    path('view_wishlist/',views.view_wishlist, name='view_wishlist'),
    path('delete_from_wishlist/<int:id>',views.delete_from_wishlist, name='delete_from_wishlist'),
    path('myprofile/',views.myprofile, name='my_profile'),
    path('address_management/',views.address_management, name='address_management'),
    path('delete_address/<int:id>',views.delete_address, name='delete_address'),
    path('edit_profile/<int:id>',views.edit_profile, name='edit_profile'),
    path('user_order_management/',views.user_order_management, name='user_order_management'),
    path('user_cancel_order/<int:id>',views.user_cancel_order, name='user_cancel_order'), 
    path('download/<int:productID>',views.download, name='download'),
    path('admin_order_management',views.admin_order_management),
    path('filter_order/<str:status>',views.filter_order,name='filter_order'),
    path('admin_cancel_order/<int:id>',views.admin_cancel_order, name='admin_cancel_order'), 
    path('admin_order_detailed_view/<int:id>',views.admin_order_detailed_view, name='admin_order_detailed_view'),
    path('category_offer_management/', views.category_offer_management, name="category_offer_management"),
    path('product_offer_management/', views.product_offer_management, name="product_offer_management"),
    path('view_offers',views.view_offers, name='view_offers'),
    path('delete_category_offer/<int:id>',views.delete_category_offer, name='delete_category_offer'),
    path('delete_product_offer/<int:id>',views.delete_product_offer, name='delete_product_offer'),
    path('coupan_management/', views.coupan_management, name="coupan_management"),
    path('view_coupan',views.view_coupan, name='view_coupan'),
    path('delete_coupan_offer/<int:id>',views.delete_coupan_offer, name='delete_coupan_offer'),
    path('view_category',views.view_category),
    path('delete_category/<int:id>',views.delete_category),
    path('sales',views.sales_report_date, name='sales'),
    path('export_to_pdf',views.export_to_pdf, name='export_to_pdf'),
    path('export_to_excel',views.export_to_excel, name='export_to_excel'),
    

  

   
   

    

    
    
    

   
   
    

   
   
    
  



]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)