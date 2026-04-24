from .cart import Cart

#create conetxt processor so our cart can work for all pages
def cart(request):
    #returns default data
    return{'cart':Cart(request)}