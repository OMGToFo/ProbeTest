
import streamlit as st

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import altair as alt

import matplotlib.pyplot as plt

#für Excel-Export-Funktionen
from io import BytesIO
from pyxlsb import open_workbook as open_xlsb

#Spezieller Optionsmenu
from streamlit_option_menu import option_menu



_="""
import matplotlib.pyplot as plt

import math

import time

from PIL import Image
"""

################ Layout und Farben ###############################

st.set_page_config(layout='wide', page_title='Benchmark - DB' )


#from scipy.optimize import minimize

#from gekko import GEKKO


FARBE_Maxwert = "#0078D7"

FARBE_Mittelwert = "#FFFFFF"

FARBE_Minwert = "#FF0000"


FARBE_Frau = "#C11D66"
FARBE_Mann = "#00B5D7"

FARBE_16_29 = "#11AA72"
FARBE_30_49 = "#D47D0F"
FARBE_50plus = "#908E7E"

FARBE_Deutsch = "#0078D7"
FARBE_Französisch = "#FF0000"




##Tip #   Reichweitenkurven - bei Serienberechnungen numpy.exp verwenden!!! ########







##############  Variabeldefinitionen ###################################3


DatenVorhanden = False


datenImportAuswahl = "Manuell"


df_ManuellImportierteDB = pd.DataFrame()

CampaignCheck_df = pd.DataFrame()

df_CampaignCheckAuswertungsSelektion = pd.DataFrame()



df_KampagnenAuswahl = pd.DataFrame() #Ein Datenframe dass nur alle getesteten Kampagnen enthält

df_KampagnenAuswahlSelektion = pd.DataFrame() #Kampagendaten für die Verwendungen von Filtern


df_Kampagnen = pd.DataFrame() #Datafrane mit aggregierten Daten pro Kampagne


df_BefragteMitOnlineKontakten = pd.DataFrame() #Dataframe das bei Berechnungen/Abbildungen zu den gemessenen Online-Werbekontakten verwendet wird

KPIAuswahl ="Start/File upload"



UnternehmenAuswahlAlsText = ""




############ Session State um Menu-Auswahl temporär zu speichern ##########################3


#Unternehmensauswahl Multiselect Box

_="""
if "Unternehmen_Gespeichert" not in st.session_state:
    # set the initial default value of the  widget
    st.session_state.Unternehmen_Gespeichert = "keine Eingabe"
"""












#######################Ees geht looo ooos  ##############################################






startText, lottieBild = st.columns((0.5, 1))
#lottieBild, startText = st.columns((0.5, 1))

with startText:
	#st.header("DES Benchmarks")
	
	#So kann man die Fonts indivudell anpassen
	st.markdown(""" <style> .font {
	font-size:38px ; font-family: 'Cooper Black'; color: #8CB6D8";} 
	</style> """, unsafe_allow_html=True)
	st.markdown('<p class="font">CCC/DES Benchmarks</p>', unsafe_allow_html=True)
	
	
	
	st.write("")
	
	st.write("Dieses Tool gibt vergleichbare Benchmarkwerte aus, die bei Campaign Check Befragungen und Digitial Effectivness Studien erhoben wurden.")

	st.write("KPI's sowie Marken und Zielgruppen können links ausgewählt werden.")

	





##### Aninimertes -Logo mit Lottie ############################################################
	
import requests

from streamlit_lottie import st_lottie


def load_lottieurl(url: str):
	r = requests.get(url)
	if r.status_code != 200:
		return None
	return r.json()


lottie_animation = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_9wpyhdzo.json")



with lottieBild: 
	st_lottie(lottie_animation, height=300)


###########################################################################################


placeholder = st.empty()



######### Automatischer oder manueller Import der Excel mrf Datenbank mit Steuerwerten  *************

if KPIAuswahl == "Start/File upload":
	datenImportAuswahl = placeholder.radio("Automatischer/Manueller Datenimport", ('Manuell', 'Automatisch'))





#Probiere es diesmal mit einen Funktion




# Manueller Dateminport ####################################################################################

if KPIAuswahl == "Start/File upload":

	if datenImportAuswahl == 'Manuell':
	
		data_file = placeholder.file_uploader("Eigene Datenbank einlesen", type=["csv"])
	
		#Funktion um Daten in das Datenframe einzulesen:
		@st.experimental_memo(suppress_st_warning=True) #um funtionswerte zu cachen, neue Variante von st.cache
		def load_data_manuell():
			if data_file is not None:
				#st.write(type(data_file))
				file_details = {"filename":data_file.name,"filesize":data_file.size}
				#st.write(file_details)
				df_ManuellImportierteDB = pd.read_csv(data_file)
				
				#Zeilen ohne Werte bei Geschlecht und Alter rauslöschen:
				df_ManuellImportierteDB.dropna(subset = ["Geschlecht"], inplace=True)
				df_ManuellImportierteDB.dropna(subset = ["Alter"], inplace=True)
				
				#df_ManuellImportierteDB["Werbeerinnerung"] = 100 * df_CampaignCheckAuswertungsSelektion["Werbeerinnerung"]
				df_ManuellImportierteDB["Markenbekanntheit"] = 100 * df_ManuellImportierteDB["Markenbekanntheit"]
				df_ManuellImportierteDB["Consideration"] = 100 * df_ManuellImportierteDB["Consideration"]
				df_ManuellImportierteDB["First Choice_codiert"] = 100 * df_ManuellImportierteDB["First Choice_codiert"]
				
				#Markensympathie 7-10 für Funnel umcodieren
				#df_ManuellImportierteDB['Sympathie_7bis10'] = df_ManuellImportierteDB['Sympathie'].apply(lambda x: 1 if x > 6       else 0)
				#df_ManuellImportierteDB['Sympathie_7bis10'] = pd.cut(df_ManuellImportierteDB.Sympathie, bins=[0,6,7], values=[0,100])
				df_ManuellImportierteDB['Sympathie_7bis10'] = df_ManuellImportierteDB['Sympathie'].replace([1,2,3,4,5,6,7,8,9,10],[0,0,0,0,0,0,100,100,100,100])
				
				#Bearbeutung/Umwandlung der Begin (Befragungsanfang)- Spalte
				
				#df_ManuellImportierteDB["Datum_formatiert"] = pd.to_datetime(df_ManuellImportierteDB["Begin"])
				#df_ManuellImportierteDB["Jahr"] = df_ManuellImportierteDB["Datum_formatiert"].dt.strftime("%Y")
				#df_ManuellImportierteDB["Monat"] = df_ManuellImportierteDB["Datum_formatiert"].dt.strftime("%m")
				
				#DES - Die automatisch Umcodierung war leider sehr langsam, habe deshalb mit String-Aufteilung gemacht:
				
				df_ManuellImportierteDB["Monat"] = df_ManuellImportierteDB.Begin.str.split('.').str[1]
				df_ManuellImportierteDB["TagMonatJahr"] = df_ManuellImportierteDB.Begin.str.split('-').str[0]
				df_ManuellImportierteDB["Jahr"] = df_ManuellImportierteDB.TagMonatJahr.str.split('.').str[2]
				df_ManuellImportierteDB["UG_Jahr_Monat"] = df_ManuellImportierteDB["Unternehmen"] +" - "+ df_ManuellImportierteDB["Jahr"] + " - "+ df_ManuellImportierteDB["Monat"]
				#df_ManuellImportierteDB["Jahr"] = (df_ManuellImportierteDB["Jahr"].astype(str))
				#st.write(df_ManuellImportierteDB['Jahr'].describe())
				
				
				
				#CCC Kampagnen - Jahr und Monate aus Kampagnen-Variablen extrahieren...
				#if df_ManuellImportierteDB["Erhebung"].any() == "CCC":
				df_ManuellImportierteDB["Monat_Jahr_CCC"] = df_ManuellImportierteDB.Kampagne.str.split('-').str[2]	
				df_ManuellImportierteDB["Monat_CCC"] = df_ManuellImportierteDB.Monat_Jahr_CCC.str.split(' ').str[1]
				df_ManuellImportierteDB["Jahr_CCC"] = df_ManuellImportierteDB.Monat_Jahr_CCC.str.split(' ').str[2]
				df_ManuellImportierteDB['Monat_CCC'] = df_ManuellImportierteDB['Monat_CCC'].replace(['Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember'],['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12'])
				
				#Jahreszahl aus DES und CCC in eine neu Kolumne/Variabe schreiben und formatieren
				df_ManuellImportierteDB['Jahr_Gesamt'] = np.where(df_ManuellImportierteDB.Erhebung == "CCC",df_ManuellImportierteDB.Jahr_CCC,df_ManuellImportierteDB.Jahr)
				df_ManuellImportierteDB['Jahr_Gesamt'].replace(["43"], ["2019"], inplace=True)
				df_ManuellImportierteDB['Jahr_Gesamt'].replace(["2021 "], ["2021"], inplace=True)
				df_ManuellImportierteDB["Jahr_Gesamt"] = df_ManuellImportierteDB["Jahr_Gesamt"].astype(str)
				
				
				#Jahr_Monat - für Zeitserien
				df_ManuellImportierteDB["Jahr_Monat"] = df_ManuellImportierteDB["Jahr_Gesamt"] +" - "+ df_ManuellImportierteDB["Monat"]
				
				#Indexvariable je Befragter erstellen - Participantnr + Zeitpunkt
				df_ManuellImportierteDB["Participant_string"] = df_ManuellImportierteDB["Participant"].astype(str)
				df_ManuellImportierteDB["Begin_string"] = df_ManuellImportierteDB["Begin"].astype(str)
				df_ManuellImportierteDB["Participant_Begin"] = df_ManuellImportierteDB["Participant_string"] +" - "+ df_ManuellImportierteDB["Begin_string"]
				
				#Unternehmen - Erster Buchstabe gross schreiben (besser für Dropdown-Sortierung)
				df_ManuellImportierteDB['Unternehmen'] = df_ManuellImportierteDB['Unternehmen'].str.capitalize()
				
				
				#Codiere Symthatie-Werte 11 in missing um, 11 = "kenne marke nicht"
				df_ManuellImportierteDB['Sympathie'].replace([11], [np.nan], inplace=True)			
				
				#Codiere auf 100er-Skala um:
				df_ManuellImportierteDB["Werbeerinnerung"] = 100 * df_ManuellImportierteDB["Werbeerinnerung"]			
			
				#Codiere ALtersklassen um, für bessere Sortierung
				df_ManuellImportierteDB['Alter'].replace(["<20"], ["16-19"], inplace=True)
				df_ManuellImportierteDB['Alter'].replace(["Jünger als 20 Jahre"], ["16-19"], inplace=True)
				df_ManuellImportierteDB['Alter'].replace(["45 - 49 Jahre"], ["45-49"], inplace=True)
				df_ManuellImportierteDB['Alter'].replace(["25 - 29 Jahre"], ["25-29"], inplace=True)
				df_ManuellImportierteDB['Alter'].replace(["35 - 39 Jahre"], ["35-39"], inplace=True)
				df_ManuellImportierteDB['Alter'].replace(["40 - 44 Jahre"], ["40-44"], inplace=True)
				df_ManuellImportierteDB['Alter'].replace(["20 - 24 Jahre"], ["20-24"], inplace=True)
				df_ManuellImportierteDB['Alter'].replace(["30 - 34 Jahre"], ["30-34"], inplace=True)
				df_ManuellImportierteDB['Alter'].replace(["50 - 55 Jahre"], ["50-54"], inplace=True)
				df_ManuellImportierteDB['Alter'].replace([">=60"], ["60+"], inplace=True)
				
				
				df_ManuellImportierteDB['Altersklasse'] = df_ManuellImportierteDB['Alter'].replace(['16-19', '20-24', '25-29','30-34','35-39','40-44','45-49','50-54','55-59','60+' ],['16-29', '16-29', '16-29','30-49','30-49','30-49','30-49','50+','50+','50+'])
				
				
				df_ManuellImportierteDB['GetestetesWerbeMedium'].replace(["OnlineOOH"], ["Online und OOH"], inplace=True)
				
				#Labeling
				df_ManuellImportierteDB['Recognition'] = df_ManuellImportierteDB['Recognition'].replace([1,2,3],['Ja', 'Nein', 'Weiss nicht'])
			
				df_ManuellImportierteDB['Recognition_Wert'] = df_ManuellImportierteDB['Recognition'].replace(['Ja', 'Nein', 'Weiss nicht'],[100, 0, 0])
			
				df_ManuellImportierteDB['Kampagnentest'] = df_ManuellImportierteDB['Recognition'].replace(['Ja', 'Nein', 'Weiss nicht', np.nan],['Ja','Ja','Ja','Nein'])
				
				#weiss nich zu nein am Ende
				df_ManuellImportierteDB['Recognition'] = df_ManuellImportierteDB['Recognition'].replace(['Ja', 'Nein', 'Weiss nicht'],['Ja', 'Nein', 'Nein'])
				
				df_ManuellImportierteDB['Unternehmen'].replace(["Mercedes-benz"], ["Mercedes"], inplace=True)
				df_ManuellImportierteDB['Unternehmen'].replace(["Nissan "], ["Nissan"], inplace=True)
				df_ManuellImportierteDB['Unternehmen'].replace(["Renault "], ["Renault"], inplace=True)	
				df_ManuellImportierteDB['Unternehmen'].replace(["Seat "], ["Seat"], inplace=True)
				
				GesamtDB_Expander = st.expander("Rohdaten einsehen:")
				with GesamtDB_Expander:
					st.write(df_ManuellImportierteDB)
				
				
				placeholder.text("Daten wurden erfolgreich geladen. Nun links Marken oder Kampagnen-KPIs auswählen")
				
				
				
				
			return df_ManuellImportierteDB




		#Wenn Daten vorhanden sind
		if data_file is not None:
		
	
			
		
			CampaignCheck_df = load_data_manuell() #Campaigncheck_df enthält die gesamt-DB "Grundgesamtheit"
			
			DatenVorhanden = True
			#st.balloons()
			
			#st.success('Daten erfolgreich geladen. Nun kannst die KPI links auswählen')
			#placeholder.info('<<< Nun kannst Du links die KPI auswählen')
			

			
			#df_Kampagnen = df_ManuellImportierteDB.dropna(subset = ['Recognition'], inplace=True)
			df_KampagnenAuswahl = CampaignCheck_df.drop(CampaignCheck_df[CampaignCheck_df.Kampagnentest == "Nein"].index)
	
			if KPIAuswahl == "Start/File upload":
				df_CampaignCheckAuswertungsSelektion = CampaignCheck_df #df_KampagnenAuswahlSelektion wird filterungen verwend

			
			if KPIAuswahl == "Marken-KPIs":
				df_CampaignCheckAuswertungsSelektion = CampaignCheck_df	#df_CampaignCheckAuswertungsSelektion enthält Daten die weiter gefiltert werden
			
			if KPIAuswahl == "Kampagnen-KPIs":
				df_CampaignCheckAuswertungsSelektion = df_KampagnenAuswahl #df_KampagnenAuswahlSelektion wird filterungen verwendet
		
			#df_Kampagnen = df_CampaignCheckAuswertungsSelektion.dropna(subset = ['Recognition'], inplace=True)
			#df_Kampagnen = df_ManuellImportierteDB.dropna(subset = ["Recognition"], inplace=True)
		
			#st.write("Test - CampaignCheck_df:")
			#st.dataframe(CampaignCheck_df)
			#st.write("Test - df_CampaignCheckAuswertungsSelektion:")
			#st.dataframe(df_CampaignCheckAuswertungsSelektion)
	
			#Mittelwerte der Variablen in der Gesamt-Datenbank mit allen Fällen, vor der Filtrierung  ####################################
			
			MittelwertAAA_Alle = CampaignCheck_df['Werbeerinnerung'].mean() 
			#st.write("Werbeerinnerung - Mittelwert GesamtDB: ", MittelwertAAA_Alle)
			
			MittelwertABA_Alle = CampaignCheck_df['Markenbekanntheit'].mean()
			
			#Statistiken für ABA
			#StatistikenABA_Alle = CampaignCheck_df['Markenbekanntheit'].median()
			#st.write("StatistikenABA_Alle ", StatistikenABA_Alle)
			
			
			MittelwertMarkensympathie_Alle = CampaignCheck_df['Sympathie'].mean()
			#st.write("Markensympathie - Mittelwert GesamtDB: ", MittelwertMarkensympathie_Alle)
			
			MittelwertMarkensympathie_7bis10 = CampaignCheck_df['Sympathie_7bis10'].mean()
			
			MittelwertFirstChoice_Alle = CampaignCheck_df['First Choice_codiert'].mean()
			
			MittelwertConsideration_Alle = CampaignCheck_df['Consideration'].mean()
			
			
			MittelwertKampagneSympathisch_Alle = df_KampagnenAuswahl['Werbebeurteilung - Gefällt mir'].mean()
			#st.write("MittelwertKampagneSympathisch_Alle  - Mittelwert GesamtDB: ", MittelwertKampagneSympathisch_Alle )
			
			
			MittelwertKampagneBesonders_Alle = df_KampagnenAuswahl['Werbebeurteilung - Ist etwas Besonderes'].mean()
			#st.write("MittelwertKampagneBesonders_Alle  - Mittelwert GesamtDB: ", MittelwertKampagneBesonders_Alle )
			
			MittelwertKampagneKaufreiz_Alle = df_KampagnenAuswahl['Werbebeurteilung - Reizt mich, mehr zu erfahren'].mean()
			#st.write("MittelwertKampagneKaufreiz_Alle  - Mittelwert GesamtDB: ", MittelwertKampagneKaufreiz_Alle )
			
			MittelwertKampagneVerständlich_Alle = df_KampagnenAuswahl['Werbebeurteilung - Ist verständlich'].mean()
			#st.write("MittelwertKampagneVerständlich_Alle  - Mittelwert GesamtDB: ", MittelwertKampagneVerständlich_Alle )
			
			MittelwertKampagneGlaubwürdig_Alle = df_KampagnenAuswahl['Werbebeurteilung - Ist glaubwürdig'].mean()
			#st.write("MittelwertKampagneGlaubwürdig_Alle  - Mittelwert GesamtDB: ", MittelwertKampagneGlaubwürdig_Alle )
			
			MittelwertKampagneNPS_Alle = df_KampagnenAuswahl['NPS'].mean()
			
			MittelwertKampagneRecognition_Alle = df_KampagnenAuswahl['Recognition_Wert'].mean()
			MittelwertRecognition_Alle = df_KampagnenAuswahl['Recognition_Wert'].mean()
			
			MittelwertKampagneKaufKDAOutcome_Alle = df_KampagnenAuswahl['Kauf (KDA Outcome)'].mean()
			
			MittelwertKampagneGefallen_Alle = df_KampagnenAuswahl['Werbebeurteilung - Gefällt mir'].mean()
			
			
			
			################################################################################################################################		





if datenImportAuswahl == 'Automatisch':
	#@st.cache(suppress_st_warning=True)
	@st.cache(allow_output_mutation=True) #sorgt dafür das der Datensatz nicht immer wieder neu geladen wird, allow.. unterdrückt load meldung und scheint das laden zu beschleunigen

	def load_data_automatisch():

	#Achtung: Excelfile muss komischerweise im Benutzerverzeichnis liegen
		df_datenImportExcelDatebank = pd.read_excel("CCC_GESAMTFILE_DB.xlsx",usecols='A:AR')

		_="""
		#Spaltenköpfe umtaufen
		df_datenImportExcelDatebank.rename(columns={'Firma_Kat':'Unternehmen'}, inplace=True)
		df_datenImportExcelDatebank.rename(columns={'F2_Geschlecht':'Geschlecht'}, inplace=True)
		df_datenImportExcelDatebank.rename(columns={'F10_StadtAgglo':'Wohnort'}, inplace=True)
		df_datenImportExcelDatebank.rename(columns={'F9_EINKO':'Einkommensklassen'}, inplace=True)
		#Multipliere ABA und AAA mit 100 - erleichert die Darstellung in Prozenten
		df_datenImportExcelDatebank["Werbeerinnerung"] = 100 * df_datenImportExcelDatebank["Werbeerinnerung"]
		df_datenImportExcelDatebank["Markenbekanntheit"] = 100 * df_datenImportExcelDatebank["Markenbekanntheit"]
		"""
		return df_datenImportExcelDatebank

	CampaignCheck_df = load_data_automatisch()
	DatenVorhanden = True
	df_CampaignCheckAuswertungsSelektion = CampaignCheck_df
	
	#Mittelwerte der Variablen in der Gesamt-Datenbank mit allen Fällen, vor der Filtrierung  ####################################
	
	MittelwertAAA_Alle = CampaignCheck_df['Werbeerinnerung'].mean() 
	#st.write("Werbeerinnerung - Mittelwert GesamtDB: ", MittelwertAAA_Alle)
	
	MittelwertABA_Alle = CampaignCheck_df['Markenbekanntheit'].mean()
	
	#Statistiken für ABA
	#StatistikenABA_Alle = CampaignCheck_df['Markenbekanntheit'].median()
	#st.write("StatistikenABA_Alle ", StatistikenABA_Alle)
	
	MittelwertMarkensympathie_Alle = CampaignCheck_df['Sympathie'].mean()
	#st.write("Markensympathie - Mittelwert GesamtDB: ", MittelwertMarkensympathie_Alle)
	
	MittelwertMarkensympathie_7bis10_Alle = CampaignCheck_df['Sympathie_7bis10'].mean()
	
	
	MittelwertKampagneSympathisch_Alle = CampaignCheck_df['Kampagne sympathisch (1 bis 7)'].mean()
	#st.write("MittelwertKampagneSympathisch_Alle  - Mittelwert GesamtDB: ", MittelwertKampagneSympathisch_Alle )
	
	
	MittelwertKampagneBesonders_Alle = CampaignCheck_df['Kampagne besonders (1 bis 7)'].mean()
	#st.write("MittelwertKampagneBesonders_Alle  - Mittelwert GesamtDB: ", MittelwertKampagneBesonders_Alle )
	
	MittelwertKampagneKaufreiz_Alle = CampaignCheck_df['Kampagne kaufreiz (1 bis 7)'].mean()
	#st.write("MittelwertKampagneKaufreiz_Alle  - Mittelwert GesamtDB: ", MittelwertKampagneKaufreiz_Alle )
	
	MittelwertKampagneVerständlich_Alle = CampaignCheck_df['Kampagne verständlich (1 bis 7)'].mean()
	#st.write("MittelwertKampagneVerständlich_Alle  - Mittelwert GesamtDB: ", MittelwertKampagneVerständlich_Alle )
	
	MittelwertKampagneGlaubwürdig_Alle = CampaignCheck_df['Kampagne glaubwürdig (1 bis 7)'].mean()
	#st.write("MittelwertKampagneGlaubwürdig_Alle  - Mittelwert GesamtDB: ", MittelwertKampagneGlaubwürdig_Alle )
	
	
	
	################################################################################################################################	
	





st.subheader("")








#Nur wenn Daten vorhanden >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


