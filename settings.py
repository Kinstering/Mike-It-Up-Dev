import pandas as pd

api_key = '3NQ3eBCvOnTDpmkO6yOI7SkqoKvLhpF2ddFyaYWEQf0QmLyweQgx6Oyw62q5xNC9'
secret = 'YcOEDE19tnJIRZJxgI9hEugVmha4grCrEXDCJH7kNRJtdIwN38QO9FjFc71n636c'
end_point = "https://api.binance.com/api/v3/userDataStream"

Removed_coins = [ 'PEPEUSDT', 'FLOKIUSDT', 'BTTCUSDT', 'SHIBUSDT', 'LUNCUSDT', 'XECUSDT',  'EPXUSDT']

M_array_1 = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'NEOUSDT', 'LTCUSDT', 'QTUMUSDT', 'ADAUSDT', 'XRPUSDT', 'EOSUSDT','ARKUSDT', 
             'CREAMUSDT', 'CELRUSDT', 'DASHUSDT', 'OMGUSDT', 'THETAUSDT', 'ENJUSDT', 'MATICUSDT', 'ATOMUSDT', 'TFUELUSDT', 'ONEUSDT', 
             'ALGOUSDT', 'DOGEUSDT', 'DUSKUSDT', 'ANKRUSDT', 'WINUSDT', 'COSUSDT', 'MTLUSDT', 'PERLUSDT', 'DENTUSDT', 'KEYUSDT', 
             'TUSDUSDT', 'FTMUSDT', 'IOTAUSDT', 'XLMUSDT', 'ONTUSDT', 'TRXUSDT', 'ETCUSDT', 'ICXUSDT', 'NULSUSDT', 'VETUSDT',
             'LINKUSDT', 'VITEUSDT', 'WAVESUSDT', 'ONGUSDT', 'HOTUSDT', 'ZILUSDT', 'ZRXUSDT', 'FETUSDT', 'BATUSDT', 'XMRUSDT', 
             'ZECUSDT', 'IOSTUSDT']

M_array_2 = ['DOCKUSDT', 'WANUSDT', 'FUNUSDT', 'CVCUSDT', 'CHZUSDT', 'BANDUSDT', 'XTZUSDT', 'RENUSDT', 'RVNUSDT', 'FTTUSDT',
             'HBARUSDT', 'NKNUSDT', 'STXUSDT', 'KAVAUSDT', 'ARPAUSDT', 'IOTXUSDT', 'RLCUSDT', 'CTXCUSDT', 'BCHUSDT', 'TROYUSDT',
             'OGNUSDT', 'DREPUSDT', 'WRXUSDT', 'BTSUSDT', 'LSKUSDT', 'BNTUSDT', 'LTOUSDT', 'MBLUSDT', 'COTIUSDT', 'STPTUSDT',
             'WTCUSDT', 'DATAUSDT', 'SOLUSDT', 'CTSIUSDT', 'HIVEUSDT', 'CHRUSDT', 'ARDRUSDT', 'MDTUSDT', 'GFTUSDT', 'IQUSDT',
             'STMXUSDT', 'KNCUSDT', 'LRCUSDT', 'PNTUSDT', 'COMPUSDT', 'SCUSDT', 'ZENUSDT', 'SNXUSDT', 'VTHOUSDT', 'DGBUSDT' ]
  
M_array_3 = ['SXPUSDT', 'MKRUSDT', 'DCRUSDT', 'STORJUSDT', 'MANAUSDT', 'YFIUSDT', 'BALUSDT', 'BLZUSDT', 'NTRNUSDT', 'TIAUSDT',
             'IRISUSDT', 'KMDUSDT', 'JSTUSDT', 'ANTUSDT', 'CRVUSDT', 'SANDUSDT', 'OCEANUSDT', 'NMRUSDT', 'DOTUSDT', 'LUNAUSDT',
             'RSRUSDT', 'PAXGUSDT', 'WNXMUSDT', 'TRBUSDT', 'SUSHIUSDT', 'KSMUSDT', 'EGLDUSDT', 'DIAUSDT', 'RUNEUSDT', 'FIOUSDT',
             'UMAUSDT', 'BELUSDT', 'WINGUSDT', 'UNIUSDT', 'OXTUSDT', 'SUNUSDT', 'AVAXUSDT', 'FLMUSDT', 'ORNUSDT', 'UTKUSDT',
             'XVSUSDT', 'ALPHAUSDT', 'AAVEUSDT', 'NEARUSDT', 'FILUSDT', 'INJUSDT', 'AUDIOUSDT', 'CTKUSDT', 'AKROUSDT', 'AXSUSDT' ]

M_array_4 = ['HARDUSDT', 'STRAXUSDT', 'UNFIUSDT', 'ROSEUSDT', 'AVAUSDT', 'XEMUSDT', 'SKLUSDT', 'GRTUSDT', 'JUVUSDT', 'PSGUSDT',
             '1INCHUSDT', 'REEFUSDT', 'OGUSDT', 'ATMUSDT', 'ASRUSDT', 'CELOUSDT', 'RIFUSDT', 'TRUUSDT', 'CKBUSDT', 'TWTUSDT',
             'FIROUSDT', 'LITUSDT', 'SFPUSDT', 'DODOUSDT', 'CAKEUSDT', 'ACMUSDT', 'BADGERUSDT', 'FISUSDT', 'OMUSDT', 'PONDUSDT',
             'DEGOUSDT', 'ALICEUSDT', 'LINAUSDT', 'PERPUSDT', 'SUPERUSDT', 'CFXUSDT', 'TKOUSDT', 'PUNDIXUSDT', 'TLMUSDT', 'BARUSDT',
             'FORTHUSDT', 'BAKEUSDT', 'BURGERUSDT', 'SLPUSDT', 'ICPUSDT', 'ARUSDT', 'POLSUSDT', 'MDXUSDT', 'MASKUSDT',
             'MEMEUSDT', 'ORDIUSDT']

