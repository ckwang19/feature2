import sys
import os
sys.path.insert(-1, '/usr/local/lib/python2.7/dist-packages')
import argparse

from module.ParserYahooFin.get_yahoo_fin import download_quotes as parser_day_info
from module.ParserStatement.get_statement import Parser
from module.XMLWriter.XMLGenerator import xml_writer

import time

def check_folder(p):
    if not os.path.exists(p):
        os.makedirs(p)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--xml_bs_pth', type=str, \
        default= 'data')
    parser.add_argument('--chrome_driver_path', type=str, \
        default= '/usr/local/share/chromedriver')
    parser.add_argument('--account', type=str, required=True, \
        default= '---')
    parser.add_argument('--password', type=str, required=True, \
        default= '---')
    parser.add_argument('--config_path', type=str)
    return parser.parse_args()

def main():
    param = get_args()
    check_folder(os.path.join(os.getcwd(), param.xml_bs_pth))
    obj = Parser(param)
    obj.parser_Login_Selenium()
    stock_num_list = []
    finish_stock_num_list = os.listdir(os.path.join(os.getcwd(), param.xml_bs_pth))
    count = len(finish_stock_num_list)
    d = {}
    pe_threshold = 14
    volume_threshold = 500
    top_N = 30
    result_p = f'result/{time.strftime("%Y-%m-%d", time.localtime())}'
    check_folder(result_p)
    with open('stock_num.txt', 'r') as f_r:
        for line in f_r.readlines():
            stock_num_list.append(line.strip()[0:4])

    for stock_num in stock_num_list:
        if stock_num == stock_num_list[-1]:
            break
        if stock_num in finish_stock_num_list:
            count += 1
            continue
        print ('right now is {}, still have {} stock unfinish'.format(stock_num, len(stock_num_list) - count))
        try:
#        if 1:
            price, pe, volume = obj.parser_price(stock_num)
            if pe > pe_threshold or volume < volume_threshold:
                count += 1 
                continue
            inv_trust_volume = obj.parser_investment_trust(stock_num)
            d[inv_trust_volume * price] = stock_num
        except:
            print ('{} has something wrong'.format(stock_num))
        obj.clear()
        count += 1
    for ITvolume in sorted(d, reverse=True)[:top_N]:
        stock_num = d[ITvolume]
        obj.parser_K_screenshot(stock_num, f'{result_p}/{stock_num}.png')


if __name__ == '__main__':
    main()