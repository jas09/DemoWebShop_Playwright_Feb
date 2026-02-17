import json
import logging
import os.path
class Utilities:

    def __init__(self,page):
        self.page = page
        self.page_locator_map = {
            'Books': "//ul[@class='top-menu']//a[normalize-space(text())='Books']",
            'Computers': "//ul[@class='top-menu']//a[normalize-space(text())='Computers']",
            'Desktops': {
                'hover': "//ul[@class='top-menu']//a[normalize-space(text())='Computers']",
                'click': "//ul[@class='top-menu']//a[normalize-space(text())='Desktops']"
            },
            'Notebooks': {
                'hover': "//ul[@class='top-menu']//a[normalize-space(text())='Computers']",
                'click': "//ul[@class='top-menu']//a[normalize-space(text())='Notebooks']"
            },
            'Accessories': {
                'hover': "//ul[@class='top-menu']//a[normalize-space(text())='Computers']",
                'click': "//ul[@class='top-menu']//a[normalize-space(text())='Accessories']"
            },
            'Electronics': "//ul[@class='top-menu']//a[normalize-space(text())='Electronics']",
            'Camera': {
                'hover': "//ul[@class='top-menu']//a[normalize-space(text())='Electronics']",
                'click': "//ul[@class='top-menu']//a[normalize-space(text())='Camera, photo']"
            },
            'Cell phones': {
                'hover': "//ul[@class='top-menu']//a[normalize-space(text())='Electronics']",
                'click': "//ul[@class='top-menu']//a[normalize-space(text())='Cell phones']"
            },
            'Apparel & Shoes': "//ul[@class='top-menu']//a[normalize-space(text())='Apparel & Shoes']",
            'Digital downloads': "//ul[@class='top-menu']//a[normalize-space(text())='Digital downloads']",
            'Jewelry': "//ul[@class='top-menu']//a[normalize-space(text())='Jewelry']",
            'Gift Cards': "//ul[@class='top-menu']//a[normalize-space(text())='Gift Cards']"
        }

    def update_order_number(self, new_order_number, json_file="Data/Data.json"):
        """Append a new order number to the JSON file."""
        if os.path.exists(json_file):
            with open(json_file, "r+") as f:
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
                json.dump({"order_numbers": [str(new_order_number)]}, f, indent=4)


    def _go_to_page(self, page_name):
        if not page_name:
            return
        locator_info = self.page_locator_map.get(page_name)
        logging.basicConfig(level=logging.WARNING)
        try:
            if isinstance(locator_info, dict):
                self.page.locator(locator_info["hover"]).hover()
                self.page.locator(locator_info["click"]).click()
            else:
                if page_name in ("Computers","Electronics"):
                    self.page.locator(locator_info).hover()
                self.page.locator(locator_info).click()
        except Exception as e:
            logging.warning(f"Failed clicking mapped locator for page '{page_name}'")
        # fallback: try clicking a link whose text equals the page_name
        try:
            self.page.get_by_text(page_name).click()
        except Exception:
            logging.warning(f"Could not navigate to page '{page_name}'")

    def _click_product_on_current_page(self, desired_product):
        """Find product title elements on current page and click it's corresponding to add button."""
        desired = desired_product.strip()
        productTitles = self.page.locator("h2.product-title > a").all()
        # map title -> index
        title_to_index = {}
        for idx, elem in enumerate(productTitles, start=1):
            try:
                title_text = elem.inner_text().strip()
            except Exception:
                title_text = ""
            title_to_index[title_text] = idx
        # try exact match first
        idx = title_to_index.get(desired)
        if not idx:
            # try case-insensitive match
            for t, i in title_to_index.items():
                if t.lower() == desired.lower():
                    idx = i
                    break
        if idx:
            try:
                #self.page.locator("//*[@class='add-info'])[{idx}]//input[@value='Add to cart']").click()
                self.page.locator(f"(//*[@class='add-info'])[{idx}]//input[@value='Add to cart']").click()
                return True
            except Exception as e:
                logging.warning(f"Click failed for product '{desired}' at index {idx}: {e}")
                return False
        else:
            logging.warning(f"Product '{desired}' not found on this page.")
            return False


    def add_products_from_pages(self, page_product_pairs):
        if isinstance(page_product_pairs, str):
            page_product_pairs = [p.strip() for p in page_product_pairs.split(',') if p.strip()]

        for pair in page_product_pairs:
            if ':' in pair:
                page,product = [s.strip() for s in pair.split(':',maxsplit=1)]
                #Navigate to page
                self._go_to_page(page)
                found = self._click_product_on_current_page(product)
                if not found:
                    logging.warning(f"Could not find product '{product}' on page '{page}'")
            else:
                product = pair.strip()
                found = self._click_product_on_current_page(product)
                if not found:
                    logging.warning(f"Could not find product '{product}' on current page and no page specified")

    # generic function to remove products from shopping cart
    def clear_shopping_cart(self):
        """Removes all products from the shopping cart."""
        remove_buttons = self.page.locator("//input[@name='removefromcart']").all()
        if not remove_buttons:
            logging.warning("Shopping cart is already empty.")
            return
        for btn in remove_buttons:
            btn.click()
            logging.debug("Clicked remove button for one item.")
        self.page.locator("//input[@name='updatecart']").click()

