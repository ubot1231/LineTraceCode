# autostart with systemd (havent implemented yet)

# import module
from gpiozero import Button
from gpiozero import Robot,MCP3004
from time import sleep


def main():
    # PIN
    PIN_BT = 3
    PIN_AIN1 = 6
    PIN_AIN2 = 5
    PIN_BIN1 = 26
    PIN_BIN2 = 27

    NUM_CH = 4 # A/D変換チャネル数
    # フォトリフレクタ（複数）設定（A/D変換）
    photorefs = [ MCP3004(channel=idx) for idx in range(0,NUM_CH) ]
    # 左右モーター設定(PWM)
    motors = Robot(left=(PIN_AIN1,PIN_AIN2),right=(PIN_BIN1,PIN_BIN2),pwm=True)
    # ループ処理
    while True:
        # 計測データの取得
        for idx in range(0,NUM_CH):
            pr = photorefs[idx]
            v = pr.value
            # フォトリフレクタの値をvalueに変換して，定義した各pに代入．
            p0 = photorefs[0].value
            p1 = photorefs[1].value
            p2 = photorefs[2].value
            p3 = photorefs[3].value
            # フォトリフレクタの値表示
            print('{}:{:4.2f} '.format(idx+1,v),end=' ') 

        # 条件分岐について
        # 閾値は0.5でいいのでは．白0.9および黒0.2程度を目安に．
        # モータの左右，前進，後進組み合わせる．
        # 場合により，外側が黒の場合は，もっと左右を火力全開にという感じで制御できるのでは．
        # sleep分だけ，モータが動作すると考えて良い．
        # 1秒になっているので，動作確認出来次第，カーブは秒数を少なくする．
        # 白白 00 前進
        if ((p0+p1)/2 < 0.5 and (p2+p3)/2 < 0.5) :
            # 1秒前進(50%)
            motors.forward(speed=0.5)
            sleep(0.5)
        # 白黒 01 右逆左正
        elif ((p0+p1)/2 < 0.5 and (p2+p3)/2 > 0.5):
            # 1秒 右カーブ(20%)逆転
            motors.reverse(curve_right=0.2)
            # 1秒 左カーブ(40%)正転
            motors.forward(curve_left=0.4)
            sleep(0.5)
                
        # 黒白 10 左逆右正
        elif ((p0+p1)/2 > 0.5 and (p2+p3)/2 < 0.5):
            # 1秒 左カーブ(20%)逆転
            motors.reserve(curve_left=0.2)
            # 1秒 右カーブ(40%)正転
            motors.forward(curve_right=0.4)
            sleep(0.5)

if __name__ == '__main__':
    main()
