# 破産確率表を出力するプログラム

import numpy as np
import pandas as pd

# ============================== 初期パラメータの設定 ==============================
win_pct = 0.5  # 勝率
risk_reward = 1.5  # リスクリワード比
risk_rate = 0.02  # 損失許容率
funds = 1000000  # 資金
ruin_line = 500000  # 破産ライン

# 表に出力する値の範囲
win_range = np.arange(0.1, 1.01, 0.1) # 勝率(10 ~ 100%まで、10%ずつ)
rr_range = np.arange(0.2, 3.01, 0.2)  # リスクリワード比(0.2 ~ 3.0まで、0.2ずつ)
# ==================================================================================

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

# パーセンテージ形式で列名とインデックスを設定
columns = [f"{int(w*100)}%" for w in win_range]  # 勝率をパーセンテージ形式の文字列に変換
index = [f"{r:.1f}" for r in rr_range]  # リスクリワード比を文字列に変換

# データフレームの作成
data = []
for rr in rr_range:
    row = [calc_ruin_rate(win_pct, rr, risk_rate, funds, ruin_line) for win_pct in win_range]
    data.append(row)

df = pd.DataFrame(data, index=index, columns=columns)

# スタイリングの適用：色を変更する関数を定義
def color_by_value(val):
    if val < 0.005:
        return "color: lime"
    elif val < 0.01:
        return "color: green"
    elif val < 0.1:
        return "color: #ffd700"
    elif val < 1:
        return "color: orange"
    else:  # 100% の場合
        return "color: red"

# パーセンテージ形式のフォーマット関数を更新
def format_percentage(val):
    if val < 0.005:  # 0.5%未満は0%とする
        return "0%"
    elif val >= 0.995:  # 99.5%以上は100%とする
        return "100%"
    else:
        return "{:.2%}".format(val).rstrip("0").rstrip(".")

# スタイリングを適用：値に応じて色分けし、パーセンテージ形式で表示
styled_df = df.style.applymap(color_by_value).format(format_percentage)
styled_df
