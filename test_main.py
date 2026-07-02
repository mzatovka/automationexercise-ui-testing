from playwright.sync_api import sync_playwright
import time
import pytest
from playwright.sync_api import expect

@pytest.fixture(scope="session")
def create_browser():
    with sync_playwright() as driver:
        browser = driver.chromium.launch(headless=False) # headless=False говорит об открытии браузера , если будет true браузер не откроется, все будет проходить в фоновом режиме 
        
        yield browser 
        
        browser.close()
        
@pytest.fixture()
def page(create_browser):
    new_page = create_browser.new_page()
    new_page.goto("https://automationexercise.com/")
    
    yield new_page
    
    new_page.close()
    

@pytest.fixture()
def new_user(create_browser):
    
    page = create_browser.new_page()
    page.goto("https://automationexercise.com/")
    page_login_btn = page.locator("//a[text()=' Signup / Login']")
    page_login_btn.click()

    time.sleep(3)
    
    new_email = f"test{time.time()}@gmail.com"
    
    page.locator("[data-qa='signup-name']").fill('mariaa')        
    page.locator("[data-qa='signup-email']").fill(new_email)
    
    signup_btn = page.locator("[data-qa='signup-button']")
    signup_btn.click()

    time.sleep(3)
    # метод для радио кнопок
    page.locator("#id_gender1").check()

    time.sleep(3)

    enter_password = page.locator('#password')
    enter_password.fill('password1234')
    
    # select option - работа с выпадающим списком 
    page.locator('#days').select_option('4')
    page.locator('#months').select_option('June')
    page.locator('#years').select_option('1996')
    
    page.get_by_label("Sign up for our newsletter!").check()
    
    page.locator('#first_name').fill('max')
    page.locator('#last_name').fill('zatovka')
    page.locator('[data-qa = "company"]').fill('freelance')
    page.locator('[data-qa = "address"]').fill('Grodno')
    page.locator('#country').select_option('United States')
    page.locator('[data-qa = "state"]').fill('Grodno')
    page.locator('[data-qa = "city"]').fill('Grodno')
    page.locator('[data-qa = "zipcode"]').fill('zipcode')
    page.locator('[data-qa = "mobile_number" ]').fill('375336200282')
    
    page.locator('[data-qa = "create-account"]').click()

    return{
        
        'email': new_email,
        'password': 'password1234'
        
    }
    
    


def test_case1(page):
    
    assert page.title() == 'Automation Exercise'
    
    page_login_btn = page.locator("//a[text()=' Signup / Login']")
    page_login_btn.click()

    time.sleep(3)

    enter_name = page.locator("[data-qa='signup-name']")
    enter_name.fill('mariaa')        
    
    enter_email = page.locator("[data-qa='signup-email']")
    current_time = time.time()
    enter_email.fill(f'mariaa{current_time}@gmail.com')
    
    signup_btn = page.locator("[data-qa='signup-button']")
    signup_btn.click()

    time.sleep(3)
    # метод для радио кнопок
    page.locator("#id_gender1").check()

    time.sleep(3)

    enter_password = page.locator('#password')
    enter_password.fill('maksim')
    
    # select option - работа с выпадающим списком 
    page.locator('#days').select_option('4')
    page.locator('#months').select_option('June')
    page.locator('#years').select_option('1996')
    
    page.get_by_label("Sign up for our newsletter!").check()
    
    page.locator('#first_name').fill('max')
    page.locator('#last_name').fill('zatovka')
    page.locator('[data-qa = "company"]').fill('freelance')
    page.locator('[data-qa = "address"]').fill('Grodno')
    page.locator('#country').select_option('United States')
    page.locator('[data-qa = "state"]').fill('Grodno')
    page.locator('[data-qa = "city"]').fill('Grodno')
    page.locator('[data-qa = "zipcode"]').fill('zipcode')
    page.locator('[data-qa = "mobile_number" ]').fill('375336200282')
    
    page.locator('[data-qa = "create-account"]').click()
    
    success_message = page.get_by_text('Account Created!').inner_text()
    assert success_message == 'ACCOUNT CREATED!'
    
    page.get_by_text('Continue').click()
    
    time.sleep(3)

    page.locator("a[href='/delete_account']").click()
    delete_message = page.locator('b').inner_text()
    
    assert delete_message.strip().lower() == 'account deleted!'


    time.sleep(3)
    

def test_login(new_user,page):   

    page_login_btn = page.locator("//a[text()=' Signup / Login']")
    page_login_btn.click()
    
    page.locator('[data-qa="login-email"]').fill(new_user['email'])
    page.locator('[data-qa="login-password"]').fill(new_user['password'])
    page.locator('[data-qa="login-button"]').click()
    
    #page.wait_for_url("https://automationexercise.com/")
    
    current_url = page.url
    assert current_url == 'https://automationexercise.com/'
    
    user_status = page.locator('text= Logout')
    assert user_status.is_visible()
    
    page.locator('a[href="/logout"]').click()    
    assert page.url == 'https://automationexercise.com/login'
        
    time.sleep(3)
    
