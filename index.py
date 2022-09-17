import csv
import sys

class Index: 


    def __init__(self, pitchbook, specter) -> None:
        """
        This is the constructor for the indexer class, in which data from the relevant sources is extracted and processed. A final dictionary is created which 
        associates a company with a score based on its investors and any located talent signals. 

        Parameters: 
        None 

        Returns:
        None 
        """
        self.pitch_filepath = pitchbook
        self.specter_filepath = specter
        self.initialize_vars()
        self.extract_data()
        self.get_score(self.company_to_score)
        self.get_score(self.early_stage_to_score)

    def initialize_vars(self) -> None: 
        """
        This method initializes the company to score dictionary which is used for the ranking, as well as the lists which contain
        the different tiers of investors. 

        Paramters: 
        None
        
        Returns: 
        None 
        """
        #initialize dictionaries 
        self.company_to_row = {}
        self.company_to_score = {}
        self.early_stage_to_score = {}

        #initialize list of relevant investors 
        self.top_investors = ["Y Combinator", "Andreessen Horowitz", "Sequoia Capital"]
        self.tier_1_investors = ["Swisscom Ventures", "Redalpine Venture Partners", "HV Capital", "Wingman Ventures", 
        "btov Partners", "Lakestar", "VI Partners", "Techstars", "EPFL Innovation Park", "Global Founders Capital"]
        self.tier_2_investors = ["F10", "Venture Kick", "EIC Accelerator", "Fongit", "ESA BIC Switzerland", 
        "Fondation pour l'Innovation Technologique"]

    def extract_data(self) -> None:
        """
        This method extracts the data from the relevant csv files, by adding the companies to the relevant data structures, allowing this
        data to then be further processed. 

        Parameters: 
        None 

        Returns: 
        None 
        """
        # initalizing the dictionaries 
        self.pitch_companies = {}
        self.specter_companies = {} 

        with open(self.pitch_filepath, 'r', encoding='utf-8-sig') as raw: #reading the pitchbook csv file 
            reader_object = csv.DictReader(raw)

            for r, row in enumerate(reader_object): 
                company = self.split_position(row['Companies']) #extract company name 
                self.company_to_row[company] = r
                self.pitch_companies[company] = row['Active Investors'].split(", ") #splitting the active investors into a list 
                self.company_to_score[company] = 0 # initializing the values in the dictionary to 0 
                if row['Last Financing Size'] == '' or int(float(row['Last Financing Size'])) <= 15.00: 
                    self.early_stage_to_score[company] = 0 

        with open(self.specter_filepath, 'r') as raw2: #reading the specter csv file 
            reader2_object = csv.DictReader(raw2)
            
            for row in reader2_object: 
                score = int(row['Signal Score']) #cast the signal score to an int 
                company = self.split_position(row['New Position']) #process the position into company name 
                self.specter_companies[company] = score #populate dictionary 
                # if contains YC in tags
                if any("YC" in string for string in row['Tags'].split(", ")) and company in self.pitch_companies.keys(): 
                    self.company_to_score[company] = 30 
                    if company in self.early_stage_to_score.keys(): 
                        self.early_stage_to_score[company] = 30 
    

    def split_position(self, pos : str) -> str:
        """
        This is a recursive method which checks for the special characters of colons, pipes and brackets, as well as any extra characters 
        to allow the position to be processed effectively into a company name. 

        Parameters: 
        pos --- string corresponding to the position to be processed 

        Returns: 
        str --- corresponding to the processed data 
        """
        if ":" not in pos and "|" not in pos and "(" not in pos: #base case: no special characters
            return pos.replace(" AG", "").replace(" SA", "").strip() #remove extra characters and spaces 
        else: #else, split on the special character 
            if ":" in pos: 
                return self.split_position(pos.split(":")[0])
            if "|" in pos: 
                return self.split_position(pos.split("|")[0])
            if "(" in pos:
                return self.split_position(pos.split("(")[0])
    
                
    def get_score(self, data : dict): 
        """
        This method calculates the score for a given company by taking into account the nature of the investor and the signals outputted
        by specter. This score populates the dictionary, associating the company with the score. 

        Parameters: 
        dict --- the dictionary of companies for which we intend to calculate the score of  

        Returns: 
        None 
        """
        for company in data.keys(): 
            if any(investor in self.pitch_companies[company] for investor in self.top_investors): #if contains any top investor 
             data[company] = 30
            else: 
                if any(investor in self.pitch_companies[company] for investor in self.tier_2_investors): # if contains any tier 2 investors 
                 data[company] = 7
                    
                tier1 = sum(el in self.pitch_companies[company] for el in self.tier_1_investors) # calculate number of tier 1 investors 
                if tier1 ==  1: #one tier 1 investor
                 data[company] = 8 
                if tier1 >= 2: #2 or more tier 1 investors 
                 data[company] = 9
                
                if company in self.specter_companies.keys() and data[company] != 30: #if a signal for this company was picked up by specter 
                 data[company] = data[company]*0.5 + self.specter_companies[company]*0.5


if __name__ == "__main__":
    if len(sys.argv) != 3: 
        raise Exception("Invalid input. Try Again.")
    else: 
        Index(sys.argv[1], sys.argv[2])