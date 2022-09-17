
import csv
import xlsxwriter
from index import * 

class Rank:

    def __init__(self, pitchbook, specter) -> None:
        """
        This is the constructor for the rank class. It sorts through the dictionary of companies to scores from the indexer class, 
        ranking them from highest to lowest. This ranking of the top quartile of companies is then written to an xlsx file. 

        Parameters: 
        None 

        Returns: 
        None 
        """
        self.pitch_csv = pitchbook
        self.specter_csv = specter
        self.rank_companies()
        self.write_to_xlsx()
    
    def rank_companies(self): 
        """
        This methods ranks the companies acquired from the indexer file, allowing for this ranking to then be written to the 
        relevant file. 

        Parameters: 
        None 

        Returns: 
        None 
        """
        self.index = Index(self.pitch_csv, self.specter_csv) #create an instance of the index class 

        # sort the dictionaries into an enumerate 
        self.ranked_list = self.sort_dict(self.index.company_to_score)
        self.early_ranked_list = self.sort_dict(self.index.early_stage_to_score)

    def sort_dict(self, ranking : dict) -> enumerate: 
        """
        Helper method to sort the dictionary of companies based on the score values, and returns an enumerate containing only the 
        top quartile of companies 

        Paramters: 
        ranking --- dict of companies to be ranked 

        Returns: 
        enumerate --- tuples of ranking and company 
        """
        n = len(ranking.keys())
        first_quartile = int(n/4) if (n/4).is_integer() else int(n/4) + 1 #calculating the first quartile 

        ranked = sorted(ranking.items(), key = lambda x:x[1], reverse=True)[0:first_quartile] #sorting list based on values 
        return enumerate([x[0] for x in ranked], 1) 

    def write_to_xlsx(self): 
        """
        This method writes the xlsx file with the ranked companies. 

        Parameters: 
        None 

        Returns:
        None 
        """
        workbook = xlsxwriter.Workbook('Ranking.xlsx') #creating the workbook 
        worksheet = workbook.add_worksheet('Full Ranking')
        worksheet2 = workbook.add_worksheet('Early Stage Ranking')

        self.fill_cells(self.ranked_list, worksheet)
        self.fill_cells(self.early_ranked_list, worksheet2)
        
        workbook.close() #close the workbook once done editing 
    
    def fill_cells(self, ranking : enumerate, worksheet):
        """
        This method fills the cells of the spreadsheet with the relevent information for the ranked companies. 

        Parameters: 
        ranking --- enumerate of ranked companies 
        worksheet --- the worksheet to be edited 

        Returns: 
        None 
        """
        num_to_row = {} #initialize dictionary mapping row number to row contents 

        with open('pitchbook-data.csv', 'r', encoding='utf-8-sig') as raw: 
            reader = csv.reader(raw) #read pitchbook data
            headers = next(reader) #extract header 

            for n, row in enumerate(reader): #populate dictionary of row number to row contents 
                num_to_row[n] = row

            for c1, header in enumerate(headers): #write the header 
                worksheet.write(0, c1, header)
                
            for r, company in ranking: #for each of the ranked companies 
                row_num = self.index.company_to_row[company] #access the relevant row number corresponding to company 
                for c, col in enumerate(num_to_row[row_num]): #for each cell of csv file 
                    worksheet.write(r, c, col)


if __name__ == "__main__":
    if len(sys.argv) != 3: 
        raise Exception("Invalid input. Try Again.")
    else: 
        Rank(sys.argv[1], sys.argv[2])      