def test_incorrect_password_or_email(page):
       
    page.locator('[data-qa="login-email"]').fill('zatvka@gmail.com')
    page.locator('[data-qa="login-password"]').fill('maks')
    page.locator('[data-qa="login-button"]').click()
    
    user_status = page.locator('text= Your email or password is incorrect!')
    assert user_status.is_visible()

    
    time.sleep(3)
    
    
def test_case4(new_user,page):
       
    assert page.url == "https://automationexercise.com/"
    
    (page.locator("a[href='/login']")).click()
    
    expect(page.get_by_text("Login to your account")).to_be_visible()
    
    page.locator('[data-qa="login-email"]').fill(new_user['email'])
    page.locator('[data-qa="login-password"]').fill(new_user['password'])
    page.locator('[data-qa="login-button"]').click()
    
    expect(page.get_by_text("Logged in as maria")).to_be_visible()    
       
    time.sleep(3)
    page.locator('a[href="/logout"]').click()
    assert page.url == 'https://automationexercise.com/login'

# def test_show_items():
    
#      with sync_playwright() as driver:
#         browser = driver.chromium.launch(headless=False) # headless=False говорит об открытии браузера , если будет true браузер не откроется, все будет проходить в фоновом режиме 
        
#         page = browser.new_page()
#         page.goto("https://automationexercise.com/login")     

#         page.locator('[data-qa="login-email"]').fill('zatvka@gmail.com')
#         page.locator('[data-qa="login-password"]').fill('maksim')
#         page.locator('[data-qa="login-button"]').click()
        
     
     
     
#pytest test_main.py::test_login -v



def test_add_products_to_cart(page):
    
    assert page.url == 'https://automationexercise.com/'
    
    page.locator('a[href="/products"]').click()
    
    
    
    page.locator('a[data-product-id="1"]').first.click()
    page.locator("button.btn-success.close-modal").click()
    page.locator('a[data-product-id="2"]').first.click()
    page.locator("button.btn-success.close-modal").click()
    page.locator('a[href="/view_cart"]').first.click()    

    assert page.locator("tr#product-1").is_visible()
    assert page.locator("tr#product-2").is_visible()
    
    product_1 = page.locator("tr#product-1")
    expect(product_1.locator("td.cart_price")).to_contain_text("Rs. 500")
    expect(product_1.locator("td.cart_quantity button")).to_contain_text("1")
    expect(product_1.locator("td.cart_total")).to_contain_text("Rs. 500")
    
    product_2 = page.locator("tr#product-2")
    expect(product_2.locator("td.cart_price")).to_contain_text("Rs. 400")
    expect(product_2.locator("td.cart_quantity button")).to_contain_text("1")
    expect(product_2.locator("td.cart_total")).to_contain_text("Rs. 400")
    
    
def test_login_before_chekout(new_user,page):
    
    assert page.url == 'https://automationexercise.com/'
    
    (page.locator("a[href='/login']")).click()

    page.locator('[data-qa="login-email"]').fill(new_user['email'])
    page.locator('[data-qa="login-password"]').fill(new_user['password'])
    page.locator('[data-qa="login-button"]').click()
    expect(page.get_by_text("Logged in as mariaa")).to_be_visible()    

    page.locator('a[data-product-id="1"]').first.click()
    page.locator("button.btn-success.close-modal").click()
    page.locator('a[data-product-id="2"]').first.click()
    page.locator("button.btn-success.close-modal").click()
    page.locator('a[data-product-id="3"]').first.click()
    page.locator("button.btn-success.close-modal").click()
    page.locator('a[href="/view_cart"]').first.click()    

    assert page.url == 'https://automationexercise.com/view_cart'
    
    page.locator("a.check_out").click()
    
    page.locator('textarea[name="message"]').fill("buy clothes")   
    page.locator('a[href="/payment"]').click()
    
    page.locator('[data-qa="name-on-card"]').fill("Maksim Zatouka")
    page.locator('[data-qa="card-number"]').fill("123456789")
    page.locator('[data-qa="cvc"]').fill("123")
    page.locator('[data-qa="expiry-month"]').fill("12")
    page.locator('[data-qa="expiry-year"]').fill('2200')
    page.locator('[data-qa="pay-button"]').click()
    
    #expect(page.get_by_text("Your order has been placed successfully!")).to_be_visible()    

    #page.locator('[data-qa="/delete_account"]')

    #expect(page.get_by_text("Account Deleted!")).to_be_visible()    
    


    time.sleep(3)
    
    