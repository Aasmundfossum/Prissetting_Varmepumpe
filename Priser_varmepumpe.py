import streamlit as st
import pandas as pd




class cost_heatpump:
    def __init__(self):
        pass
    
    def run_all_without_streamlit(self):
        self.input()
        self.read_price_excel()
        self.find_correct_price()
        self.read_datasheet_excel()


    def run_all_with_streamlit(self):
        self.streamlit_input()
        
        self.read_price_excel()
        self.find_correct_price()
        self.read_datasheet_excel()
        
        self.streamlit_results()

    ### Program
    def input(self):
        self.power_demand = 100 #kW
        self.delivered_temp_DUT = '40-45 \u2103'  # eller '50-55 \u2103'

    ### Common
    def read_price_excel(self):
        price_sheet = pd.read_excel('Priser Varmepumpeanlegg.xlsx',sheet_name='Sheet1',usecols='D:O')
        self.cost_fasility_40_45 = price_sheet.iloc[5,3:].reset_index(drop=True)
        self.cost_installation_40_45 = price_sheet.iloc[6,3:].reset_index(drop=True)

        self.cost_fasility_50_55 = price_sheet.iloc[9,3:].reset_index(drop=True)
        self.cost_installation_50_55 = price_sheet.iloc[10,3:].reset_index(drop=True)

        self.power = price_sheet.iloc[4,3:].reset_index(drop=True)
        self.type_of_HP_list = price_sheet.iloc[13,3:].reset_index(drop=True)

    def find_correct_price(self):

        def lin_int(x,x1,x2,y1,y2):
            y = y1+(x-x1)*(y2-y1)/(x2-x1)
            return y
        

        for i in range(0,len(self.power)):
            if self.power_demand <= self.power.iloc[i]:
                price_index=i
                break

        power_1 = self.power.iloc[price_index-1]
        power_2 = self.power.iloc[price_index]

        if price_index != 0:
            self.type_of_HP1 = self.type_of_HP_list.iloc[price_index-1]
        self.type_of_HP2 = self.type_of_HP_list.iloc[price_index]
        
        if self.delivered_temp_DUT == '40-45 \u2103':
            if price_index != 0:
                cost_fasility_1 = self.cost_fasility_40_45.iloc[price_index-1]
            cost_fasility_2 = self.cost_fasility_40_45.iloc[price_index]
            if price_index != 0:
                cost_installation_1 = self.cost_installation_40_45.iloc[price_index-1]
            cost_installation_2 = self.cost_installation_40_45.iloc[price_index]
        elif self.delivered_temp_DUT == '50-55 \u2103':
            if price_index != 0:
                cost_fasility_1 = self.cost_fasility_50_55.iloc[price_index-1]
            cost_fasility_2 = self.cost_fasility_50_55.iloc[price_index]
            if price_index != 0:
                cost_installation_1 = self.cost_installation_50_55.iloc[price_index-1]
            cost_installation_2 = self.cost_installation_50_55.iloc[price_index]

        if price_index != 0:
            self.cost_fasility = lin_int(self.power_demand,power_1,power_2,cost_fasility_1,cost_fasility_2)
            self.cost_installation = lin_int(self.power_demand,power_1,power_2,cost_installation_1,cost_installation_2)
        else:
            self.cost_fasility = cost_fasility_2
            self.cost_installation = cost_installation_2

        self.total_cost = self.cost_fasility+self.cost_installation
        

    def read_datasheet_excel(self):


        self.vp_name = 'IRON 120.2 50-55'
        datasheet = pd.read_excel('Varmepumper til prisberegning.xlsx',sheet_name=self.vp_name) 

        #self.cop = float(datasheet[datasheet['HEATING MODE'].str.match('COP')].iloc[0,-1])
        
    
    ### STREAMLIT
    def streamlit_input(self):
        st.set_page_config(page_title="Priser på Varmepumpe", page_icon="🔥")

        with open("styles/main.css") as f:
            st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)
        
        st.title('Priser på varmepumpe')
        st.subheader('Ønsket spesifikasjon')
        self.power_demand = st.number_input('Ønsket effekt (kW)',value=100,min_value=0,max_value=600,step=1)
        self.delivered_temp_DUT = st.selectbox('Leveransetemperatur ved DUT',options=['40-45 \u2103', '50-55 \u2103'])

    def streamlit_results(self):
        st.subheader('Priser for denne effkten blir:')
        c1,c2,c3 = st.columns(3)
        with c1:
            st.metric('Pris for anlegg',value=f'{self.cost_fasility:,} kr'.replace(",", " "))
        with c2:
            st.metric('Pris for installasjon',value=f'{self.cost_installation:,} kr'.replace(",", " "))
        with c3:
            st.metric('Totalpris',value=f'{self.total_cost:,} kr'.replace(",", " "))

        
        #def rounding_to_int(number):
        #    number = round(number, 1)
        #    return f"{number:,}".replace(",", " ")
        
        
        st.metric('Type varmepumpe',value=self.type_of_HP2)

        #st.subheader('Data for den anbefalte varmepumpen')
        #c1,c2,c3 = st.columns(3)
        #with c1:
        #    st.metric('COP',value=self.cop)
        #with c2:
        #    st.metric('Lala',value=f'{0} enhet')
        #with c3:
        #    st.metric('Lala',value=f'{0} enhet')


cost_heatpump().run_all_with_streamlit()