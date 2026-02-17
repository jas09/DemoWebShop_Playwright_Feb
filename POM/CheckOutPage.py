from cProfile import label

from playwright.sync_api import Page

from POM.ThankYouPage import ThankYouPage


class CheckOutPage:
    def __init__(self,page:Page):
        self.page = page

    def _select_address(self, prefix, company_checkout, country_checkout, stateProvince_checkout, city_checkout, addr1_checkout, addr2_checkout, postalCode_checkout, phone_checkout, fax_checkout):
        """
        Generic helper to select an address (billing or shipping).
        prefix: 'BillingNewAddress' or 'ShippingNewAddress'
        """
        dropdown_id = f"#{prefix.lower().replace('newaddress', '')}-address-select"
        #Check if dropdown exists
        self.page.locator(dropdown_id).wait_for(state="attached")
        self.page.locator(dropdown_id).wait_for(state="visible")
        if self.page.locator(dropdown_id).count()>0:
            # Dropdown is present → either select existing or "New Address"
            self.page.locator(dropdown_id).wait_for(state="visible")
            selected_value = self.page.locator(dropdown_id).input_value()
            #print(f"{prefix} dropdown selected value: {selected_value}")
            if selected_value and selected_value != "New Address":
                #Existing address already selected → just continue
                self.page.get_by_role("button", name="Continue").click()
                return
            else:
                # No existing address → select "New Address"
                self.page.locator(dropdown_id).select_option("New Address")
                self.page.locator(f"#{prefix}_Company").wait_for(state="visible")
                # Fill form only if "New Address" chosen
                self.page.locator(f"#{prefix}_Company").fill(company_checkout)
                self.page.locator(f"#{prefix}_CountryId").select_option(label=country_checkout)
                self.page.locator(f"#{prefix}_StateProvinceId").select_option(label=stateProvince_checkout)
                self.page.locator(f"#{prefix}_City").fill(city_checkout)
                self.page.locator(f"#{prefix}_Address1").fill(addr1_checkout)
                self.page.locator(f"#{prefix}_Address2").fill(addr2_checkout)
                self.page.locator(f"#{prefix}_ZipPostalCode").fill(str(postalCode_checkout))
                self.page.locator(f"#{prefix}_PhoneNumber").fill(str(phone_checkout))
                self.page.locator(f"#{prefix}_FaxNumber").fill(str(fax_checkout))
                self.page.get_by_role("button", name="Continue").click()
                return
        else:
            self.page.locator(f"#{prefix}_Company").fill(company_checkout)
            self.page.locator(f"#{prefix}_CountryId").select_option(label=country_checkout)
            self.page.locator(f"#{prefix}_StateProvinceId").select_option(label=stateProvince_checkout)
            self.page.locator(f"#{prefix}_City").fill(city_checkout)
            self.page.locator(f"#{prefix}_Address1").fill(addr1_checkout)
            self.page.locator(f"#{prefix}_Address2").fill(addr2_checkout)
            self.page.locator(f"#{prefix}_ZipPostalCode").fill(str(postalCode_checkout))
            self.page.locator(f"#{prefix}_PhoneNumber").fill(str(phone_checkout))
            self.page.locator(f"#{prefix}_FaxNumber").fill(str(fax_checkout))
            self.page.get_by_role("button", name="Continue").click()
            return

    def select_billing_address(self, company_checkout,country_checkout,stateProvince_checkout,city_checkout,addr1_checkout,addr2_checkout,postalCode_checkout,phone_checkout,fax_checkout):
        return self._select_address("BillingNewAddress", company_checkout,country_checkout,stateProvince_checkout,city_checkout,addr1_checkout,addr2_checkout,postalCode_checkout,phone_checkout,fax_checkout)

    def select_shipping_address(self, company_checkout,country_checkout,stateProvince_checkout,city_checkout,addr1_checkout,addr2_checkout,postalCode_checkout,phone_checkout,fax_checkout):
        return self._select_address("ShippingNewAddress", company_checkout,country_checkout,stateProvince_checkout,city_checkout,addr1_checkout,addr2_checkout,postalCode_checkout,phone_checkout,fax_checkout)

    def select_ShippingMethod(self,shippingMethod):
        self.page.locator(f"//label[contains(text(),'{shippingMethod}')]").click()
        self.page.locator("input[onclick='ShippingMethod.save()']").click()

    def _fill_credit_card(self, CreditCardType, cardHolderName, cardNumber, cardCode):
        self.page.locator("#CreditCardType").select_option(value=CreditCardType)
        self.page.locator("#CardholderName").fill(cardHolderName)
        self.page.locator("#CardNumber").fill(cardNumber)
        self.page.locator("#CardCode").fill(cardCode)


    def select_PaymentMethod(self,paymentMethod_Name,CreditCardType=None,cardHolderName=None,cardNumber=None,cardCode=None,PurchaseOrderNumber=None):
        self.page.locator("//div[@class='payment-details']").first.wait_for(state="visible")
        paymentMethods = self.page.locator("//div[@class='payment-details']")
        count = paymentMethods.count()
        #print("Found payment options:", count)
        for i in range(count):
            label_text = paymentMethods.nth(i).locator("label").inner_text().strip()
            #print(f"Option {i}: {label_text}")
            if paymentMethod_Name in label_text:
                paymentMethods.nth(i).locator("input").click()
                self.page.locator("input[onclick='PaymentMethod.save()']").click()
                if paymentMethod_Name == "Cash On Delivery (COD) (7.00)":
                    paymentInformation = self.page.locator(".info p").inner_text()
                    assert paymentInformation == "You will pay by COD"
                elif paymentMethod_Name == "Check / Money Order (5.00)":
                    paymentInformation = self.page.locator("//div[@class='info']//td/p[1]").inner_text()
                    assert paymentInformation in "Mail Personal or Business Check, Cashier's Check or money order to:"
                elif paymentMethod_Name == "Credit Card":
                    self._fill_credit_card(CreditCardType, cardHolderName, cardNumber, cardCode)
                elif paymentMethod_Name == "Purchase Order":
                    self.page.locator("#PurchaseOrderNumber").fill(str(PurchaseOrderNumber))
                self.page.locator("input[onclick='PaymentInfo.save()']").wait_for(state="visible")
                self.page.locator("input[onclick='PaymentInfo.save()']").click()
                break

    def confirmOrder(self):
        self.page.locator(".confirm-order-next-step-button").wait_for(state="attached")
        self.page.locator(".confirm-order-next-step-button").click()
        thankYouPage = ThankYouPage(self.page)
        return thankYouPage











