import streamlit as st
import pandas as pd

class cost_heatpump:
    def __init__(self):
        pass
    
    def run_all_non_streamlit(self):
        self.input_non_streamlit()
        self.read_price_excel()
        self.find_correct_price()
        self.read_datasheet_excel()
        self.results_non_streamlit()

    def run_all_streamlit(self):
        self.input_streamlit()
        self.read_price_excel()
        self.find_correct_price()
        self.read_datasheet_excel()
        self.results_streamlit()

    ### INPUT ######################################################################################################################
    def input_non_streamlit(self):
        self.power_demand =         250                 #kW  Mellom 50 og 500
        self.delivered_temp_DUT =   '40-45 \u2103'      # eller '50-55 \u2103'

    # OR:

    def input_streamlit(self):
        st.set_page_config(page_title="Priser på Varmepumpe", page_icon="🔥")
        with open("styles/main.css") as f:
            st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)
        
        st.title('Priser på varmepumpe')
        st.subheader('Ønsket spesifikasjon')
        
        self.power_demand = st.number_input('Ønsket effekt (kW)',value=100,min_value=50,max_value=500,step=1)
        self.delivered_temp_DUT = st.selectbox('delivered_temperatur ved DUT',options=['40-45 \u2103', '50-55 \u2103'])
    ##################################################################################################################################


    ### CALCULATIONS #################################################################################################################
    def read_price_excel(self):
        price_sheet = pd.read_excel('Priser Varmepumpeanlegg.xlsx',sheet_name='Sheet1',usecols='D:O')
        self.cost_fasility_40_45 = price_sheet.iloc[5,3:].reset_index(drop=True)
        self.cost_installation_40_45 = price_sheet.iloc[6,3:].reset_index(drop=True)

        self.cost_fasility_50_55 = price_sheet.iloc[9,3:].reset_index(drop=True)
        self.cost_installation_50_55 = price_sheet.iloc[10,3:].reset_index(drop=True)

        self.power = price_sheet.iloc[4,3:].reset_index(drop=True)
        self.type_of_HP_list = price_sheet.iloc[13,3:].reset_index(drop=True)

    # AND:

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

        #if price_index != 0:
        #    self.type_of_HP1 = self.type_of_HP_list.iloc[price_index-1]
        self.type_of_HP2 = self.type_of_HP_list.iloc[price_index]
        
        if self.delivered_temp_DUT == '40-45 \u2103':
            if price_index != 0:
                cost_fasility_1 = self.cost_fasility_40_45.iloc[price_index-1]
                cost_installation_1 = self.cost_installation_40_45.iloc[price_index-1]
            cost_fasility_2 = self.cost_fasility_40_45.iloc[price_index]
            cost_installation_2 = self.cost_installation_40_45.iloc[price_index]
        elif self.delivered_temp_DUT == '50-55 \u2103':
            if price_index != 0:
                cost_fasility_1 = self.cost_fasility_50_55.iloc[price_index-1]
                cost_installation_1 = self.cost_installation_50_55.iloc[price_index-1]
            cost_fasility_2 = self.cost_fasility_50_55.iloc[price_index]
            cost_installation_2 = self.cost_installation_50_55.iloc[price_index]

        if price_index != 0:
            self.cost_fasility = lin_int(self.power_demand,power_1,power_2,cost_fasility_1,cost_fasility_2)
            self.cost_installation = lin_int(self.power_demand,power_1,power_2,cost_installation_1,cost_installation_2)
        else:
            self.cost_fasility = cost_fasility_2
            self.cost_installation = cost_installation_2

        self.total_cost = self.cost_fasility+self.cost_installation
        self.power_2 = power_2
        
    # AND:

    def read_datasheet_excel(self):
        delivered_temp_str = self.delivered_temp_DUT.replace(' \u2103','')
        self.hp_name2 = None

        if self.type_of_HP2 == '1x Steel 55.4':
            self.number_of_hp = 1
            self.hp_name = f'STEEL 55.4 {delivered_temp_str}'
            self.hp_power = '50'
        elif self.type_of_HP2 == '1x IRON 120.2':
            self.number_of_hp = 1
            self.hp_name = f'IRON 120.2 {delivered_temp_str}'
            self.hp_power = '100'
        elif self.type_of_HP2 == '1x IRON 170.2':
            self.number_of_hp = 1
            self.hp_name = f'IRON 170.2 {delivered_temp_str}'
            self.hp_power = '150'
        elif self.type_of_HP2 == '2x IRON 120.2':
            self.number_of_hp = 2
            self.hp_name = f'IRON 120.2 {delivered_temp_str}'
            self.hp_power = '2x100'
        elif self.type_of_HP2 == '1x IRON 120.2 +\n1x IRON 170.2':
            self.number_of_hp = 1
            self.hp_name = f'IRON 120.2 {delivered_temp_str}'
            self.number_of_hp2 = 1
            self.hp_name2 = f'IRON 170.2 {delivered_temp_str}'
            self.hp_power = '100+150'
        elif self.type_of_HP2 == '2x IRON 170.2':
            self.number_of_hp = 2
            self.hp_name = f'IRON 170.2 {delivered_temp_str}'
            self.hp_power = '2x150'
        elif self.type_of_HP2 == '2x IRON 200.2':
            self.number_of_hp = 2
            self.hp_name = f'IRON 200.2 {delivered_temp_str}'
            self.hp_power = '2x175'
        elif self.type_of_HP2 == '3x IRON 150.2':
            self.number_of_hp = 3
            self.hp_name = f'IRON 150.2 {delivered_temp_str}'
            self.hp_power = '3x133'
        elif self.type_of_HP2 == '3x IRON 200.2':
            self.number_of_hp = 2
            self.hp_name = f'IRON 200.2 {delivered_temp_str}'
            self.hp_power = '2x175'
        
        
        self.datasheet = pd.read_excel('Varmepumper til prisberegning.xlsx',sheet_name=self.hp_name) 
        self.cop = float(self.datasheet[self.datasheet['HEATING MODE'].str.match('COP')].iloc[0,-1])
        
        if self.hp_name2 is not None:
            self.datasheet2 = pd.read_excel('Varmepumper til prisberegning.xlsx',sheet_name=self.hp_name2)
            self.cop2 = float(self.datasheet2[self.datasheet2['HEATING MODE'].str.match('COP')].iloc[0,-1])
    ##################################################################################################################################
    

    ### RESULTS ######################################################################################################################
    def results_non_streamlit(self):
        print('')
        print('RESULTATER:')
        print(f'Pris for selve anlegget: {self.cost_fasility} kr')
        print(f'Pris for installasjon: {self.cost_installation} kr')
        print(f'Pris totalt: {self.total_cost} kr')
        print('')
        print(f'Eksempel på varmepumpe som dekker dette: {self.type_of_HP2}')
        print('')

        print('Data for eksempel-varmepumper:')
        print(f'{self.hp_name} \u2103 ({self.number_of_hp} stk):')
        print(f'Effekt: {self.hp_power} kW')
        print(f'COP (inntakstemperatur 4 \u2103): {self.cop}')
        print('')
        print(self.datasheet)

        if self.hp_name2 is not None:
            print('')
            print(f'{self.hp_name2} \u2103 ({self.number_of_hp2} stk):')
            print(f'Effekt: {self.hp_power} kW')
            print(f'COP (inntakstemperatur 4 \u2103): {self.cop2}')
            print('')
            print(self.datasheet2)

    # OR:

    def results_streamlit(self):
        st.markdown('---')
        st.subheader('Priser for denne effekten blir:')
        
        c1,c2,c3 = st.columns(3)
        with c1:
            st.metric('Pris for anlegg',value=f'{self.cost_fasility:,} kr'.replace(",", " "))
        with c2:
            st.metric('Pris for installasjon',value=f'{self.cost_installation:,} kr'.replace(",", " "))
        with c3:
            st.metric('Totalpris',value=f'{self.total_cost:,} kr'.replace(",", " "))
        
        st.metric('Eksempel på varmepumpe(r) som dekker dette:',value=self.type_of_HP2)

        st.markdown('---')
        st.subheader(f'Data for eksempel-varmepumper')
        st.markdown(f'{self.hp_name} \u2103 ({self.number_of_hp} stk):')
        
        c1,c2 = st.columns(2)
        with c1:
            st.metric('Effekt',value=f'{self.hp_power} kW')
        with c2:
            st.metric('COP (inntakstemperatur 4 \u2103):',value=self.cop)
        st.dataframe(self.datasheet)
        
        if self.hp_name2 is not None:
            st.markdown('---')
            st.markdown(f'{self.hp_name2} \u2103 ({self.number_of_hp2} stk):')
            c1,c2 = st.columns(2)
            with c1:
                st.metric('Effekt',value=f'{self.hp_power} kW')
            with c2:
                st.metric('COP (inntakstemperatur 4 \u2103):',value=self.cop2)

            st.dataframe(self.datasheet2)
    ##################################################################################################################################


### RUN ##############################################################################################################################

#cost_heatpump().run_all_streamlit()
cost_heatpump().run_all_non_streamlit()