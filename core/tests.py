from django.test import TestCase
from django.shortcuts import reverse
from django.contrib.auth import get_user_model
from .models import Item

#users models 
User = get_user_model()

# Home page
class HomeTestCase(TestCase):
    #test that home page returns a 200
    def test_home_page(self):
        response = self.client.get(reverse('core:home'))
        self.assertEqual(response.status_code, 200)


#post detail
class ItemDetailTestCase(TestCase):
    """ item detail test case """
    def setUp(self):
        """ post detail test case setup """
        #user creation
        self.client.post(reverse('account_signup'),
        {
            'username':'test',
            'email':'test@gmail.com',
            'password1':'TestPassword00',
            'password2':'TestPassword00',
        })
        #get of the user
        self.user = User.objects.get(username='test', email='test@gmail.com')
        #creation of a item
        Item.objects.create(
            title='test item', 
            price=28, 
            image='kdf.png',
            category=('S','Shirt'),
            description='test item description',
            quantity=3,
        )
        #get of the item
        self.item = Item.objects.get(title='test item')

    def test_item_detail_page_return_200(self):
        """ item detail page return 200 status code test case """

        #get of the item id
        item_id = self.item.id
        #request
        response = self.client.get(reverse('core:item_detail',
            kwargs={
                'pk':item_id
            }
        ))
        #test
        self.assertEqual(response.status_code, 200)

    def test_item_detail_page_return_404(self):
        """ test detail page return 200 as request status code """
        #get not exists item id
        not_exists_item_id = self.item.id + 1 
        #make the get request to access the item detail
        response = self.client.get(
            reverse('core:item_detail', 
                kwargs={
                'pk':not_exists_item_id
                }
            )
        )
        print('RESPONSE', dir(response))

        self.assertEqual(response.status_code, 404)

