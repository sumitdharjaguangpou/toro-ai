# --- STOCK LIST (BACKEND) ---
import difflib

stocks_dict = {
"RELIANCE": "RELIANCE.NS",
"RELIANCE INDUSTRIES": "RELIANCE.NS",
"RIL": "RELIANCE.NS",

"TCS": "TCS.NS",
"TATA CONSULTANCY SERVICES": "TCS.NS",

"INFOSYS": "INFY.NS",
"INFY": "INFY.NS",

"HDFC BANK": "HDFCBANK.NS",
"HDFC": "HDFCBANK.NS",

"ICICI BANK": "ICICIBANK.NS",
"ICICI": "ICICIBANK.NS",

"AXIS BANK": "AXISBANK.NS",
"AXIS": "AXISBANK.NS",

"KOTAK MAHINDRA BANK": "KOTAKBANK.NS",
"KOTAK BANK": "KOTAKBANK.NS",
"KOTAK": "KOTAKBANK.NS",

"INDUSIND BANK": "INDUSINDBK.NS",
"INDUSIND": "INDUSINDBK.NS",

"BANK OF BARODA": "BANKBARODA.NS",
"BOB": "BANKBARODA.NS",

"PUNJAB NATIONAL BANK": "PNB.NS",
"PNB": "PNB.NS",

"CANARA BANK": "CANBK.NS",
"CANARA": "CANBK.NS",

"UNION BANK": "UNIONBANK.NS",
"UNION BANK OF INDIA": "UNIONBANK.NS",

"IDFC FIRST BANK": "IDFCFIRSTB.NS",
"IDFC": "IDFCFIRSTB.NS",

"FEDERAL BANK": "FEDERALBNK.NS",
"FEDERAL": "FEDERALBNK.NS",

"AU SMALL FINANCE BANK": "AUBANK.NS",
"AU BANK": "AUBANK.NS",
"AU FINANCE": "AUBANK.NS",

"BAJAJ FINANCE": "BAJFINANCE.NS",

"BAJAJ FINSERV": "BAJAJFINSV.NS",

"HDFC LIFE": "HDFCLIFE.NS",

"SBI LIFE": "SBILIFE.NS",

"ICICI PRUDENTIAL": "ICICIPRULI.NS",
"ICICI PRU": "ICICIPRULI.NS",

"LIC HOUSING FINANCE": "LICHSGFIN.NS",
"LIC HOUSING": "LICHSGFIN.NS",

"POWER FINANCE CORP": "PFC.NS",
"PFC": "PFC.NS",

"REC LTD": "RECLTD.NS",
"REC": "RECLTD.NS",

"MUTHOOT FINANCE": "MUTHOOTFIN.NS",
"MUTHOOT": "MUTHOOTFIN.NS",

"SHRIRAM FINANCE": "SHRIRAMFIN.NS",
"SHRIRAM": "SHRIRAMFIN.NS",

"L&T FINANCE": "LTF.NS",
"LT FINANCE": "LTF.NS",

"ASIAN PAINTS": "ASIANPAINT.NS",
"ASIANPAINT": "ASIANPAINT.NS",

"BERGER PAINTS": "BERGEPAINT.NS",
"BERGER": "BERGEPAINT.NS",

"PIDILITE INDUSTRIES": "PIDILITIND.NS",
"PIDILITE": "PIDILITIND.NS",

"HAVELLS INDIA": "HAVELLS.NS",
"HAVELLS": "HAVELLS.NS",

"POLYCAB INDIA": "POLYCAB.NS",
"POLYCAB": "POLYCAB.NS",

"DIXON TECHNOLOGIES": "DIXON.NS",
"DIXON": "DIXON.NS",

"VOLTAS": "VOLTAS.NS",

"WHIRLPOOL INDIA": "WHIRLPOOL.NS",
"WHIRLPOOL": "WHIRLPOOL.NS",

"CROMPTON GREAVES": "CROMPTON.NS",
"CROMPTON": "CROMPTON.NS",

"ITC": "ITC.NS",
"Hindustan Unilever": "HINDUNILVR.NS",
"HUL": "HINDUNILVR.NS",
"Nestle India": "NESTLEIND.NS",
"Nestle": "NESTLEIND.NS",
"Britannia": "BRITANNIA.NS",
"Dabur India": "DABUR.NS",
"Dabur": "DABUR.NS",
"Godrej Consumer": "GODREJCP.NS",
"Godrej": "GODREJCP.NS",
"Marico": "MARICO.NS",
"Tata Consumer": "TATACONSUM.NS",
"Tata Consumer Products": "TATACONSUM.NS",
"Colgate Palmolive": "COLPAL.NS",
"Colgate": "COLPAL.NS",
"Emami": "EMAMILTD.NS",

#pharma and healthcare
"Sun Pharma": "SUNPHARMA.NS",
"Sun Pharmaceutical": "SUNPHARMA.NS",
"Sunpharma": "SUNPHARMA.NS",

"Dr Reddy's": "DRREDDY.NS",
"Dr Reddys": "DRREDDY.NS",
"Dr Reddy Laboratories": "DRREDDY.NS",

"Cipla": "CIPLA.NS",
"Cipla Ltd": "CIPLA.NS",

"Divis Labs": "DIVISLAB.NS",
"Divis Laboratories": "DIVISLAB.NS",

"Lupin": "LUPIN.NS",
"Lupin Pharma": "LUPIN.NS",

"Aurobindo Pharma": "AUROPHARMA.NS",
"Aurobindo": "AUROPHARMA.NS",

"Biocon": "BIOCON.NS",
"Biocon Ltd": "BIOCON.NS",

"Torrent Pharma": "TORNTPHARM.NS",
"Torrent Pharmaceuticals": "TORNTPHARM.NS",

"Alkem Labs": "ALKEM.NS",
"Alkem Laboratories": "ALKEM.NS",

"Abbott India": "ABBOTINDIA.NS",
"Abbott": "ABBOTINDIA.NS",

#automobile
"Tata Motors": "TATAMOTORS.NS",
"Tata": "TATAMOTORS.NS",

"Maruti Suzuki": "MARUTI.NS",
"Maruti": "MARUTI.NS",
"MSIL": "MARUTI.NS",

"Mahindra & Mahindra": "M&M.NS",
"Mahindra": "M&M.NS",
"M&M": "M&M.NS",

"Bajaj Auto": "BAJAJ-AUTO.NS",
"Bajaj": "BAJAJ-AUTO.NS",

"Eicher Motors": "EICHERMOT.NS",
"Eicher": "EICHERMOT.NS",

"Hero MotoCorp": "HEROMOTOCO.NS",
"Hero": "HEROMOTOCO.NS",
"Hero Honda": "HEROMOTOCO.NS",

"Ashok Leyland": "ASHOKLEY.NS",
"Ashok": "ASHOKLEY.NS",

"TVS Motors": "TVSMOTOR.NS",
"TVS": "TVSMOTOR.NS",

"Bosch": "BOSCHLTD.NS",
"Bosch India": "BOSCHLTD.NS",

"MRF": "MRF.NS",
"MRF Tyres": "MRF.NS",

#engeneering & industrial
"Larsen & Toubro": "LT.NS",
"L&T": "LT.NS",
"Larsen": "LT.NS",

"Siemens": "SIEMENS.NS",
"Siemens India": "SIEMENS.NS",

"ABB India": "ABB.NS",
"ABB": "ABB.NS",

"BHEL": "BHEL.NS",
"Bharat Heavy Electricals": "BHEL.NS",

"Cummins India": "CUMMINSIND.NS",
"Cummins": "CUMMINSIND.NS",

"Thermax": "THERMAX.NS",
"Thermax Ltd": "THERMAX.NS",

"AIA Engineering": "AIAENG.NS",
"AIA": "AIAENG.NS",


"ONGC": "ONGC.NS",
"Oil and Natural Gas": "ONGC.NS",

"Coal India": "COALINDIA.NS",
"Coal": "COALINDIA.NS",

"NTPC": "NTPC.NS",
"National Thermal Power": "NTPC.NS",

"Power Grid": "POWERGRID.NS",
"PGCIL": "POWERGRID.NS",
"Powergrid": "POWERGRID.NS",

"Adani Green": "ADANIGREEN.NS",
"Adani Green Energy": "ADANIGREEN.NS",

"Adani Power": "ADANIPOWER.NS",
"Adani": "ADANIPOWER.NS",

"JSW Energy": "JSWENERGY.NS",
"JSW": "JSWENERGY.NS",

"Tata Power": "TATAPOWER.NS",
"Tata": "TATAPOWER.NS",

"GAIL": "GAIL.NS",
"Gas Authority": "GAIL.NS",

"IOC": "IOC.NS",
"Indian Oil": "IOC.NS",

#Ports, Logistics & Public Sector
"Adani Ports": "ADANIPORTS.NS",
"Adani Port": "ADANIPORTS.NS",
"APSEZ": "ADANIPORTS.NS",

"Zomato": "ZOMATO.NS",
"Zomato Ltd": "ZOMATO.NS",

"Paytm": "PAYTM.NS",
"One97": "PAYTM.NS",

"IRCTC": "IRCTC.NS",
"Indian Railways Catering": "IRCTC.NS",

"IRFC": "IRFC.NS",
"Indian Railway Finance": "IRFC.NS",

"RVNL": "RVNL.NS",
"Rail Vikas": "RVNL.NS",

"IRCON": "IRCON.NS",
"IRCON International": "IRCON.NS",

"NBCC": "NBCC.NS",
"NBCC India": "NBCC.NS",

"HUDCO": "HUDCO.NS",
"Housing & Urban Dev": "HUDCO.NS",


"Titan": "TITAN.NS",
"Titan Company": "TITAN.NS",

"Trent": "TRENT.NS",
"Trent Ltd": "TRENT.NS",

"Avenue Supermarts": "DMART.NS",
"D-Mart": "DMART.NS",
"DMart": "DMART.NS",

"Page Industries": "PAGEIND.NS",
"Page": "PAGEIND.NS",
"Jockey": "PAGEIND.NS",

"Relaxo Footwear": "RELAXO.NS",
"Relaxo": "RELAXO.NS",


"Apollo Hospitals": "APOLLOHOSP.NS",
"Apollo": "APOLLOHOSP.NS",

"Max Healthcare": "MAXHEALTH.NS",
"Max": "MAXHEALTH.NS",

"Fortis Healthcare": "FORTIS.NS",
"Fortis": "FORTIS.NS",

"Laurus Labs": "LAURUSLABS.NS",
"Laurus": "LAURUSLABS.NS",


"Deepak Nitrite": "DEEPAKNTR.NS",
"Deepak": "DEEPAKNTR.NS",

"SRF": "SRF.NS",
"SRF Ltd": "SRF.NS",

"PI Industries": "PIIND.NS",
"PI": "PIIND.NS",

"UPL": "UPL.NS",
"United Phosphorus": "UPL.NS",

"Tata Chemicals": "TATACHEM.NS",
"Tata Chem": "TATACHEM.NS",

"Jubilant Foodworks": "JUBLFOOD.NS",
"Jubilant": "JUBLFOOD.NS",
"Dominos": "JUBLFOOD.NS",

"Westlife Foodworld": "WESTLIFE.NS",
"Westlife": "WESTLIFE.NS",
"McDonalds India": "WESTLIFE.NS",

"Devyani International": "DEVYANI.NS",
"Devyani": "DEVYANI.NS",
"KFC India": "DEVYANI.NS",
"Pizza Hut India": "DEVYANI.NS",

# Exchanges & Financial Infrastructure
"BSE": "BSE.NS",
"Bombay Stock Exchange": "BSE.NS",

"CDSL": "CDSL.NS",
"Central Depository": "CDSL.NS",

"MCX": "MCX.NS",
"Multi Commodity Exchange": "MCX.NS",


"HAL": "HAL.NS",
"Hindustan Aeronautics": "HAL.NS",

"BEL": "BEL.NS",
"Bharat Electronics": "BEL.NS",

"Bharat Dynamics": "BDL.NS",
"BDL": "BDL.NS",

"Cochin Shipyard": "COCHINSHIP.NS",
"Cochin": "COCHINSHIP.NS",

"Mazagon Dock": "MAZDOCK.NS",
"Mazagon": "MAZDOCK.NS",
"Mazdock": "MAZDOCK.NS",

"Wipro": "WIPRO.NS",
"Wipro Ltd": "WIPRO.NS",

"Tech Mahindra": "TECHM.NS",
"TechM": "TECHM.NS",

"HCL Technologies": "HCLTECH.NS",
"HCL Tech": "HCLTECH.NS",

"SBI": "SBIN.NS",
"State Bank of India": "SBIN.NS",

"LTIMindtree": "LTIM.NS",
"LTI": "LTIM.NS",
"Mindtree": "LTIM.NS",

"Mphasis": "MPHASIS.NS",
"Mphasis Ltd": "MPHASIS.NS",

"Persistent Systems": "PERSISTENT.NS",
"Persistent": "PERSISTENT.NS",

"Coforge": "COFORGE.NS",
"Coforge Ltd": "COFORGE.NS",

"Oracle Financial": "OFSS.NS",
"OFSS": "OFSS.NS",

"KPIT Technologies": "KPITTECH.NS",
"KPIT": "KPITTECH.NS",

"Sonata Software": "SONATSOFTW.NS",
"Sonata": "SONATSOFTW.NS",


"ACC": "ACC.NS",
"ACC Cement": "ACC.NS",

"Ambuja Cements": "AMBUJACEM.NS",
"Ambuja": "AMBUJACEM.NS",

"UltraTech Cement": "ULTRACEMCO.NS",
"Ultratech": "ULTRACEMCO.NS",

"Shree Cement": "SHREECEM.NS",
"Shree": "SHREECEM.NS",

"Ramco Cements": "RAMCOCEM.NS",
"Ramco": "RAMCOCEM.NS",

"JK Cement": "JKCEMENT.NS",
"JK": "JKCEMENT.NS",

"Dalmia Bharat": "DALBHARAT.NS",
"Dalmia": "DALBHARAT.NS",


"JSW Steel": "JSWSTEEL.NS",
"JSW": "JSWSTEEL.NS",

"Tata Steel": "TATASTEEL.NS",
"Tata": "TATASTEEL.NS",

"SAIL": "SAIL.NS",
"Steel Authority": "SAIL.NS",

"Jindal Steel": "JINDALSTEL.NS",
"Jindal": "JINDALSTEL.NS",

"APL Apollo": "APLAPOLLO.NS",
"Apollo Steel": "APLAPOLLO.NS",

"NMDC": "NMDC.NS",
"National Mineral": "NMDC.NS",

"Vedanta": "VEDL.NS",
"Vedanta Ltd": "VEDL.NS",

"Hindalco": "HINDALCO.NS",
"Hindalco Industries": "HINDALCO.NS",

"NALCO": "NATIONALUM.NS",
"National Aluminium": "NATIONALUM.NS",

"Hindustan Zinc": "HINDZINC.NS",
"HZL": "HINDZINC.NS",

# Real Estate
"DLF": "DLF.NS",
"DLF Ltd": "DLF.NS",

"Godrej Properties": "GODREJPROP.NS",
"Godrej Prop": "GODREJPROP.NS",

"Oberoi Realty": "OBEROIRLTY.NS",
"Oberoi": "OBEROIRLTY.NS",

"Prestige Estates": "PRESTIGE.NS",
"Prestige": "PRESTIGE.NS",

"Phoenix Mills": "PHOENIXLTD.NS",
"Phoenix": "PHOENIXLTD.NS",

"Brigade Enterprises": "BRIGADE.NS",
"Brigade": "BRIGADE.NS",

# Logistics
"Container Corp": "CONCOR.NS",
"CONCOR": "CONCOR.NS",

"Blue Dart": "BLUEDART.NS",
"BlueDart": "BLUEDART.NS",

"Delhivery": "DELHIVERY.NS",
"Delhivery Ltd": "DELHIVERY.NS",

"TCI Express": "TCIEXP.NS",
"TCI": "TCIEXP.NS",

"Allcargo Logistics": "ALLCARGO.NS",
"Allcargo": "ALLCARGO.NS",

# Entertainment
"PVR INOX": "PVRINOX.NS",
"PVR": "PVRINOX.NS",
"Inox": "PVRINOX.NS",

"Inox Wind": "INOXWIND.NS",
"InoxWind": "INOXWIND.NS",

"Saregama": "SAREGAMA.NS",
"Saregama India": "SAREGAMA.NS",

"Tips Industries": "TIPSINDLTD.NS",
"Tips": "TIPSINDLTD.NS",

# Hospitality
"Indian Hotels": "INDHOTEL.NS",
"Taj Hotels": "INDHOTEL.NS",

"EIH": "EIHOTEL.NS",
"Oberoi Hotels": "EIHOTEL.NS",

"Lemon Tree Hotels": "LEMONTREE.NS",
"Lemon Tree": "LEMONTREE.NS",

"Easy Trip Planners": "EASEMYTRIP.NS",
"EaseMyTrip": "EASEMYTRIP.NS",

# Telecom
"Tata Communications": "TATACOMM.NS",
"Tata Comm": "TATACOMM.NS",

"Bharti Airtel": "BHARTIARTL.NS",
"Airtel": "BHARTIARTL.NS",

"Indus Towers": "INDUSTOWER.NS",
"Indus": "INDUSTOWER.NS",

"Vodafone Idea": "IDEA.NS",
"Vodafone": "IDEA.NS",
"Idea": "IDEA.NS",

# Textiles & Lifestyle
"Grasim": "GRASIM.NS",
"Grasim Industries": "GRASIM.NS",

"Aditya Birla Fashion": "ABFRL.NS",
"ABFRL": "ABFRL.NS",

"Raymond": "RAYMOND.NS",
"Raymond Ltd": "RAYMOND.NS",

"Arvind Ltd": "ARVIND.NS",
"Arvind": "ARVIND.NS",

# Chemicals
"Navin Fluorine": "NAVINFLUOR.NS",
"Navin": "NAVINFLUOR.NS",

"Balaji Amines": "BALAMINES.NS",
"Balaji": "BALAMINES.NS",

"Vinati Organics": "VINATIORGA.NS",
"Vinati": "VINATIORGA.NS",

"Atul Ltd": "ATUL.NS",
"Atul": "ATUL.NS",

"Clean Science": "CLEAN.NS",
"Clean": "CLEAN.NS",

# Engineering
"Escorts Kubota": "ESCORTS.NS",
"Escorts": "ESCORTS.NS",

"Schaeffler India": "SCHAEFFLER.NS",
"Schaeffler": "SCHAEFFLER.NS",

"SKF India": "SKFINDIA.NS",
"SKF": "SKFINDIA.NS",

"Timken India": "TIMKEN.NS",
"Timken": "TIMKEN.NS",

# Banks
"RBL Bank": "RBLBANK.NS",
"RBL": "RBLBANK.NS",

"Yes Bank": "YESBANK.NS",
"Yes": "YESBANK.NS",

"South Indian Bank": "SOUTHBANK.NS",
"SIB": "SOUTHBANK.NS",

"Karur Vysya Bank": "KARURVYSYA.NS",
"KVB": "KARURVYSYA.NS",

"City Union Bank": "CUB.NS",
"CUB": "CUB.NS",

# Gas & Energy
"Gujarat Gas": "GUJGASLTD.NS",
"GUJ Gas": "GUJGASLTD.NS",

"Indraprastha Gas": "IGL.NS",
"IGL": "IGL.NS",

"Mahanagar Gas": "MGL.NS",
"MGL": "MGL.NS",

"Petronet LNG": "PETRONET.NS",
"Petronet": "PETRONET.NS",

# Food & Beverages
"Bikaji Foods": "BIKAJI.NS",
"Bikaji": "BIKAJI.NS",

"Varun Beverages": "VBL.NS",
"Varun": "VBL.NS",
"VBL": "VBL.NS",

"Radico Khaitan": "RADICO.NS",
"Radico": "RADICO.NS",

"United Spirits": "UNITDSPR.NS",
"USL": "UNITDSPR.NS",
"Diageo India": "UNITDSPR.NS",

# Logistics & Fertilisers
"Aegis Logistics": "AEGISLOG.NS",
"Aegis": "AEGISLOG.NS",

"Chambal Fertilisers": "CHAMBLFERT.NS",
"Chambal": "CHAMBLFERT.NS",

"Coromandel International": "COROMANDEL.NS",
"Coromandel": "COROMANDEL.NS",

"Deepak Fertilisers": "DEEPAKFERT.NS",
"Deepak Fert": "DEEPAKFERT.NS",

# Construction & Infra
"KNR Constructions": "KNRCON.NS",
"KNR": "KNRCON.NS",

"NCC": "NCC.NS",
"Nagarjuna Construction": "NCC.NS",

"KEC International": "KEC.NS",
"KEC": "KEC.NS",

"Kalpataru Projects": "KPIL.NS",
"Kalpataru": "KPIL.NS",

# Textiles
"Trident": "TRIDENT.NS",
"Trident Ltd": "TRIDENT.NS",

"Welspun India": "WELSPUNIND.NS",
"Welspun": "WELSPUNIND.NS",

"Vardhman Textiles": "VTL.NS",
"Vardhman": "VTL.NS",

"KPR Mill": "KPRMILL.NS",
"KPR": "KPRMILL.NS",

# Renewables
"Suzlon Energy": "SUZLON.NS",
"Suzlon": "SUZLON.NS",

"Inox Green": "INOXGREEN.NS",
"InoxGreen": "INOXGREEN.NS",

"Waaree Renewables": "WAAREERTL.NS",
"Waaree": "WAAREERTL.NS",

"Borosil Renewables": "BORORENEW.NS",
"Borosil Renew": "BORORENEW.NS",

# Chemicals & Pharma
"Aarti Industries": "AARTIIND.NS",
"Aarti": "AARTIIND.NS",

"Aavas Financiers": "AAVAS.NS",
"Aavas": "AAVAS.NS",

"Adani Total Gas": "ATGL.NS",
"ATGL": "ATGL.NS",

"Affle India": "AFFLE.NS",
"Affle": "AFFLE.NS",

"Ajanta Pharma": "AJANTPHARM.NS",
"Ajanta": "AJANTPHARM.NS",

"Alembic Pharma": "APLLTD.NS",
"Alembic": "APLLTD.NS",

"Amara Raja Energy": "ARE&M.NS",
"Amara Raja": "ARE&M.NS",

"Anupam Rasayan": "ANURAS.NS",
"Anupam": "ANURAS.NS",

"Apollo Tyres": "APOLLOTYRE.NS",
"Apollo Tyre": "APOLLOTYRE.NS",

"Aptus Value Housing": "APTUS.NS",
"Aptus": "APTUS.NS",

# Manufacturing & Banks
"Balkrishna Industries": "BALKRISIND.NS",
"BKT": "BALKRISIND.NS",

"Balrampur Chini": "BALRAMCHIN.NS",
"Balrampur": "BALRAMCHIN.NS",

"Bandhan Bank": "BANDHANBNK.NS",
"Bandhan": "BANDHANBNK.NS",

"Bank of India": "BANKINDIA.NS",
"BOI": "BANKINDIA.NS",

"Bata India": "BATAINDIA.NS",
"Bata": "BATAINDIA.NS",

"BEML": "BEML.NS",
"BEML Ltd": "BEML.NS",

"Birlasoft": "BSOFT.NS",
"Birla Soft": "BSOFT.NS",

"Birla Corporation": "BIRLACORPN.NS",
"Birla Corp": "BIRLACORPN.NS",

"Bombay Burmah": "BBTC.NS",
"BBTC": "BBTC.NS",

"Borosil": "BOROLTD.NS",
"Borosil Ltd": "BOROLTD.NS",

# Power & Finance
"CESC": "CESC.NS",
"CESC Ltd": "CESC.NS",

"Central Bank of India": "CENTRALBK.NS",
"Central Bank": "CENTRALBK.NS",

"Century Plyboards": "CENTURYPLY.NS",
"Century Ply": "CENTURYPLY.NS",

"CG Power": "CGPOWER.NS",
"CG": "CGPOWER.NS",

"Cholamandalam Finance": "CHOLAFIN.NS",
"Chola": "CHOLAFIN.NS",

"Craftsman Automation": "CRAFTSMAN.NS",
"Craftsman": "CRAFTSMAN.NS",

"CreditAccess Grameen": "CREDITACC.NS",
"CreditAccess": "CREDITACC.NS",

"Cyient": "CYIENT.NS",
"Cyient Ltd": "CYIENT.NS",

# IT & Services
"Datamatics": "DATAMATICS.NS",
"Datamatics Ltd": "DATAMATICS.NS",

"DCM Shriram": "DCMSHRIRAM.NS",
"DCM": "DCMSHRIRAM.NS",

"Delta Corp": "DELTACORP.NS",
"Delta": "DELTACORP.NS",

"Dr Lal PathLabs": "LALPATHLAB.NS",
"Lal Path": "LALPATHLAB.NS",

"eClerx Services": "ECLERX.NS",
"eClerx": "ECLERX.NS",

"Elgi Equipments": "ELGIEQUIP.NS",
"Elgi": "ELGIEQUIP.NS",

"Endurance Technologies": "ENDURANCE.NS",
"Endurance": "ENDURANCE.NS",

"Equitas Small Finance": "EQUITASBNK.NS",
"Equitas": "EQUITASBNK.NS",

# Cables & Infra
"Finolex Cables": "FINCABLES.NS",
"Finolex": "FINCABLES.NS",

"Fine Organic": "FINEORG.NS",
"Fine": "FINEORG.NS",

"Firstsource Solutions": "FSL.NS",
"Firstsource": "FSL.NS",

"Glenmark Pharma": "GLENMARK.NS",
"Glenmark": "GLENMARK.NS",

"GMR Airports": "GMRINFRA.NS",
"GMR": "GMRINFRA.NS",

"Graphite India": "GRAPHITE.NS",
"Graphite": "GRAPHITE.NS",

"Gujarat Fluorochem": "FLUOROCHEM.NS",
"Fluorochem": "FLUOROCHEM.NS",

"Gujarat State Petronet": "GSPL.NS",
"GSPL": "GSPL.NS",

# Telecom & IT
"HFCL": "HFCL.NS",
"Himachal Futuristic": "HFCL.NS",

"Happiest Minds": "HAPPSTMNDS.NS",
"Happiest": "HAPPSTMNDS.NS",

"Hatsun Agro": "HATSUN.NS",
"Hatsun": "HATSUN.NS",

"Honeywell Automation": "HONAUT.NS",
"Honeywell": "HONAUT.NS",

"ICRA": "ICRA.NS",
"ICRA Ltd": "ICRA.NS",

"IDBI Bank": "IDBI.NS",
"IDBI": "IDBI.NS",

"IEX": "IEX.NS",
"Indian Energy Exchange": "IEX.NS",

"India Cements": "INDIACEM.NS",
"India Cement": "INDIACEM.NS",

"Indian Bank": "INDIANB.NS",
"IndianBank": "INDIANB.NS",

"Indian Overseas Bank": "IOB.NS",
"IOB": "IOB.NS",

"Indiamart": "INDIAMART.NS",
"IndiaMart": "INDIAMART.NS",

"Ingersoll Rand": "INGERRAND.NS",
"Ingersoll": "INGERRAND.NS",

"Intellect Design": "INTELLECT.NS",
"Intellect": "INTELLECT.NS",

"Jindal Saw": "JINDALSAW.NS",
"JindalSaw": "JINDALSAW.NS",

"JK Lakshmi Cement": "JKLAKSHMI.NS",
"JK Lakshmi": "JKLAKSHMI.NS",


# Paper, Finance & Ceramics
"JK Paper": "JKPAPER.NS",
"JKP": "JKPAPER.NS",

"JM Financial": "JMFINANCIL.NS",
"JM": "JMFINANCIL.NS",

"JTEKT India": "JTEKTINDIA.NS",
"JTEKT": "JTEKTINDIA.NS",

"Jubilant Ingrevia": "JUBLINGREA.NS",
"Ingrevia": "JUBLINGREA.NS",

"Just Dial": "JUSTDIAL.NS",
"JD": "JUSTDIAL.NS",

"Kalyan Jewellers": "KALYANKJIL.NS",
"Kalyan": "KALYANKJIL.NS",

"Kajaria Ceramics": "KAJARIACER.NS",
"Kajaria": "KAJARIACER.NS",

"KEI Industries": "KEI.NS",
"KEI": "KEI.NS",

# Engineering & Tech
"Linde India": "LINDEINDIA.NS",
"Linde": "LINDEINDIA.NS",

"L&T Technology Services": "LTTS.NS",
"LTTS": "LTTS.NS",
"L&T Tech": "LTTS.NS",

"Mastek": "MASTEK.NS",
"Mastek Ltd": "MASTEK.NS",

"Metropolis Healthcare": "METROPOLIS.NS",
"Metropolis": "METROPOLIS.NS",

"Minda Corporation": "MINDACORP.NS",
"Minda": "MINDACORP.NS",

"MOIL": "MOIL.NS",
"MOIL Ltd": "MOIL.NS",

"Motilal Oswal": "MOTILALOFS.NS",
"Motilal": "MOTILALOFS.NS",

"Mphasis": "MPHASIS.NS",
"Mphasis Ltd": "MPHASIS.NS",

# Healthcare & Pharma
"Narayana Hrudayalaya": "NH.NS",
"Narayana": "NH.NS",
"NH": "NH.NS",

"Natco Pharma": "NATCOPHARM.NS",
"Natco": "NATCOPHARM.NS",

"NESCO": "NESCO.NS",
"NESCO Ltd": "NESCO.NS",

"NOCIL": "NOCIL.NS",
"NOCIL Ltd": "NOCIL.NS",

"Olectra Greentech": "OLECTRA.NS",
"Olectra": "OLECTRA.NS",

"Orient Electric": "ORIENTELEC.NS",
"Orient": "ORIENTELEC.NS",

"Page Industries": "PAGEIND.NS",
"Page": "PAGEIND.NS",
"Jockey": "PAGEIND.NS",

"Patanjali Foods": "PATANJALI.NS",
"Patanjali": "PATANJALI.NS",

# Diversified & Manufacturing
"Piramal Enterprises": "PEL.NS",
"Piramal": "PEL.NS",

"Poly Medicure": "POLYMED.NS",
"Polymed": "POLYMED.NS",

"Praj Industries": "PRAJIND.NS",
"Praj": "PRAJIND.NS",

"Prince Pipes": "PRINCEPIPE.NS",
"Prince": "PRINCEPIPE.NS",

"Quess Corp": "QUESS.NS",
"Quess": "QUESS.NS",

"Rain Industries": "RAIN.NS",
"Rain": "RAIN.NS",

"Rallis India": "RALLIS.NS",
"Rallis": "RALLIS.NS",

"Redington": "REDINGTON.NS",
"Redington Ltd": "REDINGTON.NS",

# Telecom & Infra
"Route Mobile": "ROUTE.NS",
"Route": "ROUTE.NS",

"STATE BANK OF INDIA": "SBIN.NS",
"SBI": "SBIN.NS",
"State Bank": "SBIN.NS",

"SJVN": "SJVN.NS",
"SJVN Ltd": "SJVN.NS",

"Solar Industries": "SOLARINDS.NS",
"Solar": "SOLARINDS.NS",

"Sterlite Technologies": "STLTECH.NS",
"Sterlite": "STLTECH.NS",

"Supreme Industries": "SUPREMEIND.NS",
"Supreme": "SUPREMEIND.NS",

"Tanla Platforms": "TANLA.NS",
"Tanla": "TANLA.NS",

"TTK Prestige": "TTKPRESTIG.NS",
"TTK": "TTKPRESTIG.NS",
"Prestige": "TTKPRESTIG.NS",


"UJJIVAN SMALL FINANCE": "UJJIVANSFB.NS",
"UJJIVAN": "UJJIVANSFB.NS",
"UJJIVAN SFB": "UJJIVANSFB.NS",

"V-GUARD": "VGUARD.NS",
"V GUARD": "VGUARD.NS",
"VGUARD": "VGUARD.NS",

"VIP INDUSTRIES": "VIPIND.NS",
"VIP": "VIPIND.NS",

"ZENSAR TECHNOLOGIES": "ZENSARTECH.NS",
"ZENSAR": "ZENSARTECH.NS",

"SUN TV NETWORK": "SUNTV.NS",
"SUN TV": "SUNTV.NS",
"SUNTV": "SUNTV.NS",

"ANANT RAJ": "ANANTRAJ.NS",
"ANANTRAJ": "ANANTRAJ.NS"

}

