import os
import inspect


default_number_of_speech_rec_alternatives = 10

static_folder = os.path.join(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))), 'html_pages')

templates_folder = os.path.join(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))), 'templates')


port = 7004
local = False

if local:
    mysql_host = "localhost"
    mongodb_host = "localhost"
else:
    mongodb_host = "mongodb"
    mysql_host = "mysql"


news_summary_address = 'http://localhost:{}/news.html'.format(port)



companies = {
    'III': ['3i Group', '3I GRP'],
    'ABF': ['Associated Brititsh Foods', 'A.B.FOOD'],
    'ADM': ['Admiral Group', 'ADMIRAL GRP'],
    'AAL': ['Anglo American'],
    'ANTO': ['Antofagasta'],
    'AHT': ['Ashtead Group', 'ASHTEAD GRP.'],
    'AZN': ['ASTRAZENCA'],
    'AV.': ['Aviva'],
    'BA.': ['BAE systems', 'BAE SYS.'],
    'BARC': ['Barclays'],
    'BDEV': ['Barratt Developments', 'BARRATT DEVL.'],
    'BKG': ['Berkeley Group Holdings', 'BERKELEY GP. HLD'],
    'BLT': ['BHP BILLITON'],
    'BP':  ['British Petroleum', 'BP'],
    'BATS': ['British American Tobacco', 'BR.AMER.TOB.'],
    'BLND': ['British Land', 'BR.LAND'],
    'BT.A': ['BT GROUP'],
    'BNZL': ['BUNZL'],
    'BRBY': ['BURBERRY GRP', 'Burberry Group'],
    'CCL': ['CARNIVAL'],
    'CNA': ['CENTRICA'],
    'CCH': ['Coca Cola Hellenic Bottling Company', 'COCACOLA HBC AG'],
    'CPG': ['COMPASS GROUP'],
    'CRH': ['CRH'],
    'CRDA': ['Croda', 'CRODA INTL.', 'Croda International'],
    'DCC': ['DCC'],
    'DGE': ['DIAGEO'],
    'DLG': ['DIRECT LINE'],
    'EZJ': ['EASY JET'],
    'EVR': ['EVRAZ'],
    'EXPN': ['EXPERIAN'],
    'FERG': ['FERGUSON'],
    'FRES': ['FRESNILLO'],
    'GFS': ['G4S'],
    'GKN': ['GKN'],
    'GSK': ['Glaxo Smith Kline', 'GLAXOSMITHKLINE', 'Smith'],
    'GLEN': ['GLENCORE'],
    'HLMA': ['HALMA'],
    'HMSO': ['HAMMERSON'],
    'HL.': ['Hargreaves Lansdown', 'HARGREAVES LANS'],
    'HSBA': ['HSBC Holdings', 'HSBC HLDGS.UK', 'HSBC'],
    'IMB': ['Imperial Brands', 'IMP.BRANDS'],
    'INF': ['INFORMA'],
    'IHG': ['INTERCON. HOTEL', 'Intercontinental Hotels Group'],
    'ITRK': ['INTERTEK GROUP'],
    'IAG': ['International Consolidated Airlines Group', 'INTL CONSOL AIR'],
    'ITV': ['ITV'],
    'JMAT': ['JOHNSON MATTHEY', 'Matthey', 'JM'],
    'JE.': ['JUST EAT'],
    'KGF': ['KINGFISHER'],
    'LAND': ['Land Securities', 'LAND SECS.'],
    'LGEN': ['Legal and General', 'LEGAL&GEN.'],
    'LLOY': ['Lloyds', 'LLOYDS GRP.'],
    'LSE': ['London Stock Exchange', 'LON.STK.EXCH'],
    'MKS': ['Marks and Spencer', 'MARKS & SP.'],
    'MDC': ['MEDICLINIC'],
    'MCRO': ['MICRO FOCUS'],
    'MNDI': ['MONDI'],
    'MRW': ['Morrison', 'MORRISON (WM)'],
    'NG.': ['NATIONAL GRID'],
    'NXT': ['NEXT'],
    'NMC': ['NMC HEALTH'],
    'OML': ['OLD MUTUAL'],
    'PPB': ['Paddy Power Betfair', 'PADDY PWR BET'],
    'PSON': ['PEARSON'],
    'PSN': ['PERSIMMON'],
    'PRU': ['PRUDENTIAL'],
    'RRS': ['Randgold Resources Limited', 'RANDGOLD RES.'],
    'RDSA': ['Royal Dutch Shell', 'RDS \'A\'', 'RDS A', 'Royal Dutch Shell A', 'Royal Shell'], # test
    'RDSB': ['Royal Dutch Shell', 'RDS \'B\'', 'RDS B', 'Royal Dutch Shell B', 'Royal Shell'],
    'RB.': ['Reckitt Benckiser Group', 'RECKITT BEN. GP'],
    'REL': ['RELX'],
    'RTO': ['Rentokil Initial', 'RENTOKIL INITL.'],
    'RIO': ['RIO TINTO'],
    'RR.': ['Rolls Royce', 'ROLLS-ROYCE HLG'],
    'RBS': ['Royal Bank of Scotland', 'ROYAL BANK SCOT', 'RBS'],
    'RSA': ['RSA Insurance', 'RSA INS.'],
    'SGE': ['Sage Group', 'SAGE GRP.'],
    'SBRY': ['Sainsbury\'s', 'SAINSBURY(J)', 'J Sainsbury'],
    'SDR': ['SCHRODERS'],
    'SMT': ['SCOTTISH MORT'],
    'SGRO': ['SEGRO'],
    'SVT': ['SEVERN TRENT'],
    'SHP': ['SHIRE'],
    'SKY': ['SKY PLC', 'Sky'],
    'SN.': ['Smith and Nephew', 'SMITH&NEPHEW', 'Smith'], # test all four smith
    'SMDS': ['DS Smith', 'SMITH(DS)', 'Smith'],
    'SMIN': ['Smith Group', 'SMITHS GROUP', 'Smith'],
    'SKG': ['Smurfit Kappa', 'SMURFIT KAP.', 'Smurfit'],
    'SSE': ['Scottish and Southern Energy', 'SSE'],
    'STJ': ['St James Place Wealth Management', 'ST.JAMES\'S PLAC', 'St James Place'],
    'STAN': ['Standard Chartered', 'STAND.CHART'],
    'SLA': ['Standard Life Aberdeen', 'STD LIFE ABER', 'Standard Life'],
    'TW.': ['TAYLOR WIMPEY'],
    'TSCO': ['Tesco'],
    'TUI': ['Tui', 'TUI AG'],
    'ULVR': ['UNILEVER'],
    'UU.': ['United Utilities', 'UTD.UTILITES'],
    'VOD': ['Vodafone', 'VODAFONE GRP.'],
    'TWB': ['WHITBREAD'],
    'WWP': ['WWP']
}


