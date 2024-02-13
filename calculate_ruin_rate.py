# 破産確率を出力するプログラム

import numpy as np

# ==================== 初期パラメータの設定 ====================
win_pct = 0.4  # 勝率
risk_reward = 1.6  # リスクリワード比
risk_rate = 0.02  # 損失許容率
funds = 1000000  # 資金
ruin_line = 500000  # 破産ライン
# ==============================================================

# 入力パラメータが正しいかチェックする関数
def is_error(win_pct, risk_reward, risk_rate, funds, ruin_line):
    # 勝率が0～100(%)の範囲外の場合にエラー
    if not 0 <= win_pct <= 1:
        return True

    # リスクリワード比が0以下の場合にエラー
    if risk_reward <= 0:
        return True

    # 損失許容率が0～100(%)の範囲外の場合にエラー
    if not 0 <= risk_rate <= 1:
        return True

    # 資金が0以下の場合にエラー
    if funds <= 0:
        return True

    # 破産ラインが0未満、または資金よりも大きい場合にエラー
    if ruin_line < 0 or ruin_line > funds:
        return True

    # 上記のいずれの条件も満たさない場合はFalseを返し、エラーなしとする
    return False


# 破産確率の方程式を計算する関数
def equation(x, P, R):
    return P * x**(R + 1) + (1 - P) - x

# 方程式の解を求める関数
def solve_equation(win_pct, R):
    S, P = 0, win_pct
    while equation(S, P, R) > 0:
        S += 1e-4
    if S >= 1: S = 1
    return S

# 破産確率を計算する関数
def calc_ruin_rate(win_pct, risk_reward, risk_rate, funds, ruin_line):
    # 入力パラメータに誤りがある場合はエラーを投げる
    if is_error(win_pct, risk_reward, risk_rate, funds, ruin_line):
        raise ValueError("入力パラメータが無効です。")

    a = np.log(1 + risk_reward * risk_rate)
    b = abs(np.log(1 - risk_rate))
    n = np.log(funds / ruin_line)
    R = a / b
    S = solve_equation(win_pct, R)
    return S ** (n / b)

# 初期パラメータを元に破産確率を求める
try:
    ruin_rate = calc_ruin_rate(win_pct, risk_reward, risk_rate, funds, ruin_line)
    # 出力(小数点以下第二位まで)
    print(f"破産確率は{ruin_rate:.2%}です")
except ValueError as e:
    print(e)