if DatenVorhanden == True:
	
	#gesamtTabellenExpander = st.expander('Gesamt-DB-Tabelle anzeigen')
	#with gesamtTabellenExpander:
	#	st.dataframe(CampaignCheck_df)


	
	
	#KPIAuswahl = st.sidebar.selectbox("  ",("Marken-KPIs", "Kampagnen-KPIs"))








	#st.sidebar.markdown("---")

	#Dropdowns in der linken Sidebar-Spalte  >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

	#BranchenAuswahl #####################################

	#st.sidebar.header("Branchen / Unternehmen")
	
	#Branchen die zur Auswahl stehen
	#BranchenAuswahl = CampaignCheck_df['Branche'].unique().tolist()
	#st.write("BranchenAuswahl: ", BranchenAuswahl)
	
	#BranchenAuswahl.sort()
	
	#my_BranchenSelect = st.sidebar.multiselect("Branche(n):",BranchenAuswahl)
	#st.write('You selected:', my_criteriaSelect)
	
	
	
	#df_BranchenAuswahl = CampaignCheck_df[CampaignCheck_df["Branche"].isin(my_BranchenSelect)]
	
	
	#Ausgewählte kriterien / KPI aus Multiselct in stringvariable konvertieren:
	
	#BranchenAuswahlAlsText = str(my_BranchenSelect)
	#BranchenAuswahlAlsText = BranchenAuswahlAlsText.replace("[", "")
	#BranchenAuswahlAlsText = BranchenAuswahlAlsText.replace("]", "")
	#BranchenAuswahlAlsText = BranchenAuswahlAlsText.replace("'", "")
	
	
	
	#st.write("BranchenAuswahlAlsText: ", BranchenAuswahlAlsText)
	
	
	#df_BranchenAuswahlExpander = st.expander("Dataframe - nur Zeilen mit ausgewähltem KPI(s)")
	#with df_BranchenAuswahlExpander:
	#	st.write('df_BranchenAuswahl - Dataframe - nur Zeilen mit ausgewähltem KPI:',df_BranchenAuswahl)
	
	
	
	#if my_BranchenSelect !=[]:
	#	df_CampaignCheckAuswertungsSelektion = df_BranchenAuswahl
	
	
		

	##### Option-Menu #########################################################################
	
	
	
	with st.sidebar:
		KPIAuswahl = option_menu(
			menu_title = None, #required, kann z.B "Home" stehen oder auch None
			options = ["Start/File upload","Marken-KPIs", "Kampagnen-KPIs", "Media Effects"],#required
			icons = ["file-earmark-arrow-up","vinyl","badge-ad", "volume-up"], #optional, siehe https://icons.getbootstrap.com/ !!
			menu_icon = "cast",
			default_index=0, #optional - welches ist die start-position
			#orientation = "horizontal" #optional
			
		)
		
		if KPIAuswahl == "Marken-KPIs":
			st.write(" ")
		if KPIAuswahl == "Kampagnen-KPIs":
			st.write(" ")
			df_CampaignCheckAuswertungsSelektion = df_KampagnenAuswahl
			
			
	
	st.sidebar.markdown("---")
	
	##########################################################################################




	#BrancheAuswahl ###################################################
	
	
	
	
	BranchenAuswahl = df_CampaignCheckAuswertungsSelektion['Branche'].unique().tolist()
	BranchenAuswahl.sort()
	
	if 'Branchen_options' not in st.session_state:
		st.session_state.Branchen_options = BranchenAuswahl #Alle Auswahloptionen werden am Start gezeigt
	
	if 'Branchen_default' not in st.session_state:
		st.session_state.Branchen_default = [] #hier ist die getätigte Auswahl am Start, [] weil nichts ausgewählt ist



	
	my_BrancheSelect = st.sidebar.multiselect("Branche(n):",
       options = st.session_state.Branchen_options,
       default = st.session_state.Branchen_default)
	
	
	df_BranchenAuswahl = df_CampaignCheckAuswertungsSelektion[df_CampaignCheckAuswertungsSelektion["Branche"].isin(my_BrancheSelect)]
	
	
	
	if my_BrancheSelect !=[]:
		df_CampaignCheckAuswertungsSelektion = df_BranchenAuswahl

		#Um die BrancheAuswahl aus der Multiselectbox als Text auszulesen, z.B. für Beschriftungen von Abbildungen
		BrancheAuswahlAlsText = str(my_BrancheSelect)
		BrancheAuswahlAlsText = BrancheAuswahlAlsText.replace("[", "")
		BrancheAuswahlAlsText = BrancheAuswahlAlsText.replace("]", "")
		BrancheAuswahlAlsText = BrancheAuswahlAlsText.replace("'", "")
		
		st.session_state.UG_options = df_BranchenAuswahl['Unternehmen'].unique().tolist()

	if len(my_BrancheSelect) == 1:
		#Test-Abbildung Entwicklung in der Branche im Durchschnitt
		AAA_Branche_Zeitverlauf = df_BranchenAuswahl
		AAA_Branche_Zeitverlauf_Mittelwerte = AAA_Branche_Zeitverlauf.groupby('Jahr_Monat').agg({'Werbeerinnerung':'mean'})['Werbeerinnerung']
		#st.write(AAA_Branche_Zeitverlauf_Mittelwerte)
		#Abbildung_AAA_Branche_Zeitverlauf = px.line(AAA_Branche_Zeitverlauf_Mittelwerte, x = AAA_Branche_Zeitverlauf_Mittelwerte.index, y = 'Werbeerinnerung')
		#st.plotly_chart(Abbildung_AAA_Branche_Zeitverlauf, use_container_width = True)



	#UnternehmenAuswahl ###################################################

	UnternehmenAuswahl = df_CampaignCheckAuswertungsSelektion['Unternehmen'].unique().tolist()
	UnternehmenAuswahl.sort()


	if 'UG_options' not in st.session_state:
		st.session_state.UG_options = UnternehmenAuswahl

	if 'UG_default' not in st.session_state:
		st.session_state.UG_default = [] #hier ist der Startwert, wenn nichts ausgewählt ist

	
	if my_BrancheSelect ==[]:
		st.session_state.UG_options = UnternehmenAuswahl



	#st.write("my_BrancheSelect:", my_BrancheSelect)

	
	#Wenn kein Unternehmen ausgewählt wurde, z.B. beim Starten
	#init_options = UnternehmensAuswahl

	my_UnternehmenSelect = st.sidebar.multiselect("Unternehmen zur Auswahl:",
          options=st.session_state.UG_options,
          default=st.session_state.UG_default
        )
		#my_UnternehmenSelect = st.sidebar.multiselect("Unternehmen:",UnternehmensAuswahl)
		#st.write("UG Auswahl: ", my_UnternehmenSelect)
	
	#st.write("st.session_state.options :",st.session_state.options)
	#st.write("st.session_state.default: ", st.session_state.default)
	
	#st.write("my_UnternehmenSelect: ", my_UnternehmenSelect)
	
	df_UnternehmensAuswahl = df_CampaignCheckAuswertungsSelektion[df_CampaignCheckAuswertungsSelektion['Unternehmen'].isin(my_UnternehmenSelect)]
	
	#st.write("df_UnternehmensAuswahl:", df_UnternehmensAuswahl)
	
	if my_UnternehmenSelect !=[]:
		st.session_state.UG_default = my_UnternehmenSelect
		df_CampaignCheckAuswertungsSelektion = df_UnternehmensAuswahl

		#Um die UnternehmenAuswahl aus der Multiselectbox als Text auszulesen, z.B. für Beschriftungen von Abbildungen
		UnternehmenAuswahlAlsText = str(my_UnternehmenSelect)
		UnternehmenAuswahlAlsText = UnternehmenAuswahlAlsText.replace("[", "")
		UnternehmenAuswahlAlsText = UnternehmenAuswahlAlsText.replace("]", "")
		UnternehmenAuswahlAlsText = UnternehmenAuswahlAlsText.replace("'", "")
		#st.write("Ausgewählte Unternehmen: ",UnternehmenAuswahlAlsText)
	
	
	
	
	if my_BrancheSelect ==[] and my_UnternehmenSelect ==[]:
		del st.session_state.Branchen_options #= BranchenAuswahl
		del st.session_state.Branchen_default #= []
		
		del st.session_state.UG_default #= []
		del st.session_state.UG_options #= UnternehmenAuswahl
		#st.experimental_rerun()
	
	
	
	
	
	
	
	
	
	#Zielgruppenauswahl ###################################################
	
	st.sidebar.markdown("---")
	

	
	st.sidebar.header("Zielgruppe")
	
	
	
	
	#Geschlechtsauswahl ###################################################
	
	if KPIAuswahl == "Kampagnen-KPIs":
		Geschlechtsauswahl = df_KampagnenAuswahl['Geschlecht'].unique()

	Geschlechtsauswahl = df_CampaignCheckAuswertungsSelektion['Geschlecht'].unique()
	
	my_GeschlechtSelect = st.sidebar.multiselect("Geschlecht:",Geschlechtsauswahl)
	
	df_GeschlechtsAuswahl = df_CampaignCheckAuswertungsSelektion[df_CampaignCheckAuswertungsSelektion["Geschlecht"].isin(my_GeschlechtSelect)]
	
	if my_GeschlechtSelect !=[]:
		df_CampaignCheckAuswertungsSelektion = df_GeschlechtsAuswahl
	
	
	
	
	#Altersklassenauswahl #### ###############################################
	
	st.sidebar.subheader("")
	
	Altersklasse_3KatAuswahl = df_CampaignCheckAuswertungsSelektion['Altersklasse'].unique()
	Altersklasse_3KatAuswahl.sort()
	#st.write(Altersklasse_3KatAuswahl)
	
	my_Altersklasse_3KatSelect = st.sidebar.multiselect("Altersklassen - 3 Kategorien:",Altersklasse_3KatAuswahl )
	
	df_Altersklasse_3KatAuswahl = df_CampaignCheckAuswertungsSelektion[df_CampaignCheckAuswertungsSelektion["Altersklasse"].isin(my_Altersklasse_3KatSelect)]
	
	if my_Altersklasse_3KatSelect !=[]:
		df_CampaignCheckAuswertungsSelektion = df_Altersklasse_3KatAuswahl 
	
	
	
	
	
	
	AltersklasseAuswahl = df_CampaignCheckAuswertungsSelektion['Alter'].unique()
	#AltersklasseAuswahl.sort()
	#st.write(AltersklasseAuswahl)
	
	my_AltersklasseSelect = st.sidebar.multiselect("Detaillierte Altersklasse(n):",AltersklasseAuswahl )
	
	df_AltersklasseAuswahl = df_CampaignCheckAuswertungsSelektion[df_CampaignCheckAuswertungsSelektion["Alter"].isin(my_AltersklasseSelect)]
	
	if my_AltersklasseSelect !=[]:
		df_CampaignCheckAuswertungsSelektion = df_AltersklasseAuswahl 
	
	
	
	
	
	
	#Sprachenauswahl ###################################################
	
	st.sidebar.subheader("")
	
	SpracheAuswahl = df_CampaignCheckAuswertungsSelektion['Sprache'].unique()
	
	my_SpracheSelect = st.sidebar.multiselect("Sprache(n):",SpracheAuswahl )
	
	df_SpracheAuswahl = df_CampaignCheckAuswertungsSelektion[df_CampaignCheckAuswertungsSelektion["Sprache"].isin(my_SpracheSelect)]
	
	if my_SpracheSelect !=[]:
		df_CampaignCheckAuswertungsSelektion = df_SpracheAuswahl 
	
	
	
	st.sidebar.markdown("---")
	
	
	
	#Medienauswahl ###################################################
	
	st.sidebar.subheader("")
	
	GetestetesWerbeMediumAuswahl = df_CampaignCheckAuswertungsSelektion['GetestetesWerbeMedium'].unique()
	
	my_GetestetesWerbeMediumSelect = st.sidebar.multiselect("Getestete Werbemedien",GetestetesWerbeMediumAuswahl)
	
	df_GetestetesWerbeMedium= df_CampaignCheckAuswertungsSelektion[df_CampaignCheckAuswertungsSelektion["GetestetesWerbeMedium"].isin(my_GetestetesWerbeMediumSelect)]
	
	if my_GetestetesWerbeMediumSelect !=[]:
		df_CampaignCheckAuswertungsSelektion = df_GetestetesWerbeMedium 
	

	

	#Kampagnenauswahl ###################################################
	
	st.sidebar.subheader("")
	
	GetetesteKampagneAuswahl = df_CampaignCheckAuswertungsSelektion['Kampagne'].unique()
	
	my_GetetesteKampagneSelect = st.sidebar.multiselect("Kampagnen",GetetesteKampagneAuswahl)
	
	df_GetetesteKampagneAuswahl= df_CampaignCheckAuswertungsSelektion[df_CampaignCheckAuswertungsSelektion["Kampagne"].isin(my_GetetesteKampagneSelect)]
	
	if my_GetetesteKampagneSelect !=[]:
		df_CampaignCheckAuswertungsSelektion = df_GetetesteKampagneAuswahl



	

	
	
	#Erhebungsauswahl ###################################################
	
	st.sidebar.subheader("")
	
	ErhebungsAuswahl = df_CampaignCheckAuswertungsSelektion['Erhebung'].unique()
	
	my_ErhebungsAuswahlSelect = st.sidebar.multiselect("Erhebung",ErhebungsAuswahl)
	
	df_ErhebungsAuswahl = df_CampaignCheckAuswertungsSelektion[df_CampaignCheckAuswertungsSelektion["Erhebung"].isin(my_ErhebungsAuswahlSelect)]
	
	if my_ErhebungsAuswahlSelect !=[]:
		df_CampaignCheckAuswertungsSelektion = df_ErhebungsAuswahl 	
	
	
	#Jahrauswahl ###################################################
	
	st.sidebar.subheader("")
	
	JahrAuswahl = df_CampaignCheckAuswertungsSelektion['Jahr_Gesamt'].unique()
	JahrAuswahl.sort()
	
	#Wiviele Einträge aus unterschiedliche Jahr_Monat gibt es? Diese Info brauchen wir für Zitreihen-Abbildungen
	MonatsAuswahl = df_CampaignCheckAuswertungsSelektion['Jahr_Monat'].unique()
	
	my_JahrAuswahlSelect = st.sidebar.multiselect("Jahr",JahrAuswahl)
	
	df_JahrAuswahl= df_CampaignCheckAuswertungsSelektion[df_CampaignCheckAuswertungsSelektion["Jahr_Gesamt"].isin(my_JahrAuswahlSelect)]
	
	if my_JahrAuswahlSelect !=[]:
		df_CampaignCheckAuswertungsSelektion = df_JahrAuswahl 		

	
	# Ende der Dropdowns im Sidebar<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
	
	
	#Auswahl von Diagrammfarben im Sidebar
	st.sidebar.markdown("---")
	
	farbSkalenExpander = st.sidebar.expander("Farbskala auswählen")
	with farbSkalenExpander:
	
		FARBE_MaxwertKolumne1, FARBE_MittelwertKolumne2, FARBE_MinwertKolumne3 = st.columns(3)

		with FARBE_MaxwertKolumne1:
			FARBE_Maxwert = st.color_picker("Max",FARBE_Maxwert)
		
		with FARBE_MittelwertKolumne2:
			FARBE_Mittelwert = st.color_picker("Mittel",FARBE_Mittelwert)
		
		with FARBE_MinwertKolumne3:
			FARBE_Minwert = st.color_picker("Min",FARBE_Minwert)
		
		
		FARBE_GeschlechtKolumne1, GeschlechtKolumne2 = st.columns(2)

		with FARBE_GeschlechtKolumne1:
			FARBE_Frau = st.color_picker("Frau",FARBE_Frau)
		
		with GeschlechtKolumne2:
			FARBE_Mann = st.color_picker("Mann",FARBE_Mann)
			
	
		FARBE_AlterKolumne1, FARBE_AlterKolumne2, FARBE_AlterKolumne3 = st.columns(3)

		with FARBE_AlterKolumne1:
			FARBE_16_29 = st.color_picker("16-29",FARBE_16_29)
		
		with FARBE_AlterKolumne2:
			FARBE_30_49 = st.color_picker("30-49",FARBE_30_49)
		
		with FARBE_AlterKolumne3:
			FARBE_50plust = st.color_picker("50+",FARBE_50plus)
	
	
		FARBE_SpracheKolumne1, SpracheKolumne2 = st.columns(2)

		with FARBE_SpracheKolumne1:
			FARBE_Deutsch = st.color_picker("Deutsch",FARBE_Deutsch)
		
		with SpracheKolumne2:
			FARBE_Französisch = st.color_picker("Französisch",FARBE_Französisch)
	
	
	
	

	
	##########################################################################################################
	###Marken-KPIs#############################################################################################################
	###########################################################################################################################
	
	
	
	if KPIAuswahl == "Marken-KPIs":
		placeholder.empty()
		
		
		
		# Aktuelles Auswertungsdataframe nach dem alle Auswahlmöglichkeiten in den Menüs links getätigt wurden ####
		
		CampaignCheckAuswertungsSelektionExpander = st.expander("Aktuelles Auswertungsdataframe")
		with CampaignCheckAuswertungsSelektionExpander:
			st.write("Aktuelle Auswertungsdatenbank df_CampaignCheckAuswertungsSelektion: ",df_CampaignCheckAuswertungsSelektion)
			
		MarkenTabelleExpander = st.expander("Tabelle mit durchschnittswerten pro Unternehmen")
		with MarkenTabelleExpander:	
			#Dataframe mit ausgewählten Marken-Variablen
			df_Unternehmen = df_CampaignCheckAuswertungsSelektion.groupby(['Unternehmen']).agg({'Markenbekanntheit':['mean'],'Werbeerinnerung':['mean'],'Sympathie':['mean'],'Consideration':['mean'],'First Choice_codiert':['mean']}) 
			# rename columns
			df_Unternehmen.columns = ['Markenbekanntheit - Mittelwert (%)', 'Allgemeine Werbeerinnerung - Mittelwert (%)', 'Sympathie (1-10)', 'Consideration  - Mittelwert (%)', 'First Choice  - Mittelwert (%)']
			# reset index to get grouped columns back
			df_Unternehmen = df_Unternehmen.reset_index()
			st.write(df_Unternehmen)

			speicherZeitpunkt = pd.to_datetime('today')
			st.write("")
			if len(df_Unternehmen) > 0:					
				def to_excel(df_Unternehmen):
					output = BytesIO()
					writer = pd.ExcelWriter(output, engine='xlsxwriter')
					df_Unternehmen.to_excel(writer, index=False, sheet_name='Sheet1')
					workbook = writer.book
					worksheet = writer.sheets['Sheet1']
					format1 = workbook.add_format({'num_format': '0.00'}) 
					worksheet.set_column('A:A', None, format1)  
					writer.save()
					processed_data = output.getvalue()
					return processed_data
				df_xlsx = to_excel(df_Unternehmen)
				st.download_button(label='📥 Tabelle in Excel abspeichern?',
					data=df_xlsx ,
					file_name= 'CCC_DES_Benchmarks_Markenwerte_Tabellenexport '+str(speicherZeitpunkt) +'.xlsx' )
			
			
			
			
			
			
			
	
		#Auswertungen  - Anzeige von ø Messwerte ##########################################################################
		#st.subheader("Marken-KPIs")
		#So kann man die Fonts indivudell anpassen
		st.markdown(""" <style> .font {font-size:30px ; font-family: 'Cooper Black'; color: #8CB6D8";} </style> """, unsafe_allow_html=True)
		
		st.markdown('<p class="font">Marken-KPIs</p>', unsafe_allow_html=True)
		
		
		KPIcol1, KPIcol2 = st.columns (2)
		with KPIcol1:
		
			AnzahlMesswerte = len(df_CampaignCheckAuswertungsSelektion)
			st.write("Anzahl Messwerte (Zeilen) in der Auswahl: ", AnzahlMesswerte)
			
			#Kampagnen_Tabelle = df_CampaignCheckAuswertungsSelektion.groupby('Firma_KW_Monat_Jahr').agg({'Werbeerinnerung':'mean'})['Werbeerinnerung']
			#KampagnenTabelle = df_CampaignCheckAuswertungsSelektion['Firma_KW_Monat_Jahr'].unique()
			#anzahlKampagnen = len(KampagnenTabelle)
			#st.write("Anzahl Kampagnen: ",anzahlKampagnen)
			
			UnternehmenTabelle = df_CampaignCheckAuswertungsSelektion['Unternehmen'].unique()
			anzahlUnternehmen = len(UnternehmenTabelle)
			st.write("Anzahl Unternehmen: ",anzahlUnternehmen)	
	
			BranchenTabelle = df_CampaignCheckAuswertungsSelektion['Branche'].unique()
			anzahlBranchen = len(BranchenTabelle)
			st.write("Anzahl Branchen: ",anzahlBranchen)
			
			
			#KampagnenTabelle = df_CampaignCheckAuswertungsSelektion['UG_Jahr_Monat'].unique()
			#anzahlKampagnen = len(KampagnenTabelle)
			#st.write("Anzahl Kampagnen: ",anzahlKampagnen)
			#st.write(KampagnenTabelle)
		
			BefragteTabelle = df_CampaignCheckAuswertungsSelektion['Participant_Begin'].unique()
			anzahlBefragte = len(BefragteTabelle)
			st.write("Anzahl Befragte: ",anzahlBefragte)
			#st.write(KampagnenTabelle)
		

		
		
		
		#Blaue Infofenster die anzeigen welche Branchen / Unternehmen ausgewählt wurden
		st.subheader("")

		if my_BrancheSelect !=[]:
			if len (my_BrancheSelect) == 1:
				st.info("Ausgewählte Branche: "+ BrancheAuswahlAlsText)
			else:
				st.info("Ausgewählte Branchen: "+ BrancheAuswahlAlsText)	
		
		if my_UnternehmenSelect !=[]:
			if len (my_UnternehmenSelect) == 1:
				st.info("Ausgewählte Marke: "+UnternehmenAuswahlAlsText)
			else:
				st.info("Ausgewählte Marken: "+UnternehmenAuswahlAlsText)
		
		st.subheader("ø Messwerte:")

		
		
		
		col1, col2, col3, col4, col5 = st.columns (5) 
		
		MittelwertAAA = df_CampaignCheckAuswertungsSelektion['Werbeerinnerung'].mean()
		MittelwertAAA_Gerundet = "{:.1f}".format(MittelwertAAA) #Umwandlung von Dezimal zu Prozent
		#st.write("Werbeerinnerung - Mittelwert: ", MittelwertAAA)
		MittelwertAAA_VergleichZuGesamtDB = MittelwertAAA-MittelwertAAA_Alle
		MittelwertAAA_VergleichZuGesamtDB_Gerundet = "{:.1f}".format(MittelwertAAA_VergleichZuGesamtDB) +"%"
		if MittelwertAAA_VergleichZuGesamtDB == 0.0:
			MittelwertAAA_VergleichZuGesamtDB_Gerundet = ""
			
		col3.metric("AAA - Werbeerinnerung" , value=MittelwertAAA_Gerundet +"%", delta=MittelwertAAA_VergleichZuGesamtDB_Gerundet)
		
		
		
		st.write("")
		
		MittelwertABA = df_CampaignCheckAuswertungsSelektion['Markenbekanntheit'].mean()
		MittelwertABA_Gerundet = "{:.1f}".format(MittelwertABA) #Umwandlung von Dezimal zu Prozent
		#st.write("Markenbekanntheit - Mittelwert: ", MittelwertABA)
		MittelwertABA_VergleichZuGesamtDB = MittelwertABA-MittelwertABA_Alle
		MittelwertABA_VergleichZuGesamtDB_Gerundet = "{:.1f}".format(MittelwertABA_VergleichZuGesamtDB) +"%"
		if MittelwertABA_VergleichZuGesamtDB == 0.0:
			MittelwertABA_VergleichZuGesamtDB_Gerundet = ""
		
		col1.metric("ABA - Markenbekanntheit" , value=MittelwertABA_Gerundet +"%", delta=MittelwertABA_VergleichZuGesamtDB_Gerundet)
		
		
		
		st.write("")
		MittelwertMarkensympathie_7bis10 = df_CampaignCheckAuswertungsSelektion['Sympathie_7bis10'].mean()
		MittelwertMarkensympathie_7bis10_Gerundet = "{:.1f}".format(MittelwertMarkensympathie_7bis10) #Umwandlung Dezimalstelle 
		
		MittelwertMarkensympathie = df_CampaignCheckAuswertungsSelektion['Sympathie'].mean()
		MittelwertMarkensympathie_Gerundet = "{:.1f}".format(MittelwertMarkensympathie) #Umwandlung Dezimalstelle 
		#st.write("Markenbekanntheit - Mittelwert: ", MittelwertMarkensympathie)
		MittelwertMarkensympathie_VergleichZuGesamtDB = MittelwertMarkensympathie-MittelwertMarkensympathie_Alle
		MittelwertMarkensympathie_VergleichZuGesamtDB_Gerundet = "{:.1f}".format(MittelwertMarkensympathie_VergleichZuGesamtDB)
		if MittelwertMarkensympathie_VergleichZuGesamtDB == 0.0:
			MittelwertMarkensympathie_VergleichZuGesamtDB_Gerundet = ""
		
		col2.metric("Markensympathie (1-10)" , value=MittelwertMarkensympathie_Gerundet, delta=MittelwertMarkensympathie_VergleichZuGesamtDB_Gerundet)
		
	
	
		st.write("")
		
		MittelwertFirstChoice = df_CampaignCheckAuswertungsSelektion['First Choice_codiert'].mean()
		MittelwertFirstChoice_Gerundet = "{:.1f}".format(MittelwertFirstChoice) #Umwandlung Dezimalstelle 
		#st.write("First Choice - Mittelwert: ", MittelwertFirstChoice)
		MittelwertFirstChoice_VergleichZuGesamtDB = MittelwertFirstChoice-MittelwertFirstChoice_Alle
		MittelwertFirstChoice_VergleichZuGesamtDB_Gerundet = "{:.1f}".format(MittelwertFirstChoice_VergleichZuGesamtDB) +"%"
		if MittelwertFirstChoice_VergleichZuGesamtDB == 0.0:
			MittelwertFirstChoice_VergleichZuGesamtDB_Gerundet = ""
		
		col5.metric("FirstChoice (0-100)" , value=MittelwertFirstChoice_Gerundet + "%", delta=MittelwertFirstChoice_VergleichZuGesamtDB_Gerundet)
	
	
		st.write("")
		
		MittelwertConsideration = df_CampaignCheckAuswertungsSelektion['Consideration'].mean()
		MittelwertConsideration_Gerundet = "{:.1f}".format(MittelwertConsideration) #Umwandlung Dezimalstelle 
		#st.write("First Choice - Mittelwert: ", MittelwertConsideration)
		MittelwertConsideration_VergleichZuGesamtDB = MittelwertConsideration-MittelwertConsideration_Alle
		MittelwertConsideration_VergleichZuGesamtDB_Gerundet = "{:.1f}".format(MittelwertConsideration_VergleichZuGesamtDB) +"%"
		if MittelwertConsideration_VergleichZuGesamtDB == 0.0:
			MittelwertConsideration_VergleichZuGesamtDB_Gerundet = ""
		
		col4.metric("Consideration (0-100)" , value=MittelwertConsideration_Gerundet + "%", delta=MittelwertConsideration_VergleichZuGesamtDB_Gerundet)
	
	
	
		if (MittelwertAAA_VergleichZuGesamtDB + MittelwertABA_VergleichZuGesamtDB) != 0.0:
			st.caption("Werte in Grün oder Rot hinter den Pfeilen zeigen hier die absolute Differenz zum Mittelwert in der Gesamtbefragung")
		
		
		# Abbildungen Marken KPIs#############################################################################################################################
		
		
		
		#### Abbildung **** Funnels ****** ##############################################################################3
		
		#st.write("Ausgewählte Unternehmen im Session State:")
		#st.write(st.session_state.Unternehmen)
		
		
		st.subheader("")
		st.subheader("Marken-Funnel")

		
		data = dict(
                number=[MittelwertABA, MittelwertMarkensympathie_7bis10, MittelwertAAA, MittelwertConsideration, MittelwertFirstChoice],
		       stage=["Markenbekanntheit","Sympathie (7-10)", "Allgemeine Werbeerinnerung", "Consideration","First Choice"])
		FunnelAbbildung = px.funnel(data, x='number', y='stage', text='number', hover_name ='stage' #,color='number')
			      )
		
		FunnelAbbildung.update_traces(texttemplate='%{text:.1f}'+" %", textposition='inside')
		
		st.plotly_chart(FunnelAbbildung, use_container_width = True)
		
		_="""
		data_Alle = dict(
                number_Alle =[MittelwertABA_Alle, MittelwertMarkensympathie_7bis10_Alle, MittelwertAAA_Alle, MittelwertConsideration_Alle, MittelwertFirstChoice_Alle],
		       stage=["Markenbekanntheit","Sympathie (7-10)", "Allgemeine Werbeerinnerung", "Consideration","First Choice"])
		FunnelAbbildung_Alle = px.funnel(data_Alle, x='number_Alle ', y='stage')
		st.plotly_chart(FunnelAbbildung_Alle, use_container_width = True)		
		"""
		
		
		
		
		
		# Abbildungen ########  Allgemeine, gestützte Werbeerinnerung:******************************************************************************
		
		
		#st.subheader("Allgemeine, gestützte Werbeerinnerung:")
		
		
	
	
	
		_="""
		#Abbildung - AAA je Branche ******************************************************************************************************************
		
		
		
		
		
		n_AAABranche = df_CampaignCheckAuswertungsSelektion.groupby('Branche').agg({'Werbeerinnerung':'mean'})['Werbeerinnerung']
		anzahlBrancheGesamt = len(n_AAABranche)
		
		#Branchen-durchschnitt (n_AAABranche ist eine Series!)
		#n_AAABranche_mean = n_AAABranche.mean()
		#st.write("Branchen-Durchschnitt: ",n_AAABranche_mean )
		
		if anzahlBrancheGesamt > 1:
		
			st.subheader("Allgemeine, gestützte Werbeerinnerung - nach Branchen:")
		
			st.write("Anzahl Branchen: ",anzahlBrancheGesamt)
		
			if anzahlBrancheGesamt > 10:
				minAnzahlBranche = 10
			else:
				minAnzahlBranche = anzahlBrancheGesamt
		
			if anzahlBrancheGesamt == 1:
				minAnzahlBranche = 1
		
		
			#Schalte Slider aus, macht bei max 12 Branchen wenig Sinn
			#top_AAABranche = st.slider('Wähle die Anzahl angezeigte Branchen - sortiert nach der Allgemeinen Werbeerinnerung:', min_value=0, max_value=anzahlBrancheGesamt, value=anzahlBrancheGesamt)
			#top_n_AAABranche = df_CampaignCheckAuswertungsSelektion.groupby('Branche').agg({'Werbeerinnerung':'mean'})['Werbeerinnerung'].nlargest(top_AAABranche)
			top_n_AAABranche = df_CampaignCheckAuswertungsSelektion.groupby('Branche').agg({'Werbeerinnerung':'mean'})['Werbeerinnerung'].nlargest(anzahlBrancheGesamt)
		
		
			anzahlBranche = len(top_n_AAABranche)
		
		
			Abbildung_top_n_AAABranche = px.bar(top_n_AAABranche, 
			x=top_n_AAABranche.index, 
			y='Werbeerinnerung',
			color='Werbeerinnerung',
			#color_continuous_scale=px.colors.sequential.Mint,
			#color_continuous_scale=px.colors.sequential.Viridis,
			#color_continuous_scale=px.colors.sequential.Plasma,
			#color_continuous_scale=px.colors.sequential.Hot_r,
			#color_continuous_scale=px.colors.sequential.Aggrnyl,
			#color_continuous_scale=px.colors.sequential.Blues,
			#color_continuous_scale=px.colors.sequential.Blackbody,
			#color_continuous_scale=px.colors.sequential.Brwnyl,
			text='Werbeerinnerung', #beschriftung auf Balken
			#hover_name='Werbeerinnerung', #Beschriftungstextauswahl für Balken
			title=f'AAA - Allgemeine gestützte Werbeerinnerung je Branche',
			orientation='v', #braucht es hier eigentlich nicht
			#color=top_n_AAABranche.index - unterschiedliche Farbe je Branche
			color_continuous_scale=[(0, FARBE_Minwert), (0.5, FARBE_Mittelwert), (1, FARBE_Maxwert)]
			)
			#Weitere Formatierungen der Abbildung
			#Abbildung_top_n_AAABranche.update_traces(texttemplate='%{text:.2f}', textposition='outside')
			Abbildung_top_n_AAABranche.update_traces(texttemplate='%{text:.1f}'+" %", textposition='outside')
			Abbildung_top_n_AAABranche.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
			Abbildung_top_n_AAABranche.update_yaxes(showline=True, linewidth=1, linecolor='white', gridcolor='Black')
		
		
			Abbildung_top_n_AAABranche.add_hline(y=MittelwertAAA_Alle, line_width=5, line_dash="dot", line_color="grey", opacity=0.6, annotation_text="ø Alle Messwerte", 
		              annotation_position="top left", annotation_font_size=16,
		              annotation_font_color="grey")
		
		
			st.plotly_chart(Abbildung_top_n_AAABranche, use_container_width = True)
		
		
		"""
		

		
		#Abbildung - AAA je Unternehmung ******************************************************************************************************************
		
		n_AAAUnternehmen = df_CampaignCheckAuswertungsSelektion.groupby('Unternehmen').agg({'Werbeerinnerung':'mean'})['Werbeerinnerung']
		

		
		
		
		
		
		
		anzahlUnternehmenGesamt = len(n_AAAUnternehmen)
		
		if anzahlUnternehmenGesamt > 1:
		
			st.subheader("Allgemeine, gestützte Werbeerinnerung - nach Unternehmen:")
		
			st.write("Anzahl Unternehmen zur Auswahl: ",anzahlUnternehmenGesamt)
		
			if anzahlUnternehmenGesamt > 10:
				minAnzahlUnternehmen = 10
			else:
				minAnzahlUnternehmen = anzahlUnternehmenGesamt
		
			if anzahlUnternehmenGesamt == 1:
				minAnzahlUnternehmen = 1
		
			top_AAAUnternehmen = st.slider('Wähle die Anzahl Unternehmen die angezeigt werden sollen:', min_value=0, max_value=anzahlUnternehmenGesamt, value=minAnzahlUnternehmen)
			top_n_AAAUnternehmen = df_CampaignCheckAuswertungsSelektion.groupby('Unternehmen').agg({'Werbeerinnerung':'mean'})['Werbeerinnerung'].nlargest(top_AAAUnternehmen)
		
			anzahlUnternehmen = len(top_n_AAAUnternehmen)
		
			Abbildung_top_n_AAAUnternehmen = px.bar(top_n_AAAUnternehmen, 
			x=top_n_AAAUnternehmen.index, 
			y='Werbeerinnerung',
			color='Werbeerinnerung',
			#color_continuous_scale=px.colors.sequential.Blackbody,
			#color_continuous_scale=px.colors.sequential.Brwnyl,
			#color=top_n_AAAUnternehmen.index - unterschiedliche Farbe je Unternehmen
			text='Werbeerinnerung', #beschriftung auf Balken
			#hover_name='Werbeerinnerung', #Beschriftungstextauswahl für Balken
			title=f'AAA - Allgemeine gestützte Werbeerinnerung je Unternehmen - Top ' + str(top_AAAUnternehmen),
			orientation='v', #braucht es hier eigentlich nicht
			#color_continuous_scale=[(0, FARBE_Minwert),(0.25, FARBE_Mittelwert), (0.5, FARBE_Mittelwert), (0.75, FARBE_Maxwert),(1, FARBE_Maxwert)]
			color_continuous_scale=[(0, FARBE_Minwert), (0.5, FARBE_Mittelwert), (1, FARBE_Maxwert)]
			#color_continuous_scale[color_continuous_scale[0]] = "black"
			
			)
			#Weitere Formatierungen der Abbildung
			Abbildung_top_n_AAAUnternehmen.update_traces(texttemplate='%{text:.1f}'+" %", textposition='inside')
			Abbildung_top_n_AAAUnternehmen.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
			Abbildung_top_n_AAAUnternehmen.update_yaxes(showline=True, linewidth=1, linecolor='white', gridcolor='black')
			

			
			#Horizontale Line mit Durchschnitt aller Messerwerte aus der DB
			Abbildung_top_n_AAAUnternehmen.add_hline(y=MittelwertAAA_Alle, line_width=5, line_dash="dot", line_color="grey", opacity=0.6, annotation_text="ø Alle Messwerte", 
		              annotation_position="top left", annotation_font_size=16,
		              annotation_font_color="grey")
		
			if MittelwertAAA_Alle != MittelwertAAA:
				Abbildung_top_n_AAAUnternehmen.add_hline(y=MittelwertAAA, line_width=2, line_dash="dot", line_color="white", opacity=0.8, annotation_text="ø Auswahl", 
		              annotation_position="top right")
		
		
			st.plotly_chart(Abbildung_top_n_AAAUnternehmen, use_container_width = True)
		
		

			_=""" Beispiel mit einem eingefärbten Balken
			data = {'Name':['2020/01', '2020/02', '2020/03', '2020/04',  
'2020/05', '2020/07', '2020/08'],  
        'Value':[34,56,66,78,99,55,22]}
			df = pd.DataFrame(data)
			df['category'] = [str(i) for i in df.index]
	

			color_discrete_sequence = ['#ec7c34']*len(df)
			color_discrete_sequence[5] = '#609cd4'
			fig=px.bar(df,x='Name',y='Value',
           color = 'category',
           color_discrete_sequence=color_discrete_sequence,
           )
			st.plotly_chart(fig)
			"""
	
		#AAA -  Abbildungen mit Splits nach Geschlecht - wenn nur eine Unternehmung gewählt ist #######################
		if anzahlUnternehmenGesamt == 1:
			st.subheader("Allgemeine Werbeerinnerung - " + UnternehmenAuswahlAlsText)
		
			AAA_AbbildungenMitBreakKolumne1, AAA_AbbildungenMitBreakKolumne2, AAA_AbbildungenMitBreakKolumne3 = st.columns(3)
	
			with AAA_AbbildungenMitBreakKolumne1:
				#Abbildung AAA - nach Geschlecht ***
				AAAUnternehmen_Geschlecht = df_CampaignCheckAuswertungsSelektion.groupby('Geschlecht').agg({'Werbeerinnerung':'mean'})['Werbeerinnerung']
			
				Abbildung_AAAUnternehmen_Geschlecht = px.bar(AAAUnternehmen_Geschlecht, 
				x=AAAUnternehmen_Geschlecht.index, #in der Indexspalte steht das Geschlecht in den Zeilen
				y='Werbeerinnerung',
				color=AAAUnternehmen_Geschlecht.index,
				color_discrete_map={'Frau' : FARBE_Frau ,'Mann' : FARBE_Mann},
				text='Werbeerinnerung', #beschriftung auf Balken
				#hover_name='Werbeerinnerung', #Beschriftungstextauswahl für Balken
				title=f'AAA - ' + UnternehmenAuswahlAlsText + " - nach Geschlecht"
				)
				
				#Weitere Formatierungen der Abbildung
				Abbildung_AAAUnternehmen_Geschlecht.update_traces(texttemplate='%{text:.1f}'+" %", textposition='outside')
				Abbildung_AAAUnternehmen_Geschlecht.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
				Abbildung_AAAUnternehmen_Geschlecht.update_yaxes(showline=True, linewidth=1, linecolor='white', gridcolor='black')
				Abbildung_AAAUnternehmen_Geschlecht.update_layout(showlegend=False)
				
				st.plotly_chart(Abbildung_AAAUnternehmen_Geschlecht, use_container_width = True)
				#st.plotly_chart(Abbildung_AAAUnternehmen_Geschlecht, width=300)
			
			with AAA_AbbildungenMitBreakKolumne2:
				#Abbildung AAA - nach Alter ***
				AAAUnternehmen_Alter = df_CampaignCheckAuswertungsSelektion.groupby('Alter').agg({'Werbeerinnerung':'mean'})['Werbeerinnerung']
			
				Abbildung_AAAUnternehmen_Alter = px.bar(AAAUnternehmen_Alter, 
				x=AAAUnternehmen_Alter.index, #in der Indexspalte steht das Alter in den Zeilen
				y='Werbeerinnerung',
				color=AAAUnternehmen_Alter.index,
				color_discrete_map={'16-19' : FARBE_16_29 ,'20-24' : FARBE_16_29 ,'25-29' : FARBE_16_29 ,'30-34' : FARBE_30_49,'35-39' : FARBE_30_49,'40-44' : FARBE_30_49,'45-49' : FARBE_30_49,'50-54' : FARBE_50plus,'55-59' : FARBE_50plus,'60+' : FARBE_50plus},
				text='Werbeerinnerung', #beschriftung auf Balken
				#hover_name='Werbeerinnerung', #Beschriftungstextauswahl für Balken
				title=f'AAA - ' + UnternehmenAuswahlAlsText + " - nach Alter"
				)
				
				#Weitere Formatierungen der Abbildung
				Abbildung_AAAUnternehmen_Alter.update_traces(texttemplate='%{text:.1f}'+" %", textposition='outside')
				Abbildung_AAAUnternehmen_Alter.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
				Abbildung_AAAUnternehmen_Alter.update_yaxes(showline=True, linewidth=1, linecolor='white', gridcolor='black')
				Abbildung_AAAUnternehmen_Alter.update_layout(showlegend=False)
				
				st.plotly_chart(Abbildung_AAAUnternehmen_Alter, use_container_width = True)
				#st.plotly_chart(Abbildung_AAAUnternehmen_Alter, width=500)
				
			with AAA_AbbildungenMitBreakKolumne3:	
				#Abbildung AAA - nach Sprache ***
				AAAUnternehmen_Sprache = df_CampaignCheckAuswertungsSelektion.groupby('Sprache').agg({'Werbeerinnerung':'mean'})['Werbeerinnerung']
			
				Abbildung_AAAUnternehmen_Sprache = px.bar(AAAUnternehmen_Sprache, 
				x=AAAUnternehmen_Sprache.index, #in der Indexspalte steht das Sprache in den Zeilen
				y='Werbeerinnerung',
				color=AAAUnternehmen_Sprache.index,
				color_discrete_map={'Deutsch' : FARBE_Deutsch ,'Französisch' : FARBE_Französisch},
				text='Werbeerinnerung', #beschriftung auf Balken
				#hover_name='Werbeerinnerung', #Beschriftungstextauswahl für Balken
				title=f'AAA - ' + UnternehmenAuswahlAlsText  +" - nach Sprache"
				)
				
				#Weitere Formatierungen der Abbildung
				Abbildung_AAAUnternehmen_Sprache.update_traces(texttemplate='%{text:.1f}'+" %", textposition='outside')
				Abbildung_AAAUnternehmen_Sprache.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
				Abbildung_AAAUnternehmen_Sprache.update_yaxes(showline=True, linewidth=1, linecolor='white', gridcolor='black')
				Abbildung_AAAUnternehmen_Sprache.update_layout(showlegend=False)
				
				st.plotly_chart(Abbildung_AAAUnternehmen_Sprache, use_container_width = True)
				#st.plotly_chart(Abbildung_AAAUnternehmen_Sprache, width=300)
		
			if len(JahrAuswahl) > 1:
				#Abbildung AAA - nach Jahr_Gesamt ***
				AAAUnternehmen_Jahr_Gesamt = df_CampaignCheckAuswertungsSelektion.groupby('Jahr_Gesamt').agg({'Werbeerinnerung':'mean'})['Werbeerinnerung']
				
				Abbildung_AAAUnternehmen_Jahr_Gesamt = px.bar(AAAUnternehmen_Jahr_Gesamt, 
				x=AAAUnternehmen_Jahr_Gesamt.index, #in der Indexspalte steht das Jahr_Gesamt in den Zeilen
				y='Werbeerinnerung',
				color=AAAUnternehmen_Jahr_Gesamt.index,
				text='Werbeerinnerung', #beschriftung auf Balken
				#hover_name='Markenbekanntheit', #Beschriftungstextauswahl für Balken
				title=f'AAA - ' + UnternehmenAuswahlAlsText + " - im Zeitverlauf"
				)
				
				#Weitere Formatierungen der Abbildung
				Abbildung_AAAUnternehmen_Jahr_Gesamt.update_traces(texttemplate='%{text:.1f}'+" %", textposition='inside')
				Abbildung_AAAUnternehmen_Jahr_Gesamt.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
				Abbildung_AAAUnternehmen_Jahr_Gesamt.update_yaxes(showline=True, linewidth=1, linecolor='white', gridcolor='black')
				Abbildung_AAAUnternehmen_Jahr_Gesamt.update_layout(showlegend=False)
				
				st.plotly_chart(Abbildung_AAAUnternehmen_Jahr_Gesamt, use_container_width = True)
				#st.plotly_chart(Abbildung_AAAUnternehmen_Jahr_Gesamt, width=300)
	
			if len(MonatsAuswahl) > 1:
				#Linienchart Abbildung AAA - nach Jahr_Monat ***
				AAAUnternehmen_Jahr_Monat = df_CampaignCheckAuswertungsSelektion.groupby('Jahr_Monat').agg({'Werbeerinnerung':'mean'})['Werbeerinnerung']
				
				Abbildung_AAAUnternehmen_Jahr_Monat = px.line(AAAUnternehmen_Jahr_Monat, 
				x=AAAUnternehmen_Jahr_Monat.index, #in der Indexspalte steht das Jahr_Monat in den Zeilen
				y='Werbeerinnerung',
				#color=AAAUnternehmen_Jahr_Monat.index,
				text='Werbeerinnerung', #beschriftung auf Balken
				#hover_name='Markenbekanntheit', #Beschriftungstextauswahl für Balken
				title=f'AAA - ' + UnternehmenAuswahlAlsText + " - im Zeitverlauf"
				)
				
				#Weitere Formatierungen der Abbildung
				Abbildung_AAAUnternehmen_Jahr_Monat.update_yaxes(range=[0, 100])
				Abbildung_AAAUnternehmen_Jahr_Monat.update_traces(texttemplate='%{text:.1f}'+" %")
				Abbildung_AAAUnternehmen_Jahr_Monat.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
				#Abbildung_AAAUnternehmen_Jahr_Monat.update_yaxes(showline=True, linewidth=0.2, linecolor='black', gridcolor='black')
				
				Abbildung_AAAUnternehmen_Jahr_Monat.update_xaxes(showline=True, linewidth=1, linecolor='black', gridcolor='Black')
				Abbildung_AAAUnternehmen_Jahr_Monat.update_yaxes(showline=True, linewidth=2, linecolor='black', gridcolor='Black')
				Abbildung_AAAUnternehmen_Jahr_Monat.update_layout(xaxis=dict(showticklabels=True,linewidth=1))
				#Abbildung_AAAUnternehmen_Jahr_Monat.update_layout(showlegend=False)
				Abbildung_AAAUnternehmen_Jahr_Monat.update_xaxes(title_text='Jahr - Monat')
				st.plotly_chart(Abbildung_AAAUnternehmen_Jahr_Monat, use_container_width = True)	
		
				
				#Test-Abbildung Entwicklung in der Branche im Durchschnitt
				Abbildung_AAA_Branche_ZeitverlaufExpander = st.expander("Entwicklung in der Branche")
				with Abbildung_AAA_Branche_ZeitverlaufExpander: 
					Abbildung_AAA_Branche_Zeitverlauf = px.line(AAA_Branche_Zeitverlauf_Mittelwerte, 
					x = AAA_Branche_Zeitverlauf_Mittelwerte.index, 
					y = 'Werbeerinnerung',
					#color ='Unternehmen',
					text='Werbeerinnerung',
					color_discrete_sequence = ['orange'],
					title=f'AAA - ' + BrancheAuswahlAlsText + " - im Zeitverlauf")
					Abbildung_AAA_Branche_Zeitverlauf.update_yaxes(range=[0, 100])
					Abbildung_AAA_Branche_Zeitverlauf.update_traces(texttemplate='%{text:.1f}'+" %")
					Abbildung_AAA_Branche_Zeitverlauf.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
					#Abbildung_AAAUnternehmen_Jahr_Monat.update_yaxes(showline=True, linewidth=0.2, linecolor='black', gridcolor='black')
					
					Abbildung_AAA_Branche_Zeitverlauf.update_xaxes(showline=True, linewidth=1, linecolor='black', gridcolor='Black')
					Abbildung_AAA_Branche_Zeitverlauf.update_yaxes(showline=True, linewidth=2, linecolor='black', gridcolor='Black')
					Abbildung_AAA_Branche_Zeitverlauf.update_layout(xaxis=dict(showticklabels=True,linewidth=1))
					#Abbildung_AAAUnternehmen_Jahr_Monat.update_layout(showlegend=False)
					Abbildung_AAA_Branche_Zeitverlauf.update_xaxes(title_text='Jahr - Monat')
	
					st.plotly_chart(Abbildung_AAA_Branche_Zeitverlauf, use_container_width = True)
				
		_="""
		#Abbildung - ABA je Branche ******************************************************************************************************************
		
		
		
		
		
		n_ABABranche = df_CampaignCheckAuswertungsSelektion.groupby('Branche').agg({'Markenbekanntheit':'mean'})['Markenbekanntheit']
		anzahlBrancheGesamt = len(n_ABABranche)
		
		if anzahlBrancheGesamt > 1:
		
			st.subheader("Gestützte Markenbekanntheit - nach Branchen:")
		
			st.write("Anzahl Branchen: ",anzahlBrancheGesamt)
		
			if anzahlBrancheGesamt > 10:
				minAnzahlBranche = 10
			else:
				minAnzahlBranche = anzahlBrancheGesamt
		
			if anzahlBrancheGesamt == 1:
				minAnzahlBranche = 1
		
		
			#Schalte Slider aus, macht bei max 12 Branchen wenig Sinn
			#top_ABABranche = st.slider('Wähle die Anzahl angezeigte Branchen - sortiert nach der Allgemeinen Werbeerinnerung:', min_value=0, max_value=anzahlBrancheGesamt, value=anzahlBrancheGesamt)
			#top_n_ABABranche = df_CampaignCheckAuswertungsSelektion.groupby('Branche').agg({'Markenbekanntheit':'mean'})['Markenbekanntheit'].nlargest(top_ABABranche)
			top_n_ABABranche = df_CampaignCheckAuswertungsSelektion.groupby('Branche').agg({'Markenbekanntheit':'mean'})['Markenbekanntheit'].nlargest(anzahlBrancheGesamt)
		
		
			anzahlBranche = len(top_n_ABABranche)
		
			Abbildung_top_n_ABABranche = px.bar(top_n_ABABranche, 
			x=top_n_ABABranche.index, 
			y='Markenbekanntheit',
			color='Markenbekanntheit',
			text='Markenbekanntheit', #beschriftung auf Balken
			#hover_name='Markenbekanntheit', #Beschriftungstextauswahl für Balken
			title=f'ABA - Allgemeine gestützte Markenbekanntheit je Branche',
			orientation='v', #braucht es hier eigentlich nicht
			#color=top_n_ABABranche.index - unterschiedliche Farbe je Branche
			color_continuous_scale=[(0, FARBE_Minwert), (0.5, FARBE_Mittelwert), (1, FARBE_Maxwert)]
			)
			#Weitere Formatierungen der Abbildung
			#Abbildung_top_n_ABABranche.update_traces(texttemplate='%{text:.2f}', textposition='outside')
			Abbildung_top_n_ABABranche.update_traces(texttemplate='%{text:.1f}'+" %", textposition='inside')
			Abbildung_top_n_ABABranche.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
			Abbildung_top_n_ABABranche.update_yaxes(showline=True, linewidth=1, linecolor='white', gridcolor='Black')
			#Horizontale Line mit Durchschnitt aller Messerwerte aus der DB
			Abbildung_top_n_ABABranche.add_hline(y=MittelwertABA_Alle, line_width=5, line_dash="dot", line_color="grey", opacity=0.6, annotation_text="ø Alle Messwerte", 
		              annotation_position="top left", annotation_font_size=16,
		              annotation_font_color="grey")
		
			st.plotly_chart(Abbildung_top_n_ABABranche, use_container_width = True)
		
		"""
		
		
		
		#Abbildung - ABA je Unternehmung ******************************************************************************************************************
		
		n_ABAUnternehmen = df_CampaignCheckAuswertungsSelektion.groupby('Unternehmen').agg({'Markenbekanntheit':'mean'})['Markenbekanntheit']
		anzahlUnternehmenGesamt = len(n_ABAUnternehmen)
		
		if anzahlUnternehmenGesamt > 1:
			
		
			st.subheader("Gestützte Markenbekanntheit - nach Unternehmen:")
		
			st.write("Anzahl Unternehmen zur Auswahl: ",anzahlUnternehmenGesamt)
		
			if anzahlUnternehmenGesamt > 10:
				minAnzahlUnternehmen = 10
			else:
				minAnzahlUnternehmen = anzahlUnternehmenGesamt
		
			if anzahlUnternehmenGesamt == 1:
				minAnzahlUnternehmen = 1
		
			top_ABAUnternehmen = st.slider('Wähle die Anzahl Unternehmen die angezeigt werden sollen:', min_value=0, max_value=anzahlUnternehmenGesamt, value=minAnzahlUnternehmen, key="ABA_UGSlider")
			top_n_ABAUnternehmen = df_CampaignCheckAuswertungsSelektion.groupby('Unternehmen').agg({'Markenbekanntheit':'mean'})['Markenbekanntheit'].nlargest(top_ABAUnternehmen)
		
			anzahlUnternehmen = len(top_n_ABAUnternehmen)
		
			Abbildung_top_n_ABAUnternehmen = px.bar(top_n_ABAUnternehmen, 
			x=top_n_ABAUnternehmen.index, 
			y='Markenbekanntheit',
			color='Markenbekanntheit',
			#color=top_n_ABAUnternehmen.index - unterschiedliche Farbe je Unternehmen
			text='Markenbekanntheit', #beschriftung auf Balken
			#hover_name='Markenbekanntheit', #Beschriftungstextauswahl für Balken
			title=f'ABA - Gestützte Markenbekanntheit je Unternehmen - Top ' + str(top_ABAUnternehmen),
			orientation='v', #braucht es hier eigentlich nicht
			color_continuous_scale=[(0, FARBE_Minwert), (0.5, FARBE_Mittelwert), (1, FARBE_Maxwert)]
			)
			#Weitere Formatierungen der Abbildung
			Abbildung_top_n_ABAUnternehmen.update_traces(texttemplate='%{text:.1f}'+" %", textposition='inside')
			Abbildung_top_n_ABAUnternehmen.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
			Abbildung_top_n_ABAUnternehmen.update_yaxes(showline=True, linewidth=1, linecolor='white', gridcolor='Black')
		
			#Horizontale Line mit Durchschnitt aller Messerwerte aus der DB
			Abbildung_top_n_ABAUnternehmen.add_hline(y=MittelwertABA_Alle, line_width=5, line_dash="dot", line_color="grey", opacity=0.6, annotation_text="ø Alle Messwerte", 
		              annotation_position="top left", annotation_font_size=16,
		              annotation_font_color="grey")
		
			if MittelwertABA_Alle != MittelwertABA:
				Abbildung_top_n_ABAUnternehmen.add_hline(y=MittelwertABA, line_width=2, line_dash="dot", line_color="white", opacity=0.8, annotation_text="ø Auswahl", 
		              annotation_position="top right")
		
		
			st.plotly_chart(Abbildung_top_n_ABAUnternehmen, use_container_width = True)
		
		
		#ABA -  Abbildungen mit Splits nach Geschlecht - wenn nur eine Unternehmung gewählt ist #######################

		if anzahlUnternehmenGesamt == 1:
			st.subheader("Gestützte Markenbekanntheit - " + UnternehmenAuswahlAlsText)
		
			_="""
			#Idee - Zeilennummer von ausgewähltes Unternehmen finden, um dann dieses in der Abbildung zu"Highlighten" mit einer Textbox
			n_AAAUnternehmen = n_AAAUnternehmen.reset_index(drop=False)
			n_AAAUnternehmen.sort_values(by=['Werbeerinnerung'], inplace=True, ascending=False)
			n_AAAUnternehmen = n_AAAUnternehmen.reset_index(drop=False)
			st.write("n_AAAUnternehmen: ", n_AAAUnternehmen)
			row_number = n_AAAUnternehmen[n_AAAUnternehmen['Unternehmen'] == 'Aldi'].index[0]
			st.write("row_number", row_number)
		
			#Textbox um ausgewähltes Unternehmen in der Abbildung zu "highlighten"
			Abbildung_top_n_AAAUnternehmen.update_layout(
			#einzelnen Punkt mit einer Box hervorheben
			annotations= [
			{"x": 2, "y":50,
			"text":"Test-Text"}
			])
			Abbildung_top_n_AAAUnternehmen.update_annotations(arrowcolor="white")
			Abbildung_top_n_AAAUnternehmen.update_annotations(arrowhead=1)
			Abbildung_top_n_AAAUnternehmen.update_annotations(bordercolor="white")
			Abbildung_top_n_AAAUnternehmen.update_annotations(yanchor="middle")
		
			"""
		
		
			ABA_AbbildungenMitBreakKolumne1, ABA_AbbildungenMitBreakKolumne2, ABA_AbbildungenMitBreakKolumne3 = st.columns(3)
	
			with ABA_AbbildungenMitBreakKolumne1:
				#Abbildung ABA - nach Geschlecht ***
				ABAUnternehmen_Geschlecht = df_CampaignCheckAuswertungsSelektion.groupby('Geschlecht').agg({'Markenbekanntheit':'mean'})['Markenbekanntheit']
			
				Abbildung_ABAUnternehmen_Geschlecht = px.bar(ABAUnternehmen_Geschlecht, 
				x=ABAUnternehmen_Geschlecht.index, #in der Indexspalte steht das Geschlecht in den Zeilen
				y='Markenbekanntheit',
				color=ABAUnternehmen_Geschlecht.index,
				color_discrete_map={'Frau' : FARBE_Frau ,'Mann' : FARBE_Mann},
				text='Markenbekanntheit', #beschriftung auf Balken
				#hover_name='Markenbekanntheit', #Beschriftungstextauswahl für Balken
				title=f'ABA - ' + UnternehmenAuswahlAlsText + " - nach Geschlecht"
				)
				
				#Weitere Formatierungen der Abbildung
				Abbildung_ABAUnternehmen_Geschlecht.update_traces(texttemplate='%{text:.1f}'+" %", textposition='inside')
				Abbildung_ABAUnternehmen_Geschlecht.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
				Abbildung_ABAUnternehmen_Geschlecht.update_yaxes(showline=True, linewidth=1, linecolor='white', gridcolor='black')
				Abbildung_ABAUnternehmen_Geschlecht.update_layout(showlegend=False)
				
				st.plotly_chart(Abbildung_ABAUnternehmen_Geschlecht, use_container_width = True)
				#st.plotly_chart(Abbildung_ABAUnternehmen_Geschlecht, width=300)
			
			with ABA_AbbildungenMitBreakKolumne2:
				#Abbildung ABA - nach Alter ***
				ABAUnternehmen_Alter = df_CampaignCheckAuswertungsSelektion.groupby('Alter').agg({'Markenbekanntheit':'mean'})['Markenbekanntheit']
			
				Abbildung_ABAUnternehmen_Alter = px.bar(ABAUnternehmen_Alter, 
				x=ABAUnternehmen_Alter.index, #in der Indexspalte steht das Alter in den Zeilen
				y='Markenbekanntheit',
				color=ABAUnternehmen_Alter.index,
				color_discrete_map={'16-19' : FARBE_16_29 ,'20-24' : FARBE_16_29 ,'25-29' : FARBE_16_29 ,'30-34' : FARBE_30_49,'35-39' : FARBE_30_49,'40-44' : FARBE_30_49,'45-49' : FARBE_30_49,'50-54' : FARBE_50plus,'55-59' : FARBE_50plus,'60+' : FARBE_50plus},
				text='Markenbekanntheit', #beschriftung auf Balken
				#hover_name='Markenbekanntheit', #Beschriftungstextauswahl für Balken
				title=f'ABA - ' + UnternehmenAuswahlAlsText +" - nach Alter"
				)
				
				#Weitere Formatierungen der Abbildung
				Abbildung_ABAUnternehmen_Alter.update_traces(texttemplate='%{text:.1f}'+" %", textposition='inside')
				Abbildung_ABAUnternehmen_Alter.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
				Abbildung_ABAUnternehmen_Alter.update_yaxes(showline=True, linewidth=1, linecolor='white', gridcolor='black')
				Abbildung_ABAUnternehmen_Alter.update_layout(showlegend=False)
				
				st.plotly_chart(Abbildung_ABAUnternehmen_Alter, use_container_width = True)
				#st.plotly_chart(Abbildung_ABAUnternehmen_Alter, width=500)
				
			with ABA_AbbildungenMitBreakKolumne3:	
				#Abbildung ABA - nach Sprache ***
				ABAUnternehmen_Sprache = df_CampaignCheckAuswertungsSelektion.groupby('Sprache').agg({'Markenbekanntheit':'mean'})['Markenbekanntheit']
			
				Abbildung_ABAUnternehmen_Sprache = px.bar(ABAUnternehmen_Sprache, 
				x=ABAUnternehmen_Sprache.index, #in der Indexspalte steht das Sprache in den Zeilen
				y='Markenbekanntheit',
				color=ABAUnternehmen_Sprache.index,
				color_discrete_map={'Deutsch' : FARBE_Deutsch ,'Französisch' : FARBE_Französisch},
				text='Markenbekanntheit', #beschriftung auf Balken
				#hover_name='Markenbekanntheit', #Beschriftungstextauswahl für Balken
				title=f'ABA - ' + UnternehmenAuswahlAlsText +" - nach Sprache"
				)
				
				#Weitere Formatierungen der Abbildung
				Abbildung_ABAUnternehmen_Sprache.update_traces(texttemplate='%{text:.1f}'+" %", textposition='inside')
				Abbildung_ABAUnternehmen_Sprache.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
				Abbildung_ABAUnternehmen_Sprache.update_yaxes(showline=True, linewidth=1, linecolor='white', gridcolor='black')
				Abbildung_ABAUnternehmen_Sprache.update_layout(showlegend=False)
				
				st.plotly_chart(Abbildung_ABAUnternehmen_Sprache, use_container_width = True)
				#st.plotly_chart(Abbildung_ABAUnternehmen_Sprache, width=300)
				
			if len(JahrAuswahl) > 1:
				#Abbildung ABA - nach Jahr_Gesamt ***
				ABAUnternehmen_Jahr_Gesamt = df_CampaignCheckAuswertungsSelektion.groupby('Jahr_Gesamt').agg({'Markenbekanntheit':'mean'})['Markenbekanntheit']
				
				Abbildung_ABAUnternehmen_Jahr_Gesamt = px.bar(ABAUnternehmen_Jahr_Gesamt, 
				x=ABAUnternehmen_Jahr_Gesamt.index, #in der Indexspalte steht das Jahr_Gesamt in den Zeilen
				y='Markenbekanntheit',
				color=ABAUnternehmen_Jahr_Gesamt.index,
				text='Markenbekanntheit', #beschriftung auf Balken
				#hover_name='Markenbekanntheit', #Beschriftungstextauswahl für Balken
				title=f'ABA - ' + UnternehmenAuswahlAlsText + " - im Zeitverlauf"
				)
				
				#Weitere Formatierungen der Abbildung
				Abbildung_ABAUnternehmen_Jahr_Gesamt.update_traces(texttemplate='%{text:.1f}'+" %", textposition='inside')
				Abbildung_ABAUnternehmen_Jahr_Gesamt.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
				Abbildung_ABAUnternehmen_Jahr_Gesamt.update_yaxes(showline=True, linewidth=1, linecolor='white', gridcolor='black')
				Abbildung_ABAUnternehmen_Jahr_Gesamt.update_layout(showlegend=False)
				
				st.plotly_chart(Abbildung_ABAUnternehmen_Jahr_Gesamt, use_container_width = True)
				#st.plotly_chart(Abbildung_ABAUnternehmen_Jahr_Gesamt, width=300)
	
			if len(MonatsAuswahl) > 1:
				#Abbildung ABA - nach Jahr_Monat ***
				ABAUnternehmen_Jahr_Monat = df_CampaignCheckAuswertungsSelektion.groupby('Jahr_Monat').agg({'Markenbekanntheit':'mean'})['Markenbekanntheit']
				
				Abbildung_ABAUnternehmen_Jahr_Monat = px.line(ABAUnternehmen_Jahr_Monat, 
				x=ABAUnternehmen_Jahr_Monat.index, #in der Indexspalte steht das Jahr_Monat in den Zeilen
				y='Markenbekanntheit',
				#color=ABAUnternehmen_Jahr_Monat.index,
				text='Markenbekanntheit', #beschriftung auf Balken
				#hover_name='Markenbekanntheit', #Beschriftungstextauswahl für Balken
				title=f'ABA - ' + UnternehmenAuswahlAlsText + " - im Zeitverlauf"
				)
				
				#Weitere Formatierungen der Abbildung
				Abbildung_ABAUnternehmen_Jahr_Monat.update_yaxes(range=[0, 100])
				Abbildung_ABAUnternehmen_Jahr_Monat.update_traces(texttemplate='%{text:.1f}'+" %")
				Abbildung_ABAUnternehmen_Jahr_Monat.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
				#Abbildung_ABAUnternehmen_Jahr_Monat.update_yaxes(showline=True, linewidth=0.2, linecolor='black', gridcolor='black')
				
				Abbildung_ABAUnternehmen_Jahr_Monat.update_xaxes(showline=True, linewidth=1, linecolor='black', gridcolor='Black')
				Abbildung_ABAUnternehmen_Jahr_Monat.update_yaxes(showline=True, linewidth=2, linecolor='black', gridcolor='Black')
				Abbildung_ABAUnternehmen_Jahr_Monat.update_layout(xaxis=dict(showticklabels=True,linewidth=1))
				#Abbildung_ABAUnternehmen_Jahr_Monat.update_layout(showlegend=False)
				Abbildung_ABAUnternehmen_Jahr_Monat.update_xaxes(title_text='Jahr - Monat')
				st.plotly_chart(Abbildung_ABAUnternehmen_Jahr_Monat, use_container_width = True)
	
		
		
		
		
		
		
		
		
		
		
		
		_="""
		#Abbildung - MarkenSympathie je Branche ******************************************************************************************************************
		
		
		
		
		
		n_MarkenSympathieBranche = df_CampaignCheckAuswertungsSelektion.groupby('Branche').agg({'Sympathie':'mean'})['Sympathie']
		anzahlBrancheGesamt = len(n_MarkenSympathieBranche)
		
		if anzahlBrancheGesamt > 1:
		
			st.subheader("Sympathie - nach Branchen:")
		
			st.write("Anzahl Branchen: ",anzahlBrancheGesamt)
		
			if anzahlBrancheGesamt > 10:
				minAnzahlBranche = 10
			else:
				minAnzahlBranche = anzahlBrancheGesamt
		
			if anzahlBrancheGesamt == 1:
				minAnzahlBranche = 1
		
		
			#Schalte Slider aus, macht bei max 12 Branchen wenig Sinn
			#top_MarkenSympathieBranche = st.slider('Wähle die Anzahl angezeigte Branchen - sortiert nach der Allgemeinen Werbeerinnerung:', min_value=0, max_value=anzahlBrancheGesamt, value=anzahlBrancheGesamt)
			#top_n_MarkenSympathieBranche = df_CampaignCheckAuswertungsSelektion.groupby('Branche').agg({'Sympathie':'mean'})['Sympathie'].nlargest(top_MarkenSympathieBranche)
			top_n_MarkenSympathieBranche = df_CampaignCheckAuswertungsSelektion.groupby('Branche').agg({'Sympathie':'mean'})['Sympathie'].nlargest(anzahlBrancheGesamt)
		
		
			anzahlBranche = len(top_n_MarkenSympathieBranche)
		
			Abbildung_top_n_MarkenSympathieBranche = px.bar(top_n_MarkenSympathieBranche, 
			x=top_n_MarkenSympathieBranche.index, 
			y='Sympathie',
			color='Sympathie',
			text='Sympathie', #beschriftung auf Balken
			#hover_name='Sympathie', #Beschriftungstextauswahl für Balken
			title=f'MarkenSympathie (1-10) - Mittelwerte je Branche',
			orientation='v', #braucht es hier eigentlich nicht
			#color=top_n_MarkenSympathieBranche.index - unterschiedliche Farbe je Branche
			color_continuous_scale=[(0, FARBE_Minwert), (0.5, FARBE_Mittelwert), (1, FARBE_Maxwert)]
			)
			#Weitere Formatierungen der Abbildung
			#Abbildung_top_n_MarkenSympathieBranche.update_traces(texttemplate='%{text:.2f}', textposition='outside')
			Abbildung_top_n_MarkenSympathieBranche.update_traces(texttemplate='%{text:.1f}', textposition='outside')
			Abbildung_top_n_MarkenSympathieBranche.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
			Abbildung_top_n_MarkenSympathieBranche.update_yaxes(showline=True, linewidth=1, linecolor='white', gridcolor='Black')
			Abbildung_top_n_MarkenSympathieBranche.update_yaxes(range=[1, 10])
			#Horizontale Line mit Durchschnitt aller Messerwerte aus der DB
			Abbildung_top_n_MarkenSympathieBranche.add_hline(y=MittelwertMarkensympathie_Alle, line_width=5, line_dash="dot", line_color="grey", opacity=0.6, annotation_text="ø Alle Messwerte", 
		              annotation_position="top left", annotation_font_size=16,
		              annotation_font_color="grey")
		
			st.plotly_chart(Abbildung_top_n_MarkenSympathieBranche, use_container_width = True)
		
		
		"""
		
		
		
		
		
		
		
		#Abbildung - MarkenSympathie je Unternehmung ******************************************************************************************************************
		
		n_MarkenSympathieUnternehmen = df_CampaignCheckAuswertungsSelektion.groupby('Unternehmen').agg({'Sympathie':'mean'})['Sympathie']
		anzahlUnternehmenGesamt = len(n_MarkenSympathieUnternehmen)
		
		if anzahlUnternehmenGesamt > 1:
		
			st.subheader("Sympathie - nach Unternehmen:")
		
			st.write("Anzahl Unternehmen zur Auswahl: ",anzahlUnternehmenGesamt)
		
			if anzahlUnternehmenGesamt > 10:
				minAnzahlUnternehmen = 10
			else:
				minAnzahlUnternehmen = anzahlUnternehmenGesamt
		
			if anzahlUnternehmenGesamt == 1:
				minAnzahlUnternehmen = 1
		
			top_MarkenSympathieUnternehmen = st.slider('Wähle die Anzahl Unternehmen die angezeigt werden sollen:', min_value=0, max_value=anzahlUnternehmenGesamt, value=minAnzahlUnternehmen, key="MarkenSympathie_UGSlider")
			top_n_MarkenSympathieUnternehmen = df_CampaignCheckAuswertungsSelektion.groupby('Unternehmen').agg({'Sympathie':'mean'})['Sympathie'].nlargest(top_MarkenSympathieUnternehmen)
		
			anzahlUnternehmen = len(top_n_MarkenSympathieUnternehmen)
		
			Abbildung_top_n_MarkenSympathieUnternehmen = px.bar(top_n_MarkenSympathieUnternehmen, 
			x=top_n_MarkenSympathieUnternehmen.index, 
			y='Sympathie',
			color='Sympathie',
			#color=top_n_MarkenSympathieUnternehmen.index - unterschiedliche Farbe je Unternehmen
			text='Sympathie', #beschriftung auf Balken
			#hover_name='Sympathie', #Beschriftungstextauswahl für Balken
			title=f'MarkenSympathie - Sympathie je Unternehmen - Top ' + str(top_MarkenSympathieUnternehmen),
			orientation='v', #braucht es hier eigentlich nicht
			color_continuous_scale=[(0, FARBE_Minwert), (0.5, FARBE_Mittelwert), (1, FARBE_Maxwert)]
			)
			#Weitere Formatierungen der Abbildung
			Abbildung_top_n_MarkenSympathieUnternehmen.update_traces(texttemplate='%{text:.1f}', textposition='outside')
			Abbildung_top_n_MarkenSympathieUnternehmen.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
			Abbildung_top_n_MarkenSympathieUnternehmen.update_yaxes(showline=True, linewidth=1, linecolor='white', gridcolor='Black')
			Abbildung_top_n_MarkenSympathieUnternehmen.update_yaxes(range=[1, 10])
		
			#Horizontale Line mit Durchschnitt aller Messerwerte aus der DB
			Abbildung_top_n_MarkenSympathieUnternehmen.add_hline(y=MittelwertMarkensympathie_Alle, line_width=5, line_dash="dot", line_color="grey", opacity=0.6, annotation_text="ø Alle Messwerte", 
		              annotation_position="top left", annotation_font_size=16,
		              annotation_font_color="grey")
		
			if MittelwertMarkensympathie_Alle != MittelwertMarkensympathie:
				Abbildung_top_n_MarkenSympathieUnternehmen.add_hline(y=MittelwertMarkensympathie, line_width=2, line_dash="dot", line_color="white", opacity=0.8, annotation_text="ø Auswahl", 
		              annotation_position="top right")
		
		
			st.plotly_chart(Abbildung_top_n_MarkenSympathieUnternehmen, use_container_width = True)
			
			
		#MarkenSympathie -  Abbildungen mit Splits nach Geschlecht - wenn nur eine Unternehmung gewählt ist #######################
		if anzahlUnternehmenGesamt == 1:
			st.subheader ("Markensympathie (1-10) - "+ UnternehmenAuswahlAlsText)
			MarkenSympathie_AbbildungenMitBreakKolumne1, MarkenSympathie_AbbildungenMitBreakKolumne2, MarkenSympathie_AbbildungenMitBreakKolumne3 = st.columns(3)
	
			with MarkenSympathie_AbbildungenMitBreakKolumne1:
				#Abbildung MarkenSympathie - nach Geschlecht ***
				MarkenSympathieUnternehmen_Geschlecht = df_CampaignCheckAuswertungsSelektion.groupby('Geschlecht').agg({'Sympathie':'mean'})['Sympathie']
			
				Abbildung_MarkenSympathieUnternehmen_Geschlecht = px.bar(MarkenSympathieUnternehmen_Geschlecht, 
				x=MarkenSympathieUnternehmen_Geschlecht.index, #in der Indexspalte steht das Geschlecht in den Zeilen
				y='Sympathie',
				color=MarkenSympathieUnternehmen_Geschlecht.index,
				color_discrete_map={'Frau' : FARBE_Frau ,'Mann' : FARBE_Mann},
				text='Sympathie', #beschriftung auf Balken
				#hover_name='Sympathie', #Beschriftungstextauswahl für Balken
				title=f'Markensympathie - ' + UnternehmenAuswahlAlsText +" - nach Geschlecht"
				)
				
				#Weitere Formatierungen der Abbildung
				Abbildung_MarkenSympathieUnternehmen_Geschlecht.update_traces(texttemplate='%{text:.1f}', textposition='inside')
				Abbildung_MarkenSympathieUnternehmen_Geschlecht.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
				Abbildung_MarkenSympathieUnternehmen_Geschlecht.update_yaxes(showline=True, linewidth=1, linecolor='white', gridcolor='black')
				Abbildung_MarkenSympathieUnternehmen_Geschlecht.update_layout(showlegend=False)
				Abbildung_MarkenSympathieUnternehmen_Geschlecht.update_yaxes(range=[1, 10])
				
				st.plotly_chart(Abbildung_MarkenSympathieUnternehmen_Geschlecht, use_container_width = True)
				#st.plotly_chart(Abbildung_MarkenSympathieUnternehmen_Geschlecht, width=300)
				
			with MarkenSympathie_AbbildungenMitBreakKolumne2:
				#Abbildung MarkenSympathie - nach Alter ***
				MarkenSympathieUnternehmen_Alter = df_CampaignCheckAuswertungsSelektion.groupby('Alter').agg({'Sympathie':'mean'})['Sympathie']
			
				Abbildung_MarkenSympathieUnternehmen_Alter = px.bar(MarkenSympathieUnternehmen_Alter, 
				x=MarkenSympathieUnternehmen_Alter.index, #in der Indexspalte steht das Alter in den Zeilen
				y='Sympathie',
				color=MarkenSympathieUnternehmen_Alter.index,
				
				color_discrete_map={'16-19' : FARBE_16_29 ,'20-24' : FARBE_16_29 ,'25-29' : FARBE_16_29 ,'30-34' : FARBE_30_49,'35-39' : FARBE_30_49,'40-44' : FARBE_30_49,'45-49' : FARBE_30_49,'50-54' : FARBE_50plus,'55-59' : FARBE_50plus,'60+' : FARBE_50plus},

				text='Sympathie', #beschriftung auf Balken
				#hover_name='Sympathie', #Beschriftungstextauswahl für Balken
				title=f'Markensympathie - ' + UnternehmenAuswahlAlsText +" - nach Alter"
				)
				
				#Weitere Formatierungen der Abbildung
				Abbildung_MarkenSympathieUnternehmen_Alter.update_traces(texttemplate='%{text:.1f}', textposition='inside')
				Abbildung_MarkenSympathieUnternehmen_Alter.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
				Abbildung_MarkenSympathieUnternehmen_Alter.update_yaxes(showline=True, linewidth=1, linecolor='white', gridcolor='black')
				Abbildung_MarkenSympathieUnternehmen_Alter.update_layout(showlegend=False)
				Abbildung_MarkenSympathieUnternehmen_Alter.update_yaxes(range=[1, 10])
				
				st.plotly_chart(Abbildung_MarkenSympathieUnternehmen_Alter, use_container_width = True)
				#st.plotly_chart(Abbildung_MarkenSympathieUnternehmen_Alter, width=500)
				
			with MarkenSympathie_AbbildungenMitBreakKolumne3:	
				#Abbildung MarkenSympathie - nach Sprache ***
				MarkenSympathieUnternehmen_Sprache = df_CampaignCheckAuswertungsSelektion.groupby('Sprache').agg({'Sympathie':'mean'})['Sympathie']
			
				Abbildung_MarkenSympathieUnternehmen_Sprache = px.bar(MarkenSympathieUnternehmen_Sprache, 
				x=MarkenSympathieUnternehmen_Sprache.index, #in der Indexspalte steht das Sprache in den Zeilen
				y='Sympathie',
				color=MarkenSympathieUnternehmen_Sprache.index,
				color_discrete_map={'Deutsch' : FARBE_Deutsch ,'Französisch' : FARBE_Französisch},
				text='Sympathie', #beschriftung auf Balken
				#hover_name='Sympathie', #Beschriftungstextauswahl für Balken
				title=f'MarkenSympathie - ' + UnternehmenAuswahlAlsText +" - nach Sprache"
				)
				
				#Weitere Formatierungen der Abbildung
				Abbildung_MarkenSympathieUnternehmen_Sprache.update_traces(texttemplate='%{text:.1f}', textposition='inside')
				Abbildung_MarkenSympathieUnternehmen_Sprache.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
				Abbildung_MarkenSympathieUnternehmen_Sprache.update_yaxes(showline=True, linewidth=1, linecolor='white', gridcolor='black')
				Abbildung_MarkenSympathieUnternehmen_Sprache.update_layout(showlegend=False)
				Abbildung_MarkenSympathieUnternehmen_Sprache.update_yaxes(range=[1, 10])
				
				st.plotly_chart(Abbildung_MarkenSympathieUnternehmen_Sprache, use_container_width = True)
				#st.plotly_chart(Abbildung_MarkenSympathieUnternehmen_Sprache, width=300)
				
				
			if len(JahrAuswahl) > 1:
				#Abbildung MarkenSympathie - nach Jahr_Gesamt ***
				MarkenSympathieUnternehmen_Jahr_Gesamt = df_CampaignCheckAuswertungsSelektion.groupby('Jahr_Gesamt').agg({'Sympathie':'mean'})['Sympathie']
				
				Abbildung_MarkenSympathieUnternehmen_Jahr_Gesamt = px.bar(MarkenSympathieUnternehmen_Jahr_Gesamt, 
				x=MarkenSympathieUnternehmen_Jahr_Gesamt.index, #in der Indexspalte steht das Jahr_Gesamt in den Zeilen
				y='Sympathie',
				color=MarkenSympathieUnternehmen_Jahr_Gesamt.index,
				text='Sympathie', #beschriftung auf Balken
				#hover_name='Sympathie', #Beschriftungstextauswahl für Balken
				title=f'MarkenSympathie - ' + UnternehmenAuswahlAlsText + " - im Zeitverlauf"
				)
				
				#Weitere Formatierungen der Abbildung
				Abbildung_MarkenSympathieUnternehmen_Jahr_Gesamt.update_traces(texttemplate='%{text:.1f}', textposition='inside')
				Abbildung_MarkenSympathieUnternehmen_Jahr_Gesamt.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
				Abbildung_MarkenSympathieUnternehmen_Jahr_Gesamt.update_yaxes(showline=True, linewidth=1, linecolor='white', gridcolor='black')
				Abbildung_MarkenSympathieUnternehmen_Jahr_Gesamt.update_layout(showlegend=False)
				Abbildung_MarkenSympathieUnternehmen_Jahr_Gesamt.update_yaxes(range=[1, 10])
				
				st.plotly_chart(Abbildung_MarkenSympathieUnternehmen_Jahr_Gesamt, use_container_width = True)
				#st.plotly_chart(Abbildung_MarkenSympathieUnternehmen_Jahr_Gesamt, width=300)
	
			if len(MonatsAuswahl) > 1:
				#Abbildung MarkenSympathie - nach Jahr_Monat ***
				MarkenSympathieUnternehmen_Jahr_Monat = df_CampaignCheckAuswertungsSelektion.groupby('Jahr_Monat').agg({'Sympathie':'mean'})['Sympathie']
				
				Abbildung_MarkenSympathieUnternehmen_Jahr_Monat = px.line(MarkenSympathieUnternehmen_Jahr_Monat, 
				x=MarkenSympathieUnternehmen_Jahr_Monat.index, #in der Indexspalte steht das Jahr_Monat in den Zeilen
				y='Sympathie',
				#color=MarkenSympathieUnternehmen_Jahr_Monat.index,
				text='Sympathie', #beschriftung auf Balken
				#hover_name='Sympathie', #Beschriftungstextauswahl für Balken
				title=f'MarkenSympathie - ' + UnternehmenAuswahlAlsText + " - im Zeitverlauf"
				)
				
				#Weitere Formatierungen der Abbildung
				Abbildung_MarkenSympathieUnternehmen_Jahr_Monat.update_yaxes(range=[1, 10])
				Abbildung_MarkenSympathieUnternehmen_Jahr_Monat.update_traces(texttemplate='%{text:.1f}')
				Abbildung_MarkenSympathieUnternehmen_Jahr_Monat.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
				#Abbildung_MarkenSympathieUnternehmen_Jahr_Monat.update_yaxes(showline=True, linewidth=0.2, linecolor='black', gridcolor='black')
				
				Abbildung_MarkenSympathieUnternehmen_Jahr_Monat.update_xaxes(showline=True, linewidth=1, linecolor='black', gridcolor='Black')
				Abbildung_MarkenSympathieUnternehmen_Jahr_Monat.update_yaxes(showline=True, linewidth=2, linecolor='black', gridcolor='Black')
				Abbildung_MarkenSympathieUnternehmen_Jahr_Monat.update_layout(xaxis=dict(showticklabels=True,linewidth=1))
				#Abbildung_MarkenSympathieUnternehmen_Jahr_Monat.update_layout(showlegend=False)
				Abbildung_MarkenSympathieUnternehmen_Jahr_Monat.update_xaxes(title_text='Jahr - Monat')
				st.plotly_chart(Abbildung_MarkenSympathieUnternehmen_Jahr_Monat, use_container_width = True)
	
	
	
	
	
	
	
	
	
	
		#Abbildung - FirstChoice je Unternehmung ******************************************************************************************************************
		
		n_FirstChoiceUnternehmen = df_CampaignCheckAuswertungsSelektion.groupby('Unternehmen').agg({'First Choice_codiert':'mean'})['First Choice_codiert']
		#st.write("n_FirstChoiceUnternehmen: ", n_FirstChoiceUnternehmen)
		
		
		
		
		
		
		
		anzahlUnternehmenGesamt = len(n_FirstChoiceUnternehmen)
		
		if anzahlUnternehmenGesamt > 1:
		
			st.subheader("First Choice (0-100%) - nach Unternehmen:")
		
			st.write("Anzahl Unternehmen zur Auswahl: ",anzahlUnternehmenGesamt)
		
			if anzahlUnternehmenGesamt > 10:
				minAnzahlUnternehmen = 10
			else:
				minAnzahlUnternehmen = anzahlUnternehmenGesamt
		
			if anzahlUnternehmenGesamt == 1:
				minAnzahlUnternehmen = 1
		
			top_FirstChoiceUnternehmen = st.slider('Wähle die Anzahl Unternehmen die angezeigt werden:', min_value=0, max_value=anzahlUnternehmenGesamt, value=minAnzahlUnternehmen)
			top_n_FirstChoiceUnternehmen = df_CampaignCheckAuswertungsSelektion.groupby('Unternehmen').agg({'First Choice_codiert':'mean'})['First Choice_codiert'].nlargest(top_FirstChoiceUnternehmen)
		
			anzahlUnternehmen = len(top_n_FirstChoiceUnternehmen)
		
			Abbildung_top_n_FirstChoiceUnternehmen = px.bar(top_n_FirstChoiceUnternehmen, 
			x=top_n_FirstChoiceUnternehmen.index, 
			y='First Choice_codiert',
			color='First Choice_codiert',
			#color_continuous_scale=px.colors.sequential.Blackbody,
			#color_continuous_scale=px.colors.sequential.Brwnyl,
			#color=top_n_FirstChoiceUnternehmen.index - unterschiedliche Farbe je Unternehmen
			text='First Choice_codiert', #beschriftung auf Balken
			#hover_name='First Choice_codiert', #Beschriftungstextauswahl für Balken
			title=f'FirstChoice - First Choice je Unternehmen - Top ' + str(top_FirstChoiceUnternehmen),
			orientation='v', #braucht es hier eigentlich nicht
			color_continuous_scale=[(0, FARBE_Minwert), (0.5, FARBE_Mittelwert), (1, FARBE_Maxwert)]
			)
			#Weitere Formatierungen der Abbildung
			Abbildung_top_n_FirstChoiceUnternehmen.update_traces(texttemplate='%{text:.1f}'+" %", textposition='inside')
			Abbildung_top_n_FirstChoiceUnternehmen.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
			Abbildung_top_n_FirstChoiceUnternehmen.update_yaxes(showline=True, linewidth=1, linecolor='white', gridcolor='black')
			
			#Horizontale Line mit Durchschnitt aller Messerwerte aus der DB
			Abbildung_top_n_FirstChoiceUnternehmen.add_hline(y=MittelwertFirstChoice_Alle, line_width=5, line_dash="dot", line_color="grey", opacity=0.6, annotation_text="ø Alle Messwerte", 
		              annotation_position="top left", annotation_font_size=16,
		              annotation_font_color="grey")
		
			if MittelwertFirstChoice_Alle != MittelwertFirstChoice:
				Abbildung_top_n_FirstChoiceUnternehmen.add_hline(y=MittelwertFirstChoice, line_width=2, line_dash="dot", line_color="white", opacity=0.8, annotation_text="ø Auswahl", 
		              annotation_position="top right")
		
		
			st.plotly_chart(Abbildung_top_n_FirstChoiceUnternehmen, use_container_width = True)
		
		
		
		
		
	
		#FirstChoice -  Abbildungen mit Splits nach Geschlecht - wenn nur eine Unternehmung gewählt ist #######################
		if anzahlUnternehmenGesamt == 1:
			st.subheader ("First Choice (0-100%) - "+ UnternehmenAuswahlAlsText)
			FirstChoice_AbbildungenMitBreakKolumne1, FirstChoice_AbbildungenMitBreakKolumne2, FirstChoice_AbbildungenMitBreakKolumne3 = st.columns(3)
	
			with FirstChoice_AbbildungenMitBreakKolumne1:
				#Abbildung FirstChoice - nach Geschlecht ***
				FirstChoiceUnternehmen_Geschlecht = df_CampaignCheckAuswertungsSelektion.groupby('Geschlecht').agg({'First Choice_codiert':'mean'})['First Choice_codiert']
			
				Abbildung_FirstChoiceUnternehmen_Geschlecht = px.bar(FirstChoiceUnternehmen_Geschlecht, 
				x=FirstChoiceUnternehmen_Geschlecht.index, #in der Indexspalte steht das Geschlecht in den Zeilen
				y='First Choice_codiert',
				color=FirstChoiceUnternehmen_Geschlecht.index,
				color_discrete_map={'Frau' : FARBE_Frau ,'Mann' : FARBE_Mann},
				text='First Choice_codiert', #beschriftung auf Balken
				#hover_name='First Choice_codiert', #Beschriftungstextauswahl für Balken
				title=f'FirstChoice - ' + UnternehmenAuswahlAlsText +" - nach Geschlecht"
				)
				
				#Weitere Formatierungen der Abbildung
				Abbildung_FirstChoiceUnternehmen_Geschlecht.update_traces(texttemplate='%{text:.1f}'+" %", textposition='outside')
				Abbildung_FirstChoiceUnternehmen_Geschlecht.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
				Abbildung_FirstChoiceUnternehmen_Geschlecht.update_yaxes(showline=True, linewidth=1, linecolor='white', gridcolor='black')
				Abbildung_FirstChoiceUnternehmen_Geschlecht.update_layout(showlegend=False)
				
				st.plotly_chart(Abbildung_FirstChoiceUnternehmen_Geschlecht, use_container_width = True)
				#st.plotly_chart(Abbildung_FirstChoiceUnternehmen_Geschlecht, width=300)
			
			with FirstChoice_AbbildungenMitBreakKolumne2:
				#Abbildung FirstChoice - nach Alter ***
				FirstChoiceUnternehmen_Alter = df_CampaignCheckAuswertungsSelektion.groupby('Alter').agg({'First Choice_codiert':'mean'})['First Choice_codiert']
			
				Abbildung_FirstChoiceUnternehmen_Alter = px.bar(FirstChoiceUnternehmen_Alter, 
				x=FirstChoiceUnternehmen_Alter.index, #in der Indexspalte steht das Alter in den Zeilen
				y='First Choice_codiert',
				color=FirstChoiceUnternehmen_Alter.index,
				color_discrete_map={'16-19' : FARBE_16_29 ,'20-24' : FARBE_16_29 ,'25-29' : FARBE_16_29 ,'30-34' : FARBE_30_49,'35-39' : FARBE_30_49,'40-44' : FARBE_30_49,'45-49' : FARBE_30_49,'50-54' : FARBE_50plus,'55-59' : FARBE_50plus,'60+' : FARBE_50plus},
				text='First Choice_codiert', #beschriftung auf Balken
				#hover_name='First Choice_codiert', #Beschriftungstextauswahl für Balken
				title=f'FirstChoice - ' + UnternehmenAuswahlAlsText +" - nach Alter"
				)
				
				#Weitere Formatierungen der Abbildung
				Abbildung_FirstChoiceUnternehmen_Alter.update_traces(texttemplate='%{text:.1f}'+" %", textposition='outside')
				Abbildung_FirstChoiceUnternehmen_Alter.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
				Abbildung_FirstChoiceUnternehmen_Alter.update_yaxes(showline=True, linewidth=1, linecolor='white', gridcolor='black')
				Abbildung_FirstChoiceUnternehmen_Alter.update_layout(showlegend=False)
				
				st.plotly_chart(Abbildung_FirstChoiceUnternehmen_Alter, use_container_width = True)
				#st.plotly_chart(Abbildung_FirstChoiceUnternehmen_Alter, width=500)
				
			with FirstChoice_AbbildungenMitBreakKolumne3:	
				#Abbildung FirstChoice - nach Sprache ***
				FirstChoiceUnternehmen_Sprache = df_CampaignCheckAuswertungsSelektion.groupby('Sprache').agg({'First Choice_codiert':'mean'})['First Choice_codiert']
			
				Abbildung_FirstChoiceUnternehmen_Sprache = px.bar(FirstChoiceUnternehmen_Sprache, 
				x=FirstChoiceUnternehmen_Sprache.index, #in der Indexspalte steht das Sprache in den Zeilen
				y='First Choice_codiert',
				color=FirstChoiceUnternehmen_Sprache.index,
				color_discrete_map={'Deutsch' : FARBE_Deutsch ,'Französisch' : FARBE_Französisch},
				text='First Choice_codiert', #beschriftung auf Balken
				#hover_name='First Choice_codiert', #Beschriftungstextauswahl für Balken
				title=f'FirstChoice - ' + UnternehmenAuswahlAlsText +" - nach Sprache"
				)
				
				#Weitere Formatierungen der Abbildung
				Abbildung_FirstChoiceUnternehmen_Sprache.update_traces(texttemplate='%{text:.1f}'+" %", textposition='outside')
				Abbildung_FirstChoiceUnternehmen_Sprache.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
				Abbildung_FirstChoiceUnternehmen_Sprache.update_yaxes(showline=True, linewidth=1, linecolor='white', gridcolor='black')
				Abbildung_FirstChoiceUnternehmen_Sprache.update_layout(showlegend=False)
				
				st.plotly_chart(Abbildung_FirstChoiceUnternehmen_Sprache, use_container_width = True)
				#st.plotly_chart(Abbildung_FirstChoiceUnternehmen_Sprache, width=300)
	
				#Abbildung - Consideration je Unternehmung ******************************************************************************************************************
		
		
			if len(JahrAuswahl) > 1:
				#Abbildung FirstChoice - nach Jahr_Gesamt ***
				FirstChoiceUnternehmen_Jahr_Gesamt = df_CampaignCheckAuswertungsSelektion.groupby('Jahr_Gesamt').agg({'First Choice_codiert':'mean'})['First Choice_codiert']
				
				Abbildung_FirstChoiceUnternehmen_Jahr_Gesamt = px.bar(FirstChoiceUnternehmen_Jahr_Gesamt, 
				x=FirstChoiceUnternehmen_Jahr_Gesamt.index, #in der Indexspalte steht das Jahr_Gesamt in den Zeilen
				y='First Choice_codiert',
				color=FirstChoiceUnternehmen_Jahr_Gesamt.index,
				text='First Choice_codiert', #beschriftung auf Balken
				#hover_name='Markenbekanntheit', #Beschriftungstextauswahl für Balken
				title=f'FirstChoice - ' + UnternehmenAuswahlAlsText + " - im Zeitverlauf"
				)
				
				#Weitere Formatierungen der Abbildung
				Abbildung_FirstChoiceUnternehmen_Jahr_Gesamt.update_traces(texttemplate='%{text:.1f}'+" %", textposition='inside')
				Abbildung_FirstChoiceUnternehmen_Jahr_Gesamt.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
				Abbildung_FirstChoiceUnternehmen_Jahr_Gesamt.update_yaxes(showline=True, linewidth=1, linecolor='white', gridcolor='black')
				Abbildung_FirstChoiceUnternehmen_Jahr_Gesamt.update_layout(showlegend=False)
				
				st.plotly_chart(Abbildung_FirstChoiceUnternehmen_Jahr_Gesamt, use_container_width = True)
				#st.plotly_chart(Abbildung_FirstChoiceUnternehmen_Jahr_Gesamt, width=300)
	
			if len(MonatsAuswahl) > 1:
				#Linienchart Abbildung FirstChoice - nach Jahr_Monat ***
				FirstChoiceUnternehmen_Jahr_Monat = df_CampaignCheckAuswertungsSelektion.groupby('Jahr_Monat').agg({'First Choice_codiert':'mean'})['First Choice_codiert']
				
				Abbildung_FirstChoiceUnternehmen_Jahr_Monat = px.line(FirstChoiceUnternehmen_Jahr_Monat, 
				x=FirstChoiceUnternehmen_Jahr_Monat.index, #in der Indexspalte steht das Jahr_Monat in den Zeilen
				y='First Choice_codiert',
				#color=FirstChoiceUnternehmen_Jahr_Monat.index,
				text='First Choice_codiert', #beschriftung auf Balken
				#hover_name='Markenbekanntheit', #Beschriftungstextauswahl für Balken
				title=f'FirstChoice - ' + UnternehmenAuswahlAlsText + " - im Zeitverlauf"
				)
				
				#Weitere Formatierungen der Abbildung
				Abbildung_FirstChoiceUnternehmen_Jahr_Monat.update_yaxes(range=[0, 100])
				Abbildung_FirstChoiceUnternehmen_Jahr_Monat.update_traces(texttemplate='%{text:.1f}'+" %")
				Abbildung_FirstChoiceUnternehmen_Jahr_Monat.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
				#Abbildung_FirstChoiceUnternehmen_Jahr_Monat.update_yaxes(showline=True, linewidth=0.2, linecolor='black', gridcolor='black')
				
				Abbildung_FirstChoiceUnternehmen_Jahr_Monat.update_xaxes(showline=True, linewidth=1, linecolor='black', gridcolor='Black')
				Abbildung_FirstChoiceUnternehmen_Jahr_Monat.update_yaxes(showline=True, linewidth=2, linecolor='black', gridcolor='Black')
				Abbildung_FirstChoiceUnternehmen_Jahr_Monat.update_layout(xaxis=dict(showticklabels=True,linewidth=1))
				#Abbildung_FirstChoiceUnternehmen_Jahr_Monat.update_layout(showlegend=False)
				Abbildung_FirstChoiceUnternehmen_Jahr_Monat.update_xaxes(title_text='Jahr - Monat')
				st.plotly_chart(Abbildung_FirstChoiceUnternehmen_Jahr_Monat, use_container_width = True)	
		
				



		n_ConsiderationUnternehmen = df_CampaignCheckAuswertungsSelektion.groupby('Unternehmen').agg({'Consideration':'mean'})['Consideration']
		#st.write("n_ConsiderationUnternehmen: ", n_ConsiderationUnternehmen)
		

		anzahlUnternehmenGesamt = len(n_ConsiderationUnternehmen)
		
		if anzahlUnternehmenGesamt > 1:
		
			st.subheader("Consideration (0-100%) - nach Unternehmen:")
		
			st.write("Anzahl Unternehmen zur Auswahl: ",anzahlUnternehmenGesamt)
		
			if anzahlUnternehmenGesamt > 10:
				minAnzahlUnternehmen = 10
			else:
				minAnzahlUnternehmen = anzahlUnternehmenGesamt
		
			if anzahlUnternehmenGesamt == 1:
				minAnzahlUnternehmen = 1
		
			top_ConsiderationUnternehmen = st.slider('Anzahl Unternehmen die angezeigt werden sollen:', min_value=0, max_value=anzahlUnternehmenGesamt, value=minAnzahlUnternehmen)
			top_n_ConsiderationUnternehmen = df_CampaignCheckAuswertungsSelektion.groupby('Unternehmen').agg({'Consideration':'mean'})['Consideration'].nlargest(top_ConsiderationUnternehmen)
		
			anzahlUnternehmen = len(top_n_ConsiderationUnternehmen)
		
			Abbildung_top_n_ConsiderationUnternehmen = px.bar(top_n_ConsiderationUnternehmen, 
			x=top_n_ConsiderationUnternehmen.index, 
			y='Consideration',
			color='Consideration',
			#color_continuous_scale=px.colors.sequential.Blackbody,
			#color_continuous_scale=px.colors.sequential.Brwnyl,
			#color=top_n_ConsiderationUnternehmen.index - unterschiedliche Farbe je Unternehmen
			text='Consideration', #beschriftung auf Balken
			#hover_name='Consideration', #Beschriftungstextauswahl für Balken
			title=f'Consideration je Unternehmen - Top ' + str(top_ConsiderationUnternehmen),
			orientation='v', #braucht es hier eigentlich nicht
			color_continuous_scale=[(0, FARBE_Minwert), (0.5, FARBE_Mittelwert), (1, FARBE_Maxwert)]
			)
			#Weitere Formatierungen der Abbildung
			Abbildung_top_n_ConsiderationUnternehmen.update_traces(texttemplate='%{text:.1f}'+" %", textposition='outside')
			Abbildung_top_n_ConsiderationUnternehmen.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
			Abbildung_top_n_ConsiderationUnternehmen.update_yaxes(showline=True, linewidth=1, linecolor='white', gridcolor='black')
			
			#Horizontale Line mit Durchschnitt aller Messerwerte aus der DB
			Abbildung_top_n_ConsiderationUnternehmen.add_hline(y=MittelwertConsideration_Alle, line_width=5, line_dash="dot", line_color="grey", opacity=0.6, annotation_text="ø Alle Messwerte", 
		              annotation_position="top left", annotation_font_size=16,
		              annotation_font_color="grey")
		
			if MittelwertConsideration_Alle != MittelwertConsideration:
				Abbildung_top_n_ConsiderationUnternehmen.add_hline(y=MittelwertConsideration, line_width=2, line_dash="dot", line_color="white", opacity=0.8, annotation_text="ø Auswahl", 
		              annotation_position="top right")
		
		
			st.plotly_chart(Abbildung_top_n_ConsiderationUnternehmen, use_container_width = True)
		
		
		
		
		
	
		#Consideration -  Abbildungen mit Splits nach Geschlecht - wenn nur eine Unternehmung gewählt ist #######################
		if anzahlUnternehmenGesamt == 1:
			st.subheader ("Consideration (0-100%) - "+ UnternehmenAuswahlAlsText)
		
			Consideration_AbbildungenMitBreakKolumne1, Consideration_AbbildungenMitBreakKolumne2, Consideration_AbbildungenMitBreakKolumne3 = st.columns(3)
	
			with Consideration_AbbildungenMitBreakKolumne1:
				#Abbildung Consideration - nach Geschlecht ***
				ConsiderationUnternehmen_Geschlecht = df_CampaignCheckAuswertungsSelektion.groupby('Geschlecht').agg({'Consideration':'mean'})['Consideration']
			
				Abbildung_ConsiderationUnternehmen_Geschlecht = px.bar(ConsiderationUnternehmen_Geschlecht, 
				x=ConsiderationUnternehmen_Geschlecht.index, #in der Indexspalte steht das Geschlecht in den Zeilen
				y='Consideration',
				color=ConsiderationUnternehmen_Geschlecht.index,
				color_discrete_map={'Frau' : FARBE_Frau ,'Mann' : FARBE_Mann},
				text='Consideration', #beschriftung auf Balken
				#hover_name='Consideration', #Beschriftungstextauswahl für Balken
				title=f'Consideration - ' + UnternehmenAuswahlAlsText +" - nach Geschlecht"
				)
				
				#Weitere Formatierungen der Abbildung
				Abbildung_ConsiderationUnternehmen_Geschlecht.update_traces(texttemplate='%{text:.1f}'+" %", textposition='outside')
				Abbildung_ConsiderationUnternehmen_Geschlecht.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
				Abbildung_ConsiderationUnternehmen_Geschlecht.update_yaxes(showline=True, linewidth=1, linecolor='white', gridcolor='black')
				Abbildung_ConsiderationUnternehmen_Geschlecht.update_layout(showlegend=False)
				
				st.plotly_chart(Abbildung_ConsiderationUnternehmen_Geschlecht, use_container_width = True)
				#st.plotly_chart(Abbildung_ConsiderationUnternehmen_Geschlecht, width=300)
			
			with Consideration_AbbildungenMitBreakKolumne2:
				#Abbildung Consideration - nach Alter ***
				ConsiderationUnternehmen_Alter = df_CampaignCheckAuswertungsSelektion.groupby('Alter').agg({'Consideration':'mean'})['Consideration']
			
				Abbildung_ConsiderationUnternehmen_Alter = px.bar(ConsiderationUnternehmen_Alter, 
				x=ConsiderationUnternehmen_Alter.index, #in der Indexspalte steht das Alter in den Zeilen
				y='Consideration',
				color=ConsiderationUnternehmen_Alter.index,
				color_discrete_map={'16-19' : FARBE_16_29 ,'20-24' : FARBE_16_29 ,'25-29' : FARBE_16_29 ,'30-34' : FARBE_30_49,'35-39' : FARBE_30_49,'40-44' : FARBE_30_49,'45-49' : FARBE_30_49,'50-54' : FARBE_50plus,'55-59' : FARBE_50plus,'60+' : FARBE_50plus},
				text='Consideration', #beschriftung auf Balken
				#hover_name='Consideration', #Beschriftungstextauswahl für Balken
				title=f'Consideration - ' + UnternehmenAuswahlAlsText +" - nach Alter"
				)
				
				#Weitere Formatierungen der Abbildung
				Abbildung_ConsiderationUnternehmen_Alter.update_traces(texttemplate='%{text:.1f}'+" %", textposition='outside')
				Abbildung_ConsiderationUnternehmen_Alter.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
				Abbildung_ConsiderationUnternehmen_Alter.update_yaxes(showline=True, linewidth=1, linecolor='white', gridcolor='black')
				Abbildung_ConsiderationUnternehmen_Alter.update_layout(showlegend=False)
				
				st.plotly_chart(Abbildung_ConsiderationUnternehmen_Alter, use_container_width = True)
				#st.plotly_chart(Abbildung_ConsiderationUnternehmen_Alter, width=500)
				
			with Consideration_AbbildungenMitBreakKolumne3:	
				#Abbildung Consideration - nach Sprache ***
				ConsiderationUnternehmen_Sprache = df_CampaignCheckAuswertungsSelektion.groupby('Sprache').agg({'Consideration':'mean'})['Consideration']
			
				Abbildung_ConsiderationUnternehmen_Sprache = px.bar(ConsiderationUnternehmen_Sprache, 
				x=ConsiderationUnternehmen_Sprache.index, #in der Indexspalte steht das Sprache in den Zeilen
				y='Consideration',
				color=ConsiderationUnternehmen_Sprache.index,
				color_discrete_map={'Deutsch' : FARBE_Deutsch ,'Französisch' : FARBE_Französisch},
				text='Consideration', #beschriftung auf Balken
				#hover_name='Consideration', #Beschriftungstextauswahl für Balken
				title=f'Consideration - ' + UnternehmenAuswahlAlsText +" - nach Sprache"
				)
				
				#Weitere Formatierungen der Abbildung
				Abbildung_ConsiderationUnternehmen_Sprache.update_traces(texttemplate='%{text:.1f}'+" %", textposition='outside')
				Abbildung_ConsiderationUnternehmen_Sprache.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
				Abbildung_ConsiderationUnternehmen_Sprache.update_yaxes(showline=True, linewidth=1, linecolor='white', gridcolor='black')
				Abbildung_ConsiderationUnternehmen_Sprache.update_layout(showlegend=False)
				
				st.plotly_chart(Abbildung_ConsiderationUnternehmen_Sprache, use_container_width = True)
				#st.plotly_chart(Abbildung_ConsiderationUnternehmen_Sprache, width=300)
	
			if len(JahrAuswahl) > 1:
				#Abbildung Consideration - nach Jahr_Gesamt ***
				ConsiderationUnternehmen_Jahr_Gesamt = df_CampaignCheckAuswertungsSelektion.groupby('Jahr_Gesamt').agg({'Consideration':'mean'})['Consideration']
				
				Abbildung_ConsiderationUnternehmen_Jahr_Gesamt = px.bar(ConsiderationUnternehmen_Jahr_Gesamt, 
				x=ConsiderationUnternehmen_Jahr_Gesamt.index, #in der Indexspalte steht das Jahr_Gesamt in den Zeilen
				y='Consideration',
				color=ConsiderationUnternehmen_Jahr_Gesamt.index,
				text='Consideration', #beschriftung auf Balken
				#hover_name='Markenbekanntheit', #Beschriftungstextauswahl für Balken
				title=f'Consideration - ' + UnternehmenAuswahlAlsText + " - im Zeitverlauf"
				)
				
				#Weitere Formatierungen der Abbildung
				Abbildung_ConsiderationUnternehmen_Jahr_Gesamt.update_traces(texttemplate='%{text:.1f}'+" %", textposition='inside')
				Abbildung_ConsiderationUnternehmen_Jahr_Gesamt.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
				Abbildung_ConsiderationUnternehmen_Jahr_Gesamt.update_yaxes(showline=True, linewidth=1, linecolor='white', gridcolor='black')
				Abbildung_ConsiderationUnternehmen_Jahr_Gesamt.update_layout(showlegend=False)
				
				st.plotly_chart(Abbildung_ConsiderationUnternehmen_Jahr_Gesamt, use_container_width = True)
				#st.plotly_chart(Abbildung_ConsiderationUnternehmen_Jahr_Gesamt, width=300)
	
			if len(MonatsAuswahl) > 1:
				#Linienchart Abbildung Consideration - nach Jahr_Monat ***
				ConsiderationUnternehmen_Jahr_Monat = df_CampaignCheckAuswertungsSelektion.groupby('Jahr_Monat').agg({'Consideration':'mean'})['Consideration']
				
				Abbildung_ConsiderationUnternehmen_Jahr_Monat = px.line(ConsiderationUnternehmen_Jahr_Monat, 
				x=ConsiderationUnternehmen_Jahr_Monat.index, #in der Indexspalte steht das Jahr_Monat in den Zeilen
				y='Consideration',
				#color=ConsiderationUnternehmen_Jahr_Monat.index,
				text='Consideration', #beschriftung auf Balken
				#hover_name='Markenbekanntheit', #Beschriftungstextauswahl für Balken
				title=f'Consideration - ' + UnternehmenAuswahlAlsText + " - im Zeitverlauf"
				)
				
				#Weitere Formatierungen der Abbildung
				Abbildung_ConsiderationUnternehmen_Jahr_Monat.update_yaxes(range=[0, 100])
				Abbildung_ConsiderationUnternehmen_Jahr_Monat.update_traces(texttemplate='%{text:.1f}'+" %")
				Abbildung_ConsiderationUnternehmen_Jahr_Monat.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
				#Abbildung_ConsiderationUnternehmen_Jahr_Monat.update_yaxes(showline=True, linewidth=0.2, linecolor='black', gridcolor='black')
				
				Abbildung_ConsiderationUnternehmen_Jahr_Monat.update_xaxes(showline=True, linewidth=1, linecolor='black', gridcolor='Black')
				Abbildung_ConsiderationUnternehmen_Jahr_Monat.update_yaxes(showline=True, linewidth=2, linecolor='black', gridcolor='Black')
				Abbildung_ConsiderationUnternehmen_Jahr_Monat.update_layout(xaxis=dict(showticklabels=True,linewidth=1))
				#Abbildung_ConsiderationUnternehmen_Jahr_Monat.update_layout(showlegend=False)
				Abbildung_ConsiderationUnternehmen_Jahr_Monat.update_xaxes(title_text='Jahr - Monat')
				st.plotly_chart(Abbildung_ConsiderationUnternehmen_Jahr_Monat, use_container_width = True)	
		
				

	
	
		



