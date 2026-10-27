"""Execute separadamente com o servidor em execução; não chama OpenAI no modo demo."""
import os
from playwright.sync_api import sync_playwright, expect

base = os.getenv('TEST_BASE_URL', 'http://127.0.0.1:8000')
with sync_playwright() as p:
    browser = p.chromium.launch()
    for width, height in [(1280, 900), (375, 667)]:
        page = browser.new_page(viewport={'width': width, 'height': height})
        # Fontes externas não são necessárias para validar os fluxos locais.
        page.route('https://fonts.googleapis.com/**', lambda route: route.abort())
        page.route('https://fonts.gstatic.com/**', lambda route: route.abort())
        page.goto(base)
        expect(page.locator('.produto-item')).to_have_count(7)
        page.locator('#chat-toggle').focus()
        page.keyboard.press('Enter')
        expect(page.locator('#chat-input')).to_be_focused()
        page.locator('#chat-input').fill('Qual produto custa menos de R$ 50?')
        page.keyboard.press('Enter')
        expect(page.locator('.chat-assistant')).to_contain_text('15,00')
        box = page.locator('#chat-panel').bounding_box()
        assert box and box['x'] >= 0 and box['x'] + box['width'] <= width
        assert box['y'] >= 0 and box['y'] + box['height'] <= height
        page.keyboard.press('Escape')
        expect(page.locator('#chat-panel')).to_be_hidden()
        expect(page.locator('#chat-toggle')).to_be_focused()
        page.route('**/api/chat', lambda route: route.fulfill(status=503, json={'detail': 'unavailable'}))
        page.locator('#chat-toggle').click()
        page.locator('#chat-input').fill('bolos')
        page.locator('#chat-send').click()
        expect(page.locator('.chat-assistant').last).to_contain_text('indisponível')
        expect(page.locator('.produto-item')).to_have_count(7)
        page.close()
        print(f'PASS: catálogo, chat, teclado e falha da API em {width}×{height}')
    browser.close()
