def select_billing_address(self, billingAddressCompany, billingAddressCountry, billingAddressStateProvince,
                           billingAddressCity, billingAddress1, billingAddress2, billingAddressPostalCode,
                           billingAddressPhoneNumber, billingAddressFaxNumber):
    self.page.locator("#billing-address-select").wait_for(state="visible")
    options = self.page.locator("#billing-address-select option").all_text_contents()
    if options and any("New Address" not in opt for opt in options):
        # Existing address found → select the first one
        existing_value = self.page.locator("#billing-address-select option").first.get_attribute("value")
        self.page.locator("#billing-address-select").select_option(existing_value)
    else:
        # No existing address → select "New Address"
        self.page.locator("#billing-address-select").select_option("New Address")
        # Fill billing details
        self.page.locator("#BillingNewAddress_Company").fill(billingAddressCompany)
        self.page.locator("#BillingNewAddress_CountryId").select_option(label=billingAddressCountry)
        self.page.locator("#BillingNewAddress_StateProvinceId").select_option(label=billingAddressStateProvince)
        self.page.locator("#BillingNewAddress_City").fill(billingAddressCity)
        self.page.locator("#BillingNewAddress_Address1").fill(billingAddress1)
        self.page.locator("#BillingNewAddress_Address2").fill(billingAddress2)
        self.page.locator("#BillingNewAddress_ZipPostalCode").fill(billingAddressPostalCode)
        self.page.locator("#BillingNewAddress_PhoneNumber").fill(billingAddressPhoneNumber)
        self.page.locator("#BillingNewAddress_FaxNumber").fill(billingAddressFaxNumber)
        # Click Continue
        self.page.get_by_role("button", name="Continue").click()


    def update_order_number(self,new_order_number, json_file="Data/Data_1.json"):
        """Append a new order number to the JSON file."""
        if os.path.exists(json_file):
            with open(json_file,"r+") as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = {}
                # Ensure Key exists
                if "order_numbers" not in data:
                    data["order_numbers"] = []
                # Append new order number
                data["order_numbers"].append(str(new_order_number))
                # Rewrite file
                f.seek(0)
                json.dump(data, f, indent=4)
                f.truncate()
        else:
            # Create new file with first order number
            with open(json_file, "w") as f:
                json.dump({"order_numbers":[str(new_order_number)]}, f, indent=4)


    def update_order_number(self, test_case_id, new_order_number, json_file="Data/Data_1.json"):
        """Update the JSON file with order number mapped to test case ID."""
        if os.path.exists(json_file):
            with open(json_file, "r+") as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = {}
                # Ensure key exists
                if "order_numbers" not in data:
                    data["order_numbers"] = {}
                # Update mapping
                data["order_numbers"][test_case_id] = str(new_order_number)
                # Rewrite file
                f.seek(0)
                json.dump(data, f, indent=4)
                f.truncate()
        else:
            # Create new file with first mapping
            with open(json_file, "w") as f:
                json.dump({"order_numbers": {test_case_id: str(new_order_number)}}, f, indent=4)