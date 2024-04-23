import os
import random
import sys
import pygame as pg


WIDTH, HEIGHT = 1600, 900
DELTA = {  # 移動量辞書
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, 5),
    pg.K_RIGHT: (5, 0),
    pg.K_LEFT: (-5, 0)
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(obj_rct:pg.Rect):
    """
    こうかとんRect または 爆弾Rect の画面内外判定用の関数
    引数:こうかとんRect または 爆弾Rect
    戻り値:横方向判定結果, 縦方向判定結果(画面内:True, 画面外:False)
    """
    yoko, tate = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right:
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:
        tate = False
    return yoko, tate


def gameover():
    """
    ゲームオーバーになったときの関数
    引数なし
    戻り値 : ゲームオーバーのときの画面全体を表す go_sc
    """
    go_sc = pg.display.set_mode((WIDTH, HEIGHT))  # ゲームオーバー時の背景
    go_bg = pg.Surface((WIDTH, HEIGHT))
    pg.draw.rect(go_bg, (0, 0, 0), (0, 0, WIDTH, HEIGHT))
    pg.Surface.set_alpha(go_bg, 50)  # 背景を透けさせたかった
    go_sc.blit(go_bg, [0, 0])
    fo = pg.font.Font(None, 80)
    txt = fo.render("Game Over", True, (255, 255, 255))  # ゲームオーバーの文字
    go_sc.blit(txt, [700, 350])
    img = pg.image.load("fig/8.png")  # 泣いてるこうかとん
    kk_cry = pg.transform.rotozoom(img, 0, 2.0)  # こうかとんのサイズを倍に
    go_sc.blit(kk_cry, [800, 600])
    pg.display.update()
    return go_sc


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 900, 400
    clock = pg.time.Clock()
    tmr = 0
    # 爆弾の設定
    bd_img = pg.Surface((20, 20))
    bd_img.set_colorkey((0, 0, 0))
    bd_rct = bd_img.get_rect()
    bd_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    pg.draw.circle(bd_img, (255, 0, 0), (10, 10), 10)
    vx, vy = 5, 5
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bd_rct):  # こうかとんと爆弾がぶつかったら
            screen.blit(gameover(), [0, 0]) 
            clock.tick(0.2)  # 5秒の遅延
            return
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for k, v in DELTA.items():
            if key_lst[k]:
                sum_mv[0] += v[0]
                sum_mv[1] += v[1]
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)
        # 爆弾の追加と移動
        screen.blit(bd_img, bd_rct)
        bd_rct.move_ip(vx, vy)
        yoko, tate = check_bound(bd_rct)
        if not yoko:  # 横方向にはみ出てたら
            vx *= -1
        if not tate:  # 縦方向にはみ出てたら
            vy *= -1
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