def clean_stocks(data):
    """Clean and normalize stock names to uppercase"""
    cleaned = {}
    for name, symbol in data.items():
        cleaned[name.upper()] = symbol
    return cleaned

# Apply cleaning
stocks_dict = clean_stocks(stocks_dict)

# ==========================================
# RESOLVE STOCK FUNCTION
# ==========================================
def resolve_stock_name(query: str) -> str:
    """Return ticker if query matches an alias or closest fuzzy match, else None."""
    if not query:
        return None
        
    query = query.strip().upper()   # normalize input

    # First try exact match
    if query in stocks_dict:
        return stocks_dict[query]

    # If no exact match, try fuzzy matching
    matches = difflib.get_close_matches(query, stocks_dict.keys(), n=1, cutoff=0.7)
    if matches:
        return stocks_dict[matches[0]]

    return None

# ==========================================
# SEARCH STOCKS FUNCTION
# ==========================================
def search_stocks(query: str):
    """
    Search for stocks matching the query
    Returns list of (stock_name, symbol) matches
    """
    if not query:
        return []
    
    query = query.strip().upper()
    results = []
    
    # Search through all stock names
    for name, symbol in stocks_dict.items():
        # Exact match
        if name == query:
            return [(name, symbol)]
        
        # Partial match (if query is contained in name)
        if query in name:
            results.append((name, symbol))
        
        # Check if query matches parts of the name
        elif any(query in part for part in name.split()):
            if (name, symbol) not in results:
                results.append((name, symbol))
    
    # If no results, try fuzzy matching
    if not results:
        matches = difflib.get_close_matches(query, stocks_dict.keys(), n=5, cutoff=0.6)
        for match in matches:
            results.append((match, stocks_dict[match]))
    
    return results[:10]  # Limit to 10 results

# ==========================================
# HELPER FUNCTIONS
# ==========================================
def get_all_stock_names():
    """Return list of all stock names for autocomplete"""
    return list(stocks_dict.keys())

def is_valid_stock(query):
    """Check if query is a valid stock name or ticker"""
    if not query:
        return False
    query = query.strip().upper()
    return query in stocks_dict or resolve_stock_name(query) is not None
     
# CLEAN STOCK
def clean_stocks(data):
    cleaned = {}
    for name, symbol in data.items():
        # normalize all keys to uppercase so lookups are consistent
        cleaned[name.upper()] = symbol
    return cleaned

# ✅ Apply cleaning
stocks_dict = clean_stocks(stocks_dict)

