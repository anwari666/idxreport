import pandas as pd
stock_df            = pd.read_csv('shortlist.csv')[['KodeEmiten']]
stock_list          = [s[0] for s in stock_df.values]
year_list           = [2016, 2017]
quarter_obj         = {
                        "TW1"       : "I" ,
                        "TW2"       : "II" ,
                        "TW3"       : "III" ,
                        "Tahunan"   : "Tahunan"    
                       }



for stock in stock_list:
    stock_dt = []
    year_dt = []
    q_dt = []
    profit_dt = []

    for year in year_list:

        for quarter_key in quarter_obj.keys():

            try:
                url = 'http://www.idx.co.id/Portals/0/StaticData/ListedCompanies/Corporate_Actions/New_Info_JSX/Jenis_Informasi/01_Laporan_Keuangan/02_Soft_Copy_Laporan_Keuangan//Laporan%20Keuangan%20Tahun%20{year}/{quarter_key}/{stock}/FinancialStatement-{year}-{quarter_val}-{stock}.xlsx'.format(    stock=stock,
                year=str(year),
                quarter_key= quarter_key if quarter_key != "Tahunan" else "Audit",
                quarter_val=quarter_obj.get(quarter_key, "none") )

                df = pd.read_excel(url, sheet_name=3, skiprows=2, usecols='A:D')

                print(stock, year, quarter_key)
                stock_dt.append(stock)
                year_dt.append(year)
                q_dt.append(quarter_key)
                profit_dt.append(df[df[df.columns[3]] == 'Total profit (loss)'].iloc[:,1].values[0])
            except Exception:
                print('File not found for '+ stock +'-'+ quarter_key +'-'+ str(year))
                pass


    raw_data = pd.DataFrame.from_dict({'stock_label':stock_dt, 'year':year_dt, 'quarter':q_dt, 'profit':profit_dt})
    raw_data.to_csv('source/'+stock+'.csv', index=False)