import re
from playwright.sync_api import expect


def test_user_creates_car_in_browser(page, live_server):
    page.goto(f"{live_server}/cars/new")
    page.locator("#make").fill("Toyota")
    page.locator("#model").fill("Yaris")
    page.locator("#year").fill("2020")
    page.locator("#color").fill("Blue")
    page.locator("#save-button").click()

    expect(page).to_have_url(re.compile(r"/cars/\d+$"))
    expect(page.locator("#car-title")).to_have_text("Toyota Yaris")
    expect(page.locator("#car-model")).to_have_text("Yaris")


def test_user_edits_car_and_change_survives_reload(page, live_server):
    # 1. 创建一台车
    page.goto(f"{live_server}/cars/new")
    page.locator("#make").fill("Honda")
    page.locator("#model").fill("Civic")
    page.locator("#year").fill("2022")
    page.locator("#color").fill("Silver")
    page.locator("#save-button").click()

    # 2. 等待跳到详情页，确认标题显示
    expect(page).to_have_url(re.compile(r"/cars/\d+$"))
    expect(page.locator("#car-title")).to_have_text("Honda Civic")

    # 3. 点编辑链接，进入编辑表单
    page.locator("#edit-link").click()

    # 4. 等待编辑表单加载完成
    expect(page.locator("#page-title")).to_have_text("Edit car")
    expect(page.locator("#save-button")).to_have_text("Save changes")
    # ==========新增这一行！！等待按钮可用==========
    expect(page.locator("#save-button")).to_be_enabled(timeout=8000)

    # 5. 修改车型和年份，先清空输入框
    page.locator("#model").clear()
    page.locator("#model").fill("Accord")
    page.locator("#year").clear()
    page.locator("#year").fill("2023")

    # 6. 点击保存
    page.locator("#save-button").click()

    # 7. 等待跳转回详情页面，增加超时
    expect(page).to_have_url(re.compile(r"/cars/\d+$"), timeout=8000)
    expect(page.locator("#car-title")).to_have_text("Honda Accord", timeout=8000)

    # 8. 刷新页面持久化校验
    page.reload()
    expect(page.locator("#car-title")).to_have_text("Honda Accord", timeout=8000)
    expect(page.locator("#car-model")).to_have_text("Accord", timeout=8000)
    expect(page.locator("#car-year")).to_have_text("2023", timeout=8000)