def get_ticker(name):
    global companies
    for ticker in companies.keys():
        if name.lower() in [alternative.lower() for alternative in companies[ticker]]:
            return ticker
    return None

industries = {
    1: ['Aerospace & Defence', 'Aerospace', 'Defence'],
    2: ['Alternative Energy'],
    3: ['Automobiles & Parts', 'Automobiles and Parts', 'Automobile', 'Automobiles', 'Car', 'Parts'],
    4: ['Banks'],
    5: ['Beverages'],
    6: ['Chemicals'],
    7: ['Construction & Materials', 'Construction and Materials', 'Construction', 'Materials'],
    8: ['Electricity'],
    9: ['Electronic & Electrical Equipment', 'Electronic Equipment', 'Electrical Equipment', 'Electronic', 'Electrical'],
    10: ['Equity Investment Instruments', 'Equity', 'Equity Investment'],
    11: ['Financial Services'],
    12: ['Fixed Line Telecommunications', 'Fixed Line'],
    13: ['Food & Drug Retailers', 'Food and Drug Retailers', 'Food Retailers', 'Drug Retailers'],
    14: ['Food Producers'],
    15: ['Forestry & Paper', 'Forestry and Paper', 'Forestry', 'Paper'],
    16: ['Gas, Water & Multiutilities', 'Gas and Water and Mulitutilities', 'Gas', 'Water', 'Multiutilities'],
    17: ['General Industrials', 'Industrials'],
    18: ['General Retailers', 'Retailers'],
    19: ['Health Care Equipment & Services', 'Health Care Equipment and Services', 'Health Care'],
    20: ['Household Goods & Home Construction', 'Household Goods and Home Construction', 'Household', 'Home Construction'],
    21: ['Industrial Engineering', 'Engineering'],
    22: ['Industrial Metals & Mining', 'Industrial Metals and Mining', 'Metals', 'Mining'],
    23: ['Industrial Transportation', 'Transportation'],
    24: ['Leisure Goods', 'Leisure'],
    25: ['Life Insurance'],
    26: ['Media'],
    27: ['Mining'],
    28: ['Mobile Telecommunications'],
    29: ['Nonequity Investment Instruments', 'Nonequity Investment'],
    30: ['Nonlife Insurance', 'Non-life Insurance'],
    31: ['Oil & Gas Producers', 'Oil and Gas Producers', 'Oil Producers', 'Gas Producers'],
    32: ['Oil Equipment & Services', 'Oil Equipment and Services', 'Oil Equipment', 'Oil Services'],
    33: ['Personal Goods'],
    34: ['Pharmaceuticals & Biotechnology', 'Pharmaceuticals and Biotechnology', 'Pharmaceutical', 'Biotechnology'],
    35: ['Real Estate Investment & Services', 'Real Estate Investment and Services', 'Real Estate Investment', 'Real Estate Services'],
    36: ['Real Estate Investment Trusts'],
    37: ['Software & Computer Services', 'Software and Computer Services', 'Software Services', 'Computer Services', 'Software', 'Computer'],
    38: ['Support Services'],
    39: ['Technology Hardware & Equipment', 'Technology Hardware and Equipment', 'Technology Hardware', 'Hardware', 'Technology Equipment'],
    40: ['Tobacco'],
    41: ['Travel & Leisure', 'Travel & Leisure', 'Travel', 'Leisure'],
}

