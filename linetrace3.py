#!/usr/bin/python3
# coding: UTF-8

import gpiozero
from gpiozero import MCP3004, Robot
from signal import pause

def prs2mtrs(Ks,kakozure,Szure,target,photorefs):
    pr = [0,0,0,0]
    zurepr = [0,0,0,0]
    zuresapr = [0,0,0,0]
    atai = [0,0,0,0]

    for i in range(pr):
        #　フォトリフレクタの値を読み出し
        pr[i] = photorefs[i].value
        #　ズレを計算
        zurepr[i] = pr[i] -target[i]
        #　ズレの総和を計算
        Szure[i] += zurepr[i]
        #　過去のズレと現在のズレの差を計算
        zuresapr[i] = zurepr[i] - kakozure[i]
        #　モーター制御の強度値の計算（PID制御を用いている。)
        atai[i] = Ks[0] * zurepr[i] + Ks[1] * Szure[i] + Ks[2] + zuresapr[i]

    left = (atai[0]+atai[1])/2.0
    right = (atai[2]+atai[3])/2.0

    kakozure = zurepr

    return (clamped(left),clamped(right))

def clamped(v):
        return max(-1,min(1,v))

def line_follow(Ks,kakozure,Szure,target,photorefs):
    while True:
        yield prs2mtrs(Ks,kakozure,Szure,target,photorefs)

def main():
    """ メイン関数 """
    #　モータードライバ接続ピン
    PIN_AIN1 = 6
    PIN_AIN2 = 5
    PIN_BIN1 = 26
    PIN_BIN2 = 27

    #　A/D変換チャネル数
    NUM_CH = 4

    """
    リストはミュータブルなオブジェクトであるため、
    あとから要素の値などを変更することができる。
    関数内で実引数を代入された変数に変更が加えられると、現在の保管場所に保管されている値が変更されるため、
    関数の呼び出し元の変数が参照している値も変更される。
    参照:https://www.javadrive.jp/python/userfunc/index3.html
    """
    
    #　Ks[0]にPゲイン,Ks[1]にIゲイン,Ks[2]にDゲインを入れる
    Ks = [0,0,0]
    #　過去のズレのリスト宣言 
    kakozure = [0,0,0,0]
    #　ズレの総和のリスト宣言
    Szure = [0,0,0,0]
    #　ターゲット値のリスト宣言
    target = [0,0,0,0]

    #　左右モーター設定(PWM)
    motors = Robot(left=(PIN_AIN1,PIN_AIN2),right=(PIN_BIN1,PIN_BIN2),pwm=True)
    #　フォトリフレクタ（複数）設定（A/D変換）
    photorefs = [ MCP3004(channel=idx) for idx in range(NUM_CH) ]
    #　ライントレース処理
    motors.source = line_follow(Ks,kakozure,Szure,target,photorefs)
    #　停止(Ctr+c)まで待機
    pause()

if __name__ == '__main__':
        main()