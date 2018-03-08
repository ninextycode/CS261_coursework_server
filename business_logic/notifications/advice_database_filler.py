import sys; print('Python %s on %s' % (sys.version, sys.platform))
sys.path.extend(['/server',
                 '/server/data_providers/data_wrappers/mysql_scripts'])


import business_logic.notifications.adviser as adviser
import config

adv: adviser.Adviser = adviser.Adviser.get_instance()

for company in config.companies.keys():
    print(company)
    adv.add_subscription_stock(company, 0.1)

for industry_id in config.industries.keys():
    print(config.industries[industry_id])
    if len(config.industry_companies[industry_id]) > 2:
        adv.add_subscription_industry(industry_id)