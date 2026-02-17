import json
import pytest
from playwright.sync_api import Page, expect
from POM.LoginPage import LoginPage
from POM.ShoppingCartPage import ShoppingCartPage

test_data_path = "Data/Data_1.json"
try:
    with open(test_data_path) as f:
        test_data = json.load(f)
        test_data_list = test_data["data"]
except Exception as e:
    print(f"Test data file not found: {test_data_path}")

@pytest.mark.parametrize("test_data_list_items",test_data_list,ids=[item["ID"] for item in test_data_list])
def test_e2e_DemoWebShop(playwright,browserInstance,test_data_list_items):
    loginPage = LoginPage(browserInstance)
    dashBoardPage = loginPage.login(test_data_list_items["Email"],test_data_list_items["Password"])
    dashBoardPage.verifyHeaderLinks(test_data_list_items["Email"])
    dashBoardPage.add_products_from_pages(test_data_list_items["listOfProducts"])
    shoppingCartPage = dashBoardPage.click_shopping_cart_link()
    shoppingCartPage.provide_estimate_shipping_details(test_data_list_items["country"],test_data_list_items["stateProvince"],test_data_list_items["postalCode"])
    checkOutPage = shoppingCartPage.provide_termsAndConditions_checkout()
    checkOutPage.select_billing_address(test_data_list_items["company_checkout"],test_data_list_items["country_checkout"],test_data_list_items["stateProvince_checkout"],test_data_list_items["city_checkout"],test_data_list_items["addr1_checkout"],test_data_list_items["addr2_checkout"],test_data_list_items["postalCode_checkout"],test_data_list_items["phone_checkout"],test_data_list_items["fax_checkout"])
    checkOutPage.select_shipping_address(test_data_list_items["company_checkout"],test_data_list_items["country_checkout"],test_data_list_items["stateProvince_checkout"],test_data_list_items["city_checkout"],test_data_list_items["addr1_checkout"],test_data_list_items["addr2_checkout"],test_data_list_items["postalCode_checkout"],test_data_list_items["phone_checkout"],test_data_list_items["fax_checkout"])
    checkOutPage.select_ShippingMethod(test_data_list_items["shippingMethod"])
    checkOutPage.select_PaymentMethod(test_data_list_items["paymentMethod_Name"],test_data_list_items["CreditCardType"],test_data_list_items["cardHolderName"],test_data_list_items["cardNumber"],test_data_list_items["cardCode"],test_data_list_items["PurchaseOrderNumber"])
    thankYouPage = checkOutPage.confirmOrder()
    thankYouPage.verifyOrderSuccessMessage()
    thankYouPage.verifyOrderNumber()
    thankYouPage.clickContinue_navigateBackTo_DashboardPage()
    #dashBoardPage.click_shopping_cart_link()
    #shoppingCartPage.clear_shopping_cart()


