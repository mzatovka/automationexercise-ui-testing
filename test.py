
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