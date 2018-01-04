#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    Create  : 2017/12/13 下午5:56
    Author  : Richard Chen
    File    : history_financial_stock.py
    Software: IntelliJ IDEA
'''
from conf.requests_useragent import get_user_agent
import requests
from common.db_utils.stock_crawler_inner_db import LmInnerReportDBMgr
from common.utils.time_utils import date_turn_timestamp, get_date_object


def install_history_financial_crawler(stock_code):
    baseurl = 'http://quotes.money.163.com'
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'User-Agent': get_user_agent(),
    }
    zcfzb_url = baseurl + '/service/zcfzb_%s.html' % stock_code
    zcfzb_response = requests.get(url=zcfzb_url, headers=headers)
    zcfzb(zcfzb_response, stock_code)

    xjllb_url = baseurl + '/service/xjllb_%s.html' % stock_code
    xjllb_response = requests.get(url=xjllb_url, headers=headers)
    xjllb(xjllb_response, stock_code)

    lrb_url = baseurl + '/service/lrb_%s.html' % stock_code
    lrb_response = requests.get(url=lrb_url, headers=headers)
    lrb(lrb_response, stock_code)

    zycwzb_url = baseurl + '/service/zycwzb_%s.html' % stock_code
    zycwzb_response = requests.get(url=zycwzb_url, headers=headers)
    zycwzb(zycwzb_response, stock_code)

    cwbbzy_url = baseurl + '/service/cwbbzy_%s.html' % stock_code
    cwbbzy_response = requests.get(url=cwbbzy_url, headers=headers)
    cwbbzy(cwbbzy_response, stock_code)

    print('%s save history financial of stock successful...' % stock_code)


def zcfzb(response, stock_code):
    '''

    :param response: 资产负债表的数据 str
    :param stock_code: 股票代码
    :return:
    '''
    zd_list = ["YEAREND_DATE", "CURRENCY_CAPITAL", "SETTLEMENT_RESERVE", "DEMOLITION_CAPITAL",
               "TRANSACTIONAL_ASS", "DERIVATIVE_ASS", "BILL_RECEIVABLE", "ACCOUNTS_RECEIVABLE",
               "ADVANCE_PAYMENT", "PREMIUMS_RECEIVABLE", "ACCOUNT_REINSURANCE_RECEIVABLE",
               "RESERVE_CONTRACT_REINSURANCE_REVEIVABLE", "INTEREST_DECIVABLE", "DIVIDEND_DECIVABLE",
               "OTHER_DECIVABLES", "EXPORT_REBATE_DECIVABLE", "SUBSIDYS_DECIVABLE",
               "CASH_DEPOSIT_AS_COLLATERAL_DECIVABLE", "INTERNAL_RECEIVABLE",
               "BUY_BACK_THE_SALE_OF_FINANCIAL_ASS",
               "STOCK", "DEFERRED_EXPENSES", "PENDING_CURRENT_ASSETS_PROFIT_LOSS",
               "NON_CURRENT_ASSETS_DUE_WITHIN_ONE_YEAR", "OTHER_CURRENT_ASSETS", "TOTAL_CURRENT_ASSETS",
               "LOANS_AND_ADVANCES", "FINANCIAL_ASSETS_AVAILABLE_FOR_SALE", "HOLDING_TO_MATURIY_INVESTMENT",
               "LONG_TERM_RECIVABLES", "LONG_TERM_EQUITY_INVESTMENT", "OTHER_LONG_TERM_INVESTMENT",
               "INVESTMENT_REAL_ESTATE", "ORIGINAL_VALUE_OF_FIXED_ASSETS", "ACCUMULATED_DEPRECIATION",
               "NET_VALUE_OF_FIXED_ASSETS", "FIXED_ASSETS_IMPAIRMENT_RESERVES", "FIXED_ASSETS",
               "CONSTRUCTION_IN_PROCESS", "ENGINEERING_MATERIALS", "CLEAR_OF_FIXED_ASSETS", "BIOLOGICAL_ASSETS",
               "PUBLIC_WELFARE_BIOLOGICAL_ASSETS", "OIL_AND_GAS_ASSETS", "IMMATERIAL_ASSETS",
               "DEVELOPMENT_AMOUNT_OF_EXPENDITURE", "GOODWILL", "LONG_TERM_PREPAID_EXPENSES",
               "RIGHT_OF_SPLIT_SHARE_CIRCULATION", "DEFERRED_TAX_ASSETS", "OTHER_NON_CURRENT_ASSETS",
               "TOTAL_NON_CURRENT_ASSETS", "TOTAL_ASSETS", "MONEY_BORROWED_FOR_SHORT_TIME",
               "BORROWING_FROM_THE_CENTRAL_BANK", "DEPOSIT_TAKING_AND_INTERBANK_DEPOSIT",
               "LOANS_FROM_OTHER_BANKS",
               "TRANSACTIONAL_FINANCIAL_LIABILTIES", "DERIVATIVE_FINANCIAL_LIABILTIES", "BILL_PAYABLE",
               "ACCOUNTS_PAYABLE", "DEPOSIT_RECEIVED", "FINANCIAL_ASSETS_SOLD_FOR_REPURCHASE",
               "HANDING_FEE_AND_COMMISSION", "SALARY_PAYABLE_TO_EMPLOYEES", "TAX_PAYABLE", "INTEREST_PAYABLE",
               "DIVIDENDS_PAYABLE", "OTHER_ACCOUNTS_PAYABLES", "MARGIN_PAYABLE", "INTERNAL_PAYABLES",
               "OTHER_PAYABLE", "ACCRUED_EXPENSES", "PROJECTED_CURRENT_LIABILITIES",
               "ACCOUNTS_PAYABLE_REINSURANCE", "INSURANCE_CONTRACT_RESERVES", "BUY_ANDSELL_SECURITIES_BY_PROXY",
               "ACTING_UNDERWEITING_SECURITIES", "INTERNATIONAL_TICKET_SETTLAEMENT",
               "DOMESTIC_TICKET_SETTLAEMENT", "DEFERRED_INCOME", "SHORT_TERM_BONDS_PAYABLE",
               "NON_CURRENT_LIABILITIES_DUE_WITHIN_ONE_YEAR", "OTHER_CURRENT_LIABILITIES",
               "TOTAL_CURRENT_LIABILITIES",
               "LONG_TERM_LOAN", "BONDS_PAYABLE", "LONG_TERM_PAYABLES", "ACCOUNT_PAYABLE_SPECIAL_FUNDS",
               "PROJECTED_NON)CURRENT_LIABILITIES", "LONG_TERM_DEFERRED_INCOME", "DEFERRED_TAX_LIABILITY",
               "OTHER_NON_CURRENT_LIABILTIES", "TOTAL_NON_CURRENT_LIABILTIES",
               "TOTAL_LIABILITIES", "PAID_IN_CAPITAL", "CAPITAL_SURPLUS", "REDUCE:STOCK_THIGH",
               "SPECIAL_RESERVE", "SURPLUS_PUBLIC_ACCUMULATION", "GENERAL_RISK_RESERVE",
               "UNCERTAIN_INVESTMENT_LOSS", "UNDISTRIBUTED_PROFIT", "QUASI_DISTRIBUTIVE_CASH)DIVIDEND",
               "CONVERSION_BALANCE_OF_FOREIGN_CURRENCY_STATEMENTS",
               "TOTAL_EQUITY_ATTRIBUTABLE_TO_SHAREHOLDERS_OF_THE_PARENT_COMPANY",
               "MINORITY_SHAREHOLDER_RIGHT_AND_INTERESTS", "OWNER_S_EQUITY", "LIABILITIES_AND_OWNER_S_EQUITY", ]
    zcfzb_data = [{j[0]: j[1] for j in i} for i in (zip(zd_list, it) for it in zip(
        *[item.strip().split(",")[1:-1] for item in response.text.strip().split("\n")]))]

    db_report_date = LmInnerReportDBMgr.get_code('lm_stock_data', stock_code, 'financial_report_date')
    if db_report_date:
        if date_turn_timestamp(db_report_date, zcfzb_data[0]['YEAREND_DATE']):
            LmInnerReportDBMgr.save_set_result('lm_stock_data', {'code': stock_code}, 'report.zcfzb',
                                               zcfzb_data)
            LmInnerReportDBMgr.save_insert_result('lm_stock_data',
                                                  {'code': stock_code,
                                                   'financial_report_date': zcfzb_data[0]['YEAREND_DATE'],
                                                   })
    else:

        LmInnerReportDBMgr.save_insert_result('lm_stock_data',
                                              {'code': stock_code,
                                               'financial_report_date': zcfzb_data[0]['YEAREND_DATE'],
                                               'report': {'zcfzb': zcfzb_data}})


def xjllb(response, stock_code):
    '''

    :param response: 现金流量表的数据 str
    :param stock_code: 股票代码
    :return:
    '''
    zd_list = ["YEAREND_DATE", "SELLING_CASH_RECEIVED_FROM_SERVICES",
               "NET_INCREASE_IN_CUSTOMER_DEPOSITS_AND_TRADE_DEPOSITS",
               "NET_INCREASE_IN_BORROWING_FROM_THE_CENTRAL_BANK",
               "FROM_OTHER_FINANCIAL_INSTITUIONS_NET_INCREASE_OF_LOANS",
               "CASH_RECEIVED_FROM_THE_PERMIUMS_OF_THE_ORIGINAL_INSURANCE_CONTRACT",
               "RECEIPT_OF_REINSURANCE_NET_CASH",
               "INSURED_SAVINGS_AND_INVESTMENT_FUND_NET_INCREASE",
               "DISPOSAL_OF_NET_INCREASE_IN_TRANSACTION_FINANCIAL_ASSETS",
               "CASH_FOR_INTEREST,COMMISSION_AND_COMMISSION", "NET_INCREASE_OF_LOANS",
               "NET_INCREASE_IN_REPO_BUSINESS_FUNDS",
               "THE_TAX_AND_FEE_RECEIVED", "OTHER_CASH_RELATED_TO_BUSINESS_ACTIVITIES_RECEIVED",
               "CASH_INFLOWS_FROM_OPERATING_ACTIVITIES",
               "CASH_FOR_PURCHASE_OF_GOODS_AND_LABOR_SERVICES", "NET_INCREASE_IN_LOANS_AND_ADVANCES",
               "NET_INCREASE_OF_NET_INCREASE_OF_CENTRAL_BANK_AND_INDUSTRY",
               "CASH_PAID_FOR_THE_ORIGINAL_INSURANCE_CONTRACT",
               "CASH_FOR_PAYMENT_OF_INTEREST,COMMISSION_AND_COMMISSION", "CASH_PAYMENT_OF_POLICY_BONUS",
               "CASH_PAID_TO_WORKERS_AND_WORKERS", "VARIOUS_TAXES_AND_FEES_PAID",
               "OTHER_CASH_RELATED_TO_BUSIONESS_ACTIVITIES", "OPERATING_CASH_OUTFLOWSUBTOTAL",
               "NET_CASH_FLOW_GENERATED_BY_OPERAtiNG_ACTIVITI", "CASH_RECEIVED_FROM_THE_RETURN_OF_INVESTMENT",
               "CASH_RECEIVED_FROM_THE_PROCEEDS_OF_INVESTMENT",
               "NET_CASH_RECOVERED_FROM_THE_DISPOSAL_OF_FIX_ASSETS,INTANGIBLE_ASSETS_AND_OTHER_LONG_TERM_ASSETS",
               "NET_ASHT_RECEIVED_BY_THE_SUBSIDIARY_AND_OTHER_BUSINESS_UNITS",
               "OTHER_CASH_RELATED_TO_INVESTMENT_ACTIVITIES_RECEIVED",
               "REDUCTION_OF_CASH_RECEIVED_BY_PLEDGE_AND_FIX_DEPOSIT", "CASH_INFLOW_FROM_INVESTMENT_ACTIVITIES",
               "CASH_PAID_FOR_PURCHASE_OF_FIX_ASSETS,INTANGIBLE_ASSET_AND_OTHER_LONG_TERM_ASSET",
               "THE_CASH_PAID_BY_THE_INVESTMENT", "NET_INCREASE_IN_MORTGAGE_LOAN",
               "NET_CASH_PAID_BY_SUBSIDIARY_AND_OTHER_BUSINESS_UNITS",
               "OTHER_CASH_RELATED_TO_INVESTMENT_ACTIVITIEs",
               "INCREASE_THE_AMOUNT_OF_CASH_PAID_BY_PLEDGE_AND_FIX_DEPOSIT",
               "CASH_OUTFLOW_FOR_INVESTMENT_ACTIVITIES", "NET_CASH_FLOW_GENERATED_BY_INVESTMENT_ACTIVITIES",
               "CASH_RECEIVED_BY_INVESTMENT",
               "AMONG_THEM:SUBSIDIARY_COMPANY_ABSORBS_THE_CASH_RECEIVED_BY_THE_MINORITY_SHAREHOLDERS",
               "CHASH_RECEIVED_FROM_THE_LOAN",
               "CASH_RECEIVED_FROM_THE_ISSUANCE_OF_BONDS",
               "RECEIVING_OTHER_CASH_RELATED_TO_FUND_RAISING_ACTIVITIES", "CASH_INFLOW_FROM_FINANCING_ACTIVITIES",
               "CASH_IN_PAYMENT_OF_DEBT", "CASH_PAID_FOR_DISTRBUTION_OG_DIVIDENDS,PROFITS,OR_PAYMENT_OF_INTEREST",
               "AMONG_THEM:THE_DIVIDEND_AND_PROFIT_PAID_BY_SUBSIDIARY_TO_MINORITY_SHAREHOLDERS",
               "PAYMENT_OF_OTHER_CASH_RELATED_TO_FUND_RAISIONG_ACTIVItiES", "CASH_OUTFLOW_FOR_FINANCING_ACTIVITIES",
               "NET_CASH_FLOW_GENERATED_BY_FUND_RAISING_ACTIVITIES",
               "EFFECT_OF_EXCHANGE_RATE_CHANGES_ON_CASH_AND_CASH_EQUIVALENTS",
               "NET_INCREASE_IN_CASH_AND_EQUIVALENTS", "ADD:THE_BALANCE_OF_CASH_AND_CASH_EQUIVALENTS",
               "END_OF_TERM_CASH_AND_CASH_EQUIVALENTS_BALANCE", "NET_PROFIT",
               "PROFIT_AND_LOSS_OF_MINORITY_SHAREHOLDERS", "UNIDENTIFIED_INVESTMENT_LOSSES",
               "ASSET_IMPAIRMENT_PREPARATION",
               "FIXED_ASSETS_DEPRECIATION,DEPLETION_OF_OIL_AND_GASASSETS,DEPRECIATION_OF_PRODUCTION_MATERIALS",
               "AMORTIZATION_OF_INTANGIBLE_ASSETS", "AMORTIZATION_OF_LONG_TERM_APPORTIONED_EXPENSES",
               "REDUCED_COAST_OF_APPORTIONED", "AN_INCREASE_IN_THE_ADVANCE_COAST",
               "DISPOSE_OF_LOSS_OF_FIXED_ASSETS,INTANGIBLE_ASSETS_AND_OTHER_LONG_TERM_ASSETS",
               "LOSS_OF_FIXED_ASSETS", "LOSS_OF_FAIR_VALUE_CHANGE", "INCREASE_IN_DEFERRED_INCOME(REDUCE:REDUCTION)",
               "EXPECTED_LIABILITIES", "FINANCIAL_COST", "INVESTMENT_LOSS", "DEFERRED_INCOME_TAX_ASSETS",
               "INCREASE_OF_DEFERRED_INCOME_TAX_LIABILITIES", "REDUCTION_IN_INVENTORY",
               "REDUCTION_OF_OPERATIONAL_RECEIVABLE_PROJECTS", "AN_INCREASE_IN_OPERATIONAL_PROJECTS",
               "REDUCTIONG_OF_COMPLETED_UNSETTLED_PAYMENTS(REDUCE:INCREASE)",
               "AN_INCREASE_IN_THE_SETTLEMENT_OF_UNCOMPLETED_FUNDS(REDUCE:REDUCTION)", "OTHER",
               "OPERATING_ACTIVIITIES_PRODUCE_NET_CASH_FLOW", "DEBT_TO_CAPITAL",
               "SWITCHING_COMPANY_BONDS_THAT_EXPIRE_WITHIN_ONE_YEAR", "FINANCING_IS_RENTED_INTO_FIXED_ASSETS",
               "FINAL_BALANCE_OF_CASH", "INITIAL_BALANCE_OF_CASH", "FINAL_BALANCE_OF_CASH_EQUIVALENTS",
               "THE_INITIAL_BALANCE_OF_THE_CASH_EQUIVALENTS", "NET_INCREASE_IN_CASH_AND_CASH_EQUIVALENTS"]

    xjllb_data = [{j[0]: j[1] for j in i} for i in (zip(zd_list, it) for it in zip(
        *[item.strip().split(",")[1:-1] for item in response.text.strip().split("\n")]))]
    db_report_date = LmInnerReportDBMgr.get_code('lm_stock_data', stock_code, 'financial_report_date')
    if db_report_date:
        if date_turn_timestamp(db_report_date, xjllb_data[0]['YEAREND_DATE']):
            LmInnerReportDBMgr.save_set_result('lm_stock_data', {'code': stock_code}, 'report.xjllb',
                                               xjllb_data)
    else:
        LmInnerReportDBMgr.save_insert_result('lm_stock_data',
                                              {'code': stock_code,
                                               'financial_report_date': xjllb_data[0]['YEAREND_DATE'],
                                               'report': {'xjllb': xjllb_data}})


def lrb(response, stock_code):
    '''

    :param response: 利润表的数据 str
    :param stock_code: 股票代码
    :return:
    '''
    zd_list = ["YEAREND_DATE", "GROSS_REVENUE", "OPERATIONG_RECEIPT", "INTEREST_REVENUE", "EARNED_PREMIUM",
               "POUNDAGE_AND_COMMISSION_INCOME",
               "SALES_INCOME_OF_REAL_ESTATE", "OTHER_BUSINESS_INCOME", "TOTAL_OPERATING_COST", "COST_IN_BUSINESS",
               "INTEREST_EXPENSE",
               "POUNDAGE_AND_COMMISSION_EXPENSES", "SALE_COST_OF_REAL_ESTATE", "RESEARCH_AND_DEV_ELOPMENT_COST",
               "SURRENDER_VALUE",
               "PAYMENT_NET_EXPENDITURE", "EXTRACT_INSURANCE_CONTRACT_RESERVE_NET", "EXPENDITURE_DIVIDEND_POLICY",
               "REINSURANCE_EXPENSES",
               "OTHER_BUSINESS_COSTS", "BUSINESS_TAXES_AND_SURCHARGES", "SELLING_EXPENSES", "MANAGEMENT_EXPENSES",
               "FINANCIAL_EXPENSES",
               "ASSETS_IMPAIRMENT_LOSS", "FAIR_VALUE_CHANGE_INCOME", "INVESTMENT_PROFIT",
               "INVESTMENT_INCOME_FOR_VENTURES_AND_JOINT_VENTURES",
               "EXCHANGE_EARNINGS", "FUTURES_PROFIT_AND_LOSS", "MANAGED_INCOME", "SUBSIDY_INCOME",
               "OTHER_BUSINESS_PROFITS", "OPERATING_PROFIT",
               "NON_BUSINESS_INCOME", "NON_BUSINESS_ESPENDITURE", "DISPOSAL_LOSS_OF_NON_CURRENT_ASSETS",
               "TOTAL_PROFIT", "INCOME_TAX_EXPENSE",
               "UNCINFIRMED_INVESTMENT_LOSS", "NET_MARGIN", "VEST_IN_PARENT_COMPANY_PROPRIETOR_NET_MARGIN",
               "NET_PROFIT_OF_THE_MERGED_PARTY_BEFORE_MERGER",
               "MINORITY_SHAREHOLDER_PROFIT_AND_LOSS", "BASIC_PER_SHARE_PROFIT", "BILUTED_EARNINGS_PER_SHARE"]

    lrb_data = [{j[0]: j[1] for j in i} for i in (zip(zd_list, it) for it in zip(
        *[item.strip().split(",")[1:-1] for item in response.text.strip().split("\n")]))]
    for i in range(len(lrb_data)):
        '''
        处理单季度归属母公司净利润数据
        '''
        try:
            first_data = lrb_data[i]
            second_data = lrb_data[i + 1]
            first_date_obj = get_date_object(first_data['YEAREND_DATE'])
            second_date_obj = get_date_object(second_data['YEAREND_DATE'])
            if first_date_obj.month == 3 or first_date_obj.year != second_date_obj.year:
                # 3月的库里数据就是单季度的，则直接设置新字段存入mongo
                # print('三月的数据,可直接存入库中...first: {},second: {}'.format(first_data['YEAREND_DATE'],
                #                                                     second_data['YEAREND_DATE']))
                SIGNLE_VEST_IN_PARENT_COMPANY_PROPRIETOR_NET_MARGIN = float(
                    first_data['VEST_IN_PARENT_COMPANY_PROPRIETOR_NET_MARGIN'])
            elif first_date_obj.year == second_date_obj.year and (first_date_obj.month - second_date_obj.month) == 3:
                # 6月- 3月 9月 - 6月，或12月 - 9月，直接将数据做减法
                # print('month相差3个月，则做减法输出 first: {},second: {}'.format(first_data['YEAREND_DATE'],
                #                                                       second_data['YEAREND_DATE']))
                try:
                    SIGNLE_VEST_IN_PARENT_COMPANY_PROPRIETOR_NET_MARGIN = float(
                        first_data['VEST_IN_PARENT_COMPANY_PROPRIETOR_NET_MARGIN']) - float(
                        second_data['VEST_IN_PARENT_COMPANY_PROPRIETOR_NET_MARGIN'])
                except ValueError:
                    print('净利润数据为:--,无法计算,则忽略')
                    SIGNLE_VEST_IN_PARENT_COMPANY_PROPRIETOR_NET_MARGIN = ''
            else:
                print('未上市的财报不需要处理')
                # print('有问题的数据 first:{},second:{}'.format(first_data['YEAREND_DATE'], second_data['YEAREND_DATE']))
                SIGNLE_VEST_IN_PARENT_COMPANY_PROPRIETOR_NET_MARGIN = ''
        except IndexError:
            first_data = lrb_data[i]
            # print('最后一条数据，不需要进行任何操作first: {}'.format(first_data['YEAREND_DATE']))
            SIGNLE_VEST_IN_PARENT_COMPANY_PROPRIETOR_NET_MARGIN = float(first_data[
                                                                            'VEST_IN_PARENT_COMPANY_PROPRIETOR_NET_MARGIN'])
        lrb_data[i][
            'SIGNLE_VEST_IN_PARENT_COMPANY_PROPRIETOR_NET_MARGIN'] = SIGNLE_VEST_IN_PARENT_COMPANY_PROPRIETOR_NET_MARGIN
    db_report_date = LmInnerReportDBMgr.get_code('lm_stock_data', stock_code, 'financial_report_date')
    if db_report_date:
        if date_turn_timestamp(db_report_date, lrb_data[0]['YEAREND_DATE']):
            LmInnerReportDBMgr.save_set_result('lm_stock_data', {'code': stock_code}, 'report.lrb',
                                               lrb_data)
    else:
        LmInnerReportDBMgr.save_insert_result('lm_stock_data',
                                              {'code': stock_code,
                                               'financial_report_date': lrb_data[0]['YEAREND_DATE'],
                                               'report': {'lrb': lrb_data}})


def zycwzb(response, stock_code):
    '''

    :param response: 主要财务指标的数据 str
    :param stock_code: 股票代码
    :return:
    '''
    zd_list = ["YEAREND_DATE", "BASIC_PER_SHARE_PROFIT", "NET_ASSET_VALUE_PER_SHARE",
               "NET_CASH_FLOW_ARISIONG_FROM_OPERATING_ACTIVITIES_PER_SHARE", "MAIN_BUSINESS_INCOME",
               "MAIN_BUSINESS_PROFIT", "OPERATIONG_PROFIT", "INCOME_FROM_INVESTMENT",
               "NON_BALANCE_OF_PAYMENTS_NET_AMOUNT", "TOTAL_PROFIT", "NET_MARGIN",
               "NET_PROFIT_DEDUCTION_RECURRENT_PROFIT_AND_LOSS", "NET_AMOUNT_OPERATIONG_ACTIVITIES_CASH_FLOW",
               "NET_INCREASE_IN_CASH_AND_CASH_EQUIVALENTS", "TOTAL_ASSETS", "CURRENT_ASSETS",
               "TOTAL_LIABILITIES", "CURRENT_LIABILITIES", "STOCKHOLDERS_S_EQUITY_DOES_NOT_MINORITY_EQUITY",
               "NET_ASSET_YIELD_WEIGHTED"]
    zycwzb_data = [{j[0]: j[1] for j in i} for i in (zip(zd_list, it) for it in zip(
        *[item.strip().split(",")[1:-1] for item in response.text.strip().split("\n")]))]
    db_report_date = LmInnerReportDBMgr.get_code('lm_stock_data', stock_code, 'financial_report_date')
    if db_report_date:
        if date_turn_timestamp(db_report_date, zycwzb_data[0]['YEAREND_DATE']):
            LmInnerReportDBMgr.save_set_result('lm_stock_data', {'code': stock_code}, 'report.zycwzb',
                                               zycwzb_data)
    else:
        LmInnerReportDBMgr.save_insert_result('lm_stock_data',
                                              {'code': stock_code,
                                               'financial_report_date': zycwzb_data[0]['YEAREND_DATE'],
                                               'report': {'zycwzb': zycwzb_data}})


def cwbbzy(response, stock_code):
    '''

    :param response: 财务报表摘要的数据 str
    :param stock_code: 股票代码
    :return:
    '''
    zd_list = ["YEAREND_DATE", "OPERATING_RECEIPT", "COST_IN_BUSINESS", "OPERATING_PROFIT", "TOTAL_PROFIT",
               "INCOME_TAX_EXPENSE", "NET_PROFIT",
               "BASIC_PER_SHARE_PROFIT", "MONETARY_RESOURCES", "ACCOUNTS_RECEIVABLE", "STOCK",
               "TOTAL_CURRENT_ASSETS", "NET_FIXED_ASSETS", "TOTAL_ASSETS",
               "TOTAL_CURRENT_LIABILITIES", "TOTAL_NON_CURRENT_LIABILTIES", "TOTAL_LIABILITIES", "OWNER_S_EQUITY",
               "BALANCE_CASH_AND_CASH_EQUIVALENTS_BEGINNING_PERIOD",
               "NET_CASH_FLOW_ARISIONG_FROM_OPERATIONG_ACTIVITIES",
               "NET_CASH_FLOW_ARISIONG_FROM_INVESTMENT_ACTIVITIES",
               "NET_CASH_FLOW_ARISIONG_FROM_FINANCING_ACTIVITIES",
               "NET_INCRWASE_IN_CASH_AND_CASH_EQUICALENTS", "BALANCE_CASH_AND_CASH_EQUIVALENTS_END_PERIOD"]
    cwbbzy_data = [{j[0]: j[1] for j in i} for i in (zip(zd_list, it) for it in zip(
        *[item.strip().split(",")[1:-1] for item in response.text.strip().split("\n")]))]
    db_report_date = LmInnerReportDBMgr.get_code('lm_stock_data', stock_code, 'financial_report_date')
    if db_report_date:
        if date_turn_timestamp(db_report_date, cwbbzy_data[0]['YEAREND_DATE']):
            LmInnerReportDBMgr.save_set_result('lm_stock_data', {'code': stock_code}, 'report.cwbbzy',
                                               cwbbzy_data)
    else:
        LmInnerReportDBMgr.save_insert_result('lm_stock_data',
                                              {'code': stock_code,
                                               'financial_report_date': cwbbzy_data[0]['YEAREND_DATE'],
                                               'report': {'cwbbzy': cwbbzy_data}})
if __name__ == '__main__':
    # code_list = ["600000", "600016", "600028", "600029", "600030", "600036", "600048", "600050", "600100",
    #              "600104", "600111", "600340", "600485", "600518", "600519", "600547", "600606", "600837",
    #              "600887", "600919", "600958", "600999", "601006", "601088", "601166", "601169", "601186",
    #              "601198", "601211", "601229", "601288", "601318", "601328", "601336", "601390", "601398",
    #              "601601", "601628", "601668", "601688", "601766", "601788", "601800", "601818", "601857",
    #              "601881", "601901", "601985", "601988", "601989"]
    code_list = ['600919', '600958', '600999', '601088', '601166', '601169', '601186', '601198', '601211', '601336',
                 '601390', '601398', '601628', '601688','601766','601800','601881','601901','601988']
    for code in code_list:
        install_history_financial_crawler(code)
