"""Рендер мокапов «Гуляй!» из index.html.
Запуск из корня репозитория:  python3 tools/render.py
Нужно: pip install playwright && python3 -m playwright install chromium
Результат: mockups/*.png (рамка iPhone 15, прозрачный фон, 1251×2628)
           mockups/screens/*.png (только экран, 1179×2556)
Свой кадр: python3 tools/render.py "имя|screen=route;arg=r2"
Параметры кадра: screen=input|variants|route|map|replace|walk|saved|pick, arg=id маршрута (r1–r3, f1–f3, s1, s2),
p=индекс точки, sel=выбранный вариант замены, prog=пройдено точек, clock=время в статус-баре, seed=saved."""
import sys, asyncio, pathlib
from playwright.async_api import async_playwright
ROOT = pathlib.Path(__file__).resolve().parent.parent
DEFAULT = ["01_ввод|screen=input", "02_варианты|screen=variants", "03_маршрут|screen=route;arg=r1",
           "04_карта|screen=map;arg=r1;p=1", "05_замена|screen=replace;arg=r1;p=2;sel=0",
           "06_гулять|screen=walk;arg=r1;prog=1;clock=18:32", "07_сохранённые|screen=saved;seed=saved"]
async def main(shots):
    out = ROOT / "mockups"; (out / "screens").mkdir(parents=True, exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch()
        framed = await b.new_page(viewport={"width": 417, "height": 876}, device_scale_factor=3)
        clean = await b.new_page(viewport={"width": 393, "height": 852}, device_scale_factor=3)
        for name, q in (s.split("|", 1) for s in shots):
            q = q.replace(";", "&")
            await framed.goto((ROOT / "tools/frame.html").as_uri() + "?" + q); await framed.wait_for_timeout(700)
            await framed.screenshot(path=str(out / f"{name}.png"), omit_background=True)
            await clean.goto((ROOT / "index.html").as_uri() + "?mock&reset&" + q); await clean.wait_for_timeout(500)
            await clean.screenshot(path=str(out / "screens" / f"{name}.png"))
        await b.close()
asyncio.run(main(sys.argv[1:] or DEFAULT))
