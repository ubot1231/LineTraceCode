# import module
# reference
# https://www.ma-chanblog.com/2019/03/raspi-photo-reflector.html
# https://hellobreak.net/raspberry-pi-pico-line-trace-sensor1/
# EicDesignLab/eiclab_line_follower.py


# autostart with systemd (havent implemented yet)

from gpiozero import Button
from subprocess import check_call
from signal import pause
from gpiozero import Robot
from gpiozero.tools import sin_values, cos_values, post_delayed


def main():
    """ メイン関数 """
    # 接続PIN
    PIN_BT = 3 # シャットダウンボタン用
    PIN_AIN1 = 6 # モータ用
	PIN_AIN2 = 5 # モータ用
	PIN_BIN1 = 26 # モータ用
	PIN_BIN2 = 27 # モータ用

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
			v = pr.value # 仮に残してあるだけ

			p0 = photorefs[0].value
			p1 = photorefs[1].value
			p2 = photorefs[2].value
			p3 = photorefs[3].value

			print('{}:{:4.2f} '.format(idx+1,v),end=' ') # フォトリフレクタの値表示
            # 条件分岐
			# 閾値は0.5でいいのでは？白0.9くらい黒0.2くらい
			# モータの左右，前進，後進組み合わせる

            # 白白白白 0000 前進
            if (p0 < 0.5 and p1 < 0.5 and p2 < 0.5 and p3 < 0.5) :
                # 0.2秒前進(50%)
		        motors.forward(speed=0.5)
		        sleep(0.5)
			
            # 白白黒黒 0011 右逆左正
            elif (p0 < 0.5 and p1 < 0.5 and p2 > 0.5 and p3 > 0.5):
		    	# 0.2秒右カーブ(40%)逆転
		        motors.reverse(curve_right=0.4)
				# 0.2秒左カーブ(40%)正転
		        motors.forward(curve_left=0.4)
		        sleep(0.5)
			
            # 黒黒白白 1100 左逆右正
            elif (p0 > 0.5 and p1 > 0.5 and p2 < 0.5 and p3 < 0.5):
				# 0.2秒左カーブ(40%)逆転
		        motors.reserve(curve_left=0.4)
				# 0.2秒右カーブ(40%)正転
		        motors.forward(curve_right=0.4)
		        sleep(0.5)
			
			# # 白白白白 0000 前進
            # if ((photorefs[0] * photorefs[1])/2 < 0.5 and (photorefs[2] * photorefs[3])/2 < 0.5) :
            #     # 0.2秒前進(50%)
		    #     motors.forward(speed=0.5)
		    #     sleep(1)
			
            # # 白白黒黒 0011 右逆左正
            # elif ((photorefs[0] * photorefs[1])/2 < 0.5 and (photorefs[2] * photorefs[3])/2 > 0.5):
		    # 	# 0.2秒右カーブ(40%)逆転
		    #     motors.reverse(curve_right=0.4)
			# 	# 0.2秒左カーブ(40%)正転
		    #     motors.forward(curve_left=0.4)
		    #     sleep(1)
			
            # # 黒黒白白 1100 左逆右正
            # elif ((photorefs[0] * photorefs[1])/2 > 0.5 and (photorefs[2] * photorefs[3])/2 < 0.5):
			# 	# 0.2秒左カーブ(40%)逆転
		    #     motors.reserve(curve_left=0.4)
			# 	# 0.2秒右カーブ(40%)正転
		    #     motors.forward(curve_right=0.4)
		    #     sleep(1)



if __name__ == '__main__':
    main()
