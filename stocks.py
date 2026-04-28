# --- STOCK LIST (BACKEND) ---
stocks_dict = {
    "Reliance Industries": "RELIANCE.NS",
    "TCS": "TCS.NS",
    "Infosys": "INFY.NS",
    "HDFC Bank": "HDFCBANK.NS",
    "ICICI Bank": "ICICIBANK.NS",
    "State Bank of India": "SBIN.NS",
    "Axis Bank": "AXISBANK.NS",
    "Kotak Mahindra Bank": "KOTAKBANK.NS",
    "IndusInd Bank": "INDUSINDBK.NS",
    "Bank of Baroda": "BANKBARODA.NS",
    "Punjab National Bank": "PNB.NS",
    "Canara Bank": "CANBK.NS",
    "Union Bank": "UNIONBANK.NS",
    "IDFC First Bank": "IDFCFIRSTB.NS",
    "Federal Bank": "FEDERALBNK.NS",
    "AU Small Finance Bank": "AUBANK.NS",
    "Bajaj Finance": "BAJFINANCE.NS",
    "Bajaj Finserv": "BAJAJFINSV.NS",
    "HDFC Life": "HDFCLIFE.NS",
    "SBI Life": "SBILIFE.NS",
    "ICICI Prudential": "ICICIPRULI.NS",
    "LIC Housing Finance": "LICHSGFIN.NS",
    "Power Finance Corp": "PFC.NS",
    "REC Ltd": "RECLTD.NS",
    "Muthoot Finance": "MUTHOOTFIN.NS",
    "Shriram Finance": "SHRIRAMFIN.NS",
    "L&T Finance": "LTF.NS",

    "Asian Paints": "ASIANPAINT.NS",
    "Berger Paints": "BERGEPAINT.NS",
    "Pidilite Industries": "PIDILITIND.NS",
    "Havells India": "HAVELLS.NS",
    "Polycab India": "POLYCAB.NS",
    "Dixon Technologies": "DIXON.NS",
    "Voltas": "VOLTAS.NS",
    "Whirlpool India": "WHIRLPOOL.NS",
    "Crompton Greaves": "CROMPTON.NS",

    "ITC": "ITC.NS",
    "Hindustan Unilever": "HINDUNILVR.NS",
    "Nestle India": "NESTLEIND.NS",
    "Britannia": "BRITANNIA.NS",
    "Dabur India": "DABUR.NS",
    "Godrej Consumer": "GODREJCP.NS",
    "Marico": "MARICO.NS",
    "Tata Consumer": "TATACONSUM.NS",
    "Colgate Palmolive": "COLPAL.NS",
    "Emami": "EMAMILTD.NS",

    "Sun Pharma": "SUNPHARMA.NS",
    "Dr Reddy's": "DRREDDY.NS",
    "Cipla": "CIPLA.NS",
    "Divis Labs": "DIVISLAB.NS",
    "Lupin": "LUPIN.NS",
    "Aurobindo Pharma": "AUROPHARMA.NS",
    "Biocon": "BIOCON.NS",
    "Torrent Pharma": "TORNTPHARM.NS",
    "Alkem Labs": "ALKEM.NS",
    "Abbott India": "ABBOTINDIA.NS",

    "Tata Motors": "TATAMOTORS.NS",
    "Maruti Suzuki": "MARUTI.NS",
    "Mahindra & Mahindra": "M&M.NS",
    "Bajaj Auto": "BAJAJ-AUTO.NS",
    "Eicher Motors": "EICHERMOT.NS",
    "Hero MotoCorp": "HEROMOTOCO.NS",
    "Ashok Leyland": "ASHOKLEY.NS",
    "TVS Motors": "TVSMOTOR.NS",
    "Bosch": "BOSCHLTD.NS",
    "MRF": "MRF.NS",

    "Larsen & Toubro": "LT.NS",
    "Siemens": "SIEMENS.NS",
    "ABB India": "ABB.NS",
    "BHEL": "BHEL.NS",
    "Cummins India": "CUMMINSIND.NS",
    "Thermax": "THERMAX.NS",
    "AIA Engineering": "AIAENG.NS",

    "ONGC": "ONGC.NS",
    "Coal India": "COALINDIA.NS",
    "NTPC": "NTPC.NS",
    "Power Grid": "POWERGRID.NS",
    "Adani Green": "ADANIGREEN.NS",
    "Adani Power": "ADANIPOWER.NS",
    "JSW Energy": "JSWENERGY.NS",
    "Tata Power": "TATAPOWER.NS",
    "GAIL": "GAIL.NS",
    "IOC": "IOC.NS",

    "Adani Ports": "ADANIPORTS.NS",
    "Zomato": "ZOMATO.NS",
    "Paytm": "PAYTM.NS",
    "IRCTC": "IRCTC.NS",
    "IRFC": "IRFC.NS",
    "RVNL": "RVNL.NS",
    "IRCON": "IRCON.NS",
    "NBCC": "NBCC.NS",
    "HUDCO": "HUDCO.NS",

    "Titan": "TITAN.NS",
    "Trent": "TRENT.NS",
    "Avenue Supermarts": "DMART.NS",
    "Page Industries": "PAGEIND.NS",
    "Relaxo Footwear": "RELAXO.NS",

    "Apollo Hospitals": "APOLLOHOSP.NS",
    "Max Healthcare": "MAXHEALTH.NS",
    "Fortis Healthcare": "FORTIS.NS",
    "Laurus Labs": "LAURUSLABS.NS",

    "Deepak Nitrite": "DEEPAKNTR.NS",
    "SRF": "SRF.NS",
    "PI Industries": "PIIND.NS",
    "UPL": "UPL.NS",
    "Tata Chemicals": "TATACHEM.NS",

    "Jubilant Foodworks": "JUBLFOOD.NS",
    "Westlife Foodworld": "WESTLIFE.NS",
    "Devyani International": "DEVYANI.NS",

    "BSE": "BSE.NS",
    "CDSL": "CDSL.NS",
    "MCX": "MCX.NS",

    "HAL": "HAL.NS",
    "BEL": "BEL.NS",
    "Bharat Dynamics": "BDL.NS",
    "Cochin Shipyard": "COCHINSHIP.NS",
    "Mazagon Dock": "MAZDOCK.NS",
    "Wipro": "WIPRO.NS",
    "Tech Mahindra": "TECHM.NS",
    "HCL Technologies": "HCLTECH.NS",
    "LTIMindtree": "LTIM.NS",
    "Mphasis": "MPHASIS.NS",
    "Persistent Systems": "PERSISTENT.NS",
    "Coforge": "COFORGE.NS",
    "Oracle Financial": "OFSS.NS",
    "KPIT Technologies": "KPITTECH.NS",
    "Sonata Software": "SONATSOFTW.NS",

    "ACC": "ACC.NS",
    "Ambuja Cements": "AMBUJACEM.NS",
    "UltraTech Cement": "ULTRACEMCO.NS",
    "Shree Cement": "SHREECEM.NS",
    "Ramco Cements": "RAMCOCEM.NS",
    "JK Cement": "JKCEMENT.NS",
    "Dalmia Bharat": "DALBHARAT.NS",

    "JSW Steel": "JSWSTEEL.NS",
    "Tata Steel": "TATASTEEL.NS",
    "SAIL": "SAIL.NS",
    "Jindal Steel": "JINDALSTEL.NS",
    "APL Apollo": "APLAPOLLO.NS",
    "NMDC": "NMDC.NS",
    "Vedanta": "VEDL.NS",
    "Hindalco": "HINDALCO.NS",
    "NALCO": "NATIONALUM.NS",
    "Hindustan Zinc": "HINDZINC.NS",

    "DLF": "DLF.NS",
    "Godrej Properties": "GODREJPROP.NS",
    "Oberoi Realty": "OBEROIRLTY.NS",
    "Prestige Estates": "PRESTIGE.NS",
    "Phoenix Mills": "PHOENIXLTD.NS",
    "Brigade Enterprises": "BRIGADE.NS",

    "Container Corp": "CONCOR.NS",
    "Blue Dart": "BLUEDART.NS",
    "Delhivery": "DELHIVERY.NS",
    "TCI Express": "TCIEXP.NS",
    "Allcargo Logistics": "ALLCARGO.NS",

    "PVR INOX": "PVRINOX.NS",
    "Inox Wind": "INOXWIND.NS",
    "Saregama": "SAREGAMA.NS",
    "Tips Industries": "TIPSINDLTD.NS",

    "Indian Hotels": "INDHOTEL.NS",
    "EIH": "EIHOTEL.NS",
    "Lemon Tree Hotels": "LEMONTREE.NS",
    "Easy Trip Planners": "EASEMYTRIP.NS",

    "Tata Communications": "TATACOMM.NS",
    "Bharti Airtel": "BHARTIARTL.NS",
    "Indus Towers": "INDUSTOWER.NS",
    "Vodafone Idea": "IDEA.NS",

    "Grasim": "GRASIM.NS",
    "Aditya Birla Fashion": "ABFRL.NS",
    "Raymond": "RAYMOND.NS",
    "Arvind Ltd": "ARVIND.NS",

    "Navin Fluorine": "NAVINFLUOR.NS",
    "Balaji Amines": "BALAMINES.NS",
    "Vinati Organics": "VINATIORGA.NS",
    "Atul Ltd": "ATUL.NS",
    "Clean Science": "CLEAN.NS",

    "Escorts Kubota": "ESCORTS.NS",
    "Schaeffler India": "SCHAEFFLER.NS",
    "SKF India": "SKFINDIA.NS",
    "Timken India": "TIMKEN.NS",

    "RBL Bank": "RBLBANK.NS",
    "Yes Bank": "YESBANK.NS",
    "South Indian Bank": "SOUTHBANK.NS",
    "Karur Vysya Bank": "KARURVYSYA.NS",
    "City Union Bank": "CUB.NS",

    "Gujarat Gas": "GUJGASLTD.NS",
    "Indraprastha Gas": "IGL.NS",
    "Mahanagar Gas": "MGL.NS",
    "Petronet LNG": "PETRONET.NS",

    "Bikaji Foods": "BIKAJI.NS",
    "Varun Beverages": "VBL.NS",
    "Radico Khaitan": "RADICO.NS",
    "United Spirits": "UNITDSPR.NS",

    "Aegis Logistics": "AEGISLOG.NS",
    "Chambal Fertilisers": "CHAMBLFERT.NS",
    "Coromandel International": "COROMANDEL.NS",
    "Deepak Fertilisers": "DEEPAKFERT.NS",

    "KNR Constructions": "KNRCON.NS",
    "NCC": "NCC.NS",
    "KEC International": "KEC.NS",
    "Kalpataru Projects": "KPIL.NS",

    "Trident": "TRIDENT.NS",
    "Welspun India": "WELSPUNIND.NS",
    "Vardhman Textiles": "VTL.NS",
    "KPR Mill": "KPRMILL.NS",

    "Suzlon Energy": "SUZLON.NS",
    "Inox Green": "INOXGREEN.NS",
    "Waaree Renewables": "WAAREERTL.NS",
    "Borosil Renewables": "BORORENEW.NS",

    "Aarti Industries": "AARTIIND.NS",
    "Aavas Financiers": "AAVAS.NS",
    "Adani Total Gas": "ATGL.NS",
    "Affle India": "AFFLE.NS",
    "Ajanta Pharma": "AJANTPHARM.NS",
    "Alembic Pharma": "APLLTD.NS",
    "Amara Raja Energy": "ARE&M.NS",
    "Anupam Rasayan": "ANURAS.NS",
    "Apollo Tyres": "APOLLOTYRE.NS",
    "Aptus Value Housing": "APTUS.NS",

    "Balkrishna Industries": "BALKRISIND.NS",
    "Balrampur Chini": "BALRAMCHIN.NS",
    "Bandhan Bank": "BANDHANBNK.NS",
    "Bank of India": "BANKINDIA.NS",
    "Bata India": "BATAINDIA.NS",
    "BEML": "BEML.NS",
    "Birlasoft": "BSOFT.NS",
    "Birla Corporation": "BIRLACORPN.NS",
    "Bombay Burmah": "BBTC.NS",
    "Borosil": "BOROLTD.NS",

    "CESC": "CESC.NS",
    "Central Bank of India": "CENTRALBK.NS",
    "Century Plyboards": "CENTURYPLY.NS",
    "CG Power": "CGPOWER.NS",
    "Cholamandalam Finance": "CHOLAFIN.NS",
    "Craftsman Automation": "CRAFTSMAN.NS",
    "CreditAccess Grameen": "CREDITACC.NS",
    "Cyient": "CYIENT.NS",

    "Datamatics": "DATAMATICS.NS",
    "DCM Shriram": "DCMSHRIRAM.NS",
    "Delta Corp": "DELTACORP.NS",
    "Dr Lal PathLabs": "LALPATHLAB.NS",
    "eClerx Services": "ECLERX.NS",
    "Elgi Equipments": "ELGIEQUIP.NS",
    "Endurance Technologies": "ENDURANCE.NS",
    "Equitas Small Finance": "EQUITASBNK.NS",

    "Finolex Cables": "FINCABLES.NS",
    "Fine Organic": "FINEORG.NS",
    "Firstsource Solutions": "FSL.NS",
    "Glenmark Pharma": "GLENMARK.NS",
    "GMR Airports": "GMRINFRA.NS",
    "Graphite India": "GRAPHITE.NS",
    "Gujarat Fluorochem": "FLUOROCHEM.NS",
    "Gujarat State Petronet": "GSPL.NS",

    "HFCL": "HFCL.NS",
    "Happiest Minds": "HAPPSTMNDS.NS",
    "Hatsun Agro": "HATSUN.NS",
    "Honeywell Automation": "HONAUT.NS",
    "ICRA": "ICRA.NS",
    "IDBI Bank": "IDBI.NS",
    "IEX": "IEX.NS",
    "India Cements": "INDIACEM.NS",

    "Indian Bank": "INDIANB.NS",
    "Indian Energy Exchange": "IEX.NS",
    "Indian Overseas Bank": "IOB.NS",
    "Indiamart": "INDIAMART.NS",
    "Ingersoll Rand": "INGERRAND.NS",
    "Intellect Design": "INTELLECT.NS",
    "Jindal Saw": "JINDALSAW.NS",
    "JK Lakshmi Cement": "JKLAKSHMI.NS",

    "JK Paper": "JKPAPER.NS",
    "JM Financial": "JMFINANCIL.NS",
    "JTEKT India": "JTEKTINDIA.NS",
    "Jubilant Ingrevia": "JUBLINGREA.NS",
    "Just Dial": "JUSTDIAL.NS",
    "Kalyan Jewellers": "KALYANKJIL.NS",
    "Kajaria Ceramics": "KAJARIACER.NS",
    "KEI Industries": "KEI.NS",

    "Linde India": "LINDEINDIA.NS",
    "L&T Technology Services": "LTTS.NS",
    "Mastek": "MASTEK.NS",
    "Metropolis Healthcare": "METROPOLIS.NS",
    "Minda Corporation": "MINDACORP.NS",
    "MOIL": "MOIL.NS",
    "Motilal Oswal": "MOTILALOFS.NS",
    "Mphasis": "MPHASIS.NS",

    "Narayana Hrudayalaya": "NH.NS",
    "Natco Pharma": "NATCOPHARM.NS",
    "NESCO": "NESCO.NS",
    "NOCIL": "NOCIL.NS",
    "Olectra Greentech": "OLECTRA.NS",
    "Orient Electric": "ORIENTELEC.NS",
    "Page Industries": "PAGEIND.NS",
    "Patanjali Foods": "PATANJALI.NS",

    "Piramal Enterprises": "PEL.NS",
    "Poly Medicure": "POLYMED.NS",
    "Praj Industries": "PRAJIND.NS",
    "Prince Pipes": "PRINCEPIPE.NS",
    "Quess Corp": "QUESS.NS",
    "Rain Industries": "RAIN.NS",
    "Rallis India": "RALLIS.NS",
    "Redington": "REDINGTON.NS",

    "Route Mobile": "ROUTE.NS",
    "STATE BANK OF INDIA": "SBIN.NS",
    "SJVN": "SJVN.NS",
    "Solar Industries": "SOLARINDS.NS",
    "Sterlite Technologies": "STLTECH.NS",
    "Supreme Industries": "SUPREMEIND.NS",
    "Tanla Platforms": "TANLA.NS",
    "TTK Prestige": "TTKPRESTIG.NS",

    "Ujjivan Small Finance": "UJJIVANSFB.NS",
    "V-Guard": "VGUARD.NS",
    "VIP Industries": "VIPIND.NS",
    "Zensar Technologies": "ZENSARTECH.NS"
}



    
    
    
    










def clean_stocks(data):
    seen = set()
    cleaned = {}

    for name, symbol in data.items():
        if symbol not in seen:
            cleaned[name] = symbol
            seen.add(symbol)
        else:
            print(f"⚠️ Removed duplicate: {name} -> {symbol}")

    return cleaned

# ✅ Apply cleaning
stocks_dict = clean_stocks(stocks_dict)
