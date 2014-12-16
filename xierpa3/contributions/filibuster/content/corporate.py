# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#    xierpa server
#    Copyright (c) 2014+  buro@petr.com, www.petr.com, www.xierpa.com
#
#    X I E R P A  3
#    Distribution by the MIT License.
#
# -----------------------------------------------------------------------------
#
#    Contributed by Erik van Blokland and Jonathan Hoefler
#    Original from filibuster.
#
"""
        history
        Corporation names, corporate related text
--------------------------------------------------------------------
3.0.0    - split all the content into babycontents
evb        - note: only one dictionary named 'content' allowed per module
        this limitation is to speed up loading

3.0.1    - added some more collected mottos for filibuster
evb
"""

__version__ = '3.0.1'
__author__ = "someone"

# ------------------------------------------------------
#    corporate
#


content = {
    'business_headline':['<#^,corporate_headline#>','<#^,corporate_biz_news_headline#>','<#^,corporate_news_headline#>',],
    'business_section':['Business','Business','Business','Business','Corporate','Stock','Stock','Trade','International',],
    'corporate_headline': [
        '<#^,j_thing#>', 'New <#odd_material#>',
        '<#^,j_thing#>', 'Valuable <#odd_material#>',
        '<#^,j_thing#>', 'Sustainable <#odd_material#>',
        '<#^,auction_antiques_adj#> <#auction_antiques_material#>',
        '<#^,auction_antiques_adj#> <#auction_antiques_material#>',
        '<#^,bank_co_ptr#>', '<#^,startup_company#>',
    ],
    'corporate_biz_news_headline': [
        '<#company#> <#verb_cooperates#> <#j_thing#>',
        u'<#company#>’s <#j_thing#> <#prod_accolades#> at <#events_tradeshow#>',
    ],
    'corporate_partnership_headline': [
        '<#company#> announces <#j_noun_gerund#> <#j_noun_pl#> with <#company#>',
    ],
    'corporate_news_headline': [
        '<#corporate_newproduct_headline#>',
        '<#corporate_partnership_headline#>',
    ],
    'corporate_newproduct_headline': [
        '<#jargon#> <#j_thing#> <#prod_accolades#> at <#events_corporate#>',
        u'<#company#>’s <#jargon#> <#prod_accolades#> at <#events_tradeshow#>',
        u'<#events_tradeshow#>: <#company#>’s <#jargon#> <#prod_accolades#>',
        u'<#newssource#>: <#company#>’s <#jargon#> <#prod_accolades#> for <#j_thing#>',
    ],
    'corporate_prod_announcement_headline': [
        '<#company#> <#verb_introduces#> <#prod_upgrade#> <#jargon#> <#j_noun_sing#> <#j_noun_pl#>',
    ],
    'IPO1': [
        '<#p_business_px#><#p_business_name#><#p_business_sx#>',
    ],
    'IPO2': [
        '<#p_business_px#><#p_business_name#><#p_business_sx#><#p_corporateform#>',
    ],
    'bank_co_description_pl': [
        'banks',
        'financial institutions',
        'brokers',
        'capitalists',
    ],
    'bank_co_description_sing': [
        'a bank',
        'a financial institution',
        'broker',
        'investment bank',
    ],
    'bank_co_motto': [
        'More than a century of experience with your money.',
    ],
    'bank_co_ptr': [
        '<#creditcard#> 1.9% APR',
        'Mortgages',
        'Refinance the house!',
        'Retirement plan?',
        'Retiring?',
        'Made some money?',
        'Playing the markets?',
    ],
    'bank_company': [
        '<#p_USbank_px1#> <#p_USbank_px2#> <#usbank_name#>',
    ],
    'bank_companyparts': [
        '<#p_USbank_px1#>+<#p_USbank_px2#>+<#usbank_name#>',
    ],
    'company': [
        '<#IPO1#>',
        '<#IPO2#>',
    ],
    'company_consolidated': [
        '<#p_consolidatedbiz_px#><#p_consolidatedbiz_sx#>',
    ],
    'company_oldschool': [
        '<#p_oldbiz_px#> <#p_oldbiz_sx#><#p_oldbiz_corporateform#>',
    ],
    'events_conference': [
        '<#j_noun_gerund#><#p_events_number#>',
    ],
    'events_corporate': [
        '<#events_tradeshow#>',
        '<#events_conference#>',
    ],
    'events_tradeshow': [
        '<#p_events_tech_px#><#p_events_tech_sx#>',
    ],
    'filibuster_co_description_pl': [
        'incubator sites',
        'venture capitalists',
        'investment bankers',
        'online equity developers',
    ],
    'filibuster_co_description_sing': [
        'an incubator site',
        'a venture capitalist',
        'an investment banker',
        'an online equity developer',
    ],
    'filibuster_co_motto': [
        'We offer a fine selection of everything.',
        u'We’re huge.',
        'It will all be OK!',
        'Content is our department!',
        'We Power the Internet',
        'Yes, coming next is a motto maker',
        'We are the internet, you will be.',
        'Time capsule material.',
        'We want you to do the work for us.',
        'If it is out there, it is in here.',
        'Content is Power, We rule.',
        'Content is nothing.',
        'Content is for suckers',
        'Content is overrated.',
        u'It’s All Getting Better',
        u'Our internet kicks your internet’s assAuctions speak louder than words!',
    ],
    'filibuster_company': [
        'Filibuster.org',
    ],
    'filibuster_companyparts': [
        'Fili+buster+.org',
    ],
    'news_co_description_pl': [
        'wireservices',
        'press',
    ],
    'news_co_description_sing': [
        'a news service',
        'internet news',
        'press',
        'a bunch of reporters and an anchor',
    ],
    'news_co_motto': [
        'More news than is fit to... ehm, well, - more news than is fitting.',
    ],
    'news_co_n': [
        'News',
        'News',
        'News',
        'News',
        'Information',
        'Headlines',
        'Data',
        'Network',
    ],
    'news_co_px': [
        'e',
        'i',
        'Direct',
        'Internet',
        'Online',
        'Inter',
        'Cable',
        'Channel',
        'Sat',
        'Future',
        'Global',
        'World',
        'Central',
        'Universal',
        '<#names_last_patrician#>',
        'Your',
        'Direct',
        'Flash',
    ],
    'news_co_sx': [
        '.com',
        '.net',
        'Center',
        'Connection',
        'Update',
        'Desk',
    ],
    'news_company': [
        '<#news_co_px#><#news_co_n#><#news_co_sx#>',
    ],
    'news_companyparts': [
        '<#news_co_px#>+<#news_co_n#>+<#news_co_sx#>',
    ],
    'p_business_name': [
        'Brand',
        'Group',
        'Sale',
        'Biz',
        'Trust',
        'Bank',
        'Corp',
        'Auctions',
        'Vision',
        'Net',
        'Networking',
        'Trade',
        'Works',
        'Net',
    ],
    'p_business_px': [
        'i',
        'e',
        'go',
        'Inter',
        'Equi',
        'Hyper',
        'Cyber',
        'my',
        'get',
        'meta',
        'net',
        'web',
    ],
    'p_business_sx': [
        '.com',
        'online',
        'Now!',
        '2000',
    ],
    'p_consolidatedbiz_px': [
        'Nat',
        'Ameri',
        'West',
        'Sun',
        'Sky',
        'Trans',
        'Inter',
        'Tele',
        'Medi',
        'Bio',
    ],
    'p_consolidatedbiz_sx': [
        'Tel',
        'Tron',
        'Com',
        'Corp',
        'Tech',
    ],
    'p_corporateform': [
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        ' Inc.',
        ' Inc.',
        ' Inc.',
        ', Inc.',
        ' LLC',
        ' PLC',
        ' S.A.',
        ' GmBH',
    ],
    'p_events_number': [
        '2000',
        '00',
        '99',
        '3',
    ],
    'p_events_tech_px': [
        'Com',
        'Mac',
        'Ce',
        'Cyber',
        'PC',
    ],
    'p_events_tech_sx': [
        'dex',
        'World',
        'Bit',
        'View',
    ],
    'p_industries': [
        'Industry',
        'Manufacturing',
        'Mining',
        'Oil',
        'Automobiles',
        'Motors',
        'Steel',
        'Freight',
        'Pipe',
        'Oil &amp; Gas',
        'Forestry',
    ],
    'p_news_name': [
        'News',
        'Data',
        'Info',
        'Vision',
    ],
    'p_oldbiz_corporateform': [
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        ' Company',
        ' Corporation',
    ],
    'p_oldbiz_px': [
        'National',
        'US',
        'Western',
        'American',
        'Amalgamated',
        'Atlantic',
        'International',
        'Continental',
        'Consolidated',
    ],
    'p_oldbiz_sx': [
        'Telephone',
        'Electric',
        'Edison',
        'Electronics',
        'Communications',
        'Industry',
        'Payroll',
        'Data Processing',
        'Cash Register',
        'Calculator',
        'Appliance',
        'Machinery',
        'Underwriters',
        '<#p_industries#>',
    ],
    'portal_co_description_pl': [
        'portals',
        'communities',
        'search engines',
    ],
    'portal_co_description_sing': [
        'a portal',
        'an online community developer',
        'a search engine',
    ],
    'portal_co_motto': [
        'We will bury you with links.',
    ],
    'portal_co_n': [
        'Find',
        'Finder',
        'Things',
        'Planet',
        'WorldStreet',
        'Boulevard',
        'Place',
        'Mall',
        'Central',
        'Center',
        'Area',
        'Zone',
        'Personal',
        'AndMore',
    ],
    'portal_co_px': [
        'e',
        'i',
        'Direct',
        'Internet',
        'Online',
        'Inter',
        'More',
        'Your',
        'Everything',
        'All',
        'Entire',
        'My',
        'Community',
        'Global',
    ],
    'portal_co_sx': [
        '.com',
        '.net',
    ],
    'portal_company': [
        '<#portal_co_px#><#portal_co_n#><#portal_co_sx#>',
    ],
    'portal_companyparts': [
        '<#portal_co_px#>+<#portal_co_n#>+<#portal_co_sx#>',
    ],
    'prod_accolades': [
        'announced',
        'unveiled',
        'meets with great success',
        'wins best of show',
    ],
    'prod_upgrade': [
        'a new generation of',
        'updates to',
        'new line of',
        'OpenSource',
        'next generation of',
        'new platform for',
        'overhauled',
    ],
    'section_biznews': [
        'Financial News:',
        'Business update:',
        'The Markets Today',
    ],
    'section_corpnews': [
        '<#company#> update:',
        '<#company#> news:',
        'Corporate reader:',
        'Corporate update:',
        'Read all about:',
    ],
    'section_worldnews': [
        'World News:',
        'World Headlines',
        'The World Today',
    ],
    'shop_co_description_pl': [
        'online shops',
        'etailers',
        'ecommerce developers',
    ],
    'shop_co_description_sing': [
        'an online shop',
        'an etailer',
        'ecommerce developer',
    ],
    'shop_co_motto': [
        'Stuff you could have bought elsewhere, but with the thrill of getting your <#creditcard#> number nicked.',
    ],
    'shop_co_n': [
        'Buy',
        'Trade',
        'Shop',
        'Shopping',
        'Order',
        'Consumer',
        'Buyers',
        'Traders',
        'Factory',
        '<#names_last_patrician#>&amp;<#names_last_patrician#>',
        'Auction',
    ],
    'shop_co_px': [
        'e',
        'i',
        'Direct',
        'Internet',
        'Online',
        'Inter',
        'Quality',
        'Home',
        'Mega',
        'Hyper',
        'Discount',
        'Value',
        'Valu',
    ],
    'shop_co_sx': [
        'Store',
        'Shop',
        'Mall',
        'Place',
        'Network',
        'Now',
        'Central',
        'Catalog',
        '2000',
        'Brand',
        'Products',
        'Goodies',
        'Points',
        'Market',
        'Fair',
        'Barn',
        'Hut',
        'Stuff',
        'Shack',
        'Outlet',
        '.com',
        '.com',
        '.com',
    ],
    'shop_company': [
        '<#shop_co_px#><#shop_co_n#><#shop_co_sx#>',
    ],
    'shop_companyparts': [
        '<#shop_co_px#>+<#shop_co_n#>+<#shop_co_sx#>',
    ],
    'startup_co_description_pl': [
        '<#jargon#> companies',
    ],
    'startup_co_description_sing': [
        'a <#jargon#> company',
    ],
    'startup_co_motto': [
        'We make massive losses, but we promise to make more!',
    ],
    'startup_co_n': [
        'Brand',
        'Group',
        'Corp',
        'Vision',
        'Net',
        'Networking',
    ],
    'startup_co_px': [
        '<#p_business_px#>',
    ],
    'startup_co_sx': [
        '<#p_business_sx#>',
    ],
    'startup_company': [
        '<#startup_co_px#><#startup_co_n#><#startup_co_sx#>',
    ],
    'startup_companyparts': [
        '<#startup_co_px#>+<#startup_co_n#>+<#startup_co_sx#>',
    ],
    'verb_cooperates': [
        'acquires',
        'to acquire',
        'talks with',
        'to talk with',
        'merges with',
        'to merge with',
        'bids on',
        'to bid on',
        'forms alliance with',
        'announces partnership with',
    ],
    'verb_introduces': [
        'announces',
        'introduces',
        'unveils',
        'presents',
        'premieres',
        'debuts',
        'shows',
        'demonstrates',
    ],    }

