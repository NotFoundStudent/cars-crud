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

    # 4. 等待编辑表单加载完成（JS会把按钮文字改成"Save changes"）
    expect(page.locator("#page-title")).to_have_text("Edit car")
    expect(page.locator("#save-button")).to_have_text("Save changes")

    # 5. 修改车型和年份
    page.locator("#model").fill("Accord")
    page.locator("#year").fill("2023")
    page.locator("#save-button").click()

    # 6. 等待跳回详情页，标题变成新名字
    expect(page.locator("#car-title")).to_have_text("Honda Accord")

    # 7. 刷新页面，确认修改持久化
    page.reload()
    expect(page.locator("#car-title")).to_have_text("Honda Accord")
    expect(page.locator("#car-model")).to_have_text("Accord")
    expect(page.locator("#car-year")).to_have_text("2023")