M_array_5 = ['LPTUSDT', 'XVGUSDT', 'ATAUSDT', 'GTCUSDT', 'ERNUSDT', 'KLAYUSDT', 'PHAUSDT', 'BONDUSDT', 'MLNUSDT', 'DEXEUSDT', 
             'C98USDT', 'CLVUSDT', 'QNTUSDT', 'FLOWUSDT', 'TVKUSDT', 'MINAUSDT', 'RAYUSDT', 'FARMUSDT', 'ALPACAUSDT', 'QUICKUSDT',
             'MBOXUSDT', 'FORUSDT', 'REQUSDT', 'GHSTUSDT', 'WAXPUSDT', 'GNOUSDT', 'ELFUSDT', 'DYDXUSDT', 'IDEXUSDT',
             'VIDTUSDT', 'GALAUSDT', 'ILVUSDT', 'YGGUSDT', 'SYSUSDT', 'DFUSDT', 'FIDAUSDT', 'FRONTUSDT', 'CVPUSDT', 'AGLDUSDT',
             'RADUSDT', 'BETAUSDT', 'RAREUSDT', 'LAZIOUSDT', 'CHESSUSDT', 'ADXUSDT', 'AUCTIONUSDT', 'DARUSDT', 'BNXUSDT', 'MOVRUSDT',
             'BEAMXUSDT', 'PIVXUSDT']

M_array_6 = ['CITYUSDT', 'ENSUSDT', 'KP3RUSDT', 'QIUSDT', 'PORTOUSDT', 'POWRUSDT', 'VGXUSDT', 'JASMYUSDT', 'AMPUSDT', 'PLAUSDT',
             'PYRUSDT', 'RNDRUSDT', 'ALCXUSDT', 'SANTOSUSDT', 'BICOUSDT', 'FLUXUSDT', 'FXSUSDT', 'VOXELUSDT', 'HIGHUSDT', 'CVXUSDT',
             'PEOPLEUSDT', 'OOKIUSDT', 'SPELLUSDT', 'JOEUSDT', 'ACHUSDT', 'IMXUSDT', 'GLMRUSDT', 'LOKAUSDT', 'SCRTUSDT', 'API3USDT',
             'ACAUSDT', 'XNOUSDT', 'WOOUSDT', 'ALPINEUSDT', 'TUSDT', 'ASTRUSDT', 'GMTUSDT', 'KDAUSDT', 'APEUSDT',
             'BSWUSDT', 'BIFIUSDT', 'MULTIUSDT', 'STEEMUSDT', 'MOBUSDT', 'NEXOUSDT', 'REIUSDT', 'GALUSDT', 'LDOUSDT']

M_array_7 = ['OPUSDT', 'LEVERUSDT', 'STGUSDT', 'GMXUSDT', 'POLYXUSDT', 'APTUSDT', 'OSMOUSDT', 'HFTUSDT', 'PHBUSDT',
             'HOOKUSDT', 'MAGICUSDT', 'HIFIUSDT', 'RPLUSDT', 'PROSUSDT', 'AGIXUSDT', 'GNSUSDT', 'SYNUSDT', 'VIBUSDT', 'SSVUSDT',
             'LQTYUSDT', 'AMBUSDT', 'USTCUSDT', 'GASUSDT', 'GLMUSDT', 'PROMUSDT', 'QKCUSDT', 'UFTUSDT', 'IDUSDT', 'ARBUSDT',
             'LOOMUSDT', 'OAXUSDT', 'RDNTUSDT', 'WBTCUSDT', 'EDUUSDT', 'SUIUSDT', 'AERGOUSDT', 'ASTUSDT',
             'SNTUSDT', 'COMBOUSDT', 'MAVUSDT', 'PENDLEUSDT', 'ARKMUSDT', 'WBETHUSDT', 'WLDUSDT', 'FDUSDUSDT', 'SEIUSDT', 'CYBERUSDT']


total_df     = pd.DataFrame({'coin': pd.Series(dtype='str'), 'price': pd.Series(dtype='float'), 'amount': pd.Series(dtype='float'), 'buyer': pd.Series(dtype='boolean')})
total_df_15m = pd.DataFrame({'coin': pd.Series(dtype='str'), 'price': pd.Series(dtype='float'), 'amount': pd.Series(dtype='float'), 'buyer': pd.Series(dtype='boolean')})
total_df_4h  = pd.DataFrame({'coin': pd.Series(dtype='str'), 'price': pd.Series(dtype='float'), 'amount': pd.Series(dtype='float'), 'buyer': pd.Series(dtype='boolean')})


liq_df = pd.DataFrame({'coin': pd.Series(dtype='str'), 'price': pd.Series(dtype='float'), 'amount': pd.Series(dtype='float'), 'type': pd.Series(dtype='str')})
liq_df_15m = pd.DataFrame({'coin': pd.Series(dtype='str'), 'price': pd.Series(dtype='float'), 'amount': pd.Series(dtype='float'), 'type': pd.Series(dtype='str')})
liq_df_4h = pd.DataFrame({'coin': pd.Series(dtype='str'), 'price': pd.Series(dtype='float'), 'amount': pd.Series(dtype='float'), 'type': pd.Series(dtype='str')})