############################################################################################	
#Kampagnen-KPIs ############################################################################
############################################################################################	

	if KPIAuswahl == "Kampagnen-KPIs":
		
		placeholder.empty()
		
		#df_CampaignCheckAuswertungsSelektion = df_KampagnenAuswahl
		#df_Kampagnen = df_CampaignCheckAuswertungsSelektion.drop(df_CampaignCheckAuswertungsSelektion[df_CampaignCheckAuswertungsSelektion['Recognition']!="<NA>"].index, inplace = True)
		#df_Kampagnen = df_CampaignCheckAuswertungsSelektion.dropna(subset = ["Recognition"], inplace=True)
		#df_Kampagnen = df_ManuellImportierteDB.dropna(subset = ["Recognition"], inplace=True)
		
		#st.write(df_KampagnenAuswahl) #Alle Kampagnendaten
		
		df_CampaignCheckAuswertungsSelektion['Anzahl Kontakte Andere'] = df_CampaignCheckAuswertungsSelektion['Anzahl Kontakte Andere'].fillna(0)
		df_CampaignCheckAuswertungsSelektion['Anzahl Kontakte Omnet'] = df_CampaignCheckAuswertungsSelektion['Anzahl Kontakte Omnet'].fillna(0)
		
		#Gesamtkontakte Online
		df_CampaignCheckAuswertungsSelektion['Online-Kontake Gesamt'] = df_CampaignCheckAuswertungsSelektion['Anzahl Kontakte Omnet'] + df_CampaignCheckAuswertungsSelektion['Anzahl Kontakte Andere']
		
		
		
		#Dataframe mit ausgewählten Kampagnen-Variablen
		df_Kampagnen = df_CampaignCheckAuswertungsSelektion.groupby(['Unternehmen','Kampagne','GetestetesWerbeMedium']).agg({'Recognition_Wert':['mean'],'Werbebeurteilung - Gefällt mir':['mean'],'Werbebeurteilung - Ist etwas Besonderes':['mean'],'Werbebeurteilung - Ist glaubwürdig':['mean'],'Werbebeurteilung - Ist verständlich':['mean'],'Werbebeurteilung - Reizt mich, mehr zu erfahren':['mean'],'Kauf (KDA Outcome)':['mean'],'NPS':['mean'],'Anzahl Kontakte Omnet':['mean'],'Anzahl Kontakte Andere':['mean'],'Online-Kontake Gesamt':['mean']}) 
		
		# rename columns
		df_Kampagnen.columns = ['Recognition - Mittelwert (%)', 'Kampagne gefällt (1-7)', 'Kampagne besonders (1-7)', 'Kampagne glaubwürdig (1-7)', 'Kampagne verständlich (1-7)', 'Kampagne kaufreiz (1-7)', 'KDA (1-7)', 'NPS (0-10)', 'Omnet-Kontakte Mittelwert', 'Kontakte andere Netzwerke - Mittelwert', 'Onlinekontake Gesamt (Omnet und Andere) - Mittelwert']
		
		
		# reset index to get grouped columns back
		df_Kampagnen = df_Kampagnen.reset_index()
		
		
		# Aktuelles Auswertungsdataframe nach dem alle Auswahlmöglichkeiten in den Menüs links getätigt wurden ####
		
		CampaignCheckAuswertungsSelektionExpander = st.expander("Aktuelles Auswertungsdataframe")
		with CampaignCheckAuswertungsSelektionExpander:
			st.write("Aktuelle Auswertungsdatenbank df_CampaignCheckAuswertungsSelektion: ",df_CampaignCheckAuswertungsSelektion)
		
		
		
		
		
		KampagnenAuswahleExpander = st.expander("Tabelle mit den ø-Werten der einzelnen Kampagnen")
		with KampagnenAuswahleExpander:

			speicherZeitpunkt = pd.to_datetime('today')
			st.write("")
			st.write(df_Kampagnen)
			st.write("")
			if len(df_Kampagnen) > 0:					
				def to_excel(df_Kampagnen):
					output = BytesIO()
					writer = pd.ExcelWriter(output, engine='xlsxwriter')
					df_Kampagnen.to_excel(writer, index=False, sheet_name='Sheet1')
					workbook = writer.book
					worksheet = writer.sheets['Sheet1']
					format1 = workbook.add_format({'num_format': '0.00'}) 
					worksheet.set_column('A:A', None, format1)  
					writer.save()
					processed_data = output.getvalue()
					return processed_data
				df_xlsx = to_excel(df_Kampagnen)
				st.download_button(label='📥 Tabelle in Excel abspeichern?',
					data=df_xlsx ,
					file_name= 'CCC_DES_Benchmarks_Kampagnenwerte_Tabellenexport '+str(speicherZeitpunkt) +'.xlsx' )	
			




		#Auswertungen  - Anzeige von ø Messwerte ##########################################################################
		st.subheader("")
		#st.subheader("Kampagnen-KPIs")
		st.markdown(""" <style> .font {font-size:30px ; font-family: 'Cooper Black'; color: #8CB6D8";} </style> """, unsafe_allow_html=True)
		
		st.markdown('<p class="font">Kampagnen-KPIs</p>', unsafe_allow_html=True)
		
		#st.subheader("ø Messwerte:")
		
		AnzahlMesswerte = len(df_CampaignCheckAuswertungsSelektion)
		st.write("Anzahl Messwerte (Zeilen) in der Auswahl: ", AnzahlMesswerte)
		
		#Kampagnen_Tabelle = df_CampaignCheckAuswertungsSelektion.groupby('Firma_KW_Monat_Jahr').agg({'Werbeerinnerung':'mean'})['Werbeerinnerung']
		#KampagnenTabelle = df_CampaignCheckAuswertungsSelektion['Firma_KW_Monat_Jahr'].unique()
		#anzahlKampagnen = len(KampagnenTabelle)
		#st.write("Anzahl Kampagnen: ",anzahlKampagnen)
		
		UnternehmenTabelle = df_CampaignCheckAuswertungsSelektion ['Unternehmen'].unique()
		anzahlUnternehmen = len(UnternehmenTabelle)
		st.write("Anzahl Unternehmen: ",anzahlUnternehmen)	
		
		BranchenTabelle = df_CampaignCheckAuswertungsSelektion['Branche'].unique()
		anzahlBranchen = len(BranchenTabelle)
		st.write("Anzahl Branchen: ",anzahlBranchen)
		
		
		
		KampagnenTabelle = df_CampaignCheckAuswertungsSelektion['Kampagne'].unique()
		anzahlKampagnen = len(KampagnenTabelle)
		st.write("Anzahl Kampagnen: ",anzahlKampagnen)
		#st.write(KampagnenTabelle)
	
		BefragteTabelle = df_CampaignCheckAuswertungsSelektion ['Participant_Begin'].unique()
		anzahlBefragte = len(BefragteTabelle)
		st.write("Anzahl Befragte: ",anzahlBefragte)
		#st.write(KampagnenTabelle)
	
		#Blaue Infofenster die anzeigen welche Branchen / Unternehmen ausgewählt wurden
		st.subheader("")

		if my_BrancheSelect !=[]:
			if len (my_BrancheSelect) == 1:
				st.info("Ausgewählte Branche: "+ BrancheAuswahlAlsText)
			else:
				st.info("Ausgewählte Branchen: "+ BrancheAuswahlAlsText)
				
		if my_UnternehmenSelect !=[]:
			if len (my_UnternehmenSelect) == 1:
				st.info("Ausgewählte Marke: "+UnternehmenAuswahlAlsText)
			else:
				st.info("Ausgewählte Marken: "+UnternehmenAuswahlAlsText)
		st.subheader("ø Messwerte:")
		
		#Zeile1 mit Kampagnen-Durchschnittswerten

		Kampagnenkolumne1, Kampagnenkolumne2, Kampagnenkolumne3, Kampagnenkolumne4, Kampagnenkolumne5 = st.columns(5)
		
		with Kampagnenkolumne1:
			MittelwertKampagneSympathisch = df_CampaignCheckAuswertungsSelektion['Werbebeurteilung - Gefällt mir'].mean()
			MittelwertKampagneSympathisch_Gerundet = "{:.1f}".format(MittelwertKampagneSympathisch) #Umwandlung Dezimalstelle 
			#st.write("Markenbekanntheit - Mittelwert: ", MittelwertKampagneSympathisch)
			MittelwertKampagneSympathisch_VergleichZuGesamtDB = MittelwertKampagneSympathisch-MittelwertKampagneSympathisch_Alle
			MittelwertKampagneSympathisch_VergleichZuGesamtDB_Gerundet = "{:.1f}".format(MittelwertKampagneSympathisch_VergleichZuGesamtDB)
			if MittelwertKampagneSympathisch_VergleichZuGesamtDB == 0.0:
				MittelwertKampagneSympathisch_VergleichZuGesamtDB_Gerundet = ""
		
			st.metric("Kampagne sympathisch (1-7)" , value=MittelwertKampagneSympathisch_Gerundet, delta=MittelwertKampagneSympathisch_VergleichZuGesamtDB_Gerundet)
		
		
		
		with Kampagnenkolumne2:
			MittelwertKampagneBesonders = df_CampaignCheckAuswertungsSelektion['Werbebeurteilung - Ist etwas Besonderes'].mean()
			MittelwertKampagneBesonders_Gerundet = "{:.1f}".format(MittelwertKampagneBesonders) #Umwandlung Dezimalstelle 
			#st.write("Markenbekanntheit - Mittelwert: ", MittelwertKampagneBesonders)
			MittelwertKampagneBesonders_VergleichZuGesamtDB = MittelwertKampagneBesonders-MittelwertKampagneBesonders_Alle
			MittelwertKampagneBesonders_VergleichZuGesamtDB_Gerundet = "{:.1f}".format(MittelwertKampagneBesonders_VergleichZuGesamtDB)
			if MittelwertKampagneBesonders_VergleichZuGesamtDB == 0.0:
				MittelwertKampagneBesonders_VergleichZuGesamtDB_Gerundet = ""
		
			st.metric("Kampagne besonders (1-7)" , value=MittelwertKampagneBesonders_Gerundet, delta=MittelwertKampagneBesonders_VergleichZuGesamtDB_Gerundet)
		
		
		with Kampagnenkolumne3:
			MittelwertKampagneKaufreiz = df_CampaignCheckAuswertungsSelektion['Werbebeurteilung - Reizt mich, mehr zu erfahren'].mean()
			MittelwertKampagneKaufreiz_Gerundet = "{:.1f}".format(MittelwertKampagneKaufreiz) #Umwandlung Dezimalstelle 
			#st.write("Markenbekanntheit - Mittelwert: ", MittelwertKampagneKaufreiz)
			MittelwertKampagneKaufreiz_VergleichZuGesamtDB = MittelwertKampagneKaufreiz-MittelwertKampagneKaufreiz_Alle
			MittelwertKampagneKaufreiz_VergleichZuGesamtDB_Gerundet = "{:.1f}".format(MittelwertKampagneKaufreiz_VergleichZuGesamtDB)
			if MittelwertKampagneKaufreiz_VergleichZuGesamtDB == 0.0:
				MittelwertKampagneKaufreiz_VergleichZuGesamtDB_Gerundet = ""
		
			st.metric("Kampagne kaufreiz (1-7)" , value=MittelwertKampagneKaufreiz_Gerundet, delta=MittelwertKampagneKaufreiz_VergleichZuGesamtDB_Gerundet)
		
		
		
		with Kampagnenkolumne4:
			MittelwertKampagneVerständlich = df_CampaignCheckAuswertungsSelektion['Werbebeurteilung - Ist verständlich'].mean()
			MittelwertKampagneVerständlich_Gerundet = "{:.1f}".format(MittelwertKampagneVerständlich) #Umwandlung Dezimalstelle 
			#st.write("Markenbekanntheit - Mittelwert: ", MittelwertKampagneVerständlich)
			MittelwertKampagneVerständlich_VergleichZuGesamtDB = MittelwertKampagneVerständlich-MittelwertKampagneVerständlich_Alle
			MittelwertKampagneVerständlich_VergleichZuGesamtDB_Gerundet = "{:.1f}".format(MittelwertKampagneVerständlich_VergleichZuGesamtDB)
			if MittelwertKampagneVerständlich_VergleichZuGesamtDB == 0.0:
				MittelwertKampagneVerständlich_VergleichZuGesamtDB_Gerundet = ""
		
			st.metric("Kampagne verständlich (1-7)" , value=MittelwertKampagneVerständlich_Gerundet, delta=MittelwertKampagneVerständlich_VergleichZuGesamtDB_Gerundet)
		
		with Kampagnenkolumne5:
			MittelwertKampagneGlaubwürdig = df_CampaignCheckAuswertungsSelektion['Werbebeurteilung - Ist glaubwürdig'].mean()
			MittelwertKampagneGlaubwürdig_Gerundet = "{:.1f}".format(MittelwertKampagneGlaubwürdig) #Umwandlung Dezimalstelle 
			#st.write("Markenbekanntheit - Mittelwert: ", MittelwertKampagneGlaubwürdig)
			MittelwertKampagneGlaubwürdig_VergleichZuGesamtDB = MittelwertKampagneGlaubwürdig-MittelwertKampagneGlaubwürdig_Alle
			MittelwertKampagneGlaubwürdig_VergleichZuGesamtDB_Gerundet = "{:.1f}".format(MittelwertKampagneGlaubwürdig_VergleichZuGesamtDB)
			if MittelwertKampagneGlaubwürdig_VergleichZuGesamtDB == 0.0:
				MittelwertKampagneGlaubwürdig_VergleichZuGesamtDB_Gerundet = ""
		
			st.metric("Kampagne glaubwürdig (1-7)" , value=MittelwertKampagneGlaubwürdig_Gerundet, delta=MittelwertKampagneGlaubwürdig_VergleichZuGesamtDB_Gerundet)
		
		
	

		
		
		#Zeile2 mit Kampagnen-Durchschnittswerten

		Kampagnenkolumne2_1, Kampagnenkolumne2_2, Kampagnenkolumne2_3 = st.columns(3)
		
		with Kampagnenkolumne2_1:
			MittelwertKampagneRecognition = df_CampaignCheckAuswertungsSelektion['Recognition_Wert'].mean()
			MittelwertKampagneRecognition_Gerundet = "{:.1f}".format(MittelwertKampagneRecognition) #Umwandlung Dezimalstelle 
			#st.write("Markenbekanntheit - Mittelwert: ", MittelwertKampagneRecognition)
			MittelwertKampagneRecognition_VergleichZuGesamtDB = MittelwertKampagneRecognition-MittelwertKampagneRecognition_Alle
			MittelwertKampagneRecognition_VergleichZuGesamtDB_Gerundet = "{:.1f}".format(MittelwertKampagneRecognition_VergleichZuGesamtDB)
			if MittelwertKampagneRecognition_VergleichZuGesamtDB == 0.0:
				MittelwertKampagneRecognition_VergleichZuGesamtDB_Gerundet = ""
		
			st.metric("Kampagne Recognition (0-100 %)" , value=MittelwertKampagneRecognition_Gerundet +"%", delta=MittelwertKampagneRecognition_VergleichZuGesamtDB_Gerundet)

		
		with Kampagnenkolumne2_2:
			MittelwertKampagneKaufKDAOutcome = df_CampaignCheckAuswertungsSelektion['Kauf (KDA Outcome)'].mean()
			MittelwertKampagneKaufKDAOutcome_Gerundet = "{:.1f}".format(MittelwertKampagneKaufKDAOutcome) #Umwandlung Dezimalstelle 
			#st.write("Markenbekanntheit - Mittelwert: ", MittelwertKampagneKaufKDAOutcome)
			MittelwertKampagneKaufKDAOutcome_VergleichZuGesamtDB = MittelwertKampagneKaufKDAOutcome-MittelwertKampagneKaufKDAOutcome_Alle
			MittelwertKampagneKaufKDAOutcome_VergleichZuGesamtDB_Gerundet = "{:.1f}".format(MittelwertKampagneKaufKDAOutcome_VergleichZuGesamtDB)
			if MittelwertKampagneKaufKDAOutcome_VergleichZuGesamtDB == 0.0:
				MittelwertKampagneKaufKDAOutcome_VergleichZuGesamtDB_Gerundet = ""
			if MittelwertKampagneKaufKDAOutcome > 0:
				st.metric("Kauf KDA (1-7)" , value=MittelwertKampagneKaufKDAOutcome_Gerundet, delta=MittelwertKampagneKaufKDAOutcome_VergleichZuGesamtDB_Gerundet)
		
		with Kampagnenkolumne2_3:
			MittelwertKampagneNPS = df_CampaignCheckAuswertungsSelektion['NPS'].mean()
			MittelwertKampagneNPS_Gerundet = "{:.1f}".format(MittelwertKampagneNPS) #Umwandlung Dezimalstelle 
			#st.write("Markenbekanntheit - Mittelwert: ", MittelwertKampagneNPS)
			MittelwertKampagneNPS_VergleichZuGesamtDB = MittelwertKampagneNPS-MittelwertKampagneNPS_Alle
			MittelwertKampagneNPS_VergleichZuGesamtDB_Gerundet = "{:.1f}".format(MittelwertKampagneNPS_VergleichZuGesamtDB)
			if MittelwertKampagneNPS_VergleichZuGesamtDB == 0.0:
				MittelwertKampagneNPS_VergleichZuGesamtDB_Gerundet = ""
			if MittelwertKampagneNPS > 0:
				st.metric("NPS (0-10)" , value=MittelwertKampagneNPS_Gerundet, delta=MittelwertKampagneNPS_VergleichZuGesamtDB_Gerundet)		
		
	
		if (MittelwertKampagneRecognition_VergleichZuGesamtDB + MittelwertKampagneKaufreiz_VergleichZuGesamtDB) != 0.0:
			st.caption ("Werte in Grün/Rot hinter den Pfeilen zeigen hier die absolute Differenz zum Mittelwert in der Gesamtbefragung")	
		
		
		#Abbildungen zur Kampagnenauswertung ###############################################################
		
		
		#Recognition Pie-Chart ################3
		#Erst nur Auswahl interessanten Spalten
		df_Recognition = df_CampaignCheckAuswertungsSelektion [['Recognition']]
		#st.write(df_Recognition)
		df_RecognitionAnzahl = df_Recognition['Recognition'].value_counts()
		df_RecognitionAnzahl = df_RecognitionAnzahl.reset_index(level=0)
		df_RecognitionAnzahl['Antwort'] = df_RecognitionAnzahl['index']
		#st.write(df_RecognitionAnzahl)
			
		#df_UG_Geschlecht_Glaubwürdig = df_UG_Geschlecht_Glaubwürdig.reset_index(level=0)
		#df_UG_Geschlecht_Glaubwürdig['Geschlecht'] = df_UG_Geschlecht_Glaubwürdig.index
		#st.write(df_UG_Geschlecht_Glaubwürdig)
		
		with Kampagnenkolumne2_1:
			RecognitionChart = px.pie(df_RecognitionAnzahl,values='Recognition',names='Antwort', 
			title='Recognition', 
			hole = 0.4, 
			color='Antwort',
			color_discrete_map={'Ja' : FARBE_Maxwert ,'Nein' : FARBE_Minwert ,'Weiss nicht' : FARBE_Mittelwert},
			hover_name = 'Antwort',
			#hover_data=['Recognition'], #kan visa all info i dataframen
			labels={'Recognition':"Anzahl Nennungen ",'Antwort' : "Antwort" }
			)
			RecognitionChart.update_traces(textposition='inside', 
			marker=dict(line=dict(color='#FFFFFF',width=2)), #fixar ramar kring kakbitarna
			textinfo='percent+label')
			RecognitionChart.update_layout(showlegend=False)
			RecognitionChart.update_layout(width=350,height=350)
			
			st.plotly_chart(RecognitionChart)
		
		
		#Kauf (KDA Outcome) Pie-Chart ##################
		#Erst nur Auswahl interessanten Spalten
		df_Kauf_KDA_Outcome = df_CampaignCheckAuswertungsSelektion [['Kauf (KDA Outcome)']]
		#st.write(df_Kauf (KDA Outcome))
		df_Kauf_KDA_OutcomeAnzahl = df_Kauf_KDA_Outcome['Kauf (KDA Outcome)'].value_counts()
		df_Kauf_KDA_OutcomeAnzahl = df_Kauf_KDA_OutcomeAnzahl.reset_index(level=0)
		df_Kauf_KDA_OutcomeAnzahl['Antwort'] = df_Kauf_KDA_OutcomeAnzahl['index']
		df_Kauf_KDA_OutcomeAnzahl_sortiert = df_Kauf_KDA_OutcomeAnzahl.sort_values(by=['Antwort'], ascending=False)
		#st.write(df_Kauf_KDA_OutcomeAnzahl_sortiert)
			
		
		with Kampagnenkolumne2_2:
			Kauf_KDA_OutcomeChart = px.pie(df_Kauf_KDA_OutcomeAnzahl_sortiert,values='Kauf (KDA Outcome)',names='Antwort', 
			title='Kauf (KDA Outcome)',
			hole = 0.4, 
			color='Antwort',
			color_discrete_sequence=px.colors.sequential.Inferno,
			hover_name = 'Antwort',
			#hover_data=['Kauf (KDA Outcome)'], #kan visa all info i dataframen
			labels={'Kauf (KDA Outcome)':"Anzahl Nennungen ",'Antwort' : "Antwort" }
			)
			Kauf_KDA_OutcomeChart.update_traces(textposition='inside', 
			marker=dict(line=dict(color='#FFFFFF',width=2)), #fixar ramar kring kakbitarna
			textinfo='percent+label')
			Kauf_KDA_OutcomeChart.update_layout(showlegend=False)
			Kauf_KDA_OutcomeChart.update_layout(width=350,height=350)
			Kauf_KDA_OutcomeChart.update_traces(sort=False) #Slices nicht sortieren
			if MittelwertKampagneKaufKDAOutcome > 0:
				st.plotly_chart(Kauf_KDA_OutcomeChart)
		
		
		#NPS Pie-Chart ##################
		#Erst nur Auswahl interessanten Spalten
		df_NPS = df_CampaignCheckAuswertungsSelektion [['NPS']]
		#st.write(df_NPS)
		df_NPSAnzahl = df_NPS['NPS'].value_counts()
		df_NPSAnzahl = df_NPSAnzahl.reset_index(level=0)
		df_NPSAnzahl['Antwort'] = df_NPSAnzahl['index']
		df_NPSAnzahl_sortiert = df_NPSAnzahl.sort_values(by=['Antwort'], ascending=False)
		#st.write(df_NPSAnzahl_sortiert)
			
		
		with Kampagnenkolumne2_3:
			NPS_Chart = px.pie(df_NPSAnzahl_sortiert,values='NPS',names='Antwort', 
			title='NPS',
			hole = 0.4, 
			color='Antwort',
			color_discrete_sequence=px.colors.sequential.Inferno,
			hover_name = 'Antwort',
			#hover_data=['NPS'], #kan visa all info i dataframen
			labels={'NPS':"Anzahl Nennungen ",'Antwort' : "Antwort" }
			)
			NPS_Chart.update_traces(textposition='inside', 
			marker=dict(line=dict(color='#FFFFFF',width=2)), #fixar ramar kring kakbitarna
			textinfo='percent+label')
			NPS_Chart.update_layout(showlegend=False)
			NPS_Chart.update_layout(width=350,height=350)
			NPS_Chart.update_traces(sort=False) #Slices nicht sortieren
			if MittelwertKampagneNPS > 0:
				st.plotly_chart(NPS_Chart)
		
		
		
		
		#Abbildung - Recognition je Kampagne - Durchschnittswerte ******************************************************************************************************************
		
		n_RecognitionKampagne = df_CampaignCheckAuswertungsSelektion.groupby('Kampagne').agg({'Recognition_Wert':'mean'})['Recognition_Wert']
		

		
		anzahlKampagneGesamt = len(n_RecognitionKampagne)
		
		if anzahlKampagneGesamt > 1:
			st.subheader("")
			st.subheader("Recognition der Werbemittel (0-100%):")
		
			st.write("Anzahl Kampagnen zur Auswahl: ",anzahlKampagneGesamt)
		
			if anzahlKampagneGesamt > 10:
				minAnzahlKampagne = 10
			else:
				minAnzahlKampagne = anzahlKampagneGesamt
		
			if anzahlKampagneGesamt == 1:
				minAnzahlKampagne = 1
		
			top_RecognitionKampagne = st.slider('Wähle die Anzahl Kampagnen die angezeigt werden sollen:', min_value=0, max_value=anzahlKampagneGesamt, value=minAnzahlKampagne)
			top_n_RecognitionKampagne = df_CampaignCheckAuswertungsSelektion.groupby('Kampagne').agg({'Recognition_Wert':'mean'})['Recognition_Wert'].nlargest(top_RecognitionKampagne)
		
			anzahlKampagne = len(top_n_RecognitionKampagne)
		
			Abbildung_top_n_RecognitionKampagne = px.bar(top_n_RecognitionKampagne, 
			x=top_n_RecognitionKampagne.index, 
			y='Recognition_Wert',
			color='Recognition_Wert',
			#color_continuous_scale=px.colors.sequential.Blackbody,
			#color_continuous_scale=px.colors.sequential.Brwnyl,
			#color=top_n_RecognitionKampagne.index - unterschiedliche Farbe je Kampagne
			text='Recognition_Wert', #beschriftung auf Balken
			#hover_name='Recognition_Wert', #Beschriftungstextauswahl für Balken
			title=f'Recognition (0-100%) je Kampagne - Top ' + str(top_RecognitionKampagne),
			orientation='v', #braucht es hier eigentlich nicht
			#color_continuous_scale=[(0, FARBE_Minwert),(0.25, FARBE_Mittelwert), (0.5, FARBE_Mittelwert), (0.75, FARBE_Maxwert),(1, FARBE_Maxwert)]
			color_continuous_scale=[(0, FARBE_Minwert), (0.5, FARBE_Mittelwert), (1, FARBE_Maxwert)]
			#color_continuous_scale[color_continuous_scale[0]] = "black"
			
			)
			#Weitere Formatierungen der Abbildung
			Abbildung_top_n_RecognitionKampagne.update_traces(texttemplate='%{text:.1f}'+" %", textposition='inside')
			Abbildung_top_n_RecognitionKampagne.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
			Abbildung_top_n_RecognitionKampagne.update_yaxes(showline=True, linewidth=1, linecolor='white', gridcolor='black')
			

			
			#Horizontale Line mit Durchschnitt aller Messerwerte aus der DB
			Abbildung_top_n_RecognitionKampagne.add_hline(y=MittelwertRecognition_Alle, line_width=5, line_dash="dot", line_color="grey", opacity=0.6, annotation_text="ø Alle Messwerte", 
		              annotation_position="top left", annotation_font_size=16,
		              annotation_font_color="grey")
		
			if MittelwertKampagneRecognition_Alle != MittelwertKampagneRecognition:
				Abbildung_top_n_RecognitionKampagne.add_hline(y=MittelwertKampagneRecognition, line_width=2, line_dash="dot", line_color="white", opacity=0.8, annotation_text="ø Auswahl", 
		              annotation_position="top right")
		
		
			st.plotly_chart(Abbildung_top_n_RecognitionKampagne, use_container_width = True)
		
		#Ende Abbildung Recognition je Kampagne - Durschschnittswerte
		
		

	
		#Recognition Mittelwerte-  Abbildungen mit Splits nach Geschlecht - Branche und/oder Unternehmung gewählt ist #######################
		#if anzahlUnternehmen == 1 or anzahlBranchen == 1:
		#if my_UnternehmenSelect !=[] or my_BrancheSelect !=[]:
		if anzahlKampagneGesamt > 1:	
			RecognitionGesamtmittelExpander = st.expander("ø Recognition - nach Geschlecht, Alter, Sprache")
			with RecognitionGesamtmittelExpander:
				#Abbildung Recognition - nach Geschlecht ***
				RecognitionKampagne_Geschlecht = df_CampaignCheckAuswertungsSelektion.groupby('Geschlecht').agg({'Recognition_Wert':'mean'})['Recognition_Wert']
			
				Abbildung_RecognitionKampagne_Geschlecht = px.bar(RecognitionKampagne_Geschlecht, 
				x=RecognitionKampagne_Geschlecht.index, #in der Indexspalte steht das Geschlecht in den Zeilen
				y='Recognition_Wert',
				color=RecognitionKampagne_Geschlecht.index,
				color_discrete_map={'Frau' : FARBE_Frau ,'Mann' : FARBE_Mann},
				text='Recognition_Wert', #beschriftung auf Balken
				#hover_name='Recognition_Wert', #Beschriftungstextauswahl für Balken
				title=f'ø Recognition nach Geschlecht'
				)
				
				#Weitere Formatierungen der Abbildung
				Abbildung_RecognitionKampagne_Geschlecht.update_traces(texttemplate='%{text:.1f}'+" %", textposition='outside')
				Abbildung_RecognitionKampagne_Geschlecht.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
				Abbildung_RecognitionKampagne_Geschlecht.update_yaxes(showline=True, linewidth=1, linecolor='white', gridcolor='black')
				Abbildung_RecognitionKampagne_Geschlecht.update_layout(showlegend=False)
				
				st.plotly_chart(Abbildung_RecognitionKampagne_Geschlecht, use_container_width = True)
				#st.plotly_chart(Abbildung_RecognitionKampagne_Geschlecht, width=300)
			

				#Abbildung Recognition - nach Alter ***
				RecognitionKampagne_Alter = df_CampaignCheckAuswertungsSelektion.groupby('Alter').agg({'Recognition_Wert':'mean'})['Recognition_Wert']
			
				Abbildung_RecognitionKampagne_Alter = px.bar(RecognitionKampagne_Alter, 
				x=RecognitionKampagne_Alter.index, #in der Indexspalte steht das Alter in den Zeilen
				y='Recognition_Wert',
				color=RecognitionKampagne_Alter.index,
				color_discrete_map={'16-19' : FARBE_16_29 ,'20-24' : FARBE_16_29 ,'25-29' : FARBE_16_29 ,'30-34' : FARBE_30_49,'35-39' : FARBE_30_49,'40-44' : FARBE_30_49,'45-49' : FARBE_30_49,'50-54' : FARBE_50plus,'55-59' : FARBE_50plus,'60+' : FARBE_50plus},
				text='Recognition_Wert', #beschriftung auf Balken
				#hover_name='Recognition_Wert', #Beschriftungstextauswahl für Balken
				title=f'ø Recognition nach Alter'
				)
				
				#Weitere Formatierungen der Abbildung
				Abbildung_RecognitionKampagne_Alter.update_traces(texttemplate='%{text:.1f}'+" %", textposition='outside')
				Abbildung_RecognitionKampagne_Alter.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
				Abbildung_RecognitionKampagne_Alter.update_yaxes(showline=True, linewidth=1, linecolor='white', gridcolor='black')
				Abbildung_RecognitionKampagne_Alter.update_layout(showlegend=False)
				
				st.plotly_chart(Abbildung_RecognitionKampagne_Alter, use_container_width = True)
				#st.plotly_chart(Abbildung_RecognitionKampagne_Alter, width=500)
				
	
				#Abbildung Recognition - nach Sprache ***
				RecognitionKampagne_Sprache = df_CampaignCheckAuswertungsSelektion.groupby('Sprache').agg({'Recognition_Wert':'mean'})['Recognition_Wert']
			
				Abbildung_RecognitionKampagne_Sprache = px.bar(RecognitionKampagne_Sprache, 
				x=RecognitionKampagne_Sprache.index, #in der Indexspalte steht das Sprache in den Zeilen
				y='Recognition_Wert',
				color=RecognitionKampagne_Sprache.index,
				color_discrete_map={'Deutsch' : FARBE_Deutsch ,'Französisch' : FARBE_Französisch},
				text='Recognition_Wert', #beschriftung auf Balken
				#hover_name='Recognition_Wert', #Beschriftungstextauswahl für Balken
				title=f'ø Recognition nach Sprache' 
				)
				
				#Weitere Formatierungen der Abbildung
				Abbildung_RecognitionKampagne_Sprache.update_traces(texttemplate='%{text:.1f}'+" %", textposition='outside')
				Abbildung_RecognitionKampagne_Sprache.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
				Abbildung_RecognitionKampagne_Sprache.update_yaxes(showline=True, linewidth=1, linecolor='white', gridcolor='black')
				Abbildung_RecognitionKampagne_Sprache.update_layout(showlegend=False)
				
				st.plotly_chart(Abbildung_RecognitionKampagne_Sprache, use_container_width = True)
				#st.plotly_chart(Abbildung_RecognitionKampagne_Sprache, width=300)
		


		#Abbildungen - Gefallen je Kampagne - Durchschnittswerte ******************************************************************************************************************
		
		n_GefallenKampagne = df_CampaignCheckAuswertungsSelektion.groupby('Kampagne').agg({'Werbebeurteilung - Gefällt mir':'mean'})['Werbebeurteilung - Gefällt mir']
		

		
		anzahlKampagneGesamt = len(n_GefallenKampagne)
		
		if anzahlKampagneGesamt > 1:
			st.subheader("")
			st.subheader("Gefallen/Sympathie der Werbemittel (1-7):")
		
			st.write("Anzahl Kampagnen zur Auswahl: ",anzahlKampagneGesamt)
		
			if anzahlKampagneGesamt > 10:
				minAnzahlKampagne = 10
			else:
				minAnzahlKampagne = anzahlKampagneGesamt
		
			if anzahlKampagneGesamt == 1:
				minAnzahlKampagne = 1
		
			top_GefallenKampagne = st.slider('Wähle die Anzahl Kampagnen aus:', min_value=0, max_value=anzahlKampagneGesamt, value=minAnzahlKampagne)
			top_n_GefallenKampagne = df_CampaignCheckAuswertungsSelektion.groupby('Kampagne').agg({'Werbebeurteilung - Gefällt mir':'mean'})['Werbebeurteilung - Gefällt mir'].nlargest(top_GefallenKampagne)
		
			anzahlKampagne = len(top_n_GefallenKampagne)
		
			Abbildung_top_n_GefallenKampagne = px.bar(top_n_GefallenKampagne, 
			x=top_n_GefallenKampagne.index, 
			y='Werbebeurteilung - Gefällt mir',
			color='Werbebeurteilung - Gefällt mir',
			#color_continuous_scale=px.colors.sequential.Blackbody,
			#color_continuous_scale=px.colors.sequential.Brwnyl,
			#color=top_n_GefallenKampagne.index - unterschiedliche Farbe je Kampagne
			text='Werbebeurteilung - Gefällt mir', #beschriftung auf Balken
			#hover_name='Werbebeurteilung - Gefällt mir', #Beschriftungstextauswahl für Balken
			title=f'Gefallen (1-7) je Kampagne - Top ' + str(top_GefallenKampagne),
			orientation='v', #braucht es hier eigentlich nicht
			#color_continuous_scale=[(0, FARBE_Minwert),(0.25, FARBE_Mittelwert), (0.5, FARBE_Mittelwert), (0.75, FARBE_Maxwert),(1, FARBE_Maxwert)]
			color_continuous_scale=[(0, FARBE_Minwert), (0.5, FARBE_Mittelwert), (1, FARBE_Maxwert)]
			#color_continuous_scale[color_continuous_scale[0]] = "black"
			
			)
			#Weitere Formatierungen der Abbildung
			Abbildung_top_n_GefallenKampagne.update_traces(texttemplate='%{text:.1f}', textposition='inside')
			Abbildung_top_n_GefallenKampagne.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
			Abbildung_top_n_GefallenKampagne.update_yaxes(showline=True, linewidth=1, linecolor='white', gridcolor='black')
			Abbildung_top_n_GefallenKampagne.update_yaxes(range=[1, 7])
			
			#Horizontale Line mit Durchschnitt aller Messerwerte aus der DB
			Abbildung_top_n_GefallenKampagne.add_hline(y=MittelwertKampagneGefallen_Alle, line_width=5, line_dash="dot", line_color="grey", opacity=0.6, annotation_text="ø Alle Messwerte", 
		              annotation_position="top left", annotation_font_size=16,
		              annotation_font_color="grey")
		
			if MittelwertKampagneGefallen_Alle != MittelwertKampagneSympathisch:
				Abbildung_top_n_GefallenKampagne.add_hline(y=MittelwertKampagneSympathisch, line_width=2, line_dash="dot", line_color="white", opacity=0.8, annotation_text="ø Auswahl", 
		              annotation_position="top right")
		
		
			st.plotly_chart(Abbildung_top_n_GefallenKampagne, use_container_width = True)
			

		# Abbildungen zu Werbebeurteilung der Kampagnen nach Soziodemographie- Gefällt mir #################################
		
		#if anzahlUnternehmen == 1 or anzahlBranchen == 1:
		if my_UnternehmenSelect !=[] or my_BrancheSelect !=[]:
		
			GefallenExpander = st.expander ('Gefallen - Breaks nach Soziodemographie')
			with GefallenExpander:
		
		
		
				st.subheader("")
				st.subheader("Gefallen (1-7) nach Soziodemographie:")
			
				#Grouped Bar Chart - Kampagne- Geschlecht - Kampagne gefallen #############
				#st.write("Auswahl von interessanten Spalten")
				#Erst nur Auswahl interessanten Spalten
				df_Test_Kampagne_Geschlecht = df_CampaignCheckAuswertungsSelektion [['Kampagne','Geschlecht', 'Werbebeurteilung - Gefällt mir']]
				#st.write(df_Test_Kampagne_Geschlecht)
				
				
				#st.write("hejhopp, här blir det nästan en longform-variant visst tror jag:")
				#st.write("Für altair wird  die longform-data bevorzugt.. umstellung kann mit melt gemacht werden")
				df_Kampagne_Geschlecht_Gefallen = df_Test_Kampagne_Geschlecht.groupby(['Kampagne', 'Geschlecht']).mean('Werbebeurteilung - Gefällt mir')#['Werbebeurteilung - Gefällt mir'].nlargest(10)
					
				df_Kampagne_Geschlecht_Gefallen = df_Kampagne_Geschlecht_Gefallen.reset_index(level=0)
				df_Kampagne_Geschlecht_Gefallen['Geschlecht'] = df_Kampagne_Geschlecht_Gefallen.index
				#st.write(df_Kampagne_Geschlecht_Gefallen)
				
					
				#Ploly-Variante #########
				Abb_gefallen_Kampagne_Geschlecht = px.bar(df_Kampagne_Geschlecht_Gefallen, 
				x="Kampagne",
				#y="Kampagne",  
				y="Werbebeurteilung - Gefällt mir",
				#x="Werbebeurteilung - Gefällt mir",
				color="Geschlecht",
				color_discrete_map={'Frau' : FARBE_Frau ,'Mann' : FARBE_Mann},
				text='Werbebeurteilung - Gefällt mir', #beschriftung auf Balken
				hover_name='Kampagne', #Beschriftungstextauswahl für Balken 
				title=f'Werbebeurteilung je Kampagne- Gefällt mir (1-7) - nach Geschlecht ',
				orientation='v', #braucht es hier eigentlich nicht
				hover_data=['Werbebeurteilung - Gefällt mir'],
				barmode = 'group')
				
				#Weitere Formatierungen der Abbildung
				Abb_gefallen_Kampagne_Geschlecht.update_traces(texttemplate='%{text:.2f}', textposition='inside')
				Abb_gefallen_Kampagne_Geschlecht.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
				Abb_gefallen_Kampagne_Geschlecht.update_yaxes(showline=True, linewidth=1, linecolor='white', gridcolor='black')
				Abb_gefallen_Kampagne_Geschlecht.update_yaxes(range=[1, 7])
				#Abb_gefallen_Kampagne_Geschlecht.update_xaxes(range=[1, 7])
				
				st.plotly_chart(Abb_gefallen_Kampagne_Geschlecht, use_container_width = True)
	
			

			
				#Grouped Bar Chart - Kampagne- Altersklasse - Kampagne gefallen #############
				#st.write("Auswahl von interessanten Spalten")
				#Erst nur Auswahl interessanten Spalten
				df_Test_Kampagne_Altersklasse = df_CampaignCheckAuswertungsSelektion [['Kampagne','Altersklasse', 'Werbebeurteilung - Gefällt mir']]
				#st.write(df_Test_Kampagne_Altersklasse)
				
				
				#st.write("hejhopp, här blir det nästan en longform-variant visst tror jag:")
				#st.write("Für altair wird  die longform-data bevorzugt.. umstellung kann mit melt gemacht werden")
				df_Kampagne_Altersklasse_Gefallen = df_Test_Kampagne_Altersklasse.groupby(['Kampagne', 'Altersklasse']).mean('Werbebeurteilung - Gefällt mir')#['Werbebeurteilung - Gefällt mir'].nlargest(10)
					
				df_Kampagne_Altersklasse_Gefallen = df_Kampagne_Altersklasse_Gefallen.reset_index(level=0)
				df_Kampagne_Altersklasse_Gefallen['Altersklasse'] = df_Kampagne_Altersklasse_Gefallen.index
				#st.write(df_Kampagne_Altersklasse_Gefallen)
				
					
				#Ploly-Variante #########
				Abb_gefallen_Kampagne_Altersklasse = px.bar(df_Kampagne_Altersklasse_Gefallen, 
				x="Kampagne",
				#y="Kampagne",  
				y="Werbebeurteilung - Gefällt mir",
				#x="Werbebeurteilung - Gefällt mir",
				color="Altersklasse",
				color_discrete_map={'16-29' : FARBE_16_29 ,'30-49' : FARBE_30_49,'50+' : FARBE_50plus},
				text='Werbebeurteilung - Gefällt mir', #beschriftung auf Balken
				hover_name='Kampagne', #Beschriftungstextauswahl für Balken 
				title=f'Werbebeurteilung - Gefällt mir (1-7) - nach Altersklasse ',
				orientation='v', #braucht es hier eigentlich nicht
				hover_data=['Werbebeurteilung - Gefällt mir'],
				barmode = 'group')
				
				#Weitere Formatierungen der Abbildung
				Abb_gefallen_Kampagne_Altersklasse.update_traces(texttemplate='%{text:.2f}', textposition='inside')
				Abb_gefallen_Kampagne_Altersklasse.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
				Abb_gefallen_Kampagne_Altersklasse.update_yaxes(showline=True, linewidth=1, linecolor='white', gridcolor='black')
				Abb_gefallen_Kampagne_Altersklasse.update_yaxes(range=[1, 7])
				#Abb_gefallen_Kampagne_Altersklasse.update_xaxes(range=[1, 7])
				
				st.plotly_chart(Abb_gefallen_Kampagne_Altersklasse, use_container_width = True)
			
			

			
				#Grouped Bar Chart - Kampagne- Sprache- Kampagne gefallen #############
				#st.write("Auswahl von interessanten Spalten")
				#Erst nur Auswahl interessanten Spalten
				df_Test_Kampagne_Sprache= df_CampaignCheckAuswertungsSelektion [['Kampagne','Sprache', 'Werbebeurteilung - Gefällt mir']]
				#st.write(df_Test_Kampagne_Sprache)
				
				
				#st.write("hejhopp, här blir det nästan en longform-variant visst tror jag:")
				#st.write("Für altair wird  die longform-data bevorzugt.. umstellung kann mit melt gemacht werden")
				df_Kampagne_Sprache_Gefallen = df_Test_Kampagne_Sprache.groupby(['Kampagne', 'Sprache']).mean('Werbebeurteilung - Gefällt mir')#['Werbebeurteilung - Gefällt mir'].nlargest(10)
					
				df_Kampagne_Sprache_Gefallen = df_Kampagne_Sprache_Gefallen.reset_index(level=0)
				df_Kampagne_Sprache_Gefallen['Sprache'] = df_Kampagne_Sprache_Gefallen.index
				#st.write(df_Kampagne_Sprache_Gefallen)
				
					
				#Ploly-Variante #########
				Abb_gefallen_Kampagne_Sprache= px.bar(df_Kampagne_Sprache_Gefallen, 
				x="Kampagne",
				#y="Kampagne",  
				y="Werbebeurteilung - Gefällt mir",
				#x="Werbebeurteilung - Gefällt mir",
				color="Sprache",
				color_discrete_map={'Deutsch' : FARBE_Deutsch ,'Französisch' : FARBE_Französisch},
				text='Werbebeurteilung - Gefällt mir', #beschriftung auf Balken
				hover_name='Kampagne', #Beschriftungstextauswahl für Balken 
				title=f'Werbebeurteilung - Gefällt mir (1-7) - nach Sprache',
				orientation='v', #braucht es hier eigentlich nicht
				hover_data=['Werbebeurteilung - Gefällt mir'],
				barmode = 'group')
				
				#Weitere Formatierungen der Abbildung
				Abb_gefallen_Kampagne_Sprache.update_traces(texttemplate='%{text:.2f}', textposition='inside')
				Abb_gefallen_Kampagne_Sprache.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
				Abb_gefallen_Kampagne_Sprache.update_yaxes(showline=True, linewidth=1, linecolor='white', gridcolor='black')
				Abb_gefallen_Kampagne_Sprache.update_yaxes(range=[1, 7])
				#Abb_gefallen_Kampagne_Sprache.update_xaxes(range=[1, 7])
				
				st.plotly_chart(Abb_gefallen_Kampagne_Sprache, use_container_width = True)
		

		
		######## Ende Abbildungen zu Werbebeurteilung - Gefällt mir  ####################


		#Abbildungen - Ist etwas Besonderes je Kampagne - Durchschnittswerte ******************************************************************************************************************
		
		n_BesondersKampagne = df_CampaignCheckAuswertungsSelektion.groupby('Kampagne').agg({'Werbebeurteilung - Ist etwas Besonderes':'mean'})['Werbebeurteilung - Ist etwas Besonderes']
		

		
		anzahlKampagneGesamt = len(n_BesondersKampagne)
		
		if anzahlKampagneGesamt > 1:
			st.subheader("")
			st.subheader("Werbemittel besonders(1-7):")
		
			st.write("Anzahl Kampagnen zur Auswahl: ",anzahlKampagneGesamt)
		
			if anzahlKampagneGesamt > 10:
				minAnzahlKampagne = 10
			else:
				minAnzahlKampagne = anzahlKampagneGesamt
		
			if anzahlKampagneGesamt == 1:
				minAnzahlKampagne = 1
		
			top_BesondersKampagne = st.slider('Wähle Anzahl Kampagnen aus:', min_value=0, max_value=anzahlKampagneGesamt, value=minAnzahlKampagne)
			top_n_BesondersKampagne = df_CampaignCheckAuswertungsSelektion.groupby('Kampagne').agg({'Werbebeurteilung - Ist etwas Besonderes':'mean'})['Werbebeurteilung - Ist etwas Besonderes'].nlargest(top_BesondersKampagne)
		
			anzahlKampagne = len(top_n_BesondersKampagne)
		
			Abbildung_top_n_BesondersKampagne = px.bar(top_n_BesondersKampagne, 
			x=top_n_BesondersKampagne.index, 
			y='Werbebeurteilung - Ist etwas Besonderes',
			color='Werbebeurteilung - Ist etwas Besonderes',
			#color_continuous_scale=px.colors.sequential.Blackbody,
			#color_continuous_scale=px.colors.sequential.Brwnyl,
			#color=top_n_BesondersKampagne.index - unterschiedliche Farbe je Kampagne
			text='Werbebeurteilung - Ist etwas Besonderes', #beschriftung auf Balken
			#hover_name='Werbebeurteilung - Ist etwas Besonderes', #Beschriftungstextauswahl für Balken
			title=f'Besonders (1-7) je Kampagne - Top ' + str(top_BesondersKampagne),
			orientation='v', #braucht es hier eigentlich nicht
			#color_continuous_scale=[(0, FARBE_Minwert),(0.25, FARBE_Mittelwert), (0.5, FARBE_Mittelwert), (0.75, FARBE_Maxwert),(1, FARBE_Maxwert)]
			color_continuous_scale=[(0, FARBE_Minwert), (0.5, FARBE_Mittelwert), (1, FARBE_Maxwert)]
			#color_continuous_scale[color_continuous_scale[0]] = "black"
			
			)
			#Weitere Formatierungen der Abbildung
			Abbildung_top_n_BesondersKampagne.update_traces(texttemplate='%{text:.1f}', textposition='inside')
			Abbildung_top_n_BesondersKampagne.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
			Abbildung_top_n_BesondersKampagne.update_yaxes(showline=True, linewidth=1, linecolor='white', gridcolor='black')
			Abbildung_top_n_BesondersKampagne.update_yaxes(range=[1, 7])
			
			#Horizontale Line mit Durchschnitt aller Messerwerte aus der DB
			Abbildung_top_n_BesondersKampagne.add_hline(y=MittelwertKampagneBesonders_Alle, line_width=5, line_dash="dot", line_color="grey", opacity=0.6, annotation_text="ø Alle Messwerte", 
		              annotation_position="top left", annotation_font_size=16,
		              annotation_font_color="grey")
		
			if MittelwertKampagneBesonders_Alle != MittelwertKampagneBesonders:
				Abbildung_top_n_BesondersKampagne.add_hline(y=MittelwertKampagneBesonders, line_width=2, line_dash="dot", line_color="white", opacity=0.8, annotation_text="ø Auswahl", 
		              annotation_position="top right")
		
		
			st.plotly_chart(Abbildung_top_n_BesondersKampagne, use_container_width = True)
			

		# Abbildungen zu Werbebeurteilung der Kampagnen nach Soziodemographie- Ist etwas Besonderes (1-7) #################################
		
		#if anzahlUnternehmen == 1 or anzahlBranchen == 1:
		if my_UnternehmenSelect !=[] or my_BrancheSelect !=[]:
			BesondersExpander = st.expander ('Besonders - Breaks nach Soziodemographie')
			with BesondersExpander:
				st.subheader("")
				st.subheader("Ist etwas Besonderes (1-7) nach Soziodemographie:")
			
				#Grouped Bar Chart - Kampagne- Geschlecht - Kampagne gefallen #############
				#st.write("Auswahl von interessanten Spalten")
				#Erst nur Auswahl interessanten Spalten
				df_Test_Kampagne_Geschlecht = df_CampaignCheckAuswertungsSelektion [['Kampagne','Geschlecht', 'Werbebeurteilung - Ist etwas Besonderes']]
				#st.write(df_Test_Kampagne_Geschlecht)
				
				
				#st.write("hejhopp, här blir det nästan en longform-variant visst tror jag:")
				#st.write("Für altair wird  die longform-data bevorzugt.. umstellung kann mit melt gemacht werden")
				df_Kampagne_Geschlecht_Besonders = df_Test_Kampagne_Geschlecht.groupby(['Kampagne', 'Geschlecht']).mean('Werbebeurteilung - Ist etwas Besonderes')#['Werbebeurteilung - Ist etwas Besonderes'].nlargest(10)
					
				df_Kampagne_Geschlecht_Besonders = df_Kampagne_Geschlecht_Besonders.reset_index(level=0)
				df_Kampagne_Geschlecht_Besonders['Geschlecht'] = df_Kampagne_Geschlecht_Besonders.index
				#st.write(df_Kampagne_Geschlecht_Besonders)
				
					
				#Ploly-Variante #########
				Abb_gefallen_Kampagne_Geschlecht = px.bar(df_Kampagne_Geschlecht_Besonders, 
				x="Kampagne",
				#y="Kampagne",  
				y="Werbebeurteilung - Ist etwas Besonderes",
				#x="Werbebeurteilung - Ist etwas Besonderes",
				color="Geschlecht",
				color_discrete_map={'Frau' : FARBE_Frau ,'Mann' : FARBE_Mann},
				text='Werbebeurteilung - Ist etwas Besonderes', #beschriftung auf Balken
				hover_name='Kampagne', #Beschriftungstextauswahl für Balken 
				title=f'Werbebeurteilung - Ist etwas Besonderes (1-7)- nach Geschlecht ',
				orientation='v', #braucht es hier eigentlich nicht
				hover_data=['Werbebeurteilung - Ist etwas Besonderes'],
				barmode = 'group')
				
				#Weitere Formatierungen der Abbildung
				Abb_gefallen_Kampagne_Geschlecht.update_traces(texttemplate='%{text:.2f}', textposition='inside')
				Abb_gefallen_Kampagne_Geschlecht.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
				Abb_gefallen_Kampagne_Geschlecht.update_yaxes(showline=True, linewidth=1, linecolor='white', gridcolor='black')
				Abb_gefallen_Kampagne_Geschlecht.update_yaxes(range=[1, 7])
				#Abb_gefallen_Kampagne_Geschlecht.update_xaxes(range=[1, 7])
				
				st.plotly_chart(Abb_gefallen_Kampagne_Geschlecht, use_container_width = True)
	
			
			
			

			
				#Grouped Bar Chart - Kampagne- Altersklasse - Kampagne gefallen #############
				#st.write("Auswahl von interessanten Spalten")
				#Erst nur Auswahl interessanten Spalten
				df_Test_Kampagne_Altersklasse = df_CampaignCheckAuswertungsSelektion [['Kampagne','Altersklasse', 'Werbebeurteilung - Ist etwas Besonderes']]
				#st.write(df_Test_Kampagne_Altersklasse)
				
				
				#st.write("hejhopp, här blir det nästan en longform-variant visst tror jag:")
				#st.write("Für altair wird  die longform-data bevorzugt.. umstellung kann mit melt gemacht werden")
				df_Kampagne_Altersklasse_Besonders = df_Test_Kampagne_Altersklasse.groupby(['Kampagne', 'Altersklasse']).mean('Werbebeurteilung - Ist etwas Besonderes')#['Werbebeurteilung - Ist etwas Besonderes'].nlargest(10)
					
				df_Kampagne_Altersklasse_Besonders = df_Kampagne_Altersklasse_Besonders.reset_index(level=0)
				df_Kampagne_Altersklasse_Besonders['Altersklasse'] = df_Kampagne_Altersklasse_Besonders.index
				#st.write(df_Kampagne_Altersklasse_Besonders)
				
					
				#Ploly-Variante #########
				Abb_gefallen_Kampagne_Altersklasse = px.bar(df_Kampagne_Altersklasse_Besonders, 
				x="Kampagne",
				#y="Kampagne",  
				y="Werbebeurteilung - Ist etwas Besonderes",
				#x="Werbebeurteilung - Ist etwas Besonderes",
				color="Altersklasse",
				color_discrete_map={'16-29' : FARBE_16_29 ,'30-49' : FARBE_30_49,'50+' : FARBE_50plus},
				text='Werbebeurteilung - Ist etwas Besonderes', #beschriftung auf Balken
				hover_name='Kampagne', #Beschriftungstextauswahl für Balken 
				title=f'Werbebeurteilung - Ist etwas Besonderes (1-7) - nach Altersklasse ',
				orientation='v', #braucht es hier eigentlich nicht
				hover_data=['Werbebeurteilung - Ist etwas Besonderes'],
				barmode = 'group')
				
				#Weitere Formatierungen der Abbildung
				Abb_gefallen_Kampagne_Altersklasse.update_traces(texttemplate='%{text:.2f}', textposition='inside')
				Abb_gefallen_Kampagne_Altersklasse.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
				Abb_gefallen_Kampagne_Altersklasse.update_yaxes(showline=True, linewidth=1, linecolor='white', gridcolor='black')
				Abb_gefallen_Kampagne_Altersklasse.update_yaxes(range=[1, 7])
				#Abb_gefallen_Kampagne_Altersklasse.update_xaxes(range=[1, 7])
				
				st.plotly_chart(Abb_gefallen_Kampagne_Altersklasse, use_container_width = True)
			
			

			
				#Grouped Bar Chart - Kampagne- Sprache- Kampagne gefallen #############
				#st.write("Auswahl von interessanten Spalten")
				#Erst nur Auswahl interessanten Spalten
				df_Test_Kampagne_Sprache= df_CampaignCheckAuswertungsSelektion [['Kampagne','Sprache', 'Werbebeurteilung - Ist etwas Besonderes']]
				#st.write(df_Test_Kampagne_Sprache)
				
				
				#st.write("hejhopp, här blir det nästan en longform-variant visst tror jag:")
				#st.write("Für altair wird  die longform-data bevorzugt.. umstellung kann mit melt gemacht werden")
				df_Kampagne_Sprache_Besonders = df_Test_Kampagne_Sprache.groupby(['Kampagne', 'Sprache']).mean('Werbebeurteilung - Ist etwas Besonderes')#['Werbebeurteilung - Ist etwas Besonderes'].nlargest(10)
					
				df_Kampagne_Sprache_Besonders = df_Kampagne_Sprache_Besonders.reset_index(level=0)
				df_Kampagne_Sprache_Besonders['Sprache'] = df_Kampagne_Sprache_Besonders.index
				#st.write(df_Kampagne_Sprache_Besonders)
				
					
				#Ploly-Variante #########
				Abb_gefallen_Kampagne_Sprache= px.bar(df_Kampagne_Sprache_Besonders, 
				x="Kampagne",
				#y="Kampagne",  
				y="Werbebeurteilung - Ist etwas Besonderes",
				#x="Werbebeurteilung - Ist etwas Besonderes",
				color="Sprache",
				color_discrete_map={'Deutsch' : FARBE_Deutsch ,'Französisch' : FARBE_Französisch},
				text='Werbebeurteilung - Ist etwas Besonderes', #beschriftung auf Balken
				hover_name='Kampagne', #Beschriftungstextauswahl für Balken 
				title=f'Werbebeurteilung - Ist etwas Besonderes (1-7) - nach Sprache',
				orientation='v', #braucht es hier eigentlich nicht
				hover_data=['Werbebeurteilung - Ist etwas Besonderes'],
				barmode = 'group')
				
				#Weitere Formatierungen der Abbildung
				Abb_gefallen_Kampagne_Sprache.update_traces(texttemplate='%{text:.2f}', textposition='inside')
				Abb_gefallen_Kampagne_Sprache.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
				Abb_gefallen_Kampagne_Sprache.update_yaxes(showline=True, linewidth=1, linecolor='white', gridcolor='black')
				Abb_gefallen_Kampagne_Sprache.update_yaxes(range=[1, 7])
				#Abb_gefallen_Kampagne_Sprache.update_xaxes(range=[1, 7])
				
				st.plotly_chart(Abb_gefallen_Kampagne_Sprache, use_container_width = True)
		

		
		######## Ende Abbildungen zu Werbebeurteilung - Ist etwas Besonderes  ####################









	
	
	
	
	
	
	
		#Abbildungen - Glaubwürdigkeit je Kampagne - Durchschnittswerte ******************************************************************************************************************
		
		n_GlaubwürdigKampagne = df_CampaignCheckAuswertungsSelektion.groupby('Kampagne').agg({'Werbebeurteilung - Ist glaubwürdig':'mean'})['Werbebeurteilung - Ist glaubwürdig']
		

		
		anzahlKampagneGesamt = len(n_GlaubwürdigKampagne)
		
		if anzahlKampagneGesamt > 1:
			st.subheader("")
			st.subheader("Glaubwürdigkeit der Werbemittel (1-7):")
		
			st.write("Anzahl Kampagnen zur Auswahl: ",anzahlKampagneGesamt)
		
			if anzahlKampagneGesamt > 10:
				minAnzahlKampagne = 10
			else:
				minAnzahlKampagne = anzahlKampagneGesamt
		
			if anzahlKampagneGesamt == 1:
				minAnzahlKampagne = 1
		
			top_GlaubwürdigKampagne = st.slider('Wähle Anzahl Kampagnen:', min_value=0, max_value=anzahlKampagneGesamt, value=minAnzahlKampagne)
			top_n_GlaubwürdigKampagne = df_CampaignCheckAuswertungsSelektion.groupby('Kampagne').agg({'Werbebeurteilung - Ist glaubwürdig':'mean'})['Werbebeurteilung - Ist glaubwürdig'].nlargest(top_GlaubwürdigKampagne)
		
			anzahlKampagne = len(top_n_GlaubwürdigKampagne)
		
			Abbildung_top_n_GlaubwürdigKampagne = px.bar(top_n_GlaubwürdigKampagne, 
			x=top_n_GlaubwürdigKampagne.index, 
			y='Werbebeurteilung - Ist glaubwürdig',
			color='Werbebeurteilung - Ist glaubwürdig',
			#color_continuous_scale=px.colors.sequential.Blackbody,
			#color_continuous_scale=px.colors.sequential.Brwnyl,
			#color=top_n_GlaubwürdigKampagne.index - unterschiedliche Farbe je Kampagne
			text='Werbebeurteilung - Ist glaubwürdig', #beschriftung auf Balken
			#hover_name='Werbebeurteilung - Ist glaubwürdig', #Beschriftungstextauswahl für Balken
			title=f'Glaubwürdigkeit (1-7) je Kampagne - Top ' + str(top_GlaubwürdigKampagne),
			orientation='v', #braucht es hier eigentlich nicht
			#color_continuous_scale=[(0, FARBE_Minwert),(0.25, FARBE_Mittelwert), (0.5, FARBE_Mittelwert), (0.75, FARBE_Maxwert),(1, FARBE_Maxwert)]
			color_continuous_scale=[(0, FARBE_Minwert), (0.5, FARBE_Mittelwert), (1, FARBE_Maxwert)]
			#color_continuous_scale[color_continuous_scale[0]] = "black"
			
			)
			#Weitere Formatierungen der Abbildung
			Abbildung_top_n_GlaubwürdigKampagne.update_traces(texttemplate='%{text:.1f}', textposition='inside')
			Abbildung_top_n_GlaubwürdigKampagne.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
			Abbildung_top_n_GlaubwürdigKampagne.update_yaxes(showline=True, linewidth=1, linecolor='white', gridcolor='black')
			Abbildung_top_n_GlaubwürdigKampagne.update_yaxes(range=[1, 7])
			
			#Horizontale Line mit Durchschnitt aller Messerwerte aus der DB
			Abbildung_top_n_GlaubwürdigKampagne.add_hline(y=MittelwertKampagneGlaubwürdig_Alle, line_width=5, line_dash="dot", line_color="grey", opacity=0.6, annotation_text="ø Alle Messwerte", 
		              annotation_position="top left", annotation_font_size=16,
		              annotation_font_color="grey")
		
			if MittelwertKampagneGlaubwürdig_Alle != MittelwertKampagneGlaubwürdig:
				Abbildung_top_n_GlaubwürdigKampagne.add_hline(y=MittelwertKampagneGlaubwürdig, line_width=2, line_dash="dot", line_color="white", opacity=0.8, annotation_text="ø Auswahl", 
		              annotation_position="top right")
		
		
			st.plotly_chart(Abbildung_top_n_GlaubwürdigKampagne, use_container_width = True)
			

		# Abbildungen zu Werbebeurteilung der Kampagnen nach Soziodemographie- Ist glaubwürdig #################################
		
		#if anzahlUnternehmen == 1 or anzahlBranchen == 1:
		if my_UnternehmenSelect !=[] or my_BrancheSelect !=[]:
			
			GlaubwürdigExpander = st.expander ('Glaubwürdigkeit - Breaks nach Soziodemographie')
			with GlaubwürdigExpander:
			
				st.subheader("")
				st.subheader("Glaubwürdigkeit (1-7) nach Soziodemographie:")
			
				#Grouped Bar Chart - Kampagne- Geschlecht - Kampagne glaubwürdig #############
				#st.write("Auswahl von interessanten Spalten")
				#Erst nur Auswahl interessanten Spalten
				df_Test_Kampagne_Geschlecht = df_CampaignCheckAuswertungsSelektion [['Kampagne','Geschlecht', 'Werbebeurteilung - Ist glaubwürdig']]
				#st.write(df_Test_Kampagne_Geschlecht)
				
				
				#st.write("hejhopp, här blir det nästan en longform-variant visst tror jag:")
				#st.write("Für altair wird  die longform-data bevorzugt.. umstellung kann mit melt gemacht werden")
				df_Kampagne_Geschlecht_Glaubwürdig = df_Test_Kampagne_Geschlecht.groupby(['Kampagne', 'Geschlecht']).mean('Werbebeurteilung - Ist glaubwürdig')#['Werbebeurteilung - Ist glaubwürdig'].nlargest(10)
					
				df_Kampagne_Geschlecht_Glaubwürdig = df_Kampagne_Geschlecht_Glaubwürdig.reset_index(level=0)
				df_Kampagne_Geschlecht_Glaubwürdig['Geschlecht'] = df_Kampagne_Geschlecht_Glaubwürdig.index
				#st.write(df_Kampagne_Geschlecht_Glaubwürdig)
				
					
				#Ploly-Variante #########
				Abb_glaubwürdig_Kampagne_Geschlecht = px.bar(df_Kampagne_Geschlecht_Glaubwürdig, 
				x="Kampagne",
				#y="Kampagne",  
				y="Werbebeurteilung - Ist glaubwürdig",
				#x="Werbebeurteilung - Ist glaubwürdig",
				color="Geschlecht",
				color_discrete_map={'Frau' : FARBE_Frau ,'Mann' : FARBE_Mann},
				text='Werbebeurteilung - Ist glaubwürdig', #beschriftung auf Balken
				hover_name='Kampagne', #Beschriftungstextauswahl für Balken 
				title=f'Werbebeurteilung je Kampagne- Ist glaubwürdig (1-7) - nach Geschlecht ',
				orientation='v', #braucht es hier eigentlich nicht
				hover_data=['Werbebeurteilung - Ist glaubwürdig'],
				barmode = 'group')
				
				#Weitere Formatierungen der Abbildung
				Abb_glaubwürdig_Kampagne_Geschlecht.update_traces(texttemplate='%{text:.2f}', textposition='inside')
				Abb_glaubwürdig_Kampagne_Geschlecht.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
				Abb_glaubwürdig_Kampagne_Geschlecht.update_yaxes(showline=True, linewidth=1, linecolor='white', gridcolor='black')
				Abb_glaubwürdig_Kampagne_Geschlecht.update_yaxes(range=[1, 7])
				#Abb_glaubwürdig_Kampagne_Geschlecht.update_xaxes(range=[1, 7])
				
				st.plotly_chart(Abb_glaubwürdig_Kampagne_Geschlecht, use_container_width = True)
	
			
			
	
			
				#Grouped Bar Chart - Kampagne- Altersklasse - Kampagne glaubwürdig #############
				#st.write("Auswahl von interessanten Spalten")
				#Erst nur Auswahl interessanten Spalten
				df_Test_Kampagne_Altersklasse = df_CampaignCheckAuswertungsSelektion [['Kampagne','Altersklasse', 'Werbebeurteilung - Ist glaubwürdig']]
				#st.write(df_Test_Kampagne_Altersklasse)
				
				
				#st.write("hejhopp, här blir det nästan en longform-variant visst tror jag:")
				#st.write("Für altair wird  die longform-data bevorzugt.. umstellung kann mit melt gemacht werden")
				df_Kampagne_Altersklasse_Glaubwürdig = df_Test_Kampagne_Altersklasse.groupby(['Kampagne', 'Altersklasse']).mean('Werbebeurteilung - Ist glaubwürdig')#['Werbebeurteilung - Ist glaubwürdig'].nlargest(10)
					
				df_Kampagne_Altersklasse_Glaubwürdig = df_Kampagne_Altersklasse_Glaubwürdig.reset_index(level=0)
				df_Kampagne_Altersklasse_Glaubwürdig['Altersklasse'] = df_Kampagne_Altersklasse_Glaubwürdig.index
				#st.write(df_Kampagne_Altersklasse_Glaubwürdig)
				
					
				#Ploly-Variante #########
				Abb_glaubwürdig_Kampagne_Altersklasse = px.bar(df_Kampagne_Altersklasse_Glaubwürdig, 
				x="Kampagne",
				#y="Kampagne",  
				y="Werbebeurteilung - Ist glaubwürdig",
				#x="Werbebeurteilung - Ist glaubwürdig",
				color="Altersklasse",
				color_discrete_map={'16-29' : FARBE_16_29 ,'30-49' : FARBE_30_49,'50+' : FARBE_50plus},
				text='Werbebeurteilung - Ist glaubwürdig', #beschriftung auf Balken
				hover_name='Kampagne', #Beschriftungstextauswahl für Balken 
				title=f'Werbebeurteilung - Ist glaubwürdig (1-7) - nach Altersklasse ',
				orientation='v', #braucht es hier eigentlich nicht
				hover_data=['Werbebeurteilung - Ist glaubwürdig'],
				barmode = 'group')
				
				#Weitere Formatierungen der Abbildung
				Abb_glaubwürdig_Kampagne_Altersklasse.update_traces(texttemplate='%{text:.2f}', textposition='inside')
				Abb_glaubwürdig_Kampagne_Altersklasse.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
				Abb_glaubwürdig_Kampagne_Altersklasse.update_yaxes(showline=True, linewidth=1, linecolor='white', gridcolor='black')
				Abb_glaubwürdig_Kampagne_Altersklasse.update_yaxes(range=[1, 7])
				#Abb_glaubwürdig_Kampagne_Altersklasse.update_xaxes(range=[1, 7])
				
				st.plotly_chart(Abb_glaubwürdig_Kampagne_Altersklasse, use_container_width = True)
			
			
			
				#Grouped Bar Chart - Kampagne- Sprache- Kampagne glaubwürdig #############
				#st.write("Auswahl von interessanten Spalten")
				#Erst nur Auswahl interessanten Spalten
				df_Test_Kampagne_Sprache= df_CampaignCheckAuswertungsSelektion [['Kampagne','Sprache', 'Werbebeurteilung - Ist glaubwürdig']]
				#st.write(df_Test_Kampagne_Sprache)
				
				
				#st.write("hejhopp, här blir det nästan en longform-variant visst tror jag:")
				#st.write("Für altair wird  die longform-data bevorzugt.. umstellung kann mit melt gemacht werden")
				df_Kampagne_Sprache_Glaubwürdig = df_Test_Kampagne_Sprache.groupby(['Kampagne', 'Sprache']).mean('Werbebeurteilung - Ist glaubwürdig')#['Werbebeurteilung - Ist glaubwürdig'].nlargest(10)
					
				df_Kampagne_Sprache_Glaubwürdig = df_Kampagne_Sprache_Glaubwürdig.reset_index(level=0)
				df_Kampagne_Sprache_Glaubwürdig['Sprache'] = df_Kampagne_Sprache_Glaubwürdig.index
				#st.write(df_Kampagne_Sprache_Glaubwürdig)
				
					
				#Ploly-Variante #########
				Abb_glaubwürdig_Kampagne_Sprache= px.bar(df_Kampagne_Sprache_Glaubwürdig, 
				x="Kampagne",
				#y="Kampagne",  
				y="Werbebeurteilung - Ist glaubwürdig",
				#x="Werbebeurteilung - Ist glaubwürdig",
				color="Sprache",
				color_discrete_map={'Deutsch' : FARBE_Deutsch ,'Französisch' : FARBE_Französisch},
				text='Werbebeurteilung - Ist glaubwürdig', #beschriftung auf Balken
				hover_name='Kampagne', #Beschriftungstextauswahl für Balken 
				title=f'Werbebeurteilung - Ist glaubwürdig (1-7) - nach Sprache',
				orientation='v', #braucht es hier eigentlich nicht
				hover_data=['Werbebeurteilung - Ist glaubwürdig'],
				barmode = 'group')
				
				#Weitere Formatierungen der Abbildung
				Abb_glaubwürdig_Kampagne_Sprache.update_traces(texttemplate='%{text:.2f}', textposition='inside')
				Abb_glaubwürdig_Kampagne_Sprache.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
				Abb_glaubwürdig_Kampagne_Sprache.update_yaxes(showline=True, linewidth=1, linecolor='white', gridcolor='black')
				Abb_glaubwürdig_Kampagne_Sprache.update_yaxes(range=[1, 7])
				#Abb_glaubwürdig_Kampagne_Sprache.update_xaxes(range=[1, 7])
				
				st.plotly_chart(Abb_glaubwürdig_Kampagne_Sprache, use_container_width = True)
		

		
		######## Ende Abbildungen zu Werbebeurteilung - Ist glaubwürdig  ####################
		
		

		#Abbildungen - Kaufreiz je Kampagne - Durchschnittswerte ******************************************************************************************************************
		
		n_KaufreizKampagne = df_CampaignCheckAuswertungsSelektion.groupby('Kampagne').agg({'Werbebeurteilung - Reizt mich, mehr zu erfahren':'mean'})['Werbebeurteilung - Reizt mich, mehr zu erfahren']
		

		
		anzahlKampagneGesamt = len(n_KaufreizKampagne)
		
		if anzahlKampagneGesamt > 1:
			st.subheader("")
			st.subheader("Kaufreiz der Werbemittel (1-7):")
		
			st.write("Anzahl Kampagnen zur Auswahl: ",anzahlKampagneGesamt)
		
			if anzahlKampagneGesamt > 10:
				minAnzahlKampagne = 10
			else:
				minAnzahlKampagne = anzahlKampagneGesamt
		
			if anzahlKampagneGesamt == 1:
				minAnzahlKampagne = 1
		
			top_KaufreizKampagne = st.slider('Wähle Anzahl anzuzeigender Kampagnen:', min_value=0, max_value=anzahlKampagneGesamt, value=minAnzahlKampagne)
			top_n_KaufreizKampagne = df_CampaignCheckAuswertungsSelektion.groupby('Kampagne').agg({'Werbebeurteilung - Reizt mich, mehr zu erfahren':'mean'})['Werbebeurteilung - Reizt mich, mehr zu erfahren'].nlargest(top_KaufreizKampagne)
		
			anzahlKampagne = len(top_n_KaufreizKampagne)
		
			Abbildung_top_n_KaufreizKampagne = px.bar(top_n_KaufreizKampagne, 
			x=top_n_KaufreizKampagne.index, 
			y='Werbebeurteilung - Reizt mich, mehr zu erfahren',
			color='Werbebeurteilung - Reizt mich, mehr zu erfahren',
			#color_continuous_scale=px.colors.sequential.Blackbody,
			#color_continuous_scale=px.colors.sequential.Brwnyl,
			#color=top_n_KaufreizKampagne.index - unterschiedliche Farbe je Kampagne
			text='Werbebeurteilung - Reizt mich, mehr zu erfahren', #beschriftung auf Balken
			#hover_name='Werbebeurteilung - Reizt mich, mehr zu erfahren', #Beschriftungstextauswahl für Balken
			title=f'Kaufreiz(1-7) je Kampagne - Top ' + str(top_KaufreizKampagne),
			orientation='v', #braucht es hier eigentlich nicht
			#color_continuous_scale=[(0, FARBE_Minwert),(0.25, FARBE_Mittelwert), (0.5, FARBE_Mittelwert), (0.75, FARBE_Maxwert),(1, FARBE_Maxwert)]
			color_continuous_scale=[(0, FARBE_Minwert), (0.5, FARBE_Mittelwert), (1, FARBE_Maxwert)]
			#color_continuous_scale[color_continuous_scale[0]] = "black"
			
			)
			#Weitere Formatierungen der Abbildung
			Abbildung_top_n_KaufreizKampagne.update_traces(texttemplate='%{text:.1f}', textposition='inside')
			Abbildung_top_n_KaufreizKampagne.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
			Abbildung_top_n_KaufreizKampagne.update_yaxes(showline=True, linewidth=1, linecolor='white', gridcolor='black')
			Abbildung_top_n_KaufreizKampagne.update_yaxes(range=[1, 7])
			
			#Horizontale Line mit Durchschnitt aller Messerwerte aus der DB
			Abbildung_top_n_KaufreizKampagne.add_hline(y=MittelwertKampagneKaufreiz_Alle, line_width=5, line_dash="dot", line_color="grey", opacity=0.6, annotation_text="ø Alle Messwerte", 
		              annotation_position="top left", annotation_font_size=16,
		              annotation_font_color="grey")
		
			if MittelwertKampagneKaufreiz_Alle != MittelwertKampagneKaufreiz:
				Abbildung_top_n_KaufreizKampagne.add_hline(y=MittelwertKampagneKaufreiz, line_width=2, line_dash="dot", line_color="white", opacity=0.8, annotation_text="ø Auswahl", 
		              annotation_position="top right")
		
		
			st.plotly_chart(Abbildung_top_n_KaufreizKampagne, use_container_width = True)








		# Abbildungen zu Werbebeurteilung der Kampagnen nach Soziodemographie- Reizt mich, mehr zu erfahren (1-7) #################################
		
		#if anzahlUnternehmen == 1 or anzahlBranchen == 1:
		if my_UnternehmenSelect !=[] or my_BrancheSelect !=[]:
			KaufreizExpander = st.expander ('Kaufreiz/Interesse - Breaks nach Soziodemographie')
			with KaufreizExpander:
				st.subheader("")
				st.subheader("Reizt mich, mehr zu erfahren (1-7) nach Soziodemographie:")
			
				#Grouped Bar Chart - Kampagne- Geschlecht - Kampagne kaufreiz #############
				#st.write("Auswahl von interessanten Spalten")
				#Erst nur Auswahl interessanten Spalten
				df_Test_Kampagne_Geschlecht = df_CampaignCheckAuswertungsSelektion [['Kampagne','Geschlecht', 'Werbebeurteilung - Reizt mich, mehr zu erfahren']]
				#st.write(df_Test_Kampagne_Geschlecht)
				
				
				#st.write("hejhopp, här blir det nästan en longform-variant visst tror jag:")
				#st.write("Für altair wird  die longform-data bevorzugt.. umstellung kann mit melt gemacht werden")
				df_Kampagne_Geschlecht_Kaufreiz = df_Test_Kampagne_Geschlecht.groupby(['Kampagne', 'Geschlecht']).mean('Werbebeurteilung - Reizt mich, mehr zu erfahren')#['Werbebeurteilung - Reizt mich, mehr zu erfahren'].nlargest(10)
					
				df_Kampagne_Geschlecht_Kaufreiz = df_Kampagne_Geschlecht_Kaufreiz.reset_index(level=0)
				df_Kampagne_Geschlecht_Kaufreiz['Geschlecht'] = df_Kampagne_Geschlecht_Kaufreiz.index
				#st.write(df_Kampagne_Geschlecht_Kaufreiz)
				
					
				#Ploly-Variante #########
				Abb_kaufreiz_Kampagne_Geschlecht = px.bar(df_Kampagne_Geschlecht_Kaufreiz, 
				x="Kampagne",
				#y="Kampagne",  
				y="Werbebeurteilung - Reizt mich, mehr zu erfahren",
				#x="Werbebeurteilung - Reizt mich, mehr zu erfahren",
				color="Geschlecht",
				color_discrete_map={'Frau' : FARBE_Frau ,'Mann' : FARBE_Mann},
				text='Werbebeurteilung - Reizt mich, mehr zu erfahren', #beschriftung auf Balken
				hover_name='Kampagne', #Beschriftungstextauswahl für Balken 
				title=f'Werbebeurteilung - Reizt mich, mehr zu erfahren (1-7)- nach Geschlecht ',
				orientation='v', #braucht es hier eigentlich nicht
				hover_data=['Werbebeurteilung - Reizt mich, mehr zu erfahren'],
				barmode = 'group')
				
				#Weitere Formatierungen der Abbildung
				Abb_kaufreiz_Kampagne_Geschlecht.update_traces(texttemplate='%{text:.2f}', textposition='inside')
				Abb_kaufreiz_Kampagne_Geschlecht.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
				Abb_kaufreiz_Kampagne_Geschlecht.update_yaxes(showline=True, linewidth=1, linecolor='white', gridcolor='black')
				Abb_kaufreiz_Kampagne_Geschlecht.update_yaxes(range=[1, 7])
				#Abb_kaufreiz_Kampagne_Geschlecht.update_xaxes(range=[1, 7])
				
				st.plotly_chart(Abb_kaufreiz_Kampagne_Geschlecht, use_container_width = True)
	
			
			
			

			
				#Grouped Bar Chart - Kampagne- Altersklasse - Kampagne kaufreiz #############
				#st.write("Auswahl von interessanten Spalten")
				#Erst nur Auswahl interessanten Spalten
				df_Test_Kampagne_Altersklasse = df_CampaignCheckAuswertungsSelektion [['Kampagne','Altersklasse', 'Werbebeurteilung - Reizt mich, mehr zu erfahren']]
				#st.write(df_Test_Kampagne_Altersklasse)
				
				
				#st.write("hejhopp, här blir det nästan en longform-variant visst tror jag:")
				#st.write("Für altair wird  die longform-data bevorzugt.. umstellung kann mit melt gemacht werden")
				df_Kampagne_Altersklasse_Kaufreiz = df_Test_Kampagne_Altersklasse.groupby(['Kampagne', 'Altersklasse']).mean('Werbebeurteilung - Reizt mich, mehr zu erfahren')#['Werbebeurteilung - Reizt mich, mehr zu erfahren'].nlargest(10)
					
				df_Kampagne_Altersklasse_Kaufreiz = df_Kampagne_Altersklasse_Kaufreiz.reset_index(level=0)
				df_Kampagne_Altersklasse_Kaufreiz['Altersklasse'] = df_Kampagne_Altersklasse_Kaufreiz.index
				#st.write(df_Kampagne_Altersklasse_Kaufreiz)
				
					
				#Ploly-Variante #########
				Abb_kaufreiz_Kampagne_Altersklasse = px.bar(df_Kampagne_Altersklasse_Kaufreiz, 
				x="Kampagne",
				#y="Kampagne",  
				y="Werbebeurteilung - Reizt mich, mehr zu erfahren",
				#x="Werbebeurteilung - Reizt mich, mehr zu erfahren",
				color="Altersklasse",
				color_discrete_map={'16-29' : FARBE_16_29 ,'30-49' : FARBE_30_49,'50+' : FARBE_50plus},
				text='Werbebeurteilung - Reizt mich, mehr zu erfahren', #beschriftung auf Balken
				hover_name='Kampagne', #Beschriftungstextauswahl für Balken 
				title=f'Werbebeurteilung - Reizt mich, mehr zu erfahren (1-7) - nach Altersklasse ',
				orientation='v', #braucht es hier eigentlich nicht
				hover_data=['Werbebeurteilung - Reizt mich, mehr zu erfahren'],
				barmode = 'group')
				
				#Weitere Formatierungen der Abbildung
				Abb_kaufreiz_Kampagne_Altersklasse.update_traces(texttemplate='%{text:.2f}', textposition='inside')
				Abb_kaufreiz_Kampagne_Altersklasse.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
				Abb_kaufreiz_Kampagne_Altersklasse.update_yaxes(showline=True, linewidth=1, linecolor='white', gridcolor='black')
				Abb_kaufreiz_Kampagne_Altersklasse.update_yaxes(range=[1, 7])
				#Abb_kaufreiz_Kampagne_Altersklasse.update_xaxes(range=[1, 7])
				
				st.plotly_chart(Abb_kaufreiz_Kampagne_Altersklasse, use_container_width = True)
			
			

			
				#Grouped Bar Chart - Kampagne- Sprache- Kampagne kaufreiz #############
				#st.write("Auswahl von interessanten Spalten")
				#Erst nur Auswahl interessanten Spalten
				df_Test_Kampagne_Sprache= df_CampaignCheckAuswertungsSelektion [['Kampagne','Sprache', 'Werbebeurteilung - Reizt mich, mehr zu erfahren']]
				#st.write(df_Test_Kampagne_Sprache)
				
				
				#st.write("hejhopp, här blir det nästan en longform-variant visst tror jag:")
				#st.write("Für altair wird  die longform-data bevorzugt.. umstellung kann mit melt gemacht werden")
				df_Kampagne_Sprache_Kaufreiz = df_Test_Kampagne_Sprache.groupby(['Kampagne', 'Sprache']).mean('Werbebeurteilung - Reizt mich, mehr zu erfahren')#['Werbebeurteilung - Reizt mich, mehr zu erfahren'].nlargest(10)
					
				df_Kampagne_Sprache_Kaufreiz = df_Kampagne_Sprache_Kaufreiz.reset_index(level=0)
				df_Kampagne_Sprache_Kaufreiz['Sprache'] = df_Kampagne_Sprache_Kaufreiz.index
				#st.write(df_Kampagne_Sprache_Kaufreiz)
				
					
				#Ploly-Variante #########
				Abb_kaufreiz_Kampagne_Sprache= px.bar(df_Kampagne_Sprache_Kaufreiz, 
				x="Kampagne",
				#y="Kampagne",  
				y="Werbebeurteilung - Reizt mich, mehr zu erfahren",
				#x="Werbebeurteilung - Reizt mich, mehr zu erfahren",
				color="Sprache",
				color_discrete_map={'Deutsch' : FARBE_Deutsch ,'Französisch' : FARBE_Französisch},
				text='Werbebeurteilung - Reizt mich, mehr zu erfahren', #beschriftung auf Balken
				hover_name='Kampagne', #Beschriftungstextauswahl für Balken 
				title=f'Werbebeurteilung - Reizt mich, mehr zu erfahren (1-7) - nach Sprache',
				orientation='v', #braucht es hier eigentlich nicht
				hover_data=['Werbebeurteilung - Reizt mich, mehr zu erfahren'],
				barmode = 'group')
				
				#Weitere Formatierungen der Abbildung
				Abb_kaufreiz_Kampagne_Sprache.update_traces(texttemplate='%{text:.2f}', textposition='inside')
				Abb_kaufreiz_Kampagne_Sprache.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
				Abb_kaufreiz_Kampagne_Sprache.update_yaxes(showline=True, linewidth=1, linecolor='white', gridcolor='black')
				Abb_kaufreiz_Kampagne_Sprache.update_yaxes(range=[1, 7])
				#Abb_kaufreiz_Kampagne_Sprache.update_xaxes(range=[1, 7])
				
				st.plotly_chart(Abb_kaufreiz_Kampagne_Sprache, use_container_width = True)
		

		
		######## Ende Abbildungen zu Werbebeurteilung - Reizt mich, mehr zu erfahren  ####################




		#Abbildungen - Verständlich je Kampagne - Durchschnittswerte ******************************************************************************************************************
		
		n_VerständlichKampagne = df_CampaignCheckAuswertungsSelektion.groupby('Kampagne').agg({'Werbebeurteilung - Ist verständlich':'mean'})['Werbebeurteilung - Ist verständlich']
		

		
		anzahlKampagneGesamt = len(n_VerständlichKampagne)
		
		if anzahlKampagneGesamt > 1:
			st.subheader("")
			st.subheader("Verständlichkeit der Werbemittel (1-7):")
		
			st.write("Anzahl Kampagnen zur Auswahl: ",anzahlKampagneGesamt)
		
			if anzahlKampagneGesamt > 10:
				minAnzahlKampagne = 10
			else:
				minAnzahlKampagne = anzahlKampagneGesamt
		
			if anzahlKampagneGesamt == 1:
				minAnzahlKampagne = 1
		
			top_VerständlichKampagne = st.slider('Wähle Anzahl anzuzeigende Kampagnen:', min_value=0, max_value=anzahlKampagneGesamt, value=minAnzahlKampagne)
			top_n_VerständlichKampagne = df_CampaignCheckAuswertungsSelektion.groupby('Kampagne').agg({'Werbebeurteilung - Ist verständlich':'mean'})['Werbebeurteilung - Ist verständlich'].nlargest(top_VerständlichKampagne)
		
			anzahlKampagne = len(top_n_VerständlichKampagne)
		
			Abbildung_top_n_VerständlichKampagne = px.bar(top_n_VerständlichKampagne, 
			x=top_n_VerständlichKampagne.index, 
			y='Werbebeurteilung - Ist verständlich',
			color='Werbebeurteilung - Ist verständlich',
			#color_continuous_scale=px.colors.sequential.Blackbody,
			#color_continuous_scale=px.colors.sequential.Brwnyl,
			#color=top_n_VerständlichKampagne.index - unterschiedliche Farbe je Kampagne
			text='Werbebeurteilung - Ist verständlich', #beschriftung auf Balken
			#hover_name='Werbebeurteilung - Ist verständlich', #Beschriftungstextauswahl für Balken
			title=f'Verständlich(1-7) je Kampagne - Top ' + str(top_VerständlichKampagne),
			orientation='v', #braucht es hier eigentlich nicht
			#color_continuous_scale=[(0, FARBE_Minwert),(0.25, FARBE_Mittelwert), (0.5, FARBE_Mittelwert), (0.75, FARBE_Maxwert),(1, FARBE_Maxwert)]
			color_continuous_scale=[(0, FARBE_Minwert), (0.5, FARBE_Mittelwert), (1, FARBE_Maxwert)]
			#color_continuous_scale[color_continuous_scale[0]] = "black"
			
			)
			#Weitere Formatierungen der Abbildung
			Abbildung_top_n_VerständlichKampagne.update_traces(texttemplate='%{text:.1f}', textposition='inside')
			Abbildung_top_n_VerständlichKampagne.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
			Abbildung_top_n_VerständlichKampagne.update_yaxes(showline=True, linewidth=1, linecolor='white', gridcolor='black')
			Abbildung_top_n_VerständlichKampagne.update_yaxes(range=[1, 7])
			
			#Horizontale Line mit Durchschnitt aller Messerwerte aus der DB
			Abbildung_top_n_VerständlichKampagne.add_hline(y=MittelwertKampagneVerständlich_Alle, line_width=5, line_dash="dot", line_color="grey", opacity=0.6, annotation_text="ø Alle Messwerte", 
		              annotation_position="top left", annotation_font_size=16,
		              annotation_font_color="grey")
		
			if MittelwertKampagneVerständlich_Alle != MittelwertKampagneVerständlich:
				Abbildung_top_n_VerständlichKampagne.add_hline(y=MittelwertKampagneVerständlich, line_width=2, line_dash="dot", line_color="white", opacity=0.8, annotation_text="ø Auswahl", 
		              annotation_position="top right")
		
		
			st.plotly_chart(Abbildung_top_n_VerständlichKampagne, use_container_width = True)








		# Abbildungen zu Werbebeurteilung der Kampagnen nach Soziodemographie- Ist verständlich (1-7) #################################
		
		#if anzahlUnternehmen == 1 or anzahlBranchen == 1:
		if my_UnternehmenSelect !=[] or my_BrancheSelect !=[]:
			VerständlichExpander = st.expander ('Verständlichkeit - Breaks nach Soziodemographie')
			with VerständlichExpander:
				st.subheader("")
				st.subheader("Verständlichkeit (1-7) nach Soziodemographie:")
			
				#Grouped Bar Chart - Kampagne- Geschlecht - Kampagne kaufreiz #############
				#st.write("Auswahl von interessanten Spalten")
				#Erst nur Auswahl interessanten Spalten
				df_Test_Kampagne_Geschlecht = df_CampaignCheckAuswertungsSelektion [['Kampagne','Geschlecht', 'Werbebeurteilung - Ist verständlich']]
				#st.write(df_Test_Kampagne_Geschlecht)
				
				
				#st.write("hejhopp, här blir det nästan en longform-variant visst tror jag:")
				#st.write("Für altair wird  die longform-data bevorzugt.. umstellung kann mit melt gemacht werden")
				df_Kampagne_Geschlecht_Verständlich = df_Test_Kampagne_Geschlecht.groupby(['Kampagne', 'Geschlecht']).mean('Werbebeurteilung - Ist verständlich')#['Werbebeurteilung - Ist verständlich'].nlargest(10)
					
				df_Kampagne_Geschlecht_Verständlich = df_Kampagne_Geschlecht_Verständlich.reset_index(level=0)
				df_Kampagne_Geschlecht_Verständlich['Geschlecht'] = df_Kampagne_Geschlecht_Verständlich.index
				#st.write(df_Kampagne_Geschlecht_Verständlich)
				
					
				#Ploly-Variante #########
				Abb_kaufreiz_Kampagne_Geschlecht = px.bar(df_Kampagne_Geschlecht_Verständlich, 
				x="Kampagne",
				#y="Kampagne",  
				y="Werbebeurteilung - Ist verständlich",
				#x="Werbebeurteilung - Ist verständlich",
				color="Geschlecht",
				color_discrete_map={'Frau' : FARBE_Frau ,'Mann' : FARBE_Mann},
				text='Werbebeurteilung - Ist verständlich', #beschriftung auf Balken
				hover_name='Kampagne', #Beschriftungstextauswahl für Balken 
				title=f'Werbebeurteilung - Ist verständlich (1-7)- nach Geschlecht ',
				orientation='v', #braucht es hier eigentlich nicht
				hover_data=['Werbebeurteilung - Ist verständlich'],
				barmode = 'group')
				
				#Weitere Formatierungen der Abbildung
				Abb_kaufreiz_Kampagne_Geschlecht.update_traces(texttemplate='%{text:.2f}', textposition='inside')
				Abb_kaufreiz_Kampagne_Geschlecht.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
				Abb_kaufreiz_Kampagne_Geschlecht.update_yaxes(showline=True, linewidth=1, linecolor='white', gridcolor='black')
				Abb_kaufreiz_Kampagne_Geschlecht.update_yaxes(range=[1, 7])
				#Abb_kaufreiz_Kampagne_Geschlecht.update_xaxes(range=[1, 7])
				
				st.plotly_chart(Abb_kaufreiz_Kampagne_Geschlecht, use_container_width = True)
	
			
			
			

			
				#Grouped Bar Chart - Kampagne- Altersklasse - Kampagne kaufreiz #############
				#st.write("Auswahl von interessanten Spalten")
				#Erst nur Auswahl interessanten Spalten
				df_Test_Kampagne_Altersklasse = df_CampaignCheckAuswertungsSelektion [['Kampagne','Altersklasse', 'Werbebeurteilung - Ist verständlich']]
				#st.write(df_Test_Kampagne_Altersklasse)
				
				
				#st.write("hejhopp, här blir det nästan en longform-variant visst tror jag:")
				#st.write("Für altair wird  die longform-data bevorzugt.. umstellung kann mit melt gemacht werden")
				df_Kampagne_Altersklasse_Verständlich = df_Test_Kampagne_Altersklasse.groupby(['Kampagne', 'Altersklasse']).mean('Werbebeurteilung - Ist verständlich')#['Werbebeurteilung - Ist verständlich'].nlargest(10)
					
				df_Kampagne_Altersklasse_Verständlich = df_Kampagne_Altersklasse_Verständlich.reset_index(level=0)
				df_Kampagne_Altersklasse_Verständlich['Altersklasse'] = df_Kampagne_Altersklasse_Verständlich.index
				#st.write(df_Kampagne_Altersklasse_Verständlich)
				
					
				#Ploly-Variante #########
				Abb_kaufreiz_Kampagne_Altersklasse = px.bar(df_Kampagne_Altersklasse_Verständlich, 
				x="Kampagne",
				#y="Kampagne",  
				y="Werbebeurteilung - Ist verständlich",
				#x="Werbebeurteilung - Ist verständlich",
				color="Altersklasse",
				color_discrete_map={'16-29' : FARBE_16_29 ,'30-49' : FARBE_30_49,'50+' : FARBE_50plus},
				text='Werbebeurteilung - Ist verständlich', #beschriftung auf Balken
				hover_name='Kampagne', #Beschriftungstextauswahl für Balken 
				title=f'Werbebeurteilung - Ist verständlich (1-7) - nach Altersklasse ',
				orientation='v', #braucht es hier eigentlich nicht
				hover_data=['Werbebeurteilung - Ist verständlich'],
				barmode = 'group')
				
				#Weitere Formatierungen der Abbildung
				Abb_kaufreiz_Kampagne_Altersklasse.update_traces(texttemplate='%{text:.2f}', textposition='inside')
				Abb_kaufreiz_Kampagne_Altersklasse.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
				Abb_kaufreiz_Kampagne_Altersklasse.update_yaxes(showline=True, linewidth=1, linecolor='white', gridcolor='black')
				Abb_kaufreiz_Kampagne_Altersklasse.update_yaxes(range=[1, 7])
				#Abb_kaufreiz_Kampagne_Altersklasse.update_xaxes(range=[1, 7])
				
				st.plotly_chart(Abb_kaufreiz_Kampagne_Altersklasse, use_container_width = True)
			
			

			
				#Grouped Bar Chart - Kampagne- Sprache- Kampagne kaufreiz #############
				#st.write("Auswahl von interessanten Spalten")
				#Erst nur Auswahl interessanten Spalten
				df_Test_Kampagne_Sprache= df_CampaignCheckAuswertungsSelektion [['Kampagne','Sprache', 'Werbebeurteilung - Ist verständlich']]
				#st.write(df_Test_Kampagne_Sprache)
				
				
				#st.write("hejhopp, här blir det nästan en longform-variant visst tror jag:")
				#st.write("Für altair wird  die longform-data bevorzugt.. umstellung kann mit melt gemacht werden")
				df_Kampagne_Sprache_Verständlich = df_Test_Kampagne_Sprache.groupby(['Kampagne', 'Sprache']).mean('Werbebeurteilung - Ist verständlich')#['Werbebeurteilung - Ist verständlich'].nlargest(10)
					
				df_Kampagne_Sprache_Verständlich = df_Kampagne_Sprache_Verständlich.reset_index(level=0)
				df_Kampagne_Sprache_Verständlich['Sprache'] = df_Kampagne_Sprache_Verständlich.index
				#st.write(df_Kampagne_Sprache_Verständlich)
				
					
				#Ploly-Variante #########
				Abb_kaufreiz_Kampagne_Sprache= px.bar(df_Kampagne_Sprache_Verständlich, 
				x="Kampagne",
				#y="Kampagne",  
				y="Werbebeurteilung - Ist verständlich",
				#x="Werbebeurteilung - Ist verständlich",
				color="Sprache",
				color_discrete_map={'Deutsch' : FARBE_Deutsch ,'Französisch' : FARBE_Französisch},
				text='Werbebeurteilung - Ist verständlich', #beschriftung auf Balken
				hover_name='Kampagne', #Beschriftungstextauswahl für Balken 
				title=f'Werbebeurteilung - Ist verständlich (1-7) - nach Sprache',
				orientation='v', #braucht es hier eigentlich nicht
				hover_data=['Werbebeurteilung - Ist verständlich'],
				barmode = 'group')
				
				#Weitere Formatierungen der Abbildung
				Abb_kaufreiz_Kampagne_Sprache.update_traces(texttemplate='%{text:.2f}', textposition='inside')
				Abb_kaufreiz_Kampagne_Sprache.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
				Abb_kaufreiz_Kampagne_Sprache.update_yaxes(showline=True, linewidth=1, linecolor='white', gridcolor='black')
				Abb_kaufreiz_Kampagne_Sprache.update_yaxes(range=[1, 7])
				#Abb_kaufreiz_Kampagne_Sprache.update_xaxes(range=[1, 7])
				
				st.plotly_chart(Abb_kaufreiz_Kampagne_Sprache, use_container_width = True)
		

		
		######## Ende Abbildungen zu Werbebeurteilung - Ist verständlich  ####################
		
		
		
		
		
		
		
		
		
		_="""
		#Grouped Bar Chart - UG - Geschlecht - Kampagne glaubwürdig #############
		#st.write("Auswahl von interessanten Spalten")
		#Erst nur Auswahl interessanten Spalten
		df_Test_UG_Geschlecht = df_CampaignCheckAuswertungsSelektion [['Unternehmen','Geschlecht', 'Werbebeurteilung - Ist glaubwürdig']]
		#st.write(df_Test_UG_Geschlecht)
		
		
		#st.write("hejhopp, här blir det nästan en longform-variant visst tror jag:")
		#st.write("Für altair wird  die longform-data bevorzugt.. umstellung kann mit melt gemacht werden")
		df_UG_Geschlecht_Glaubwürdig = df_Test_UG_Geschlecht.groupby(['Unternehmen', 'Geschlecht']).mean('Werbebeurteilung - Ist glaubwürdig')#['Werbebeurteilung - Ist glaubwürdig'].nlargest(10)
			
		df_UG_Geschlecht_Glaubwürdig = df_UG_Geschlecht_Glaubwürdig.reset_index(level=0)
		df_UG_Geschlecht_Glaubwürdig['Geschlecht'] = df_UG_Geschlecht_Glaubwürdig.index
		#st.write(df_UG_Geschlecht_Glaubwürdig)
		
			
		#Ploly-Variante #########
		Abb_glaubwürdig_UG_Geschlecht = px.bar(df_UG_Geschlecht_Glaubwürdig, 
		#x="Unternehmen",
		y="Unternehmen",  
		#y="Werbebeurteilung - Ist glaubwürdig",
		x="Werbebeurteilung - Ist glaubwürdig",
		color="Geschlecht",
		color_discrete_map={'Frau' : FARBE_Minwert ,'Mann' : FARBE_Maxwert},
		text='Werbebeurteilung - Ist glaubwürdig', #beschriftung auf Balken
		hover_name='Unternehmen', #Beschriftungstextauswahl für Balken 
		title=f'Werbebeurteilung je Unternehmen - Ist glaubwürdig (1-7) - nach Geschlecht ',
		orientation='h', #braucht es hier eigentlich nicht
		hover_data=['Werbebeurteilung - Ist glaubwürdig'],
		barmode = 'group')
		
		#Weitere Formatierungen der Abbildung
		Abb_glaubwürdig_UG_Geschlecht.update_traces(texttemplate='%{text:.2f}', textposition='inside')
		Abb_glaubwürdig_UG_Geschlecht.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
		Abb_glaubwürdig_UG_Geschlecht.update_yaxes(showline=True, linewidth=1, linecolor='white', gridcolor='black')
		#Abb_glaubwürdig_UG_Geschlecht.update_yaxes(range=[1, 10])
		Abb_glaubwürdig_UG_Geschlecht.update_xaxes(range=[1, 7])
		
		st.plotly_chart(Abb_glaubwürdig_UG_Geschlecht)
		"""

		
		_="""
		#Tabelle mit Breaks
		#Erst nur Auswahl interessanten Spalten
		df_Kampagne_Glaubwürdig_Geschlecht = df_CampaignCheckAuswertungsSelektion [['Kampagne','Geschlecht','Werbebeurteilung - Ist glaubwürdig']]

		st.write("")
		st.write("Tabelle - Werbebeurteilung je Kampagne nach Geschlecht - ist Glaubwürdig (1-7)")
		Kampagne_Glaubwürdig_Geschlecht_Tabelle = df_Kampagne_Glaubwürdig_Geschlecht.pivot_table('Werbebeurteilung - Ist glaubwürdig', ['Kampagne'],'Geschlecht')
		#rearranged['Unternehmen'] = rearranged.index
		Kampagne_Glaubwürdig_Geschlecht_Tabelle = Kampagne_Glaubwürdig_Geschlecht_Tabelle.reset_index(level=0)
		#rearranged['Mittelwert'] = (rearranged['Frau'] + rearranged['Mann']) * 0.5
		st.write(Kampagne_Glaubwürdig_Geschlecht_Tabelle)

		#Ytterligare försök
		st.write("px bar chart som visar i perfekt uppställning, dock med summa istället för medelvärde...")
		fig = px.bar(df_CampaignCheckAuswertungsSelektion, x="Unternehmen", y=('Werbebeurteilung - Ist glaubwürdig'), color="Geschlecht", hover_data=['Werbebeurteilung - Ist glaubwürdig'],barmode ='group')
		st.plotly_chart(fig, use_container_width = True)

		"""
		

		
		
