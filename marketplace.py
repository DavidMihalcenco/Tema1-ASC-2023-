"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

import unittest
from threading import Lock
import logging
#from tema import product as product_class

FILE_HANDLER = logging.FileHandler('.log')

class Marketplace:
    """
    Class that represents the Marketplace. It's the central part of the implementation.
    The producers and consumers use its methods concurrently.
    """
    def __init__(self, queue_size_per_producer):
        """
        Constructor

        :type queue_size_per_producer: Int
        :param queue_size_per_producer: the maximum size of a queue associated with each producer
        """
        self.queue_size_per_producer = queue_size_per_producer
        self.cons_cart_list = []
        self.cart_id = 0
        self.producer_id = 0
        self.producer_list = []
        self.register_id_producer_generator_lock = Lock()
        self.register_id_cart_generator_lock = Lock()
        self.all_funtion_lock = Lock()
        self.print_lock = Lock()
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s %(levelname)s %(message)s',
            handlers=[
                FILE_HANDLER
            ]
        )
        # create a logger instance
        self.logger = logging.getLogger('.log')


    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """
        self.producer_list.append([])
        with self.register_id_producer_generator_lock:
            self.producer_id += 1
            self.logger.log(logging.INFO,"Producer with id %d has registred", self.producer_id - 1)
        return self.producer_id - 1

    def publish(self, producer_id, product):
        """
        Adds the product provided by the producer to the marketplace

        :type producer_id: String
        :param producer_id: producer id

        :type product: Product
        :param product: the Product that will be published in the Marketplace

        :returns True or False. If the caller receives False, it should wait and then try again.
        """
        with self.all_funtion_lock :
            if len(self.producer_list[producer_id]) >= self.queue_size_per_producer:
                self.logger.log(logging.INFO,"Product %s cant be added because list is full",
                                 product)
                return False
            self.producer_list[producer_id].append(product)
            self.logger.log(logging.INFO,"Product %s has been added to producer list with id %d",
                             product, producer_id)
        return True

    def new_cart(self):
        """
        Creates a new cart for the consumer

        :returns an int representing the cart_id
        """
        self.cons_cart_list.append([])
        with self.register_id_cart_generator_lock:
            self.cart_id += 1
            self.logger.log(logging.INFO,"Cart with id %d has added", self.cart_id - 1)
        return self.cart_id - 1


    def add_to_cart(self, cart_id, product):
        """
        Adds a product to the given cart. The method returns

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to add to cart

        :returns True or False. If the caller receives False, it should wait and then try again
        """
        with self.all_funtion_lock :
            for produces in self.producer_list:
                if product in produces:
                    produces.remove(product)
                    self.cons_cart_list[cart_id].append(product)
                    self.logger.log(logging.INFO,"Product %s has been added to cart with id %d",
                                     product, cart_id)
                    return True
        self.logger.log(logging.INFO, "Product %s is not available", product)
        return False

    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart
        """
        with self.all_funtion_lock :
            try:
                self.cons_cart_list[cart_id].remove(product)
                self.producer_list[0].append(product)
                self.logger.log(logging.INFO,"Product %s has been removed from cart with id %d",
                                 product, cart_id)
                return True
            except ValueError:
                self.logger.log(logging.INFO,"Product %s dosen't exist in cart with id %d",
                                 product, cart_id)
                return False

    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart
        """
        self.logger.log(logging.INFO,"Cart with id %d finished order",cart_id)
        return self.cons_cart_list[cart_id]

class TestMarketplace(unittest.TestCase):
    """
    Class to test Marketplace
    """

    def setUp(self):
        """
        SetUp function for all parameters
        """
        self.marketplace = Marketplace(5)
        self.product = "Tea(name='Pai Mu Tan', price=9, type='White')"
        self.product_false = "Tea(name='Pai Mu Tan', price=9, type='Black')"

    def test_register_producer(self):
        """
        Testing regisert_producer, add 2 new producers, and check ids
        """
        self.assertEqual(self.marketplace.register_producer(),0)
        self.assertEqual(self.marketplace.register_producer(),1)

    def test_publish(self):
        """
        Testing publish, checking if 5 obiects are created is true, 6 is false
        Marketplace was initialized with 5
        """
        producer_id = self.marketplace.register_producer()
        for _ in range(5):
            self.assertEqual(self.marketplace.publish(producer_id, self.product),True)
        for _ in range(6):
            self.assertEqual(self.marketplace.publish(producer_id, self.product),False)

    def test_new_cart(self):
        """
        Testing new_cart, creating 2 new carts, 2 is not equal because next cart has 
        id 1
        """
        self.assertEqual(self.marketplace.new_cart(),0)
        self.assertNotEqual(self.marketplace.new_cart(),2)

    def test_add_to_cart(self):
        """
        Testing add_to_cart, adding new cart and new producer, then add from producer
        product to cart, because product_F is not added in producer list function return false
        """
        cart_id = self.marketplace.new_cart()
        producer_id = self.marketplace.register_producer()
        self.marketplace.publish(producer_id,self.product)
        self.assertEqual(self.marketplace.add_to_cart(cart_id,self.product),True)
        self.assertEqual(self.marketplace.add_to_cart(cart_id,self.product_false),False)

    def test_remove_from_cart(self):
        """
        Testing remove_from_cart, try to remove a product from cart, because in cart 
        product_f is not added it cant be removed
        """
        cart_id = self.marketplace.new_cart()
        producer_id = self.marketplace.register_producer()

        self.marketplace.publish(producer_id,self.product)
        self.marketplace.add_to_cart(cart_id,self.product)

        self.assertEqual(self.marketplace.remove_from_cart(cart_id, self.product),True)
        self.assertEqual(self.marketplace.remove_from_cart(cart_id, self.product_false),False)

    def test_place_order(self):
        """
        Testing place_order, checking if in list i have 1 product, because i added
        1 product, 2 are false
        """
        producer_id = self.marketplace.register_producer()
        self.marketplace.publish(producer_id,self.product)

        cart_id = self.marketplace.new_cart()
        self.marketplace.add_to_cart(cart_id,self.product)

        order_list = self.marketplace.place_order(cart_id)
        self.assertEqual(len(order_list),1)
        self.assertNotEqual(len(order_list),2)
        assert self.product in order_list
