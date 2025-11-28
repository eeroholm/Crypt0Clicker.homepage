import pygame, time, sys, textwrap, os
os.environ["PYGBAG"] = "1"
pygame.init()
WIDTH, HEIGHT = 900, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Crypt0 Clicker")
FONT = pygame.font.SysFont("Courier", 22)
BIGFONT = pygame.font.SysFont("Courier", 30)
SMALLFONT = pygame.font.SysFont("Courier", 16)
CLOCK = pygame.time.Clock()
BLACK = (0,0,0)
GREEN = (0,255,0)
LIGHT_GREEN = (140,255,140)
crypto = 0.0
givecrypto = 0.1
cryptominers = 0.5
computerlevel = 1
achievements = []
globalprice = 5.0
gp_growth = 1.011
GP_COST = {
    "income": 3,
    "miner": 4,
    "computer": 15,
    "datacenter": 25,
    "hack": 100
}

EFFECTS = {
    "income": 1.5,
    "miner": 1.8,
    "computer": 2.0,
    "datacenter": 3.0,
    "hack": 4.0
}
ACHIEVEMENT_COST = 1_000_000
achievement_name = "The J. V."
achievement_unlocked = False
class Button:
    def __init__(self, text, y, action):
        self.text = text
        self.y = y
        self.action = action
        self.active_since = 0.0
        self._render()
    def _render(self):
        self.label = FONT.render(self.text, True, GREEN)
        self.rect = self.label.get_rect(center=(WIDTH//2, self.y))
    def update_text(self, new_text):
        if new_text != self.text:
            self.text = new_text
            self._render()
    def draw(self, surf):
        mx, my = pygame.mouse.get_pos()
        color = LIGHT_GREEN if self.rect.collidepoint((mx,my)) else GREEN
        lbl = FONT.render(self.text, True, color)
        surf.blit(lbl, self.rect)
    def click_if_hit(self, pos):
        if self.rect.collidepoint(pos):
            self.active_since = time.time()
            self.action()
            return True
        return False
def draw_text(surface, text, pos, which_font=FONT):
    surface.blit(which_font.render(text, True, GREEN), pos)
def draw_wrapped(surface, text, x, y, max_chars, which_font=SMALLFONT):
    lines = textwrap.wrap(text, width=max_chars)
    for i, line in enumerate(lines):
        surface.blit(which_font.render(line, True, GREEN), (x, y + i * (which_font.get_height()+2)))
def add_achievement(name):
    if name not in achievements:
        achievements.append(name)
def click_action():
    global crypto
    crypto += givecrypto
def buy_income():
    global crypto, givecrypto, globalprice
    cost = int(globalprice * GP_COST["income"])
    if crypto >= cost:
        crypto -= cost
        givecrypto *= EFFECTS["income"]
        globalprice *= gp_growth
        update_all_texts()
        add_achievement("first boost")
def buy_miner():
    global crypto, cryptominers, globalprice
    cost = int(globalprice * GP_COST["miner"])
    if crypto >= cost:
        crypto -= cost
        cryptominers *= EFFECTS["miner"]
        globalprice *= gp_growth
        update_all_texts()
def buy_computer():
    global crypto, givecrypto, cryptominers, computerlevel, globalprice
    cost = int(globalprice * GP_COST["computer"])
    if crypto >= cost:
        crypto -= cost
        givecrypto *= EFFECTS["computer"]
        cryptominers *= EFFECTS["computer"]
        computerlevel += 1
        globalprice *= gp_growth
        update_all_texts()
        if computerlevel == 5:
            add_achievement("supercomputer")
def buy_datacenter():
    global crypto, cryptominers, globalprice
    cost = int(globalprice * GP_COST["datacenter"])
    if crypto >= cost:
        crypto -= cost
        cryptominers *= EFFECTS["datacenter"]
        globalprice *= gp_growth
        update_all_texts()
hack_unlocked = False
def buy_hack():
    global crypto, hack_unlocked, globalprice
    cost = int(globalprice * GP_COST["hack"])
    if crypto >= cost and not hack_unlocked:
        crypto -= cost
        hack_unlocked = True
        global givecrypto, cryptominers
        givecrypto *= EFFECTS["hack"]
        cryptominers *= EFFECTS["hack"]
        globalprice *= gp_growth
        update_all_texts()
        add_achievement("H4CK3R")
def hack_action():
    global crypto, givecrypto
    if hack_unlocked:
        crypto += 5 * givecrypto
def check_achievement_auto():
    global achievement_unlocked
    if (not achievement_unlocked) and crypto >= ACHIEVEMENT_COST:
        achievement_unlocked = True
        add_achievement(achievement_name)
click_btn = Button("Click this!", 150, click_action)
incomes_button = Button("", 210, buy_income)
miners_button = Button("", 260, buy_miner)
computer_button = Button("", 310, buy_computer)
datacenter_button = Button("", 360, buy_datacenter)
hack_button = Button("", 410, buy_hack)
hack_action_button = None
buttons = [click_btn, incomes_button, miners_button, computer_button, datacenter_button, hack_button]
def update_all_texts():
    incomes_button.update_text(f"Buy income boost (click) — cost: {int(globalprice * GP_COST['income'])}")
    miners_button.update_text(f"Buy miner (passive) — cost: {int(globalprice * GP_COST['miner'])}")
    computer_button.update_text(f"Buy computer (double all) — cost: {int(globalprice * GP_COST['computer'])}")
    datacenter_button.update_text(f"Buy data center (triple passive) — cost: {int(globalprice * GP_COST['datacenter'])}")
    hack_button.update_text(f"Buy HACK (upgrade) — cost: {int(globalprice * GP_COST['hack'])}")
update_all_texts()
last_miner_time = time.time()
running = True
while running:
    dt = CLOCK.tick(60) / 1000.0
    now = time.time()
    if now - last_miner_time >= 0.5:
        crypto += cryptominers
        last_miner_time = now
    check_achievement_auto()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            for b in buttons:
                if b.click_if_hit(pos):
                    break
            if hack_unlocked and hack_action_button:
                hack_action_button.click_if_hit(pos)
    WIN.fill(BLACK)
    draw_text(WIN, f"Bitcoins: {round(crypto,1)}", (20, 18), BIGFONT)
    draw_text(WIN, f"Computer level: {computerlevel}", (20, 56))
    for b in buttons:
        b.draw(WIN)
    if hack_unlocked:
        if hack_action_button is None:
            hack_action_button = Button("HACK!", 470, hack_action)
        hack_action_button.draw(WIN)
    if achievements:
        draw_wrapped(WIN, "Achievements: " + ", ".join(achievements), 20, HEIGHT - 70, 80, SMALLFONT)
    pygame.display.flip()
pygame.quit()
sys.exit()