############################################################################################	
#Media Effects ############################################################################
############################################################################################	

	if KPIAuswahl == "Media Effects":
		
		placeholder.empty()
		
		
		df_CampaignCheckAuswertungsSelektion['Anzahl Kontakte Andere'] = df_CampaignCheckAuswertungsSelektion['Anzahl Kontakte Andere'].fillna(0)
		df_CampaignCheckAuswertungsSelektion['Anzahl Kontakte Omnet'] = df_CampaignCheckAuswertungsSelektion['Anzahl Kontakte Omnet'].fillna(0)
		
		#Gesamtkontakte Online
		df_CampaignCheckAuswertungsSelektion['Online-Kontake Gesamt'] = df_CampaignCheckAuswertungsSelektion['Anzahl Kontakte Omnet'] + df_CampaignCheckAuswertungsSelektion['Anzahl Kontakte Andere']
		
		
		
		#Dataframe mit ausgewählten Kampagnen-Variablen
		df_Kampagnen = df_CampaignCheckAuswertungsSelektion.groupby(['Unternehmen','Kampagne','GetestetesWerbeMedium']).agg({'Recognition_Wert':['mean'],'Werbebeurteilung - Gefällt mir':['mean'],'Werbebeurteilung - Ist etwas Besonderes':['mean'],'Werbebeurteilung - Ist glaubwürdig':['mean'],'Werbebeurteilung - Ist verständlich':['mean'],'Werbebeurteilung - Reizt mich, mehr zu erfahren':['mean'],'Kauf (KDA Outcome)':['mean'],'NPS':['mean'],'Anzahl Kontakte Omnet':['mean'],'Anzahl Kontakte Andere':['mean'],'Online-Kontake Gesamt':['mean']}) 
		
		# rename columns
		df_Kampagnen.columns = ['Recognition - Mittelwert (%)', 'Kampagne gefällt (1-7)', 'Kampagne besonders (1-7)', 'Kampagne glaubwürdig (1-7)', 'Kampagne verständlich (1-7)', 'Kampagne kaufreiz (1-7)', 'KDA (1-7)', 'NPS (0-10)', 'Omnet-Kontakte Mittelwert', 'Kontakte andere Netzwerke - Mittelwert', 'Onlinekontake Gesamt (Omnet und Andere) - Mittelwert']
		
		
		# reset index to get grouped columns back
		df_Kampagnen = df_Kampagnen.reset_index()
		
		
		n_RecognitionKampagne = df_CampaignCheckAuswertungsSelektion.groupby('Kampagne').agg({'Recognition_Wert':'mean'})['Recognition_Wert']
		anzahlKampagneGesamt = len(n_RecognitionKampagne)
		
		
		KampagnenAuswahleExpander = st.expander("Tabelle mit den ø-Werten der einzelnen Kampagnen")
		with KampagnenAuswahleExpander:

			speicherZeitpunkt = pd.to_datetime('today')
			st.write("")
			st.write(df_Kampagnen)
			st.write("")
			if len(df_Kampagnen) > 0:					
				def to_excel(df_Kampagnen):
					output = BytesIO()
					writer = pd.ExcelWriter(output, engine='xlsxwriter')
					df_Kampagnen.to_excel(writer, index=False, sheet_name='Sheet1')
					workbook = writer.book
					worksheet = writer.sheets['Sheet1']
					format1 = workbook.add_format({'num_format': '0.00'}) 
					worksheet.set_column('A:A', None, format1)  
					writer.save()
					processed_data = output.getvalue()
					return processed_data
				df_xlsx = to_excel(df_Kampagnen)
				st.download_button(label='📥 Tabelle in Excel abspeichern?',
					data=df_xlsx ,
					file_name= 'CCC_DES_Benchmarks_Kampagnenwerte_Tabellenexport '+str(speicherZeitpunkt) +'.xlsx' )
					
					
		if anzahlKampagneGesamt > 1:
			#Abbildung - Recognition je GetestetesWerbemedium******************************************************************************************************************
			
			
			
			n_RecognitionGetestetesWerbemedium = df_CampaignCheckAuswertungsSelektion.groupby('GetestetesWerbeMedium').agg({'Recognition_Wert':'mean'})['Recognition_Wert']
			
	
			
			#n_RecognitionGetestetesWerbemedium = n_RecognitionGetestetesWerbemedium.reset_index(level=0)
			#AnzahlGetesteteWerbeMedien  = n_RecognitionGetestetesWerbemedium['GetestetesWerbeMedium'].value_counts() 
			
			
			#Ohne Online und OOH - weil nur ein Messwert!
			top_n_RecognitionGetestetesWerbemedium = n_RecognitionGetestetesWerbemedium.reset_index(level=0)
			#top_n_RecognitionGetestetesWerbemedium['GetestetesWerbeMedium'] = top_n_RecognitionGetestetesWerbemedium['index']
			top_n_RecognitionGetestetesWerbemedium = top_n_RecognitionGetestetesWerbemedium.loc[top_n_RecognitionGetestetesWerbemedium['GetestetesWerbeMedium'] != "Online und OOH"]
	
			
	
			
			Abbildung_top_n_RecognitionGetestetesWerbemedium = px.bar(top_n_RecognitionGetestetesWerbemedium, 
			x='GetestetesWerbeMedium', 
			y='Recognition_Wert',
			color='Recognition_Wert',
			#color_continuous_scale=px.colors.sequential.Blackbody,
			#color_continuous_scale=px.colors.sequential.Brwnyl,
			#color=top_n_RecognitionGetestetesWerbemedium.index, #- unterschiedliche Farbe je GetestetesWerbemedium
			text='Recognition_Wert', #beschriftung auf Balken
			hover_name='GetestetesWerbeMedium', #Beschriftungstextauswahl für Balken
			title=f'Recognition nach getestetem Werbemedium',
			orientation='v', #braucht es hier eigentlich nicht
			color_continuous_scale=[(0, FARBE_Minwert), (0.5, FARBE_Mittelwert), (1, FARBE_Maxwert)]
			)
			
			#Weitere Formatierungen der Abbildung
			Abbildung_top_n_RecognitionGetestetesWerbemedium.update_traces(texttemplate='%{text:.1f}'+" %", textposition='inside')
			Abbildung_top_n_RecognitionGetestetesWerbemedium.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
			Abbildung_top_n_RecognitionGetestetesWerbemedium.update_yaxes(showline=True, linewidth=1, linecolor='white', gridcolor='black')
		
			st.plotly_chart(Abbildung_top_n_RecognitionGetestetesWerbemedium, use_container_width = True)	
		
			#Fallzahl - Anzahl getestete Werbemittel je Medium/Kombo
			AnzahlGetesteteWerbeMedien  = df_Kampagnen['GetestetesWerbeMedium'].value_counts()
			AnzahlGetesteteWerbeMedien = AnzahlGetesteteWerbeMedien.reset_index(level=0)
			AnzahlGetesteteWerbeMedien.rename(columns={'index' : 'Werbmedien(-Kombo)','GetestetesWerbeMedium' : 'Anzahl getestete Kampagnen'},inplace=True) 
			AnzahlGetesteteWerbeMedien = AnzahlGetesteteWerbeMedien.set_index('Werbmedien(-Kombo)').T
			st.write(AnzahlGetesteteWerbeMedien)
		
			#AnzahlGetesteteWerbeMedienAlsString = AnzahlGetesteteWerbeMedien.astype('string')
			#st.write(AnzahlGetesteteWerbeMedienAlsString)
			
			
			##################################################################################################################################################	
	
	
	
			#Abbildung Punktediagramme - gemessene Onlinekontakte und Recognition ######################################
			
			
			#gemessene Onlinekontakte pro Kampagne 
			
			import altair as alt
			
			df_KampagnenMitOnlineKontakten = df_Kampagnen[df_Kampagnen['Onlinekontake Gesamt (Omnet und Andere) - Mittelwert'] > 0]
			
			df_AltairTest = df_KampagnenMitOnlineKontakten
			
			Abbildung_Kampagnen_OLKontakte_Recognition = alt.Chart(df_AltairTest).mark_circle().encode(
			x='Onlinekontake Gesamt (Omnet und Andere) - Mittelwert', y='Recognition - Mittelwert (%)', size='Recognition - Mittelwert (%)', color='Recognition - Mittelwert (%)', tooltip=['Kampagne', 'Recognition - Mittelwert (%)', 'Onlinekontake Gesamt (Omnet und Andere) - Mittelwert'])
		
			st.altair_chart(Abbildung_Kampagnen_OLKontakte_Recognition, use_container_width=True)
			
			_="""
			#Abbildung Punktediagramme - gemessene Onlinekontakte und Kaufreiz ######################################
				
			Abbildung_Kampagnen_OLKontakte_Kaufreiz = alt.Chart(df_AltairTest).mark_circle().encode(
			x='Onlinekontake Gesamt (Omnet und Andere) - Mittelwert', y='Kampagne kaufreiz (1-7)', size='Recognition - Mittelwert (%)', color='Kampagne kaufreiz (1-7)', tooltip=['Kampagne', 'Kampagne kaufreiz (1-7)', 'Onlinekontake Gesamt (Omnet und Andere) - Mittelwert'])
		
			st.altair_chart(Abbildung_Kampagnen_OLKontakte_Kaufreiz, use_container_width=True)			
			"""
			
			
			
			
			
			
			_="""
			#gemessene Onlinekontakte pro Person, na ja ...
			df_CampaignCheckAuswertungsSelektion['Anzahl Kontakte Andere'] = df_CampaignCheckAuswertungsSelektion['Anzahl Kontakte Andere'].fillna(0)
			df_CampaignCheckAuswertungsSelektion['Anzahl Kontakte Omnet'] = df_CampaignCheckAuswertungsSelektion['Anzahl Kontakte Omnet'].fillna(0)
		
			#Gemessene Onlinekontakte pro Person
			df_BefragteMitOnlineKontakten = df_CampaignCheckAuswertungsSelektion
			
			#Gesamtkontakte Online
			df_BefragteMitOnlineKontakten['Online-Kontakte Gesamt - gemessen'] = df_BefragteMitOnlineKontakten['Anzahl Kontakte Omnet'] + df_BefragteMitOnlineKontakten['Anzahl Kontakte Andere']
			df_BefragteMitOnlineKontakten = df_BefragteMitOnlineKontakten[df_BefragteMitOnlineKontakten['Online-Kontake Gesamt - gemessen'] > 0]
			
			st.write(df_BefragteMitOnlineKontakten)
			
			Abbildung_Befragte_OLKontakte_Recognition = alt.Chart(df_BefragteMitOnlineKontakten).mark_circle().encode(
			x='Online-Kontakte Gesamt - gemessen', y='Recognition - Mittelwert (%)', size='Recognition - Mittelwert (%)', color='Recognition - Mittelwert (%)', tooltip=['Kampagne', 'Recognition - Mittelwert (%)', 'Onlinekontake Gesamt (Omnet und Andere) - Mittelwert'])
		
			st.altair_chart(Abbildung_Befragte_OLKontakte_Recognition, use_container_width=True)
			"""