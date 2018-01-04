#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    Create  : 2018/1/2 下午8:41
    Author  : Richard Chen
    File    : financial_data.py
    Software: IntelliJ IDEA
'''
'''
网站分析:
    # url='http://money.finance.sina.com.cn/corp/go.php/vDOWN_CashFlow/displaytype/4/stockid/600000/ctrl/all.phtml',    #vDOWN_CashFlow 现金流量表
    # url='http://money.finance.sina.com.cn/corp/go.php/vDOWN_ProfitStatement/displaytype/4/stockid/600000/ctrl/all.phtml',  #vDOWN_ProfitStatement 利润表
    # url='http://money.finance.sina.com.cn/corp/go.php/vDOWN_BalanceSheet/displaytype/4/stockid/600000/ctrl/all.phtml',  #vDOWN_BalanceSheet 资产负债表
'''

import requests
from conf.requests_useragent import get_user_agent
from common.db_utils.stock_crawler_inner_db import LmInnerReportDBMgr
from common.utils.time_utils import get_date_object, date_turn_timestamp

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'User-Agent': get_user_agent(),
}


def history_financial_crawler(code):
    baseurl = 'http://money.finance.sina.com.cn'
    zcfzb_url = baseurl + '/corp/go.php/vDOWN_BalanceSheet/displaytype/4/stockid/%s/ctrl/all.phtml' % code
    zcfzb_response = requests.get(url=zcfzb_url, headers=headers, timeout=15)
    zcfzb(zcfzb_response, code)

    # xjllb_url = baseurl + '/corp/go.php/vDOWN_CashFlow/displaytype/4/stockid/%s/ctrl/all.phtml' % code
    # xjllb_response = requests.get(url=xjllb_url, headers=headers)
    # xjllb(xjllb_response, code)
    #
    # lrb_url = baseurl + '/corp/go.php/vDOWN_ProfitStatement/displaytype/4/stockid/%s/ctrl/all.phtml' % code
    # lrb_response = requests.get(url=lrb_url, headers=headers)
    # lrb(lrb_response, code)

    print('%s save history financial of stock successful...' % code)


def xjllb(response, stock_code):
    zd_list = [
        "YEAREND_DATE", "NET_INCREASE_IN_CUSTOMER_DEPOSITS_AND_TRADE_DEPOSITS",
        "NET_INCREASE_IN_BORROWING_FROM_THE_CENTRAL_BANK", "FROM_OTHER_FINANCIAL_INSTITUIONS_NET_INCREASE_OF_LOANS",
        "CASH_FOR_INTEREST,COMMISSION_AND_COMMISSION",
        "OTHER_CASH_RELATED_TO_BUSINESS_ACTIVITIES_RECEIVED", "CASH_INFLOWS_FROM_OPERATING_ACTIVITIES",
        "NET_INCREASE_IN_LOANS_AND_ADVANCES", "NET_INCREASE_OF_NET_INCREASE_OF_CENTRAL_BANK_AND_INDUSTRY",
        "CASH_PAID_TO_WORKERS_AND_WORKERS",
        "VARIOUS_TAXES_AND_FEES_PAID", "OTHER_CASH_RELATED_TO_BUSIONESS_ACTIVITIES",
        "CASH_FOR_PAYMENT_OF_INTEREST,COMMISSION_AND_COMMISSION", "OPERATING_CASH_OUTFLOWSUBTOTAL",
        "NET_CASH_FLOW_GENERATED_BY_OPERAtiNG_ACTIVITI",
        "CASH_RECEIVED_FROM_THE_RETURN_OF_INVESTMENT", "CASH_RECEIVED_FROM_THE_PROCEEDS_OF_INVESTMENT",
        "NET_CASH_RECOVERED_FROM_THE_DISPOSAL_OF_FIX_ASSETS,INTANGIBLE_ASSETS_AND_OTHER_LONG_TERM_ASSETS",
        "NET_ASHT_RECEIVED_BY_THE_SUBSIDIARY_AND_OTHER_BUSINESS_UNITS",
        "OTHER_CASH_RELATED_TO_INVESTMENT_ACTIVITIES_RECEIVED", "CASH_INFLOW_FROM_INVESTMENT_ACTIVITIES",
        "THE_CASH_PAID_BY_THE_INVESTMENT",
        "CASH_PAID_FOR_PURCHASE_OF_FIX_ASSETS,INTANGIBLE_ASSET_AND_OTHER_LONG_TERM_ASSET",
        "OTHER_CASH_RELATED_TO_INVESTMENT_ACTIVITIEs",
        "CASH_OUTFLOW_FOR_INVESTMENT_ACTIVITIES", "NET_CASH_FLOW_GENERATED_BY_INVESTMENT_ACTIVITIES",
        "CASH_RECEIVED_BY_INVESTMENT", "CASH_RECEIVED_FROM_THE_ISSUANCE_OF_BONDS",
        "RECEIVING_OTHER_CASH_RELATED_TO_FUND_RAISING_ACTIVITIES", "CASH_INFLOW_FROM_FINANCING_ACTIVITIES",
        "CASH_IN_PAYMENT_OF_DEBT", "CASH_PAID_FOR_DISTRBUTION_OG_DIVIDENDS,PROFITS,OR_PAYMENT_OF_INTEREST",
        "PAYMENT_OF_OTHER_CASH_RELATED_TO_FUND_RAISIONG_ACTIVItiES", "CASH_OUTFLOW_FOR_FINANCING_ACTIVITIES",
        "NET_CASH_FLOW_GENERATED_BY_FUND_RAISING_ACTIVITIES",
        "EFFECT_OF_EXCHANGE_RATE_CHANGES_ON_CASH_AND_CASH_EQUIVALENTS",
        "NET_INCREASE_IN_CASH_AND_EQUIVALENTS", "ADD:THE_BALANCE_OF_CASH_AND_CASH_EQUIVALENTS",
        "END_OF_TERM_CASH_AND_CASH_EQUIVALENTS_BALANCE", "NET_PROFIT",
        "PROFIT_AND_LOSS_OF_MINORITY_SHAREHOLDERS", "ASSET_IMPAIRMENT_PREPARATION",
        "FIXED_ASSETS_DEPRECIATION,DEPLETION_OF_OIL_AND_GASASSETS,DEPRECIATION_OF_PRODUCTION_MATERIALS",
        "AMORTIZATION_OF_INTANGIBLE_ASSETS",
        "AMORTIZATION_OF_LONG_TERM_APPORTIONED_EXPENSES",
        "DISPOSE_OF_LOSS_OF_FIXED_ASSETS,INTANGIBLE_ASSETS_AND_OTHER_LONG_TERM_ASSETS", "LOSS_OF_FIXED_ASSETS",
        "FINANCIAL_COST", "INVESTMENT_LOSS",
        "LOSS_OF_FAIR_VALUE_CHANGE", "REDUCTION_IN_INVENTORY", "DEFERRED_INCOME_TAX_ASSETS",
        "INCREASE_OF_DEFERRED_INCOME_TAX_LIABILITIES", "REDUCTION_OF_OPERATIONAL_RECEIVABLE_PROJECTS",
        "AN_INCREASE_IN_OPERATIONAL_PROJECTS", "OTHER", "OPERATING_ACTIVIITIES_PRODUCE_NET_CASH_FLOW",
        "DEBT_TO_CAPITAL", "SWITCHING_COMPANY_BONDS_THAT_EXPIRE_WITHIN_ONE_YEAR",
        "FINANCING_IS_RENTED_INTO_FIXED_ASSETS", "FINAL_BALANCE_OF_CASH", "INITIAL_BALANCE_OF_CASH",
        "FINAL_BALANCE_OF_CASH_EQUIVALENTS", "THE_INITIAL_BALANCE_OF_THE_CASH_EQUIVALENTS",
        'INCREASE_THE_AMOUNT_OF_CASH_PAID_BY_PLEDGE_AND_FIX_DEPOSIT',
        'AMONG_THEM:THE_DIVIDEND_AND_PROFIT_PAID_BY_SUBSIDIARY_TO_MINORITY_SHAREHOLDERS',
        'AMONG_THEM:SUBSIDIARY_COMPANY_ABSORBS_THE_CASH_RECEIVED_BY_THE_MINORITY_SHAREHOLDERS',
        'NET_INCREASE_IN_MORTGAGE_LOAN', 'REDUCTIONG_OF_COMPLETED_UNSETTLED_PAYMENTS(REDUCE:INCREASE)',
        'CHASH_RECEIVED_FROM_THE_LOAN', 'CASH_FOR_PURCHASE_OF_GOODS_AND_LABOR_SERVICES',
        'INSURED_SAVINGS_AND_INVESTMENT_FUND_NET_INCREASE', 'UNIDENTIFIED_INVESTMENT_LOSSES',
        'EXPECTED_LIABILITIES', 'CASH_PAYMENT_OF_POLICY_BONUS', 'SELLING_CASH_RECEIVED_FROM_SERVICES',
        'AN_INCREASE_IN_THE_ADVANCE_COAST', 'CASH_PAID_FOR_THE_ORIGINAL_INSURANCE_CONTRACT',
        'RECEIPT_OF_REINSURANCE_NET_CASH', 'NET_INCREASE_IN_CASH_AND_CASH_EQUIVALENTS',
        'NET_CASH_PAID_BY_SUBSIDIARY_AND_OTHER_BUSINESS_UNITS', 'REDUCED_COAST_OF_APPORTIONED',
        'AN_INCREASE_IN_THE_SETTLEMENT_OF_UNCOMPLETED_FUNDS(REDUCE:REDUCTION)',
        'INCREASE_IN_DEFERRED_INCOME(REDUCE:REDUCTION)', 'NET_INCREASE_IN_REPO_BUSINESS_FUNDS',
        'THE_TAX_AND_FEE_RECEIVED', 'DISPOSAL_OF_NET_INCREASE_IN_TRANSACTION_FINANCIAL_ASSETS',
        'REDUCTION_OF_CASH_RECEIVED_BY_PLEDGE_AND_FIX_DEPOSIT', 'NET_INCREASE_OF_LOANS',
        'CASH_RECEIVED_FROM_THE_PERMIUMS_OF_THE_ORIGINAL_INSURANCE_CONTRACT'
    ]
    CJ_zd_list = ['INCREASE_THE_AMOUNT_OF_CASH_PAID_BY_PLEDGE_AND_FIX_DEPOSIT',
                  'AMONG_THEM:THE_DIVIDEND_AND_PROFIT_PAID_BY_SUBSIDIARY_TO_MINORITY_SHAREHOLDERS',
                  'AMONG_THEM:SUBSIDIARY_COMPANY_ABSORBS_THE_CASH_RECEIVED_BY_THE_MINORITY_SHAREHOLDERS',
                  'NET_INCREASE_IN_MORTGAGE_LOAN', 'REDUCTIONG_OF_COMPLETED_UNSETTLED_PAYMENTS(REDUCE:INCREASE)',
                  'CHASH_RECEIVED_FROM_THE_LOAN', 'CASH_FOR_PURCHASE_OF_GOODS_AND_LABOR_SERVICES',
                  'INSURED_SAVINGS_AND_INVESTMENT_FUND_NET_INCREASE', 'UNIDENTIFIED_INVESTMENT_LOSSES',
                  'EXPECTED_LIABILITIES', 'CASH_PAYMENT_OF_POLICY_BONUS', 'SELLING_CASH_RECEIVED_FROM_SERVICES',
                  'AN_INCREASE_IN_THE_ADVANCE_COAST', 'CASH_PAID_FOR_THE_ORIGINAL_INSURANCE_CONTRACT',
                  'RECEIPT_OF_REINSURANCE_NET_CASH', 'NET_INCREASE_IN_CASH_AND_CASH_EQUIVALENTS',
                  'NET_CASH_PAID_BY_SUBSIDIARY_AND_OTHER_BUSINESS_UNITS', 'REDUCED_COAST_OF_APPORTIONED',
                  'AN_INCREASE_IN_THE_SETTLEMENT_OF_UNCOMPLETED_FUNDS(REDUCE:REDUCTION)',
                  'INCREASE_IN_DEFERRED_INCOME(REDUCE:REDUCTION)', 'NET_INCREASE_IN_REPO_BUSINESS_FUNDS',
                  'THE_TAX_AND_FEE_RECEIVED', 'DISPOSAL_OF_NET_INCREASE_IN_TRANSACTION_FINANCIAL_ASSETS',
                  'REDUCTION_OF_CASH_RECEIVED_BY_PLEDGE_AND_FIX_DEPOSIT', 'NET_INCREASE_OF_LOANS',
                  'CASH_RECEIVED_FROM_THE_PERMIUMS_OF_THE_ORIGINAL_INSURANCE_CONTRACT']
    data = response.text.strip().split("\n")
    tmp_list = []
    for i in range(len(data)):
        if i in [1, 2, 17, 29, 31, 33, 38, 39, 47, 51, 52, 53, 55, 56, 59, 61, 66, 67, 68, 70, 71, 72, 73, 74, 75, 80,
                 81, 84, 85, 86, 90, 95]:
            continue
        tmp_list.append(data[i].strip().split("\t")[1:])
    for j in range(len(CJ_zd_list)):
        tmp_list.append(["0" for c in range(len(data[0]))])
    xjllb_data = [{j[0]: j[1] for j in i} for i in (zip(zd_list, it) for it in list(zip(*tmp_list)))]
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

def zcfzb(response, stock_code):
    zd_list = ["YEAREND_DATE", "CURRENCY_CAPITAL", "DEMOLITION_CAPITAL", "TRANSACTIONAL_ASS", "DERIVATIVE_ASS",
               "BUY_BACK_THE_SALE_OF_FINANCIAL_ASS",
               "INTEREST_DECIVABLE", "LOANS_AND_ADVANCES", "FINANCIAL_ASSETS_AVAILABLE_FOR_SALE",
               "HOLDING_TO_MATURIY_INVESTMENT", "LONG_TERM_EQUITY_INVESTMENT",
               "FIXED_ASSETS", "IMMATERIAL_ASSETS", "GOODWILL", "DEFERRED_TAX_ASSETS", "INVESTMENT_REAL_ESTATE",
               "OTHER_NON_CURRENT_ASSETS", "TOTAL_ASSETS",
               "BORROWING_FROM_THE_CENTRAL_BANK", "LOANS_FROM_OTHER_BANKS", "DERIVATIVE_FINANCIAL_LIABILTIES",
               "TRANSACTIONAL_FINANCIAL_LIABILTIES", "FINANCIAL_ASSETS_SOLD_FOR_REPURCHASE",
               "SALARY_PAYABLE_TO_EMPLOYEES", "TAX_PAYABLE", "INTEREST_PAYABLE", "ACCOUNTS_PAYABLE", "BONDS_PAYABLE",
               "DEFERRED_TAX_LIABILITY", "OTHER_NON_CURRENT_LIABILTIES",
               "TOTAL_LIABILITIES", "PAID_IN_CAPITAL", "CAPITAL_SURPLUS", "SURPLUS_PUBLIC_ACCUMULATION",
               "UNDISTRIBUTED_PROFIT", "GENERAL_RISK_RESERVE", "CONVERSION_BALANCE_OF_FOREIGN_CURRENCY_STATEMENTS",
               "TOTAL_EQUITY_ATTRIBUTABLE_TO_SHAREHOLDERS_OF_THE_PARENT_COMPANY",
               "MINORITY_SHAREHOLDER_RIGHT_AND_INTERESTS", "OWNER_S_EQUITY", "LIABILITIES_AND_OWNER_S_EQUITY",
               'NET_VALUE_OF_FIXED_ASSETS', 'BUY_ANDSELL_SECURITIES_BY_PROXY', 'DOMESTIC_TICKET_SETTLAEMENT',
               'ACCOUNTS_RECEIVABLE', 'STOCK', 'TOTAL_NON_CURRENT_ASSETS', 'RESERVE_CONTRACT_REINSURANCE_REVEIVABLE',
               'FIXED_ASSETS_IMPAIRMENT_RESERVES', 'ACCOUNT_PAYABLE_SPECIAL_FUNDS', 'INTERNATIONAL_TICKET_SETTLAEMENT',
               'ACTING_UNDERWEITING_SECURITIES', 'OTHER_DECIVABLES', 'OTHER_CURRENT_LIABILITIES', 'INTERNAL_PAYABLES',
               'CASH_DEPOSIT_AS_COLLATERAL_DECIVABLE', 'TOTAL_NON_CURRENT_LIABILTIES', 'LONG_TERM_PREPAID_EXPENSES',
               'OIL_AND_GAS_ASSETS', 'PUBLIC_WELFARE_BIOLOGICAL_ASSETS', 'OTHER_LONG_TERM_INVESTMENT',
               'ACCOUNT_REINSURANCE_RECEIVABLE', 'SHORT_TERM_BONDS_PAYABLE', 'ACCOUNTS_PAYABLE_REINSURANCE',
               'UNCERTAIN_INVESTMENT_LOSS', 'OTHER_ACCOUNTS_PAYABLES', 'SPECIAL_RESERVE', 'MARGIN_PAYABLE',
               'ADVANCE_PAYMENT', 'NON_CURRENT_ASSETS_DUE_WITHIN_ONE_YEAR', 'TOTAL_CURRENT_LIABILITIES',
               'INTERNAL_RECEIVABLE', 'CLEAR_OF_FIXED_ASSETS', 'BILL_PAYABLE', 'SETTLEMENT_RESERVE',
               'ACCUMULATED_DEPRECIATION', 'DIVIDENDS_PAYABLE', 'ENGINEERING_MATERIALS', 'BILL_RECEIVABLE',
               'EXPORT_REBATE_DECIVABLE', 'PENDING_CURRENT_ASSETS_PROFIT_LOSS', 'ACCRUED_EXPENSES',
               'DEVELOPMENT_AMOUNT_OF_EXPENDITURE', 'OTHER_CURRENT_ASSETS', 'SUBSIDYS_DECIVABLE',
               'PROJECTED_NON)CURRENT_LIABILITIES', 'DEFERRED_EXPENSES', 'REDUCE:STOCK_THIGH', 'DIVIDEND_DECIVABLE',
               'OTHER_PAYABLE', 'DEPOSIT_TAKING_AND_INTERBANK_DEPOSIT', 'LONG_TERM_DEFERRED_INCOME',
               'LONG_TERM_RECIVABLES', 'NON_CURRENT_LIABILITIES_DUE_WITHIN_ONE_YEAR', 'ORIGINAL_VALUE_OF_FIXED_ASSETS',
               'QUASI_DISTRIBUTIVE_CASH)DIVIDEND', 'PROJECTED_CURRENT_LIABILITIES', 'RIGHT_OF_SPLIT_SHARE_CIRCULATION',
               'CONSTRUCTION_IN_PROCESS', 'DEPOSIT_RECEIVED', 'INSURANCE_CONTRACT_RESERVES', 'BIOLOGICAL_ASSETS',
               'LONG_TERM_LOAN', 'TOTAL_CURRENT_ASSETS', 'LONG_TERM_PAYABLES', 'MONEY_BORROWED_FOR_SHORT_TIME',
               'PREMIUMS_RECEIVABLE', 'DEFERRED_INCOME', 'HANDING_FEE_AND_COMMISSION',
               ]
    CJ_zd_list = ['NET_VALUE_OF_FIXED_ASSETS', 'BUY_ANDSELL_SECURITIES_BY_PROXY', 'DOMESTIC_TICKET_SETTLAEMENT',
                  'ACCOUNTS_RECEIVABLE', 'STOCK', 'TOTAL_NON_CURRENT_ASSETS', 'RESERVE_CONTRACT_REINSURANCE_REVEIVABLE',
                  'FIXED_ASSETS_IMPAIRMENT_RESERVES', 'ACCOUNT_PAYABLE_SPECIAL_FUNDS',
                  'INTERNATIONAL_TICKET_SETTLAEMENT',
                  'ACTING_UNDERWEITING_SECURITIES', 'OTHER_DECIVABLES', 'OTHER_CURRENT_LIABILITIES',
                  'INTERNAL_PAYABLES',
                  'CASH_DEPOSIT_AS_COLLATERAL_DECIVABLE', 'TOTAL_NON_CURRENT_LIABILTIES', 'LONG_TERM_PREPAID_EXPENSES',
                  'OIL_AND_GAS_ASSETS', 'PUBLIC_WELFARE_BIOLOGICAL_ASSETS', 'OTHER_LONG_TERM_INVESTMENT',
                  'ACCOUNT_REINSURANCE_RECEIVABLE', 'SHORT_TERM_BONDS_PAYABLE', 'ACCOUNTS_PAYABLE_REINSURANCE',
                  'UNCERTAIN_INVESTMENT_LOSS', 'OTHER_ACCOUNTS_PAYABLES', 'SPECIAL_RESERVE', 'MARGIN_PAYABLE',
                  'ADVANCE_PAYMENT', 'NON_CURRENT_ASSETS_DUE_WITHIN_ONE_YEAR', 'TOTAL_CURRENT_LIABILITIES',
                  'INTERNAL_RECEIVABLE', 'CLEAR_OF_FIXED_ASSETS', 'BILL_PAYABLE', 'SETTLEMENT_RESERVE',
                  'ACCUMULATED_DEPRECIATION', 'DIVIDENDS_PAYABLE', 'ENGINEERING_MATERIALS', 'BILL_RECEIVABLE',
                  'EXPORT_REBATE_DECIVABLE', 'PENDING_CURRENT_ASSETS_PROFIT_LOSS', 'ACCRUED_EXPENSES',
                  'DEVELOPMENT_AMOUNT_OF_EXPENDITURE', 'OTHER_CURRENT_ASSETS', 'SUBSIDYS_DECIVABLE',
                  'PROJECTED_NON)CURRENT_LIABILITIES', 'DEFERRED_EXPENSES', 'REDUCE:STOCK_THIGH', 'DIVIDEND_DECIVABLE',
                  'OTHER_PAYABLE', 'DEPOSIT_TAKING_AND_INTERBANK_DEPOSIT', 'LONG_TERM_DEFERRED_INCOME',
                  'LONG_TERM_RECIVABLES', 'NON_CURRENT_LIABILITIES_DUE_WITHIN_ONE_YEAR',
                  'ORIGINAL_VALUE_OF_FIXED_ASSETS',
                  'QUASI_DISTRIBUTIVE_CASH)DIVIDEND', 'PROJECTED_CURRENT_LIABILITIES',
                  'RIGHT_OF_SPLIT_SHARE_CIRCULATION',
                  'CONSTRUCTION_IN_PROCESS', 'DEPOSIT_RECEIVED', 'INSURANCE_CONTRACT_RESERVES', 'BIOLOGICAL_ASSETS',
                  'LONG_TERM_LOAN', 'TOTAL_CURRENT_ASSETS', 'LONG_TERM_PAYABLES', 'MONEY_BORROWED_FOR_SHORT_TIME',
                  'PREMIUMS_RECEIVABLE', 'DEFERRED_INCOME', 'HANDING_FEE_AND_COMMISSION']
    data = response.text.strip().split("\n")
    tmp_list = []
    for i in range(len(data)):
        if i in [1, 2, 4, 6, 12, 16, 23, 24, 26, 27, 32, 37, 40, 43, 45, 46, 48, 49, 54]:
            continue
        print(data[i].strip().split("\t"))
        tmp_list.append(data[i].strip().split("\t")[1:])
    for j in range(len(CJ_zd_list)):
        tmp_list.append(["0" for c in range(len(data[0]))])
    zcfzb_data = [{j[0]: j[1] for j in i} for i in (zip(zd_list, it) for it in list(zip(*tmp_list)))]

    # db_report_date = LmInnerReportDBMgr.get_code('lm_stock_data', stock_code, 'financial_report_date')
    # if db_report_date:
    #     if date_turn_timestamp(db_report_date, zcfzb_data[0]['YEAREND_DATE']):
    #         LmInnerReportDBMgr.save_set_result('lm_stock_data', {'code': stock_code}, 'report.zcfzb',
    #                                            zcfzb_data)
    #         LmInnerReportDBMgr.save_insert_result('lm_stock_data',
    #                                               {'code': stock_code,
    #                                                'financial_report_date': zcfzb_data[0]['YEAREND_DATE'],
    #                                                })
    # else:
    #     LmInnerReportDBMgr.save_insert_result('lm_stock_data',
    #                                           {'code': stock_code,
    #                                            'financial_report_date': zcfzb_data[0]['YEAREND_DATE'],
    #                                            'report': {'zcfzb': zcfzb_data}})


def lrb(response, stock_code):
    '''

    :param response: 利润表的数据 str
    :param stock_code: 股票代码
    :return:
    '''
    zd_list = ["YEAREND_DATE", "GROSS_REVENUE", "INTEREST_REVENUE", "INTEREST_EXPENSE",
               "POUNDAGE_AND_COMMISSION_INCOME", "POUNDAGE_AND_COMMISSION_EXPENSES",
               "EXCHANGE_EARNINGS", "INVESTMENT_PROFIT",
               "INVESTMENT_INCOME_FOR_VENTURES_AND_JOINT_VENTURES", "FAIR_VALUE_CHANGE_INCOME", "OTHER_BUSINESS_INCOME",
               "TOTAL_OPERATING_COST", "BUSINESS_TAXES_AND_SURCHARGES", "SELLING_EXPENSES", "ASSETS_IMPAIRMENT_LOSS",
               "OTHER_BUSINESS_COSTS",
               "OPERATING_PROFIT", "NON_BUSINESS_INCOME", "NON_BUSINESS_ESPENDITURE", "TOTAL_PROFIT",
               "INCOME_TAX_EXPENSE", "NET_MARGIN",
               "VEST_IN_PARENT_COMPANY_PROPRIETOR_NET_MARGIN", "MINORITY_SHAREHOLDER_PROFIT_AND_LOSS",
               "BASIC_PER_SHARE_PROFIT", "BILUTED_EARNINGS_PER_SHARE",
               'COST_IN_BUSINESS', 'REINSURANCE_EXPENSES', 'SUBSIDY_INCOME',
               'EXTRACT_INSURANCE_CONTRACT_RESERVE_NET', 'EXPENDITURE_DIVIDEND_POLICY',
               'SALES_INCOME_OF_REAL_ESTATE', 'UNCINFIRMED_INVESTMENT_LOSS',
               'NET_PROFIT_OF_THE_MERGED_PARTY_BEFORE_MERGER', 'RESEARCH_AND_DEV_ELOPMENT_COST',
               'SALE_COST_OF_REAL_ESTATE', 'OTHER_BUSINESS_PROFITS', 'EARNED_PREMIUM', 'MANAGEMENT_EXPENSES',
               'OPERATIONG_RECEIPT', 'MANAGED_INCOME', 'FUTURES_PROFIT_AND_LOSS', 'SURRENDER_VALUE',
               'PAYMENT_NET_EXPENDITURE', 'DISPOSAL_LOSS_OF_NON_CURRENT_ASSETS', 'FINANCIAL_EXPENSES',
               ]
    CJ_zd_list = ['COST_IN_BUSINESS', 'REINSURANCE_EXPENSES', 'SUBSIDY_INCOME',
                  'EXTRACT_INSURANCE_CONTRACT_RESERVE_NET', 'EXPENDITURE_DIVIDEND_POLICY',
                  'SALES_INCOME_OF_REAL_ESTATE', 'UNCINFIRMED_INVESTMENT_LOSS',
                  'NET_PROFIT_OF_THE_MERGED_PARTY_BEFORE_MERGER', 'RESEARCH_AND_DEV_ELOPMENT_COST',
                  'SALE_COST_OF_REAL_ESTATE', 'OTHER_BUSINESS_PROFITS', 'EARNED_PREMIUM', 'MANAGEMENT_EXPENSES',
                  'OPERATIONG_RECEIPT', 'MANAGED_INCOME', 'FUTURES_PROFIT_AND_LOSS', 'SURRENDER_VALUE',
                  'PAYMENT_NET_EXPENDITURE', 'DISPOSAL_LOSS_OF_NON_CURRENT_ASSETS', 'FINANCIAL_EXPENSES']
    tmp_list = []
    data = response.text.strip().split("\n")
    for i in range(len(data)):
        if i == 1 or i == 3 or i == 6 or i == 27 or i >= 30:
            continue
        tmp_list.append(data[i].strip().split("\t")[1:])
    for j in range(len(CJ_zd_list)):
        tmp_list.append(["0" for c in range(len(data[0]))])
    lrb_data = [{j[0]: j[1] for j in i} for i in (zip(zd_list, it) for it in list(zip(*tmp_list)))]
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


if __name__ == '__main__':
    for i in ['600205']: #'600205'600002
        history_financial_crawler(i)
    # c = [1,2,3,4]
    # d = [2,3,4,5]
    # f = [3,4,5,6]
    # dd = [c,d,f]
    # for i in zip(*dd):
    #     print(i)
    # res = requests.get('http://money.finance.sina.com.cn/corp/go.php/vDOWN_BalanceSheet/displaytype/4/stockid/600000/ctrl/all.phtml',headers=headers,)
    # print(res.text)
    # lrb(1, 2)