industry_companies = {
    1: ['BA.', 'RR.'],
    2: [],
    3: ['GKN'],
    4: ['BARC', 'HSBA', 'LLOY', 'RBS', 'STAN'],
    5: ['CCH', 'DGE'],
    6: ['CRDA', 'JMAT'],
    7: ['CRH'],
    8: ['SSE'],
    9: ['HLMA'],
    10: ['SMT'],
    11: ['III', 'HL.', 'LSE', 'SDR', 'SLA'],
    12: ['BT.A'],
    13: ['MRW', 'SBRY', 'TSCO'],
    14: ['ABF'],
    15: ['MNDI'],
    16: ['CNA', 'NG.', 'SVT', 'UU.'],
    17: ['SMDS', 'SMIN', 'SKG'],
    18: ['JE.', 'KGF', 'MKS', 'NXT'],
    19: ['MDC', 'NMC', 'SN.'],
    20: ['BDEV', 'BKG', 'PSN', 'RB.', 'TW.'],
    21: [],
    22: ['EVR'],
    23: [],
    24: [],
    25: ['AV.', 'LGEN', 'OML', 'PRU', 'STJ'],
    26: ['INF', 'ITV', 'PSON', 'REL', 'SKY', 'WPP'],
    27: ['AAL', 'ANTO', 'BLT', 'FRES', 'GLEN', 'RRS', 'RIO'],
    28: ['VOD'],
    29: [],
    30: ['ADM', 'DLG', 'RSA'],
    31: ['BP.', 'RDSA', 'RDSB'],
    32: [],
    33: ['BRBY', 'ULVR'],
    34: ['AZN', 'GSK', 'SHP'],
    35: [],
    36: ['BLND', 'HMSO', 'LAND', 'SGRO'],
    37: ['MCRO', 'SGE'],
    38: ['AHT', 'BNZL', 'DCC', 'EXPN', 'FERG', 'GFS', 'ITRK', 'RTO'],
    39: [],
    40: ['BATS'],
    41: ['CCL', 'CPG', 'EZJ', 'IHG', 'IAG', 'PPB', 'TUI', 'WTB'],
}

